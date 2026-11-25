---
name: spec-crlp
description: Run a spec-driven correction loop for code that already exists by comparing the current implementation against the spec and using linter output, test failures, runtime logs, and review feedback to diagnose and fix gaps. Use this whenever code is failing checks, drifting from acceptance criteria, regressing after changes, or needs a fix-verify-repeat loop after CI, tests, logs, or review comments.
---

# Spec Correction Loop

Use this skill when implementation already exists and feedback shows a mismatch between expected and actual behavior.

This skill is about converging on correct behavior with evidence. Start from the spec, reproduce the problem, find the root cause, make the smallest coherent fix, and verify the result. Treat lint, tests, logs, CI, and review comments as signals that help narrow the gap between the implementation and the acceptance criteria.

## Repository preference override

Before starting the correction loop, look for a `SPEC.md` in the target repository root.

If it exists, treat it as the repository-specific preference layer for:

- validation commands and validation order
- setup and environment expectations
- knowledge-base location for durable findings
- cross-skill workflow conventions

If it is missing, use the built-in defaults for this skill series instead of blocking on the missing file.

If it is partial, use the fields it defines and fall back to defaults for the rest.

## Built-in defaults

When no repository root `SPEC.md` is available, use these defaults:

- validation behavior: prefer discoverable repository tooling; if no validation commands are discoverable, say validation is not configured yet
- knowledge-base location: `docs/knowledge-base/`
- context retrieval: query `spec-index` for similar symptoms, root causes, fix patterns, setup gotchas, and validation rules before correction work

## Core responsibilities

- Reconstruct the expected behavior from the current spec, acceptance criteria, or user request.
- Compare the expected behavior with actual behavior using concrete evidence.
- Trace failures to a root cause instead of patching symptoms.
- Apply focused fixes and re-run the most relevant checks.
- Surface reusable lessons that should be captured by `spec-index`.

## Context retrieval before correction

Before starting a correction loop, retrieve relevant memory through `spec-index`.

Look for:

- similar symptoms or error messages
- prior root causes
- reusable fix patterns
- setup or environment gotchas
- validation rules and known flaky checks
- component-specific pitfalls

Build retrieval queries from failing test names, CI output, stack traces, log messages, file paths, tools, frameworks, components, and observed symptoms.

Use the retrieved memory as diagnostic context, not as proof. Confirm the current root cause with local evidence before changing code.

If no relevant memory is found, say so briefly and continue. Do not block correction on an empty knowledge base.

## When this skill is not the right fit

- If the task is still ambiguous and there is no clear definition of done, switch to `spec-plan` first.
- If the main need is to store or retrieve prior decisions, fixes, or setup knowledge, use `spec-index`.
- If the user is asking for greenfield planning rather than debugging or correction, use `spec-plan`.

## Working inputs

Gather as many of these as the task provides:

- The current spec, acceptance criteria, or expected behavior.
- The repository root `SPEC.md` when present.
- Relevant memory retrieved through `spec-index`.
- Failing tests, CI output, linter diagnostics, logs, stack traces, or screenshots.
- The current code and the files most likely involved in the failure.
- Review feedback that points to a regression, missing case, or poor implementation choice.

If the expected behavior is missing, derive the minimum workable acceptance criteria from the conversation and say that you are doing so. If that would be risky, hand off to `spec-plan`.

## Correction loop

1. Restate the target behavior in observable terms.
2. Read the repository root `SPEC.md` when present and apply the built-in defaults for anything it does not define.
3. Retrieve relevant memory through `spec-index`.
4. Reproduce or localize the failure using the strongest available signal.
5. Classify the signal: spec mismatch, lint issue, test failure, runtime bug, environment issue, or review concern.
6. Inspect the code path that explains the failure.
7. Identify the root cause and explain why it produces the observed behavior, using memory only when local evidence supports it.
8. Implement the smallest coherent change that fixes the root cause.
9. Re-run the most relevant validation steps defined by the repository root `SPEC.md` when present, otherwise use the built-in default behavior and discoverable repo tooling.
10. Summarize the outcome, residual risk, relevant memory used, and any new knowledge worth persisting.

## Preferred output structure

Prefer this structure unless the user asks for something lighter:

```markdown
# Correction Summary
## Expected Behavior
## Observed Behavior
## Relevant Memory
## Root Cause
## Fix
## Validation
## Residual Risk
## Memory To Capture
```

## Good habits

- Use the spec as the source of truth whenever possible.
- Retrieve relevant memory before debugging so prior root causes and setup gotchas are not missed.
- Prefer narrow, testable fixes over broad rewrites.
- Keep cause and effect explicit.
- Validate with the checks most likely to catch the same issue again.
- Prefer validation commands from the repository root `SPEC.md` when present, otherwise use the built-in default behavior instead of ad hoc command choices.
- If a failure comes from missing setup or environment assumptions, state that clearly and include the concrete prerequisite.

## Avoid

- Silent fallbacks that hide the real failure.
- Cosmetic fixes that do not address the root cause.
- Expanding scope into replanning when the real problem is local and diagnosable.
- Treating unverified guesses as confirmed causes.

## Handoffs

- Hand off to `spec-plan` when the acceptance criteria are unclear, conflicting, or incomplete.
- Hand off to `spec-index` when you confirm a reusable root cause, setup rule, fix pattern, or debugging lesson.
- Recommend updates to a repository root `SPEC.md` when repeated correction work exposes a repository-specific validation or setup convention that should become explicit.

## Example requests

- "The feature mostly works, but the tests are failing after the refactor. Please fix it against the original acceptance criteria."
- "CI says the API contract is broken. Compare the implementation with the spec and close the gap."
- "This PR got review comments about a regression. Diagnose the root cause and iterate until the behavior matches the intended flow."
