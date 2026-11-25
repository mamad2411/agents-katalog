# Frictionless Tabular Validation Starter

Use this skill to validate a small CSV or TSV table against a simple Frictionless schema and emit a compact machine-readable error summary.

## What it does

- loads a tabular input file plus a JSON schema descriptor
- runs `frictionless` validation from the repo-managed `data-tools` prefix
- reports row counts, field names, and normalized validation errors

## When to use it

- you need a verified starter for `data-validation`
- you want a deterministic schema-validation smoke fixture for tabular scientific data
- you need structured validation output before downstream ingestion or conversion

## Example

```bash
./slurm/envs/data-tools/bin/python skills/data-acquisition-and-dataset-handling/frictionless-tabular-validation-starter/scripts/run_frictionless_tabular_validation.py \
  --input skills/data-acquisition-and-dataset-handling/frictionless-tabular-validation-starter/examples/toy_people_valid.csv \
  --schema skills/data-acquisition-and-dataset-handling/frictionless-tabular-validation-starter/examples/toy_people_schema.json \
  --out scratch/data-validation/frictionless_summary.json
```

## Verification

- Skill-local tests: `python3 -m unittest discover -s skills/data-acquisition-and-dataset-handling/frictionless-tabular-validation-starter/tests -p 'test_*.py'`
- Expected valid summary: `valid == true`, `row_count == 3`, `error_count == 0`
