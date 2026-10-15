---
name: byte-build
description: Execute Your ByteDance / Byte OS plan files by dependency-ready waves. Use when the user asks to build, implement, execute plans, run the next wave, run `byte-build --wave N`, run `byte-build --plan ID`, or run `byte-build --all`.
---

# Byte Build

Build executes plans. By default, it executes the next dependency-ready wave, not simply plan 001.

## Inputs

Read:

```text
.byte-os/STATUS.md
.byte-os/plans/*.plan.md
.byte-os/PRODUCT_SPEC.md
.byte-os/UX_SPEC.md
.byte-os/TECH_SPEC.md
.byte-os/OKRS.md
```

If no plans exist, run or recommend `byte-plan`.

## Modes

```text
byte-build
```

Execute the next wave whose dependencies are complete.

```text
byte-build --wave N
```

Execute all ready plans in wave `N`.

```text
byte-build --plan ID
```

Execute one plan only.

```text
byte-build --all
```

Execute all waves until plans complete or a blocker appears.

## Execution Rules

- Inspect the repository before editing.
- Apply `byte-code-rules` for all coding work: think before coding, keep the implementation simple, make surgical changes, and verify against explicit success criteria.
- Never revert user changes.
- Keep each plan's write scope clear.
- Use actual worker subagents only when explicitly authorized by the user or auto workflow; assign disjoint ownership.
- If subagents are not authorized, execute locally but still preserve role ownership in plan logs.
- Mark a plan `in_progress` before work and `complete` only after verification.
- Mark `blocked` with a clear reason when execution cannot continue.
- Run the most relevant tests, linters, type checks, builds, or manual verification available.
- For frontend apps, start the dev server when appropriate and provide the URL after successful implementation.
- Keep a candid build log: what worked, what failed, what changed, and which Key Results moved.

## Wave Selection

A plan is ready when:

- status is `pending` or `ready`
- all `depends_on` plans are `complete`
- no blocker is recorded

When multiple plans are ready in the same wave, execute in parallel only if subagent use is explicitly authorized and write scopes do not overlap.

## Artifacts

Update:

```text
.byte-os/plans/*.plan.md
.byte-os/STATUS.md
.byte-os/BUILD_LOG.md
```

`BUILD_LOG.md` should include:

- Date
- Mode
- Plans executed
- Files changed
- Code rule notes: assumptions, scope decisions, and any intentional tradeoffs
- Verification run
- OKR or metric impact
- Failures or blockers
- Next wave

Update `STATUS.md`:

```text
Stage: building
Current wave: <N>
Plans complete: <X>/<Y>
Next recommended command: byte-build or byte-review
```

## Completion Criteria

Build is complete when every v0 plan is complete and the product can be reviewed as a working deliverable or faithful prototype.
