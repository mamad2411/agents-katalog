---
name: esp32-secure-ota-production
description: Use when designing production OTA, signed firmware delivery, rollback, anti-rollback, secure boot, flash encryption or fleet rollout.
license: MIT
---

# Secure Ota Production

OTA is a boot-chain and lifecycle feature, not just an HTTP download. A production update must authenticate the image, preserve a recoverable boot path and survive power loss at every write boundary.

## Image trust

Define the threat model: network attacker, compromised update server, physical access and downgrade attempts. Use supported Secure Boot and flash encryption according to platform lifecycle guidance; irreversible eFuse operations require explicit review. Authenticate firmware cryptographically before marking it bootable. A checksum detects corruption but does not authenticate the publisher.

## Partition and rollback design

Validate partition layout against actual flash size and bootloader requirements. Use A/B slots sized for the largest image plus growth. Define when a candidate image is marked valid; require health checks before confirmation. Configure rollback and anti-rollback deliberately because version counters and eFuse policy can make recovery impossible if mishandled.

## Transport and server

Use TLS with certificate validation and a trustworthy time/bootstrap strategy. Enforce image size, version, target chip, project identity and content type before writing. Authenticate devices and authorize update channels; browser-side checks are not device authentication. Support staged rollout, pause/abort, rate limits and per-device audit logs.

## Power-fail resilience

Test power removal during download, erase, write, verification, boot and confirmation. Keep the currently confirmed image intact until candidate verification completes. Avoid changing boot metadata before validation. Provide a factory recovery path matching the exact partition table and image type.

## Verification

| Fault | Required outcome |
|---|---|
| Truncated download | Candidate rejected; old image boots |
| Wrong chip/project image | Rejected before activation |
| Invalid signature | Rejected |
| Power loss during write | Recoverable boot path remains |
| New image crashes early | Rollback or recovery policy executes |
| Downgrade attempt | Policy enforced and logged |

## Agent rules

TLS alone does not make firmware updates trusted; image signatures are separate. Never assume factory image and OTA app image share a flash offset. Document key provisioning and irreversible eFuse steps. Require a tested recovery procedure before production rollout.

