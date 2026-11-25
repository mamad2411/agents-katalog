---
name: targets-spatial
description: Spatial data in a {targets} pipeline -- a plain tar_target() stores a dead terra pointer without complaint, so use geotargets tar_terra_* or format = "file" targets that return paths; registering geotargets factories with tarborist; the GPKG settings geotargets stores need; manifest targets for directories of outputs; and worker memory settings for large rasters.
when_to_use: Writing a target that returns a SpatRaster, SpatVector or sf object; "NULL value passed as symbol address" raised in a downstream target; a geotargets target fails to read back; dynamic branching over an sf object fails; sizing crew workers for raster targets.
paths:
  - "**/_targets.R"
  - "**/_targets*.R"
  - "**/R/targets_*.R"
---

# Spatial objects in a targets pipeline

Why terra objects cannot be stored as values, and the general rules for spatial I/O
and CRS, are in `spatial-io-and-crs` in `r-geospatial`. This skill is the `targets`
side.

## A plain `tar_target()` stores a dead pointer

`targets` serialises every value it stores. A `SpatRaster` or `SpatVector` returned
by a plain `tar_target()` is stored without complaint, and the **consumer** fails
later with `NULL value passed as symbol address`.

```r
geotargets::tar_terra_rast(dem, make_dem(...))      # SpatRaster -> .tif
geotargets::tar_terra_vect(aoi, make_aoi(...))      # SpatVector -> .gpkg
tar_target(big_layer, write_layer(...), format = "file")   # returns a PATH
```

- **Heavy or spatial output is never a plain `tar_target()`.** Use
  `tar_terra_rast` / `tar_terra_vect` / `format = "file"`.
- A function backing a `format = "file"` target **returns the path it wrote**.
- A `tar_read()` of a file-backed geotarget returns an object pointing at a file in
  the store. Re-read it in each session.

Register the factories with the tarborist extension so it can still discover the
targets, in `.vscode/settings.json`:

```json
{ "tarborist.additionalSingleTargetFactories":
  ["tar_terra_rast", "tar_terra_vect", "tar_terra_sprc", "tar_terra_tiles"] }
```

## GPKG settings for geotargets stores

`geotargets` stores `SpatVector` targets at extensionless object paths, which GDAL's
GPKG driver refuses by default. Set `OGR_SQLITE_ALLOW_ANY_EXTENSION=YES` in
`.Rprofile` **so crew workers inherit it**, and repeat it in `_targets.R` for
interactive use -- one of the few duplications worth making, with the reason written
down at both sites.

Pin `OGR_CURRENT_DATE` when writing GPKGs from a pipeline: GDAL's write timestamp
otherwise makes an identical re-write hash differently under `format = "file"`, and
every downstream target rebuilds.

## A stable path is not a stable value

A `format = "file"` target whose *path* never changes will not invalidate its
consumers when the contents behind it change. If a target returns a directory root
or a `list.files()` scan, add a `*_manifest` companion carrying path/size/mtime
fingerprints and have consumers depend on that. See `targets-staleness`.

## Large rasters under crew

```r
tar_option_set(memory = "transient", storage = "worker", retrieval = "worker")
```

and call `gc()` explicitly inside long loops.

`terra` memory fractions apply per worker. Cap the fraction for the worker count, and
scope the cap to the stage that needs it: applying it globally puts a runtime knob
into an expensive stage's command hash, and retuning it rebuilds that stage.

## Chunking what cannot be branched over

Dynamic branching over an `sf` object fails, even though `sf` inherits from
`data.frame`. Chunk manually and recombine, and put the chunk-maker on
`deployment = "main"` so worker dispatch stays sane.

For out-of-core aggregation, name each branch's chunk after the branch so reruns
overwrite rather than duplicate:

```r
arrow::write_parquet(data.frame(distance = dists),
  sink = file.path(ds_dir, paste0("chunk_", targets::tar_name(), ".parquet")))
```
