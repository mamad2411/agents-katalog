---
name: implementation-workflow
description: Use when implementing repository changes through the smallest safe path, from direct routine fixes to risk-driven clarification, specs, plans, task coordination, validation, and documentation updates.
---

# Implementation Workflow

Use this skill when moving from OpenArc governance into actual implementation.

## Choose the Smallest Path

### Routine Work

Use direct implementation when scope, constraints, expected behavior, and validation are clear and the change has no unresolved product, compatibility, migration, security, or cross-system decision.

1. Inspect the affected flow and callers.
2. Reuse the existing implementation and conventions.
3. Make the smallest coherent change.
4. Run the smallest check that would catch a regression.
5. Update existing documentation only when behavior changed or repository policy requires it.

Do not create or patch an agent guide, governance document, spec, plan, or task list as a prerequisite for routine work.

### Non-Trivial Work

1. Inspect the repository, affected architecture, existing governance, and reusable systems.
2. Run `clarification-gate` only when material decisions remain unresolved.
3. Create or update a spec in `docs/specs/*` when behavior, acceptance criteria, or compatibility needs durable alignment.
4. Create or update a plan in `docs/plans/*` when sequencing, migration, rollback, or validation risk needs structure.
5. Use both a spec and a plan only when both decision alignment and execution risk justify them.
6. Use `docs/TASKS.md` only when execution spans multiple stages, people, or agents.
7. Classify version impact when the change is release-visible.
8. Implement incrementally, apply the component reuse gate for UI work, validate, and update relevant existing documentation.

## Component Reuse Gate

For UI or frontend changes:

1. Read `docs/DESIGN.md` when it exists.
2. Inspect the local component library before creating a new component.
3. Reuse or extend an existing component when it covers roughly 70-80% of the use case.
4. If creating a reusable component, update `docs/DESIGN.md` with a `Component Patterns` entry in the same change.
5. If creating a one-off component, document the reason in the related spec or plan.

This gate prevents silent component duplication while keeping `docs/DESIGN.md` from becoming a component inventory dump.

For script, CLI, automation, data-processing, library, or docs-only repositories, skip this gate unless the task introduces UI, visual assets, or public brand surfaces.

## Optimization Targets

- Long-running repositories
- AI continuity
- Low context drift
- Maintainable vibe coding
- Small, reviewable diffs

## Rules

- Do not begin unrelated business features while setting up OpenArc.
- Do not start implementation while a material decision is unresolved; use `clarification-gate`, then continue in the same turn when readiness is `ready` and the original request authorizes implementation.
- Do not require a spec and a plan together when either one is sufficient.
- Do not create a task tree parallel to `docs/TASKS.md`.
- Reuse existing code, docs, scripts, and conventions.
- Prefer patch-based updates over rewrites.
- Keep implementation and documentation in sync.
- Do not create `docs/DESIGN.md`, `docs/BRAND.md`, or `docs/assets/*` just to satisfy a generic checklist.
- Do not create duplicate UI components without first checking existing components and `docs/DESIGN.md`.
- Report created files, modified files, validation performed, conflicts, and next-step recommendations.
- Use `release-workflow` for branch, commit, PR, merge, and GitHub release update work.
