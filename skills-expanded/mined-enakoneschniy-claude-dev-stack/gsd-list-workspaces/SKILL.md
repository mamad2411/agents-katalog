---
name: gsd-list-workspaces
description: "[DEPRECATED] Use /cds-list-workspaces instead"
allowed-tools:
  - Skill
---

<objective>
This command is deprecated. Use /cds-list-workspaces instead.
</objective>

<process>
1. Display: "⚠ /gsd-list-workspaces is deprecated. Use /cds-list-workspaces instead."
2. Invoke: Skill(skill="cds-list-workspaces", args="$ARGUMENTS")
</process>
