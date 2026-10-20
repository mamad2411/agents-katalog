---
name: android-intent-security
description: >
  Review Android Intent security: exported components, intent filters, PendingIntent
  mutability, deeplinks, and parcel extras validation. Use when auditing owned apps or
  authorized mobile assessments beyond generic exported-component lists.
---

# Android Intent Security

## Scope And Authorization

- **In scope:** Owned apps, labs, CTFs, authorized mobile assessments.
- **Out of scope:** Delivering malware intents against third-party apps without authorization.
- Use test devices/accounts; redact tokens found in extras.
- Builds on `android-exported-components`; pair fixes with `code-quality-standards`.

## When To Use

- Auditing Intent extras handling and type confusion.
- PendingIntent flags (`FLAG_IMMUTABLE` / mutability).
- Deep link parameter injection and identity assertion.
- Implicit intent hijacking / intent redirection.

## Do Not Use As Primary

| Need | Skill instead |
| --- | --- |
| Exported surface inventory only | `android-exported-components` |
| WebView-specific issues | `android-webview-security` |
| Full pentest toolbox | `android-pentesting-tricks` |
| Implementation quality baseline | `code-quality-standards` |

## Domain Focus

| Issue class | Summary |
| --- | --- |
| Implicit intent hijack | Sending implicit intents with sensitive extras |
| Intent redirection | Forwarding attacker-controlled Intent to privileged component |
| Extras trust | Assuming types/ranges; parcel mismatch |
| PendingIntent | Mutable PI allows attacker fill-in |
| Deep links | Auth tokens in query; open redirect |
| Task affinity / trampoline | UI spoofing patterns |

## Workflow

### 1. Confirm scope and success criteria

1. Package, components of interest, auth model.
2. Success: dangerous intent paths listed with repro; PendingIntents immutable where required; extras validated; deep links don’t grant auth alone.
3. Combine with exported inventory.

### 2. Static review

```bash
jadx -d out app.apk
rg -n "getParcelableExtra|getSerializableExtra|getStringExtra|startActivity|sendBroadcast|PendingIntent" out/
rg -n "FLAG_MUTABLE|FLAG_IMMUTABLE|getIntent\\(\\)" out/
```

1. Flag `getIntent()` data passed to `startActivity` without validation (redirection).
2. Flag mutable PendingIntents for notifications/alarms on modern SDKs.

### 3. PendingIntent hardening

```kotlin
val flags = PendingIntent.FLAG_UPDATE_CURRENT or PendingIntent.FLAG_IMMUTABLE
PendingIntent.getActivity(ctx, 0, explicitIntent, flags)
```

| Case | Guidance |
| --- | --- |
| Fixed target/action | Prefer IMMUTABLE |
| Need fill-in | Use carefully; explicit component; minimal attacker control |
| Notifications | Immutable default on recent Android |

### 4. Extras validation

```kotlin
// Bad: trust
val url = intent.getStringExtra("url")
webView.loadUrl(url!!)
// Better: allowlist schemes/hosts; null-check; size limits
```

| Check | Action |
| --- | --- |
| Null/missing | Fail closed |
| Type | Use typed APIs; careful with custom Parcelable |
| Ranges | IDs positive; lengths capped |
| Nested intents | Unwrap only if trusted |

### 5. Intent redirection tests

```bash
# Attacker crafts intent extra that victim forwards
adb shell am start -n com.victim/.GatewayActivity --es redirect '...'
# Prefer instrumented PoC app in lab
```

1. Prove whether untrusted app can force privileged activity or data leak.
2. Fix: never forward raw attacker Intent; copy allowed fields only.

### 6. Deep links and identity

```bash
adb shell am start -a android.intent.action.VIEW -d 'myapp://login?token=STOLEN'
```

1. Tokens in links leak via logs, referrers, history — prefer server-side one-time codes.
2. Validate path/host; reject unexpected schemes.

### 7. Implicit intents with sensitive data

1. Prefer explicit component when targeting your own app.
2. For `ACTION_SEND`, assume other apps can read extras.

### 8. Hand off

1. File each issue with component, intent payload, impact.
2. Add lint/rules if available for mutable PI and intent redirects.
3. Regression tests for deep link allowlists.

## Good / Bad

| Topic | Good | Bad |
| --- | --- | --- |
| PI flags | IMMUTABLE default | Mutable “for convenience” |
| Redirection | Field allowlist | `startActivity(intent.getParcelableExtra("next"))` |
| Deep link | One-time server code | Long-lived session in URL |
| Implicit | No secrets in extras | Auth headers in SEND extras |

## Output Checklist

- [ ] Exported inventory available
- [ ] PendingIntent mutability reviewed
- [ ] Extras validation reviewed on entry points
- [ ] Redirection paths tested
- [ ] Deep links auth model verified
- [ ] Implicit sensitive sends reviewed
- [ ] Fixes verified
- [ ] `code-quality-standards` applied

## Rules

- Authorized testing only.
- Validate all untrusted Intent data.
- Prefer explicit intents and immutable PendingIntents.
- Deep links are not authentication by themselves.
- Redact tokens from PoCs and reports.
