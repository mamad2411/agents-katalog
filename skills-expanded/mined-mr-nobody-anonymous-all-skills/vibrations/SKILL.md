---
name: vibrations
description: "Free and forced vibration, single and multi-DOF systems, resonance, damping models, vibration isolation, and modal analysis"
category: mechanical-engineering
version: 1.0.0
disable-model-invocation: false
risk: low
source: "https://github.com/Mr-Nobody-Anonymous/All-skills"
source_repository: "Mr-Nobody-Anonymous/All-skills"
source_path: "awesome_skills/mechanical-engineering/vibrations/SKILL.md"
license: "MIT"
imported_at: "2026-09-20"
---

# Mechanical Vibrations

## Scope
Mechanical vibrations investigates oscillatory motion in structures and machines, resonant frequencies, damping mechanisms, and vibration isolation design.

## Core Formulations
- **Single Degree of Freedom (SDOF) Equation**:
  $$m \ddot{x} + c \dot{x} + k x = F_0 \cos(\omega t)$$
  - Natural Frequency: $\omega_n = \sqrt{k / m}$.
  - Damping Ratio: $\zeta = \frac{c}{2 m \omega_n} = \frac{c}{c_c}$.
  - Damped Frequency: $\omega_d = \omega_n \sqrt{1 - \zeta^2}$ (for $\zeta < 1$).
- **Magnification Factor & Resonance**:
  $$M = \frac{1}{\sqrt{(1 - r^2)^2 + (2\zeta r)^2}} \quad (r = \omega / \omega_n)$$
  At resonance ($r \approx 1$), $M_{\max} \approx \frac{1}{2\zeta} = Q$ (Quality Factor).
- **Vibration Transmissibility**:
  $$TR = \frac{F_{\text{transmitted}}}{F_0} = \sqrt{\frac{1 + (2\zeta r)^2}{(1 - r^2)^2 + (2\zeta r)^2}}$$
  Isolation requires $r > \sqrt{2}$.

## Tools & Standards
- **Standards**: ISO 10816 (Mechanical vibration evaluation on non-rotating parts).
- **Software**: MATLAB, ANSYS Modal, Dewesoft.
- **Canonical References**: Rao — *Mechanical Vibrations*; Inman — *Engineering Vibration*.
