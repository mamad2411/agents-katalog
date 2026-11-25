# SciPy Statistical Testing Starter

Use this skill to run a small deterministic hypothesis-testing workflow over two toy groups and summarize the results.

## What This Skill Does

- reads a tiny tabular dataset with `group` and `value` columns
- computes per-group means
- runs Welch's t-test and Mann-Whitney U
- reports p-values, effect size, and the higher-mean group

## When To Use It

- when you need a starter for `statistical-testing`
- when you want a small `scipy.stats` regression fixture
- when you need a machine-readable summary for downstream reporting

## Run

```bash
./slurm/envs/statistics/bin/python skills/statistical-and-machine-learning-foundations-for-science/scipy-statistical-testing-starter/scripts/run_scipy_statistical_testing.py --input skills/statistical-and-machine-learning-foundations-for-science/scipy-statistical-testing-starter/examples/toy_groups.tsv --out scratch/statistics/scipy_statistical_testing_summary.json
```
