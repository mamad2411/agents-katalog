---
name: tedflow-implement-plan
description: Implement an approved coding plan phase by phase with automated verification, plan checkbox updates, and manual testing checkpoints. Use when the user asks to implement a plan, execute a plan file, continue implementation, resume work from a plan, complete the next phase, or work through a plan from the plans/ directory.
---

# Workflow Implement Plan

Use this skill to implement an approved plan from `plans/`.

## Inputs

Treat the user's current request as the input. If it does not include a plan path, ask for one.

Example path:

```text
plans/2026-05-14-feature-name.md
```

## Preparation

1. Read the plan completely.
2. Check existing checkboxes and resume from the first incomplete implementation item.
3. Read all files mentioned in the plan fully before editing.
4. Read project guidance when present: `AGENTS.md`, `CLAUDE.md`, `.claude/CLAUDE.md`, `.cursor/rules`, or equivalent docs.
5. Track progress with the agent's native todo/plan mechanism. If none exists, maintain a short visible Markdown checklist.

## Implementation Rules

- Follow the plan's intent while adapting to current code reality.
- Complete one phase at a time unless the user explicitly asks to run multiple phases.
- Keep edits scoped to the phase and the surrounding code required to make it work.
- Use existing project patterns, helpers, tests, and build tools.
- Update unit tests in the same phase as the implementation they cover.
- Do not mark manual verification items complete unless the user confirms them.

If the plan does not match the codebase, stop and report:

```markdown
Issue in Phase [N]:
Expected: [what the plan says]
Found: [actual situation]
Why this matters: [impact]

How should I proceed?
```

## Verification

After each phase:

1. Run the automated checks listed in that phase.
2. If the plan does not list commands, infer the narrowest useful lint, typecheck, test, or build commands from project guidance.
3. Fix failures before proceeding.
4. Update completed implementation checkboxes in the plan file.
5. Leave manual verification checkboxes unchecked until the user confirms them.

Then pause with:

```markdown
Phase [N] Complete - Ready for Manual Verification

Automated verification passed:
- [command/result]

Please perform the manual verification steps listed in the plan:
- [manual step]

Let me know when manual testing is complete so I can proceed to Phase [N+1].
```

If the user explicitly asked to execute multiple phases consecutively, skip intermediate manual pauses and pause after the last requested phase.

## Resuming

If the plan already has checked items, trust them unless something looks inconsistent. Continue from the first unchecked item and preserve the end goal over mechanical checkbox completion.
