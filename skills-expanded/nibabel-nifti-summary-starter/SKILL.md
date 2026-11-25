# NiBabel NIfTI Summary Starter

Use this skill to generate or load a small NIfTI image with `nibabel` and summarize the core shape, affine, zoom, and unit metadata.

## What it does

- Builds a deterministic toy 4D neuroimaging volume when no input file is supplied.
- Saves the image to disk when requested and reloads it through `nibabel`.
- Reports shape, voxel sizes, affine determinant, basic intensity statistics, and header units.

## When to use it

- You need a runnable starter for `Neuroimaging I/O and formats`.
- You want a verified example of NIfTI creation and inspection before moving to larger neuroimaging pipelines.

## Example

```bash
slurm/envs/neuro/bin/python skills/neuroscience-and-neuroimaging/nibabel-nifti-summary-starter/scripts/run_nibabel_nifti_summary.py \
  --nifti-out scratch/neuro/toy_bold.nii.gz \
  --out scratch/neuro/toy_bold_summary.json
```

## Verification

- Skill-local tests: `python3 -m unittest discover -s skills/neuroscience-and-neuroimaging/nibabel-nifti-summary-starter/tests -p 'test_*.py'`
- Repository smoke: `python3 -m unittest tests.smoke.test_phase30_empty_domain_seed_skills -v`
