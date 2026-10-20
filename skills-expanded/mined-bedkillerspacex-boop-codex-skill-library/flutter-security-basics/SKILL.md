---
name: flutter-security-basics
description: >
  Authorized Flutter app security basics: flutter_secure_storage and secret placement,
  MethodChannel/EventChannel trust boundaries, Dart obfuscation limits, deep-link / App
  Links validation, and certificate-pinning packages. Use when reviewing or hardening
  owned Flutter (Android/iOS/desktop) clients, lab builds, or CTF APKs/IPAs—not
  unauthorized third-party mobile apps.
---

# Flutter Security Basics

## Scope And Authorization

- **In scope:** Flutter clients you own, internal apps, labs/CTFs, authorized mobile assessments.
- **Out of scope:** piracy, bypassing third-party app protections without authorization, shipping spyware.
- Prefer debug/profile lab builds for invasive testing; production tests need explicit scope.
- Redact tokens harvested during tests.
- Pair fixes with `code-quality-standards`; storage depth with `flutter-secure-storage-ops`.

## When To Use

- Security review of a **Flutter** mobile/desktop client.
- Checking secret storage, API base URLs, pinning, deep links, and platform channels.
- Understanding that **obfuscation is not security**.
- Preparing hand-off to Frida skills only when authorized runtime RE is needed.

## Do Not Use As Primary

| Need | Skill instead |
| --- | --- |
| flutter_secure_storage ops detail | `flutter-secure-storage-ops` |
| Impeller graphics | `flutter-impeller` |
| Flutter web Wasm | `flutter-wasm-web` |
| Runtime hooking playbook | `frida-hooking-playbook` |
| SSL pinning bypass (authorized) | `mobile-ssl-pinning-bypass` |
| Implementation quality baseline | `code-quality-standards` |

## Domain Focus

| Area | Guidance |
| --- | --- |
| Secrets | No API master secrets in app; use short-lived tokens; secure storage for refresh |
| Channels | Native code is trust boundary; validate all data crossing MethodChannel |
| Transport | TLS; optional pinning with backup pins and report-only rollout |
| Deep links | Validate HTTPS App Links / Universal Links; signed intents; no open redirects |
| Obfuscation | `--obfuscate` + split debug info raises cost only |
| WebView | Minimize; JS bridges are high risk |
| Logging | No tokens in `print`/crash reporters |

## Workflow

### 1. Confirm scope and success criteria

1. Platforms, Flutter version, release mode config, backend auth model.
2. Success: no long-lived secrets in binary; deep links safe; channels validated; clear residual risk on rooted devices.
3. Authorization for any dynamic interception.

### 2. Inventory attack surface

```bash
rg -n "MethodChannel|EventChannel|FlutterSecureStorage|http://|allowBadCertificates|onHttpClientCreate|uni_links|app_links|WebView" -g '*.dart'
flutter build apk --release  # owned; then optional strings triage in lab
```

1. List plugins with native code.
2. Extract endpoints and third-party SDKs.
3. Check Android `network_security_config` / iOS ATS exceptions.

### 3. Secrets and local storage

1. Move tokens to secure storage patterns (`flutter-secure-storage-ops`).
2. Ensure no `.env` with production secrets in assets.
3. Certificate pins and API keys: pins OK to ship; **private API keys** that grant god-mode must not ship.

### 4. Platform channels

```dart
// Native results are untrusted if malware/hooked environment — still validate types/ranges
final result = await platform.invokeMethod<String>('getSession');
if (result == null || result.length > 4096) {
  throw StateError('invalid session payload');
}
```

1. Minimize sensitive logic on the Dart side if it must be secret (prefer server).
2. Audit each channel method for path traversal, intent injection, or URL opens.

### 5. Deep links and navigation

1. Use verified App Links / Universal Links.
2. Parse URIs strictly; allowlist hosts and paths.
3. Do not auto-login from unsigned custom schemes without extra proof.

### 6. TLS and pinning

```dart
// Prefer maintained pinning plugins; always plan pin rotation
// Never ship `badCertificateCallback => true` in release
```

1. If pinning: include backup pin; monitor failures; document rotate procedure.
2. For authorized assessment of *your* app’s pin strength, see `mobile-ssl-pinning-bypass` only in scope.

### 7. Release hardening

```bash
flutter build apk --release --obfuscate --split-debug-info=build/debug-info
flutter build ipa --release --obfuscate --split-debug-info=build/debug-info
```

1. Store debug-info artifacts privately for crash deobfuscation.
2. Enable platform backup rules excluding secret stores where required.
3. Review permissions and exported components in AndroidManifest / iOS Info.plist.

### 8. Verify with evidence

| Check | Evidence |
| --- | --- |
| Strings/secrets | No live production private keys in package |
| Cleartext | No accidental `http://` API |
| Deep link | Malicious host rejected |
| Channel | Fuzzed args don’t crash into RCE (lab) |
| Storage | Tokens not in plaintext prefs |

### 9. Hand off

1. Risk register with residual rooted/hooked device notes.
2. Link Frida skills only if authorized deeper RE required.
3. Apply `code-quality-standards`.

## Good / Bad

| Topic | Good | Bad |
| --- | --- | --- |
| Secrets | Backend-issued tokens | Hardcoded admin JWT |
| TLS | System trust + optional pin | `allowBadCertificates: true` |
| Deep links | Verified HTTPS links | Open `myapp://` trust all |
| Obfuscation | Extra cost layer | “Cannot be reversed” claim |
| Channels | Validate + least data | Reflect raw paths to native FS |
| Logs | Scrubbed | Full response bodies with PII |

## Output Checklist

- [ ] Scope/authorization recorded
- [ ] Secrets storage reviewed
- [ ] Channels inventoried and validated
- [ ] Deep links allowlisted
- [ ] TLS/pinning posture documented
- [ ] Release obfuscation/debug-info process set
- [ ] Cleartext and manifest issues checked
- [ ] Residual device-compromise risk stated
- [ ] Neighbor skills used as needed
- [ ] `code-quality-standards` applied

## Rules

- Owned/authorized apps only.
- Client-side controls are bypassable on compromised devices—enforce critical authZ on servers.
- Do not provide third-party app cracking guidance.
- Prefer honest threat models over security-through-obscurity.
