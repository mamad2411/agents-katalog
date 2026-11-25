---
name: esp32-security-advisory-version-triage
description: Use when assessing whether an ESP32 firmware product is affected by a newly published ESP-IDF security advisory or parser vulnerability.
license: MIT
version: "1.0.0"
---

# ESP-IDF SECURITY ADVISORY VERSION TRIAGE

## Purpose and decision boundary

This skill defines a focused engineering review for esp-idf security advisory version triage in ESP32 firmware. It supports architecture, implementation review, incident response and release qualification. It does not replace the exact SoC datasheet, board schematic, ESP-IDF release notes or measured evidence. Treat unsupported assumptions as unknown.

Freeze the hardware/software tuple before diagnosis: SoC and silicon revision, module and board revision, ESP-IDF release or commit, compiler, sdkconfig, component lockfile and build flags. Preserve raw logs and reproduce the symptom before changing the system.

## Required inputs

- Exact chip, revision, module, board and peripheral part numbers.
- ESP-IDF version, compiler, sdkconfig and relevant configuration.
- Minimal reproducer, expected behavior, observed behavior and timestamped logs.
- Task, ISR, callback, buffer and resource ownership map.
- Power rail conditions, reset behavior, temperature, workload and instrumentation.
- Acceptance limits with units, tolerances and explicit pass/fail criteria.

Mark missing information unknown. Never infer capabilities from a generic ESP32 family name.

## Engineering model

Map advisory component, affected release branches, commit ranges, chip targets and configuration prerequisites to the exact product SBOM and build provenance. Distinguish reachable code from compiled-but-disabled components.

Model the feature as explicit states and transitions. For every transition identify owner, preconditions, side effects, timeout, cancellation behavior and recovery path. Make buffer lifetime and ownership explicit across tasks, callbacks, drivers and DMA. A pointer valid in one execution context may be invalid in another, especially across reset or cache-disabled intervals.

### Design and investigation sequence

1. Reproduce before modifying. Record target revision, firmware commit, configuration and stimulus.
2. Reduce the system. Disable unrelated workloads one at a time while retaining the failing path.
3. Enumerate competing hypotheses: software race, silicon behavior, driver regression, power integrity, memory capability, timing or external-device cause.
4. Inspect the exact API contract and matching release notes. Verify alignment, memory capability, callback context, timeout and lifecycle semantics.
5. Instrument the boundary with bounded counters and timestamps for state transitions, retries, queue depth and error codes.
6. Implement a bounded correction with explicit ownership, finite queues, validated inputs and deterministic error propagation.
7. Exercise reset, timeout, cancellation, power interruption, malformed input and resource exhaustion.
8. Qualify the exact release and keep unresolved risks visible.

## Constraints and invariants

- Never invent GPIO capabilities, peripheral availability, memory properties or timing guarantees for an unspecified SoC.
- Treat reset, power loss, brownout, watchdog escalation and interrupted updates as first-class states.
- Keep ISR work bounded; do not block, allocate unpredictably or call APIs not documented as ISR-safe.
- Validate buffer length, alignment, memory capability and lifetime before DMA, crypto, flash or asynchronous driver use.
- Define a single owner for mutable queues, buffers and lifecycle objects.
- Bound every queue, retry loop, timeout and allocation; specify behavior at the limit.
- Never disable brownout detection, watchdogs, authentication or integrity checks to conceal a failure.
- Never treat an ESP32 as a safety-rated controller; independent safety functions remain external.
- A successful build does not prove runtime correctness, RF performance, electrical integrity or field reliability.

## Failure analysis

| Failure mode | Diagnostic questions | Evidence |
|---|---|---|
| Timing-dependent failure | Does it correlate with load, interrupt rate or cache state? | Timestamped trace and repeat count |
| Memory corruption | Are alignment, capability and ownership correct? | Heap diagnostics, map file and canaries |
| Reset or brownout | Which reset source occurred and what state survived? | Reset reason, rail capture and boot log |
| Resource exhaustion | Can queues or descriptors become unbounded? | High-water marks and allocation counters |
| Version regression | Does the exact release or commit change the result? | Reproducible version matrix |
| Recovery failure | Can the system return to a known state? | Fault-injection and recovery trace |

A high-severity advisory does not automatically mean every product is exploitable, and an apparently unused feature is not proof of safety. Missing version provenance makes both false alarms and missed exposure likely.


### November 2026 advisory watch (checked 2026-11-11)

Match each advisory to exact component, configuration and commit: GHSA-49x8-xqjg-2pjg (ESP-TEE; C5/C6/C61/H2; affected v5.5.5, v6.0.3 and v6.1; v5.5.6 fixed, v6.0.4/v6.1.1 pending; no runtime workaround); GHSA-ch63-jxm5-vmvf (lwIP DNS; requires CONFIG_LWIP_DNS_MAX_HOST_IP > 1 and a multi-address cache hit; v5.2 is EOL); GHSA-rjvf-fxv5-x87j (Bluedroid BLE Mesh GATT with PB-GATT or GATT Proxy; NimBLE not affected); GHSA-c26h-gm53-qg83 (OpenThread Border Router only; requires CONFIG_OPENTHREAD_BORDER_ROUTER=y). Full per-branch affected/fixed ranges and commit IDs are maintained in docs/research/field-issue-patterns.md. Never merge version ranges across advisories or infer exposure from chip family alone.
## Verification plan

| Layer | Method | Pass/fail evidence |
|---|---|---|
| Static | Review call graph, memory sections, configuration and ownership | No undocumented context or lifecycle violation |
| Host | Deterministic state-machine, boundary and fault-sequence tests | Expected state and error contract for every vector |
| Build | Compile exact target and pinned configuration | Reproducible build and artifact hash |
| Hardware | Test stated board revision with appropriate probes and loads | Measured timing and signal behavior within limits |
| System | Soak and inject faults under concurrent load | Bounded recovery and no silent corruption |

Produce an affected/not-affected/unknown matrix with evidence, owner, remediation commit, regression test and release gate. Rebuild from pinned dependencies and preserve the resulting SBOM and artifact digest.

A test is not evidence unless target, setup, stimulus, expected result, actual result and raw artifact are recorded. Host tests cannot prove RF, DMA, power or electrical properties of a physical board.

## Deliverables

1. Target/version compatibility statement and unknown inputs.
2. State, resource and ownership model for the subsystem.
3. Root-cause analysis with competing hypotheses and evidence.
4. Minimal implementation change with bounded recovery behavior.
5. Positive, boundary, negative and fault-injection tests.
6. Validation report separating static, host, build, hardware and system evidence.
7. Residual-risk register with owner and closure evidence.

## Review checklist

- [ ] Exact SoC, revision, module, board and ESP-IDF commit are recorded.
- [ ] Unknown inputs are explicit; family-wide assumptions are avoided.
- [ ] State transitions, task/ISR context and buffer ownership are documented.
- [ ] Power, reset, timeout, cancellation and resource exhaustion are tested.
- [ ] Retries, queues, allocations and timeouts are bounded.
- [ ] No safety, watchdog, brownout or security control was disabled.
- [ ] Pass/fail limits include units and target conditions.
- [ ] Hardware claims have measurements on the stated revision.
- [ ] Raw evidence, firmware commit and unresolved risks accompany the result.

## References and source policy

Use the matching ESP-IDF Programming Guide: https://docs.espressif.com/projects/esp-idf/en/latest/esp32/ and Espressif technical documents: https://www.espressif.com/en/support/documents/technical-documents . Treat issue reports as leads for investigation, not universal guarantees. Record issue status, affected versions and whether the behavior reproduces locally.

Primary topic reference: https://github.com/espressif/esp-idf/security/advisories

When sources disagree, prefer the exact target datasheet and official release-specific documentation. Never copy a workaround without its target, version and limitations. Do not claim hardware validation when only a host test or successful compile exists.

## Repository integration

Use existing checkers only when their encoded rules directly cover the condition. Add a checker only when inputs, units, assumptions, failure codes and regression vectors can be maintained independently. Keep this skill focused and link adjacent skills rather than duplicating their procedures.
