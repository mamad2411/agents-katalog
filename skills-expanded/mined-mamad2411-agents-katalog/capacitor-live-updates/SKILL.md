---
name: capacitor-live-updates
description: Use when implementing or governing OTA live update delivery for CapacitorJS apps including update channel configuration, bundle verification, rollback triggers, staged rollout, and user-facing update UX patterns.
---

# Capacitor Live Updates

## Specialization

Design and govern over-the-air (OTA) live update pipelines for CapacitorJS apps with deterministic channel management, cryptographic bundle verification, rollback-safe promotion gates, and user-transparent update UX.

## Scope Boundaries

In scope:

- OTA update channel configuration (Ionic Appflow, Capacitor Updater, or self-hosted).
- Bundle signing and cryptographic verification at install time.
- Update check, download, and apply lifecycle management.
- Staged rollout percentages and channel promotion governance.
- Rollback trigger conditions and automatic revert behavior.
- User-facing update prompts, background update UX patterns, and forced-update policies.
- Live update interaction with App Store / Play Store binary versioning rules.

Out of scope:

- Store binary releases (see `capacitor-release-readiness`).
- CI pipeline signing for store artifacts (see `capacitor-ci-integration`).
- Push notification delivery mechanics (see `capacitor-native-apis`).

## Trigger Conditions

- A project is adding OTA live update capability for the first time.
- Update delivery is failing, rolling back unexpectedly, or not reaching target devices.
- A staged rollout channel promotion decision must be evidenced and governed.
- Security review identifies unsigned or unverified update bundle delivery.
- Store compliance for OTA update content scope must be validated.

## Inputs

- OTA provider in use or under evaluation (Ionic Appflow, `capacitor-updater` plugin, self-hosted).
- App binary version and native API surface freeze policy.
- Rollout strategy: immediate, percentage-staged, or opt-in.
- Rollback tolerance and acceptable error-rate threshold.
- Evaluation date in ISO format (`YYYY-MM-DD`).

## Required Outputs

- Update channel configuration with version pinning and promotion rules.
- Bundle verification strategy (signature, checksum, or provider-managed).
- Update lifecycle implementation: check, download, confirm, apply, and revert.
- Staged rollout plan with promotion gates and rollback triggers.
- User-facing update UX pattern (silent, prompted, or forced).
- Store compliance checklist for OTA content scope rules.

## Depth Modes

| Level | Intent | Stop Rule |
|---|---|---|
| L1 Orientation | Understand OTA update mechanics | Update check and apply flow works end-to-end |
| L2 Practical Delivery | Ship safe OTA updates | Channel, verification, and rollback are configured |
| L3 Staged Governance | Production-grade rollout control | Promotion gates, staged percentages, and triggers are enforced |
| L4 Expert Standardization | Reusable OTA operating model | Channel governance, verification policy, and rollback runbook are documented for cross-project use |

## Update Lifecycle Pattern

```typescript
import { CapacitorUpdater } from '@capgo/capacitor-updater';

// 1. Notify the updater that the app has launched successfully (prevents auto-revert)
await CapacitorUpdater.notifyAppReady();

// 2. Check for updates on resume or app start
const latest = await CapacitorUpdater.getLatest();
if (latest.url) {
  // 3. Download in background
  const bundle = await CapacitorUpdater.download({ url: latest.url, version: latest.version });

  // 4. Apply on next restart (or immediately for forced updates)
  await CapacitorUpdater.set(bundle);
}
```

- Always call `notifyAppReady()` after confirming the new bundle renders correctly.
- Never apply an update immediately without confirming the bundle is functional.
- Use `reset()` to revert to the bundled version when a critical defect is detected.

## Bundle Verification Rules

- Verify bundle integrity using provider-managed signatures or a self-computed checksum validated against a trusted manifest.
- Never apply a bundle downloaded from an untrusted or unvalidated URL.
- Validate bundle content scope: OTA updates must not replace native binary code, permissions, or plugin bridge implementations — only web layer assets.
- Store the verification result before applying; do not skip verification under poor network conditions.

## Staged Rollout Rules

- Start at ≤10% of devices for any new OTA version; monitor crash rate and error telemetry before expanding.
- Define an explicit promotion gate: metric threshold + minimum observation window.
- Rollback trigger must be automatic when crash rate exceeds the approved threshold.
- Staged percentage and promotion history must be durable artifacts, not inferred from chat or ticket history.

## Store Compliance Rules

- OTA updates may only deliver web layer changes (HTML, CSS, JavaScript).
- OTA must not change the app's core functionality, monetization model, or purpose beyond what is declared in the store listing.
- iOS App Store Review Guidelines §3.3.2 and Google Play Policy must be reviewed before every major OTA content change.
- Native plugin updates, new permissions, and native capability additions require a binary store release.

## Quality Gates

- `notifyAppReady()` is called on every successful app launch after an update is applied.
- Bundle verification is non-optional and runs before `set()` is called.
- Rollback revert path is tested before any production rollout begins.
- Staged rollout gate metrics are defined, monitored, and recorded as durable evidence.
- Store compliance checklist is completed for every OTA content change.

## Done Criteria

- Update lifecycle is implemented and smoke-tested on iOS and Android.
- Bundle verification is configured and passing.
- Staged rollout plan with promotion gates and rollback triggers is documented.
- Store compliance checklist is complete.
- Residual risks are explicit and owner-assigned.
