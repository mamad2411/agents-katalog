---
name: fail-closed-eval-gate
description: "Use when a Claude Code plugin or skill change is about to merge or release and CI must block it unless the plugin measurably beats the no-plugin baseline. Fires on: 'gate this release on evals', 'fail CI if the plugin regresses', 'claude plugin eval passed but the delta is negative', 'can I trust this results.json', 'the eval run was partial, can we ship', 'set up claude plugin eval in GitHub Actions', 'my eval gate always passes'. Also use when reviewing an existing agent eval gate that cannot fail. Do not use for ordinary unit-test or lint CI, for skill-creator evals.json or promptfoo suites (claude plugin eval reads neither), or for grading one conversation by hand."
metadata:
  version: "2.0.0"
---

# Fail-closed eval gate

Cost: every `claude plugin eval` run and every judge grader is a real model call billed to your plan
or API key (`ANTHROPIC_API_KEY` in CI). Requires Claude Code v2.1.269 or later. The gate script
itself is free, offline, zero-dependency Node 18+.

## The gap this closes

`claude plugin eval` exits 0 when every case's with-plugin score meets `--threshold`. It also
measures the with-minus-without delta, and the docs say: "The with-minus-without delta is reported
but never changes the exit code". A plugin that scores 1.0 where the bare model also scores 1.0
passes while adding nothing; one that makes answers worse than no plugin passes too, if its
absolute score clears the threshold.

`scripts/delta-gate.mjs` reads the run's JSON result and fails unless the plugin beat the baseline,
the run finished, and every number it judged is comparable.

## Procedure

1. Write cases in the plugin's `evals/` directory: one directory per case with `prompt.md` and
   `graders/*.md`. Score the outcome (a `regex` over the reply or a produced file, an `llm` rubric
   with concrete PASS and FAIL conditions). Add `tool_used` with `tool: Skill` as the
   "did my skill fire" indicator; in a two-arm run it is reported but excluded from the score, so
   it cannot inflate the delta. See `evals/` in this skill for working examples.
2. Tag cases that should improve on the baseline (`tags: [delta]`) apart from no-trigger cases
   (`tags: [no-trigger]`). A no-trigger case scores the same with and without the plugin by design,
   so its delta is 0 and it belongs in a separate `--ablation none` run judged by exit code alone.
3. Run the delta cases two-armed and write the result:
   `claude plugin eval . --trust-plugin --json results.json --ablation with-without --threshold 0.8 --model <pinned> --judge-model <pinned> --no-publish --max-cost-usd 20 --tag delta`
   (target first; `--json` takes an optional path, and `--tag` takes a list, so keep it last).
4. Gate on the result: `node scripts/delta-gate.mjs results.json --min-delta 0 --min-score 0.8`.
5. Prove the gate can fail before trusting it: hand-edit one case's `delta` in a copy of
   `results.json` to `0` and confirm exit 1 names that case. An eval that has never gone red is not
   a gate. `node --test scripts/delta-gate.test.mjs` does this for the script itself.
6. Wire both steps into CI. `references/ci.md` has a complete GitHub Actions job.

## Exit codes

`claude plugin eval` (from the docs):

| Exit | Meaning |
| :- | :- |
| 0 | Every case at or above `--threshold`, every case file loaded |
| 1 | A case below threshold, a case file failed to load, no cases found, a run could not start, directory not trusted without `--trust-plugin`, or an invalid option |
| 2 | Partial run: `--max-cost-usd` ceiling hit, or the credential was rejected. `results.json` is still written with `partial: true` |
| 130 / 143 | Interrupted / terminated (for example a CI timeout) |

`delta-gate.mjs`:

| Exit | Meaning |
| :- | :- |
| 0 | Valid `schemaVersion: 1`, not partial, every case has a comparable delta, no run skipped its judge graders or ended abnormally, the required share of cases has delta above 0, `aggregates.meanDelta` above `--min-delta`, `aggregates.overallScore` at or above `--min-score`, and `casesPassed` equals `casesTotal` |
| 1 | The measurement is valid and missed the bar. Each failure line names the case, its delta and its score |
| 2 | The input cannot be trusted: missing file, malformed JSON, wrong `schemaVersion`, `partial: true`, no cases, missing counts or case scores, malformed arm runs, or a bad option |

What the gate treats as failure, and why:

- A missing `delta` (one-arm run, or arms not comparable) fails.
- `skippedPaidGraders: true` on any run fails: the docs say that run's score "isn't comparable".
- A non-null `error` on any run fails, in either arm. Rate-limit errors do not mark a suite partial;
  the run is graded on what it produced and usually scores 0, so an errored baseline run inflates
  the delta.
- An `aborted` run (a mock's `expect:` was violated) fails.
- Unknown fields are ignored, as the docs require of consumers.

## Thresholds are defaults to tune

None of these is a rule. Set them from your own score history and record why.

| Flag | Default | Where it comes from |
| :- | :- | :- |
| `--min-delta` | `0` | The weakest claim worth gating: on average the plugin beats no plugin |
| `--min-score` | `0.8` | Matches the `--threshold 0.8` in the docs' CI example; their own default threshold is 1.0 |
| `--min-positive-share` | `1.0` | Strict start: every delta case must beat baseline. Lower it (for example `0.8`) once you know which cases are noisy; flat cases are still printed as notes |

Three runs per case is the docs' default. Raise `--runs` before you tighten `--min-delta`: a delta
measured on three runs is noisy, and tightening a noisy bar trains people to rerun until green.

## Grade outcomes, not paths

Score what the plugin produced: the reply, a file, a command's recorded result. `tool_order` and
`tool_used` checks on intermediate steps break whenever the model finds a different valid route,
and they reward the route instead of the result. The one path check worth keeping is
`tool_used: Skill`, as an indicator of whether the skill fired, which the eval tool already
excludes from the score in two-arm runs.

## Do not

- Do not test `$?` in a later CI step. Each step runs in its own shell, and a step that exits
  non-zero already fails the job.
- Do not chart or approve from a `partial: true` document or a run with `skippedPaidGraders`.
- Do not leave `--model` unpinned in CI; a model rollout then looks like a plugin regression.
- Do not let a red gate be overridden by an approving comment. Make the gate job a required check.
- Do not let the spec change without the cases. Whoever owns the skill owns its evals, and every
  production failure becomes a case.

## Provenance

Verified against code.claude.com/docs/en/plugin-evals on 2026-10-02: command flags, exit codes,
JSON result fields, case layout, grader types, and the two-arm scoring exclusions.

Re-verify the JSON field names and exit codes whenever `claude --version` changes minor version,
or `schemaVersion` in a result stops being `1`. The gate refuses any other `schemaVersion` with
exit 2. The test fixtures are hand-built from
the documented schema, not captured from a real run; capture one real `results.json` and add it
as a fixture when you first run the suite.
