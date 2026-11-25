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

## Rules for the agent

- Never enable secure boot or flash encryption in a change that also touches
  application logic. One irreversible step per change, verified on its own.
- Never commit a signing key, a `.pem`, or a generated `nvs_keys` partition.
- If a build fails after enabling either feature, suspect the signing step before
  the application code: a bad signature looks exactly like a bootloop.
