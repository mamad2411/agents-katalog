---
name: gsd-remove-workspace
description: "[DEPRECATED] Use /cds-remove-workspace instead"
allowed-tools:
  - Skill
---

<objective>
This command is deprecated. Use /cds-remove-workspace instead.
</objective>

<process>
1. Display: "⚠ /gsd-remove-workspace is deprecated. Use /cds-remove-workspace instead."
2. Invoke: Skill(skill="cds-remove-workspace", args="$ARGUMENTS")
</process>
