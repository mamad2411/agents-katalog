---
name: rtl
description: "Register-Transfer Level design: synchronous state machines, pipeline registers, clock domain crossing (CDC), and FIFOs"
category: semiconductor
version: 1.0.0
disable-model-invocation: false
risk: low
source: "https://github.com/Mr-Nobody-Anonymous/All-skills"
source_repository: "Mr-Nobody-Anonymous/All-skills"
source_path: "awesome_skills/semiconductor/rtl/SKILL.md"
license: "MIT"
imported_at: "2026-09-20"
---

# RTL Design & Microarchitecture

## Scope
Register-Transfer Level microarchitecture designs synchronous digital logic describing data transfers between hardware registers in Verilog/SystemVerilog/VHDL.

## Microarchitectural Patterns
- **Clock Domain Crossing (CDC)**:
  - 2-Flip-Flop Synchronizer for single-bit quasi-static control signals (mitigates metastability, MTBF calculation).
  - Asynchronous Dual-Clock FIFO with Gray code pointers for multi-bit data transfers.
- **Pipelining**: Breaking combinational logic paths with intermediate registers to increase maximum operating frequency ($f_{\max}$).
- **Finite State Machine (FSM)**: Moore (outputs depend only on current state) vs. Mealy (outputs depend on current state and inputs).

## Tools & Standards
- **Software**: Synopsys Design Compiler, Cadence Genus, ModelSim, Verilator.
