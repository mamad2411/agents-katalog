---
name: formal-verification
description: "Model checking, property specification language (SVA), bounded model checking (BMC), and equivalence checking"
category: semiconductor
version: 1.0.0
disable-model-invocation: false
risk: low
source: "https://github.com/Mr-Nobody-Anonymous/All-skills"
source_repository: "Mr-Nobody-Anonymous/All-skills"
source_path: "awesome_skills/semiconductor/formal-verification/SKILL.md"
license: "MIT"
imported_at: "2026-09-20"
---

# Formal Hardware Verification

## Scope
Formal verification mathematically proves whether an RTL digital design conforms to specification properties under all allowable input sequences, without simulation testbenches.

## Verification Formalisms & Languages
- **SystemVerilog Assertions (SVA)**:
  - Immediate vs. Concurrent assertions (`assert property (@(posedge clk) req |-> ##[1:5] ack);`).
  - Sequence operators: Implication (`|->`, `|=>`), consecutive repetition (`[*n]`).
- **Engines**: Bounded Model Checking (BMC, unrolls design to depth $k$), k-induction, Mathematical equivalence checking (LEC, proves RTL equals synthesized gate netlist).

## Tools & Standards
- **Software**: Synopsys Formality, Cadence JasperGold, OneSpin, SymbiYosys.
