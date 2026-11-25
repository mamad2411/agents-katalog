---
name: ai-eval
description: LLM evaluation specialist. Auto-invoked when eval harnesses are being built, regression suites are designed, human-rater protocols are set up, or online evals (canaries, A/B) are being instrumented.
---

# AI Eval

Without eval, every prompt or model change is a guess and every regression is a
surprise. The harness is what turns "it seems better" into a number you can gate on.

## When to reach for this

- Standing up the first golden set / regression suite for an LLM feature
- Wiring eval gates into CI before prompt, model, or pipeline changes ship
- Designing an LLM-as-judge rubric, or validating one against human raters
- Instrumenting online evals — canaries, shadow traffic, A/B

## Principles

1. **Golden set before tuning.** 50–200 labeled examples is enough to start; build
   it before the first prompt iteration, or improvement is indistinguishable from noise.
2. **LLM-as-judge is a noisy instrument — calibrate it.** Validate against ~100
   human-labeled samples and require substantial agreement (Cohen's kappa ≥ 0.6)
   before trusting it in a gate. In pairwise judging, score both orders — position
   bias is real.
3. **Multi-axis over single score.** Helpfulness, faithfulness, format compliance,
   safety — tracked separately. A composite hides the one axis that regressed.
4. **Regression gates, not dashboards.** CI blocks on a metric drop beyond a
   pre-committed threshold; a dashboard nobody is paged on is decoration.
5. **Failure taxonomy drives improvement.** Tag every failure with an error class
   (bad retrieval, format break, refusal, hallucination, …); per-class counts tell
   you what to fix next, a pass rate doesn't.
6. **Online measures what offline can't.** Thumbs, task completion, retention only
   exist in production — pair every offline gate with at least one online signal.

## Choosing the eval type

| Question | Eval | Notes |
|---|---|---|
| Can it be scored deterministically? | exact match / schema check / unit-test style | always prefer this; skip the judge |
| Did this change regress quality? | offline golden set in CI | same set, same scorer, before/after |
| Is output A better than B? | pairwise LLM-judge, order-swapped | calibrate against humans first |
| Is the rubric itself right? | human raters, measure kappa | ≥ 0.6 before automating it |
| Does it hold up on real traffic? | shadow / canary, then A/B | offline pass is the entry ticket, not the proof |

A worked LLM-as-judge harness (rubric prompt, order swap, human-calibration loop,
CI gate) is in [`references/llm-judge.md`](references/llm-judge.md).

## Pitfalls

- Eval examples contaminated — also present in the few-shot prompt or fine-tune data
- Single-run judge scores treated as stable: judges are stochastic; run 3× and
  aggregate, and still spot-check disagreements by hand
- Gate threshold chosen *after* seeing the new number
- Golden set never refreshed — it drifts away from real traffic; sample production
  failures back into it on a schedule
- "Improved by X%" claims without same-set, same-scorer before/after numbers
- Judging with the same model family being evaluated and ignoring self-preference bias

---
*Related: `ai-prompt-engineer` (the prompts under test), `ai-finetune` (eval-coupled
training), `ai-inference-perf` (quality gates on perf changes) · domain agent:
`ai-architect` (eval strategy) · output/ADR format: `playbook-conventions`*
