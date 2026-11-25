---
name: wifi-disconnect-reason-forensics
description: Use when wi-Fi station links drop, reconnect loops occur, or logs expose WIFI_REASON codes. Establish target-specific constraints, evidence, failure analysis and measurable verification before release.
license: MIT
version: "1.0.0"
---

# WIFI DISCONNECT REASON FORENSICS

## Purpose and decision boundary

Treat the disconnect reason as evidence, not as a root cause. Preserve the event sequence and distinguish scan failure, authentication, association, handshake, beacon loss, AP reset, DHCP/IP loss and application timeout. This skill is an engineering workflow, not a substitute for the exact SoC datasheet, module documentation, board schematic, SDK release notes, protocol specification, safety assessment or measured evidence. It must not claim hardware validation from host tests or a successful compile.

Invoke this skill when the symptom or design change matches its trigger. First establish whether the issue is in scope. Record observations separately from hypotheses and confirmed causes. If the available evidence cannot distinguish competing explanations, say so and define the next measurement rather than guessing.

## Required inputs

Capture WIFI_EVENT_STA_DISCONNECTED reason, RSSI, channel, BSSID, auth mode, retry count, AP model/firmware, country/channel policy, power-save setting, DHCP events and monotonic timestamps. Build a reason-code map from the exact ESP-IDF version headers; do not hard-code numeric meanings across releases.

Also collect the exact SoC ordering code and silicon revision; module and board revision; schematic; ESP-IDF or Arduino core version; compiler/toolchain version; sdkconfig and build flags; connected components; power and voltage domains; operating envelope; relevant logs; and a reproducible pass/fail requirement. Mark missing information **unknown**. Never infer pin capabilities, RF behavior, power limits or peripheral support from a family name alone.

## Engineering model

### Scope and ownership

Identify the owner of each relevant resource: hardware rail, GPIO, peripheral, interrupt, task, queue, DMA buffer, protocol endpoint, persistent record and external service. Define units, valid ranges, timing assumptions, error semantics and recovery authority. Distinguish vendor guarantees, issue-reporter observations, engineering hypotheses and measurements from the user's own target.

### Investigation procedure

1. **Freeze the configuration.** Capture board/SoC revision, SDK/toolchain versions, build flags, partition layout and relevant component versions. Preserve the failing binary and ELF where applicable.
2. **Preserve raw evidence.** Save complete logs, timestamps, waveforms, packet captures, reset reason and environmental conditions before clearing state or reflashing.
3. **Build a minimal reproducer.** Remove unrelated application code without changing the hardware, SDK or workload that triggers the symptom. Record every simplification.
4. **Separate hypotheses.** List plausible hardware, driver, application, protocol and environmental causes. For each, name a measurement or experiment that could falsify it.
5. **Measure the boundary.** Use a scope, logic analyzer, RF sniffer, current probe, packet capture or diagnostic counters as appropriate. State instrument bandwidth, probe point and uncertainty where relevant.
6. **Choose a bounded correction.** Prefer explicit state machines, finite timeouts, bounded retries, resource ownership and safe failure states. Avoid disabling protections or hiding errors.
7. **Verify independently.** Add host tests for deterministic logic, target tests for peripheral behavior and environmental tests for RF/power/thermal claims. Keep those evidence classes separate.
8. **Close the incident.** Record root cause confidence, workaround limitations, fixed version, regression test, deployment/rollback plan and residual risk.

## Constraints and invariants

- Never treat a community issue's workaround as a universal vendor recommendation.
- Do not disable brownout, watchdog, TLS verification, memory checks or protocol validation merely to make a symptom disappear.
- Do not erase NVS, repartition flash, change eFuses or alter bootloader security state without an approved data-loss and recovery plan.
- Do not drive actuators or external loads from GPIO without checking reset defaults, voltage domains and hardware protection.
- Keep ISRs and event callbacks bounded; do not block, allocate unpredictably or perform long logging in interrupt context.
- Use target-specific pin/peripheral maps. A value or API that works on classic ESP32 may not apply to S2/S3/C3/C6/H2/P4.
- Treat every missing specification as unknown and every unmeasured claim as unverified.
- Protect credentials, private keys, customer payloads and identifying telemetry in logs and crash records.

## Failure analysis

### Symptom-specific branches

NO_AP_FOUND, AUTH_FAIL, ASSOC_FAIL, HANDSHAKE_TIMEOUT, BEACON_TIMEOUT and IP loss require different branches. A generic immediate esp_restart() hides evidence and can amplify AP load. A password mismatch is not repaired by endless rapid retries.

### Evidence quality

Classify each statement as one of: **vendor-documented behavior**, **reproduced on the target**, **reported by an upstream issue**, **engineering hypothesis**, or **not yet tested**. For upstream reports, preserve issue number, affected version, board/revision and reporter's reproduction conditions. An issue being open or recently filed does not mean the reported root cause is confirmed.

### Recovery policy

Define what the firmware does when the condition persists: continue in degraded mode, retry with bounded backoff, isolate a peripheral, return to a safe output state, roll back an update or require service. Include a maximum retry/time budget and an observable diagnostic state. Avoid automatic reboot loops unless reset is the explicitly justified safety/recovery action.

## Verification plan

Assert that each reason maps to a classified state, retry delay is bounded, credentials are never logged, repeated events do not create duplicate handlers, and the application does not report online before IP acquisition. Validate with packet capture and AP logs on the target.

### Test layers

- **Host/unit:** state transitions, parsers, error classification, retry policy, bounds, serialization and persistence policy.
- **Build/configuration:** exact target, SDK version, sdkconfig, partition map, compiler warnings and generated artifacts.
- **On-target:** GPIO/peripheral timing, power, memory capabilities, radio behavior, wake sources and reset behavior.
- **System/field:** worst-case load, long-duration soak, environmental envelope, AP/device interoperability and recovery after faults.

For every test record setup, firmware hash, target revision, procedure, expected result, actual result and retained evidence. A passing host test is not hardware qualification.

## Deliverables

- Target and version manifest with unknowns explicitly listed.
- Symptom timeline and raw evidence bundle.
- Minimal reproducer or a clear explanation why one cannot be produced.
- Hypothesis table with evidence and confidence.
- Corrective change with bounded recovery behavior.
- Regression tests and target validation report.
- Residual-risk note and deployment/rollback instructions.

## Review checklist

- [ ] Exact SoC, module, board revision and SDK tuple are recorded.
- [ ] The original symptom and raw evidence are preserved.
- [ ] Root cause is distinguished from correlation and workaround.
- [ ] No target-family assumptions or undocumented pin capabilities are present.
- [ ] Retry, timeout, memory and queue bounds are explicit.
- [ ] Safety protections and TLS verification remain enabled.
- [ ] Host, build, target and field evidence are clearly separated.
- [ ] The fix has a reproducible regression test and recovery plan.
- [ ] Credentials and sensitive payloads are absent from logs.

## References and source policy

Use the exact vendor documentation for the selected target and SDK release first. The links below are starting points, not proof that a particular reported defect affects every release. Check issue status, maintainer comments and release notes before adopting a workaround.

- https://docs.espressif.com/projects/esp-idf/en/latest/esp32/api-guides/wifi.html
- https://github.com/espressif/esp-idf/issues/18702
- https://github.com/espressif/esp-idf/issues/13598
