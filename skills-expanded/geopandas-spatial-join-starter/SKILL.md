# GeoPandas Spatial Join Starter

Use this skill to run a deterministic point-in-polygon join with GeoPandas and summarize the result in compact JSON.

## What it does

- Builds a toy vector dataset with two regions and four observation points.
- Performs a spatial join to assign points to regions.
- Reprojects the joined data to `EPSG:3857` and records projected bounds.
- Emits a reusable JSON summary for downstream geospatial workflows.

## When to use it

- You need a local, no-auth starter for vector geospatial analysis.
- You want a minimal example of `GeoDataFrame`, `sjoin`, and `to_crs`.
- You want a repo-aware wrapper that fixes the `PROJ` data-path issue automatically.

## Example

```bash
slurm/envs/geospatial/bin/python skills/earth-climate-and-geospatial-science/geopandas-spatial-join-starter/scripts/run_geopandas_spatial_join.py \
  --out scratch/geopandas/spatial_join_summary.json
```

## Verification

- Skill-local tests: `python3 -m unittest discover -s skills/earth-climate-and-geospatial-science/geopandas-spatial-join-starter/tests -p 'test_*.py'`
- Repository smoke: `python3 -m unittest tests.smoke.test_frontier_domain_skills -v`
