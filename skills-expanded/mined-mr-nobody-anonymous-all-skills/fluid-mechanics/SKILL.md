---
name: fluid-mechanics
description: "Navier-Stokes equations, boundary layer theory, turbulent flow (Reynolds decomposition), external aerodynamics (lift/drag), and pipe flow"
category: mechanical-engineering
version: 1.0.0
disable-model-invocation: false
risk: low
source: "https://github.com/Mr-Nobody-Anonymous/All-skills"
source_repository: "Mr-Nobody-Anonymous/All-skills"
source_path: "awesome_skills/mechanical-engineering/fluid-mechanics/SKILL.md"
license: "MIT"
imported_at: "2026-09-20"
---

# Fluid Mechanics

## Scope
Fluid mechanics analyzes liquids and gases at rest and in motion, covering laminar/turbulent pipe networks, compressible flows, boundary layers, and aerodynamic forces.

## Governing Equations
- **Navier-Stokes Equation (Incompressible Newtonian)**:
  $$\rho \left(\frac{\partial \mathbf{v}}{\partial t} + \mathbf{v} \cdot \nabla \mathbf{v}\right) = -\nabla p + \mu \nabla^2 \mathbf{v} + \rho \mathbf{g}$$
- **Reynolds Number**: $Re = \frac{\rho v D}{\mu}$ ($Re < 2300$ laminar in pipe, $Re > 4000$ turbulent).
- **Prandtl Boundary Layer Equations**: Boundary layer thickness $\delta(x) \approx \frac{5.0 x}{\sqrt{Re_x}}$ (laminar) or $\delta(x) \approx \frac{0.37 x}{Re_x^{1/5}}$ (turbulent).
- **Lift & Drag Formulations**: $L = \frac{1}{2} C_L \rho v^2 A$, $D = \frac{1}{2} C_D \rho v^2 A$.

## Tools & Standards
- **Software**: OpenFOAM, ANSYS Fluent, Flow-3D.
- **Canonical References**: White — *Fluid Mechanics*; Munson, Young & Okiishi.
