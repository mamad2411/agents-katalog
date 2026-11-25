# Scanpy DPT Trajectory Starter

Use this skill to compute a deterministic toy diffusion-pseudotime trajectory with Scanpy `tl.dpt`.

## What it does

- Loads a tiny genes-by-cells matrix and a root cell.
- Builds a Scanpy neighbors graph, computes diffusion components, and runs `tl.dpt`.
- Exports per-cell pseudotime values and the inferred cell order.

## When to use it

- You need a verified starter for the `trajectory inference` leaf in transcriptomics.
- You want a bounded example of DPT before moving to larger pseudotime workflows.
- You need deterministic JSON output that can be checked in repository tests.

## Example

```bash
slurm/envs/scanpy/bin/python skills/transcriptomics/scanpy-dpt-trajectory-starter/scripts/run_scanpy_dpt_trajectory.py \
  --counts skills/transcriptomics/scanpy-dpt-trajectory-starter/examples/toy_counts.tsv \
  --root-cell c0 \
  --expected-order skills/transcriptomics/scanpy-dpt-trajectory-starter/examples/expected_order.txt \
  --summary-out scratch/scanpy-dpt/summary.json
```

## Verification

- Skill-local tests: `python3 -m unittest discover -s skills/transcriptomics/scanpy-dpt-trajectory-starter/tests -p 'test_*.py'`
- Expected summary: the inferred order equals `c0..c5` and pseudotime increases monotonically from `0.0` to `1.0`
