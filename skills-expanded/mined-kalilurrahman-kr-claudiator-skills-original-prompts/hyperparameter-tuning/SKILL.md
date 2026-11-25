---
name: hyperparameter-tuning
description: Optimize ML model hyperparameters with grid search, random search, Bayesian optimization. Outputs tuning strategy, search spaces, and best parameters.
argument-hint: [model type, compute budget, optimization metric]
allowed-tools: Read, Write, Bash
---

# Hyperparameter Tuning

Optimize model hyperparameters systematically. Not manual guessing — grid search, random search, Bayesian optimization to find best parameters within compute budget.

## Process

1. **Define search space.** Hyperparameters to tune, ranges, distributions.
2. **Choose search strategy.** Grid (exhaustive), random (budget), Bayesian (efficient).
3. **Select metric.** Accuracy, F1, RMSE, AUC, cross-validation score.
4. **Set budget.** Max trials, time limit, early stopping.
5. **Run tuning.** Parallel trials, track results, log best params.
6. **Validate best model.** Test set performance, compare to baseline.
7. **Document results.** Best params, performance gain, compute cost.

## Output Format

### Hyperparameter Tuning: [Model]

**Model:** XGBoost Classifier  
**Strategy:** Bayesian Optimization (Optuna)  
**Search Space:** 6 hyperparameters  
**Trials:** 100  
**Best F1:** 0.89 (baseline: 0.84)  
**Compute:** 2 hours on 8 CPUs

---

## Search Strategies Comparison

| Strategy | Trials | Coverage | Efficiency | Use When |
|----------|--------|----------|------------|----------|
| Grid Search | All combinations | 100% | Low | Small search space (< 100 trials) |
| Random Search | Random sampling | Stochastic | Medium | Large search space, limited budget |
| Bayesian Optimization | Guided by priors | Focused | High | Expensive evaluations, >50 trials |
| Hyperband | Early stopping | Adaptive | High | Deep learning, long training times |

---

## Grid Search

### Scikit-learn
```python
from sklearn.model_selection import GridSearchCV
from sklearn.ensemble import RandomForestClassifier

# Define search space
param_grid = {
    'n_estimators': [100, 200, 300],
    'max_depth': [10, 20, 30, None],
    'min_samples_split': [2, 5, 10],
    'min_samples_leaf': [1, 2, 4]
}

# Total trials: 3 × 4 × 3 × 3 = 108

# Create grid search
grid_search = GridSearchCV(
    estimator=RandomForestClassifier(),
    param_grid=param_grid,
    cv=5,  # 5-fold cross-validation
    scoring='f1',
    n_jobs=-1,  # Use all CPUs
    verbose=2
)

# Run search
grid_search.fit(X_train, y_train)

# Best parameters
print(f"Best params: {grid_search.best_params_}")
print(f"Best score: {grid_search.best_score_:.3f}")

# Best model
best_model = grid_search.best_estimator_
```

### Results Analysis
```python
import pandas as pd

# View all results
results = pd.DataFrame(grid_search.cv_results_)

# Top 10 configurations
top_10 = results.sort_values('rank_test_score').head(10)
print(top_10[['params', 'mean_test_score', 'std_test_score']])

# Visualize parameter importance
import matplotlib.pyplot as plt

for param in param_grid.keys():
    plt.figure()
    for value in param_grid[param]:
        mask = results['param_' + param] == value
        plt.scatter(
            results[mask]['mean_test_score'],
            [value] * mask.sum()
        )
    plt.xlabel('Score')
    plt.ylabel(param)
    plt.title(f'Impact of {param}')
    plt.show()
```

---

## Random Search

```python
from sklearn.model_selection import RandomizedSearchCV
from scipy.stats import randint, uniform

# Define distributions
param_distributions = {
    'n_estimators': randint(100, 500),
    'max_depth': randint(5, 50),
    'min_samples_split': randint(2, 20),
    'min_samples_leaf': randint(1, 10),
    'max_features': uniform(0.1, 0.9)
}

# Random search
random_search = RandomizedSearchCV(
    estimator=RandomForestClassifier(),
    param_distributions=param_distributions,
    n_iter=100,  # Budget: 100 trials
    cv=5,
    scoring='f1',
    n_jobs=-1,
    random_state=42
)

random_search.fit(X_train, y_train)

print(f"Best params: {random_search.best_params_}")
print(f"Best score: {random_search.best_score_:.3f}")
```

**Advantage:** Explores more of search space with same budget
```
Grid Search (100 trials):
  n_estimators: [100, 200, 300, 400, 500]  # 5 values
  max_depth: [10, 20, 30, 40]              # 4 values
  Total: 5 × 4 = 20 combinations, run 5 times = 100 trials
  Coverage: Only 20 unique configurations

Random Search (100 trials):
  n_estimators: uniform(100, 500)
  max_depth: uniform(5, 50)
  Total: 100 unique configurations
  Coverage: Much broader
```

---

## Bayesian Optimization (Optuna)

```python
import optuna
from sklearn.ensemble import XGBClassifier
from sklearn.model_selection import cross_val_score

def objective(trial):
    """Objective function to minimize"""
    
    # Define hyperparameters
    params = {
        'n_estimators': trial.suggest_int('n_estimators', 100, 1000),
        'max_depth': trial.suggest_int('max_depth', 3, 10),
        'learning_rate': trial.suggest_float('learning_rate', 0.01, 0.3, log=True),
        'subsample': trial.suggest_float('subsample', 0.5, 1.0),
        'colsample_bytree': trial.suggest_float('colsample_bytree', 0.5, 1.0),
        'gamma': trial.suggest_float('gamma', 0, 5),
        'reg_alpha': trial.suggest_float('reg_alpha', 0, 10),
        'reg_lambda': trial.suggest_float('reg_lambda', 0, 10)
    }
    
    # Train model
    model = XGBClassifier(**params, random_state=42)
    
    # Cross-validation score
    score = cross_val_score(
        model, X_train, y_train,
        cv=5,
        scoring='f1',
        n_jobs=-1
    ).mean()
    
    return score

# Create study
study = optuna.create_study(
    direction='maximize',  # Maximize F1 score
    sampler=optuna.samplers.TPESampler(seed=42)
)

# Run optimization
study.optimize(
    objective,
    n_trials=100,
    timeout=3600,  # 1 hour max
    show_progress_bar=True
)

# Best trial
print(f"Best params: {study.best_params}")
print(f"Best score: {study.best_value:.3f}")

# Visualize optimization
import optuna.visualization as vis

vis.plot_optimization_history(study)
vis.plot_param_importances(study)
vis.plot_parallel_coordinate(study)
```

### Optuna with Pruning (Early Stopping)
```python
from optuna.integration import XGBoostPruningCallback

def objective_with_pruning(trial):
    params = {
        'n_estimators': 1000,  # Large number
        'max_depth': trial.suggest_int('max_depth', 3, 10),
        'learning_rate': trial.suggest_float('learning_rate', 0.01, 0.3, log=True),
        # ... other params
    }
    
    model = XGBClassifier(**params)
    
    # Add pruning callback
    pruning_callback = XGBoostPruningCallback(trial, 'validation-logloss')
    
    model.fit(
        X_train, y_train,
        eval_set=[(X_val, y_val)],
        callbacks=[pruning_callback],
        verbose=False
    )
    
    score = f1_score(y_val, model.predict(X_val))
    
    return score

study.optimize(objective_with_pruning, n_trials=100)
```

**Benefit:** Stops unpromising trials early, saves compute

---

## Hyperband (Successive Halving)

```python
from sklearn.model_selection import HalvingRandomSearchCV

# Define search space
param_distributions = {
    'n_estimators': randint(100, 1000),
    'max_depth': randint(3, 20),
    'learning_rate': uniform(0.01, 0.3)
}

# Hyperband search
halving_search = HalvingRandomSearchCV(
    estimator=XGBClassifier(),
    param_distributions=param_distributions,
    factor=3,  # Reduce candidates by 3x each round
    resource='n_estimators',  # Train with increasing n_estimators
    max_resources=1000,
    min_resources=100,
    cv=5,
    scoring='f1',
    n_jobs=-1
)

halving_search.fit(X_train, y_train)

print(f"Best params: {halving_search.best_params_}")
print(f"Best score: {halving_search.best_score_:.3f}")
```

**How it works:**
```
Round 1: 81 configs, n_estimators=100
  → Keep top 27 (81/3)

Round 2: 27 configs, n_estimators=300
  → Keep top 9 (27/3)

Round 3: 9 configs, n_estimators=900
  → Keep top 3 (9/3)

Round 4: 3 configs, n_estimators=1000 (full training)
  → Select best
```

---

## Deep Learning: Ray Tune

```python
from ray import tune
from ray.tune.schedulers import ASHAScheduler
import torch
import torch.nn as nn

def train_model(config):
    """Training function"""
    model = nn.Sequential(
        nn.Linear(config['input_size'], config['hidden_size']),
        nn.ReLU(),
        nn.Dropout(config['dropout']),
        nn.Linear(config['hidden_size'], config['output_size'])
    )
    
    optimizer = torch.optim.Adam(
        model.parameters(),
        lr=config['lr'],
        weight_decay=config['weight_decay']
    )
    
    for epoch in range(10):
        # Training loop
        loss = train_epoch(model, optimizer, train_loader)
        val_acc = validate(model, val_loader)
        
        # Report metrics to Ray Tune
        tune.report(loss=loss, accuracy=val_acc)

# Define search space
config = {
    'lr': tune.loguniform(1e-4, 1e-1),
    'hidden_size': tune.choice([64, 128, 256, 512]),
    'dropout': tune.uniform(0.1, 0.5),
    'weight_decay': tune.loguniform(1e-5, 1e-2)
}

# ASHA scheduler (early stopping)
scheduler = ASHAScheduler(
    max_t=10,
    grace_period=1,
    reduction_factor=2
)

# Run tuning
result = tune.run(
    train_model,
    config=config,
    num_samples=100,
    scheduler=scheduler,
    resources_per_trial={'cpu': 2, 'gpu': 0.5}
)

# Best config
best_config = result.get_best_config(metric='accuracy', mode='max')
print(f"Best config: {best_config}")
```

---

## MLflow Tracking

```python
import mlflow
import mlflow.sklearn

mlflow.set_experiment("hyperparameter-tuning")

def objective_with_logging(trial):
    with mlflow.start_run(nested=True):
        params = {
            'n_estimators': trial.suggest_int('n_estimators', 100, 1000),
            'max_depth': trial.suggest_int('max_depth', 3, 10),
            'learning_rate': trial.suggest_float('learning_rate', 0.01, 0.3, log=True)
        }
        
        # Log parameters
        mlflow.log_params(params)
        
        # Train model
        model = XGBClassifier(**params)
        model.fit(X_train, y_train)
        
        # Evaluate
        score = f1_score(y_val, model.predict(X_val))
        
        # Log metrics
        mlflow.log_metric('f1_score', score)
        
        # Log model
        mlflow.sklearn.log_model(model, "model")
        
        return score

study = optuna.create_study(direction='maximize')
study.optimize(objective_with_logging, n_trials=100)
```

**View in MLflow UI:**
```bash
mlflow ui
# Open http://localhost:5000
```

---

## Nested Cross-Validation

```python
from sklearn.model_selection import cross_val_score, KFold

# Outer CV: Evaluate generalization
outer_cv = KFold(n_splits=5, shuffle=True, random_state=42)

# Inner CV: Tune hyperparameters
inner_cv = KFold(n_splits=3, shuffle=True, random_state=42)

outer_scores = []

for train_idx, test_idx in outer_cv.split(X):
    X_train_outer, X_test_outer = X[train_idx], X[test_idx]
    y_train_outer, y_test_outer = y[train_idx], y[test_idx]
    
    # Inner loop: Hyperparameter tuning
    grid_search = GridSearchCV(
        RandomForestClassifier(),
        param_grid,
        cv=inner_cv,
        scoring='f1'
    )
    grid_search.fit(X_train_outer, y_train_outer)
    
    # Evaluate best model on outer test set
    best_model = grid_search.best_estimator_
    score = f1_score(y_test_outer, best_model.predict(X_test_outer))
    outer_scores.append(score)

print(f"Outer CV scores: {outer_scores}")
print(f"Mean: {np.mean(outer_scores):.3f} ± {np.std(outer_scores):.3f}")
```

---

## Search Space Design

### Continuous Parameters (log-scale)
```python
# Learning rate (spans orders of magnitude)
'learning_rate': trial.suggest_float('learning_rate', 1e-5, 1e-1, log=True)
# Samples: 0.00001, 0.0001, 0.001, 0.01, 0.1

# NOT log-scale (poor sampling)
'learning_rate': trial.suggest_float('learning_rate', 0, 0.1)
# Samples: 0.00, 0.02, 0.04, 0.06, 0.08 (misses small values!)
```

### Categorical Parameters
```python
# Activation function
'activation': trial.suggest_categorical('activation', ['relu', 'tanh', 'sigmoid'])

# Optimizer
'optimizer': trial.suggest_categorical('optimizer', ['adam', 'sgd', 'rmsprop'])
```

### Conditional Parameters
```python
def objective(trial):
    optimizer_name = trial.suggest_categorical('optimizer', ['adam', 'sgd'])
    
    if optimizer_name == 'adam':
        beta1 = trial.suggest_float('adam_beta1', 0.8, 0.99)
        beta2 = trial.suggest_float('adam_beta2', 0.9, 0.999)
    elif optimizer_name == 'sgd':
        momentum = trial.suggest_float('sgd_momentum', 0, 0.99)
```

---

## Early Stopping

```python
from sklearn.metrics import f1_score

best_score = 0
patience = 10
trials_without_improvement = 0

for trial in range(max_trials):
    score = evaluate_config(config)
    
    if score > best_score:
        best_score = score
        trials_without_improvement = 0
    else:
        trials_without_improvement += 1
    
    if trials_without_improvement >= patience:
        print(f"Early stopping at trial {trial}")
        break
```

---

## Parallel Tuning

```python
# Optuna with parallel workers
study = optuna.create_study(
    direction='maximize',
    storage='mysql://user:pass@localhost/optuna',  # Shared DB
    study_name='xgboost-tuning'
)

# Run multiple workers
# Worker 1:
study.optimize(objective, n_trials=50)

# Worker 2 (different machine):
study.optimize(objective, n_trials=50)

# Results combined in shared database
```

## Rules

- Start with random search, not grid — explores more configurations with same budget.
- Use log-scale for learning rates — spans orders of magnitude (1e-5 to 1e-1).
- Bayesian optimization for expensive models — deep learning, large datasets.
- Hyperband for quick iterations — early stopping saves compute.
- Track all trials in MLflow — reproducibility and analysis.
- Nested CV for unbiased estimates — tune on inner loop, evaluate on outer.
- Set realistic budgets — 100 trials often sufficient, 1000+ rarely needed.
- Tune most impactful params first — learning rate, depth, regularization.
- Validate on holdout set — cross-validation scores can be optimistic.
- Document best params and gains — baseline vs tuned performance comparison.
