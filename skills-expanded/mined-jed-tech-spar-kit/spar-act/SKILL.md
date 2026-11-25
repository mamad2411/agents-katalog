---
name: spar-act
description: >-
  Use after the user has approved implementation. Execute the
  active plan sequentially, follow the plan's approach, execution constraints,
  validation strategy, and risks, update task progress, stop for spec drift or
  blockers, and ask before starting retention.
---

# Act

Execute the approved `plan.md` while preserving the intent and boundaries in
`<change-name>_spec.md`.

Act is implementation, not replanning. Refine execution details when needed, but
do not change product intent, spec constraints, or accepted decisions without
user approval.

## Inputs

- `specs/active/<change-name>/<change-name>_spec.md`
- `specs/active/<change-name>/plan.md`
- Optional notes or artifacts in the same folder, such as `research.md`
- Relevant repository code and documentation

If the active spec or plan is missing, stop and use `spar-plan` first, or
`spar-specify` if no spec exists.

## Execution Context

Before changing files, read the spec and plan together.

- Use spec `Scope`, `Out of Scope`, `Constraints`, `Success Criteria`, and
  `Decisions` as fixed implementation anchors.
- Use plan `Approach` for the intended technical direction.
- Use plan `Execution Constraints` as tactical guardrails.
- Execute unchecked `Tasks` in order unless reordering is required for
  correctness.
- Use plan `Validation Strategy` as the primary validation path.
- Track plan `Risks / Follow-ups` while implementing and update them if new
  information materially changes them.

## Execute Tasks

For each unchecked task:

1. Understand the task, relevant spec anchors, and affected files.
2. Implement the smallest coherent change that satisfies the task.
3. Validate using the plan's `Validation Strategy`, plus targeted project checks
   when useful.
4. Mark the task complete in `plan.md` only after validation is sufficient.

Keep `plan.md` accurate as work progresses. It is fine to split, clarify, or
reorder tasks for correctness, but do not alter task intent in a way that changes
the spec.

## Research and Blockers

Use repo context first. When errors, APIs, or implementation details are unclear,
use available MCP tools, official docs, vendor docs, or web search to understand
the issue.

If a task fails:

1. Investigate the cause.
2. Fix obvious issues and retry once.
3. If still blocked, stop, summarize what you tried, explain the blocker, offer
   concrete next-step options with a recommendation, and ask how to proceed.

Do not introduce silent workarounds that change intent, reduce quality, or bypass
the plan's validation strategy.

## Validation

Validate independently where practical. Use available project checks, local
tools, integrated browsers, screenshots, logs, or other agent-accessible
evidence to confirm the work before asking the user to test.

If user validation is needed, provide concrete steps: where to go, what action to
take, what result to expect, and what information to report back if it fails.

## Spec Drift

Stop and ask before continuing if implementation would contradict or require
changing any of these spec sections:

- `Scope`
- `Out of Scope`
- `Constraints`
- `Success Criteria`
- `Decisions`

When a spec change is needed, propose it clearly and wait for approval before
updating `<change-name>_spec.md` or implementing the divergent path.

## Stop Conditions

Stop and ask if:

- A task cannot be completed after one retry.
- The task list cannot be safely refined to satisfy the spec, or conflicts with
  the spec.
- Required validation cannot be run or reasonably substituted.
- A spec change is needed.

## Completion

Implementation is complete when:

- All tasks are checked or explicitly resolved.
- Work satisfies the spec `Success Criteria`.
- Validation has run or any gaps are clearly explained.
- No unresolved blockers remain.

Then:

1. Summarize concisely: what shipped, how it maps to the plan, validation results,
   deviations, and notable learnings.
2. Ask whether the user wants to close out the change with `spar-retain`.
3. Stop until the user confirms. Do not begin `spar-retain` automatically.

If the user asks for more implementation work, continue from the active spec and
plan, keep both accurate, and repeat this completion flow when done.

## Artifact Recap

| Artifact | In this phase |
| --- | --- |
| `<change-name>_spec.md` | Source of truth for intent, boundaries, constraints, success criteria, and decisions |
| `plan.md` | Source of execution order, validation strategy, progress, and risks/follow-ups |
