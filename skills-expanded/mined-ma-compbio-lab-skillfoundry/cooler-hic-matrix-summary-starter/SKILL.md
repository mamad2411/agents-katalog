# cooler Hi-C Matrix Summary Starter

Use this skill to generate or inspect a tiny Hi-C contact matrix in Cooler format and summarize its bins and pixel counts in JSON.

## What it does

- Creates a deterministic toy `.cool` file with three bins and five nonzero upper-triangle pixels.
- Opens the Cooler store with `cooler.Cooler` and summarizes matrix shape, pixel count, and total contact count.
- Can also summarize an existing Cooler file if `--input` is provided.

## When to use it

- You need a runnable starter for Hi-C contact matrix formats.
- You want a small verified example before building larger chromatin-interaction workflows.
- You need a smoke-testable wrapper around `cooler` in the repo-managed scientific Python environment.

## Example

```bash
slurm/envs/scientific-python/bin/python skills/epigenomics-and-chromatin/cooler-hic-matrix-summary-starter/scripts/run_cooler_hic_matrix_summary.py \
  --out scratch/epigenomics/cooler_hic_summary.json \
  --cooler-out scratch/epigenomics/toy_contacts.cool
```

## Verification

- Skill-local tests: `python3 -m unittest discover -s skills/epigenomics-and-chromatin/cooler-hic-matrix-summary-starter/tests -p 'test_*.py'`
- Expected summary: `bin_count == 3`, `pixel_count == 5`, and `total_contact_count == 38`
