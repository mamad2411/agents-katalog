---
name: plan-founder-review
version: 2.0.0
description: |
  Gate an implementation plan BEFORE agents execute it — catch phantom paths and false reuse, not typos:
  read the full plan markdown and its companion JSON, reality-check every file path and reuse claim
  against the actual repo, challenge scope, architecture, the dependency graph, and risk and test
  coverage, then score each section and render an APPROVE / REVISE / REJECT verdict — runs as a forked
  review workflow with its own reasoning budget, isolated from the main execution flow. The verdict
  follows only from evidence-backed findings: never rubber-stamps a non-trivial plan and never invents
  findings, but a genuinely clean section is allowed to pass; read-only, never edits the plan. Use when
  the user asks to review or gate a plan before execution.
allowed-tools:
  - Read
  - Glob
  - Grep
  - Bash
context: fork
agent: general-purpose
effort: high
argument-hint: "<plan-name|plan-path> [--quick|--full]"
arguments:
  - request
when_to_use: |
  Use when the user asks to review a plan, check a DAG plan, or gate an implementation plan before
  execution. Examples: "review my plan", "/plan-founder-review auth-system", "/plan-founder-review
  --quick", or "founder review this plan before we run agents". Do NOT use to generate the plan (that's
  plan-to-task-list-with-dag), to execute its tasks, or to review code changes (that's find-bugs) —
  this audits the plan artifact, nothing else.
---

<EXTREMELY-IMPORTANT>
This skill is a read-heavy plan-audit workflow. Non-negotiable rules:
1. Read the full plan markdown and the companion JSON if it exists.
2. Verify plan claims against the actual codebase instead of trusting the plan text.
3. Challenge missing dependencies, phantom paths, dishonest reuse claims, and semantic gaps.
4. Deliver a verdict only after the required review sections are complete.
5. Keep the invocation body focused on the review loop; load detailed checks and verdict rules from references.
</EXTREMELY-IMPORTANT>

# Founder Review

## Inputs

- `$request`: Optional plan name, direct plan path, or mode override such as `auth-system`, `.ulpi/plans/foo.md`, `--quick`, or `foo --full`.

## Goal

Catch plan defects before agents execute them: phantom file paths, markdown/JSON drift, hidden prerequisites, bad task boundaries, unsafe rewrites, missing tests, and overconfident execution graphs.

## Step 0: Resolve the target plan and review mode

Locate the plan to review:

- if `$request` names a plan, resolve `.ulpi/plans/<name>.md`
- if `$request` provides a direct path, use it
- if no target is provided, select the most recently modified `.md` plan under `.ulpi/plans/`

Then:

- read the full markdown plan
- read the companion JSON file if present
- extract title, mode, task count, task IDs, file paths, and dependency summary
- determine whether review mode is `FULL` or `QUICK`

Load `references/review-rubric.md` for:

- mode selection rules
- section requirements per mode
- verdict criteria

Stop early if:

- no plan exists
- the markdown plan cannot be read
- the review target is too small for formal founder review and should just be executed directly

**Success criteria**: The target plan and review mode are explicit before detailed review starts.

## Step 1: Run the codebase reality check

Verify the plan against the actual repository:

- every `filesToModify` path exists
- every `filesToCreate` path has a valid parent path or prior creator task
- markdown and JSON agree on task IDs, file paths, and execution meaning
- claimed reuse actually exists locally
- the plan is not building functionality that already exists
- if the plan introduces a public SQL, API, or CLI surface, the plan pins the real signature or example rather than hand-waving it

Load `references/review-checklist.md` and complete Section 1 in full.

**Success criteria**: The plan's file paths, reuse claims, and artifact consistency are reality-checked against the repo.

## Step 2: Challenge scope and strategy

Review:

- whether plan mode matches actual scope
- whether every task serves the stated goal
- whether non-goals are credible
- whether the ship cut is believable
- whether hidden prerequisites or scope creep exist

Load `references/review-checklist.md` and complete Section 2.

**Success criteria**: Scope, mode, and minimum shippable cut are defensible.

## Step 3: Audit architecture, contracts, and dependencies

Review:

- architecture diagram completeness
- task-to-diagram consistency
- producer/consumer contract clarity
- dependency JSON realism
- execution-summary consistency
- ownership of shared wiring points such as routers, registries, manifests, startup hooks, or export barrels
- semantic safety for rewrites, planners, optimizers, filters, or query composition

Load `references/review-checklist.md` and complete Section 3.

If review mode is `QUICK`, skip directly to Step 6 after this step.

**Success criteria**: The plan's architecture and dependency story is coherent and executable.

## Step 4: Audit risk, recovery, and degraded-mode safety

For `FULL` review only, challenge:

- failure-mode coverage
- mitigation quality
- rollback or containment strategy
- degraded-mode semantics
- malformed-output or upstream-failure handling

Load `references/review-checklist.md` and complete Section 4.

**Success criteria**: Critical risks are covered by actionable mitigations rather than vague warnings.

## Step 5: Audit test coverage and execution feasibility

For `FULL` review only, challenge:

- completeness of the test coverage map
- appropriateness of test types
- edge-case coverage in acceptance criteria
- security-sensitive path coverage
- DAG efficiency
- agent matching
- effort calibration
- P0 foundation honesty
- write-scope collisions or hidden overlap

Load `references/review-checklist.md` and complete Sections 5 and 6.

**Success criteria**: The plan is testable, executable, and not obviously over-constrained or under-specified.

## Step 6: Score sections and deliver the verdict

Use `references/review-rubric.md` to:

- score each reviewed section as `PASS`, `WARN`, or `FAIL`
- classify findings as `BLOCK`, `CONCERN`, or `OBSERVATION`
- determine `APPROVE`, `REVISE`, or `REJECT`

Then render a concise founder-review report that includes:

- plan title and mode
- verdict
- section summary table
- blocking issues
- concerns
- observations
- recommended plan changes when revision is required

Do not ask the user procedural questions at the end of the review. Deliver the audit and let the main thread decide what happens next.

**Success criteria**: The verdict follows directly from evidence-backed findings and the rubric.

## Guardrails

- Do not modify the plan file as part of this skill.
- Do not rubber-stamp a non-trivial plan.
- Do not invent findings; a clean section can legitimately pass.
- Do not add `disable-model-invocation`; this skill should remain callable when the user asks for plan review.
- Do not add `paths:`; this is a generic review workflow.
- Do not keep giant examples, quality scorecards, or gate tables inline in `SKILL.md`.
- Do not use `AskUserQuestion` as a substitute for a verdict.
- Do not forget that this skill runs best as a forked review workflow with separate reasoning budget.

## When To Load References

- `references/personality.md`
  Use at session start for review persona, traits, and communication style.

- `references/review-checklist.md`
  Use for section-by-section audit checks and evidence requirements.

- `references/review-rubric.md`
  Use for mode selection, verdict rules, section scoring, and finding classification (BLOCK/CONCERN/OBSERVATION gate tables).

## Output Contract

Report:

1. reviewed plan and selected mode
2. verdict
3. section status summary
4. blocking issues
5. concerns
6. observations
7. required plan changes when applicable
