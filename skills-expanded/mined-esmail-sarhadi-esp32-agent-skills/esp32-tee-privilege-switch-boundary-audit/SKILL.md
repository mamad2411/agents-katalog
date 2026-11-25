---
name: esp32-tee-privilege-switch-boundary-audit
description: Use when auditing ESP-TEE secure-service trap entry, REE/TEE stack separation or privilege-switch pointer validation on supported ESP32 RISC-V targets.
license: MIT
version: "1.0.0"
---

# ESP-TEE PRIVILEGE-SWITCH BOUNDARY AUDIT

## Purpose and decision boundary

Review the trust boundary between the Rich Execution Environment (REE) and the Trusted Execution Environment (TEE). This skill applies only to SoCs and builds that actually support and include ESP-TEE; it is not a generic ESP32 stack review. The advisory scope names ESP32-C5, ESP32-C6, ESP32-C61 and ESP32-H2.

The reported attack requires local code execution in the REE. It is not, by itself, a remote network entry point. A product is not affected merely because it uses one of the listed chips: establish that the relevant ESP-TEE component and secure-service trap path are present and reachable.

## Required inputs

- Exact SoC, silicon revision, module, board and security configuration.
- ESP-IDF release, branch, commit and resolved component revisions.
- Build system, compiler, sdkconfig, generated configuration, map file and SBOM.
- Whether ESP-TEE is included, which secure services are exposed and whether PLIC or CLIC trap entry is built.
- TEE-exclusive memory ranges, REE address ranges, stack bounds, stack alignment and interrupt configuration.
- Boot mode, secure-boot state, debug policy, source diff, firmware hash and a non-production test image.

Mark unavailable inputs unknown. Do not assume that an application uses ESP-TEE just because its target supports it.

## Engineering model

### Trust and control-flow boundary

The REE application runs with less privilege than the TEE. ESP-TEE handles secure-service calls through a RISC-V machine-mode trap entry. The incoming REE stack pointer is caller-controlled input until it has been validated. Saving a register frame through that pointer before switching to a trusted TEE stack crosses the privilege boundary with an untrusted address.

Audit both the user ecall path and the interrupt entry path. A fix in only one path is incomplete. Validate the entire register-save frame, not merely the starting pointer, before any store through the supplied pointer.

### Advisory evidence and version scope

Espressif advisory GHSA-49x8-xqjg-2pjg, CVE-2026-113780, was published 2026-10-27 with Critical severity (CVSS 9.3). The trap entry reportedly saved caller context through an REE-supplied stack pointer before validating it. A pointer into TEE-exclusive memory could therefore cause an M-mode write into the trusted region, with possible TEE memory corruption, denial of service or escalation to code execution in the TEE.

| ESP-IDF line | Affected release reported | Fixed release / commit |
|---|---|---|
| v5.5 | v5.5.5 | v5.5.6 / dabd37f |
| v6.0 | v6.0.3 | v6.0.4 / b85a7b0 |
| v6.1 | v6.1 | v6.1.1 / 773761a |
| master | Check exact ancestry | acb7d99 |

As of 2026-11-11, the advisory identifies v5.5.6 as released; v6.0.4 and v6.1.1 were listed as not yet released. Recheck the official release feed before making a deployment decision. The affected SoC families named by the advisory are ESP32-C5, ESP32-C6, ESP32-C61 and ESP32-H2.
## Design and investigation sequence

1. Freeze the exact SoC, silicon revision, IDF commit, component graph and generated configuration.
2. Establish whether ESP-TEE is built and whether the secure-service ecall or interrupt path is reachable in the shipped image.
3. Compare the exact source commit with the branch-specific fix. Do not infer a fix from a major/minor version label.
4. Inspect both PLIC and CLIC entry paths where applicable. Trace the first memory store after trap entry.
5. Confirm that pointer validation occurs before any save through the untrusted pointer and that the full frame is checked.
6. For an affected downstream branch, use the vendor fix commit or a fixed release; review and test the backport rather than copying a partial code fragment.
7. Build the exact target and retain the ELF, map, sdkconfig, component lock and firmware digest.
8. Record residual risk and the exact evidence required for release approval.

## Constraints and invariants

- Never dereference or write through an REE-supplied stack pointer before validating it.
- Use overflow-safe range arithmetic; reject wraparound, misalignment and a frame that crosses a permitted boundary.
- Validate the entire frame against the allowed REE stack region and ensure it cannot overlap TEE-exclusive memory.
- Apply the same rule to user ecall and interrupt entry paths.
- Invalid pointers must fail closed through a trusted path; do not fall back to saving context on the untrusted stack.
- Do not expose TEE memory, private keys, secure-service arguments or production crash dumps in logs.
- Do not change eFuses, production keys or secure-boot state as part of an unreviewed debugging experiment.
- There is no runtime workaround for the reported vulnerability. Disabling an application feature is not equivalent to repairing the trap boundary.

## Failure analysis

| Condition | Expected security consequence | Evidence to collect |
|---|---|---|
| Caller SP points into TEE memory | Potential M-mode write across the isolation boundary | Static trace of validation before first store |
| Save frame wraps address space | Range check may be bypassed if arithmetic is unchecked | Boundary and integer-overflow tests |
| Only ecall path is fixed | Interrupt entry may retain the same primitive | Separate audit of both entry paths |
| ESP-TEE is absent or unreachable | This advisory path may not be exposed | Build graph, map file and call-path evidence |
| Version label appears fixed but commit is absent | Product may remain vulnerable | Commit ancestry and source diff |

Do not claim exploitability for a product until component presence, configuration, call path and exact commit have been matched. Conversely, do not mark a product safe merely because no crash has been observed.

## Verification plan

- Static: inspect assembly and source for both entry paths; prove pointer validation precedes the first context store.
- Host/unit: exercise valid, misaligned, out-of-range, TEE-overlap and arithmetic-wrap pointer values using a test model of the range check.
- Build: compile the exact SoC and configuration; retain generated configuration, map and artifact hashes.
- Target: use a disposable board and test-only TEE image to verify rejection behavior without production secrets or irreversible provisioning.
- System: repeat secure-service and interrupt entry tests under the shipped configuration and retain trace evidence.

Host tests validate range logic only; they do not prove trap-entry assembly, silicon behavior or TEE isolation on a physical chip.

## Deliverables

1. Affected/not-affected/unknown matrix by SoC, IDF commit, component presence and configuration.
2. Source-level proof for both trap entry paths.
3. Fixed commit or release evidence and backport review.
4. Static, host, build and target test records with firmware hashes.
5. Residual-risk statement and release/rollback decision.

## Review checklist

- [ ] Exact SoC, silicon revision, IDF commit and ESP-TEE component presence are recorded.
- [ ] REE and TEE memory ranges and stack bounds come from the actual build.
- [ ] The entire caller frame is validated before any write through the supplied pointer.
- [ ] Both user ecall and interrupt entry paths are covered.
- [ ] Address arithmetic is overflow-safe and alignment is checked.
- [ ] No runtime workaround is presented as a security fix.
- [ ] No production key, eFuse or TEE memory is exposed during testing.
- [ ] Hardware claims are backed by a named target and retained evidence.

## References and source policy

- Espressif advisory GHSA-49x8-xqjg-2pjg: https://github.com/espressif/esp-idf/security/advisories/GHSA-49x8-xqjg-2pjg
- ESP-IDF fix on master: https://github.com/espressif/esp-idf/commit/acb7d996b07293abf591b93f4aaffa04ae6732d9
- ESP-IDF fix on release/v6.1: https://github.com/espressif/esp-idf/commit/773761abb893d43d0a5b8b75ec0a1c2cf0287d53
- ESP-IDF fix on release/v6.0: https://github.com/espressif/esp-idf/commit/b85a7b0e1449ac9aec30a0c3e3b6515725556fd1
- ESP-IDF fix on release/v5.5: https://github.com/espressif/esp-idf/commit/dabd37fae8d2a7b1cc71f48fce824b0b9d909a07
- ESP-TEE architecture overview: https://developer.espressif.com/blog/2025/02/announcing-esp-tee/

Use the advisory and exact branch commits as primary evidence. Recheck release status and source ancestry on the date of deployment.
