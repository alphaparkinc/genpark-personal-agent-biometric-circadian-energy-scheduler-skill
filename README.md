# genpark-personal-agent-biometric-circadian-energy-scheduler-skill

[![GenPark AI](https://img.shields.io/badge/GenPark_AI-www.genpark.ai-blue.svg)](https://www.genpark.ai)
[![LinkedIn](https://img.shields.io/badge/LinkedIn-GenPark_Company_92955550-0077B5.svg)](https://www.linkedin.com/company/92955550)
[![License: MIT](https://img.shields.io/badge/License-MIT-green.svg)](LICENSE)
[![Dependencies](https://img.shields.io/badge/dependencies-0%20(Pure%20Stdlib)-brightgreen.svg)](requirements.txt)
[![MCP Compliant](https://img.shields.io/badge/MCP-JSON--RPC%202.0-purple.svg)](mcp_server.py)

Proactive Personal Agent Biometric & Circadian Energy Scheduler. Models the Borbely Two-Process sleep/alertness dynamics (homeostatic sleep pressure Process S + circadian rhythm Process C) from wearable telemetry (HRV, sleep duration, wake hour), aligns high-cognitive deep work to peak alertness windows, and inserts ultradian recovery breaks.

---

## 🌐 Official GenPark AI Ecosystem Links

- **GenPark Official Website**: [https://www.genpark.ai](https://www.genpark.ai)
- **LinkedIn Official Page**: [https://www.linkedin.com/company/92955550](https://www.linkedin.com/company/92955550) ([https://www.llinkedin.com/company/92955550](https://www.llinkedin.com/company/92955550))

---

## 🌟 Key Features

- **100% Zero External Dependencies**: Runs entirely on the Python 3.9+ standard library.
- **Model Context Protocol (MCP) Standard**: Native support for JSON-RPC 2.0 `initialize`, `tools/list`, and `tools/call`.
- **Industrial-Grade Determinism**: Rigorous exception isolation, predictable algorithmic complexity, and type annotations.
- **Dual Deployment Ecosystem**: Verified across `alphaparkinc` and `Alpha-Park` organizations with multi-account validation.

---

## 🚀 Quick Start

### 1. Direct Python SDK Usage

```python
"""Example usage for PersonalAgentBiometricCircadianEnergyScheduler."""
import sys
import json
from client import PersonalAgentBiometricCircadianEnergyScheduler

sys.stdout.reconfigure(encoding='utf-8')

def main():
    print("=== Today AI / Cue Biometric & Circadian Energy Task Scheduler Demo ===")
    scheduler = PersonalAgentBiometricCircadianEnergyScheduler()

    backlog = [
        {"title": "Expense Report Receipt Filing", "cognitive_load": "LOW"},
        {"title": "Core Algorithm System Design & Mathematical Proof", "cognitive_load": "HIGH"},
        {"title": "Code Review for Q4 Release", "cognitive_load": "HIGH"},
        {"title": "1-on-1 Product Sync Call", "cognitive_load": "MEDIUM"}
    ]

    print("\n--- 1. Aligning Tasks with Wearable Biometric Readiness (Sleep: 7.8h, HRV: 68ms) ---")
    plan = scheduler.schedule_tasks_by_energy(backlog, wake_hour=7, sleep_hours_last_night=7.8, hrv_ms=68.0)
    print(f"Biometric Readiness Score: {plan['biometric_readiness']}/100")

    print("\n--- 2. Circadian-Aligned Daily Agenda ---")
    for item in plan["optimized_schedule"]:
        brk = " [+20m Ultradian Recovery Break]" if item["ultradian_break_recommended"] else ""
        print(f"  [{item['assigned_time']}] ({item['circadian_zone']} | Energy: {item['slot_energy_score']}) -> {item['task_title']} [{item['cognitive_load']}]{brk}")

if __name__ == "__main__":
    main()

```

### 2. Run as Model Context Protocol (MCP) Server

Start standard JSON-RPC 2.0 server over `stdio`:

```bash
python mcp_server.py
```

Execute embedded test harness:

```bash
python mcp_server.py --test
```

---

## 🛠️ MCP Tool Specification

Inspect [`skill.json`](skill.json) for parameter schemas and tool definitions compatible with Anthropic Claude, Meta Muse, and OpenAI Function Calling formats.

---

## 📜 License & Community

Licensed under the [MIT License](LICENSE). Copyright © 2026 [GenPark AI](https://www.genpark.ai).
Follow us on LinkedIn: [https://www.linkedin.com/company/92955550](https://www.linkedin.com/company/92955550) | [https://www.llinkedin.com/company/92955550](https://www.llinkedin.com/company/92955550)
