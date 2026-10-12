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
