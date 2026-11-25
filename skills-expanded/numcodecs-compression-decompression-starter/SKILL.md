# numcodecs Compression / Decompression Starter

Use this skill to round-trip a small integer matrix through a deterministic `numcodecs` compressor and inspect the encoded payload summary.

## What This Skill Does

- reads a tiny tabular integer matrix
- encodes the matrix bytes with `numcodecs.Blosc`
- decodes the payload and verifies lossless recovery
- reports shape, dtype, encoded byte count, and simple row statistics

## When To Use It

- when you need a starter for `compression-decompression`
- when you want a repo-local `numcodecs` example outside the full Zarr stack
- when you need a small regression fixture for round-trip codec checks

## Run

```bash
./slurm/envs/data-tools/bin/python skills/data-acquisition-and-dataset-handling/numcodecs-compression-decompression-starter/scripts/run_numcodecs_compression_decompression.py --input skills/data-acquisition-and-dataset-handling/numcodecs-compression-decompression-starter/examples/toy_matrix.tsv --out scratch/numcodecs/toy_matrix_summary.json
```

## Notes

- The codec configuration is fixed so the canonical asset stays stable.
- The example is intentionally tiny and integer-only; validate codec choices on real payloads before production use.
