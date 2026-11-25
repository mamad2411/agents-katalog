# Matminer Composition Featurization

Use this skill to compute deterministic stoichiometry-style composition features for a short list of formulas with `matminer`.

## What it does

- Parses one or more formulas with `pymatgen`.
- Computes `matminer` stoichiometry features for each composition.
- Returns compact JSON with reduced formulas, simple stoichiometry norms, and top element fractions.

## When to use it

- You need a first runnable materials-informatics starter in this repository.
- You want a light composition-featurization template before moving to heavier property-prediction workflows.

## Example

```bash
slurm/envs/materials/bin/python skills/materials-science-and-engineering/matminer-composition-featurization/scripts/run_matminer_composition_features.py \
  --formula Fe2O3 \
  --formula LiFePO4 \
  --out scratch/materials/matminer_features.json
```

## Verification

- Skill-local tests: `python3 -m unittest discover -s skills/materials-science-and-engineering/matminer-composition-featurization/tests -p 'test_*.py'`
- Repository smoke: `python3 -m unittest tests.smoke.test_frontier_domain_skills -v`
