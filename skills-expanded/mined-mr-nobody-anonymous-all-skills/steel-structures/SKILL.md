---
name: steel-structures
description: "AISC 360 specification, tension members, compact beam flexure, column buckling (Euler/Johnson), and bolted/welded connection design"
category: civil-engineering
version: 1.0.0
disable-model-invocation: false
risk: low
source: "https://github.com/Mr-Nobody-Anonymous/All-skills"
source_repository: "Mr-Nobody-Anonymous/All-skills"
source_path: "awesome_skills/civil-engineering/steel-structures/SKILL.md"
license: "MIT"
imported_at: "2026-09-20"
---

# Steel Structures

## Scope
Steel structures encompasses the design of structural steel frames, members, and connections following the AISC Specification for Structural Steel Buildings.

## Core AISC 360 Formulations
- **Tension Members**: Yielding on gross area: $\phi P_n = 0.90 F_y A_g$; Rupture on net effective area: $\phi P_n = 0.75 F_u A_e$.
- **Compression Members (Column Buckling)**:
  - Elastic critical buckling (Euler): $F_e = \frac{\pi^2 E}{(KL/r)^2}$.
  - Flexural buckling strength:
    $$F_{cr} = \left[0.658^{\frac{F_y}{F_e}}\right] F_y \quad \text{for } \frac{KL}{r} \le 4.71\sqrt{\frac{E}{F_y}}$$
- **Flexural Members (Beams)**: Lateral-Torsional Buckling (LTB) based on unbraced length $L_b$ compared to $L_p$ and $L_r$.
- **Connection Design**: Fillet welds $\phi R_n = 0.75 (0.60 F_{\text{EXX}}) (0.707 w L)$; High-strength bolts (ASTM F3125 Grade A325/A490) in shear and bearing.

## Tools & Standards
- **Codes**: AISC 360, AISC 341 (Seismic Provisions).
- **Software**: RAM Structural System, RISA-3D, IDEA StatiCa (connection FEM).
- **Canonical References**: Salmon, Johnson & Malhas — *Steel Structures: Design and Behavior*.
