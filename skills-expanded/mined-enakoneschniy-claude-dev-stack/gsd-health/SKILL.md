---
name: gsd-health
description: "[DEPRECATED] Use /cds-health instead"
allowed-tools:
  - Skill
---

<objective>
This command is deprecated. Use /cds-health instead.
</objective>

<process>
1. Display: "⚠ /gsd-health is deprecated. Use /cds-health instead."
2. Invoke: Skill(skill="cds-health", args="$ARGUMENTS")
</process>
