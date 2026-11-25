---
name: spatial-statistics
description: "Analyse spatial patterns statistically: spatial autocorrelation (Moran's I), hotspot detection, clustering, interpolation/kriging and the ecology of modifiable areal units."
type: procedural
category: geospatial
domain: geospatial
version: 1.0.0
author: Mr-Nobody-Anonymous
license: MIT
risk: low
level: advanced
triggers:
  - morans i spatial autocorrelation
  - hotspot analysis gis
  - kriging interpolation
  - spatial clustering analysis
  - geographically weighted regression
keywords:
  - spatial-statistics
  - moran
  - hotspot
  - kriging
  - autocorrelation
  - gwr
  - maup
source: custom
enabled: true
---

# Spatial Statistics

## Purpose

Analyse spatial patterns statistically: spatial autocorrelation (Moran's I), hotspot detection, clustering, interpolation/kriging and the ecology of modifiable areal units.

## When to Use

- A pattern on a map needs a significance test rather than an impression.
- You must interpolate values between sample points.
- Point clusters could be chance; you need to test them.

## When NOT to Use

- The question is descriptive mapping only.
- Sample size is too small for the test to have power — say so.
- The spatial weights or unit boundaries would drive the result (MAUP) and cannot be justified.

## Capabilities

- Choose and justify a spatial weights matrix (contiguity, distance band, k-nearest).
- Run and interpret global and local autocorrelation statistics.
- Detect hotspots with false-discovery control.
- Interpolate with kriging and validate by cross-validation.

## Inputs

- The geometry (polygons or points), the variable and its scale.
- The processes that plausibly generate spatial dependence.
- The decision the analysis informs and the acceptable false-positive rate.

## Workflow

1. Map the raw variable first and inspect the distribution before any statistic.
2. Define the weights matrix and state why it matches the process.
3. Run global Moran's I; only if significant, look for local clusters.
4. Correct for multiple comparisons across local statistics.
5. Validate interpolation by leave-one-out cross-validation and report error.

## Tools

- GeoDa / PySAL (esda, libpysal)
- R `sf` + `spdep`
- QGIS with the processing toolbox

## Examples

- `python -c "import libpysal, esda; w=libpysal.weights.Queen.from_dataframe(gdf); print(esda.Moran(gdf['rate'], w).I)"`
- `Rscript -e 'library(spdep); moran.test(gdf$rate, nb2listw(poly2nb(gdf)))'`
- `allskills route "test whether these clusters are significant"`

## Safety

- Results depend heavily on the weights matrix — report it and test sensitivity.
- Aggregating to arbitrary boundaries can manufacture or hide patterns (MAUP).
- Correlation across space is not causation; avoid causal language.

## Source

All-Skills canonical library (`skills/geospatial/spatial-statistics`). First-party skill, maintained in this repository.

## Notes

- Local indicators of association need a multiple-testing correction.
- Kriging variance is a model output, not a guarantee of true error.
- Pairs with: `scientific/statistics`, `geospatial/postgis-spatial-sql`.
