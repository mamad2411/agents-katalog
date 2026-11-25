---
name: dft
description: "Design for Testability: scan chain insertion, ATPG (automatic test pattern generation), BIST (memory BIST, logic BIST), and boundary scan"
category: semiconductor
version: 1.0.0
disable-model-invocation: false
risk: low
source: "https://github.com/Mr-Nobody-Anonymous/All-skills"
source_repository: "Mr-Nobody-Anonymous/All-skills"
source_path: "awesome_skills/semiconductor/dft/SKILL.md"
license: "MIT"
imported_at: "2026-09-20"
---

# Design for Testability (DFT)

## Scope
DFT embeds hardware test structures into IC designs to detect physical silicon fabrication defects (stuck-at, at-speed transition faults) during wafer sort and package test.

## DFT Architecture & Fault Models
- **Scan Insertion**: Replacing standard flip-flops with scan flip-flops multiplexing a test input (`SI`), test enable (`SE`), and test output (`SO`), chaining all registers into massive shift registers.
- **Fault Models**: Stuck-at-0 (SA0), Stuck-at-1 (SA1), At-Speed Transition Delay Faults (launch-off-capture, launch-off-shift).
- **Built-In Self-Test (BIST)**: Memory BIST (MBIST) state machine executing March tests (March C-) on embedded SRAM arrays.

## Tools & Standards
- **Software**: Synopsys TestMAX, Siemens Tessent, Cadence Modus.
