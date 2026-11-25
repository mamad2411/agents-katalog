# Astropy FITS Image Summary Starter

Use this skill to generate or load a tiny FITS image with `astropy.io.fits` and summarize the core image and header metadata.

## What it does

- Builds a deterministic toy 2D FITS image when no input file is supplied.
- Writes the FITS file to disk when requested and reloads it through Astropy.
- Reports image shape, mean, standard deviation, and a few astronomy-style header fields.

## When to use it

- You need a runnable starter for `Telescope image preprocessing`.
- You want a verified FITS I/O example before scaling to real sky-survey or instrument data.

## Example

```bash
slurm/envs/astronomy/bin/python skills/physics-and-astronomy/astropy-fits-image-summary-starter/scripts/run_astropy_fits_image_summary.py \
  --fits-out scratch/astronomy/toy_image.fits \
  --out scratch/astronomy/toy_image_summary.json
```

## Verification

- Skill-local tests: `python3 -m unittest discover -s skills/physics-and-astronomy/astropy-fits-image-summary-starter/tests -p 'test_*.py'`
- Repository smoke: `python3 -m unittest tests.smoke.test_phase30_empty_domain_seed_skills -v`
