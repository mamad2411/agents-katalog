---
name: zno-feature
description: Use when the user writes /zno-feature or asks to add a new feature to an ongoing project. Clarifies only what affects scope or design, follows TDD when a test framework exists, updates the relevant docs and the feature changelog, and passes the verification gate before completion.
---

# Zno-Feature — Mid-Project New Feature

`<skills-root>` below means the directory containing all zno-* skills (e.g. `~/.claude/skills` or `~/.agents/skills`).

## Workflow

1. Do not ask the user to re-paste any kickoff prompt. Restate the feature requirement briefly.
2. Ask clarification questions only if the request affects scope, business rules, data shape, permissions, technical decisions, deployment, or acceptance. Never invent unknown business rules.
3. If `docs/development/03-feature-changelog.md` does not exist yet, scaffold it first:

   ```bash
   python <skills-root>/zno-init/scripts/init_project_docs.py <project-root> --scaffold feature
   ```

4. If the feature requires a major technology choice (new framework, database, heavy dependency, external service), apply the technical selection gate from `references/tech-gate.md` before implementing.
5. If the project has a test framework configured, follow Test-First (TDD): write a failing test for the new behavior, implement minimally to pass, then refactor under green tests. Skip TDD for pure UI tweaks, docs, or config changes.
6. Update the relevant docs before or alongside code changes (see `references/docs-map.md` for the impact → doc mapping). Update `docs/product/15-frontend-design.md` and the tokens JSON when the feature affects UI style, layout, components, or interaction states.
7. Always update `docs/development/03-feature-changelog.md` after the feature is done.
8. Before marking the task complete, satisfy the verification gate in `references/verification.md` (at least 2 pieces of evidence).
9. If the feature affects user-visible UI or browser workflows, the final response must include page-level manual test steps (template in `references/verification.md`).

## Shared references (read only when needed)

- `<skills-root>/zno-init/references/docs-map.md` — full doc set, doc update rules, scaffold triggers.
- `<skills-root>/zno-init/references/tech-gate.md` — technical selection gate and performance-aware design.
- `<skills-root>/zno-init/references/verification.md` — verification gate and final-response page test steps.
