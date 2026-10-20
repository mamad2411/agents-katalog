---
description: "Ping kapag present ang Action_Plan.md (planning output)."
globs: ["memory-bank/plan/Action_Plan.md"]
alwaysApply: false
---

<rule>
name: planning_output_presence
description: Detect Action_Plan.md exists.
actions:
  - type: suggest
    message: "✓ Detected: memory-bank/plan/Action_Plan.md (planning output present)."
</rule>
