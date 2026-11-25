---
name: skill-bug-routing
description: Classify QC defects as blocker or non-blocker and route fix work to the correct generated coder through Coder Leader.
category: workflow
---

# Skill: Bug Routing

Use when QC finds a defect.

## Blocker

```text
Main flow fails
Core API/app crashes
Auth/security is broken
Data corruption risk
Setup is blocked
Downstream QC cases cannot continue
```

Action: stop QC, create blocker bug, route to Coder Leader.

## Non-blocker

```text
Cosmetic or copy issue
Minor layout issue
Rare edge case not blocking main flow
Non-critical warning
```

Action: create non-blocker bug, continue QC, optionally fix in parallel.
