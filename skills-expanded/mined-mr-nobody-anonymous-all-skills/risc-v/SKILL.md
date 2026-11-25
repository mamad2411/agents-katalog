---
name: risc-v
description: "RISC-V ISA (RV32I, RV32E, standard extensions M, A, F, D, C), privileged architecture, CSR registers, and toolchains"
category: embedded
version: 1.0.0
disable-model-invocation: false
risk: low
source: "https://github.com/Mr-Nobody-Anonymous/All-skills"
source_repository: "Mr-Nobody-Anonymous/All-skills"
source_path: "awesome_skills/embedded/risc-v/SKILL.md"
license: "MIT"
imported_at: "2026-09-20"
---

# RISC-V Embedded Architecture

## Scope
Covers the open, modular RISC-V instruction set architecture, standard extensions, control and status registers (CSRs), and embedded firmware development.

## ISA Specifications
- **Base ISA (RV32I)**: 32-bit word size, 32 registers ($x0-x31$, $x0$ hardwired to 0).
- **Standard Modular Extensions**:
  - `M`: Integer multiplication and division hardware.
  - `A`: Atomic memory operations (load-reserved / store-conditional).
  - `F` / `D`: Single / double precision IEEE 754 floating point.
  - `C`: Compressed 16-bit instructions (reduces code size by $25-30\%$).
- **Privilege Levels**: Machine Mode (M-mode, highest, mandatory), Supervisor Mode (S-mode, OS), User Mode (U-mode).

## Tools & Standards
- **Toolchains**: `riscv64-unknown-elf-gcc`, Spike simulator, QEMU, OpenSBI.
- **Standards**: RISC-V Instruction Set Manual (Volume I: Unprivileged, Volume II: Privileged).
