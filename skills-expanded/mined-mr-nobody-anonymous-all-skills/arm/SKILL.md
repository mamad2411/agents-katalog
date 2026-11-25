---
name: arm
description: "ARM Cortex-M (M0+, M3, M4F, M7, M33) assembly, Thumb-2 instruction set, DSP extensions, FPU, and CMSIS hardware abstraction"
category: embedded
version: 1.0.0
disable-model-invocation: false
risk: low
source: "https://github.com/Mr-Nobody-Anonymous/All-skills"
source_repository: "Mr-Nobody-Anonymous/All-skills"
source_path: "awesome_skills/embedded/arm/SKILL.md"
license: "MIT"
imported_at: "2026-09-20"
---

# ARM Cortex-M Architecture

## Scope
Covers software development, assembly optimization, exception handling, and hardware abstraction on the industry-standard ARM Cortex-M processor family.

## Architectural Features
- **Registers**: $R0-R12$ general purpose, $R13$ Stack Pointer ($MSP/PSP$), $R14$ Link Register ($LR$), $R15$ Program Counter ($PC$), $xPSR$ Program Status Register.
- **Thumb-2 Instruction Set**: Blend of 16-bit and 32-bit instructions maximizing code density and performance.
- **CMSIS (Cortex Microcontroller Software Interface Standard)**:
  - CMSIS-Core: Standardized access to processor registers and peripherals.
  - CMSIS-DSP: Optimized matrix, FFT, FIR/IIR filtering utilizing Cortex-M4/M7 SIMD/FPU hardware.
  - CMSIS-RTOS2: Universal RTOS API layer.

## Tools & Standards
- **Standards**: Arm Architecture Reference Manual ARMv7-M / ARMv8-M.
- **Software**: CMSIS open-source library, OpenOCD, GDB.
