"""MCP Server for Personal Agent Biometric Circadian Energy Scheduler."""
import sys
import json
import time
from client import PersonalAgentBiometricCircadianEnergyScheduler

scheduler = PersonalAgentBiometricCircadianEnergyScheduler()

def handle_call_tool(params):
    name = params.get("name")
    args = params.get("arguments", {})
    if name != "schedule_by_circadian_energy":
        raise ValueError(f"Unknown tool: {name}")

    action = args.get("action", "schedule_tasks_by_energy")
    wake = int(args.get("wake_hour", 7))
    sleep_h = float(args.get("sleep_hours_last_night", 7.5))
    hrv = float(args.get("hrv_ms", 65.0))

    if action == "compute_hourly_energy_curve":
        return scheduler.compute_hourly_energy_curve(wake, sleep_h, hrv)
    elif action == "schedule_tasks_by_energy":
        tasks = args.get("tasks", [])
        return scheduler.schedule_tasks_by_energy(tasks, wake, sleep_h, hrv)
    else:
        raise ValueError(f"Invalid action: {action}")

def main():
    if len(sys.argv) > 1 and sys.argv[1] == "--test":
        print("Running self-test...")
        tasks = [
            {"title": "Clear Routine Promotional Emails", "cognitive_load": "LOW"},
            {"title": "Architect Distributed BFT Consensus Engine", "cognitive_load": "HIGH"},
            {"title": "Team Weekly Status Standup", "cognitive_load": "MEDIUM"}
        ]
        res = scheduler.schedule_tasks_by_energy(tasks, wake_hour=7, sleep_hours_last_night=8.0, hrv_ms=72.0)
        assert res["total_scheduled_tasks"] == 3
        high_task = [t for t in res["optimized_schedule"] if t["cognitive_load"] == "HIGH"][0]
        low_task = [t for t in res["optimized_schedule"] if t["cognitive_load"] == "LOW"][0]
        assert high_task["slot_energy_score"] > low_task["slot_energy_score"]
        print("Self-test PASSED!")
        sys.exit(0)

    for line in sys.stdin:
        line = line.strip()
        if not line:
            continue
        try:
            req = json.loads(line)
            msg_id = req.get("id")
            method = req.get("method")
            if method == "initialize":
                resp = {
                    "jsonrpc": "2.0",
                    "id": msg_id,
                    "result": {
                        "protocolVersion": "2024-11-05",
                        "serverInfo": {"name": "PersonalAgentBiometricCircadianEnergyScheduler", "version": "1.0.0"},
                        "capabilities": {"tools": {}}
                    }
                }
            elif method == "tools/list":
                resp = {
                    "jsonrpc": "2.0",
                    "id": msg_id,
                    "result": {
                        "tools": [{
                            "name": "schedule_by_circadian_energy",
                            "description": "Compute hourly cognitive alertness curve from sleep/HRV telemetry and assign tasks to optimal circadian energy slots.",
                            "inputSchema": {
                                "type": "object",
                                "properties": {
                                    "action": {"type": "string", "enum": ["compute_hourly_energy_curve", "schedule_tasks_by_energy"]},
                                    "wake_hour": {"type": "integer"},
                                    "sleep_hours_last_night": {"type": "number"},
                                    "hrv_ms": {"type": "number"},
                                    "tasks": {"type": "array"}
                                },
                                "required": ["action"]
                            }
                        }]
                    }
                }
            elif method == "tools/call":
                res = handle_call_tool(req.get("params", {}))
                resp = {
                    "jsonrpc": "2.0",
                    "id": msg_id,
                    "result": {"content": [{"type": "text", "text": json.dumps(res, indent=2)}]}
                }
            else:
                resp = {"jsonrpc": "2.0", "id": msg_id, "result": {}}
            print(json.dumps(resp), flush=True)
        except Exception as e:
            err_resp = {"jsonrpc": "2.0", "id": None, "error": {"code": -32000, "message": str(e)}}
            print(json.dumps(err_resp), flush=True)

if __name__ == "__main__":
    main()
