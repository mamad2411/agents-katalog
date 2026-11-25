# Xarray Climate Cube Starter

Use this skill to build a deterministic toy climate cube with Xarray and summarize simple spatiotemporal statistics.

## What it does

- Creates a monthly temperature cube with `time`, `lat`, and `lon` dimensions.
- Computes annual mean temperature, seasonal range, per-latitude means, and the hottest month.
- Returns compact JSON that is easy to reuse in downstream scientific-Python workflows.

## When to use it

- You need a local, no-auth starter for climate or environmental data handling.
- You want a minimal example of labeled multidimensional array operations with Xarray.

## Example

```bash
slurm/envs/scientific-python/bin/python skills/earth-climate-and-geospatial-science/xarray-climate-cube-starter/scripts/run_xarray_climate_cube.py \
  --out scratch/xarray/climate_cube_summary.json
```

## Verification

- Skill-local tests: `python3 -m unittest discover -s skills/earth-climate-and-geospatial-science/xarray-climate-cube-starter/tests -p 'test_*.py'`
- Repository smoke: `python3 -m unittest tests.smoke.test_frontier_domain_skills -v`
