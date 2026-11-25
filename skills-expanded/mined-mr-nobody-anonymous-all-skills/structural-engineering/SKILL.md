---
name: structural-engineering
description: "Design and analysis of structures, load paths, ASCE 7 load combinations, AISC steel, and ACI concrete specifications"
category: civil-engineering
version: 1.0.0
disable-model-invocation: false
risk: low
source: "https://github.com/Mr-Nobody-Anonymous/All-skills"
source_repository: "Mr-Nobody-Anonymous/All-skills"
source_path: "awesome_skills/civil-engineering/structural-engineering/SKILL.md"
license: "MIT"
imported_at: "2026-09-20"
---

# Structural Engineering

## Scope
Structural engineering analyzes and designs load-bearing structures (buildings, bridges, industrial frameworks) to withstand gravity, environmental loads (wind, seismic, snow), and transient forces without collapse or unacceptable deflection.

## Core Design Codes & Formulations
- **ASCE 7 Load Combinations (LRFD)**:
  - $1.4 D$
  - $1.2 D + 1.6 L + 0.5(\text{Lr or S or R})$
  - $1.2 D + 1.0 W + 1.0 L + 0.5(\text{Lr or S or R})$
  - $1.2 D + 1.0 E + 1.0 L + 0.2 S$
  - $0.9 D + 1.0 W$ (uplift/overturning)
- **Flexural Capacity**: $\phi M_n \ge M_u$ where $\phi$ is strength reduction factor.
- **Shear Capacity**: $\phi V_n \ge V_u$, with $V_n = V_c + V_s$.
- **Deflection Limits**: Live load deflection $\Delta_{LL} \le L/360$; Total load $\Delta_{TL} \le L/240$.

## Tools & Standards
- **Codes**: ASCE/SEI 7, AISC 360 (Steel Construction), ACI 318 (Reinforced Concrete), IBC (International Building Code).
- **Software**: SAP2000, ETABS, STAAD.Pro, RISA-3D.
- **Canonical References**: Hibbeler — *Structural Analysis*; McCormac & Nelson — *Design of Reinforced Concrete*.
