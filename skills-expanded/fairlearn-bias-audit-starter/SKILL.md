# Fairlearn Bias Audit Starter

Use this skill to run a deterministic group fairness audit over a tiny clinical toy cohort with `fairlearn`.

## What it does

- Loads a fixed tabular cohort with binary labels, binary predictions, and a sensitive group column.
- Computes per-group accuracy, selection rate, true positive rate, and false positive rate with `MetricFrame`.
- Summarizes demographic parity and equalized odds gaps and ratios.
- Emits a compact JSON report and threshold-based audit flags for local debugging.

## When to use it

- You need a local starter for fairness or bias analysis in binary clinical risk models.
- You want a small, reproducible example before auditing a real cohort.

## Example

```bash
slurm/envs/statistics/bin/python skills/clinical-biomedical-data-science/fairlearn-bias-audit-starter/scripts/run_fairlearn_bias_audit.py \
  --input skills/clinical-biomedical-data-science/fairlearn-bias-audit-starter/examples/toy_fairness_cohort.tsv \
  --summary-out scratch/fairlearn/fairness_audit_summary.json
```

## Verification

- Skill-local tests: `python3 -m unittest discover -s skills/clinical-biomedical-data-science/fairlearn-bias-audit-starter/tests -p 'test_*.py'`
