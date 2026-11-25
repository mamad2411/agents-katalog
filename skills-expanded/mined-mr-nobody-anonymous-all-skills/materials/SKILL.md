---
name: materials
description: "Mechanical behavior of materials: tension test, stress-strain, hardening, fracture mechanics (KIC), creep, and fatigue"
category: mechanical-engineering
version: 1.0.0
disable-model-invocation: false
risk: low
source: "https://github.com/Mr-Nobody-Anonymous/All-skills"
source_repository: "Mr-Nobody-Anonymous/All-skills"
source_path: "awesome_skills/mechanical-engineering/materials/SKILL.md"
license: "MIT"
imported_at: "2026-09-20"
---

# Materials Selection & Mechanical Behavior

## Scope
Evaluates physical, mechanical, thermal, and degradation properties of engineering materials to select optimal alloys, polymers, and composites for mechanical assemblies.

## Mechanical Characterization
- **Engineering vs. True Stress/Strain**: $\sigma_{\text{true}} = \sigma_{\text{eng}}(1 + \epsilon_{\text{eng}})$, $\epsilon_{\text{true}} = \ln(1 + \epsilon_{\text{eng}})$.
- **Yield Criteria**:
  - Von Mises (Distortion Energy): $\sigma_v = \frac{1}{\sqrt{2}}\sqrt{(\sigma_1 - \sigma_2)^2 + (\sigma_2 - \sigma_3)^2 + (\sigma_3 - \sigma_1)^2} \ge S_y$.
  - Tresca (Maximum Shear): $\tau_{\max} = \frac{\sigma_1 - \sigma_3}{2} \ge \frac{S_y}{2}$.
- **Linear Elastic Fracture Mechanics (LEFM)**: Stress intensity factor $K_I = Y \sigma \sqrt{\pi a} \le K_{Ic}$ (Plane-strain fracture toughness).
- **Ashby Material Selection Charts**: Performance metrics (e.g., minimum weight beam: $\max(E^{1/2} / \rho)$).

## Tools & Standards
- **Standards**: ASTM E8 (Tensile testing of metals), ASTM E399 (Fracture toughness).
- **Software**: Ansys Granta EduPack / Granta Selector.
- **Canonical References**: Ashby — *Materials Selection in Mechanical Design*; Callister & Rethwisch.
