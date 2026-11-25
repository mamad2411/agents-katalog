# MACS3 Peak Calling Starter

Use this skill to run a deterministic toy peak-calling example with `MACS3 callpeak`.

## What it does

- Runs `macs3 callpeak` on a small BED file using `--nomodel --extsize 75` so toy data can be verified reliably.
- Writes the standard `narrowPeak`, `summits.bed`, and `peaks.xls` outputs to a work directory.
- Summarizes the strongest peak into a compact JSON payload for tests and demos.

## When to use it

- You need a runnable starter for simple ChIP-seq or chromatin-style peak calling.
- You want a deterministic local example before moving to real replicate-aware workflows.
- You need a smoke-testable wrapper around MACS3.

## Example

```bash
slurm/envs/genomics/bin/python skills/epigenomics-and-chromatin/macs3-peak-calling-starter/scripts/run_macs3_peak_calling.py \
  --treatment skills/epigenomics-and-chromatin/macs3-peak-calling-starter/examples/toy_treatment.bed \
  --summary-out scratch/epigenomics/macs3_peak_summary.json
```

## Verification

- Skill-local tests: `python3 -m unittest discover -s skills/epigenomics-and-chromatin/macs3-peak-calling-starter/tests -p 'test_*.py'`
- Expected summary: `peak_count == 1` and `top_peak["name"] == "toy_peak_1"`
