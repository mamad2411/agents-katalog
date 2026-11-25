# Matminer Toy Property Prediction Starter

Use this skill to featurize a small composition table with `matminer` and fit a deterministic toy property predictor.

## What it does

- Loads a toy TSV of formulas and target values.
- Uses `matminer` composition featurizers to build numeric features.
- Fits a small scikit-learn regressor and summarizes training predictions plus feature importances.
- Returns compact JSON suitable for materials-property-prediction starter workflows.

## When to use it

- You need a local starter for materials-property prediction.
- You want a minimal example that connects composition featurization to a predictive model.

## Example

```bash
slurm/envs/materials/bin/python skills/materials-science-and-engineering/matminer-toy-property-prediction-starter/scripts/run_matminer_toy_property_prediction.py \
  --input skills/materials-science-and-engineering/matminer-toy-property-prediction-starter/examples/toy_materials.tsv \
  --out scratch/materials/property_prediction_summary.json
```

## Verification

- Skill-local tests: `python3 -m unittest discover -s skills/materials-science-and-engineering/matminer-toy-property-prediction-starter/tests -p 'test_*.py'`
- Repository smoke: `python3 -m unittest tests.smoke.test_frontier_leaf_expansion_skills -v`
