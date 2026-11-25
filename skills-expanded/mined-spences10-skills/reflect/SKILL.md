---
name: reflect
# prettier-ignore
description: "Capture reusable session learnings. Use when updating agent instructions, adding lessons learned, preserving project conventions, or fixing repeated mistakes."
metadata:
  last_updated: "2026-05-15"
  verified_against: "current local skill refresh"
---

# Reflect

Extract reusable lessons from a session and persist them to the right skill or agent instruction file.

## When to Reflect

Use after:

- Corrections: "actually use X", "no, do it this way"
- Repeated mistakes or preventable failures
- New project conventions or non-obvious constraints
- User asks to update instructions, memory, rules, or skills

## Workflow

1. **Collect evidence** — Use visible context first; use recall tooling when the user asks for prior-session context.
2. **Classify** — Keep only durable patterns, not one-off task details.
3. **Choose destination** — Update the specific skill when possible; otherwise update project/global agent instructions.
4. **Write lean rules** — Actionable, scoped, and easy for future agents to follow.
5. **Confirm** — Show the proposed change before writing when confidence is low.

## What to Add

Add guidance when it is:

- Reusable across future sessions
- Specific enough to change behavior
- Tied to a real correction, failure, or discovery

Remove or avoid guidance when it is stale, duplicated, obvious, or only useful for the current task.

## References

- [analysis-patterns.md](references/analysis-patterns.md) - Pattern detection rules
- [lesson-patterns.md](references/lesson-patterns.md) - Writing effective reusable lessons
- [structure-guide.md](references/structure-guide.md) - Organizing instruction files
- [hierarchy.md](references/hierarchy.md) - Global vs project scope
