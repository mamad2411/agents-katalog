# PyArrow Format Conversion Starter

Use this skill to convert a small tabular file into Parquet with PyArrow and inspect a deterministic round-trip summary.

## What This Skill Does

- reads a tiny tabular input with typed columns
- builds an Arrow table in memory
- writes a local Parquet file
- reads the Parquet file back and verifies the round trip

## When To Use It

- when you need a starter for `format-conversion`
- when you want a small Arrow-to-Parquet example without a larger data stack
- when you need a deterministic schema summary for tests or demos

## Run

```bash
./slurm/envs/data-tools/bin/python skills/data-acquisition-and-dataset-handling/pyarrow-format-conversion-starter/scripts/run_pyarrow_format_conversion.py --input skills/data-acquisition-and-dataset-handling/pyarrow-format-conversion-starter/examples/toy_matrix.tsv --parquet-out scratch/pyarrow/toy_table.parquet --summary-out scratch/pyarrow/toy_table_summary.json
```

## Notes

- The example uses tab-separated input to keep the fixture readable in the repository.
- The summary records typed schema information so downstream checks do not need to parse Parquet directly.
