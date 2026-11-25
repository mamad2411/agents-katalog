# Metadata Harmonization Starter

Use this skill to harmonize small metadata tables with inconsistent column names and categorical labels into one canonical TSV plus a compact JSON summary.

## What This Skill Does

- reads one or more tabular metadata files
- applies a JSON mapping from source columns to canonical fields
- normalizes selected categorical values such as `sex` and `condition`
- writes a harmonized TSV and a machine-readable summary

## When To Use It

- when you need a starter for `metadata-harmonization`
- when multiple small test fixtures use different metadata headers
- when you want deterministic harmonized outputs before validation or format conversion

## Run

```bash
python3 skills/data-acquisition-and-dataset-handling/metadata-harmonization-starter/scripts/run_metadata_harmonization.py \
  --input skills/data-acquisition-and-dataset-handling/metadata-harmonization-starter/examples/cohort_a.tsv \
  --input skills/data-acquisition-and-dataset-handling/metadata-harmonization-starter/examples/cohort_b.tsv \
  --mapping skills/data-acquisition-and-dataset-handling/metadata-harmonization-starter/examples/column_mapping.json \
  --out-tsv scratch/metadata-harmonization/harmonized_metadata.tsv \
  --summary-out scratch/metadata-harmonization/harmonized_metadata_summary.json
```

## Notes

- The starter keeps the mapping external so the same script can be reused for other tiny fixtures.
- Canonical rows are sorted by `sample_id` to keep committed outputs deterministic.
