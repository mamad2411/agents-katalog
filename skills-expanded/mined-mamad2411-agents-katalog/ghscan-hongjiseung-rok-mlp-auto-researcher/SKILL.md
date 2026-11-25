# SKILL: tea_time_with_reading_poem

## Purpose
A bounded, deterministic pause-and-review layer. It summarizes the current
stage, audits benchmark-specific lock-in, compares two or three reversible
paths, and drafts any consequential owner questions. A public-domain poem and
seeded provocations provide a lightweight self-critique reset.

## Supported use cases
- Immediately after local-state recovery.
- After checkpoint comparison and E0 diagnostics.
- Before preregistration freeze or Colab staging launch.
- Before retry/pivot decisions after a staged failure.

## Non-goals (read these twice)
- **Not evidence.** Output is agent-text class under the provenance policy:
  the skill registers `reflection` artifacts but never claims, and nothing it
  produces may back a numerical claim, table, or figure.
- No label, test-metric-detail, secret, or arbitrary artifact input.
- Not a metric source, not an evaluation, never inserted into claim chains;
  `claim_verification` ignores `reflection` artifacts.
- Not an LLM call: v0 is deterministic; the poem and techniques are fixtures.

## Typed inputs — `schema.TeaTimeInput`
`focus_question`, approved `trigger`, current-stage purpose, benchmark role,
reusable and benchmark-specific component lists, two or three bounded
alternatives, optional structured owner-question drafts, `n_provocations`,
and optional `poem_key`. The compatibility `data_path` field accepts only null.

## Typed outputs — `schema.TeaTimeOutput`
`report_artifact`/`report_path` (`tea_time_report.md`),
`reframings_artifact`/`reframings_path` (`reframings.json`), `poem_key`,
`techniques`, `n_provocations`, trigger, purpose summary, benchmark-overfitting
risk, alternative ids, and owner-question count.

## Required dependencies
`numpy` (seeded rng + alternative views). Poem corpus is in-repo
(`poems.py`, all public domain).

## Preconditions
Writable `ctx.step_dir`. No research-data or secret file is accepted.

## Validation rules (`validators.py`)
- Unknown `poem_key` → `VALIDATION_ERROR`, non-retryable.
- A non-null `data_path` is rejected by the input schema.
- Restricted payload keys fail before serialization.
- Post-condition: the claim count is unchanged, enforced in-code
  (`UNSUPPORTED_CLAIM` if violated) and by tests.

## Failure taxonomy
`VALIDATION_ERROR`, `UNSUPPORTED_CLAIM` (invariant guard; unreachable in
correct code).

## Retry and recovery policy
All failures are non-retryable input problems; the executor escalates.

## Produced artifacts
`steps/<step_id>/reframings.json` and `steps/<step_id>/tea_time_report.md`,
both kind `reflection`, byte-deterministic for a fixed seed and inputs.

## Provenance fields
Seed (via executor), trigger, purpose, audit inputs/rule, alternative paths,
question drafts, poem key, technique ids, and `evidence_class: agent_text`.

## Cost class / permission level
`trivial` / `auto`.

## Minimal example
`examples/example_input.json`.

## Correctness tests
`tests/test_tea_time.py`: byte determinism, seed sensitivity, required pause
sections, benchmark-lock-in audit, zero-claim invariant, data-artifact denial,
restricted-payload denial, unknown poem, and input bounds.
