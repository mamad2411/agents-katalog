---
name: android-exported-components
description: >
  Authorized Android exported-component security review: Activities, Services,
  BroadcastReceivers, ContentProviders, deep links, and intent-filter surface. Use when
  assessing android:exported, unprotected IPC, path permissions, or privilege escalation
  via exported components on owned apps, labs, or CTF APKs.
---

# Android Exported Components

## Scope And Authorization

- **In scope:** APKs you own, lab builds, CTFs, or mobile assessments with written authorization.
- **Out of scope:** Attacking third-party apps on user devices without permission.
- Prefer debug builds with test accounts; avoid production user data.
- Pair remediations with `code-quality-standards` and deeper intent review via `android-intent-security`.

## When To Use

- Manifest review for `android:exported="true"` components.
- Hunting IPC entry points: activities, services, receivers, providers.
- Deep link / App Link attack surface inventory.
- Privilege escalation from a same-device malicious app model.

## Do Not Use As Primary

| Need | Skill instead |
| --- | --- |
| PendingIntent / extras deep dive | `android-intent-security` |
| Full mobile pentest flow | `android-pentesting-tricks` |
| WebView XSS | `android-webview-security` |
| Implementation quality baseline | `code-quality-standards` |

## Domain Focus

| Component | Risk if exported unprotected |
| --- | --- |
| Activity | UI/task hijack, forced flows, data leak via extras |
| Service | Background action trigger, bind exposure |
| Receiver | Spoofed broadcasts causing state change |
| Provider | SQL/IDOR-like data read/write; path traversal |
| Deep links | Open redirects, token theft via params |

**Android 12+:** components with intent filters must explicitly set `android:exported`.

## Workflow

### 1. Confirm scope and success criteria

1. Record package name, build type, auth model.
2. Success: inventory of exported components with protection level; proof for each high-risk; fixes or accepted risk.
3. Threat model: malicious app on device without privileges.

### 2. Inventory from manifest

```bash
# Decode
apktool d app.apk -o apk_out
# Or aapt
aapt dump xmltree app.apk AndroidManifest.xml | rg -i 'exported|intent-filter|provider|activity|service|receiver'
jadx -d jadx_out app.apk
```

```bash
# On device
adb shell dumpsys package com.example.app | rg -i 'exported|Activity|Service|Receiver|Provider'
```

Build a table:

| Component | Type | Exported | Permission | Intent filters |
| --- | --- | --- | --- | --- |

### 3. Classify protection

| Pattern | Assessment |
| --- | --- |
| `exported=false` | Not directly invocable by other apps |
| `exported=true` + signature permission | Only same-signing apps |
| `exported=true` + normal/dangerous custom perm | Weaker; may be obtainable |
| `exported=true` + no permission | **World callable** — review code |
| Provider `grantUriPermissions` | Temporary URI exposure review |

### 4. Dynamic probes (authorized)

```bash
PKG=com.example.app
# Start exported activity
adb shell am start -n $PKG/.DebugActivity
# Send broadcast
adb shell am broadcast -a com.example.ACTION -n $PKG/.MyReceiver
# Start service
adb shell am startservice -n $PKG/.MyService
# Query provider
adb shell content query --uri content://$PKG.provider/items
```

1. Fuzz extras carefully (see `android-intent-security`).
2. Observe data returned, crashes, privilege changes.

### 5. ContentProvider specifics

1. Check `android:readPermission` / `writePermission` / `path-permission`.
2. Test SQL injection in selection if raw queries; IDOR across users if multiprofile.
3. `openFile` path traversal (`..%2F`) if file-backed.

### 6. Deep links

```bash
adb shell am start -a android.intent.action.VIEW -d 'https://example.com/path?token=TEST'
adb shell am start -a android.intent.action.VIEW -d 'myapp://reset?code=TEST'
```

1. Validate tokens server-side; do not trust deep link alone for auth.
2. Prefer verified App Links (`android:autoVerify`).

### 7. Remediate and verify

| Issue | Fix |
| --- | --- |
| Needlessly exported | `exported=false` |
| Must export | signature-level permission or system permission |
| Provider data | Enforce authz in provider code, not only manifest |
| Debug activity | Strip from release builds |

Reinstall release build and re-run `am start` expect failures where appropriate.

## Good / Bad

| Topic | Good | Bad |
| --- | --- | --- |
| Defaults | Explicit exported flags | Implicit surprises pre-review |
| Debug | Non-exported or debug-only | `DebugActivity` exported in prod |
| Providers | Permissions + in-code checks | Open `content://` with PII |
| Testing | Evidence per component | Manifest-only assumptions |

## Output Checklist

- [ ] Full exported component table
- [ ] Protection classification per entry
- [ ] Dynamic invocation results
- [ ] Provider/deep link special cases covered
- [ ] High-risk issues with repro steps
- [ ] Remediation verified on release build
- [ ] Related intent issues handed to `android-intent-security`
- [ ] Secrets redacted

## Rules

- Authorized apps only.
- Treat on-device malicious app as default adversary.
- Prefer least export surface.
- Evidence-driven: code paths + runtime.
- Do not publish exploit APKs for out-of-scope store apps.
