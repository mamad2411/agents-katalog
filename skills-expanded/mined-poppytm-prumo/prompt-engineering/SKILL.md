# Prompt Engineering & Evaluation

## Purpose
Author, version, and evaluate system prompts and few-shot examples with an eval harness, scored regression gates, and prompt-diff review so prompt changes ship with measured quality deltas instead of vibes.

## Use when
- Writing or revising system prompts, agent instructions, or skill page directives.
- Adding few-shot examples to steer output format, tone, or tool-use discipline.
- Building or extending an eval set that scores prompt behavior (format adherence, refusal correctness, tool-call validity).
- Auditing a prompt regression: output quality dropped after a prompt edit and the cause must be isolated.

## Do not use when
- Selecting runtime context for a task (use `lean-progressive-context`).
- Compressing loaded context (use `context-optimization`).
- Tuning model weights, sampling infrastructure, or provider routing policy.

## Required context
- Target model and sampling config (e.g. temperature 0.2, top_p 0.9, max_tokens 2048) pinned for eval reproducibility.
- Eval set location with N gold cases (minimum 30 for format gates, 100 for behavior gates) and scoring rubric.
- Baseline scores from the current prompt version before any edit.
- Versioning location for prompts (prompts/ directory with semantic versions, e.g. triage-v3.2.0.md).

## Procedure
1. **Freeze the baseline**: run the eval harness against the current prompt with seed 42 and record pass rates per dimension (format 96%, tool-validity 91%, refusal 100%) before editing anything.
2. **Edit one variable at a time**: change a single instruction, example, or constraint per iteration; multi-variable prompt edits are undebuggable.
3. **Version the prompt**: save as prompts/triage-v3.3.0.md with a changelog line stating what changed and why; never overwrite the previous version in place.
4. **Run the regression gate**: re-run the full eval set with identical sampling config; ship only if no dimension regresses more than 2 points and the target dimension improves.
5. **Review the prompt diff**: a second reviewer checks for instruction conflicts, leaked secrets in examples, and unbounded output directives (e.g. "list all" without a cap).
6. **Record evidence and run `scripts/verify.sh`**: attach baseline vs candidate score tables and the prompt diff to the change record.

## Decision rules
- **Baseline mandatory**: no prompt edit merges without pre-change eval scores on the same harness and seed.
- **Single-variable edits**: one instruction, example, or constraint per version bump.
- **Two-point regression bar**: any dimension dropping more than 2 points blocks the merge regardless of gains elsewhere.
- **Pinned sampling for evals**: temperature, top_p, seed, and max_tokens are fixed in the harness config; ad-hoc sampling invalidates comparisons.
- **No secrets in examples**: few-shot examples use synthetic data (e.g. user id 1007, token sk-test-0000); production credentials in prompts are a security incident.

## Evidence required
- Baseline vs candidate eval score tables with identical harness config and seed.
- Versioned prompt file plus changelog line.
- Prompt diff with reviewer sign-off.
- Passing execution log from `scripts/verify.sh`.

## Output contract
- Versioned prompt file ready for rollout or rollback.
- Eval report proving no dimension regressed beyond tolerance.
- Review record with conflicts, secrets, and bounds checks.

## Stop conditions
- Candidate prompt beats baseline on the target dimension with zero regressions beyond 2 points.
- Three iterations fail to improve; freeze and escalate the eval design.
- Token budget exhausted.
- Blocked on external dependency.

## Escalation rules
- Escalate to the model owner if evals show provider-side behavior drift (same prompt, same seed, different outputs week over week).
- Escalate to security immediately if a prompt or example is found containing production secrets or customer data.
