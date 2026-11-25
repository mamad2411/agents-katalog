---
name: heat-transfer
description: "Conduction (Fourier's law, transient lumped capacitance), convection (Nusselt correlations), and radiation (view factors, Stefan-Boltzmann)"
category: mechanical-engineering
version: 1.0.0
disable-model-invocation: false
risk: low
source: "https://github.com/Mr-Nobody-Anonymous/All-skills"
source_repository: "Mr-Nobody-Anonymous/All-skills"
source_path: "awesome_skills/mechanical-engineering/heat-transfer/SKILL.md"
license: "MIT"
imported_at: "2026-09-20"
---

# Heat Transfer

## Scope
Heat transfer analyzes the rate of thermal energy exchange across temperature gradients via conduction, convection, and electromagnetic radiation.

## Core Mechanisms & Equations
- **Conduction**: Fourier's Law: $q'' = -k \nabla T$.
  - 1D radial cylinder: $q = \frac{2\pi L k (T_1 - T_2)}{\ln(r_2 / r_1)}$.
  - Lumped Capacitance ($Bi = h L_c / k < 0.1$): $\frac{T(t) - T_\infty}{T_i - T_\infty} = \exp\left(-\frac{h A_s}{\rho V c} t\right)$.
- **Convection**: Newton's Law of Cooling: $q'' = h (T_s - T_\infty)$.
  - Nusselt number: $Nu = \frac{h L}{k_f} = f(Re, Pr)$ (Dittus-Boelter: $Nu_D = 0.023 Re_D^{0.8} Pr^n$).
- **Radiation**: Stefan-Boltzmann: $q = \epsilon \sigma A (T_1^4 - T_2^4)$, where $\sigma = 5.67 \times 10^{-8}\text{ W/m}^2\text{K}^4$; View factor algebra $\sum F_{ij} = 1$.
- **Heat Exchangers**: LMTD method $\Delta T_{lm} = \frac{\Delta T_1 - \Delta T_2}{\ln(\Delta T_1 / \Delta T_2)}$; $\epsilon-\text{NTU}$ method.

## Tools & Standards
- **Software**: COMSOL Heat Transfer, ANSYS Thermal.
- **Canonical References**: Incropera, DeWitt, Bergman & Lavine — *Fundamentals of Heat and Mass Transfer*.
