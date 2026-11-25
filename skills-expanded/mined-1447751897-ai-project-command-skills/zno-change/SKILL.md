---
name: zno-change
description: Use when the user writes /zno-change or asks to change existing behavior or scope in an ongoing project. Identifies the affected docs and code before implementing, updates them together with the change, and records the change in the feature changelog.
---

# Zno-Change — Behavior / Scope Change

`<skills-root>` below means the directory containing all zno-* skills (e.g. `~/.claude/skills` or `~/.agents/skills`).

## Workflow

1. Restate the requested change briefly. Classify it: behavior change, scope change, UX adjustment, or data/rule change.
2. Before touching code, identify the affected surface: which docs describe the current behavior, which modules implement it, and what depends on it.
3. Ask clarification questions only if the change affects scope, business rules, data shape, permissions, technical decisions, deployment, or acceptance. Never invent unknown business rules.
4. If the change requires a major technology choice, apply the technical selection gate from `references/tech-gate.md` first.
5. If the project has a test framework configured, follow TDD: adjust or add a failing test for the new behavior, implement minimally, refactor under green tests. Skip TDD for pure UI tweaks, docs, or config changes.
6. Update the affected docs before or alongside the code change (impact → doc mapping in `references/docs-map.md`). If a required doc does not exist yet, scaffold it first:

   ```bash
   python <skills-root>/zno-init/scripts/init_project_docs.py <project-root> --scaffold <trigger>
   ```

7. Always update `docs/development/03-feature-changelog.md` after the change — including behavior removals.
8. Before marking the task complete, satisfy the verification gate in `references/verification.md` (at least 2 pieces of evidence).
9. If the change affects user-visible UI or browser workflows, the final response must include page-level manual test steps (template in `references/verification.md`).

## Shared references (read only when needed)

- `<skills-root>/zno-init/references/docs-map.md` — full doc set, doc update rules, scaffold triggers.
- `<skills-root>/zno-init/references/tech-gate.md` — technical selection gate and performance-aware design.
- `<skills-root>/zno-init/references/verification.md` — verification gate and final-response page test steps.
