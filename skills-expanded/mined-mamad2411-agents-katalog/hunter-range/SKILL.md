---
name: hunter-range
description: >-
  The measurement law for Hunter changes: no improvement claim is accepted
  without a paired Range run. Defines the paired-comparison procedure (same
  corpus revision, same seeds, same budget, exactly one variable changed),
  minimum run counts for a stochastic system and why single-run comparisons are
  meaningless, the honest-regression report, and the rule that a Range result is
  itself governed by hunter-doctrine. Load this whenever about to claim a prompt,
  skill, oracle, model, or ladder-threshold change made Hunter better or worse,
  before merging any change to a skill pack, before promoting a model, when
  someone says "this improved recall", "this is faster", "this reduced false
  positives", or when tuning a ladder threshold. Reads results from and hands
  off to docs/05-the-range.md (the harness design).
allowed-tools: Read, Bash, Write
argument-hint: "<baseline-commit> <candidate-commit> [suite]"
---

# Hunter Range

`hunter-doctrine` is loaded. This skill applies its Law to Hunter itself: a claim
that a change improved Hunter is a claim, and an unproven claim is noise. The
evidence that settles it is a paired Range run, not a benchmark you ran once and
liked.

## The measurement law

> **No improvement claim is accepted without a Range run. A single-run comparison
> is not evidence. The variable under test is exactly one.**

Hunter is stochastic: the model samples, agents take different tool paths, the
scheduler interleaves. Run the identical configuration twice and recall, cost, and
time-to-first-find will differ. Therefore a change that "raised recall from 34/50
to 37/50" in one run each proves nothing — that delta is inside the noise band of a
single configuration. Anyone who reports a one-run-each comparison has reported a
coin flip and called it a trend.

Your job here is to produce a verdict, from the closed set, on whether the
candidate beat the baseline — with a confidence interval, not a point.

## Inputs

- `baseline` — a commit / skill-pack digest representing current accepted Hunter.
- `candidate` — a commit / digest differing from baseline in **exactly one**
  variable (one prompt, one skill's body, one oracle, one model id, one ladder
  threshold). If more than one thing changed, you cannot attribute the delta.
  Split the change or bisect; do not proceed.
- `suite` — a pinned Range corpus revision (see `docs/05-the-range.md` §ground
  truth). Same revision for both arms.
- A run manifest per arm (see `docs/05-the-range.md` §isolated run contract). Every
  input except the one variable is byte-pinned and recorded.

If any pin is missing from either manifest, stop. An unpinned input invalidates the
comparison — you would be measuring the change plus whatever drifted.

## The paired-comparison procedure

The two arms differ in one variable and nothing else. Same corpus revision, same
seed set, same per-hunt budget, same container image digest, same model+SDK+CLI
versions on every axis you are not testing. When you are testing the model itself,
the model is the one variable and every other pin holds.

1. Draw a fixed seed set `S = {s_1 .. s_n}` (see run counts below). Both arms run
   the whole corpus under every seed in `S`. Seeds are shared, not independently
   drawn per arm — this is what makes it *paired*. Pairing removes per-seed
   corpus difficulty as a confounder and is why you need far fewer runs than an
   unpaired test.
2. Run baseline over `S`. Run candidate over `S`. Record every arm's per-seed
   metric vector to the results store.
3. Compare **per seed**: `delta_i = metric(candidate, s_i) − metric(baseline, s_i)`.
   The statistic is the distribution of `delta_i`, not the difference of means of
   two separate runs.
4. Report the median delta and its interval, plus the win/loss/tie count across
   seeds (`candidate won 7/10 seeds, lost 2/10, tied 1/10`).

Never average the two arms into two scalars and subtract. That discards the pairing
and reinflates the run count you would need.

## Minimum run counts

`n` is the number of seeds per arm. Stochastic variance sets the floor.

| Decision | Minimum `n` per arm | Why |
|---|---|---|
| Merge a skill/prompt/oracle change | 10 | Paired design; below 10 the interval on the median delta is too wide to separate signal from sampling. |
| Promote or swap the model | 20 | Model change perturbs every stage; variance is larger, so the floor rises. |
| Tune a ladder threshold | 10, plus the full precision/recall pair reported | A threshold trades recall against false positives; one number cannot show the trade. |
| Ship a full skill-pack version bump | 20 | Composite of many changes; treat with the widest floor. |

Below these counts, the only honest verdict is `VERIFICATION-PENDING` — the run is
not yet evidence. Do not merge on a hunch that "more runs would confirm it."

A result is significant only when the delta interval excludes zero on the primary
composite (`docs/05-the-range.md` §metric set). If the interval straddles zero, the
honest verdict is a tie, reported as `PASS WITH ISSUES` (no measurable improvement)
— not `PASS`, and never rounded up.

## Output schema

Write `range/results/<baseline>__<candidate>/verdict.json`:

```json
{
  "schema_version": 1,
  "baseline": {"commit": "…", "pack_digest": "…", "manifest": "range/…/baseline.manifest.json"},
  "candidate": {"commit": "…", "pack_digest": "…", "manifest": "range/…/candidate.manifest.json"},
  "variable_changed": "skill:no-mocking-validation-gates body",
  "suite_revision": "corpus@8f2a1c",
  "seeds": [101,102,103,104,105,106,107,108,109,110],
  "n_per_arm": 10,
  "primary_composite": "find_quality",
  "per_seed_delta": [{"seed":101,"delta":0.04}, "…"],
  "median_delta": 0.031,
  "delta_interval_95": [0.006, 0.058],
  "excludes_zero": true,
  "win_loss_tie": {"win": 7, "loss": 2, "tie": 1},
  "secondary": {
    "recall": {"baseline": "34/50", "candidate": "38/50", "median_delta": 0.06, "interval_95": [0.01,0.11]},
    "false_positive_rate": {"baseline": 0.11, "candidate": 0.10, "interval_95": [-0.03,0.02]},
    "cost_per_find_usd": {"baseline": 0.42, "candidate": 0.49, "interval_95": [0.01,0.14]},
    "wall_clock_p50": {"baseline": "9m 40s", "candidate": "9m 55s"}
  },
  "coverage": {"corpus_seeds_run": "50/50", "dark_seeds": []},
  "verdict": "PASS WITH ISSUES",
  "verdict_reason": "find_quality improved 0.031 [0.006,0.058]; cost_per_find rose 0.07 [0.01,0.14] — improvement is real but not free",
  "replay": {"baseline_replays": "50/50", "candidate_replays": "50/50"}
}
```

`verdict` comes from the doctrine's closed set. A Range verdict is a report and
obeys report rules: it sits next to a coverage fraction, and it never renders green
without the stored per-seed artifacts behind it.

## How to report a regression honestly

A regression is a result, not a failure of the exercise. Suppressing it is the
anti-fabrication law violated against Hunter's own history.

- If the candidate loses on the primary composite (delta interval below zero),
  verdict is `FAIL`. State the median regression and the interval. Do not merge.
- If the candidate wins the primary but loses a secondary the operator cares about
  (cost, latency, false-positive rate), verdict is `PASS WITH ISSUES` with the
  trade named explicitly, as in the schema above. The operator decides the trade;
  you do not hide it to make the merge clean.
- If a change you personally authored regresses, you report it with the same
  numbers you would report someone else's. Never re-run to fish for a seed set that
  wins. Never widen the interval by dropping "outlier" seeds. Dropping a seed is
  editing the corpus, which invalidates the pairing.
- A "fixed" regression is itself a change: it needs its own paired Range run
  against the last-good baseline before the fix is accepted.

## The Range result is subject to the doctrine

Everything `hunter-doctrine` requires of a hunt applies to a Range run:

- **Evidence over assertion.** The verdict cites the per-seed artifacts. "It felt
  faster" is not a Range result.
- **Coverage honesty.** If some corpus seeds could not run in one arm, those seeds
  are dark in that arm; the comparison is `PASS (LIMITED COVERAGE)` at best and
  lists them. You may not compare a 50/50 arm against a 47/50 arm and call it even.
- **No fabrication.** Do not invent seeds you did not run or intervals you did not
  compute. If `n` is below the floor, say `VERIFICATION-PENDING`.
- **Anti-mock, turned inward.** A candidate that "improves recall" by weakening the
  promotion gate (accepting one-shot observations as Finds) has not improved Hunter
  — it has disabled the product. Check that the candidate still enforces the
  Sign→Find contract before crediting any recall gain. A recall gain paired with a
  precision drop that traces to a weakened ladder is `mocking_rejected`, reported
  against the change.

## Handoff

The harness that produces the runs, the ground-truth sourcing, the metric
definitions, the isolated-run contract, CI gating, and A/B + ablation procedure all
live in `docs/05-the-range.md`. Read it before running. This skill governs the
*decision*; that doc governs the *machinery*. A Range verdict written by this skill
is appended to the per-commit leaderboard defined there.

## Self-check before emitting a Range verdict

- [ ] Exactly one variable differs between the arms; both manifests confirm it
- [ ] Same corpus revision, same shared seed set, same budgets, same non-tested pins
- [ ] `n` meets or exceeds the floor for this decision class
- [ ] Comparison is paired per seed, not mean-minus-mean
- [ ] Delta interval reported; zero-crossing decides significance
- [ ] Regression, if any, reported with the same rigour as an improvement
- [ ] Candidate still enforces the Sign→Find contract (recall not bought by weakening)
- [ ] Verdict from the closed set, beside a coverage fraction, with replay counts
