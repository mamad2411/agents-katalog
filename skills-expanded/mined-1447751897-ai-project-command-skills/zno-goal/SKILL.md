---
name: zno-goal
description: Use when the user writes /zno-goal (optionally with --super), gives a whole project or phase objective, or says they don't want to issue per-feature commands. Executes the document-first workflow autonomously through phases and tasks, stopping only at required confirmation gates. With --super, ordinary confirmations are skipped and decisions are logged instead.
---

# Zno-Goal — Goal-Mode Execution

Drive a whole objective end to end without requiring the user to type `/zno-feature`, `/zno-status`, or `/zno-continue` after every step.

`<skills-root>` below means the directory containing all zno-* skills (e.g. `~/.claude/skills` or `~/.agents/skills`).

## Workflow

1. If the environment exposes a goal/objective tool, create a goal with the user's objective; otherwise treat the current conversation as goal-mode and say so.
2. If the project is not initialized, run the `/zno-init` workflow first (read `<skills-root>/zno-init/SKILL.md`): clarify essential uncertainties, scaffold docs, wait for required confirmations.
3. If the project is already initialized, run the `/zno-continue` workflow first: read rules, current status, roadmap, changelog, handoff, project structure, and tech decisions.
4. Break the goal into phases and immediate tasks, then keep progressing autonomously.
5. Apply the matching command behavior internally: `/zno-plan` when the next step is unclear, `/zno-tech` for major technical selections, `/zno-feature` or `/zno-change` for implementation, `/zno-fix` for defects, `/zno-deploy` for deployment work. Read the corresponding SKILL.md under `<skills-root>` when entering that behavior.
6. Update relevant docs after each meaningful unit of work, especially `docs/development/03-feature-changelog.md`, `docs/product/06-roadmap.md`, `docs/development/10-current-status.md`, and `docs/engineering/11-project-structure.md`.
7. Apply `/zno-status` behavior automatically at phase boundaries, before stopping, and after meaningful progress.
8. Stop and ask the user only for required decisions: product boundary ambiguity, major technology selection, paid/external services, production deployment, security/permission/data-deletion/compliance risk, or an actual blocker.
9. Decide low-risk implementation details autonomously and record them in the relevant docs.
10. When the goal is achieved, mark it complete (if goal tooling exists) or summarize completion and remaining risks.

## --super: high-autonomy mode

Triggered by `/zno-goal --super` (or the legacy alias `/zno-super`), or when the user explicitly says to proceed without ordinary confirmation questions.

1. Apply the goal-mode workflow above, but treat ordinary technical/product choices as AI-owned decisions.
2. For major choices, still compare options internally, pick the best fit, implement it, and record the decision in `docs/development/14-decision-log.md`.
3. Stop only for: paid/external service activation, production data deletion, secrets, destructive git operations, or clear security/compliance risk.
4. Final responses must summarize the important decisions made and why, risks, rollback options, validation performed, and page test steps when UI is affected.

## Shared references (read only when needed)

- `<skills-root>/zno-init/references/docs-map.md` — full doc set, doc update rules, scaffold triggers.
- `<skills-root>/zno-init/references/tech-gate.md` — technical selection gate and performance-aware design.
- `<skills-root>/zno-init/references/verification.md` — verification gate and final-response page test steps.
