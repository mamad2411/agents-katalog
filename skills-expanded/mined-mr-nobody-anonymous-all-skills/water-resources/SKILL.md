---
name: water-resources
description: "Hydrologic routing, reservoir operation, flood frequency analysis (Log-Pearson III), and watershed modeling"
category: civil-engineering
version: 1.0.0
disable-model-invocation: false
risk: low
source: "https://github.com/Mr-Nobody-Anonymous/All-skills"
source_repository: "Mr-Nobody-Anonymous/All-skills"
source_path: "awesome_skills/civil-engineering/water-resources/SKILL.md"
license: "MIT"
imported_at: "2026-09-20"
---

# Water Resources Engineering

## Scope
Water resources engineering manages surface water supplies, flood risk, reservoir capacity, and municipal stormwater infrastructure.

## Formulations & Methods
- **Flood Frequency Analysis (Log-Pearson Type III)**:
  $$\log Q_T = \bar{x} + K_T \cdot s$$
  where $K_T$ is frequency factor dependent on return period $T$ and skewness coefficient $G$.
- **Hydrologic Storage Routing (Modified Puls Method)**:
  $$\frac{2S_{j+1}}{\Delta t} + O_{j+1} = (I_j + I_{j+1}) + \left(\frac{2S_j}{\Delta t} - O_j\right)$$

## Tools & Standards
- **Software**: HEC-HMS, HEC-ResSim, USGS PeakFQ.
- **Canonical References**: Mays — *Water Resources Engineering*.
