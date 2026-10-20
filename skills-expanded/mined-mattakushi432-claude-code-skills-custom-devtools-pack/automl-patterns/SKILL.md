---
name: automl-patterns
description: "When to activate: AutoML, Optuna, Ray Tune, AutoGluon, FLAML, hyperparameter optimization, NAS, hyperparameter search"
origin: zakr
metadata:
  namespace: zakr/devtools-pack
  version: 1.0.0
  category: ml-ai
  language: python
  platforms: [claude-code, codex, gemini-cli, cursor, aider, windsurf]
---
# AutoML & Hyperparameter Optimization Patterns

## Optuna

```python
import optuna
from sklearn.ensemble import GradientBoostingClassifier
from sklearn.model_selection import cross_val_score

def objective(trial: optuna.Trial) -> float:
    params = {
        "n_estimators": trial.suggest_int("n_estimators", 100, 1000, step=100),
        "learning_rate": trial.suggest_float("learning_rate", 1e-3, 0.3, log=True),
        "max_depth": trial.suggest_int("max_depth", 3, 9),
        "subsample": trial.suggest_float("subsample", 0.5, 1.0),
        "min_samples_leaf": trial.suggest_int("min_samples_leaf", 1, 20),
    }
    model = GradientBoostingClassifier(**params, random_state=42)
    scores = cross_val_score(model, X_train, y_train, cv=5, scoring="roc_auc", n_jobs=-1)
    return scores.mean()

study = optuna.create_study(
    direction="maximize",
    sampler=optuna.samplers.TPESampler(seed=42),
    pruner=optuna.pruners.MedianPruner(n_warmup_steps=5),
    storage="sqlite:///optuna.db",
    study_name="gbm_search",
    load_if_exists=True,
)
study.optimize(objective, n_trials=100, timeout=3600, n_jobs=2)

print("Best params:", study.best_params)
print("Best AUC:", study.best_value)
```

## Optuna with Pruning (for Iterative Models)

```python
import lightgbm as lgb

def objective(trial):
    params = {
        "num_leaves": trial.suggest_int("num_leaves", 20, 300),
        "learning_rate": trial.suggest_float("lr", 1e-3, 0.1, log=True),
        "min_child_samples": trial.suggest_int("min_child_samples", 5, 100),
    }
    dtrain = lgb.Dataset(X_train, y_train)
    dval = lgb.Dataset(X_val, y_val, reference=dtrain)

    pruning_callback = optuna.integration.LightGBMPruningCallback(trial, "auc")
    model = lgb.train(
        params, dtrain, num_boost_round=1000,
        valid_sets=[dval],
        callbacks=[lgb.early_stopping(50), lgb.log_evaluation(0), pruning_callback],
    )
    return model.best_score["valid_0"]["auc"]
```

## Ray Tune

```python
from ray import tune
from ray.tune.schedulers import ASHAScheduler
from ray.tune.search.optuna import OptunaSearch

def train_fn(config):
    model = GradientBoostingClassifier(**config)
    scores = cross_val_score(model, X_train, y_train, cv=3, scoring="roc_auc")
    tune.report({"auc": scores.mean()})

scheduler = ASHAScheduler(metric="auc", mode="max", max_t=10, grace_period=1)
searcher = OptunaSearch(metric="auc", mode="max")

analysis = tune.run(
    train_fn,
    config={
        "n_estimators": tune.randint(100, 1000),
        "learning_rate": tune.loguniform(1e-3, 0.3),
        "max_depth": tune.randint(3, 10),
    },
    num_samples=50,
    scheduler=scheduler,
    search_alg=searcher,
    resources_per_trial={"cpu": 2},
)
print("Best config:", analysis.best_config)
```

## AutoGluon Tables

```python
from autogluon.tabular import TabularDataset, TabularPredictor

train_data = TabularDataset("train.csv")
test_data = TabularDataset("test.csv")

predictor = TabularPredictor(
    label="target",
    problem_type="binary",
    eval_metric="roc_auc",
    path="autogluon_models/",
).fit(
    train_data,
    time_limit=3600,
    presets="best_quality",    # or "good_quality", "medium_quality"
    excluded_model_types=["KNN"],
)

predictions = predictor.predict_proba(test_data)["True"]
print(predictor.leaderboard(test_data, silent=True))
```

## FLAML (Fast & Lightweight AutoML)

```python
from flaml import AutoML

automl = AutoML()
automl.fit(
    X_train, y_train,
    task="classification",
    metric="roc_auc",
    time_budget=600,           # seconds
    estimator_list=["lgbm", "xgboost", "rf", "extra_tree"],
    eval_method="cv",
    n_splits=5,
    seed=42,
)
print("Best model:", automl.best_estimator)
print("Best config:", automl.best_config)
preds = automl.predict_proba(X_test)[:, 1]
```

## Search Space Design Tips

- **Log-uniform** for learning rates, regularization (`log=True` in Optuna)
- **Integer with step** for tree count (`step=50` avoids dense search near optimal)
- **Categorical** for algorithms, activations, optimizers
- Start with wide ranges, then narrow around best config
- Use **MedianPruner** to kill clearly bad trials early (saves 30-50% compute)
