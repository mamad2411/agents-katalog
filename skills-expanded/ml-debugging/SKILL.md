---
name: ml-debugging
description: Use when a model won't learn, loss is NaN, metrics look too good/bad, or training is unstable. Provides a systematic decision tree for diagnosing data, optimization, and generalization failures.
---

# ML Debugging

## Overview

ML bugs are usually silent — the code runs, but the model is wrong. Debug systematically by **isolating which layer is broken**: data, optimization, or generalization. Form a hypothesis, test it with the cheapest possible experiment, then move on.

## When to use

- Loss is NaN/Inf or stuck.
- Metrics are implausibly high (leakage) or stuck at chance.
- Train/val curves diverge.

## First move: can it overfit one batch?

The fastest sanity check in ML. Take a single small batch and train until loss ≈ 0.

```python
x, y = next(iter(train_loader))
for _ in range(200):
    optimizer.zero_grad()
    loss = criterion(model(x), y)
    loss.backward(); optimizer.step()
print(loss.item())  # should approach 0
```

- **Can't overfit one batch** → bug in model/loss/labels/data wiring (not capacity).
- **Overfits one batch but not the dataset** → optimization or regularization issue.

## Symptom → cause decision tree

| Symptom | Likely cause | Fix |
|---------|-------------|-----|
| Loss = NaN | LR too high; log(0); /0; bad input scaling | Lower LR, clip grads, add eps, normalize inputs |
| Loss flat at start | LR too low; dead ReLUs; wrong loss | Raise LR; check init; verify loss/target shapes |
| Train great, val terrible | Overfitting **or** leakage | Regularize/augment; audit for leakage |
| Val better than train | Leakage; val too easy; dropout-at-train artifact | Re-check split; inspect val set |
| Metric implausibly high | Target leakage | Hunt leaked features (see EDA skill) |
| Stuck at chance | Labels misaligned; data not shuffled; LR off | Verify label mapping; shuffle; sweep LR |

## Leakage hunt (when results are "too good")

1. Any feature with |corr| ≈ 1.0 to target?
2. Is preprocessing fit before the split?
3. Do rows from one entity span train and test? (use GroupKFold)
4. Time series shuffled? (must be chronological)
5. Is a post-outcome column (e.g., `refund_issued`) used to predict the outcome?

## Optimization checklist

- Normalize/standardize inputs.
- Sweep LR over `[1e-5 ... 1e-1]` (log scale) — wrong LR causes most failures.
- Add gradient clipping for RNNs/transformers.
- Check for NaNs in inputs/targets before training.
- Verify loss matches task (CE for classification logits, not MSE).

## Pitfalls

- Changing five things at once — change one variable per experiment.
- Debugging on the full dataset — shrink to fail fast.
- Trusting metrics without inspecting predictions/confusion matrix.

## Hand-off

A root-caused fix plus a regression check (the one-batch test + a held-out metric) so experiment-tracking can confirm the issue stays fixed.
