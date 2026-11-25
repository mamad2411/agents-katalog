---
name: landis-outputs
description: Reading LANDIS-II output maps correctly -- the missing geotransform that makes terra::rast() silently mirror every map vertically, severity and status code encodings, and how to verify an output before it feeds a calibration.
when_to_use: Reading any LANDIS-II output raster; summarising burn severity or stand age; a map looks plausible but summaries by polygon are wrong; validating a LANDIS run's outputs.
paths:
  - "**/*.R"
---

# Reading LANDIS-II outputs

## The y-flip: the most expensive single bug in this corpus

LANDIS-II writes output maps with **no geotransform**. GDAL therefore reports the
identity transform, which has a *positive* pixel height -- i.e. south-up. On read,
`terra::rast()` reverses the rows.

> Every vegType, standAge and severity map the readers produced was therefore a
> vertical mirror ... Landscape totals survived that; core-vs-buffer attribution,
> reporting-polygon summaries and every map figure did not.

It **invalidated a 25-generation calibration** and produced **no error at all**.
Landscape-wide totals were unchanged, which is precisely why it survived so long.

The rule is now hard-coded in two file headers:

> Every LANDIS-II output map is opened with a dedicated reader, **never** with
> `terra::rast()`.

Write (or use) one reader that stamps the correct geotransform from the
corresponding input raster, and route every read through it. Never call
`terra::rast()` on a LANDIS output, not even "just to check something".

**How to verify you have it right:** compare a summary that is orientation-*sensitive*
against an independent source -- a per-polygon area, or a north-vs-south split.
A landscape total will agree either way and tells you nothing.

## Code encodings

- **Severity:** `0` = inactive, `1` = active but unburned, `>= 2` = burned.
  Count burned cells with `severity > 1`, **never** `> 0`. The off-by-one silently
  counts every active cell as burned.
- **Map codes generally:** `0` is inactive, not NoData. Do not convert it to `NA`
  before summarising unless you mean to drop inactive cells.

Write these encodings down next to the summarising code. They are not recoverable
by inspection -- a `> 0` threshold produces a plausible number.

## Verify before feeding a calibration

An output that is wrong in a way that preserves aggregates will pass every
sanity check you are likely to write. Before a set of outputs becomes the target of
an expensive fit:

1. Compare against an **independent** reference dataset, not another product of the
   same pipeline.
2. Compare **per-cell, or on medians** -- never on landscape means. A 5-year offset
   hid inside a +/-5-year agreement check that reported 100%.
3. Hold package and image versions fixed across the comparison. One earlier
   comparison was confounded by a library sync that landed between the two runs;
   **do not change packages mid-test.**
4. Check orientation explicitly, per the y-flip above.

## Reading run failures

The R-side exit code carries almost no information. On failure, read
`Landis-log.txt` inside the run's scratch directory and surface its tail. Container
exit codes: **126** = cannot bind-mount (root-squashed NFS), **137** = OOM,
**139** = transient SIGSEGV.

A run that reports 100% CPU after apparently completing is a known
output-flush bug, not progress.
