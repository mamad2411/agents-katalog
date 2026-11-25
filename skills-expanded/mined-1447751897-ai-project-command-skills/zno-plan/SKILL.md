---
name: zno-plan
description: Use when the user writes /zno-plan, has no clear next step, asks what to add or improve, or wants feature recommendations. Reads the project docs and recommends 3-7 prioritized directions with value, complexity, and risks, then waits for the user to choose. Never implements directly.
---

# Zno-Plan — Feature Recommendations

`<skills-root>` below means the directory containing all zno-* skills (e.g. `~/.claude/skills` or `~/.agents/skills`).

## Workflow

1. Read what exists: `docs/product/01-requirements-clarification.md`, `docs/development/03-feature-changelog.md`, `docs/product/06-roadmap.md`, `docs/development/10-current-status.md`, and `docs/engineering/11-project-structure.md` (skip files that don't exist).
2. Identify the current project phase and whether the core user journey is complete.
3. Recommend 3-7 candidate directions, drawing from: core workflow gaps, UX polish, admin/permissions/audit, performance, security, deployment/observability, data/reporting, and operations/commercialization where relevant.
4. For each candidate, state: user value, priority, implementation complexity, dependencies, performance/security/deployment impact, and whether it would hit the technical selection gate.
5. Recommend the top 1-2 next steps and ask the user to choose.
6. Do not implement anything until the user selects a direction. Once selected, hand over to the matching command workflow (`/zno-feature`, `/zno-tech`, ...).

## Shared references (read only when needed)

- `<skills-root>/zno-init/references/docs-map.md` — full doc set, doc update rules, scaffold triggers.
- `<skills-root>/zno-init/references/tech-gate.md` — what counts as a major technical selection.
