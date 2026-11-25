---
description: Capture repetitive user instructions into the memory bank automatically
alwaysApply: true
---

# Persistent user instructions

When the user gives a preference, constraint, or instruction that would apply across future sessions (not a one-off task), **append it to `memory-bank/user-instructions.md`** before or after completing the task.

## Add to `user-instructions.md` when the user says things like:

- "Always use X" / "Never use Y"
- "From now on…" / "Going forward…"
- "Don't repeat…" / "Remember that…"
- Tool, stack, style, or workflow preferences stated as standing rules
- Corrections to agent behavior they don't want to repeat

## Do NOT add when:

- It's a one-time task ("fix this bug", "add this file")
- It's already captured in `user-instructions.md`, `decisions.md`, or `tech-stack.md`
- It's project ground truth already in thesis/pipeline docs (link instead)

## Format for new entries

```markdown
### YYYY-MM-DD — Short title
**Source:** one-line context
**Instruction:** what to always do
```

Also log architectural/stack choices in `memory-bank/decisions.md` and update `vivere-pipeline/docs/tech-stack.md` when the backend stack changes.

## Before writing backend code

Read `vivere-pipeline/docs/tech-stack.md` and `memory-bank/user-instructions.md`. Do not invent libraries or versions not listed there.
