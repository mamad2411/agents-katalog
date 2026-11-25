---
name: ml-experiment-tracking
description: Logs params, metrics, code version and artifacts so ML experiments can be reproduced and compared. Use it when results are hard to trace back to a run.
---

# ML experiment tracking

A run is reproducible only if its code, data, config and seed are all recorded.

## Steps

1. Find what is in use (`grep -rn "mlflow\|wandb\|tensorboard" .`). Use it. If nothing exists, write one JSON file per run under `runs/<run_id>/` rather than adding a service.
2. Collect all settings in a single config object (dataclass or YAML) so one call can log it. Remove hardcoded hyperparameters scattered through the script.
3. At run start, record: the config, the random seed, the git commit hash, whether the working tree is dirty (`git status --porcelain`), the package versions (`pip freeze` or key libraries), and the Python and hardware details.
4. Fingerprint the data: file path plus a content hash or row count, or the version tag from your data store. A path alone is not enough.
5. Log metrics with a step number, separate for train and validation, plus final test metrics once at the end. Name them consistently (`val/auc`, not `valAUC` in one run and `auc_val` in another).
6. Save artifacts: the best checkpoint, the metrics file, and key plots. Link them to the run.
7. Tag the run with a short human name and a one line purpose, such as "lr sweep, no augmentation".
8. Add a small script that lists runs sorted by a metric and prints the config differences between two runs.

## Rules

- Never log secrets or raw personal data in params.
- Log the failure state too: mark crashed runs as failed.

## Report

What is tracked per run, where it is stored, and the command to compare two runs.
