# GitHub Actions Scientific CI Starter

Use this skill to generate a repository-aware GitHub Actions workflow that runs validation, site generation, tests, and a small smoke subset for this project.

## What This Skill Does

- renders a ready-to-commit workflow YAML file
- targets the repository's `make validate`, `make build-site`, and `make test` entry points
- optionally includes a list of smoke targets for faster CI confidence checks

## When To Use It

- when you need a starter for `ci-for-scientific-pipelines`
- when you want a canonical Actions workflow around the current `Makefile`
- when you need a reproducible template before adding heavier matrix or cache logic

## Run

```bash
python3 skills/reproducible-workflows/github-actions-scientific-ci-starter/scripts/render_github_actions_scientific_ci.py --workflow-out scratch/github-actions/sciskill_ci.yml --summary-out scratch/github-actions/sciskill_ci_summary.json --smoke-target smoke-zarr --smoke-target smoke-openmm-md --smoke-target smoke-optuna
```

## Notes

- The generated workflow is intentionally conservative and single-job.
- Extend it only after the base validation path is stable in your own CI environment.
