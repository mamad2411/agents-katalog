---
name: llm-evals
description: Builds evaluation suites for LLM features and agents - error analysis on real outputs, pass criteria, code-based checks, calibrated LLM-as-judge graders, dataset splits, CI regression runs, and noise-aware comparisons with cost and latency. Use when testing prompts or models, comparing model or prompt changes, setting up LLM regression tests, writing a judge prompt, or when someone asks "is this LLM feature good enough to ship". Not for classic ML model training metrics (use ml-experiments).
license: MIT
---

# LLM Evals

You can't improve what you only vibe-check. Read real outputs first, turn what you see into specific pass/fail criteria, check with code wherever possible, and trust an LLM judge only after it agrees with humans.

## When to use

- A prompt, model, retrieval setup or agent is about to change and you need to know if it got better or worse.
- Shipping an LLM feature and someone needs evidence it works.
- Production complaints about an LLM feature with no way to reproduce or measure them.

## Workflow

1. **Gather real inputs.** Production logs, user research, support tickets, or (if none exist yet) inputs written by people who know the domain. Add synthetic inputs only to fill gaps you can name.
2. **Run the current system and read the outputs.** At least 50, ideally 100+. Write a short note on every bad output.
3. **Cluster the notes into failure modes** ("ignores the date range", "invents a policy", "wrong JSON field", "too long"). Count them. These become your criteria; don't start from a generic metric list.
4. **Define pass criteria per failure mode**, each one binary and checkable. Prefer one criterion per check over a single "quality 1-10" score.
5. **Implement checks, cheapest first**: code checks, then reference comparisons, then LLM judges (see "Choosing a check").
6. **Calibrate every judge** against human labels before using it (see "LLM-as-judge").
7. **Split the data**: a dev set you iterate on and a held-out test set you run rarely, so you don't overfit the prompt to the eval.
8. **Automate**: one command runs the suite and writes a report with per-criterion pass rates, cost and latency. Run it in CI on every prompt, model or pipeline change.
9. **Compare against the baseline with noise in mind** (see "Noise and sample size"). Ship only on a real improvement with no important regressions.
10. **Keep it alive**: add every production failure as a new case.

## Error analysis in practice

Keep a simple table while reading outputs, then count:

| Case | Output summary | Note | Failure mode |
|---|---|---|---|
| support-0133 | Says pausing is impossible | Contradicts billing doc | Unsupported claim |
| support-0140 | Correct, 400 words | User asked yes/no | Too long |
| extract-0042 | Total = 1.24 | Misread comma separator | Number parsing |

- Write notes in your own words first; name failure modes only after 30+ notes, so categories come from data.
- Fix obvious bugs (wrong prompt variable, missing context) right away; build checks for failure modes that will recur.
- Repeat error analysis after every significant change. New failure modes appear when old ones are fixed.

## Choosing a check

| Check type | Use for | Examples |
|---|---|---|
| Code assertions | Anything a program can decide | JSON parses and matches schema, required fields present, length limits, regex for forbidden content, valid citations, SQL runs, tests pass, tool called with right arguments |
| Reference match | Short answers with a known truth | Exact or normalized match, numeric tolerance, set overlap for extracted entities |
| Similarity to reference | Rarely; weak signal | Embedding or token overlap. Treat as a hint, not a grade. |
| LLM-as-judge | Subjective or semantic criteria | Faithfulness to sources, follows tone guide, answers the actual question, no unsupported claims |
| Human review | Calibration, high-stakes or new failure modes | Labeling a sample, reviewing judge disagreements |

Rule: if a criterion can be checked with code, don't use a judge.

## LLM-as-judge

- **One criterion per judge call**, written as a yes/no question with explicit definitions and examples of pass and fail. Binary or a 3-point scale; avoid 1-10 scales, which drift and cluster.
- **Ask for a short rationale before the verdict**, and return structured output (`{"reasoning": "...", "pass": true}`).
- **Give the judge what it needs**: the input, the output, and the reference answer or source passages when relevant.
- **Calibrate**: label 50-100 outputs by hand (ideally two people; resolve disagreements). Measure judge agreement with humans, especially on failures (true positive and true negative rates, not just accuracy). Iterate on the judge prompt until it agrees well enough for the decision you're making. Keep the calibration set separate from the examples inside the judge prompt.
- **Biases to control**: position bias in pairwise comparisons (run both orders, count a win only if consistent), verbosity bias (longer looks better; state that length is not a criterion), self-preference (a judge may favor outputs from its own model family; consider a different model as judge).
- **Pairwise comparisons** ("which of A or B better satisfies X") are more reliable than absolute scores when comparing two versions.
- Re-calibrate when you change the judge prompt or judge model.

Template: [references/judge-prompt-template.md](references/judge-prompt-template.md).

## Dataset design

- Cases in a versioned file (JSONL or YAML) in the repo, each with an ID, input, optional reference, tags, and which checks apply. Format: [references/eval-case-format.md](references/eval-case-format.md).
- Cover: common cases (weighted like real traffic), known hard cases, edge cases (empty, huge, malformed, other language), adversarial cases (prompt injection, jailbreak attempts, out-of-scope requests), and cases where the correct behavior is to refuse or say "I don't know".
- Tag cases by feature, difficulty and failure mode so you can report pass rates per slice.
- Keep a held-out test set. If you tune the prompt while looking at a case, that case is now dev data.

## Noise and sample size

- LLM outputs vary between runs. Before comparing versions, run the baseline twice: the difference between those runs is your noise floor.
- With small sets, differences of a few percentage points are often noise. With 100 binary cases, a 95% confidence interval on a pass rate is roughly plus or minus 10 points at 50% pass rate. Report intervals or run multiple trials per case.
- Compare on the same cases (paired comparison) and look at which cases flipped, not just the totals.
- Fix sampling settings (temperature, seed if supported) for eval runs, and record them.

## Report every run with

- Per-criterion pass rate, overall pass rate, and slice breakdowns.
- Cost (tokens or money) and latency (p50/p95) per case, because a quality win that triples cost may not ship.
- Prompt version, model, settings, dataset version, and git commit.
- A list of cases that changed from pass to fail versus the baseline.

## CI integration

- Fast suite (code checks plus a small set of judge checks) on every change to prompts, model config, retrieval or tool definitions.
- Full suite nightly or before release.
- Fail the build on a drop beyond the noise floor in any blocking criterion, or on any failure in a "must never fail" set (safety, data leakage, format).
- Cache model responses keyed by prompt version and input to keep reruns cheap when only checks change.

## Anti-patterns

- **Metrics before reading outputs** - generic "helpfulness" and "coherence" scores that don't match what actually goes wrong.
- **Uncalibrated judges** - an LLM judge nobody compared with human labels.
- **1-10 scales** - noisy and hard to act on. Use binary criteria.
- **Overfitting the eval** - tuning on the same cases you report.
- **Only happy paths** - no adversarial, refusal or no-answer cases.
- **Declaring victory on a 2-point gain** with 40 cases and one run.
- **Quality-only reports** that hide cost and latency regressions.
- **Eval data drifting out of date** - never adding production failures.

## Done when

- Failure modes come from reading real outputs, and each has a binary pass criterion.
- Code checks cover every criterion a program can decide; each judge is calibrated against human labels with agreement recorded.
- Dev and held-out sets are separate and versioned in the repo.
- One command produces a report with per-criterion pass rates, cost, latency and flipped cases, and CI runs it on relevant changes.
- Comparisons account for run-to-run noise.

## References

- [references/judge-prompt-template.md](references/judge-prompt-template.md) - read when writing or fixing an LLM judge.
- [references/eval-case-format.md](references/eval-case-format.md) - read when creating the dataset file or eval runner.
