# PlantCV Plant Phenotyping Starter

Use this skill to generate a tiny synthetic plant image, segment it with `PlantCV`, and summarize simple morphology-style phenotyping measurements.

## What it does

- Builds a small deterministic RGB image containing one synthetic plant-like region.
- Uses `PlantCV` HSV conversion plus binary thresholding to produce a foreground mask.
- Reports foreground area, bounding box, and a simple saturation-based phenotype summary.

## When to use it

- You need a runnable starter for `Plant phenotyping`.
- You want a local segmentation and mask-summary example before scaling to real greenhouse or field images.

## Example

```bash
slurm/envs/plant-science/bin/python skills/agriculture-food-and-plant-science/plantcv-plant-phenotyping-starter/scripts/run_plantcv_plant_phenotyping.py \
  --image-out scratch/plantcv/toy_plant.png \
  --mask-out scratch/plantcv/toy_plant_mask.png \
  --out scratch/plantcv/toy_plant_summary.json
```

## Verification

- Skill-local tests: `python3 -m unittest discover -s skills/agriculture-food-and-plant-science/plantcv-plant-phenotyping-starter/tests -p 'test_*.py'`
- Repository smoke: `python3 -m unittest tests.smoke.test_phase30_empty_domain_seed_skills -v`
