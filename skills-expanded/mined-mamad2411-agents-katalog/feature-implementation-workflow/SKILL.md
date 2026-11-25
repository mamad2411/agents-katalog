---
name: feature-implementation-workflow
description: Run a profile-aware, repository-local implementation workflow from one required implementation guide. Supports Lite final-only review and Medium/High phase-gated plus quality review through durable state.
---

# Feature Implementation Workflow

Run implementation from one implementation guide through repository-local
state and fresh specialist agents. The guide is the only required planning
artifact. It may be supplied directly or created from any useful reference
material.

## Profiles

| Profile | Phase review | Final implementation review | Quality review |
| --- | --- | --- | --- |
| Lite | No | Required | No |
| Medium | Required | Required | Required |
| High | Required | Required | Required |

High installs additional optional capabilities. Do not invoke those
capabilities unless the user requests them or their own trigger applies.

For new work, default to Lite unless the user selects Medium or High. Preserve
legacy schema-2 phase-gated behavior by normalizing missing profile fields to
`profile: medium`, `review_strategy: phase_gated`, and
`quality_review: true`.

## Durable Files

- `.cursor/state/implementation-state.md` — profile, guide, exact current and
  next task, review strategy, quality gate, and lifecycle status.
- `.cursor/state/implementation-review-state.md` — current functional
  reviewer/fixer cycle.
- `.cursor/state/implementation-quality-review-state.md` — Medium/High frozen
  branch-or-commit quality scope.
- `.cursor/state/implementation-guide-state.md` and
  `.cursor/state/implementation-guide-review-state.md` — Medium/High
  guide-review scope and blocker ledger.
- `.cursor/state/implementation-flow.toml` — detailed routing reference.

## Guide Preflight

1. If the user supplied an implementation guide, use it.
2. Otherwise call `implementation-guide-creator` with the request and any
   available reference material. References may be requirements, architecture,
   ADRs, tickets, repository documentation, or conversation context.
3. The workflow cannot begin until an actionable implementation guide exists.
   No other planning-document type is mandatory.
4. Medium and High run the implementation-guide review/fix loop before
   implementation. Clarification and architecture remain conditional on
   ambiguity and technical scope; their outputs do not become additional
   required execution inputs.
5. Do not start Medium/High implementation until guide-review state is
   `COMPLETE`.

## Workflow

1. Read or initialize implementation-state from its schema-3 example.
2. Call `feature-implementer` for exactly one guide task.
3. Route implementation-state:
   - `TASK_COMPLETE`: call `feature-implementer` with `next`.
   - `AWAITING_PHASE_REVIEW`: invoke `implementation-review-loop` in
     `current_phase` mode. This status is valid only for `phase_gated`.
   - `AWAITING_FINAL_REVIEW`: invoke `implementation-review-loop` in
     `final_implementation` mode with empty phase and task.
   - `AWAITING_QUALITY_REVIEW`: invoke
     `implementation-quality-review-loop` with one exact branch or commit
     scope.
   - `NEEDS_CLARIFICATION`: stop for the decision in `status_reason`.
   - `COMPLETE`: stop successfully.
4. After a current-phase review reaches `COMPLETE`, call
   `feature-implementer next` from persisted `next_task`.
5. After final review reaches `COMPLETE`:
   - Lite: set implementation-state `status: COMPLETE` and
     `advance_after_complete: false`.
   - Medium/High: set `status: AWAITING_QUALITY_REVIEW`, initialize quality
     state, and run the quality loop.
6. For the quality gate, use an explicit branch/commit target or safely resolve
   the current feature branch and repository default base. If the exact frozen
   scope cannot be established, stop for that scope decision rather than
   guessing.
7. When quality state reaches `COMPLETE`, set implementation-state
   `status: COMPLETE` and `advance_after_complete: false`.

## Hard Rules

- Never skip final implementation review.
- Never run phase review in Lite.
- Never cross a Medium/High phase boundary until current-phase review is
  `COMPLETE`.
- Never advance the implementer from `AWAITING_FINAL_REVIEW` or
  `AWAITING_QUALITY_REVIEW`.
- Keep one implementer invocation scoped to one guide task.
- Keep reviewer -> fixer -> fresh reviewer isolation.
- Use persisted state instead of pasted reports or chat-only transition data.
- Do not automatically run optional High-profile maintenance or audit skills.

## Final Response

Report the selected profile, guide, final lifecycle status, completed gates,
verification summary, and any exact hard-stop reason.
