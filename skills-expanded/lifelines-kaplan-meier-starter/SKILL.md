# Lifelines Kaplan Meier Starter

Use this skill to run a deterministic Kaplan-Meier survival analysis over a toy cohort and summarize per-group survival curves.

## What it does

- Loads a tiny cohort table with durations, events, and group labels.
- Fits one Kaplan-Meier curve per group with `lifelines`.
- Returns compact JSON with median survival times and survival probabilities at fixed time points.
- Optionally renders a PNG survival plot.

## When to use it

- You need a local starter for survival-analysis workflows.
- You want a verified template for grouped time-to-event data in Python.

## Example

```bash
slurm/envs/statistics/bin/python skills/clinical-biomedical-data-science/lifelines-kaplan-meier-starter/scripts/run_lifelines_kaplan_meier.py \
  --input skills/clinical-biomedical-data-science/lifelines-kaplan-meier-starter/examples/toy_survival_cohort.tsv \
  --summary-out scratch/lifelines/kaplan_meier_summary.json \
  --png-out scratch/lifelines/kaplan_meier_plot.png
```

## Verification

- Skill-local tests: `python3 -m unittest discover -s skills/clinical-biomedical-data-science/lifelines-kaplan-meier-starter/tests -p 'test_*.py'`
- Repository smoke: `python3 -m unittest tests.smoke.test_phase25_agent_and_clinical_skills -v`
