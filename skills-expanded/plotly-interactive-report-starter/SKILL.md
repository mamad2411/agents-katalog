# Plotly Interactive Report Starter

Use this skill to turn a small deterministic TSV into an interactive HTML report with Plotly.

## Run

```bash
./slurm/envs/statistics/bin/python \
  skills/visualization-and-reporting/plotly-interactive-report-starter/scripts/render_plotly_interactive_report.py \
  --input skills/visualization-and-reporting/plotly-interactive-report-starter/examples/toy_measurements.tsv \
  --html-out scratch/plotly/report.html \
  --summary-out scratch/plotly/report_summary.json
```

## Output

- interactive HTML file
- compact JSON summary with trace count, slope, intercept, and `r_squared`

## Notes

- This is a starter for the taxonomy leaf `interactive-reports`.
- The example dataset is deterministic and small enough for repository-level smoke tests.
