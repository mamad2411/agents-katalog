---
name: analog-ic
description: "Operational transconductance amplifiers (OTA), current mirrors, bandgap reference circuits, frequency compensation, and phase margin"
category: semiconductor
version: 1.0.0
disable-model-invocation: false
risk: low
source: "https://github.com/Mr-Nobody-Anonymous/All-skills"
source_repository: "Mr-Nobody-Anonymous/All-skills"
source_path: "awesome_skills/semiconductor/analog-ic/SKILL.md"
license: "MIT"
imported_at: "2026-09-20"
---

# Analog IC Design

## Scope
Analog integrated circuit design creates continuous-time operational amplifiers, bandgap voltage references, low-dropout regulators (LDO), and data converters (ADC/DAC).

## Core Circuits & Formulations
- **Small-Signal Transconductance ($g_m$)**: $g_m = \mu_n C_{ox} \frac{W}{L} (V_{gs} - V_{th}) = \sqrt{2 \mu_n C_{ox} \frac{W}{L} I_D} = \frac{2 I_D}{V_{ov}}$.
- **Cascode Gain Stage**: High output impedance $R_{\text{out}} \approx g_{m2} r_{o2} r_{o1}$, boosting intrinsic gain $A_v \approx (g_{m1} r_{o1})(g_{m2} r_{o2})$.
- **Miller Frequency Compensation**: Introduces capacitor $C_c$ across high-gain stage, splitting dominant and non-dominant poles to achieve Phase Margin $\text{PM} \ge 60^\circ$.

## Tools & Standards
- **Software**: Cadence Virtuoso, Synopsys Custom Compiler, SPICE (Spectre, HSPICE).
- **Canonical References**: Razavi — *Design of Analog CMOS Integrated Circuits*; Gray & Meyer.
