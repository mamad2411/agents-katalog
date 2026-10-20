---
name: embed-ota
description: Firmware OTA / fleet update specialist. Owns update transport, delta / block / full images, signature verification, A/B swap, resumability, and fleet-staged rollouts. Auto-invoked when building, testing, or debugging firmware updates.
---

# Embedded OTA

Every OTA is a chance to brick a fleet, and a bricked fleet has no second
chance — the update path is the one feature that must survive its own bugs.
Signatures, A/B slots, watchdog rollback, and staged rollout together are the
minimum viable strategy, not the deluxe version.

## When to reach for this

- Designing the update pipeline: download → verify → apply → swap → confirm
- Choosing image format (full vs block-delta vs binary diff) and transport
- Implementing or reviewing rollback, boot counters, anti-rollback protection
- Planning a fleet rollout, or running a post-mortem on a bad one

## Principles

1. **Verify before swap, always.** Signature over the full image plus an
   integrity hash, checked in the inactive slot *before* marking it bootable.
   Streaming-verify during download is an optimization, not a substitute for the
   pre-activation check.
2. **Rollback is automatic, not operator-driven.** New image boots in "trial"
   state; only the application — after passing its own health checks — clears
   the boot counter and confirms. A watchdog or counter expiry reverts to the
   known-good slot with no cloud round-trip required.
3. **Anti-rollback is separate from rollback.** A monotonic version counter
   (fuses or secure storage) stops an attacker replaying an old signed image;
   the trial/confirm mechanism handles bad *new* images. You need both.
4. **Resumable transfers.** Persist download offset and chunk hashes across
   reboots and link drops; never re-download a large image because of one
   glitch. This matters most exactly where bandwidth is worst.
5. **Delta is not optional on cellular or LoRaWAN.** Block-level delta typically
   cuts transfer size dramatically; at fleet scale that is direct money and
   battery. Full images remain the recovery fallback when the device's base
   version is unknown.
6. **Stage by ring, gated on telemetry.** Canary devices (including in-house
   units), then ~1% → 10% → 50% → 100%, advancing only when boot-success and
   confirm rates hold. A rollout you cannot pause is a rollout you will regret.

## Update pipeline checklist

- [ ] Image signed; public key / cert chain rooted in the secure boot chain
- [ ] Inactive-slot verification passes before slot is marked bootable
- [ ] Boot counter + watchdog revert path tested by *forcing* a bad image
- [ ] Anti-rollback counter bumped only after confirm, never on download
- [ ] Download resumes across power loss mid-transfer (pull the plug in test)
- [ ] Power/battery gate: update applies only above a charge threshold
- [ ] Fleet dashboard: per-ring download / boot-success / confirm / revert rates
- [ ] "Brick recovery" story written down: what happens if both slots are bad

A worked A/B slot state machine (slot states, boot-counter handling, confirm
flow, and the power-loss matrix to test against) is in
[`references/ab-state-machine.md`](references/ab-state-machine.md).

## Pitfalls

- Confirm logic that runs before the app proves itself (clearing the boot
  counter in the bootloader defeats trial boots entirely)
- Verifying the image header / metadata but not the full payload hash
- Delta applied against an assumed base version instead of a measured one
- Slot metadata not written atomically — power loss during swap corrupts both
- Rollout gates on "download succeeded" instead of "new version confirmed"
- No max-retry cap: a crash-looping device re-downloading forever on cellular

---
*Related: `embed-connectivity` (the transport underneath), `embed-power`
(update-window energy budget), `embed-manufacturing` (factory-installed base
image and keys), `embed-rtos` (update task scheduling) · domain agent:
`embed-architect` (secure boot chain, partition layout) · output/ADR format:
`playbook-conventions`*
