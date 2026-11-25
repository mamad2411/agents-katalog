---
name: earthquake-engineering
description: "Seismic hazard analysis (PSHA), response spectra, equivalent lateral force procedure, ductility reduction, and base isolation"
category: civil-engineering
version: 1.0.0
disable-model-invocation: false
risk: low
source: "https://github.com/Mr-Nobody-Anonymous/All-skills"
source_repository: "Mr-Nobody-Anonymous/All-skills"
source_path: "awesome_skills/civil-engineering/earthquake-engineering/SKILL.md"
license: "MIT"
imported_at: "2026-09-20"
---

# Earthquake Engineering

## Scope
Earthquake engineering designs structures to resist ground motion shaking, mitigating collapse risk and ensuring post-earthquake functional recovery.

## Formulations & Procedures
- **Design Response Spectrum (ASCE 7)**:
  - Short-period parameter: $S_{DS} = \frac{2}{3} S_{MS} = \frac{2}{3} F_a S_s$
  - 1-second period parameter: $S_{D1} = \frac{2}{3} S_{M1} = \frac{2}{3} F_v S_1$
- **Equivalent Lateral Force (ELF) Procedure**:
  - Seismic Base Shear: $V = C_s W$
  - Seismic response coefficient: $C_s = \frac{S_{DS}}{(R / I_e)}$, bounded by $C_s \le \frac{S_{D1}}{T(R / I_e)}$
  - Vertical distribution of seismic force: $F_x = C_{vx} V$, with $C_{vx} = \frac{w_x h_x^k}{\sum w_i h_i^k}$.

## Tools & Standards
- **Codes**: ASCE 7 Chapter 12, NEHRP Provisions, Eurocode 8.
- **Software**: OpenSees, ETABS (Nonlinear pushover & response spectrum), Perform-3D.
- **Canonical References**: Chopra — *Dynamics of Structures: Theory and Applications to Earthquake Engineering*.
