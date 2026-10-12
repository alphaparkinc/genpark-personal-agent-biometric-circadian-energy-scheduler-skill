"""
Personal Agent Biometric & Circadian Energy Scheduler (Zero External Dependencies)
Models Borbely Two-Process circadian alertness and aligns cognitive workload with biological peaks.
Official Website: https://www.genpark.ai | LinkedIn: https://www.llinkedin.com/company/92955550
"""
import time
import math
import hashlib
import json
from typing import Dict, Any, List, Optional

class PersonalAgentBiometricCircadianEnergyScheduler:
    def __init__(self):
        pass

    def compute_hourly_energy_curve(
        self,
        wake_hour: int = 7,
        sleep_hours_last_night: float = 7.5,
        hrv_ms: float = 65.0
    ) -> Dict[str, Any]:
        """
        Models alertness score [0..100] from wake_hour to wake_hour + 15h:
        Combines sleep recovery factor, HRV readiness, morning peak (+2.5h to +5h post-wake),
        post-lunch dip (+7h to +8.5h post-wake), and early evening second wind (+10h post-wake).
        """
        sleep_factor = min(1.1, max(0.5, sleep_hours_last_night / 7.5))
        hrv_factor = min(1.1, max(0.6, hrv_ms / 60.0))
        readiness_multiplier = (0.6 * sleep_factor) + (0.4 * hrv_factor)

        hourly_curve = []
        for offset in range(16):
            hour_of_day = (wake_hour + offset) % 24
            # Homeostatic decay over time awake
            homeostatic = max(20.0, 90.0 - (offset * 3.2))

            # Circadian modulation (sinusoidal with post-lunch dip)
            if 2 <= offset <= 5:
                circadian_mod = 15.0 # Morning cognitive peak
                zone = "PEAK_DEEP_WORK"
            elif 7 <= offset <= 8:
                circadian_mod = -18.0 # Post-prandial dip
                zone = "TROUGH_ADMIN_REST"
            elif 9 <= offset <= 11:
                circadian_mod = 8.0 # Afternoon rebound / collaborative peak
                zone = "REBOUND_COLLABORATIVE"
            else:
                circadian_mod = -5.0
                zone = "WIND_DOWN_LIGHT"

            energy_score = round(min(100.0, max(10.0, (homeostatic + circadian_mod) * readiness_multiplier)), 1)
            hourly_curve.append({
                "hour_24": f"{hour_of_day:02d}:00",
                "hours_since_wake": offset,
                "energy_score": energy_score,
                "circadian_zone": zone
            })

        return {
            "readiness_score": round(min(100.0, readiness_multiplier * 88.0), 1),
            "wake_hour": f"{wake_hour:02d}:00",
            "hourly_curve": hourly_curve
        }

    def schedule_tasks_by_energy(
        self,
        tasks: List[Dict[str, Any]],
        wake_hour: int = 7,
        sleep_hours_last_night: float = 7.5,
        hrv_ms: float = 65.0
    ) -> Dict[str, Any]:
        """Matches HIGH cognitive tasks to PEAK energy hours and LOW load tasks to TROUGH hours."""
        curve_data = self.compute_hourly_energy_curve(wake_hour, sleep_hours_last_night, hrv_ms)
        available_slots = list(curve_data["hourly_curve"])

        # Sort slots descending by energy_score
        high_slots = sorted(available_slots, key=lambda x: x["energy_score"], reverse=True)
        low_slots = sorted(available_slots, key=lambda x: x["energy_score"])

        used_hours = set()
        scheduled = []

        # Order tasks: HIGH first, then MEDIUM, then LOW
        load_priority = {"HIGH": 0, "MEDIUM": 1, "LOW": 2}
        sorted_tasks = sorted(tasks, key=lambda t: load_priority.get(str(t.get("cognitive_load", "MEDIUM")).upper(), 1))

        for task in sorted_tasks:
            load = str(task.get("cognitive_load", "MEDIUM")).upper()
            candidate_pool = high_slots if load in ("HIGH", "MEDIUM") else low_slots

            chosen_slot = None
            for slot in candidate_pool:
                if slot["hour_24"] not in used_hours:
                    chosen_slot = slot
                    used_hours.add(slot["hour_24"])
                    break

            if chosen_slot:
                scheduled.append({
                    "assigned_time": chosen_slot["hour_24"],
                    "task_title": task.get("title", "Untitled Task"),
                    "cognitive_load": load,
                    "slot_energy_score": chosen_slot["energy_score"],
                    "circadian_zone": chosen_slot["circadian_zone"],
                    "ultradian_break_recommended": load == "HIGH"
                })

        scheduled.sort(key=lambda x: x["assigned_time"])

        return {
            "biometric_readiness": curve_data["readiness_score"],
            "total_scheduled_tasks": len(scheduled),
            "optimized_schedule": scheduled
        }
