---
name: zno-continue
description: Use when the user writes /zno-continue or starts a new session wanting to resume where a previous conversation left off. Reads the status snapshot and supporting docs, summarizes the project state, then continues with the next safe task.
---

# Zno-Continue — Cross-Chat Continuation

`<skills-root>` below means the directory containing all zno-* skills (e.g. `~/.claude/skills` or `~/.agents/skills`).

## Workflow

1. Read `docs/development/10-current-status.md` first.
2. Read the minimum supporting docs needed to avoid guessing: usually `docs/00_START_HERE.md`, `docs/development/03-feature-changelog.md`, `docs/product/06-roadmap.md`, and `docs/handoff/05-handoff-guide.md`.
3. Read `AI_DEVELOPMENT_RULES.md` and `docs/engineering/04-tech-decisions.md` before making implementation or technology choices.
4. Inspect the workspace for current files and uncommitted changes before editing anything.
5. Briefly summarize where the project left off.
6. Continue with the next task only if it is clear; otherwise ask the smallest necessary clarification question.
7. When continuing into implementation, apply the matching command workflow (`/zno-feature`, `/zno-change`, `/zno-fix`, ...). If the next task requires a new technical choice, apply the selection gate from `references/tech-gate.md` first.
8. Update `docs/development/10-current-status.md` again when pausing or finishing.

## Shared references (read only when needed)

- `<skills-root>/zno-init/references/docs-map.md` — full doc set, doc update rules, scaffold triggers.
- `<skills-root>/zno-init/references/tech-gate.md` — technical selection gate.
- `<skills-root>/zno-init/references/verification.md` — verification gate and final-response page test steps.
