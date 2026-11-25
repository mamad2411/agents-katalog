# Nilearn fMRI Denoising Starter

Use this skill to build a tiny toy fMRI-like timeseries matrix, regress out confounds with `nilearn.signal.clean`, and summarize the denoising effect.

## What it does

- Creates deterministic toy voxel signals with known nuisance-confound structure.
- Uses `nilearn.signal.clean` to detrend, regress confounds, and standardize the cleaned output.
- Returns pre/post confound-correlation summaries and cleaned-signal statistics in JSON.

## When to use it

- You need a runnable starter for `fMRI preprocessing and denoising`.
- You want a verified local denoising example without requiring a full BIDS or fMRIPrep runtime.

## Example

```bash
slurm/envs/neuro/bin/python skills/neuroscience-and-neuroimaging/nilearn-fmri-denoising-starter/scripts/run_nilearn_fmri_denoising.py \
  --out scratch/neuro/nilearn_denoising_summary.json
```

## Verification

- Skill-local tests: `python3 -m unittest discover -s skills/neuroscience-and-neuroimaging/nilearn-fmri-denoising-starter/tests -p 'test_*.py'`
- Repository smoke: `python3 -m unittest tests.smoke.test_phase31_frontier_leaf_conversion_skills -v`
