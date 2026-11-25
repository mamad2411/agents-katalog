# Quarto Notebook Report Starter

Use this skill to render a small deterministic Jupyter notebook into an HTML report with Quarto.

## What it does

- Copies a tiny example notebook into an isolated temporary workspace.
- Executes the notebook through Quarto's Jupyter engine.
- Produces a standalone HTML report.
- Returns compact JSON confirming that the expected title and executed output are present.

## When to use it

- You need a local starter for notebook-to-report conversion.
- You want a verified Quarto path that hides the repo-managed conda activation quirks.

## Example

```bash
python3 skills/visualization-and-reporting/quarto-notebook-report-starter/scripts/render_quarto_notebook_report.py \
  --input skills/visualization-and-reporting/quarto-notebook-report-starter/examples/toy_report.ipynb \
  --html-out scratch/quarto/toy_report.html \
  --summary-out scratch/quarto/toy_report_summary.json
```

## Verification

- Skill-local tests: `python3 -m unittest discover -s skills/visualization-and-reporting/quarto-notebook-report-starter/tests -p 'test_*.py'`
- Repository smoke: `python3 -m unittest tests.smoke.test_phase24_frontier_closure_skills -v`
