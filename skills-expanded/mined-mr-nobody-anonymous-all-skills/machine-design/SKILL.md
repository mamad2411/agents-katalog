---
name: machine-design
description: "Design of shafts, gears (spur, helical), bearings (L10 life), springs, clutches, bolted joints, and fatigue failure theories (Goodman)"
category: mechanical-engineering
version: 1.0.0
disable-model-invocation: false
risk: low
source: "https://github.com/Mr-Nobody-Anonymous/All-skills"
source_repository: "Mr-Nobody-Anonymous/All-skills"
source_path: "awesome_skills/mechanical-engineering/machine-design/SKILL.md"
license: "MIT"
imported_at: "2026-09-20"
---

# Machine Design

## Scope
Machine design focuses on the sizing, material selection, stress evaluation, and fatigue life calculation of mechanical components and power transmission assemblies.

## Core Theories & Formulations
- **Fatigue Failure Theories (Modified Goodman Relation)**:
  $$\frac{\sigma_a}{S_e} + \frac{\sigma_m}{S_{ut}} = \frac{1}{n}$$
  where $\sigma_a$ is alternating stress, $\sigma_m$ mean stress, $S_e$ endurance limit, $S_{ut}$ ultimate tensile strength, $n$ design factor.
- **Endurance Limit Modification Factors (Marin Equation)**:
  $$S_e = k_a k_b k_c k_d k_e k_f S_e'$$
  where $k_a$ surface condition, $k_b$ size, $k_c$ load type, $k_d$ temperature, $k_e$ reliability.
- **Rolling-Element Bearing Life ($L_{10}$)**:
  $$L_{10} = \left(\frac{C}{P}\right)^p \times 10^6 \text{ revs}$$
  where $C$ is dynamic load rating, $P$ equivalent dynamic load, $p = 3$ (ball bearings) or $10/3$ (roller bearings).
- **AGMA Gear Bending Stress (Lewis Formula modified)**:
  $$\sigma = \frac{W_t}{F m Y} K_v K_o K_m$$

## Tools & Standards
- **Standards**: AGMA (American Gear Manufacturers Association), ASME B106.1M (Design of Transmission Shafting), ISO 281 (Bearings).
- **Software**: MITCalc, KISSsoft, Autodesk Inventor, SolidWorks Simulation.
- **Canonical References**: Shigley's *Mechanical Engineering Design* (Budynas & Nisbett); Norton — *Machine Design*.
