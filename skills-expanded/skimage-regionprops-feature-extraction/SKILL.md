# scikit-image Regionprops Feature Extraction

Use this skill to extract deterministic morphology and intensity features from a toy image with `scikit-image` `regionprops_table`.

## What it does

- creates a reproducible grayscale toy image with three bright ellipse-like objects
- thresholds and labels connected components locally
- summarizes per-object morphology and intensity features into compact JSON
- keeps the output stable enough for smoke tests and starter workflows

## When to use it

- You need a local `feature-extraction` starter in the scikit-image ecosystem.
- You want a minimal handoff point before building larger imaging or phenotype-analysis pipelines.

## Example

```bash
./slurm/envs/scientific-python/bin/python \
  skills/imaging-and-phenotype-analysis/skimage-regionprops-feature-extraction/scripts/run_skimage_regionprops_features.py \
  --threshold 0.35 \
  --out scratch/skimage-regionprops/summary.json
```

## Verification

- Skill-local tests: `python3 -m unittest discover -s skills/imaging-and-phenotype-analysis/skimage-regionprops-feature-extraction/tests -p 'test_*.py'`
- Asset regeneration: `./slurm/envs/scientific-python/bin/python skills/imaging-and-phenotype-analysis/skimage-regionprops-feature-extraction/scripts/run_skimage_regionprops_features.py --out skills/imaging-and-phenotype-analysis/skimage-regionprops-feature-extraction/assets/toy_regionprops_summary.json`

## Notes

- This is a starter for the taxonomy leaf `feature-extraction`.
- The image is synthetic and deterministic; it is intended for scaffolding and verification rather than biological interpretation.
