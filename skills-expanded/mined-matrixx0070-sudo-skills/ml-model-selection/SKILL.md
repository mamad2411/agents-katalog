---
name: ml-model-selection
version: 1.0.0
description: Choose a model family and a hyperparameter search strategy matched to the problem type, data size, and constraints.
author: matrixx0070
tags: [ml, model-selection, hyperparameters, tuning, tradeoffs]
capabilities: []
---

## When to use

Use this after features exist and before a long training campaign, to pick a model family (or a short candidate set) and a tuning strategy justified by data shape, interpretability needs, and latency budget.

**Not for:** picking an LLM, adapter, or fine-tune-vs-RAG decision (see `ai-fine-tune-plan`, `ai-rag-pipeline`). Not for choosing a chart, statistical test, or SQL engine (see `data-statistical-analysis`).

## Method

1. Restate type and constraints: clf/reg/ranking, row count, feature count, latency ceiling, interpretability requirement.
2. Pick a family by data shape. Decision point: tabular → gradient-boosted trees (XGBoost/LightGBM) as default; strict linear/interpretable need → regularized linear/logistic; tiny data → simpler + regularized; images/audio/sequences → NN.
3. Always include a strong-but-simple candidate (logistic/linear or a single tree) as an interpretable floor to compare against.
4. Set the validation scheme the tuning will use: same CV/time-split as `ml-training-eval`. Tuning and evaluation must share it.
5. Choose search strategy. Decision point: few params / fast model → grid; many params / expensive → random or Bayesian (Optuna); wide budget → successive halving.
6. Bound the search space with sane priors (tree depth 3-10, learning rate 0.01-0.3, regularization on a log scale). Fix a random seed for the search.
7. Select by the primary metric on validation, then break ties with the guardrail metric, simplicity, and latency — not by a decimal of the primary.

## Example

Tabular fraud, 2M rows, 80 features, <50ms serving, imbalanced. Candidates: LightGBM (default) vs L2 logistic (interpretable floor). Strategy: Optuna, 60 trials over `num_leaves`, `learning_rate`, `min_child_samples`, `scale_pos_weight`, optimizing PR-AUC under 5-fold stratified CV. LightGBM wins 0.71 vs 0.58 PR-AUC; inference 8ms — within budget. Logistic is kept as the explainability reference model.

## Pitfalls

- **NN by default on tabular.** Boosted trees usually win on structured data with less tuning. Reach for trees first.
- **Tuning on the test set.** Any test-set peeking during search inflates the reported score. Tune on validation only.
- **Unbounded search.** Huge grids burn compute for noise-level gains. Use priors and early stopping.
- **Chasing third-decimal wins.** A 0.002 metric gain rarely survives production. Prefer the simpler, faster model.

## Output format

```
# Model Selection: <name>
TYPE + CONSTRAINTS: <clf|reg|rank> | rows=<n> feats=<m> | latency=<ms> | interpretable=<y/n>
CANDIDATES: <family A>, <interpretable floor>
VAL SCHEME: <cv/time-split> (shared with eval)
SEARCH: <grid|random|bayes> | trials=<n> | seed=<s>
SPACE: <param: range>
CHOSEN: <model> | primary=<x> | guardrail=<y> | latency=<ms>
RATIONALE: <why over runner-up>
```
