---
name: my-new-skill
description: One sentence on what it does. Use when the user asks to <verb> <thing>, mentions <keywords>, or provides <file type>.
metadata:
  internal: true   # hides the template from `npx skills add`; delete this line in your copy
---

# My New Skill

## When to use
- Trigger case 1
- Trigger case 2

## Workflow
1. Gather inputs: list required inputs; ask for any that are missing and can't be safely assumed. State assumptions explicitly.
2. Run `scripts/main.py` with the inputs (never do the arithmetic by hand).
3. Check results: units consistent, sanity estimate within 2x, safety factors meet target.
4. Report using the output format below.

## Output format
```
Inputs / assumptions
Results table
Checks passed / flagged
Recommendation
```

## References
- `references/table.md`: read when you need <data>.
