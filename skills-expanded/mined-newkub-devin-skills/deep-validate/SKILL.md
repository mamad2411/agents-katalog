---
name: deep-validate
description: Detailed multi-dimension validation: cross-reference, type safety, runtime, security, compliance
argument-hint: "[scope|correctness|type-safety|quality|security|compliance|cross-reference]"
related:
  - deep-thinking
  - deep-analyze
  - rethink
  - run-test
  - deep-review-codebase
  - run-typecheck
  - report
  - suggest-next-action
  - resolve-errors
  - run-check
  - run-build
  - run-verify

---

## Goal

Validate in detail across many dimensions: correctness, type safety, runtime, security, compliance, cross-reference, with severity ratings

## Scope

Use for validation that needs high thoroughness, covering every dimension of the system

- If you need to verify after `/merge` or parallel work, see `references/post-merge-verify.md`
- To validate tests use `/run-test`; to validate a review use `/deep-review-codebase`

## Execute

Step dependencies: each step depends on the previous one in order (Step N depends on Step N-1)

### 1. Define Validation Scope

> Goal: Define Validation Scope

Set the validation scope based on what must be checked

- Start with `/deep-thinking`: always analyze the problem and validation goal before defining scope
- Identify what to validate: code, documentation, design, decision, workflow, configuration
- Identify the relevant dimensions: correctness, type safety, runtime, security, compliance, cross-reference
- Set success criteria for each dimension
- Identify the standards or principles used as the criteria
- If the scope is unknown, ask the user

### Workflows

> Goal: dispatch to the dimension workflow matching the argument — or run every dimension if none is given

| Dimension/Argument | Workflow |
|--------------------|----------|
| `correctness` | `workflows/check-correctness/SKILL.md` — requirements, logic, edge cases, error handling |
| `type-safety`, `types` | `workflows/check-type-safety/SKILL.md` — typecheck, `any`/`@ts-ignore`, type flow |
| `quality` | `workflows/check-quality/SKILL.md` — readability, consistency, docs, best practices |
| `security` | `workflows/check-security/SKILL.md` — input validation, auth, secrets, injection |
| `compliance` | `workflows/check-compliance/SKILL.md` — requirements fit, conventions, regulatory |
| `cross-reference`, `refs` | `workflows/check-cross-references/SKILL.md` — config/env, module refs, API contracts, docs |
| `report`, `findings` | `workflows/report-findings/SKILL.md` — merge findings from all dimensions into a severity matrix |

1. If the argument names a single dimension → read `workflows/check-<dim>/SKILL.md` and follow its flow — skip the other dimensions but still do Step 8 (Report)
2. If none is given → do Steps 2-7 in order, each step reading and executing the matching workflow

### 2. Check Correctness

> Goal: Check Correctness

Follow `workflows/check-correctness/SKILL.md` — check requirements, logic, edge cases, error handling, recording findings + severity

### 3. Check Type Safety

> Goal: Check Type Safety

Follow `workflows/check-type-safety/SKILL.md` — typecheck, weak types (`any`/`@ts-ignore`), type flow, recording findings + severity

### 4. Check Quality

> Goal: Check Quality

Follow `workflows/check-quality/SKILL.md` — readability, consistency, docs, conventions, recording findings + severity

### 5. Check Security

> Goal: Check Security

Follow `workflows/check-security/SKILL.md` — input validation, auth, secrets, injection, rate limiting, recording findings + severity

### 6. Check Compliance

> Goal: Check Compliance

Follow `workflows/check-compliance/SKILL.md` — requirements fit, conventions (`AGENTS.md`), regulatory, recording findings + severity

### 7. Cross-Reference Validation

> Goal: Cross-Reference Validation

Follow `workflows/check-cross-references/SKILL.md` — config/env, module refs, API contracts, docs, recording findings + severity

### 8. Report And Suggest

> Goal: Report And Suggest

Follow `workflows/report-findings/SKILL.md` — merge findings into a severity matrix with recommendations, then run `/suggest-next-action`

## Rules

### 1. Validation Approach

- Check strictly and systematically; always start with `/deep-thinking`
- If scope/root cause is unclear → gather evidence like `/deep-analyze` before validating
- Consider the relevant context and constraints
- Use clear criteria when checking
- Every finding must have evidence (file path, line number, code snippet)

### 2. Severity Classification

- Critical: blocking production, security vulnerability, data loss risk
- High: core functionality at risk, significant issue
- Medium: code quality issue, minor gap
- Low: cosmetic, naming convention, minor improvement

### 3. Dimension Coverage

- Cover every dimension relevant to what is being checked
- If there is no database, skip database validation
- If there is no API, skip API validation
- Adjust scope to the characteristics of what is being checked

### 4. Feedback Style

- Give clear, constructive feedback
- Always note what is already good
- Give concrete, actionable suggestions
- State the improvement priority (Critical, High, Medium, Low)

### 5. Independence

- Run `/deep-validate` only; do not modify code during the run
- Keep the validation process separate from the fix process
- If a fix is needed, run `/resolve-errors` after validating

- Use /rethink if needed
- Use /run-check if needed
- Use /run-build if needed
- Use /run-test all if needed
- Use /run-typecheck if needed

## Subagents

> Goal: independent work that can be spawned in parallel — the profile lives in this section, no separate file needed

### dimension-validator — validate only one dimension of the scope and return a verdict with evidence

- **Inputs**: `dimension` (`tests`/`lint`/`types`/`docs`/`refs`/`security`/`runtime`), `scope` (path or validation target, e.g. workspace, file list, feature), `success-criteria` (optional: the parent's passing criteria, e.g. `typecheck 0 errors`), `ecosystem` (optional: `bun`/`pnpm`/`cargo` to pick the right commands)
- **Tools**: `read`, `grep`, `find_file_by_name`, `exec` (run validation commands such as `bun run test`, `bun run lint`, `bun run typecheck`)
- **Execute**:
  1. Determine the `dimension`'s command/checklist from the detected ecosystem, e.g. `types` → typecheck, `tests` → test suite, `refs` → imports/links
  2. Run the dimension's primary check, capturing the raw output and exit code
  3. Check the dimension's supplementary items, e.g. `types` → `any`, `@ts-ignore`; `docs` → README drift; `refs` → broken imports
  4. Classify severity per failure: `critical`/`high`/`medium`/`low` with `file:line` evidence
  5. Summarize the dimension verdict: `pass` / `fail` / `skip` (this dimension isn't in scope)
- **Output**: a `| No. | Check | Result | Severity | Evidence |` table (e.g. `1` | `bun run typecheck` | `fail` | `high` | `src/x.ts:42`); the first line is the `pass`/`fail`/`skip` verdict with a short reason; always attach the commands run and their exit codes — the verdict must be reproducible; if a check cannot run → return `error` with the cause, never report it as `pass`
- **Constraints**: read-only — `edit`/`write` forbidden; validate only the assigned dimension, never cross into another; report only — never modify code/config/tests and never run auto-fixes (`--fix`, `--write`); every failure needs evidence from real output, don't guess from code without running it; if a dimension doesn't apply to the scope → return `skip` with a reason, don't fabricate results; on an infra error → retry at most 3 times then return `error`

## Expected Outcome

- Correctness verified across every dimension
- Type safety verified
- Quality assessed
- Security verified
- Compliance with standards and constraints verified
- All cross-references correct
- A summary table: dimension, finding, severity, location, recommendation
- Actionable, prioritized recommendations
