# Optuna Bayesian Optimization Starter

Use this skill to run a deterministic Optuna optimization loop on a small synthetic objective and inspect the best trial summary.

## What This Skill Does

- defines a two-parameter toy objective
- optimizes it with Optuna's TPE sampler
- records the best trial, best parameters, and a short ranked trial table

## When To Use It

- when you need a runnable `bayesian-optimization` starter
- when you want a local Optuna example before wiring in an expensive scientific objective
- when you need deterministic optimization outputs for repository tests

## Run

```bash
./slurm/envs/statistics/bin/python skills/statistical-and-machine-learning-foundations-for-science/optuna-bayesian-optimization-starter/scripts/run_optuna_bayesian_optimization.py --out scratch/optuna/bayesian_optimization_summary.json
```

## Notes

- The objective is synthetic and smooth on purpose; it exists to verify the optimization loop, not to benchmark samplers.
- Increase the trial budget only after replacing the toy objective with a real scientific function.
