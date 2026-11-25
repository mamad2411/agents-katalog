---
name: train-evaluate-ml-model
description: Trains and evaluates a classic (non-LLM) ML model — business-aligned metric selection, leakage-safe train/validation/test splits, Pipeline-scoped feature engineering, baseline-first model selection, cross-validated hyperparameter tuning, bias/variance diagnosis, and experiment tracking — guarding against data leakage and overfitting.
when_to_use: Fitting and validating a classification, regression, ranking, forecasting, or clustering model on tabular/feature data. Distinct from profile-dataset (EDA only), wrangle-tabular-data (cleaning/shaping the feature table), serve-deploy-ml-model (deployment), monitor-ml-drift (post-deploy), and rag-pipeline/prompt-engineering (LLM work).
---

## When to Use

Reach for this skill when the request is to **fit and validate a model that predicts**, not to explore or clean data:

- "Train a classifier to predict churn / fraud / default and tell me if it's good"
- "Build a regression/forecasting model for demand/price and pick the best one"
- "My model gets 99% accuracy — is that real or leakage?"
- "Tune hyperparameters / cross-validate / compare XGBoost vs logistic regression"
- "Cluster these customers into segments"

NOT this skill:
- Summary stats, distributions, correlations, missingness *before* modeling → profile-dataset
- Cleaning, type coercion, joins, dedup, resampling to build the feature table → wrangle-tabular-data
- Asserting schema/range/null contracts on the data before training → validate-data-quality
- Packaging the trained model behind an API / batch job → serve-deploy-ml-model
- Watching a live model's inputs/outputs degrade over time → monitor-ml-drift
- Scoring or grading an LLM's outputs against a rubric/golden set → llm-eval-harness
- Getting an LLM to answer over a corpus, or designing prompts → rag-pipeline / prompt-engineering

## Steps

1. **Choose the metric from the business cost FIRST — never optimize bare accuracy on imbalanced data.** A 1%-positive fraud set scores 99% accuracy by predicting all-negative and catches zero fraud. Pick before you train:

   | Task / situation | Metric | Why |
   |---|---|---|
   | Imbalanced classification, cost of missing a positive high | Recall @ fixed precision, or **PR-AUC** | accuracy & ROC-AUC look great while recall is ~0 |
   | Imbalanced, ranking/threshold-free comparison | **PR-AUC** (not ROC-AUC) | ROC-AUC is optimistic under heavy imbalance |
   | Balanced classification | F1 or ROC-AUC | symmetric cost |
   | Asymmetric FP vs FN cost | Expected cost = `cFP·FP + cFN·FN`, tune threshold | maps directly to money |
   | Regression, outliers matter | RMSE | penalizes large errors |
   | Regression, robust to outliers | MAE / MAPE | business reads "off by X" |
   | Ranking / recsys | NDCG@k, MAP@k | position-aware |
   | Forecasting | MASE / sMAPE vs naive | scale-free, must beat seasonal-naive |
   | Clustering (no labels) | silhouette + downstream business check | inertia alone is meaningless |

   Fix the **decision threshold** from the cost matrix later — don't ship the default 0.5.

2. **Split BEFORE any feature engineering or fitting — this is the #1 leakage source.** Three sets: train / validation (or CV folds) / **held-out test touched once at the very end**. The split strategy is not optional — pick by data structure:
   - **Random stratified** for i.i.d. rows: `train_test_split(X, y, stratify=y, test_size=0.2, random_state=42)`.
   - **Time-based** for any temporal data — train on past, test on future, never shuffle. Use `TimeSeriesSplit` for CV. A random split on time-series leaks the future and inflates every metric.
   - **Group split** when rows share an entity (same user/patient/device across rows): `GroupKFold` / `StratifiedGroupKFold` so the same group never appears in both train and test.

3. **Engineer features inside a `Pipeline` fit only on train, then run a leakage audit.** Every transform that *learns* (imputation means, scaler stats, target/one-hot encoders, feature selection) must `.fit` on train and only `.transform` val/test — otherwise test statistics leak in. Wrap it:

   ```python
   from sklearn.pipeline import Pipeline
   from sklearn.compose import ColumnTransformer
   from sklearn.impute import SimpleImputer
   from sklearn.preprocessing import StandardScaler, OneHotEncoder
   from sklearn.model_selection import cross_val_score

   pre = ColumnTransformer([
       ("num", Pipeline([("imp", SimpleImputer(strategy="median")),
                         ("sc", StandardScaler())]), num_cols),
       ("cat", OneHotEncoder(handle_unknown="ignore"), cat_cols),
   ])
   pipe = Pipeline([("pre", pre), ("model", model)])
   # CV refits `pre` per fold → no leakage across folds
   cross_val_score(pipe, X_train, y_train, cv=cv, scoring="average_precision")
   ```

   **Leakage audit checklist** — a feature is leaky if it: (a) is derived from the target or post-outcome (e.g. `payment_received` predicting `will_pay`); (b) encodes future information unavailable at prediction time; (c) is an ID/timestamp that proxies the label; (d) was computed using full-dataset statistics before the split. If any single feature gives a near-perfect score, it's leakage, not skill.

4. **Establish a dumb baseline before any real model.** `DummyClassifier(strategy="most_frequent")` / `DummyRegressor(strategy="mean")`, then a linear baseline (`LogisticRegression` / `Ridge`). This is the bar every model must clear; a fancy model that barely beats majority-class isn't worth the complexity.

5. **For tabular data, reach for gradient boosting before deep nets.** Default order: linear baseline → **gradient boosting** (`XGBoost` / `LightGBM` / `HistGradientBoostingClassifier`) → deep net only if GBM plateaus and you have ample data. GBMs win on heterogeneous tabular data, need little preprocessing, and train in minutes. Handle imbalance with `class_weight` / `scale_pos_weight` or threshold tuning — not blind SMOTE (and if you oversample, do it inside the CV fold only, never before the split).

6. **Tune hyperparameters with CV, search smart not exhaustive.** `RandomizedSearchCV` or Optuna over a sensible space beats `GridSearchCV` on a huge grid. Always pass `scoring=` your step-1 metric (not accuracy) and use the same CV object as step 2. Key GBM knobs: `n_estimators` + `learning_rate` (trade off), `max_depth` / `num_leaves`, `min_child_samples`, `subsample`, `colsample_bytree`, plus `early_stopping_rounds` on a validation set.

7. **Diagnose bias vs variance, then act.** Compare train vs validation score:
   - Train high, val low (large gap) = **overfit/variance** → regularize, reduce depth/leaves, add data, drop features, stronger early stopping.
   - Train and val both low = **underfit/bias** → richer model, better features, less regularization.
   Plot a learning curve to decide whether more data would even help before collecting it.

8. **Track every experiment — params, metric, data version, code version.** Log to MLflow / Weights & Biases (or a CSV at minimum): hyperparameters, all CV metrics with std, the data snapshot hash, git commit, and the random seed. An untracked best-run is unreproducible. Pin seeds (`random_state`) everywhere.

9. **Evaluate the held-out test set EXACTLY ONCE, at the end.** Report the step-1 metric with a confidence interval (bootstrap), the confusion matrix at your chosen threshold, and the gap vs baseline. Repeatedly peeking at test = overfitting to test by hand.

## Common Errors

- **Splitting after feature engineering / scaling on the full dataset.** Test statistics bleed into train; metrics inflate, prod collapses. Split first, fit transforms on train only (use a `Pipeline`).
- **Random split on temporal data.** The model trains on future rows and "predicts" the past. Use a time-based split / `TimeSeriesSplit`.
- **Reporting accuracy on an imbalanced problem.** 99% accuracy with 0% recall is useless. Pick PR-AUC / recall-at-precision from the cost (step 1).
- **A feature that's too good.** One column driving a near-perfect score is almost always leakage (post-outcome field, ID proxy, target-derived). Audit and drop it.
- **Target encoding / imputation / feature selection computed before the split or outside the CV fold.** Subtle leakage that survives CV but not production. Fit them inside the pipeline, per fold.
- **SMOTE/oversampling applied before splitting.** Synthetic copies of test rows land in train. Resample inside the training fold only.
- **Tuning against the test set / peeking repeatedly.** You overfit to it manually. Tune on CV/validation; touch test once.
- **No baseline.** Without DummyClassifier/linear you can't tell if your model learned anything. Always beat the dumb baseline first.
- **`scoring=` left at default (accuracy/R²) during search.** The search optimizes the wrong thing. Pass your business metric to `cross_val_score` / `*SearchCV`.
- **Train/serve feature skew.** Features computed differently (or with different code/library versions) at training vs inference. Reuse the exact fitted pipeline artifact for serving.
- **Unpinned seeds / untracked runs.** Results aren't reproducible and "best model" can't be recovered. Pin `random_state`, log params+metrics+data+code version.

## Verify

1. **Beats baseline:** held-out test metric (step-1 metric) > the DummyClassifier/DummyRegressor and the linear baseline by a margin larger than the bootstrap CI. If it doesn't, there's no model.
2. **Leakage check passes:** drop each top-importance feature individually — no single feature should collapse the score to chance-level; remove any post-outcome/target-derived/ID-proxy column; confirm all learned transforms were fit on train only.
3. **Split integrity:** for temporal data, every test timestamp is strictly after every train timestamp; for grouped data, no group ID appears in two sets (assert programmatically).
4. **Generalization gap sane:** train metric − validation metric is small and explained by your bias/variance call; test ≈ validation (a big test drop means tuning overfit to validation).
5. **Metric matches business cost:** the reported metric and the chosen decision threshold come from step 1, not the library default.
6. **No train/serve skew:** running the saved pipeline on a held-out row reproduces the exact training-time prediction (same features, same library versions).
7. **Reproducible:** re-running with the logged seed + data snapshot + code commit yields the same metric (within float tolerance); the experiment tracker has params, CV metrics with std, data hash, and git commit.

Done = the held-out test metric (chosen for business cost, evaluated once) beats both baselines beyond its CI, the leakage and split-integrity checks pass, the generalization gap is explained, and the saved pipeline reproduces predictions with no train/serve skew under a pinned, tracked run.
