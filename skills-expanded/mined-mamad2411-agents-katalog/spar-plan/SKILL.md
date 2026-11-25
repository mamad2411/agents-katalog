---
name: spar-plan
description: >-
  Use after the initial spec exists and the user is ready
  to turn it into an implementation plan. Complete the spec, define testable
  success criteria, settle important decisions, create an ordered plan with
  approach, execution constraints, tasks, validation strategy, and risks, then
  ask before starting implementation.
---

# Plan

Turn an active spec into a stable implementation plan.

Planning is the bridge between intent and action. Stabilize what must be true
before defining how to execute it.

## Role

- The user represents product intent and domain context.
- You are the lead engineer for planning: concise, practical, and explicit about tradeoffs.

Use technical judgment, but do not invent product intent. If a choice materially affects scope, success, validation, or risk, surface it clearly with a short recommendation and concrete options. Prefer "I recommend X because..." over open-ended tradeoff dumps, while still letting the user choose.

## Inputs

- `specs/active/<change-name>/<change-name>_spec.md`
- Optional notes or artifacts in the same folder, such as `research.md`
- Relevant repository code and documentation

If the active change folder or spec file is missing, stop and use `spar-specify` first.

## Templates

Before completing `<change-name>_spec.md`, read [assets/spec.md](assets/spec.md) and preserve its section order.

Do not create `plan.md` until the user has explicitly approved the spec for planning.

Before creating `plan.md`, read [assets/plan.md](assets/plan.md) and use it as the template.

Do not create `plan.md` until the spec is stable enough to support reliable tasks.

## Capture Planning Context

Before asking new questions, extract what is already known from the spec, thread, notes, repository files, and docs. Do not make the user repeat context that is already available.

Use repo research to reduce burden on the user when local context can answer a planning question. Preserve optional artifacts in the change folder.

Ask only for gaps that materially affect success criteria, scope, task order, risk, or validation.

## Complete the Spec

Refine the spec so it captures durable intent, not step-by-step implementation.

- Keep `Summary`, `Problem`, `Scope`, and `Out of Scope` aligned with the user's intent.
- Fill `Constraints` with solution requirements that must remain true.
- Fill `Success Criteria` with concrete, testable outcomes.
- Fill `Decisions` with important product and technical choices that implementation should treat as fixed.
- Keep `Open Questions` only for unresolved questions that materially affect implementation or validation.

Major product choices belong in `Scope` or `Out of Scope`. Major technical choices belong in `Decisions` or, if they are execution-only, in plan `Approach`.

## Follow-up Questions

When material questions remain, ask them explicitly before creating `plan.md`.
If there is 1 question, use a bullet. If there are 2 or more, use a numbered list.

When 3 or more questions still need resolved, priortize them in your chat using helpful headers:

- **Key Considerations**: blockers to a reliable spec or plan, especially success criteria, scope, sequencing, material risk, or validation.
- **Optional Considerations**: refinements that may improve the plan but should not block progress.

If key questions remain unresolved, record them in `Open Questions` and do not pretend the plan ready for implementation. Continue taking turns until all questions are resolved.

## Build the Plan

Create `plan.md` only after the spec is stable enough.

- `Summary`: brief overview of the implementation plan.
- `Approach`: major technical direction and sequencing strategy.
- `Execution Constraints`: tactical guardrails for how the work should be carried out.
- `Tasks`: ordered, concrete, checkable steps.
- `Validation Strategy`: checks, tests, or observations that confirm success.
- `Risks / Follow-ups`: material risks, deferred work, or decisions that may need follow-up.

Every task should support the spec's success criteria or reduce a risk needed to satisfy them.

## Stop Conditions

Stop and ask before continuing if:

- Requirements are too vague for reliable tasks.
- Success criteria cannot be made testable.
- Proposed tasks conflict with `Scope`, `Out of Scope`, `Constraints`, or `Decisions`.
- Implementation would require changing product intent rather than merely planning execution.

## Completion

Planning is complete when:

- `<change-name>_spec.md` is stable and includes testable `Success Criteria`.
- `plan.md` is actionable and aligned with the spec.
- Every item in `Open Questions` and `Risks / Follow-ups` is either resolved or linked to a specific task or section in `plan.md` that defines how it will be resolved.

Then:

1. Summarize concisely: spec status, plan outline, validation strategy, and remaining questions or risks.
2. Ask: **Are we ready to proceed to implementation?**
3. Only start `spar-act` after the user confirms.

## Artifact Recap

| Artifact | In this phase |
| --- | --- |
| `<change-name>_spec.md` | Stable intent, boundaries, constraints, success criteria, decisions, and material open questions |
| `plan.md` | Approach, execution constraints, ordered tasks, validation strategy, and risks/follow-ups |
