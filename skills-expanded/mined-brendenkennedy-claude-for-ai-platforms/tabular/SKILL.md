---
name: tabular
description: >
  Classical DS on structured/tabular data — the sklearn-lane discipline. Carries: ALL
  preprocessing inside a `Pipeline`/`ColumnTransformer` so cross-validation can't leak, baselines
  first (Dummy → linear/logistic → gradient boosting; boosting beats deep nets on most tabular
  problems), CV strategy (StratifiedKFold; GroupKFold when rows share an entity), categorical
  encoding traps (target encoding leaks unless fit per-fold), imbalance handling (class_weight,
  threshold tuning on val, PR-AUC over accuracy), feature-importance honesty (permutation on val
  over impurity; SHAP), calibration, and persisting the fitted pipeline+model as one artifact.
  Load when modeling tabular/structured data. Triggers: tabular, sklearn, scikit-learn, pandas,
  dataframe, XGBoost, LightGBM, gradient boosting, random forest, ColumnTransformer, pipeline,
  one-hot, target encoding, cross-validation, StratifiedKFold, GroupKFold, feature importance,
  SHAP, class imbalance, logistic regression.
---

# tabular — classical ML on structured data

> On-demand: load this for sklearn-lane work. The universal rules still come from their owners —
> split discipline from `datasets` (group/temporal splits, test touched once), metrics + error
> analysis from `evaluation`, search from `hpo-optuna`, tracking via the active tracker skill.
> This skill carries what's *specific* to tabular: pipelines-as-leakage-armor, the boosting-first
> model ladder, and encoding/importance traps.

## The one structural rule: everything fits inside the pipeline
Any transform that *learns from data* — imputation, scaling, encodings, feature selection — lives
inside an sklearn `Pipeline`/`ColumnTransformer`, never applied to the full frame before splitting:

```python
from sklearn.compose import ColumnTransformer
from sklearn.pipeline import Pipeline

pre = ColumnTransformer([
    ("num", Pipeline([("impute", SimpleImputer()), ("scale", StandardScaler())]), num_cols),
    ("cat", OneHotEncoder(handle_unknown="ignore", min_frequency=10), cat_cols),
])
model = Pipeline([("pre", pre), ("clf", clf)])   # fit/predict/CV THIS, never the parts
```
Why it's the rule and not a style choice: `cross_val_score(model, X, y)` now re-fits the
preprocessing per fold — the only way CV estimates aren't quietly inflated by full-data statistics.
Fitting a scaler or encoder on all rows first is this lane's normalization-stats leakage.

## Prove the spine on synthetic, then flip to real (the tabular default)
`/bootstrap`'s tabular skeleton (`train.py`/`evaluate.py`/`factory.py`/`calibrate.py`) runs end-to-end
on **synthetic data** behind a `dataset.synthetic=true` flag before any real data exists — so the whole
pipeline (the `ColumnTransformer`, the split, calibration, the tracker wiring) is validated early. When
the real parquets land, flip `dataset.synthetic=false` and the modeling work is a **config flip, not a
rebuild**: adding a baseline or a model is one factory line on a spine that already runs. Build this way
by default — the synthetic run is cheap insurance that the leakage armor and persistence work before real
data is on the line. *(Dogfood: M6 baselines on real data were a single flag flip on the synthetic-proven
spine — the pattern paid for itself.)*

## The model ladder (baselines are gates, not warm-ups)
1. `DummyClassifier(strategy="most_frequent")` / `DummyRegressor` — the floor every number is read against.
2. Logistic/linear regression on the same pipeline — interpretable, fast, often embarrassing to beat.
3. Gradient boosting (LightGBM / XGBoost / HistGradientBoosting) — the tabular default; on most
   structured problems it beats neural approaches at a fraction of the tuning cost. Reach past it
   only with evidence.
Handle missing values and categoricals natively where the booster supports it — less pipeline, less to leak.

## Cross-validation strategy = the split discipline, per-fold
- `StratifiedKFold` for classification; **`GroupKFold` whenever rows share an entity** (customer,
  patient, session) — the per-row random split of grouped data is this lane's most common fake result.
- Time-ordered rows → the `timeseries` skill's splits, not shuffled CV.
- CV selects; the held-out test set (untouched by any fold) is still the reported number.

## Traps with names
- **Target encoding leaks by default** — fit it per-fold (inside the pipeline via
  `TargetEncoder`), never on the full frame. Same for any statistic keyed on the label.
- **Imbalance:** accuracy lies; use PR-AUC/F1 at a *chosen* threshold, tuned on validation.
  Prefer `class_weight="balanced"` and threshold-moving before reaching for SMOTE (and if you must
  resample, resample inside the pipeline so CV sees it per-fold).
- **Impurity feature importances mislead** (biased to high-cardinality features; computed on
  train). Use permutation importance on validation, or SHAP; drop-and-refit for the real test.
- **Calibrate if probabilities are consumed** (`CalibratedClassifierCV`, reliability curve) — a
  well-ranked but overconfident model misprices every downstream decision.
- **Persist pipeline + model as ONE artifact** (`joblib.dump(model)` of the full pipeline), with
  sklearn's exact version pinned — unpickling across sklearn versions is undefined behavior.
  Version the artifact via `data-dvc`; log it to the tracker.
