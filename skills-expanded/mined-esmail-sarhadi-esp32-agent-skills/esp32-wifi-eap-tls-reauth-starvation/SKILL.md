---
name: esp32-wifi-eap-tls-reauth-starvation
description: Use when investigating long Wi-Fi stalls or missed application deadlines during WPA2-Enterprise EAP-TLS reauthentication.
license: MIT
version: "1.0.0"
---

# WI-FI EAP TLS REAUTHENTICATION STARVATION

## Purpose and decision boundary
This skill defines a focused engineering review for wi-fi eap tls reauthentication starvation in ESP32 firmware. It is intended for architecture, implementation review, incident response and release qualification. It does not replace the exact SoC datasheet, module specification, board schematic, ESP-IDF release notes or measured evidence. Treat unsupported assumptions as **unknown**, not as defaults.

Invoke it when the symptom, change or risk intersects this boundary. First freeze the hardware/software tuple: SoC and silicon revision, module and board revision, memory configuration, ESP-IDF commit or release, compiler, sdkconfig, component lockfile and build flags. Record the exact reproduction conditions and preserve raw logs before changing the system.

## Required inputs
- Exact chip, revision, module, board and relevant external memory or peripheral part numbers.
- ESP-IDF version and commit, component versions, compiler, sdkconfig and partition table.
- Minimal reproducer, expected behavior, observed behavior, reset reason and complete timestamped logs.
- Relevant task, ISR, callback, buffer and resource ownership map.
- Power rail conditions, reset behavior, temperature, network or bus load and instrumentation setup.
- Acceptance limits with units, tolerances and explicit pass/fail criteria.

If an input is unavailable, label it **unknown** and identify the measurement or artifact needed to resolve it. Do not infer capabilities from the generic ESP32 family name.

## Engineering model
### Scope and invariants
Measure driver-task latency, handshake duration, certificate-chain cost, heap pressure and application deadline impact. Separate AP rejection, certificate validation, time synchronization and CPU scheduling hypotheses.

Model the feature as explicit states and transitions. For each transition, identify its owner, preconditions, side effects, timeout, cancellation behavior and recovery path. Make buffer lifetime and ownership explicit across tasks, callbacks, drivers and DMA. A pointer that is valid in one execution context may be invalid in another, especially across reset, cache-disabled intervals or asynchronous completion.

### Design and investigation sequence
1. **Reproduce before modifying.** Record the failing firmware commit, target revision, configuration and stimulus. Establish a baseline and preserve the original evidence.
2. **Reduce the system.** Disable unrelated workloads one at a time while retaining the failing path. Do not remove watchdogs, brownout protection, integrity checks or authentication to make the symptom disappear.
3. **Enumerate competing hypotheses.** Include software race, target-specific silicon behavior, driver regression, power integrity, memory capability, timing and external-device causes.
4. **Inspect the exact implementation contract.** Read the matching ESP-IDF API reference and release notes. Verify alignment, memory capability, callback context, timeout semantics and lifecycle requirements.
5. **Instrument the boundary.** Add counters and timestamps for state transitions, resource ownership, retries, queue depth and error codes. Keep instrumentation bounded and avoid changing timing more than necessary.
6. **Implement a bounded correction.** Use explicit ownership, finite queues, validated inputs, bounded retries and deterministic error propagation. Prefer a documented workaround or patched release over an undocumented timing hack.
7. **Exercise negative paths.** Include reset, timeout, cancellation, power interruption, malformed input, resource exhaustion and repeated recovery.
8. **Qualify the release.** Tie the result to the exact target and build provenance. Keep unresolved risks visible and do not label untested hardware behavior as passed.
## Constraints and invariants
- Never invent GPIO capabilities, peripheral availability, memory properties or timing guarantees for an unspecified SoC.
- Treat reset, power loss, brownout, watchdog escalation and interrupted updates as first-class states.
- Keep ISR work bounded; do not block, allocate unpredictably or call APIs that are not documented as ISR-safe.
- Validate buffer length, alignment, memory capability and lifetime before passing data to DMA, crypto, flash or asynchronous drivers.
- Define a single owner for each mutable queue, buffer and lifecycle object; document handoff and completion semantics.
- Bound every queue, retry loop, timeout and memory allocation. Specify the behavior when the bound is reached.
- Never disable brownout detection, watchdogs, authentication or integrity verification to conceal a failure.
- Never treat an ESP32 as a safety-rated controller. Independent safety functions must remain external and appropriately certified.
- A successful build does not prove runtime correctness, RF performance, electrical integrity or field reliability.

## Failure analysis
| Failure mode | Diagnostic questions | Evidence to retain |
|---|---|---|
| Timing-dependent failure | Does it correlate with callback order, load, interrupt rate or cache state? | Timestamped trace and repeat count |
| Memory corruption | Are alignment, capability, lifetime and ownership correct? | Heap diagnostics, map file and buffer canaries |
| Reset or brownout | Which reset source occurred and what state survived? | Reset reason, rail capture and boot log |
| Resource exhaustion | Can queues, descriptors, sockets or buffers reach an unbounded state? | High-water marks and allocation counters |
| Version-specific regression | Does the exact release/commit change the result? | Reproducible version matrix |
| Recovery failure | Can the system return to a known state without a power cycle? | Fault-injection and recovery trace |

An EAP-TLS reauthentication can occupy critical Wi-Fi processing for a substantial interval on a reported configuration. Application-level reconnect loops can amplify the outage and hide the original event.


### Duplicate EAP-TLS fragments and driver-task stalls
ESP-IDF #19408 reports an EAP-TLS reauthentication failure on ESP32-S3 and ESP32-C5 with development build v6.1-830-g0eddff3320f. In the reported OpenWrt/hostapd + RADIUS setup, a 1408-byte TLS message is reassembled and processed, then a retransmitted 424-byte EAP-TLS fragment is treated as new input rather than a duplicate request. The reassembly state is restarted, the supplicant asks for more input, and the AP rejects the exchange with WIFI_REASON_802_1X_AUTH_FAILED (reason 23). Reconnection with the same credentials reportedly succeeds. The reporter's trial patch to preserve cached responses, reject malformed TLS fragments and reset stale EAP state reportedly ran for more than 10 days, but it is not an upstream release fix.

A separate report, #19409, measures about 887 ms of Wi-Fi driver-task blocking during EAP-TLS reauthentication while wpa2_post() waits on s_wifi_wpa2_sync_sem even though TLS work is performed by wpa2T. The relationship between the duplicate-fragment failure and the long driver-task stall is not established; investigate them as separate hypotheses until a common cause is demonstrated.

Instrument EAP identifier, fragment flags, fragment length, reassembly offset, cached response identity, retry count and Wi-Fi task blocked duration. Test duplicate fragments, delayed retransmissions, partial-message timeouts and temporary EAPOL TX resource failures. Do not solve the symptom only by extending timeouts or weakening authentication.

Primary reports: https://github.com/espressif/esp-idf/issues/19408 and https://github.com/espressif/esp-idf/issues/19409

## Verification plan
Use a layered validation matrix and keep the evidence types separate:

| Layer | Method | Pass/fail evidence |
|---|---|---|
| Static | Review call graph, memory sections, configuration and resource ownership | No undocumented context, placement or lifecycle violation |
| Host | Deterministic state-machine, parser, boundary and fault-sequence tests | Expected state and error contract for every vector |
| Build | Compile the exact target and pinned ESP-IDF configuration | Reproducible build, warnings reviewed, artifact hash recorded |
| Hardware | Run on the stated board revision with appropriate probes and loads | Measured timing, reset, signal and resource behavior within limits |
| System | Soak and inject repeated faults under realistic concurrent load | Bounded recovery, no silent corruption, no unsafe output |

Capture event timestamps, reason codes, task runtime and heap snapshots. Test certificate renewal, AP roaming, clock drift and reauthentication under realistic load. Define degraded-mode behavior for the measured worst case.

A test is not evidence unless its target, setup, stimulus, expected result, actual result and raw artifact are recorded. A host test cannot prove a cache, RF, DMA, power or electrical property of the physical board.

## Deliverables
1. Target/version compatibility statement and list of unknown inputs.
2. State, resource and ownership model for the affected subsystem.
3. Root-cause analysis with competing hypotheses and evidence supporting or rejecting each.
4. Minimal implementation change with bounded error and recovery behavior.
5. Positive, boundary, negative and fault-injection tests with reproducible vectors.
6. Validation report separating static, host, build, hardware and system evidence.
7. Residual-risk register with owner, severity and evidence required for closure.

## Review checklist
- [ ] Exact SoC, silicon revision, module, board and ESP-IDF commit are recorded.
- [ ] Unknown inputs are explicit; no family-wide assumptions are presented as facts.
- [ ] State transitions, task/ISR context and buffer ownership are documented.
- [ ] Power, reset, timeout, cancellation and resource exhaustion are tested.
- [ ] Alignment and memory capability are verified for every relevant buffer.
- [ ] Retries, queues, allocations and timeouts are bounded.
- [ ] No safety, watchdog, brownout or security control was disabled to hide a defect.
- [ ] Pass/fail limits include units and target conditions.
- [ ] Hardware claims have measurements on the stated revision.
- [ ] Raw evidence, firmware commit and unresolved risks accompany the result.

## References and source policy
Start with the official ESP-IDF Programming Guide for the matching release: https://docs.espressif.com/projects/esp-idf/en/latest/esp32/ . Check the matching API reference, release notes and Espressif technical documents: https://www.espressif.com/en/support/documents/technical-documents . For issue-specific behavior, use the upstream report as a lead, not as a universal guarantee. Record issue status, affected versions and whether the behavior is reproduced locally.

Primary topic reference: https://github.com/espressif/esp-idf/issues/19409

When sources disagree, prefer the exact target datasheet and official release-specific documentation. Never copy a workaround without recording its target, version and limitations. Do not claim hardware validation when only a host test or successful compile exists.

## Repository integration
Use existing checkers only when their encoded rules directly cover the condition. Add a checker only when inputs, units, target assumptions, failure codes and regression vectors can be maintained independently. Keep the skill focused on this failure class and link adjacent skills rather than duplicating their entire procedures.
