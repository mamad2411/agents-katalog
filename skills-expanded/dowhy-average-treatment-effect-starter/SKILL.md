# DoWhy Average Treatment Effect Starter

Use this skill to estimate a deterministic toy average treatment effect with DoWhy and summarize a simple placebo refutation.

## What it does

- Builds a toy observational dataset with one confounder, one binary treatment, and one continuous outcome.
- Identifies the backdoor estimand with DoWhy.
- Estimates the average treatment effect with linear regression.
- Runs a placebo-treatment refutation and returns compact JSON.

## When to use it

- You need a minimal local starter for causal-inference workflows in Python.
- You want a verified example of identification, estimation, and refutation with DoWhy.

## Example

```bash
slurm/envs/causal/bin/python skills/statistical-and-machine-learning-foundations-for-science/dowhy-average-treatment-effect-starter/scripts/run_dowhy_average_treatment_effect.py \
  --out scratch/dowhy/average_treatment_effect_summary.json
```

## Verification

- Skill-local tests: `python3 -m unittest discover -s skills/statistical-and-machine-learning-foundations-for-science/dowhy-average-treatment-effect-starter/tests -p 'test_*.py'`
- Repository smoke: `python3 -m unittest tests.smoke.test_phase24_frontier_closure_skills -v`
