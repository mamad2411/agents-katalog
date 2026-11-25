---
name: esp32-security-and-provisioning
description: Use when an ESP32 product needs secure boot, flash encryption, per-device keys or a factory reset that actually erases secrets. Covers eFuse, the irreversible steps, and the order they must happen in.
license: MIT
---

# Security and provisioning on ESP32

Every step here is one-way. There is no "undo" for an eFuse bit, and a release-mode
device that fails to boot cannot be re-flashed. Treat this skill as a checklist to
follow on a spare board first, never on the only prototype.

## The three mechanisms

| Mechanism | What it protects | Reversible |
|---|---|---|
| Secure boot v2 | the firmware image - only signed images run | no |
| Flash encryption | the flash contents - reading it out gives ciphertext | no |
| NVS encryption | the key-value store, separately, with its own key partition | partition can be regenerated, eFuse cannot |

## Order matters

1. Generate the signing key and keep it **off** the build machine's default path.
2. Enable secure boot, build, and flash a device you are willing to lose.
3. Enable flash encryption in development mode first - it still allows a re-flash.
4. Only after the product is proven, switch to release mode.

Doing 3 before 2 means the bootloader verifies nothing. Doing 4 before 3 means you
cannot recover a board that fails to boot.

## Development versus release mode

Development mode keeps a UART download path open, so a mistake costs a re-flash.
Release mode closes it: the only way in is a signed OTA, which means the OTA path
must already work. Ship nothing in release mode that has not completed an OTA
update on a bench unit.

## Per-device keys

A single shared key across a production run is a single point of failure: one
extracted device compromises the fleet. Generate a key per device at provisioning
time and store it in an encrypted NVS partition, not in the firmware image.

## What to check afterwards

```
espefuse.py --port /dev/ttyUSB0 summary
```

It reports which eFuse blocks are burned. Read it before and after; the diff is
the only reliable record of what you changed.

## The factory reset problem

`nvs_flash_erase()` clears NVS. It does not clear the eFuse, and it does not
revoke a bond held by a phone. A "factory reset" that only erases NVS leaves the
device still trusted by every client that paired with it. If the product promises
a reset, say precisely what it erases.


## Security 2 SRP salt length and verifier integrity

ESP-IDF #19370 is an open, Reviewing report for ESP32-C5 rev v1.2 and ESP-IDF v6.0.2. It reports that esp_srp_gen_salt_verifier(..., 16, ...) can export a 15-byte minimal bignum when the random salt's leading byte is 0x00, while the API path retains a 16-byte length and computes the verifier over the short buffer. The wrapper returns the salt pointer without an actual length, so a caller copying 16 bytes can read one byte past the allocation; the resulting verifier then rejects the correct PoP with CREDENTIALS_MISMATCH. The reporter measured 11 affected results in 2,000 generations (about 1/256), not a universal failure rate for every target or release.

**Required invariant:** the allocated salt buffer, advertised length, bytes used to derive x and bytes provisioned to the client must be identical and exactly salt_len bytes. Preserve a leading zero when exporting a bignum; never copy salt_len bytes from an allocation whose size is only the minimal encoded length. Test leading-zero and non-leading-zero cases, independently recompute the SRP verifier from the exact provisioned salt, and run heap canaries or host sanitizers around the returned buffer. Treat a correct-PoP CREDENTIALS_MISMATCH as a server-side provisioning fault until the generated salt/verifier pair is verified; do not punish the user with lockout for a malformed pair.

The report is open and under review. No upstream fix is established; patch or backport only after validating the exact IDF commit and API ownership contract.

Primary report: https://github.com/espressif/esp-idf/issues/19370

## Rules for the agent

- Never enable secure boot or flash encryption in a change that also touches
  application logic. One irreversible step per change, verified on its own.
- Never commit a signing key, a `.pem`, or a generated `nvs_keys` partition.
- If a build fails after enabling either feature, suspect the signing step before
  the application code: a bad signature looks exactly like a bootloop.
