---
name: foundation-design
description: "Shallow spread footings, mat foundations, deep driven piles, drilled shafts, lateral pile capacity (p-y curves), and settlement"
category: civil-engineering
version: 1.0.0
disable-model-invocation: false
risk: low
source: "https://github.com/Mr-Nobody-Anonymous/All-skills"
source_repository: "Mr-Nobody-Anonymous/All-skills"
source_path: "awesome_skills/civil-engineering/foundation-design/SKILL.md"
license: "MIT"
imported_at: "2026-09-20"
---

# Foundation Design

## Scope
Foundation design safely transfers superstructure column and wall reactions to the subsurface soil or rock mass without structural failure or excessive differential settlement.

## Design Procedures
- **Shallow Footings**: Sized for allowable bearing pressure $q_{\text{all}} = q_{\text{ult}} / \text{FS}$ ($\text{FS} \ge 3.0$). Check one-way beam shear and two-way punching shear ($\phi V_c$).
- **Settlement Analysis**:
  - Elastic settlement (immediate): Janbu or Bowles equation.
  - Primary consolidation settlement (clays): $S_c = \frac{C_c H_0}{1 + e_0} \log_{10}\left(\frac{\sigma_{v0}' + \Delta \sigma_v'}{\sigma_{v0}'}\right)$.
- **Deep Foundations (Piles/Shafts)**: Total ultimate capacity $Q_{\text{ult}} = Q_b + Q_s = q_p A_p + \sum f_s A_s$. Lateral analysis via $p-y$ curves (Reese/Matlock).

## Tools & Standards
- **Codes**: ACI 318, IBC Chapter 18.
- **Software**: LPILE, GROUP, SAFE, ALLPILE.
- **Canonical References**: Bowles — *Foundation Analysis and Design*.
