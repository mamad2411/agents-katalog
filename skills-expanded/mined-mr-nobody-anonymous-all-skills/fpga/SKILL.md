---
name: fpga
description: "Field-Programmable Gate Arrays: LUTs, flip-flops, DSP slices, Block RAM, placement and routing, and timing closure"
category: semiconductor
version: 1.0.0
disable-model-invocation: false
risk: low
source: "https://github.com/Mr-Nobody-Anonymous/All-skills"
source_repository: "Mr-Nobody-Anonymous/All-skills"
source_path: "awesome_skills/semiconductor/fpga/SKILL.md"
license: "MIT"
imported_at: "2026-09-20"
---

# FPGA Architecture & Implementation

## Scope
FPGA engineering configures reconfigurable silicon platforms (AMD Xilinx, Intel Altera) through RTL synthesis, place-and-route, DSP optimization, and timing closure.

## FPGA Fabric Architecture
- **Configurable Logic Blocks (CLBs)**: 6-input Look-Up Tables (LUT6), flip-flops, and carry-chain logic.
- **Dedicated Hard IP**: DSP48 slices (MAC operations: $P = A \times B + C$), Block RAM (BRAM, UltraRAM), PCIe gen4/gen5 endpoints, Transceivers (GTY/GTH).
- **Timing Closure Techniques**: Register retiming, pipelining critical high-fanout paths, false-path constraints (`set_false_path`), multicycle paths.

## Tools & Standards
- **Software**: Xilinx Vivado, Intel Quartus Prime, Yosys.
