---
name: avr
description: "8-bit AVR microcontrollers (ATmega328P, ATtiny), register manipulation, timers/counters, EEPROM, and low-power sleep modes"
category: embedded
version: 1.0.0
disable-model-invocation: false
risk: low
source: "https://github.com/Mr-Nobody-Anonymous/All-skills"
source_repository: "Mr-Nobody-Anonymous/All-skills"
source_path: "awesome_skills/embedded/avr/SKILL.md"
license: "MIT"
imported_at: "2026-09-20"
---

# AVR Microcontrollers

## Scope
8-bit AVR microcontroller engineering, register-level C programming, hardware timers, analog comparators, EEPROM endurance, and power reduction techniques.

## Core Features & Hardware
- **Register Architecture**: 32 8-bit general purpose registers ($R0-R31$), with $X (R26:R27), Y (R28:R29), Z (R30:R31)$ 16-bit pointer registers.
- **Timer/Counters**: CTC (Clear Timer on Compare Match), Fast PWM, Phase-Correct PWM.
- **Fuses & Lock Bits**: Clock selection, Brown-Out Detection (BOD) level, Watchdog timer, Bootloader size.

## Tools & Standards
- **Toolchains**: `avr-gcc`, `avrdude`, Microchip Studio.
- **Canonical References**: Barnett, Cox & O'Cull — *Embedded C Programming and the Atmel AVR*.
