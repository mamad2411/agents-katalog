---
name: feature-change
description: >-
  Add, remove or rename a model feature without breaking serving. Trigger on
  "add a model feature", "new feature in the model", "add a feature", "remove this
  feature", or any diff touching the feature schema. Covers the training and
  serving sides of the contract, the leakage check, and deploy ordering.
---

# Feature change

A feature list is a contract between two repos. Changing one side alone means
the next prediction request 500s on a shape mismatch, in production, silently
until someone loads the page.

## Steps

1. **Find both sides first.** Grep the training repo for the shared feature
   schema and the serving repo for the predictor's copy of it. Do not start
   editing until you can name both files. If they already differ, stop and
   report the drift: that is a live bug, not part of this task.
2. **Leakage check, before anything else.** Ask when each input is known. A
   feature computed from data that only exists after the event being predicted
   is leakage, however good the offline metric looks. The same applies to
   holdout logic: a row's own event must be excluded from its rolling windows.
3. **Write the feature on the training side.** Deterministic, seeded where
   randomness is involved, and resilient to a missing round or column rather
   than raising on the first gap in history.
4. **Mirror it in serving.** Same name, same order, same dtype. Order matters
   for array-based models even when names match.
5. **Retrain and evaluate.** A feature change is a model change, so it goes
   through the `model-eval` gate. A single-season improvement is not evidence.
6. **State the deploy order explicitly** in the PR description: which repo
   ships first, and what breaks if they land the other way round. Serving that
   expects a column the published model does not have fails exactly as hard as
   the reverse.
7. **Write down the rejected version.** If a feature was tried and rolled back,
   record it and why, next to the feature list. Otherwise it gets re-added in
   three months by someone reading the same intuition.
