---
name: coastal-engineering
description: "Wave mechanics (Airy linear theory), coastal sediment transport, storm surge modeling, seawalls, breakwaters, and groins"
category: civil-engineering
version: 1.0.0
disable-model-invocation: false
risk: low
source: "https://github.com/Mr-Nobody-Anonymous/All-skills"
source_repository: "Mr-Nobody-Anonymous/All-skills"
source_path: "awesome_skills/civil-engineering/coastal-engineering/SKILL.md"
license: "MIT"
imported_at: "2026-09-20"
---

# Coastal Engineering

## Scope
Coastal engineering addresses coastal defense, harbor design, shoreline stabilization, and nearshore hydrodynamics under wave, tide, and storm action.

## Core Formulations
- **Airy Linear Wave Theory**:
  - Wave dispersion: $\omega^2 = g k \tanh(k h)$, where $k = 2\pi/L$, $\omega = 2\pi/T$.
  - Deep water ($h/L > 0.5$): $L_0 = \frac{g T^2}{2\pi} \approx 1.56 T^2\text{ m}$.
  - Shallow water ($h/L < 0.05$): Celerity $c = \sqrt{gh}$.
- **Hudson's Formula (Rubble-Mound Breakwater Armor Weight)**:
  $$W = \frac{\gamma_r H^3}{K_D (S_r - 1)^3 \cot \theta}$$

## Tools & Standards
- **Standards**: USACE Coastal Engineering Manual (CEM).
- **Software**: SWAN (Simulating Waves Nearshore), DELFT3D, CMS (Coastal Modeling System).
