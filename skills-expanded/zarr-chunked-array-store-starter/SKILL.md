# Zarr Chunked Array Store Starter

Use this skill to convert a small numeric matrix into a chunked, compressed Zarr store and inspect a deterministic summary of its layout.

## What This Skill Does

- reads a toy tabular matrix
- writes a local Zarr v2 array with fixed chunking and Blosc compression
- reports shape, chunk layout, compressor choice, and summary statistics

## When To Use It

- when you need a starter for `chunking-sharding`
- when you want a repo-local example of Zarr plus `numcodecs`
- when you need a tiny test fixture for chunked scientific array storage

## Run

```bash
python3 skills/data-acquisition-and-dataset-handling/zarr-chunked-array-store-starter/scripts/run_zarr_chunked_array_store.py --input skills/data-acquisition-and-dataset-handling/zarr-chunked-array-store-starter/examples/toy_matrix.tsv --store-out scratch/zarr/toy_matrix.zarr --summary-out scratch/zarr/toy_matrix_summary.json
```

## Notes

- The starter writes Zarr format 2 explicitly so classic compressor settings remain deterministic.
- The example is intentionally tiny and local; scale chunking decisions against real workloads before production use.
