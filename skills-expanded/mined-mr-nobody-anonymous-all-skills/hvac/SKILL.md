---
name: hvac
description: "Heating, ventilation, and air conditioning: cooling load calculations, psychrometric chart analysis, duct design, and ASHRAE standards"
category: mechanical-engineering
version: 1.0.0
disable-model-invocation: false
risk: low
source: "https://github.com/Mr-Nobody-Anonymous/All-skills"
source_repository: "Mr-Nobody-Anonymous/All-skills"
source_path: "awesome_skills/mechanical-engineering/hvac/SKILL.md"
license: "MIT"
imported_at: "2026-09-20"
---

# HVAC Engineering

## Scope
HVAC engineering provides indoor environmental thermal comfort and acceptable air quality via heating, ventilation, cooling, and refrigeration cycle systems.

## Psychrometrics & Cooling Load
- **Psychrometric Properties**: Dry-bulb temp ($T_{db}$), wet-bulb temp ($T_{wb}$), dew point ($T_{dp}$), relative humidity ($\text{RH}$), humidity ratio ($W$, $kg_{w}/kg_{da}$), enthalpy ($h$).
- **Cooling Load Calculation (ASHRAE CLTD/CLF or RTS Method)**:
  - Sensible heat: $q_s = 1.08 \times \text{CFM} \times \Delta T\text{ (BTU/hr)}$.
  - Latent heat: $q_l = 4840 \times \text{CFM} \times \Delta W\text{ (BTU/hr)}$.
  - Total heat: $q_t = 4.5 \times \text{CFM} \times \Delta h\text{ (BTU/hr)}$.
- **Duct Design**: Equal friction method (typically $0.1\text{ in. w.g. per } 100\text{ ft}$).

## Tools & Standards
- **Standards**: ASHRAE 62.1 (Ventilation for Acceptable Indoor Air Quality), ASHRAE 90.1 (Energy Standard), ASHRAE 55 (Thermal Comfort).
- **Software**: Carrier HAP, Trane TRACE 700 / 3D Plus, EnergyPlus.
- **Canonical References**: ASHRAE Handbooks (Fundamentals, HVAC Systems and Equipment).
