---
name: hardware-debugging
description: "JTAG/SWD debugging, logic analyzers, digital storage oscilloscopes (DSO), serial decoders, and in-circuit emulation"
category: embedded
version: 1.0.0
disable-model-invocation: false
risk: low
source: "https://github.com/Mr-Nobody-Anonymous/All-skills"
source_repository: "Mr-Nobody-Anonymous/All-skills"
source_path: "awesome_skills/embedded/hardware-debugging/SKILL.md"
license: "MIT"
imported_at: "2026-09-20"
---

# Hardware Debugging & Bench Testing

## Scope
Hardware debugging combines protocol sniffers, oscilloscopes, logic analyzers, and in-circuit debuggers to isolate electrical, signal integrity, and firmware faults.

## Diagnostic Equipment & Procedures
- **Oscilloscope Techniques**: Bandwidth sizing ($5\times$ highest signal frequency), 10X passive probes (reduces capacitive loading), triggering (edge, pulse width, runt, I2C/SPI bus triggers).
- **Logic Analyzers**: Multi-channel digital capture, state vs. timing analysis, automated decoding of UART, SPI, I2C, CAN, and USB packets.
- **SWD / JTAG Debugging**: Setting hardware breakpoints, watchpoints, trace buffers (ETM, ITM via SWO pin), memory inspection without halting CPU.

## Tools & Standards
- **Hardware**: Saleae Logic, Segger J-Link, Rigol/Keysight DSOs, Bus Pirate.
