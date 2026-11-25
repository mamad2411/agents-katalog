# Chaospy Uncertainty Propagation Starter

Use this skill to run a deterministic uncertainty-propagation toy workflow with Chaospy and inspect a machine-readable summary of the propagated response distribution.

## What This Skill Does

- defines a small two-parameter input distribution with one Gaussian and one uniform variable
- builds a polynomial-chaos surrogate with quadrature
- reports the propagated mean, standard deviation, percentiles, and representative quadrature evaluations

## When To Use It

- when you need a runnable `uncertainty-aware-simulation` starter
- when you want a local Chaospy example before wiring in an expensive scientific simulator
- when you need deterministic uncertainty summaries for repository tests

## Run

```bash
./slurm/envs/numerics/bin/python skills/scientific-computing-and-numerical-methods/chaospy-uncertainty-propagation-starter/scripts/run_chaospy_uncertainty_propagation.py \
  --config skills/scientific-computing-and-numerical-methods/chaospy-uncertainty-propagation-starter/examples/toy_parameters.json \
  --out scratch/numerics/chaospy_uncertainty_summary.json
```

## Notes

- The response model is intentionally synthetic; it exists to verify the UQ loop, not to stand in for a real simulator.
- The script uses deterministic quadrature rather than random sampling so the summary is stable across reruns.
