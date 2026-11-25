---
name: remote-sensing
description: "Satellite and aerial multispectral, hyperspectral, and SAR imaging, radiometric calibration, and spectral indices (NDVI)"
category: earth-science
version: 1.0.0
disable-model-invocation: false
risk: low
source: "https://github.com/Mr-Nobody-Anonymous/All-skills"
source_repository: "Mr-Nobody-Anonymous/All-skills"
source_path: "awesome_skills/earth-science/remote-sensing/SKILL.md"
license: "MIT"
imported_at: "2026-09-20"
---

# Remote Sensing

## Scope
Remote sensing acquires information about the Earth's surface and atmosphere without physical contact, using reflected or emitted electromagnetic radiation detected by satellite or airborne sensors.

## Core Formulations & Processing
- **Planck's Law & Wien's Displacement Law**: $\lambda_{\max} = 2898 / T\text{ (}\mu\text{m}\cdot\text{K)}$.
- **Spectral Indices**:
  - $\text{NDVI} = (\text{NIR} - \text{Red}) / (\text{NIR} + \text{Red})$
  - $\text{NDWI} = (\text{Green} - \text{NIR}) / (\text{Green} + \text{NIR})$
  - $\text{NDBI} = (\text{SWIR} - \text{NIR}) / (\text{SWIR} + \text{NIR})$
- **Synthetic Aperture Radar (SAR)**: Phase and amplitude processing, backscatter coefficient ($\sigma^0$), InSAR interferometry for millimetric crustal deformation.

## Tools & Standards
- **Platforms**: Sentinel (Copernicus), Landsat, PlanetScope, MODIS.
- **Software**: Google Earth Engine, SNAP (ESA), Rasterio, GDAL, QGIS.
- **Canonical References**: Lillesand, Kiefer & Chipman — *Remote Sensing and Image Interpretation*.
