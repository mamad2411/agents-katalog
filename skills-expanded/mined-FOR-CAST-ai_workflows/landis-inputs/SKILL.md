---
name: landis-inputs
description: Validate LANDIS-II inputs before running, and the file-format conventions it silently depends on -- NoData and map-code encoding, permitted pixel types, dyadic season proportions, ecoregion/map-code consistency, and the literal filenames the runner patches. LANDIS fails on bad input with a non-zero exit and empty stderr, so preflight validation is the only cheap defence.
when_to_use: Generating or editing LANDIS-II input rasters or text files; a LANDIS run dies seconds into extension initialisation; "Unknown map code"; a scenario or extension file is being written from R; before launching a batch or calibration; wiring LANDIS runs into a targets pipeline.
paths:
  - "**/*.R"
---

# LANDIS-II inputs: validate before you run

## Why preflight, not debugging

> LANDIS-II fails on bad inputs in the worst possible way: the run dies a few
> seconds into extension initialisation, the R-side runner reports only a non-zero
> exit with **empty stderr**, and the real message is buried in `Landis-log.txt`
> inside a scratch directory. Under a calibration warm pool that failure is
> multiplied by the pool size (56-90 containers) and can burn hours before anyone
> reads a log. Three separate instances hit this project in one week.

So: validate the scenario directory **before** any container starts, and surface
`Landis-log.txt` on failure rather than the exit code.

## The validation checklist

Run these against every scenario directory before launching:

1. **No NA cells inside the active mask, no negative values.** LANDIS reads raw
   cell values and **ignores the GDAL NoData flag**. `0` means *inactive*; an NA
   written as signed-integer NoData is `-32768`, which becomes a huge number when
   converted to unsigned and produces `System.Convert.ToUInt32(Int16 value)`.
2. **Pixel type is one of byte / short / int / float / double.** `INT4U` is
   rejected. Choose the type from the **maximum map code**, not from the raster's
   current storage type.
3. **Every map code in a raster exists in the corresponding table**, and vice
   versa. `Unknown map code` has two distinct causes seen here: a row-order flip
   between the raster and the table (which mismatched 182,556 cells), and
   **uncollapsed duplicate map codes** (397,100 codes for 9,919 communities), which
   OOM-killed every node in the pool -- twice.
4. **The fire-ecoregion mask equals the core active mask.** A cell active in one
   and not the other is an "unknown map code" waiting to happen.
5. **Season proportions are dyadic (`k/128`).** The C# parser checks the sum in
   *single-precision* float, so `0.1 + 0.2 + 0.7` does not reliably sum to 1.
6. **The weather/climate table contains no `NA`.** The Dynamic Fire weather CSV in
   particular rejects them.
7. **The master file is literally named `scenario.txt`.** Runners patch that exact
   filename to inject a per-replicate random seed.
8. **The version matches.** v7 and v8 input formats differ; check the console's
   reported version on first use and refuse to proceed against the wrong major.

## `character(0)` is the sharpest single trap

```r
ext <- names(cfg$extensions)[cfg$use_fire]   ## may be character(0)
ext[1]                                       ## NA_character_, NOT an error
```

`character(0)[1]` is `NA_character_`, so an unset extension wrote the literal
string `NA` into `scenario.txt` and **failed all 165 production replicates**.

Guard every value that reaches a generated text file:

```r
stopifnot(length(ext) == 1L, !is.na(ext), nzchar(ext))
checkmate::assert_string(ext, min.chars = 1)   ## the same three checks, and it
                                               ## names the offending value
```

More generally: **a directive that matches nothing must not pass silently.**

## Writing input rasters

```r
terra::writeRaster(r, filename = out, overwrite = TRUE,
                   datatype = landis_datatype(max_map_code), NAflag = 0)
```

- Use factor levels (`terra::levels()`) deliberately -- know whether the consumer
  wants the code or the label.
- Keep FBP fuel-type indices aligned with the table that defines them.
- Gate extensions consistently: if two features are mutually dependent, require
  both flags rather than inferring one from the other.

## Running in a container on shared storage

- **A container daemon usually cannot bind-mount root-squashed NFS.** Exit code
  **126** means exactly that. Stage the run on local scratch and rsync results back
  to shared storage afterwards.
- Exit **137** is OOM; exit **139** is a transient SIGSEGV worth one retry.
- **Pin the image by digest**, not by tag.
- **Stagger container starts.** At high concurrency every replicate fires
  `docker run` simultaneously and the daemon stops answering (it will not even
  return `docker stats`). A startup jitter of ~30 s, read at *run* time so tuning it
  does not invalidate cached work, fixes this.
- **Set an explicit retry count.** The default is 0, and a single failed container
  exec discards every generation since the last checkpoint. For a search of
  `itermax * NP * n_reps` executions -- tens of thousands -- a rare transient is
  near-certain.
- **Checkpoint every generation, not every N.** Two separate incidents in one week
  lost a day's compute to a restart before the first checkpoint landed.
- **Do not pre-emptively delete an existing output directory** to work around
  "refuses to overwrite". That was tried and reverted: deleting real results is
  worse than the error. Write logs to a temp file and copy them into place
  `on.exit()`, since the output dir cannot pre-exist.

## Running LANDIS from a targets pipeline

- **A cached input can outlive the change that should have replaced it.** A cached
  initial-communities snapshot survived a species-set change, because the target that
  built it returned a stable path; every container then died with `Ep is not a species
  name` after ~108 s. Fingerprint the inputs a scenario directory is built from (the
  `*_manifest` pattern in `targets-staleness`), so a species-set change rebuilds it.
- **Pin the run fleet** so no `tar_make()` can launch production by accident:
  `landis.run_scenarios = c("ForCS_only", "ForCS_fire")`, with the reason in a comment.
  Treat such a pin as deliberate; do not remove it without asking.
- Register the package's LANDIS target factory with tarborist
  (`"tarborist.additionalSingleTargetFactories": ["<pkg>::tar_landis"]` in
  `.vscode/settings.json`) so the IDE can see its targets.
