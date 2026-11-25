---
name: make-specs
description: Creates Orchid specs with requirements, design, spec.toml, and scoped tasks. Use for stable work that should be planned before dispatch.
---

# Make Specs

Create Orchid-compatible specs from clear requirements. A complete spec stands
alone: workers can implement focused slices without reading broad planning
notes or guessing at success criteria.

## When To Use

Use this skill for bounded work with stable requirements and clear completion
criteria.

Do not create a dispatchable numeric spec for exploratory work, ambiguous
scope, or missing success criteria. Use discovery or a `DRAFT-SLUG` spec until
the task set is ready to lease.

Do not create a spec just to host a measurable improvement loop. Use the Orchid
goal loop instead when a named evaluator, metric, direction, minimum delta,
budget, and keep/discard rule should govern repeated hypothesis cycles.

Keep the human in the loop. Before freezing non-trivial tasks, clarify the
user's intent, success criteria, desired granularity, review expectations, and
ideal spec shape. If those answers are still unstable, keep the work in a draft
or discovery state.

## Layout

```text
specs/001-short-slug/
  requirements.md
  design.md
  spec.toml
  tasks/
    T001.md
```

Use active numeric folders for dispatchable specs. Use `DRAFT-`, `TBD-`,
`MANUAL-`, or `DONE-` prefixes for specs that should not be leased.

## Workflow

1. Choose the spec id, such as `001-short-slug`, or a lifecycle prefix for
   inactive work.
2. Inspect the repo for likely files, tests, reuse targets, risks, and local
   conventions.
3. Clarify intent and spec shape with the user when scope, success criteria, or
   task boundaries are unclear.
4. Put exploration notes, raw research, transcripts, and broad context under
   `.orchid/spec-research/<spec-id>/`; keep PRD/spec files distilled to durable
   facts, decisions, and worker-facing context.
5. Write `requirements.md` with stable requirement ids such as `R001`.
6. Write `design.md` with scope, non-goals, approach, assumptions, risks, and
   validation.
7. Write `spec.toml` for policy Orchid should carry in packets, influenced by
   repo validation, review, and commit/signing conventions.
8. Split work into one task file per isolated implementation slice.
9. Give each task a narrow `scope`, explicit dependencies, DoD, validation, and
   `worker_reasoning_effort`.
10. Default normal implementation tasks to `worker_reasoning_effort = "medium"`;
    use `"low"` only for mechanical low-risk edits, and `"high"` or `"xhigh"`
    for architecture, data migrations, security, concurrency, unclear
    invariants, or broad behavioral risk. Set `worker_model` only when a model
    override is required; blank or omitted models are not emitted in ACKs.
11. Keep requirements, design, policy, and task `covers` fields aligned.
12. Leave task status as `todo`; Orchid updates completion fields later.
13. Run `orchid lint`, fix errors, and re-run until green.

## Task Template

```md
+++
id = "T001"
title = "Implement one focused slice"
status = "todo"
scope = ["src/example/"]
depends = []
covers = ["R001"]
verification_mode = "validator"
verification_status = "pending"
worker_reasoning_effort = "medium"
worker_model = ""
+++

## Context

What the worker needs to know before editing.

## DoD

What must be true when the task is complete.

## Validation

The focused command or check for this task.
```

## Task Rules

- Prefer several narrow tasks over one broad task.
- Prefer tracer-bullet slices and red-green validation loops for risky work.
- Make scopes concrete enough for touched-file checks.
- Use dependencies when one task must wait for another.
- Choose `worker_reasoning_effort` deliberately; use medium as the normal
  default and escalate only when task risk justifies it. Legacy task files may
  omit the field; Orchid treats omission as `medium`.
- Put durable facts in the spec, not in temporary research notes.
- Do not ask workers to infer requirements from broad planning documents.
- Do not mark tasks `done`; completion belongs to `orchid complete`.
- Keep inactive work under `DRAFT-`, `TBD-`, `MANUAL-`, or `DONE-` prefixes.

## Done

Before dispatch, `orchid lint` passes, each task has a concrete scope and
validation check, dependencies are valid, and the active spec contains no known
blockers.
