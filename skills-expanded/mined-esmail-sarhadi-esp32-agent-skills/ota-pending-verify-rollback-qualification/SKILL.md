---
name: ota-pending-verify-rollback-qualification
description: Use when new firmware boots once then rolls back, or an OTA update leaves devices in an update loop. Establish target-specific constraints, evidence, failure analysis and measurable verification before release.
license: MIT
version: "1.0.0"
---

# OTA PENDING VERIFY AND ROLLBACK QUALIFICATION

## Purpose and decision boundary

Treat OTA as a transactional state machine. The first boot of a new image is not success until application self-tests complete and the image is explicitly confirmed when rollback is enabled. This skill is an engineering workflow, not a substitute for the exact SoC datasheet, module documentation, board schematic, SDK release notes, protocol specification, safety assessment or measured evidence. It must not claim hardware validation from host tests or a successful compile.

Invoke this skill when the symptom or design change matches its trigger. First establish whether the issue is in scope. Record observations separately from hypotheses and confirmed causes. If the available evidence cannot distinguish competing explanations, say so and define the next measurement rather than guessing.

## Required inputs

Inspect OTA data partition, app slot sizes, rollback and anti-rollback settings, image state, secure version, bootloader config, watchdog/reset history and the exact point at which the app calls esp_ota_mark_app_valid_cancel_rollback().

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


### Confirmation after an uncertain otadata write

A failed or ambiguous persistent write must not be treated as a safe retry signal. ESP-IDF #19413 reports that on ESP32-C6 rev v0.2 with ESP-IDF v6.0.1 (the reporter also cites master commit de1e5035b5), the first esp_ota_mark_app_valid_cancel_rollback() call can erase the running image's active otadata sector and then fail while writing it. A retry reportedly returns ESP_OK after the previous application's valid record becomes the active record, even though the running image is not ESP_OTA_IMG_VALID and is no longer the next boot target. This is an open, target/version-specific report, not a claim about every release. The reporter found it by source inspection and has not observed it on a physical device; the proposed reproducer injects one failed otadata write through a linker wrapper.

**Defensive invariant after any failed or uncertain confirmation write:** do not accept a later ESP_OK by itself. Read back the running partition with esp_ota_get_state_partition(esp_ota_get_running_partition(), &state) and require state == ESP_OTA_IMG_VALID; also require esp_ota_get_boot_partition() == esp_ota_get_running_partition(). If either check fails or cannot be completed, keep the update unconfirmed, stop rollout promotion and preserve the previous recovery image. The readback is the reporter's proposed workaround pending maintainer resolution; qualify it against the exact IDF release and flash device before production use.

Primary report: https://github.com/espressif/esp-idf/issues/19413

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

Marking the image valid before verifying critical hardware can make a broken image permanent. Marking it valid too late can cause false rollback. Anti-rollback changes confirmation requirements and must be explicitly included.

### Evidence quality

Classify each statement as one of: **vendor-documented behavior**, **reproduced on the target**, **reported by an upstream issue**, **engineering hypothesis**, or **not yet tested**. For upstream reports, preserve issue number, affected version, board/revision and reporter's reproduction conditions. An issue being open or recently filed does not mean the reported root cause is confirmed.

### Recovery policy

Define what the firmware does when the condition persists: continue in degraded mode, retry with bounded backoff, isolate a peripheral, return to a safe output state, roll back an update or require service. Include a maximum retry/time budget and an observable diagnostic state. Avoid automatic reboot loops unless reset is the explicitly justified safety/recovery action.

## Verification plan

Test power loss during download, after image write, during first boot, before confirmation and after confirmation. Verify rollback to the previous image, data compatibility across versions and no bricking after repeated failures.

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

- https://docs.espressif.com/projects/esp-idf/en/latest/esp32/api-reference/system/ota.html
- https://github.com/espressif/esp-idf/blob/master/docs/en/api-reference/system/ota.rst
