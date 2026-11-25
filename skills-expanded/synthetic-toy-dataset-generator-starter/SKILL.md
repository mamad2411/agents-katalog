# Synthetic Toy Dataset Generator Starter

Use this skill to generate a deterministic tiny dataset bundle for tests, demos, and smoke fixtures.

## What This Skill Does

- creates a small sample sheet, feature sheet, and count matrix
- uses a fixed seed for deterministic values
- writes a manifest and a compact JSON summary
- keeps the output small enough to commit as a verified asset

## When To Use It

- when you need a starter for `synthetic-toy-dataset-generation-for-tests`
- when downstream skills need a small reusable fixture bundle
- when you want deterministic tabular test data without external downloads

## Run

```bash
python3 skills/data-acquisition-and-dataset-handling/synthetic-toy-dataset-generator-starter/scripts/generate_synthetic_toy_dataset.py \
  --sample-count 6 \
  --feature-count 4 \
  --seed 17 \
  --out-dir scratch/synthetic-toy-dataset/toy_bundle \
  --summary-out scratch/synthetic-toy-dataset/toy_bundle_summary.json
```

## Notes

- The generated bundle is intentionally generic and lightweight; it is designed to feed other skills' tests.
- The summary includes simple deterministic checks so regressions are easy to spot in CI.
