---
name: raster-scale-and-memory
description: Working with rasters too large for RAM -- writing straight to disk, terra memory fractions under parallel workers, tiling with overlap, out-of-core aggregation via arrow and duckdb, datatype selection, and the dimension and NoData guards that stop silent misalignment.
when_to_use: A raster operation runs out of memory or takes far too long; sizing parallel workers for raster work; tiling a large raster; computing statistics over data that does not fit in RAM; choosing a raster datatype or NoData convention; two rasters that should align but do not.
paths:
  - "**/*.R"
---

# Large rasters

## Write to disk, always

Every `terra` operation that can take a `filename=` should get one, plus
`overwrite = TRUE`, and the function returns the path:

```r
terra::rasterize(v, template, field = "class",
                 filename = out, overwrite = TRUE, datatype = "INT1U")
out
```

`datatype` matters: `INT1U` kept a 30 m national land-cover layer small enough to
be practical. Match the type to the value range, and remember that some downstream
consumers reject certain types outright (`INT4U` in particular).

Prefer `terra::lapp()` over stacking layers in memory for multi-layer algebra.

## Memory settings, and why they are per-worker

```r
Sys.setenv(OMP_NUM_THREADS = 1)     ## BEFORE loading packages
terra::terraOptions(memfrac = 0.0)  ## do raster operations on disk
```

`memfrac` is **per process**. Under N parallel workers, N x memfrac of RAM can be
claimed collectively, which is how an 8-worker run OOM-crashed in a fire-spread
model that ran fine serially. Either cap terra memory at
`memfrac * node_RAM / n_workers`, or reduce workers.

Scope the cap to the stage that needs it. If the value feeds anything that is hashed
or cached, retuning it invalidates that work -- a runtime resource knob should not be
part of a cache key.

Call `gc()` explicitly inside long loops.

`OMP_NUM_THREADS` is not the only per-process pool. **data.table takes 50% of the
logical CPUs, per process.** It drops to a single thread only inside a *fork*, and
crew and mirai workers are not forks -- so N workers each claim half the node and
oversubscribe it. Cap it where you cap the others:

```r
data.table::setDTthreads(1)         ## documented API; per process
```

`R_DATATABLE_NUM_PROCS_PERCENT` (a percentage) is the documented environment
variable; `R_DATATABLE_NUM_THREADS` is read too but is not in the package's docs.

## Tiling with overlap

For neighbourhood operations, tiles must overlap by at least twice the
neighbourhood radius, and recombine by maximum:

```r
use_buffer <- ceiling(2 * radius / pixel_size)
tile_r <- ceiling(terra::nrow(r) / ntiles[1])
tile_c <- ceiling(terra::ncol(r) / ntiles[2])
stopifnot(tile_r > use_buffer, tile_c > use_buffer)

terra::makeTiles(r, y = c(tile_r, tile_c), filename = ..., buffer = use_buffer)
## ... process each tile ...
do.call(terra::mosaic, append(tiles, list(fun = "max", filename = out, overwrite = TRUE)))
```

The `stopifnot` is not decoration: a tile smaller than its own buffer produces
silently wrong edges.

## Out-of-core aggregation

When the intermediate does not fit in RAM (distance matrices, per-cell tables),
write chunks to a parquet dataset and aggregate through duckdb:

```r
arrow::write_parquet(data.frame(distance = dists),
  sink = file.path(ds_dir, paste0("chunk_", chunk_id, ".parquet")))

ds |> arrow::to_duckdb() |>
  dplyr::summarise(q25 = quantile(distance, 0.25), q75 = quantile(distance, 0.75))
```

Record the measured cost next to the code -- one such note reads *"adding more
quantile calculations ramps up memory use; computing q00, q25, q50, q75 and q100
uses ~250 GB RAM"*. That comment is worth more than the code.

## Guards that catch silent misalignment

**Dimension guard.** Two rasters that differ by one row or column will happily
align at the top-left and be wrong everywhere else:

```r
stopifnot(identical(dim(a)[1:2], dim(b)[1:2]))
```

One bug came from reading a *cropped* template (2139x3366) where the module's grid
was 2140x3367. Assert, do not assume; and be explicit about which template is
authoritative.

**NoData conventions are consumer-specific.** Some downstream tools read raw cell
values and ignore the GDAL NoData flag entirely, so a `0` meaning "inactive" and an
`NA` are completely different things to them. Signed-integer NA is `-32768`, which
such a tool will happily convert to a huge unsigned number. Before writing a raster
for an external engine, check its NoData convention and encode it explicitly:

```r
r[is.na(r)] <- 0L          ## if 0 means inactive to the consumer
```

**Sanitise value ranges the consumer cannot represent.** A handful of stray cells
is enough to break a run:

```r
## a small number of pixels come through as 0, which the solver cannot use
resistance[resistance == 0] <- 1
resistance[is.na(resistance)] <- 1000
```

**Directional stacking rules.** When combining layers, be explicit about which
direction each may push a value -- e.g. roads may only *raise* resistance
(`pmax`) and only *lower* source weight (`pmin`). Write the rule as a comment; it
is not recoverable from the code.

## Test on the quantity that can actually differ

The highest-consequence spatial bug in this corpus made two outputs **numerically
identical** for eight months, and nobody noticed because the aggregate looked
plausible. It was found and fixed with a **synthetic concentric test case with
exactly computable areas**:

```r
## old-only interior  = (1200 - 2*25)^2  = 132.25 ha
## mature+old interior = (1600 - 2*52)^2 = 223.80 ha
## previously BOTH returned 132.25 ha
```

Two rules follow, and they generalise:

- **Compare per-cell or on medians, never on landscape aggregates.** A 5-year
  offset hid inside a +/-5-year agreement check that reported 100% agreement; it was
  visible only in the medians.
- **If two outputs could be identical, assert that they are not.** Add
  `match.arg()` on the parameter that distinguishes them, and a test that pins the
  expected difference.
