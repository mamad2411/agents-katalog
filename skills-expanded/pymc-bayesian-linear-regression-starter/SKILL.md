# PyMC Bayesian Linear Regression Starter

Use this skill to fit a tiny Bayesian linear regression with PyMC and summarize posterior means plus credible intervals.

## What it does

- Loads a deterministic toy `(x, y)` table.
- Fits a simple Bayesian regression with PyMC.
- Summarizes posterior means, 90% intervals, and a few posterior predictive means.
- Returns compact JSON suitable for downstream scientific inference workflows.

## When to use it

- You need a local starter for Bayesian modeling in science workflows.
- You want a minimal example of PyMC sampling and ArviZ-based posterior summarization.

## Example

```bash
slurm/envs/statistics/bin/python skills/statistical-and-machine-learning-foundations-for-science/pymc-bayesian-linear-regression-starter/scripts/run_pymc_linear_regression.py \
  --input skills/statistical-and-machine-learning-foundations-for-science/pymc-bayesian-linear-regression-starter/examples/toy_observations.tsv \
  --out scratch/pymc/linear_regression_summary.json
```

## Verification

- Skill-local tests: `python3 -m unittest discover -s skills/statistical-and-machine-learning-foundations-for-science/pymc-bayesian-linear-regression-starter/tests -p 'test_*.py'`
- Repository smoke: `python3 -m unittest tests.smoke.test_frontier_domain_skills -v`
