# Matplotlib Publication Plot Starter

Use this skill to turn a small tabular dataset into a deterministic publication-style figure and compact fit summary.

## What it does

- Loads a toy TSV of `x` and `y` observations.
- Fits a simple linear trend with NumPy.
- Renders a two-panel Matplotlib figure with the fitted line and residual plot.
- Saves a PNG plus a JSON summary with fit statistics.

## When to use it

- You need a local starter for publication plots.
- You want a reproducible figure-generation pattern that can later be swapped for real data.

## Example

```bash
slurm/envs/statistics/bin/python skills/visualization-and-reporting/matplotlib-publication-plot-starter/scripts/render_publication_plot.py \
  --input skills/visualization-and-reporting/matplotlib-publication-plot-starter/examples/toy_measurements.tsv \
  --png-out scratch/matplotlib/publication_plot.png \
  --summary-out scratch/matplotlib/publication_plot_summary.json
```

## Verification

- Skill-local tests: `python3 -m unittest discover -s skills/visualization-and-reporting/matplotlib-publication-plot-starter/tests -p 'test_*.py'`
- Repository smoke: `python3 -m unittest tests.smoke.test_cross_cutting_domain_skills -v`
