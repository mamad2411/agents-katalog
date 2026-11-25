---
name: held-out
description: "Use when reporting how well anything fitted or tuned performs — a model, forecast, classifier, heuristic, prompt, or threshold. The score counts only on data the thing never saw, against a bar set before scoring, a naive baseline, and a placebo. Use when a score came from the data used to build it, or when something was iterated until the eval passed."
---

# Held Out

## The failure mode this fixes

The agent builds a model, a scoring heuristic, a prompt, a threshold — then reports how well it does on the same examples it was built against. Or it has a test set, runs it, tweaks, runs it again, and repeats until the number clears the bar. Either way the reported score measures memory, not skill, and it will not survive contact with new data.

Two quieter variants. The bar gets chosen after the result is known, so whatever came out is a pass. And an inconclusive result — too few cases, a margin inside the noise — gets written up as a win because a win was expected.

This is the fitted-system cousin of tuning a constant to make a test pass. The rule is the same: the result you were optimizing against is never evidence.

## When to Use This Skill

- You're about to report accuracy, calibration, win rate, or "it beats the old one" for anything fitted or tuned
- The evaluation cases were visible while the thing was being built
- An eval was re-run after each tweak until it passed
- A feature or signal "clearly works" and nobody has checked it against a placebo
- The sample is small enough that the honest answer might be "can't tell"

**Don't use when:** the code is deterministic and has a spec — that's `test-like-you-mean-it`. And not for exploratory fitting you've labeled as exploration; the skill applies the moment a number is going to be reported as performance.

## Instructions

### 1. Set the bar before you score

Write down the metric, the threshold that counts as passing, and the baseline to beat — before running the evaluation. A bar chosen after the result is a description of the result.

### 2. Split first, and spend the held-out set once

Separate the evaluation cases before any fitting or tuning, and keep them out of sight. Every time a held-out result changes a decision, that set has been used for training. If it's spent, say so, and get fresh cases rather than reporting the contaminated score. For anything involving time, split by time: train on the past, score on what came after.

### 3. Beat a naive baseline and a placebo

A score means nothing alone. Compare against the dumbest thing that could work (always predict the majority, last value carried forward, the previous version). Then run a placebo: shuffle the labels, or swap the signal for one that can't matter — the wrong region, the wrong time window. If the placebo scores about as well, the signal isn't doing what you think.

### 4. Record predictions before outcomes

When the truth arrives later, log the prediction with a date before the outcome is known. A prospective record is the only evaluation that can't be tuned after the fact. Challengers get logged the same way, alongside the incumbent, before either is scored.

### 5. Report one of three verdicts and keep the failures

Passed, failed, or indeterminate. Indeterminate is a real answer when the sample is too small or the margin sits inside the noise; say what would settle it. A failed evaluation stays in the write-up next to the passes — a record with only wins in it is a filtered record.

## Output format

```
Evaluation: <what was scored>
Bar (set before scoring): <metric, threshold, baseline to beat>
Held-out set: <how it was split, size, times consulted>
Result: <score> | baseline: <score> | placebo: <score>
Verdict: PASSED / FAILED / INDETERMINATE because <reason>
Prospective log: <predictions recorded before outcomes | none>
Earlier failures still on record: <list | none>
```

## Anti-Patterns

| Anti-Pattern | Why it defeats the skill |
|---|---|
| Scoring on the build set | the thing has seen the answers. The score is recall. |
| Iterating against the test set | each re-run after a tweak leaks the held-out set into the design. |
| The bar set afterward | any result passes a threshold chosen to fit it. |
| No baseline, no placebo | "82% accurate" where always-guess-the-majority gets 80%, or shuffled labels get 81%. |
| Indeterminate reported as passed | six of ten on a coin-flip task is not a finding. |
| Dropping the failed run | the write-up shows the three evaluations that passed and omits the four that didn't. |

## Mental Model

> A score is only worth what it could have revealed. If the thing had already seen the answers, or the bar moved to meet it, the evaluation couldn't have failed — and an evaluation that can't fail tells you nothing.
