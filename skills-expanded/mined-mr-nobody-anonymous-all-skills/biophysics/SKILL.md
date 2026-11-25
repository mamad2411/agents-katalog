---
name: biophysics
description: "Macromolecular mechanics, membrane potential, ion channels (Hodgkin-Huxley), optical tweezers, and biological thermodynamics"
category: physics
version: 1.0.0
disable-model-invocation: false
risk: low
source: "https://github.com/Mr-Nobody-Anonymous/All-skills"
source_repository: "Mr-Nobody-Anonymous/All-skills"
source_path: "awesome_skills/physics/biophysics/SKILL.md"
license: "MIT"
imported_at: "2026-09-20"
---

# Biophysics

## Scope
Biophysics applies the theories and methods of physics to understand how biological systems work, from molecular motors to neural electrical propagation.

## Core Biophysical Models
- **Membrane Potential (Goldman-Hodgkin-Katz Equation)**:
  $$V_m = \frac{RT}{F} \ln\left(\frac{P_{\text{K}}[K^+]_o + P_{\text{Na}}[\text{Na}^+]_o + P_{\text{Cl}}[\text{Cl}^-]_i}{P_{\text{K}}[K^+]_i + P_{\text{Na}}[\text{Na}^+]_i + P_{\text{Cl}}[\text{Cl}^-]_o}\right)$$
- **Hodgkin-Huxley Model**: Action potential generation via voltage-gated $Na^+$ and $K^+$ conductances:
  $$C_m \frac{dV}{dt} = -\bar{g}_{\text{Na}} m^3 h (V - V_{\text{Na}}) - \bar{g}_{\text{K}} n^4 (V - V_{\text{K}}) - g_L (V - V_L) + I_{\text{app}}$$
- **Polymer Physics of DNA**: Worm-like chain (WLC) model, persistence length $\xi_p \approx 50\text{ nm}$.

## Tools & References
- **Software**: NEURON, Visual Molecular Dynamics (VMD).
- **Canonical References**: Nelson — *Biological Physics*; Phillips et al. — *Physical Biology of the Cell*.
