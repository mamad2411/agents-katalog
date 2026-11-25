# pre-commit Regression Testing Starter

Use this skill to build a tiny disposable repository and run deterministic local `pre-commit` hooks as a regression-testing starter.

## Run

```bash
python3 \
  skills/meta-maintenance/precommit-regression-testing-starter/scripts/run_precommit_regression.py \
  --workspace scratch/precommit-guard/workspace \
  --out scratch/precommit-guard/summary.json
```

## What It Verifies

- a tiny Python module compiles cleanly
- a tiny JSON metadata file passes a local validation hook
- the starter can run `pre-commit` end to end inside a disposable workspace

## Notes

- This is a starter for the taxonomy leaf `regression-testing`.
- The temporary repository is self-contained and does not modify the main repository.
