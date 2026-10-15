---
name: training-models
description: Staged setup and silent-failure diagnosis for neural network training. Use when you start a new training pipeline, when you review a training loop, or when a run goes wrong — the loss does not decrease, accuracy stalls, gradients explode or vanish, train and eval disagree, inference is wrong, or a one-batch overfit fails. Chinese triggers include 从零搭训练流程, 检查训练循环, loss 不下降, acc 卡住, 梯度异常, 训练验证不一致, and 推理错误. Do not use for experiment orchestration, ablation matrices, or result tables.
license: MIT
compatibility: Sample code and the sanity check require PyTorch.
---

# Training Neural Networks

A misconfigured network trains. The loss decreases, the run completes, and the model is quietly
wrong. The error surface here is logical, not syntactic, so the usual defences do not fire: no
exception, no stack trace, no unit test. A fast approach does not work here.

The defence is a **gate**. A gate is the evidence that permits entry to the next stage. Collect
that evidence before you continue. A stage that you enter through a shut gate hides a defect,
and you must then find it with more code in the way.

Two habits open gates faster than all others: **visualize** the tensors at each seam, and change
**one thing at a time**.

The stages differ in how much room they leave you. Stages 1 to 3 are a narrow bridge: the order
matters, and a skipped check costs you hours later. Stages 4 to 6 are an open field: many routes
reach a good model, so the gates there describe what you should be able to show, not what you
must do. The reference gives the reason behind each option, which is what lets you choose.

## Route

- **New pipeline** — walk the six stages in order. Open each gate before you continue.
- **Broken run** — the gates are also the diagnosis. Run the Stage 2 gates in order. The first
  gate that stays shut localizes the defect.
- **Loop review** — audit the run against the Stage 2 gates. Report each gate as open or shut.

Read [karpathy-recipe.md](references/karpathy-recipe.md) for the full tips of each stage. Read
[checklist.md](references/checklist.md) when a gate stays shut and you need the failure modes
behind it.

## Stage 1 — Become one with the data

Scan thousands of examples. Sort and filter by label, size, and length. Look at the outliers on
every axis, because an outlier almost always exposes a defect in the data or the preprocessing.

**Gate:** you can state the label noise, the duplicates, the corrupt samples, and the class
imbalance of this dataset. You can also say which architecture the data asks for, and why.

## Stage 2 — Skeleton and dumb baselines

Connect training to evaluation with a model that you cannot get wrong, such as a linear
classifier or a tiny ConvNet. Fix the seed. Turn off augmentation, dropout, and weight decay.
Evaluate on the whole test set.

These seven gates are also the diagnostic order. Open them one by one.

1. **Loss at init matches the prior.** Uniform `n`-class cross entropy starts near `log(n)`. L2
   regression starts near the label variance. A mismatch points at the labels, the final layer,
   the logit scale, or the loss input contract.
2. **The final-layer bias holds the prior.** Set it to the target mean for regression, and to
   `log(pos/neg)` for imbalanced classification. Otherwise the first hundreds of steps only
   unlearn a wrong bias.
3. **A human-checkable metric exists.** Track accuracy or a similar metric next to the loss.
   Record your own human accuracy as the reference ceiling.
4. **The input-independent baseline is clearly worse.** Train once on zeroed inputs. A similar
   result means that the model ignores its input, or that a label leaks in.
5. **One batch of 2 to 8 examples overfits to near zero.** Plot the labels and the predictions
   together and confirm that they align point by point. This gate separates a broken pipeline
   from a generalization problem.
6. **The tensors are correct at the last seam.** Print `x` and `y` in denormalized form on the
   line directly above `y_hat = model(x)`. A dataset can be correct while collate, transform, or
   the device copy corrupts the batch.
7. **Gradients respect the sample boundary.** Build a scalar from the loss of sample `i` alone,
   call backward, and confirm that only the input of sample `i` carries gradient. The same probe
   proves causality in an autoregressive model.

**Gate:** all seven gates hold under one reproduction command.

## Stage 3 — Overfit

Copy the simplest architecture that a related paper reports. Use Adam at `3e-4`. Turn learning
rate decay off. Add one signal, module, or data source at a time, and verify each one.

**Gate:** the model reaches a very low training loss on the full training set. A model that
cannot reach it gives you a defect report, not a capacity report.

## Stage 4 — Regularize

Now trade a little training fit for validation performance. More real data is the one option that
improves the model without a limit, so reach for it before the others. After that the choice
depends on your data and your compute, and the reference ranks the twelve usual options with the
reason behind each one. Two of them carry a condition worth knowing before you pick: dropout
combines poorly with BatchNorm, and a larger model only helps together with early stopping.

**Gate:** validation loss improves. The first-layer weights show reasonable edges, and the
internal activations show no odd artifact. A filter that looks like noise means a defect, so
treat that as a reason to return to Stage 2 rather than to add more regularization.

## Stage 5 — Tune

Random search suits this better than a grid, because a grid resamples the axes that do not matter.
Bayesian tools exist and some people report success with them; manual exploration of a wide space
still competes well.

**Gate:** you can say which hyperparameters the model is sensitive to, and the best configuration
repeats.

## Stage 6 — Squeeze

Two low-risk gains remain. An ensemble gives roughly 2% almost every time, and distillation folds
it back into one model when compute is short. Networks also improve for an unintuitive length of
time, so a run that still descends slowly is usually a run to leave alone.

**Gate:** you report the final number against the Stage 3 and Stage 4 results.

## Runnable checks

- [`sanity_check.py`](scripts/sanity_check.py) — Stage 2 gates 1, 4, and 5,
  plus the mode, `zero_grad`, and logits contracts. A check that cannot decide reports
  `not_applicable` rather than a pass.
- [`correct_training_loop.py`](scripts/correct_training_loop.py) — a train
  and validation loop to copy.
- [`six_pitfalls_before_after.py`](scripts/six_pitfalls_before_after.py) and
  [`extra_pitfalls_before_after.py`](scripts/extra_pitfalls_before_after.py)
  — broken and repaired pairs for the failure modes in the checklist.

## Completion

Report the reproduction command, the state of each gate that you touched, the evidence behind
the defect, the repair, and the before-and-after comparison.

A broken run is complete when the original reproduction passes and no validation step is weaker
than before. A new pipeline is complete when you name the current stage and the evidence that
opens its gate. A loop review is complete when every Stage 2 gate carries an open or shut
verdict.
