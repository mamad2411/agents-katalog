---
name: llm-evals
description: Build and run eval harnesses for features that call a model, with a keyless mock lane in CI, a budget-capped live lane behind a key gate, thresholds in a versioned file, and judge scoring. Use when adding or changing evals, testing a prompt or model swap, gating a release on output quality, or investigating a quality regression. Runs scripts/check_thresholds.py.
---

# llm-evals

Without evals, a prompt change is a guess and a model swap is a leap. With them, both become a diff you can read.

## Gate a run

```bash
python <skill>/scripts/check_thresholds.py results.json --thresholds evals/thresholds.json
```

Add `--baseline evals/baseline.json` to catch regressions that still clear the floor. A metric that stays above its minimum while dropping four points from last week is the failure that absolute thresholds miss.

Exit code is 1 on any failure or any threshold whose metric is missing from the results, unless that threshold is `warn_only`.

## Two lanes

**Mock lane.** Runs against the mock provider from [llm-pipeline](../llm-pipeline/SKILL.md). No key, no cost, deterministic, runs on every commit in CI. It tests the pipeline: schema conformance, error paths, stage ordering, that the shapes hold. It cannot test output quality, and pretending otherwise is the main way eval suites become theatre.

**Live lane.** Runs against the real provider. Key-gated, so it is skipped rather than failed when no key is present. Budget-capped with a hard token or dollar ceiling that aborts the run. Local and on-demand, not on every commit.

Keep them separate. A suite that needs a key to run is a suite that stops running.

## Thresholds are a versioned file

Put them in `evals/thresholds.json`, commit them, and change them in their own commit with a reason in the message. A threshold quietly lowered to make CI green is worse than no threshold.

```json
{
  "accuracy":         { "min": 0.82, "max_drop": 0.03 },
  "latency_p95_ms":   { "max": 4000 },
  "cost_per_run_usd": { "max": 0.35 },
  "refusal_rate":     { "max": 0.02, "warn_only": true }
}
```

The checker also lists metrics you report but do not gate. Either add a threshold or stop reporting them, because an ungated metric is decoration.

## What to measure

Always include cost and latency alongside quality. A prompt change that lifts accuracy two points and triples cost is a decision, not a win, and you cannot make that call without both numbers on the same page.

Measure the thing the product promises. If the product is a drafting tool for a human reviewer, measure agreement with the reviewer, not fluency.

## Detail

Read [references/harness.md](references/harness.md) when building the dataset, writing a judge, or running an A/B. It covers dataset design, judge prompts and their failure modes, sample size against variance, and budget capping.

## Interpreting a failure

Before changing anything, re-run. LLM evals are noisy, and a single failing run on a small set is often variance rather than regression. If the suite is too small for that to be distinguishable, the suite is too small.

Prose follows [prose-guard's rules](../prose-guard/references/rules.md).
