---
name: jtag
description: "Joint Test Action Group (IEEE 1149.1): TAP controller state machine, boundary scan testing, BSDL files, and programming targets"
category: embedded
version: 1.0.0
disable-model-invocation: false
risk: low
source: "https://github.com/Mr-Nobody-Anonymous/All-skills"
source_repository: "Mr-Nobody-Anonymous/All-skills"
source_path: "awesome_skills/embedded/jtag/SKILL.md"
license: "MIT"
imported_at: "2026-09-20"
---

# JTAG & Boundary Scan

## Scope
JTAG protocol engineering for hardware manufacturing test (boundary scan), board-level interconnect validation, and in-circuit CPU debugging.

## TAP Controller Architecture
- **4 Mandatory Pins**: TCK (Test Clock), TMS (Test Mode Select), TDI (Test Data In), TDO (Test Data Out), plus optional $\overline{\text{TRST}}$ (Test Reset).
- **TAP State Machine**: 16-state finite state machine governed by TMS transitions on TCK rising edge (Test-Logic-Reset, Run-Test/Idle, Select-DR, Select-IR).
- **Standard Instructions**: BYPASS (1-bit shift register), IDCODE (32-bit manufacturer/device ID), EXTEST (boundary scan pin driving/reading), SAMPLE/PRELOAD.
- **Boundary Scan Description Language (BSDL)**: Standardized VHDL subset modeling boundary scan register chains for automated automated test pattern generation (ATPG).

## Standards & References
- **Standards**: IEEE 1149.1 (Standard Test Access Port and Boundary-Scan Architecture).
- **Software**: OpenOCD, UrJTAG, TopJTAG.
