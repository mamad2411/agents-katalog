---
name: transistor-design
description: "MOSFET scaling, short-channel effects (DIBL, subthreshold swing), FinFET 3D architectures, and Gate-All-Around (GAA) nanosheets"
category: semiconductor
version: 1.0.0
disable-model-invocation: false
risk: low
source: "https://github.com/Mr-Nobody-Anonymous/All-skills"
source_repository: "Mr-Nobody-Anonymous/All-skills"
source_path: "awesome_skills/semiconductor/transistor-design/SKILL.md"
license: "MIT"
imported_at: "2026-09-20"
---

# Transistor Design & Advanced Architectures

## Scope
Advanced transistor engineering explores CMOS scaling, leakage mitigation, multi-gate architectures (FinFET), and Gate-All-Around (GAA) nanosheets for sub-3nm nodes.

## Transistor Physics & Short-Channel Effects (SCE)
- **Subthreshold Swing ($SS$)**:
  $$SS = \ln(10) \frac{k_B T}{q}\left(1 + \frac{C_{\text{dep}}}{C_{ox}}\right)$$
  Theoretical limit at room temperature: $60\text{ mV/decade}$.
- **Drain-Induced Barrier Lowering (DIBL)**: $\text{DIBL} = -\frac{\Delta V_{\text{th}}}{\Delta V_{ds}}$.
- **FinFET vs. GAA Nanosheet**: Electrostatic gate control wrapping 3 sides (FinFET) vs. 4 sides (Nanosheet), suppressing punch-through leakage currents.

## Tools & References
- **Canonical References**: Taur & Ning — *Fundamentals of Modern VLSI Devices*.
