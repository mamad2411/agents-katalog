---
name: esp32-mqtt-session-recovery
description: Use when reviewing or implementing esp32 mqtt session recovery on an ESP32 target., including target-specific constraints and repeatable validation steps.
license: MIT
---

# Esp32 Mqtt Session Recovery

## Purpose
A repeatable engineering method for esp32 mqtt session recovery on ESP32 products. This guidance does not replace exact SoC/module datasheets, board schematics, component datasheets, applicable standards or physical measurement.

## Required context
- Exact ESP32 SoC, module/package, board revision and schematic.
- Framework/toolchain and version (ESP-IDF, Arduino-ESP32 or PlatformIO).
- Component part numbers, wiring, electrical ratings and environment.
- Relevant source, configuration, logs, build artifacts and firmware revision.
- Product requirements, failure behavior, deployment constraints and test equipment.

## Procedure
1. Identify exact target, board, framework/toolchain versions and project configuration.
2. Read target-specific Espressif documentation, datasheets, errata and component documentation; record revision and applicability.
3. Inspect source, Kconfig/sdkconfig, partition table, board definitions and resolved dependency versions.
4. Map relevant constraints and budgets: pins, timing, CPU, stack, heap, flash, bandwidth, power, thermal and RF.
5. Analyze startup, reset, disconnect, malformed input, resource exhaustion, power loss and recovery paths.
6. Propose bounded changes with explicit ownership, range checks, timeouts, state transitions and observable errors.
7. Run relevant checkers, host tests and target builds; state what requires physical hardware.
8. Report findings with severity, evidence, affected conditions, mitigation, test results and residual uncertainty.

## Domain checklist
- Esp32 Mqtt Session Recovery: verify behavior against exact target and component revisions.
- Check normal operation, boundary values, invalid configuration and failure recovery.
- Check compatibility with the pinned SDK/framework and dependency graph.
- Record measurable budgets and margins; do not substitute estimates for measurements.
- Ensure logs identify failure causes without exposing credentials or private data.
- Separate silicon capability from module wiring and board-level implementation.

## Safety and security
- Never invent GPIO capabilities, voltage tolerance, radio limits, memory capacity or peripheral availability.
- Never disable brownout detection, watchdogs, TLS verification or security controls to hide a defect.
- Never treat an ESP32 as a safety-rated controller or replacement for independent protective hardware.
- Keep credentials, private keys and sensitive device telemetry out of source, logs and examples.
- Treat eFuse, secure-boot, flash-encryption and production provisioning as irreversible/human-approved operations.
- A successful build does not prove electrical, RF, EMC, thermal or field reliability.

## Validation matrix
| Level | Evidence | Limitation |
|---|---|---|
| Static | Source/configuration checks and cited constraints | Cannot prove runtime behavior |
| Host | Deterministic parser/state/budget tests | Does not emulate silicon or electrical behavior |
| Build | Pinned SDK/toolchain build and artifact metadata | Does not prove board wiring or peripheral operation |
| Hardware | Named board, wiring, instruments, conditions and logs | Applies only to tested configuration |

## Deliverable
Return target/version scope, confirmed facts and unknowns, ranked findings, evidence references, remediation, rollback considerations, exact commands and test outcomes, plus hardware-only validation still required.

## References
- ESP-IDF programming guide: https://docs.espressif.com/projects/esp-idf/en/stable/
- Espressif technical documents: https://www.espressif.com/en/support/documents/technical-documents
- ESP-IDF component registry: https://components.espressif.com/
