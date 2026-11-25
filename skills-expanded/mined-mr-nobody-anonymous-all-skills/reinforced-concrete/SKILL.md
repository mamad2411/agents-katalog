---
name: reinforced-concrete
description: "ACI 318 ultimate strength design, beam flexure, shear stirrups, columns (P-M interaction), development length, and crack control"
category: civil-engineering
version: 1.0.0
disable-model-invocation: false
risk: low
source: "https://github.com/Mr-Nobody-Anonymous/All-skills"
source_repository: "Mr-Nobody-Anonymous/All-skills"
source_path: "awesome_skills/civil-engineering/reinforced-concrete/SKILL.md"
license: "MIT"
imported_at: "2026-09-20"
---

# Reinforced Concrete Design

## Scope
Reinforced concrete engineering covers the composite design of concrete (high compressive strength) and steel rebar (high tensile strength) under ACI 318 code requirements.

## Core ACI 318 Formulations
- **Whitney Stress Block**: Equivalent uniform compressive stress $0.85 f_c'$ acting over depth $a = \beta_1 c$.
- **Nominal Flexural Strength ($M_n$)**:
  $$M_n = A_s f_y \left(d - \frac{a}{2}\right), \quad a = \frac{A_s f_y}{0.85 f_c' b}$$
  Design strength $\phi M_n \ge M_u$ ($\phi = 0.90$ for tension-controlled sections with strain $\epsilon_t \ge 0.005$).
- **Shear Design**: $\phi(V_c + V_s) \ge V_u$, with $V_c = 2\lambda\sqrt{f_c'} b_w d$, $V_s = \frac{A_v f_y d}{s}$.
- **Column P-M Interaction Diagram**: Plots axial capacity $P_n$ vs. moment capacity $M_n$ from pure compression down to pure tension.

## Tools & Standards
- **Codes**: ACI 318-19, Eurocode 2.
- **Software**: spColumn, ETABS, SAFE.
- **Canonical References**: Wight — *Reinforced Concrete: Mechanics and Design*.
