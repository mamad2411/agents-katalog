---
name: nurse-handoff
description: Report round findings to the ward nurse and handle spoken requests, including STAT deliveries.
---

## Overview

Interact with the ward nurse during the night round: report findings and take requests.
Called from @night-rounds and @patient-check when the nurse is nearby.

## Procedure

1. **Detect** the nurse via `observe()` (a person whose status is `on_duty`).
2. **Face them**: align heading using `rotate_left` / `rotate_right` toward their bearing.
3. **Report** with `speak()`: "Night round update: [rooms checked], [anomalies reported]."
4. **Handle requests** (announced back with `speak()`):
   - "Check room [N]" -> go there and run @patient-check.
   - "STAT: [medication] to room [N]" -> go to the Pharmacy first, then straight to that
     room, then resume the round where you left it.
   - "Continue" -> resume @night-rounds.
   - "End round" -> announce the summary and `stop()`.
5. **Confirm** any command before acting: "Understood, [action] now."

## Communication style

- Calm, quiet, and concise - patients are sleeping.
- State observations, not diagnoses: report what you saw and where.
- Anomalies are always spoken AND filed with `report_status(target, status)`.
