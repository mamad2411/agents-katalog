---
name: ml-experiment-engineering
description: Use for ML, data science, training, evaluation, benchmarking, model quality, autoresearch, or experiment iteration tasks.
---

# ML Experiment Engineering

In ML, code running without errors does not prove the idea works. Separate implementation correctness from experimental outcome.

## Validation Pyramid

1. Static/config validation:
   - dataset paths
   - schema and shapes
   - label mapping
   - seed and split policy
   - checkpoint/output directories
   - dependency/runtime compatibility
2. Runtime/pipeline validation:
   - one tiny batch or smoke run
   - loss/metric sanity
   - train/eval mode correctness
   - deterministic eval command
   - artifact persistence
3. Experimental conclusion:
   - compare to baseline
   - confidence interval or repeated run when noise matters
   - record caveats and negative results

## Experiment Brief

```md
Hypothesis:
Baseline:
Independent variable:
Dependent metric:
Controls:
Fixed eval command:
Success threshold:
Failure modes:
Artifacts:
```

## Iteration Loop

- Lock evaluation before optimizing.
- Keep a per-round experience log: strategy, changed files, metric snapshot, verdict, insight.
- Accept improvements only when they beat baseline or satisfy criteria without violating controls.
- Roll back or isolate regressions.
- Keep the human on the loop for goal changes, not every tiny step.

## Watchdog Rules

- Monitor long training with checkpoints, logs, and timeouts.
- Distinguish environment failure from strategy failure.
- Preserve useful checkpoints.
- Do not modify eval logic to rescue a poor result.

