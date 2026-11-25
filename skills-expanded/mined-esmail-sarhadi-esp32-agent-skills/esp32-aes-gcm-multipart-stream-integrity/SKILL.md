---
name: esp32-aes-gcm-multipart-stream-integrity
description: Use when a firmware uses PSA AEAD or mbedTLS GCM multipart updates and chunk boundaries can be non-block-aligned.
license: MIT
version: "1.0.0"
---

# AES-GCM MULTIPART STREAM INTEGRITY

## Purpose and decision boundary

Treat AES-GCM multipart processing as one continuous authenticated stream, not as independent block-aligned calls. Invoke this skill when firmware uses psa_aead_update(), mbedtls_gcm_update(), BLE/HTTP/serial OTA decryption, or another chunked GCM path backed by the ESP-IDF hardware AES implementation. This workflow does not replace the cryptographic API contract, exact ESP-IDF source or independent test vectors.

The trigger is especially important for ESP-IDF release/v5.5: issue #19406 reports deterministic plaintext and tag corruption when one or more update lengths are not multiples of the 16-byte AES block size with CONFIG_MBEDTLS_HARDWARE_AES=y. The report reproduces on ESP32-C6 and classic ESP32 and claims the defect is reachable on any target using that hardware AES path. Treat that scope as issue evidence, not a universal claim for every chip or configuration.

## Required inputs

- Exact SoC, silicon revision, module, board and external flash/PSRAM configuration.
- ESP-IDF tag, branch and commit; compiler; component lockfile; sdkconfig; and whether CONFIG_MBEDTLS_HARDWARE_AES / MBEDTLS_GCM_ALT are enabled.
- API path (PSA Crypto or mbedTLS), encrypt/decrypt direction, nonce, AAD, tag length and key type.
- Chunk-size sequence, total payload length, buffer lifetime/ownership and whether plaintext is consumed before final authentication.
- Known-answer vectors, expected ciphertext/tag, observed plaintext/tag and complete error codes.

Mark missing version or configuration data unknown. Do not infer hardware-AES selection from the chip family alone; inspect the generated configuration and linked implementation.

## Engineering model

GCM combines counter-mode encryption (GCTR) with GHASH authentication. Multipart calls must preserve the same stream state across every update boundary. In particular, the implementation must retain the counter offset, unused keystream bytes and any partial GHASH block until the logical message ends. A partial block at the end of an intermediate update is not the final block of the message.

### Version-scoped incident evidence

ESP-IDF #19406 reports that the v5.5 hardware path initializes nc_off, nonce_counter and stream as function-local state on each esp_aes_gcm_update() call, while carrying only the updated counter forward. The reporter also found that GHASH zero-pads a partial tail on each call rather than buffering it until the final message block. A 381-byte chunk (23 × 16 + 13) therefore fails while an aligned 368-byte control chunk passes. The issue was filed against release/v5.5 and all v5.5.x tags; its status and branch contents must be rechecked before release.

The reporter identifies fix commits e6ac065424 on master, 8767271843 on release/v6.0 and 613469ffe7 on release/v6.1. These commits preserve the partial CTR and GHASH state in the GCM context. Verify that the exact commit is present in the branch actually used; do not assume a later tag or a v5.5 backport contains it without checking ancestry and source.

For a confirmed affected v5.5 build, the reporter's temporary mitigations are to buffer intermediate updates to multiples of 16 bytes and flush the final remainder only before finish, or to disable CONFIG_MBEDTLS_HARDWARE_AES so the software GCM path is selected. These are release-specific workarounds: verify the selected backend, measure timing and energy, retain mandatory final-tag verification, and prefer the backported fix.

### Investigation sequence

1. Freeze the exact IDF tag/commit and generated Kconfig. Record whether the hardware AES alternate implementation is linked.
2. Build a minimal one-shot encrypt plus multipart decrypt reproducer using a deterministic key, nonce, AAD and payload.
3. Run the same ciphertext through multiple chunk schedules, including 1, 15, 16, 17, 31, 368 and 381 bytes, plus randomized splits.
4. Compare plaintext byte-for-byte and verify the final GCM tag. Preserve the first mismatch offset and the exact update sequence.
5. Inspect the selected implementation for state carried across calls: counter offset, keystream remainder and partial GHASH buffering.
6. Compare the source with the relevant fix commit and test the exact target/IDF branch before selecting a mitigation.

## Constraints and invariants

- Never treat a successful update call as proof that the complete GCM message authenticated.
- Do not release, execute, install or persist decrypted plaintext as trusted data until final tag verification succeeds. Stage output in a bounded inactive slot or buffer and discard it on authentication failure.
- Do not use block-aligned chunk sizes as the sole fix; alignment can hide a lost-state defect without restoring the streaming contract.
- Do not disable authentication, tag checking, flash encryption or other security controls to make the transfer complete.
- Bound chunk size, total message length, staging storage, retries and timeouts. Validate output capacity before every update.
- Preserve a single owner for the GCM operation context; concurrent update/final calls on one context are not permitted unless the API explicitly guarantees them.
- Keep key material and plaintext out of logs and crash dumps.
- Never disable brownout detection or watchdog protection to mask a transfer failure.
- Never treat an ESP32 as a safety-rated controller; independent safety functions remain external.
- A successful build does not prove cryptographic correctness or hardware qualification.

## Failure analysis

| Symptom | Likely boundary to inspect | Evidence |
|---|---|---|
| Tag fails only for irregular chunk sizes | Lost CTR offset or GHASH partial-block state | Chunk schedule and final PSA/mbedTLS status |
| Plaintext diverges after a partial block | Keystream remainder or counter offset reset | First differing byte and per-update lengths |
| Aligned chunks pass but arbitrary chunks fail | Streaming state is not preserved across calls | 368-byte control versus 381-byte reproducer |
| OTA counts match but image authentication fails | Payload bytes may be wrong despite complete transport | Received length, plaintext hash and GCM tag |
| Plaintext is acted on before finish | Application commits unauthenticated output | Staging/commit path and negative-tag test |

Do not attribute every GCM failure to this report. Invalid nonce/AAD, tag truncation, buffer overlap, output sizing, key configuration and transport corruption remain competing hypotheses.

## Verification plan

| Layer | Method | Pass/fail evidence |
|---|---|---|
| Static | Inspect exact linked GCM implementation and context fields | Partial CTR/GHASH state survives every update |
| Host | Known-answer vectors with varied chunk boundaries | Identical plaintext and valid tag for every split |
| Negative | Flip ciphertext, AAD, nonce or tag; truncate input | Final authentication fails and staged plaintext is discarded |
| Build | Compile exact target/configuration and inspect component versions | Reproducible build and recorded commit/configuration |
| Hardware | Run on the exact SoC/module and hardware-AES configuration | Same vectors pass under repeated transfer and reset tests |
| System | Exercise interrupted OTA, low storage and retry paths | No partial image is activated and previous image remains bootable |

A minimum regression set includes a 381-byte failing-shape vector, a 368-byte aligned control, one-byte updates, splits immediately before/after a block boundary, randomized chunk schedules, corrupted tags and power loss before final authentication. Host vectors do not prove the selected hardware AES path is correct.

## Deliverables

1. Target/version/configuration matrix showing whether the affected hardware path is selected.
2. Minimal reproducer and deterministic vectors with exact chunk schedules.
3. Source-level state analysis for CTR offset, keystream remainder and GHASH buffering.
4. Affected/fixed commit assessment tied to the actual branch and build provenance.
5. Regression results for aligned, non-aligned, randomized and invalid-tag inputs.
6. A safe staging/commit design and residual-risk note for OTA or other consumers.

## Review checklist

- [ ] Exact target, IDF commit, sdkconfig and linked AES/GCM implementation are recorded.
- [ ] Arbitrary update boundaries preserve counter and GHASH state.
- [ ] Both 381-byte and 368-byte reproducer paths are tested.
- [ ] Final tag verification gates every use of decrypted plaintext.
- [ ] Invalid tags, truncation, interruption and output exhaustion fail closed.
- [ ] Fix commits are verified in the selected branch, not inferred from a version label.
- [ ] No security control was disabled to obtain a passing transfer.
- [ ] Hardware results identify board revision, setup, firmware hash and raw evidence.

## References and source policy

- ESP-IDF issue report #19406: https://github.com/espressif/esp-idf/issues/19406
- Master fix: https://github.com/espressif/esp-idf/commit/e6ac0654240a1071593473131b5f497000c52306
- v6.0 fix: https://github.com/espressif/esp-idf/commit/8767271843990026e1e8768a6a14fbee753d4f9b
- v6.1 fix: https://github.com/espressif/esp-idf/commit/613469ffe7fc141d0bcd40f7c9c353b5b361e33d
- v5.5 implementation: https://github.com/espressif/esp-idf/blob/release/v5.5/components/mbedtls/port/aes/esp_aes_gcm.c
- ESP-IDF v5.5 Programming Guide: https://docs.espressif.com/projects/esp-idf/en/v5.5/esp32/

The issue is a reporter-submitted, version-scoped defect report. Recheck maintainer status, release notes and commit ancestry before declaring a branch affected or fixed. Never claim hardware validation from a source diff or host-only vector run.
