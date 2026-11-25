---
name: firmware
description: "Embedded C/C++, MISRA-C compliance, volatile qualifiers, bit manipulation, state machines (FSM), and circular ring buffers"
category: embedded
version: 1.0.0
disable-model-invocation: false
risk: low
source: "https://github.com/Mr-Nobody-Anonymous/All-skills"
source_repository: "Mr-Nobody-Anonymous/All-skills"
source_path: "awesome_skills/embedded/firmware/SKILL.md"
license: "MIT"
imported_at: "2026-09-20"
---

# Embedded Firmware Engineering

## Scope
Embedded firmware engineering writes deterministic, safe, resource-constrained C/C++ code executing directly on bare-metal hardware or real-time operating systems.

## Coding Standards & Invariants
- **MISRA-C Compliance (MISRA C:2012)**:
  - No dynamic memory allocation (`malloc`/`free`) after initialization.
  - Mandatory bounds checking on array indices.
  - Strict typing: use `stdint.h` explicit-width types (`uint8_t`, `int32_t`, etc.).
  - Avoid recursion and undefined behavior.
- **Keyword Discipline**:
  - `volatile`: Tells compiler variable can change outside program flow (hardware registers, ISR shared flags); prevents erroneous optimization.
  - `static`: Encapsulates variables and functions to file scope.
- **Core Data Structures**: Lock-free single-producer single-consumer (SPSC) circular ring buffers for interrupt-driven I/O.

## Tools & Standards
- **Standards**: MISRA C:2012, CERT C Embedded, BARR-C:2018.
- **Static Analysis**: PC-lint, Cppcheck, Clang-Tidy, SonarQube.
