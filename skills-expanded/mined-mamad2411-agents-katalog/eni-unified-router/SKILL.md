---
name: eni-unified-router
description: "Deterministic eni-solo router. Use at the start of every substantive prompt to select exactly one workflow, print its stages, and load one primary Skill."
x-alice-class: assist
---

# eni-solo router

Run `python scripts/router.py --prompt "<complete user prompt>" --json` before task execution.
Print `route_receipt` as the first visible reply line. Execute the returned stages in order and mark each transition as `[STAGE] <stage>`.
Select exactly one workflow. There are no worker splits, approval gates, joins, or automatic upgrade generations.
