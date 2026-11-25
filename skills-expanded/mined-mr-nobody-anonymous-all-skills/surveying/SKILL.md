---
name: surveying
description: "Total station measurement, leveling, traverse computations, coordinate transformations, and land boundary legal frameworks"
category: civil-engineering
version: 1.0.0
disable-model-invocation: false
risk: low
source: "https://github.com/Mr-Nobody-Anonymous/All-skills"
source_repository: "Mr-Nobody-Anonymous/All-skills"
source_path: "awesome_skills/civil-engineering/surveying/SKILL.md"
license: "MIT"
imported_at: "2026-09-20"
---

# Surveying

## Scope
Surveying and geomatics establish precise geometric boundaries, elevations, and control networks for construction, topography, and legal property boundary definition.

## Computational Workflows
- **Traverse Computations**:
  - Latitudes: $\Delta Y = L \cos \theta$
  - Departures: $\Delta X = L \sin \theta$
  - Linear Misclosure: $E_c = \sqrt{(\sum \Delta X)^2 + (\sum \Delta Y)^2}$
  - Compass Rule (Bowditch) adjustment applied proportionally to line lengths.
- **Differential Leveling**: Elevation: $\text{Elev}_{\text{BM}} + \text{BS} = \text{HI}$; $\text{HI} - \text{FS} = \text{Elev}_{\text{TP}}$.

## Tools & Standards
- **Hardware**: Robotic Total Stations (Leica, Trimble), RTK-GNSS receivers, Digital levels.
- **Canonical References**: Ghilani & Wolf — *Elementary Surveying: An Introduction to Geomatics*.
