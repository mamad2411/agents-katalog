---
name: finite-element-analysis
description: "Linear static, modal, non-linear (geometric/contact), mesh convergence, stress singularities, and element formulations"
category: mechanical-engineering
version: 1.0.0
disable-model-invocation: false
risk: low
source: "https://github.com/Mr-Nobody-Anonymous/All-skills"
source_repository: "Mr-Nobody-Anonymous/All-skills"
source_path: "awesome_skills/mechanical-engineering/finite-element-analysis/SKILL.md"
license: "MIT"
imported_at: "2026-09-20"
---

# Finite Element Analysis (FEA)

## Scope
Finite element analysis numerically predicts stress distributions, deflections, thermal gradients, and modal frequencies by discretizing continuum structures into finite elements.

## FEA Formulation & Best Practices
- **Weak Form & Element Discretization**: $[K_e] = \int_V [B]^T [D] [B] dV$.
- **Element Types**:
  - 1D Beams (Timoshenko, Euler-Bernoulli).
  - 2D Shells (Mindlin-Reissner, thin/thick plate theory).
  - 3D Continuum Bricks (Hex8, Hex20) and Tetrahedrals (Tet10 quadratic preferred over stiff Tet4).
- **Mesh Convergence Verification**: Refine mesh until maximum stress converges within $\le 3-5\%$, excluding mathematical stress singularities (reentrant sharp corners).
- **Contact Non-Linearity**: Penalty vs. Lagrange multiplier formulations for normal pressure; Coulomb friction tangentially.

## Tools & Standards
- **Software**: ANSYS Mechanical, Abaqus, Nastran, COMSOL Multiphysics, CalculiX.
- **Canonical References**: Bathe — *Finite Element Procedures*; Cook et al. — *Concepts and Applications of Finite Element Analysis*.
