---
name: domino-experiment-setup
description: Set up MLflow experiment tracking in a Domino project by generating an experiment_setup.py helper with deployment-unique experiment names, Domino context tags, and framework auto-logging, plus an example training script. Use when the user asks to add or set up experiment tracking, MLflow logging, or autologging for a traditional ML project in Domino.
compatibility: Domino 6.3 and Domino Cloud. Runs in a Domino workspace or job, where MLflow tracking is preconfigured.
---

# Set Up Domino Experiment Tracking

Applies to Domino 6.3 and Domino Cloud.

Add MLflow experiment tracking to a traditional ML project. For LLM or agent tracing, use the
`domino-trace-setup` skill instead.

## Inputs

1. **Experiment base name**: use the one the user gave; otherwise use the project directory name.
2. **ML frameworks**: detect them from `requirements.txt`, `pyproject.toml`, `environment.yml`,
   or imports in the code.

Do not stop to ask for either. Make the changes with these defaults, then state the base name
and frameworks you used in the reply so the user can change them.

## Steps

1. Copy `assets/experiment_setup.py` from this skill's folder into the project. It provides:
   - `setup_experiment(base_name)`: sets an experiment named `<base>-<project>-<username>`.
   - `log_domino_context()`: tags the run with the Domino user, project, run ID, run number, and hardware tier id (`DOMINO_HARDWARE_TIER_ID`).
   - `setup_autolog()`: enables MLflow autologging for whichever supported frameworks are installed.
2. Report which frameworks were detected and will be autologged, for example:

   ```
   Detected frameworks:
   ✅ scikit-learn (requirements.txt)
   ✅ xgboost (requirements.txt)
   ❌ tensorflow (not found)
   ```

3. If the project trains large models, add the multipart-upload settings below.
4. Create an example training script, or wire the helpers into the user's existing script.

## Example training script

```python
# train.py
from experiment_setup import setup_experiment, log_domino_context, setup_autolog
import mlflow
from sklearn.ensemble import RandomForestClassifier
from sklearn.model_selection import train_test_split
from sklearn.datasets import load_iris

experiment_name = setup_experiment("iris-classifier")
setup_autolog()

iris = load_iris()
X_train, X_test, y_train, y_test = train_test_split(
    iris.data, iris.target, test_size=0.2, random_state=42
)

with mlflow.start_run(run_name="random-forest-v1"):
    log_domino_context()
    mlflow.log_param("custom_param", "value")

    model = RandomForestClassifier(n_estimators=100, max_depth=5)
    model.fit(X_train, y_train)

    test_accuracy = model.score(X_test, y_test)
    mlflow.log_metric("test_accuracy", test_accuracy)
    print(f"Test accuracy: {test_accuracy:.4f}")
    print(f"Run ID: {mlflow.active_run().info.run_id}")
```

## Important rules

- **Experiment names must be unique across the entire Domino deployment**, not just the project.
  Always keep the username and project suffix that `setup_experiment` adds.
- For large artifacts (LLMs, deep learning checkpoints), enable multipart upload:

  ```python
  os.environ['MLFLOW_ENABLE_PROXY_MULTIPART_UPLOAD'] = "true"
  os.environ['MLFLOW_MULTIPART_UPLOAD_CHUNK_SIZE'] = "104857600"  # 100MB
  ```

For run comparison, the model registry, and deeper MLflow usage, use the
`domino-experiment-tracking` skill.
