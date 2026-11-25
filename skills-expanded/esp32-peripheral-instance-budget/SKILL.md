---
name: esp32-peripheral-instance-budget
description: Use when designing, reviewing, debugging or validating peripheral instance budget for ESP32 firmware; apply target-specific constraints, failure analysis and measurable verification before release.
license: MIT
version: "1.0.0"
---

# PERIPHERAL INSTANCE BUDGET

## Purpose and decision boundary

This skill treats **PERIPHERAL INSTANCE BUDGET** as a focused engineering activity in an ESP32 product. It supports design review, implementation planning, debugging and release verification. It is not a substitute for the exact target datasheet, board schematic, protocol specification, risk assessment or measured evidence.

Confirm exact SoC, silicon revision, module and board revision; review memory topology, boot straps, clocks, reset, RF layout and variant capabilities.

Invoke this skill when a change affects peripheral instance budget, its interfaces, resource budget, failure behavior or production acceptance criteria. Establish that the concern is in scope; do not invoke it merely because a project contains an ESP32.

## Required inputs

Collect the exact SoC ordering code and silicon revision; module and board revision; schematic; ESP-IDF or Arduino core version; compiler/toolchain version; sdkconfig and build flags; electrical interfaces and voltage domains; connected components; wiring length; protection and grounding assumptions; operating envelope; measurable requirements; fault response; recovery policy; and acceptance evidence.

Mark missing information **unknown**. Never substitute a typical ESP32 value or infer a board capability from a family name.

## Engineering model

### Scope to inspect

Chip/module mismatch, unavailable peripheral, flash/PSRAM wiring assumptions and boot failures caused by board differences.

Identify the owner of every resource and boundary: hardware, driver, task, protocol endpoint, persistent state and external system. Define units, valid ranges, timing assumptions and error semantics. Separate datasheet guarantees from typical values, application assumptions and measurements.

### Design procedure

1. **Freeze the target.** Confirm exact chip, module, board revision and framework version. Resolve family-specific differences before selecting APIs or pins.
2. **Translate requirements into limits.** State numerical limits with units, tolerance, operating conditions and pass/fail criteria. Replace vague terms such as fast, low-power and reliable with measurable requirements.
3. **Map dependencies.** Identify pins, clocks, DMA channels, memory regions, interrupts, tasks, buses, power rails, persistent records and external services.
4. **Analyze normal and abnormal paths.** Cover startup, steady state, overload, disconnect, timeout, reset, brownout, malformed input and recovery. Define safe behavior when a dependency disappears.
5. **Choose a bounded design.** Prefer explicit ownership, finite queues, bounded retries, deterministic timeouts and observable state transitions. Record rejected alternatives.
6. **Implement incrementally.** Keep hardware access behind a narrow driver boundary; validate configuration at startup; propagate errors instead of converting them to success.
7. **Verify independently.** Use static checks, unit tests, protocol vectors, build evidence and target measurements appropriate to each claim. Preserve setup and raw results.
8. **Review production behavior.** Check logging, secret handling, watchdogs, rollback/recovery, diagnostics and identification of deployed hardware and firmware.

## Constraints and invariants

- Freeze target identity; cross-check datasheet, technical reference manual, module datasheet and schematic; verify reset and boot waveforms.
- Treat reset, power loss, peripheral removal and communication loss as explicit states.
- Never assume a pin, peripheral, memory capability, clock source or feature is common across all ESP32 variants.
- Keep ISR work bounded; never perform blocking I/O, heap-heavy work or unbounded loops in interrupt context.
- Bound every queue, buffer, retry loop and timeout; define overflow and timeout actions.
- Preserve units and numeric ranges at interfaces. Validate untrusted values before allocation, indexing, arithmetic or hardware actuation.
- Do not disable brownout detection, watchdogs, authentication or integrity checks to hide a failure.
- Do not claim functional safety, electrical isolation, regulatory compliance or hardware validation without applicable evidence.

## Failure analysis

| Stimulus | Questions | Required evidence |
|---|---|---|
| Power-on / reset | Are outputs and shared pins defined before application code runs? | Reset waveform, pin levels and boot log |
| Resource exhaustion | What happens when memory, queue slots, sockets or descriptors run out? | Bounded-resource test and recovery trace |
| Invalid or delayed input | Are malformed, duplicated, stale and out-of-order values rejected safely? | Negative vectors and timeout test |
| Dependency loss | Can firmware detect and recover from bus, network, sensor or storage loss? | Disconnect/reconnect test |
| Repeated fault | Are retries bounded and free of reset or traffic storms? | Long-duration fault-injection run |
| Upgrade / configuration change | Can old and new state coexist or roll back safely? | Compatibility and interrupted-update test |

## Verification plan

Create a verification record containing requirement ID; design element; test ID; method; stimulus; expected and actual result; target board and SoC/module revision; firmware commit; toolchain version; instrumentation; calibration status; environmental conditions; units; pass/fail result; raw log or capture; deviations; and unresolved risks.

Use host-side deterministic tests for pure logic, target-side tests for MCU/peripheral behavior, and system/HIL tests for board-level interactions. A successful compile proves only that a build completed; it does not prove electrical correctness or field reliability.

## Deliverables

1. Design note stating assumptions, constraints and chosen approach.
2. Resource/interface map and configuration changes.
3. Implementation with explicit error handling and bounded behavior.
4. Positive, negative and recovery tests with reproducible fixtures.
5. Validation report separating simulated, host, target and hardware evidence.
6. Open-risk list and exact evidence needed to close each risk.

## Review checklist

- [ ] Target SoC, module, board and framework versions are explicit.
- [ ] Electrical and timing assumptions have sources or are labelled assumptions.
- [ ] Resource ownership and concurrency rules are documented.
- [ ] Startup, reset, brownout, disconnect and overload behavior are defined.
- [ ] Timeouts, retries, allocations and buffers are bounded.
- [ ] Invalid input and partial failure cannot cause unsafe actuation or memory corruption.
- [ ] Tests cover normal, boundary, negative and recovery behavior.
- [ ] Hardware claims are supported by measurements on the stated revision.
- [ ] Logs identify firmware commit, configuration and test setup.
- [ ] Remaining risks are visible; unverified results are never marked passed.

## References and source policy

Use official Espressif documentation for the exact target and framework:

- ESP-IDF Programming Guide: https://docs.espressif.com/projects/esp-idf/en/stable/esp32/
- ESP-IDF API Reference: https://docs.espressif.com/projects/esp-idf/en/stable/esp32/api-reference/
- Espressif technical documents: https://www.espressif.com/en/support/documents/technical-documents
- ESP-IDF releases: https://github.com/espressif/esp-idf/releases

For external components and protocols, prefer the manufacturer's datasheet and applicable protocol specification. Record document revision and access date. If an official source does not support a claim, state that limitation instead of inventing a register, pin capability or timing number.

## Repository integration

Use existing repository checkers only when they directly model the concern. Do not claim a checker validates a condition it does not encode. Add a checker only when its inputs, rules, units, failure codes and test vectors can be maintained independently of this prose.
