---
name: lithography
description: "Deep Ultraviolet (DUV) and Extreme Ultraviolet (EUV 13.5nm) lithography, optical proximity correction (OPC), and photoresist chemistry"
category: semiconductor
version: 1.0.0
disable-model-invocation: false
risk: low
source: "https://github.com/Mr-Nobody-Anonymous/All-skills"
source_repository: "Mr-Nobody-Anonymous/All-skills"
source_path: "awesome_skills/semiconductor/lithography/SKILL.md"
license: "MIT"
imported_at: "2026-09-20"
---

# Semiconductor Lithography

## Scope
Semiconductor lithography projects nanometer-scale circuit geometric patterns onto photoresist-coated semiconductor wafers using DUV (193nm immersion) and EUV (13.5nm) light sources.

## Optical Lithography Formulations
- **Rayleigh Resolution Limit**:
  $$R = k_1 \frac{\lambda}{\text{NA}}$$
  where $\lambda$ is wavelength ($193\text{ nm}$ ArF excimer laser, $13.5\text{ nm}$ EUV laser-produced plasma), $\text{NA} = n \sin \alpha$ numerical aperture ($1.35$ for water immersion), $k_1$ process factor.
- **Depth of Focus (DOF)**: $\text{DOF} = k_2 \frac{\lambda}{\text{NA}^2}$.
- **Computational Lithography**: Optical Proximity Correction (OPC, adding serifs and shifting polygon edges to correct diffraction blur), Phase-Shift Masks (PSM).

## Tools & Standards
- **Hardware**: ASML Twinscan EUV / DUV scanners.
- **Canonical References**: Mack — *Fundamental Principles of Optical Lithography*.
