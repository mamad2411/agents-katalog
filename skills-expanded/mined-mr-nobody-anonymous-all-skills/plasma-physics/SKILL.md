---
name: plasma-physics
description: "Plasma parameters, Debye shielding, magnetohydrodynamics (MHD), plasma waves, and magnetic confinement fusion (Tokamak)"
category: physics
version: 1.0.0
disable-model-invocation: false
risk: low
source: "https://github.com/Mr-Nobody-Anonymous/All-skills"
source_repository: "Mr-Nobody-Anonymous/All-skills"
source_path: "awesome_skills/physics/plasma-physics/SKILL.md"
license: "MIT"
imported_at: "2026-09-20"
---

# Plasma Physics

## Scope
Plasma physics studies ionized gases containing free electrons and ions, exploring collective electromagnetic interactions, waves, instabilities, and nuclear fusion confinement.

## Core Principles & Formulations
- **Plasma Criteria**:
  - Debye Length: $\lambda_D = \sqrt{\frac{\varepsilon_0 k_B T_e}{n_e e^2}}$, shielding distance of electrostatic potential.
  - Plasma Parameter: $N_D = n_e \frac{4}{3}\pi \lambda_D^3 \gg 1$ (collective behavior).
  - Plasma Frequency: $\omega_{pe} = \sqrt{\frac{n_e e^2}{\varepsilon_0 m_e}}$.
- **Ideal Magnetohydrodynamics (MHD)**:
  $$\rho \left(\frac{\partial \mathbf{v}}{\partial t} + \mathbf{v} \cdot \nabla \mathbf{v}\right) = -\nabla p + \mathbf{J} \times \mathbf{B}, \quad \nabla \times \mathbf{B} = \mu_0 \mathbf{J}, \quad \frac{\partial \mathbf{B}}{\partial t} = \nabla \times (\mathbf{v} \times \mathbf{B})$$
- **Magnetic Confinement (Tokamak)**: Lawson criterion for fusion ignition: $n \tau_E T \ge 3 \times 10^{21}\text{ keV}\cdot\text{s/m}^3$.

## Tools & References
- **Software**: BOUT++, GENE, NIMROD.
- **Canonical References**: Chen — *Introduction to Plasma Physics and Controlled Fusion*; Freidberg — *Plasma Physics and Fusion Energy*.
