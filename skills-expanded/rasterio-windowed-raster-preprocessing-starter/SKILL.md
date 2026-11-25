# Rasterio Windowed Raster Preprocessing Starter

Use this skill to generate a tiny toy raster with Rasterio, extract a window, downsample it, and summarize the preprocessing result in compact JSON.

## What it does

- Creates a deterministic single-band GeoTIFF with a simple `EPSG:4326` transform.
- Reads a 2x2 window from the raster.
- Produces a 2x2 average-resampled version of the whole raster.
- Emits a compact JSON summary with bounds, means, and extracted values.

## When to use it

- You need a local starter for raster preprocessing or remote-sensing data handling.
- You want a minimal example of `rasterio.open`, `Window`, and average resampling.
- You want a deterministic JSON artifact before moving on to larger raster pipelines.

## Example

```bash
slurm/envs/geospatial/bin/python skills/earth-climate-and-geospatial-science/rasterio-windowed-raster-preprocessing-starter/scripts/run_rasterio_windowed_preprocessing.py \
  --out scratch/geospatial/rasterio_preprocessing_summary.json
```

## Verification

- Skill-local tests: `python3 -m unittest discover -s skills/earth-climate-and-geospatial-science/rasterio-windowed-raster-preprocessing-starter/tests -p 'test_*.py'`
- Expected summary: `window_values == [[6.0, 7.0], [10.0, 11.0]]`
