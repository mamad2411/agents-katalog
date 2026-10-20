---
name: android-health-connect
description: >
  Android Health Connect integration for owned apps: permissions, data types, privacy
  rationale, read/write least privilege, and user-facing permission UX. Use when adding
  fitness/health data sync via Health Connect APIs — not for exfiltrating health data
  from other apps without user consent and policy compliance.
---

# Android Health Connect

## Scope And Authorization

- **In scope:** Health/fitness features in apps you ship; compliance with Play and privacy policies.
- **Out of scope:** Covert harvesting of health data; bypassing Health Connect permission UX.
- Health data is sensitive — minimize types, retention, and sharing.
- Pair with `code-quality-standards` and privacy review processes.

## When To Use

- Reading/writing steps, exercise, sleep, vitals via **Health Connect**.
- Migrating from Google Fit APIs to Health Connect.
- Declaring health permissions and rationales correctly.
- Security/privacy review of health data flows.

## Do Not Use As Primary

| Need | Skill instead |
| --- | --- |
| Photo/media access privacy | `android-photo-picker` |
| General Android pentest | `android-pentesting-tricks` |
| Backend API authz | `api-auth-and-jwt-abuse` / API skills |
| Implementation quality baseline | `code-quality-standards` |

## Domain Focus

| Topic | Guidance |
| --- | --- |
| Permissions | Per data-type read/write permissions; request only needed |
| Data types | Record types (Steps, ExerciseSession, HeartRate, …) |
| Aggregation | Prefer aggregates over raw samples when sufficient |
| Rationale | In-app education before system permission |
| Background | Understand foreground vs longer access limitations |
| Sync | Secure backend storage; encryption; retention limits |

## Workflow

### 1. Confirm scope and success criteria

1. Record which data types, why, retention, third-party sharing.
2. Success: least-privilege permissions; user can revoke; no access without grant; backend policies documented.
3. Legal/privacy sign-off for health data if required.

### 2. Declare permissions (manifest)

```xml
<!-- Examples — use only what you need; names evolve with SDK -->
<uses-permission android:name="android.permission.health.READ_STEPS"/>
<uses-permission android:name="android.permission.health.WRITE_STEPS"/>
<!-- Additional types as required -->
```

1. Align with Play health policy declarations.
2. Avoid broad unused types “for later.”

### 3. Feature availability and client setup

```kotlin
val availability = HealthConnectClient.getSdkStatus(context)
if (availability != HealthConnectClient.SDK_AVAILABLE) {
    // Guide user to install/update Health Connect
}
val client = HealthConnectClient.getOrCreate(context)
```

### 4. Permission request UX

```kotlin
// Use PermissionController / contract APIs for Health Connect permissions
// Show educational UI explaining why steps are needed before request
val granted = client.permissionController.getGrantedPermissions()
if (needed.none { it in granted }) {
    // launch permission request activity/contract
}
```

1. Handle deny and “don’t ask again” with settings deep link.
2. Feature must degrade gracefully without health access.

### 5. Read/write least data

```kotlin
// Sketch: read steps aggregate for a time range instead of infinite history
val request = ReadRecordsRequest(
    recordType = StepsRecord::class,
    timeRangeFilter = TimeRangeFilter.between(start, end)
)
val response = client.readRecords(request)
```

| Practice | Rationale |
| --- | --- |
| Time-bounded queries | Minimize data |
| Aggregates | Less sensitive footprint |
| No log of raw vitals | Privacy |
| Encrypt at rest server-side | Protect sync |

### 6. Security review checklist

| Check | Pass |
| --- | --- |
| Permissions match actual API calls | Yes |
| No export of health DB content providers unintentionally | Yes |
| Backup rules exclude sensitive health caches if required | Reviewed |
| Network sync TLS + authz | Yes |
| Third-party SDKs don’t over-read health | Reviewed |

### 7. Verify

```bash
adb shell dumpsys package com.example.app | rg -i health
# Manual: grant subset of types; confirm others fail closed
# Manual: revoke in system settings; app handles without crash
```

### 8. Hand off

1. Privacy policy text updated for health data.
2. Data deletion path (account delete clears health copies).
3. Monitor for SDK changes in Health Connect permissions.

## Good / Bad

| Topic | Good | Bad |
| --- | --- | --- |
| Scope | Steps only for step challenge | Read all vitals “just in case” |
| UX | Clear rationale | Silent request on first launch |
| Storage | Minimal sync + retention | Infinite raw HR on server |
| Failures | Feature disables cleanly | Crash if HC missing |

## Output Checklist

- [ ] Data types and purpose documented
- [ ] Manifest permissions minimized
- [ ] Availability + install guidance handled
- [ ] Permission UX + revoke path tested
- [ ] Queries time-bounded; logging safe
- [ ] Backend retention/deletion defined
- [ ] Play/privacy policy aligned
- [ ] `code-quality-standards` applied

## Rules

- User consent and platform permissions are mandatory.
- Minimize health data collection and retention.
- Never bypass Health Connect for covert access.
- Treat health data as high sensitivity in RE/test notes.
- Owned apps only for implementation guidance.
