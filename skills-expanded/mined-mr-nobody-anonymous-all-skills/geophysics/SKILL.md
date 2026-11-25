---
name: geophysics
description: "Seismic exploration, gravity anomalies, geomagnetic surveys, electrical resistivity, and mantle dynamics"
category: earth-science
version: 1.0.0
disable-model-invocation: false
risk: low
source: "https://github.com/Mr-Nobody-Anonymous/All-skills"
source_repository: "Mr-Nobody-Anonymous/All-skills"
source_path: "awesome_skills/earth-science/geophysics/SKILL.md"
license: "MIT"
imported_at: "2026-09-20"
---

# Geophysics

## Scope
Geophysics applies physical principles (wave propagation, gravitational fields, electromagnetism) to determine the subsurface structure, composition, and dynamics of the Earth.

## Geophysical Methods & Physics

### 1. Seismic Methods (Wave Propagation)
- **Body Waves**:
  - P-waves (compressional, longitudinal): $v_p = \sqrt{\frac{K + \frac{4}{3}\mu}{\rho}}$.
  - S-waves (shear, transverse): $v_s = \sqrt{\frac{\mu}{\rho}}$ (cannot propagate in liquids, $\mu=0$).
- **Snell's Law of Refraction**:
  $$\frac{\sin i_1}{v_1} = \frac{\sin i_2}{v_2}$$
  Critical angle $i_c = \arcsin(v_1 / v_2)$.
- **Seismic Reflection**: Normal incidence reflection coefficient:
  $$R = \frac{\rho_2 v_2 - \rho_1 v_1}{\rho_2 v_2 + \rho_1 v_1} = \frac{Z_2 - Z_1}{Z_2 + Z_1}$$
  where $Z = \rho v$ is acoustic impedance.

### 2. Gravity & Geomagnetics
- **Bouguer Anomaly**: $\Delta g_B = g_{\text{obs}} - g_\phi + \delta g_{FA} - \delta g_B + \delta g_T$.
- **Geomagnetic Induction**: Maxwell's equations applied to planetary dynamo and magnetotelluric (MT) sounding: apparent resistivity $\rho_a = \frac{1}{\omega \mu_0} |E_x / H_y|^2$.

## Tools & Standards
- **Software**: Seismic Unix, Madagascar, SimPEG, GMT (Generic Mapping Tools), ObsPy.
- **Canonical References**: Telford, Geldart & Sheriff — *Applied Geophysics*; Lowrie — *Fundamentals of Geophysics*.
