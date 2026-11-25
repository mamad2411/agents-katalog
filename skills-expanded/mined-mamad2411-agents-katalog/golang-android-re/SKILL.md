---
name: golang-android-re
description: >
  Reverse engineer Android apps that use Go (gomobile/JNI/shared objects): APK
  triage, native .so analysis, Frida on owned apps, and traffic notes. Authorized
  labs/CTF/owned apps only.
---

# Golang Android RE

## Research grounding

Runbook for **Android reverse engineering when Go is in the stack**—`libgojni.so`,
gomobile bindings, or Go-built native libraries—alongside classic APK analysis.
Skill id: `golang-android-re`.

## Scope And Authorization

- **In scope:** apps you own, CTF challenges, written authorization.
- **Out of scope:** piracy, bypassing third-party paid features without auth, malware distribution.
- Prefer offline APK analysis first; dynamic instrumentation only on owned devices/emulators.
- Redact user tokens, device IDs, and personal data from notes.
- Pair findings with responsible disclosure process when applicable.

## When To Use

- APK contains Go native libraries or gomobile artifacts.
- Need to map Java/Kotlin ↔ JNI ↔ Go symbols.
- Lab analysis of TLS, storage, or crypto in Go layer of an Android app.
- Focus tokens: **golang, android, re**.

## Do Not Use As Primary

| Need | Skill instead |
| --- | --- |
| General mobile SSL pinning bypass | `mobile-ssl-pinning-bypass` (owned/authorized) |
| Pure Java/Kotlin RE without Go | Android RE / jadx-focused external skills |
| Desktop Go binary RE | `binary-re/static-analysis` |
| Implementation quality baseline | `code-quality-standards` (if fixing your app) |

## Domain Focus

| Area | Guidance |
| --- | --- |
| APK triage | `aapt`/`apkanalyzer`, jadx, apktool, manifest exported components |
| Go markers | `libgojni.so`, many `go.` / runtime symbols, gomobile packages |
| Native analysis | `readelf`/`llvm-nm`, Ghidra/IDA on `.so`, Go pclntab recovery |
| Dynamic | Frida/gadget on owned build; emulators with writable storage |
| Build-id | Match `.so` to your CI artifacts when auditing first-party apps |
| Pitfalls | Stripped Go hard; obfuscated Java; assuming all logic in smali |

## Workflow

### 1. Confirm scope and success criteria

1. APK source, ownership/authorization, research questions (crypto? API? license?).
2. Success: map of Go entrypoints; evidence for each finding; no scope creep.
3. Lab device/emulator inventory.

### 2. Inventory APK

```bash
# Static triage (local APK file you are allowed to analyze)
unzip -l app.apk | head
aapt dump badging app.apk
# Extract native libs
unzip app.apk 'lib/*/*.so' -d apk_libs
file apk_libs/lib/*/*.so
llvm-nm -D apk_libs/lib/arm64-v8a/libgojni.so 2>/dev/null | head
strings apk_libs/lib/arm64-v8a/*.so | rg -i "go\.|gomobile|http"
```

1. Manifest: exported activities/services/receivers; `allowBackup`; network security config.
2. jadx for Java/Kotlin wrappers calling `native` methods.
3. List JNI method signatures that likely map to Go exports.

### 3. Baseline

1. Hash APK (`sha256sum app.apk`).
2. Note ABI variants (arm64-v8a vs armeabi-v7a).
3. Record app versionCode/versionName.

### 4. Analyze Go native layer

1. Load `.so` in Ghidra; enable Go analysis plugins/scripts if available (pclntab).
2. Cross-ref JNI_OnLoad and `Java_*` style exports if present.
3. Track string decryptors / config blobs used by Go code.
4. For first-party apps: rebuild with symbols to compare.

Dynamic (owned only):

```bash
adb install -r app.apk
adb shell ps -A | rg your.package
# Frida attach only on authorized lab builds
```

5. Capture traffic with mitm on lab network if TLS in scope; Go may use custom stacks.

### 5. Verify with evidence

1. Each claim has file offset / symbol / jadx snippet / screenshot (redacted).
2. Reproduce key behavior twice (cold start / after login).
3. If fixing your app: add tests and run `go test` on shared Go module.

```bash
go test ./... -count=1
govulncheck ./...
```

### 6. Observe and harden (first-party)

1. Reduce exported components; enable network security config; strip only after crash symbol pipeline exists.
2. Move secrets off device; use platform keystore; avoid hardcoding in Go strings.
3. Consider Play Integrity only as signal, not sole trust.

### 7. Hand off

1. Write RE report: architecture diagram Java↔JNI↔Go, findings, remediations.
2. Store artifacts under case folder; keep original APK immutable.
3. Route pinning work to `mobile-ssl-pinning-bypass` if needed.

## Finding categories

| Area | Check |
| --- | --- |
| Storage | World-readable files, secrets in SharedPreferences, Go-written paths |
| Crypto | Hardcoded keys in `.so` strings, custom TLS trust |
| IPC | Exported providers; intent spoofing into Go-handled paths |
| Debug | `debuggable`, leftover gomobile log prints |

## Good / Bad

| Topic | Good | Bad |
| --- | --- | --- |
| Authorization | Owned/CTF APK | Random Play Store piracy RE |
| Method | Static map then targeted dynamic | Blind Frida on production users |
| Evidence | Hashes + offsets | Unsourced claims |
| Topic fidelity | Go `.so` + Android RE | Generic go test only |

## Output Checklist

- [ ] Authorization and APK hash recorded
- [ ] Manifest and exported surface reviewed
- [ ] Native Go libraries identified and sampled
- [ ] JNI/Go boundary mapped
- [ ] Findings with evidence and severity
- [ ] Redaction applied
- [ ] Remediations for first-party apps listed
- [ ] Related skills linked if pinning/traffic deeper

## Rules

- Authorized RE only; evidence-driven.
- Keep originals immutable; derived notes separate.
- Focus on `golang-android-re`.
- Never publish full exploit chains against third parties without program rules.
