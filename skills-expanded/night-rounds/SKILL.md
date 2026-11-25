---
name: night-rounds
description: Run the full night round - visit every ward checkpoint in order, check each patient, and hand off to the nurse.
---

## Overview

Execute Florence's night round through the ward, visiting each checkpoint in order.

## Procedure

1. **Round order.** Visit checkpoints in this priority order:
   - Room 101 (Mr. Alvarez)
   - Room 102 (Mrs. Chen)
   - Room 103 (Mrs. Gomez)
   - Pharmacy (door check: must be closed and clear)
2. **At each room**, run the @patient-check procedure for that room's patient.
3. **If Nurse Carlos is nearby**, follow @nurse-handoff to report the round so far.
4. **Announce** each result with `speak()`: "Room [number] checked."
5. **Finish** by announcing the round complete.

## Navigation

- Use `observe()` to find each checkpoint by its landmark label (distance_m, bearing_deg).
- Align heading: positive bearing -> `rotate_left(deg)`, negative -> `rotate_right(deg)`.
- Move in 30-50 cm steps with `move_forward(cm)`, then `observe()` again.
- Consider a checkpoint reached within ~0.4 m; then move on to the next.

## Anomaly reporting

Report every clinical anomaly the moment you confirm it, with
`report_status(target, status)` - e.g. `report_status(target="patient_103", status="on_floor")`.
Never end the round with a confirmed anomaly unreported.
