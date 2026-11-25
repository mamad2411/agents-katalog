---
name: microcontrollers
description: "MCU architectures (Harvard/Von Neumann), memory maps, clock trees, GPIO, interrupts (NVIC), and peripheral registers"
category: embedded
version: 1.0.0
disable-model-invocation: false
risk: low
source: "https://github.com/Mr-Nobody-Anonymous/All-skills"
source_repository: "Mr-Nobody-Anonymous/All-skills"
source_path: "awesome_skills/embedded/microcontrollers/SKILL.md"
license: "MIT"
imported_at: "2026-09-20"
---

# Microcontroller Architectures

## Scope
Microcontroller engineering covers silicon-level MCU architecture, internal bus structures (AHB/APB), memory mapping, clock distribution trees, and low-level peripheral register programming.

## Architectural Foundations
- **Core Topologies**: Harvard (separate instruction/data buses, e.g., ARM Cortex-M, AVR) vs. Von Neumann (shared memory bus).
- **Memory Map Layout**: Flash (code/const), SRAM (stack/heap/.data/.bss), Memory-Mapped I/O Peripherals (registers mapped at fixed memory addresses).
- **Clock Distribution Tree**: Phase-Locked Loops (PLL), High-Speed Internal/External (HSI/HSE) oscillators, prescalers for core CPU and peripheral buses.
- **Nested Vectored Interrupt Controller (NVIC)**: Priority grouping, tail-chaining (latency reduction), interrupt service routine (ISR) entry/exit sequences.

## Tools & Standards
- **Toolchains**: GCC (`arm-none-eabi-gcc`), Clang/LLVM, Keil MDK, IAR Embedded Workbench.
- **Canonical References**: Yiu — *The Definitive Guide to ARM Cortex-M3 and Cortex-M4 Processors*.
