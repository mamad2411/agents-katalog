---
name: digital-ic
description: "Standard cell library design, CMOS inverter sizing (logical effort), static timing analysis (STA), setup/hold slack, and clock trees"
category: semiconductor
version: 1.0.0
disable-model-invocation: false
risk: low
source: "https://github.com/Mr-Nobody-Anonymous/All-skills"
source_repository: "Mr-Nobody-Anonymous/All-skills"
source_path: "awesome_skills/semiconductor/digital-ic/SKILL.md"
license: "MIT"
imported_at: "2026-09-20"
---

# Digital IC Design & Standard Cells

## Scope
Digital integrated circuit engineering covers static CMOS logic synthesis, logical effort sizing, timing paths, clock tree synthesis, and low-power multi-voltage designs.

## Timing & Logical Effort Formulations
- **Logical Effort ($g$) & Electrical Effort ($h$)**: Path delay $D = \sum (g_i h_i + p_i)$, minimum delay when stage efforts $f = g_i h_i$ are balanced.
- **Static Timing Analysis (STA)**:
  - Setup condition: $T_{\text{clk}} \ge T_{\text{cq}} + T_{\text{comb}(\max)} + T_{\text{setup}} - T_{\text{skew}}$.
  - Hold condition: $T_{\text{cq}} + T_{\text{comb}(\min)} \ge T_{\text{hold}} + T_{\text{skew}}$.
- **Clock Tree Synthesis (CTS)**: H-tree and clock mesh topologies minimizing skew and clock insertion delay.

## Tools & Standards
- **Software**: Synopsys PrimeTime, Cadence Tempus, Innovus.
- **Canonical References**: Weste & Harris — *CMOS VLSI Design: A Circuits and Systems Perspective*.
