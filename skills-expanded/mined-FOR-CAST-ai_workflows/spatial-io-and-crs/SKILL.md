---
name: spatial-io-and-crs
description: How terra and sf objects must cross process and session boundaries -- SpatRaster/SpatVector are external pointers that do not survive serialisation, so write files and pass paths instead of reaching for wrap(). Also covers the one-project-CRS rule, stamping versus reprojecting, GDAL config for GeoPackages, GPKG over shapefile, and server-side filtering.
when_to_use: Passing spatial data to a parallel, future, mirai or callr worker; saving spatial data or returning it from a function another process consumes; seeing "NULL value passed as symbol address" or an empty/invalid spatial object; setting up a project CRS; a .prj with no authority code; fetching a layer from a web service.
paths:
  - "**/*.R"
---

# Spatial objects across boundaries

## The external-pointer trap

`terra` `SpatRaster` and `SpatVector` hold their data behind an **external
pointer**. It does not survive serialisation, and nothing warns you:

> `load_nbac_polys()` returns a terra SpatVector, whose data live behind an
> external pointer that does not survive serialisation. [It was stored] without
> complaint, so the failure surfaces only in the **consumer** ... errored with
> `NULL value passed as symbol address` ... four minutes into the run and before
> any container started.

Note where it fails: in the *consumer*, not the producer, and long after the fact.
The same applies to any `parallel`/`future`/`mirai`/`callr` worker, to a cache that
serialises its values, and to a saved `.rds`.

**A stale pointer also does not survive a session.** An object read back from a
file-backed store points at a file: re-read it, never reuse a pointer carried over
from a previous session.

## The fix: files are the currency

Do not reach for `terra::wrap()`/`unwrap()`. Design so it is never needed: what
crosses a process boundary is always a file path.

- **Rasters on disk, not in RAM.** Pass filenames across stage and worker
  boundaries. Never retain an in-memory `SpatRaster` across a boundary.
- A function that writes a layer **returns the path it wrote**:

```r
write_layer <- function(x, path) {
  terra::writeRaster(x, filename = path, overwrite = TRUE, datatype = "INT1U")
  path
}
```

## GDAL config for GeoPackages

GDAL's GPKG driver refuses a GeoPackage at a path without a `.gpkg` extension, which
some stores and caches use:

```r
Sys.setenv(OGR_SQLITE_ALLOW_ANY_EXTENSION = "YES")
```

Set it in `.Rprofile` **so every worker process inherits it**.

GDAL also stamps `gpkg_contents.last_change` on write, so a byte-identical re-write
produces a different file. Anything that hashes files -- a pipeline, a cache, a
checksum manifest -- then sees a change. Pin `OGR_CURRENT_DATE` when writing GPKGs
whose hash matters.

## One declared project CRS

Declare the target CRS and resolution **once**, in the project's config, and build
everything to match:

```r
local$crs <- "EPSG:3978"    ## NAD83 Canada Atlas Lambert
local$res <- 250L
```

The alternative -- every layer following whatever raster it meets -- produces the
footgun of needing a separately pre-transformed study area for one dataset:

```r
roads <- get_roads(studyArea_LCC, LCC)   ## NOTE: different studyArea CRS needed
```

A single declared project CRS removes that entirely.

Two CRS details that bite:

- **Server-side bbox filters usually want lon/lat.** Project for the query only:
  ```r
  bb <- terra::ext(terra::project(sa, "EPSG:4326"))
  ```
- **A `.prj` may name a projection with no authority code.** Stamping and
  reprojecting are different operations; choose deliberately, verify the parameters
  match, and fail loudly when neither is possible:
  ```r
  if (!is.na(row$crs_override)) {
    terra::crs(v) <- row$crs_override        ## stamp: params verified identical
  }
  if (is.na(terra::crs(v, describe = TRUE)$code) && is.na(row$crs_override)) {
    stop("no resolvable CRS and no override for ", row$layer_key, call. = FALSE)
  }
  ```

## GPKG, not shapefile

A standing rule in these projects. Shapefiles lose long field names, have a 2 GB
limit, and split across sidecar files -- and a fetch that drops the `.shx` fails
in a way that looks like a corrupt download. Single-file `.gpkg` avoids all of it.

Where a columnar format genuinely pays -- millions of features read repeatedly,
column-wise -- use **geoarrow** (0.4.4, released 2026-09-16), not `sfarrow`, whose
last CRAN release was 2021-10-27. And if you reach for a raster data cube:
**gdalcubes was archived from CRAN on 2026-09-16**, so build the time series from
terra instead of adding an archived dependency.

## Fetch and filter server-side

Push the filter to the server rather than downloading a province and cropping:

```r
polys <- bcdata::bcdc_query_geodata(id) |>
  dplyr::filter(INTERSECTS(studyArea)) |>
  dplyr::select(dplyr::any_of(select_cols)) |>
  dplyr::collect() |>
  sf::st_intersection(studyArea)
suppressWarnings({ sf::st_transform(polys, terra::crs(rasterToMatch)) })
```

Note the narrowed `suppressWarnings()` -- it wraps only the transform, so real
warnings elsewhere in the chain still surface. Never wrap a whole pipeline in it.

The same principle applies to any reprojection: **crop in the source CRS first,
then reproject.** A helper that reprojected a country-wide layer before cropping
took >50 minutes where crop-then-project took ~1.4 seconds.
