---
name: geotechnical-engineering
description: "Soil mechanics, shear strength (Mohr-Coulomb), bearing capacity, slope stability, and earth pressure"
category: civil-engineering
version: 1.0.0
disable-model-invocation: false
risk: low
source: "https://github.com/Mr-Nobody-Anonymous/All-skills"
source_repository: "Mr-Nobody-Anonymous/All-skills"
source_path: "awesome_skills/civil-engineering/geotechnical-engineering/SKILL.md"
license: "MIT"
imported_at: "2026-09-20"
---

# Geotechnical Engineering

## Scope
Geotechnical engineering investigates subsurface soil and rock mechanics to design stable foundations, retaining structures, embankments, and slopes.

## Core Formulations
- **Effective Stress Principle (Terzaghi)**: $\sigma' = \sigma - u$.
- **Mohr-Coulomb Shear Strength**: $\tau_f = c' + \sigma' \tan \phi'$.
- **Terzaghi's Ultimate Bearing Capacity**:
  $$q_{\text{ult}} = c' N_c + q N_q + \frac{1}{2} \gamma B N_\gamma$$
- **Lateral Earth Pressure (Rankine)**:
  - Active: $K_a = \frac{1 - \sin \phi'}{1 + \sin \phi'} = \tan^2(45^\circ - \phi'/2)$
  - Passive: $K_p = \frac{1 + \sin \phi'}{1 - \sin \phi'} = \tan^2(45^\circ + \phi'/2)$

## Tools & Standards
- **Standards**: ASTM D2487 (Unified Soil Classification System), ASTM D1586 (SPT), Eurocode 7.
- **Software**: GeoStudio (SLOPE/W, SEEP/W), PLAXIS, Rocscience (Slide2).
- **Canonical References**: Das & Sobhan — *Principles of Geotechnical Engineering*; Terzaghi, Peck & Mesri.
