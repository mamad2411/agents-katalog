# scikit-image Otsu Segmentation Starter

Use this skill to generate a deterministic toy microscopy-like image, segment bright objects with Otsu thresholding, and summarize labeled regions.

## What it does

- Creates a synthetic grayscale image with three bright disk-shaped objects.
- Smooths the image, applies Otsu thresholding, removes tiny objects, and labels connected components.
- Returns compact JSON with threshold, object count, and per-object measurements.

## When to use it

- You need a local imaging starter in an officially documented ecosystem.
- You want a minimal segmentation baseline before moving to heavier microscopy pipelines.

## Example

```bash
slurm/envs/scientific-python/bin/python skills/imaging-and-phenotype-analysis/skimage-otsu-segmentation-starter/scripts/run_skimage_otsu_segmentation.py \
  --out scratch/skimage/segmentation_summary.json
```

## Verification

- Skill-local tests: `python3 -m unittest discover -s skills/imaging-and-phenotype-analysis/skimage-otsu-segmentation-starter/tests -p 'test_*.py'`
- Repository smoke: `python3 -m unittest tests.smoke.test_frontier_domain_skills -v`
