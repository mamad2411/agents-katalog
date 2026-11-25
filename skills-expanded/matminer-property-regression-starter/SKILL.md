# Matminer Property Regression Starter

Use this skill to featurize simple formulas with Matminer and fit a deterministic toy regression model for materials-property prediction.

## What This Skill Does

- converts formulas into composition features with Matminer
- fits a small deterministic regression model
- reports feature count, train fit quality, and holdout predictions

## When To Use It

- when a user asks for a starter on materials-property prediction
- when you need a lightweight local template before connecting to a larger materials dataset
- when you want a runnable example for the `materials-property-prediction` taxonomy leaf

## Run

```bash
./slurm/envs/materials/bin/python skills/materials-science-and-engineering/matminer-property-regression-starter/scripts/run_matminer_property_regression.py --out scratch/materials/property_regression_summary.json
```

## Notes

- This is a toy local regression starter, not a benchmark-quality predictive model.
- Pair it with larger curated datasets later if you need scientific performance claims.
