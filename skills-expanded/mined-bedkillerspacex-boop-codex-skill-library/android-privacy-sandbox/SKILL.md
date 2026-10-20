---
name: android-privacy-sandbox
description: >
  Android Privacy Sandbox awareness for owned apps and ads stacks: Topics, Protected
  Audience / FLEDGE-era APIs, Attribution Reporting, SDK Runtime notes, and migration off
  third-party cookies/IDs. Use when product/ads engineering must adapt to Privacy Sandbox
  on Android — not for fingerprinting users to evade privacy controls.
---

# Android Privacy Sandbox

## Scope And Authorization

- **In scope:** Apps, ads SDKs, and measurement stacks you operate, within platform policies.
- **Out of scope:** Building cross-app tracking that violates Play policy or user expectations; reverse-engineering others’ ad accounts without authorization.
- Coordinate with legal/privacy for advertising features.
- Pair engineering with `code-quality-standards`.

## When To Use

- Migrating measurement from GAID-heavy flows toward Privacy Sandbox APIs.
- Integrating Topics / Attribution Reporting / Protected Audience (names evolve).
- Reviewing ads SDK surface under SDK Runtime constraints.
- Product impact analysis when third-party cookies/IDs deprecate further.

## Do Not Use As Primary

| Need | Skill instead |
| --- | --- |
| General app privacy permissions | photo/health picker skills as relevant |
| Mobile pentest | `android-pentesting-tricks` |
| Web Privacy Sandbox only | web privacy skills if present in catalog |
| Implementation quality baseline | `code-quality-standards` |

## Domain Focus

| API / concept | Purpose (high level) |
| --- | --- |
| Topics API | Coarse interest signals without cross-site identifiers |
| Attribution Reporting | Conversion measurement with delayed/noisy reports |
| Protected Audience | Remarketing-like on-device auctions (API names evolve) |
| SDK Runtime | Isolate ads SDKs; restricted permissions/comms |
| GAID / LAT | Legacy advertising ID; user opt-out must be honored |
| Consent | Regional consent UX still required where law applies |

**Note:** Privacy Sandbox APIs and timelines change — verify current Android developer docs for your target API level.

## Workflow

### 1. Confirm product goals and success criteria

1. Record ads stack (mediation, MMP, in-house), regions, data currently collected.
2. Success: policy-compliant measurement path; GAID use minimized/justified; sandbox APIs behind feature flags; privacy review signed.
3. Inventory SDKs that access advertising ID.

### 2. Inventory current tracking

```bash
rg -n "AdvertisingIdClient|getId\\(|AD_ID|com.google.android.gms.ads" -S .
# Manifest
rg -n "AD_ID|com.google.android.gms.permission.AD_ID" app/src/main/AndroidManifest.xml
```

1. Note data shared with each partner.
2. Map user controls (opt-out, delete).

### 3. Plan Privacy Sandbox adoption

| Need | Prefer |
| --- | --- |
| Aggregate interest | Topics (where available) |
| Conversion lift | Attribution Reporting |
| Remarketing-like | Protected Audience with on-device auction |
| Legacy | Time-boxed GAID with LAT respect |

1. Feature-flag all new APIs.
2. Keep server aggregation privacy-preserving (no re-identification attempts).

### 4. Integration hygiene

```kotlin
// Conceptual — follow current Play services / AdServices APIs for your version
// - Declare permissions/services required by AdServices
// - Request measurement registration URLs only to owned endpoints
// - Handle API unavailability gracefully
```

1. Use debug enrollment only on test devices.
2. Validate origin allowlists for attribution sources/triggers.

### 5. SDK Runtime / ads isolation notes

1. Prefer ads SDKs that support Privacy Sandbox / runtime isolation guidance.
2. Reduce custom WebView-based trackers.
3. Audit IPC between app and ads processes for unexpected PII.

### 6. Verify compliance behaviors

```bash
# User limit ad tracking / delete advertising ID — ensure revenue path degrades, not crashes
adb shell settings get global limit_ad_tracking
# Manual QA: opt-out paths, consent rejection, child-directed modes if applicable
```

1. Confirm no shadow profiling via device fingerprint when ID unavailable (policy risk).
2. Log analysis: no accidental PII in ads debug logs.

### 7. Hand off

1. Privacy design doc: data flows, retention, legal bases.
2. Partner contracts updated for new measurement.
3. Monitor Play policy announcements quarterly.

## Good / Bad

| Topic | Good | Bad |
| --- | --- | --- |
| Measurement | Sandbox APIs + aggregation | Fingerprinting to replace GAID |
| Consent | Regional UX + honor opt-out | Ignore LAT |
| SDKs | Minimal, reviewed | 15 trackers “for growth” |
| Debugging | Test devices only | Production verbose ads logs with PII |

## Output Checklist

- [ ] Ads/measurement inventory complete
- [ ] GAID usage justified or reduced
- [ ] Sandbox API plan + feature flags
- [ ] Attribution/Topics/PA integrations match current docs
- [ ] Opt-out/consent paths tested
- [ ] SDK Runtime / partner review done
- [ ] Legal/privacy sign-off
- [ ] `code-quality-standards` applied

## Rules

- Honor user privacy choices and Play policies.
- Do not build evasion fingerprinting.
- Keep PII out of ads debug pipelines.
- Verify current API names/timelines — this domain moves quickly.
- Owned apps and lawful advertising only.
