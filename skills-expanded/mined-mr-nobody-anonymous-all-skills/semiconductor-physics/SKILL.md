---
name: semiconductor-physics
description: "Energy band diagrams, carrier concentration, drift-diffusion equations, recombination-generation, and p-n junction electrostatics"
category: semiconductor
version: 1.0.0
disable-model-invocation: false
risk: low
source: "https://github.com/Mr-Nobody-Anonymous/All-skills"
source_repository: "Mr-Nobody-Anonymous/All-skills"
source_path: "awesome_skills/semiconductor/semiconductor-physics/SKILL.md"
license: "MIT"
imported_at: "2026-09-20"
---

# Semiconductor Device Physics

## Scope
Semiconductor physics models carrier dynamics, energy bandgap transitions, doping profiles, and electrostatics in silicon, gallium arsenide, and wide-bandgap semiconductors (SiC, GaN).

## Core Physics & Formulations
- **Intrinsic Carrier Concentration ($n_i$)**:
  $$n_i = \sqrt{N_c N_v} \exp\left(-\frac{E_g}{2 k_B T}\right)$$
  Mass-action law: $n p = n_i^2$ in non-degenerate equilibrium.
- **Drift-Diffusion Current Equations**:
  $$J_n = q n \mu_n E + q D_n \frac{dn}{dx}, \quad J_p = q p \mu_p E - q D_p \frac{dp}{dx}$$
  Einstein relation: $\frac{D}{\mu} = \frac{k_B T}{q}$.
- **Poisson's Equation for p-n Junction**:
  $$\frac{d^2 \psi}{dx^2} = -\frac{\rho(x)}{\varepsilon_s} \implies W_{\text{dep}} = \sqrt{\frac{2\varepsilon_s (V_{bi} - V)}{q}\left(\frac{1}{N_a} + \frac{1}{N_d}\right)}$$

## Tools & References
- **Software**: Synopsys Sentaurus TCAD, Silvaco Atlas.
- **Canonical References**: Sze & Ng — *Physics of Semiconductor Devices*; Streetman & Banerjee.
