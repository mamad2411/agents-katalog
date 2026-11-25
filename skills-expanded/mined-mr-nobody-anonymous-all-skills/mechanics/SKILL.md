---
name: mechanics
description: "Statics and dynamics of rigid bodies, stress-strain tensors, Mohr's circle, torsion, beam deflection, and energy methods (Castigliano)"
category: mechanical-engineering
version: 1.0.0
disable-model-invocation: false
risk: low
source: "https://github.com/Mr-Nobody-Anonymous/All-skills"
source_repository: "Mr-Nobody-Anonymous/All-skills"
source_path: "awesome_skills/mechanical-engineering/mechanics/SKILL.md"
license: "MIT"
imported_at: "2026-09-20"
---

# Mechanics of Materials

## Scope
Mechanics of materials analyzes internal stress, strain, deformation, and stability of solid bodies subjected to external forces and moments.

## Fundamental Formulations
- **Hooke's Law (Generalized 3D Isotropic)**:
  $$\epsilon_x = \frac{1}{E}[\sigma_x - \nu(\sigma_y + \sigma_z)], \quad \gamma_{xy} = \frac{\tau_{xy}}{G}, \quad G = \frac{E}{2(1+\nu)}$$
- **Euler-Bernoulli Beam Flexure**:
  $$\sigma_x = -\frac{M y}{I}, \quad \tau = \frac{V Q}{I b}$$
- **Mohr's Circle & Principal Stresses**:
  $$\sigma_{1,2} = \frac{\sigma_x + \sigma_y}{2} \pm \sqrt{\left(\frac{\sigma_x - \sigma_y}{2}\right)^2 + \tau_{xy}^2}, \quad \tau_{\max} = \frac{\sigma_1 - \sigma_2}{2}$$
- **Castigliano's Second Theorem**: $\Delta_i = \frac{\partial U}{\partial P_i}$, where $U$ is total strain energy.

## Tools & References
- **Canonical References**: Beer, Johnston, DeWolf & Mazurek — *Mechanics of Materials*; Gere & Goodno.
