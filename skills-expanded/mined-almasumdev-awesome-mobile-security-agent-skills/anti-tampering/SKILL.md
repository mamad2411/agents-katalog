---
name: anti-tampering
description: Anti-tampering on mobile — signature checks, runtime application self-protection (RASP), and realistic return on investment. Use to decide which integrity controls are worth shipping.
---

# Anti-Tampering on Mobile

## Instructions

Anti-tampering controls are a spectrum. Pick the layers that match your actual threat model and compliance needs — not a generic checklist.

### 1. Tampering We Care About

| Threat | Example | Who it hurts |
| ------ | ------- | ------------ |
| Re-signed binary | Pirated version with ads injected | Revenue, brand |
| Modified resources | Free-upgrade patch for IAP | Revenue |
| Frida instrumentation | Bypass a feature flag or auth check | Business logic integrity |
| Emulator / cloud device | Automated account fraud | Trust & safety |
| Debugger attached | Reverse engineering in progress | Secrets, IP |

You probably don't care about **all** of these. Pick two or three.

### 2. Signature / Bundle ID Checks

Cheap, high ROI. The app verifies at runtime that it's still signed by your key / has your bundle ID.

```kotlin
fun isGenuine(ctx: Context): Boolean {
    val info = ctx.packageManager.getPackageInfo(
        ctx.packageName,
        PackageManager.GET_SIGNING_CERTIFICATES,
    )
    val expectedSha256 = "AA:BB:CC:..." // pinned at build time
    val signers = info.signingInfo?.apkContentsSigners ?: return false
    return signers.any { sha256Hex(it.toByteArray()) == expectedSha256 }
}
```

```swift
func isGenuine() -> Bool {
    guard let bundleId = Bundle.main.bundleIdentifier else { return false }
    guard bundleId == "com.example.app" else { return false }
    // Optionally validate the embedded provisioning profile / code signature
    return hasValidCodeSignature()
}
```

Don't just early-return `false` — it tells the attacker exactly where to patch. Feed the signal into a server-side anomaly score instead.

### 3. Resource / Asset Integrity

For apps where specific files must not be swapped (game balance JSON, model weights, license files):

- Ship a manifest of `sha256` digests signed with a key you control.
- At startup, recompute and compare.
- Store only the expected digests in R8-obfuscated code, not the full JSON.

### 4. RASP — Where It Pays, Where It Doesn't

RASP (Runtime Application Self-Protection) libraries attempt to detect Frida, debuggers, Magisk modules, Xposed, and various hooking frameworks.

- **Worth it for:** high-value financial, gambling, trading, DRM, and some compliance-driven (PSD2) apps.
- **Rarely worth it for:** most SaaS, productivity, content, and social apps. RASP is noisy, adds startup cost, blocks legitimate users (niche ROMs, custom kernels), and is an arms race.
- **Never a substitute for:** server-side authorization.

If you ship RASP:
- Treat detections as **signals**, not kill switches. Feed them into risk scoring.
- Test against a representative device lab before shipping — false positives on Samsung One UI / Xiaomi MIUI / Huawei EMUI are common.
- Review the vendor's CVE history and support responsiveness.

### 5. Debugger Detection

Cheap to add, cheap to bypass. Still worth it as one signal.

Android:

```kotlin
fun debuggerAttached(): Boolean =
    Debug.isDebuggerConnected() || Debug.waitingForDebugger() ||
    (ApplicationInfo.FLAG_DEBUGGABLE and context.applicationInfo.flags) != 0
```

iOS:

```swift
func isBeingDebugged() -> Bool {
    var info = kinfo_proc()
    var mib: [Int32] = [CTL_KERN, KERN_PROC, KERN_PROC_PID, getpid()]
    var size = MemoryLayout.stride(ofValue: info)
    sysctl(&mib, UInt32(mib.count), &info, &size, nil, 0)
    return (info.kp_proc.p_flag & P_TRACED) != 0
}
```

Ship these disabled in debug builds and only in release binaries.

### 6. Emulator / Cloud Device Signals

Signals to combine (none are definitive):

- `Build.FINGERPRINT` contains `"generic"` / `"emulator"` / `"vbox"`.
- `/proc/cpuinfo`, `/dev/socket/qemud`.
- Sensor availability and realism (a perfect, unchanging accelerometer reading screams emulator).
- iOS: simulator-only paths under `/Applications/Xcode.app/`.

Prefer Play Integrity (`deviceRecognitionVerdict`) / App Attest — they already do this with better fidelity. See [api-abuse-protection](../../network/api-abuse-protection/SKILL.md).

### 7. Server-Side Is Where It Matters

Whatever the client detects, it reports. The server decides:

- If a binary reports "signature invalid" **and** pins fail **and** attestation is missing, raise risk score → require step-up auth, block the transaction, or silently flag for review.
- Never trust a single client-side boolean. Assume the client can lie about any of these signals.

### 8. What Not to Do

- Do not crash the app on tamper detection. A crash is a stack trace that points to the check.
- Do not log `"tamper detected"` in plain text. Use an opaque error code.
- Do not spread checks across 200 places "to make it harder" if you never test them — they'll rot and produce false positives in production.

## Checklist

- [ ] Signature / bundle ID is checked and the result is reported, not used as a kill switch.
- [ ] Asset integrity manifest exists for files whose content must not change.
- [ ] RASP, if used, is justified by threat model and tested on a real device lab.
- [ ] Debugger detection is release-only and feeds a signal, not a crash.
- [ ] Emulator detection uses Play Integrity / App Attest as the primary source.
- [ ] Server-side risk scoring exists to weigh these signals together.
- [ ] No anti-tamper code relies on string literals visible in the binary.
