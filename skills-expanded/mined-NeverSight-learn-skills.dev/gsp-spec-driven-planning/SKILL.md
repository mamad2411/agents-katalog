---
name: gsp-spec-driven-planning
description: "Use when the user wants a persistent requirements/spec/design/tasks workflow, asks for OpenSpec-style planning, or needs durable change artifacts in the target repo."
---

# Game Spec-Driven Planning

## Goal
Add a lightweight spec-driven planning layer to a game project without replacing the normal Game Superpowers tracks.

## Artifact model

Keep stable capability specs separate from one change's working set.

- Living specs:
  - `specs/<capability>/spec.md`
- Change package:
  - `changes/<change-id>/proposal.md`
  - `changes/<change-id>/design.md`
  - `changes/<change-id>/tasks.md`
  - `changes/<change-id>/specs/<capability>/spec.md`

## Outputs

Follow the `gsp-orchestrator` output strategy:
- **inline** (default): keep the proposal, design, and task structure in conversation only.
- **minimal**: write the change package under `changes/<change-id>/`.
- **full**: write the change package and create or update the matching living specs under `specs/<capability>/`.

Use:
- `../../shared/reference/spec-driven-workflow.md`
- `../../shared/templates/change-proposal.md`
- `../../shared/templates/capability-spec.md`
- `../../shared/templates/change-design.md`
- `../../shared/templates/change-tasks.md`

## Workflow
1. Decide whether the request should stay inline or become durable repo artifacts.
2. Derive a stable `change-id` and 1-3 capability names.
3. Use `gsp-requirements-brainstorm` to lock the requirement set when intent is still fuzzy.
4. Write `proposal.md` for the user-facing goal, scope, affected capabilities, and acceptance signals.
5. Write or update the capability delta under `changes/<change-id>/specs/<capability>/spec.md`.
6. Use the design skills needed for the change, then consolidate the result into `design.md`.
7. Use `gsp-implementation-plan` to produce `tasks.md`.

## Routing

Typical downstream skills:
- `gsp-requirements-brainstorm`
- `gsp-mechanics-systems-design`
- `gsp-ux-flow-designer`
- `gsp-feedback-design`
- `gsp-implementation-plan`

Add `gsp-scope-profile`, `gsp-build-strategy`, or `gsp-production-code` when the change needs stronger scope or quality controls.

## Important rules
- Keep `specs/` durable and capability-oriented. Do not dump one-off implementation notes into them.
- Keep one `changes/<change-id>/` folder per meaningful user-facing change.
- Put design decisions in `design.md`, not in `tasks.md`.
- Keep traceability explicit. A proposal should name the capabilities it changes, the design should name the requirements it covers, and tasks should point back to the requirement or design area they implement.
- If the user did not ask for persistent artifacts, do not force file creation.
