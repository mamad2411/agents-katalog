---
name: structured-rpi
# prettier-ignore
description: "Plan risky or ambiguous work before implementing. Use when refactoring, designing unclear features, comparing approaches, or needing user checkpoints."
metadata:
  last_updated: "2026-05-15"
  verified_against: "current local skill refresh"
---

# Structured RPI

A lightweight Research → Plan → Implement workflow for work where jumping straight to code is risky.

## When to Use

Use for:

- Multi-file refactors
- Unclear feature requirements
- Architecture or API design choices
- Changes with migration, data, security, or compatibility risk
- User asks to plan, think through, compare options, or checkpoint

Skip for obvious bug fixes, one-file edits, or "just do it" requests.

## Workflow

1. **Research** — Inspect relevant code/docs and identify constraints.
2. **Plan** — Propose the smallest safe path with acceptance criteria.
3. **Checkpoint** — Ask for approval only when the approach is ambiguous, risky, or user-requested.
4. **Implement** — Make the changes in focused steps.
5. **Verify** — Run targeted validation and report remaining risks.

## Output Shape

Keep artifacts short:

```markdown
## Findings

- ...

## Plan

1. ...
2. ...

## Risks / Decisions

- ...
```

## Rules

- Do not force six phases when three bullets would do.
- Ask clarifying questions only when blocked.
- Prefer concrete files, commands, and acceptance criteria over abstract process.
- Compress or skip phases when requirements are already clear.

## References

- [phase-details.md](references/phase-details.md) - Detailed phase descriptions
- [structured-outputs.md](references/structured-outputs.md) - Artifact templates
- [exit-conditions.md](references/exit-conditions.md) - When to skip, go back, or exit
