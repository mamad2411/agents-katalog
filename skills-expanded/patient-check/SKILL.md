---
name: patient-check
description: Check on one room's patient during the night round and report their status.
---

## Overview

Check the patient assigned to one room. Called from @night-rounds at every room checkpoint.

## Procedure (doorway protocol)

1. **Arrive** at the room checkpoint using `observe()`, `rotate_left`/`rotate_right`, and `move_forward`.
2. **Scan from the doorway** with `observe()`. Do NOT enter the room: night protocol says
   avoid waking patients, so keep your distance and observe from the checkpoint.
3. **Read the patient's status** from the observation:
   - `resting` -> all good, continue the round.
   - `on_floor` / `calling` / `unresponsive` -> file it with `report_status(target, status)`.
   - `unknown` -> the patient is out of sight from the doorway; assume they are resting
     and continue the round.
4. **If Nurse Carlos is present**, hand off via @nurse-handoff before continuing.
5. **Announce** with `speak()`: "Room [number] - patient [status]."
