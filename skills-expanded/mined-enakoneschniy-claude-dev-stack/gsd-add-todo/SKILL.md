---
name: gsd-add-todo
description: "[DEPRECATED] Use /cds-add-todo instead"
allowed-tools:
  - Skill
---

<objective>
This command is deprecated. Use /cds-add-todo instead.
</objective>

<process>
1. Display: "⚠ /gsd-add-todo is deprecated. Use /cds-add-todo instead."
2. Invoke: Skill(skill="cds-add-todo", args="$ARGUMENTS")
</process>
