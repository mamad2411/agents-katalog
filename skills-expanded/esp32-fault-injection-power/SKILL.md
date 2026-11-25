---
name: esp32-fault-injection-power
description: Use when designing controlled power-interruption validation and recovery tests for ESP32 firmware and hardware.
license: MIT
---

# Fault Injection Power

## Purpose
Design safe, repeatable power-interruption experiments for ESP32 products. This skill does not authorize unsafe mains work or uncontrolled interruption of hazardous equipment.

## Required context
- Exact ESP32 SoC/module, board revision, schematic and power tree.
- Supply ratings, protection, stored energy, load and test fixture.
- Firmware state machine, persistent data and OTA/update behavior.
- Current limits, isolation requirements and approved lab procedure.

## Procedure
1. Define the hypothesis and exact interruption point before testing.
2. Use a current-limited, isolated low-voltage bench setup appropriate to the board.
3. Protect personnel and equipment; never probe exposed mains or bypass protection.
4. Identify persistent writes, NVS commits, filesystem operations, OTA transitions and actuator states.
5. Add fixture-controlled power interruption with timestamps and repeatable trigger conditions.
6. Capture serial logs, reset reason, supply waveform and resulting persistent state.
7. Repeat each case and compare recovery against explicit acceptance criteria.
8. Record fixture revision, instrument calibration, firmware hash and limitations.

## Domain checklist
- Verify brownout/reset behavior and ensure brownout detection is not disabled.
- Never invent GPIO capabilities or claim unsupported board-level behavior.
- Never disable brownout detection to conceal a power integrity fault.
- Check atomicity and recovery of persistent writes and OTA state.
- Verify outputs return to a defined safe state after restart.
- Check repeated resets cannot corrupt configuration or create boot loops.
- Separate fixture/software evidence from production power-integrity validation.

## Safety and security
- Never conduct uncontrolled tests on mains-powered or hazardous equipment.
- Never defeat isolation, current limiting or protective interlocks.
- Never treat an ESP32 as a safety-rated controller.
- A successful build does not prove power-fail resilience.

## Validation matrix
| Level | Evidence | Limitation |
|---|---|---|
| Static | State and persistence review | Cannot prove physical interruption behavior |
| Host | Recovery/state-machine tests | Does not model real rail collapse |
| Build | Pinned SDK/toolchain build | Does not prove power integrity |
| Hardware | Controlled fixture, waveform, logs and repeated trials | Applies only to tested setup |

## Deliverable
Provide test matrix, safe setup, interruption points, measured waveform, firmware hash, pass/fail results and residual risks.

## References
- ESP-IDF programming guide: https://docs.espressif.com/projects/esp-idf/en/stable/
- Espressif technical documents: https://www.espressif.com/en/support/documents/technical-documents
