# Papermill Parameterized Notebook Starter

Use this skill to execute a tiny parameterized notebook with Papermill and capture a deterministic summary plus the rendered output notebook.

## What This Skill Does

- runs a toy notebook with injected parameters
- materializes an executed `.ipynb`
- extracts the final JSON result from notebook cell outputs

## When To Use It

- when you need a runnable `reproducible-notebooks` starter
- when you want a lightweight parameterized notebook pattern before scaling to a real analysis notebook
- when you need a local smoke path for notebook execution

## Run

```bash
./slurm/envs/reporting/bin/python skills/reproducible-workflows/papermill-parameterized-notebook-starter/scripts/run_papermill_parameterized_notebook.py --input skills/reproducible-workflows/papermill-parameterized-notebook-starter/examples/toy_parameters.ipynb --output-notebook scratch/papermill/toy_parameters_executed.ipynb --summary-out scratch/papermill/toy_parameters_summary.json --x 5 --y 7
```

## Notes

- The example notebook stays intentionally small and arithmetic-only so execution remains stable on a generic `python3` kernel.
- Replace the toy notebook after the starter passes locally and in the repository test surface.
