---
name: geodesy
description: "Reference ellipsoids, geoid modeling, GNSS positioning, coordinate reference systems (CRS), and crustal deformation"
category: earth-science
version: 1.0.0
disable-model-invocation: false
risk: low
source: "https://github.com/Mr-Nobody-Anonymous/All-skills"
source_repository: "Mr-Nobody-Anonymous/All-skills"
source_path: "awesome_skills/earth-science/geodesy/SKILL.md"
license: "MIT"
imported_at: "2026-09-20"
---

# Geodesy

## Scope
Geodesy measures and represents the geometric shape, orientation in space, and gravitational field of the Earth, providing foundational reference frames for navigation and geospatial mapping.

## Geodetic Formulations
- **Reference Surface Hierarchy**:
  - Topography: Physical surface.
  - Geoid: Equipotential surface of Earth's gravity field corresponding to mean sea level.
  - Ellipsoid: Mathematical reference (WGS84, GRS80) defined by semi-major axis $a$ and flattening $f = (a - b)/a$.
- **Orthometric Height ($H$) & Ellipsoidal Height ($h$)**:
  $$h = H + N \quad (N = \text{geoid undulation})$$

## Tools & Standards
- **Standards**: EPSG registry, ITRF (International Terrestrial Reference Frame), WGS84.
- **Software**: PROJ, GDAL, GAMIT/GLOBK, RTKLIB.
- **Canonical References**: Torge & Müller — *Geodesy* (4th ed.).
