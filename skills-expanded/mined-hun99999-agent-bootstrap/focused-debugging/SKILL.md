---
name: focused-debugging
description: Use only when the user explicitly requests focused debugging for a non-obvious or repeated failure whose cause is not established.
---

# Focused Debugging

## Result

Produce the strongest supported cause, one targeted fix when authorized, direct outcome evidence, and any residual uncertainty.

## Route

1. Capture the exact symptom and the smallest practical reproduction or direct failure evidence.
2. Localize the failing boundary using the error, relevant recent change, and data flow.
3. State the leading hypothesis and the observation that would distinguish it.
4. Run the lowest-cost discriminating check.
5. When confirmed, fix the cause at its boundary and rerun the reproduction. When disproved, rank the next hypothesis only from new evidence.
6. Report cause evidence, the change, the proving check, and unresolved uncertainty.

## Stop

Finish as soon as one cause and outcome are directly supported. Return one concise blocker when the next discriminating check needs unavailable state or when the evidence points to a material architecture change. Keep broader regression proportional to the affected surface.
