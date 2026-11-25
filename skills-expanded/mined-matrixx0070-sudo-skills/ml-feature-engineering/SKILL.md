---
name: ml-feature-engineering
version: 1.0.0
description: Design leakage-safe features with correct encoding, scaling, split-aware fitting, and disciplined selection for classic ML.
author: matrixx0070
tags: [ml, features, encoding, leakage, selection]
capabilities: []
---

## When to use

Use this once the problem is framed and you have raw tables, to turn columns into model-ready features without leaking future information across your train/test boundary.

**Not for:** embedding text/images for LLM retrieval or prompt context (see `ai-rag-pipeline`). Not for exploratory profiling, ad-hoc SQL, or dashboards (see `data-explore`, `data-write-query`) — that is understanding data, not preparing modeling inputs.

## Method

1. Split FIRST. Create train/validation/test (or CV folds) before computing any statistic. Everything below is fit on train only.
2. Set the as-of rule: every feature uses data with timestamp ≤ prediction time. Time-series → split by time, never randomly.
3. Encode categoricals. Decision point: low cardinality → one-hot; high cardinality → target/frequency encoding fit inside CV folds only; tree models tolerate ordinal/native categorical.
4. Scale numerics for distance/linear/NN models (standardize or robust-scale); skip for tree ensembles — they are scale-invariant.
5. Handle missingness explicitly: add an `is_missing` flag, then impute with a train-fit statistic. Never drop rows silently.
6. Engineer signal: ratios, lags, rolling aggregates, time-since-event, interaction terms grounded in domain logic.
7. Select features. Decision point: many correlated features → L1 / tree importance / permutation importance; keep it minimal, prune redundant ones. Validate selection on held-out folds, not the full data.
8. Freeze a transform pipeline (e.g. sklearn `Pipeline`/`ColumnTransformer`) so train and serve apply identical steps.

## Example

High-cardinality `merchant_id` (40k values). One-hot explodes; instead use K-fold target encoding: for each training fold, encode with the mean target computed on the OTHER folds, smoothed toward the global mean. Test set is encoded with the full-train mapping. Result: no fold sees its own target, and offline PR-AUC stops being optimistically inflated (0.94 → a realistic 0.88).

## Pitfalls

- **Fit-before-split.** Scaling or imputing on the full dataset leaks test distribution into train. Fit on train only.
- **Target encoding without folds.** Encoding a category with its own rows' target — massive leakage. Use out-of-fold encoding.
- **Random split on time series.** Future rows train the model to predict the past. Split chronologically.
- **Kitchen-sink features.** Hundreds of correlated columns hurt generalization and serving cost. Prune deliberately.

## Output format

```
# Features: <name>
SPLIT: <scheme> (fit stats on train only)
AS-OF RULE: feature timestamp <= predict time
ENCODING: <col: method>
SCALING: <cols | none (tree)>
MISSING: flag + <impute strategy>
ENGINEERED: <feature: definition>
SELECTION: <method> -> <n kept of m>
PIPELINE: <serialized transform artifact>
```
