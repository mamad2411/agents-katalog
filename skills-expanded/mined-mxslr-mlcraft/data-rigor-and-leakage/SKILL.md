---
name: data-rigor-and-leakage
description: "Use BEFORE training any model, to build correct train/val/test splits and hunt data leakage - the #1 cause of fake-high accuracy. Covers group/patient/subject splits, temporal splits, official-benchmark splits, label correctness, class balance, and preprocessing parity. Triggers on 'split the data', 'train/test split', 'cross validation', 'why is accuracy suspiciously high', 'data leakage', 'per-patient'."
---

# Data Rigor & Leakage Audit

Wrong splits invalidate every downstream number. Do this **before** training and re-check whenever results look too good.

## Leakage checklist
- **Group leakage (most common).** If one entity (patient, person, product, document, study) yields multiple samples, ALL its samples must sit in ONE split. Random per-sample splitting scatters them across train/test the model memorizes the entity. Use `GroupShuffleSplit` / `StratifiedGroupKFold` keyed by the entity id.
- **Temporal leakage.** Time-series / any time-ordered data: train must be strictly earlier than val/test. No shuffling across time. No future-derived features.
- **Official split.** If the benchmark defines a train/test split (e.g., encoded in an ID), use it - otherwise numbers aren't comparable to papers.
- **Preprocessing / normalization leakage.** Fit scalers, PCA, class weights, augmentation stats, and target encodings on **train only**, then apply to val/test. Never fit on the full set.
- **Duplicate / near-duplicate leakage.** De-duplicate (and augmented copies) across splits.
- **Target leakage in features.** Drop features that encode the label or are only known post-outcome.
- **Threshold/selection leakage.** Choosing a decision threshold or doing model selection using **test** labels is leakage. Do it on validation.

## Make it enforceable
Add explicit **assertions** that split membership is disjoint at the entity level, e.g.:
```python
assert not (train_ids & val_ids) and not (train_ids & test_ids) and not (val_ids & test_ids)
```
Print per-split counts of **entities** (not just samples) and the class balance.

## Also verify
- **Labels** are correct and consistent (one authoritative source; handle multi-label-per-entity deliberately).
- **Class balance** - decide handling now (class-weighted loss OR resampling, not both by default).
- **Manifest, not copies.** Prefer a manifest table (path, entity, label, split) over shuffling files into folders - it makes the split auditable.
