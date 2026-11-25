---
name: root-jailbreak-detection
description: Detecting rooted Android and jailbroken iOS devices as a risk signal — not a silver bullet. Use when deciding which operations to allow on a compromised device.
---

# Root / Jailbreak Detection

## Instructions

Root and jailbreak detection are **signals**, not security controls. A rooted device can hide itself from any detection you write. Design for that reality.

### 1. What a Rooted / Jailbroken Device Actually Means

- Platform sandbox is no longer a trust boundary for your app.
- Keystore / Keychain material is still protected **if** it is hardware-backed — root can't extract from StrongBox / Secure Enclave.
- TLS pinning can be bypassed (user CA installed into system store, Frida unpinning, LSPosed modules).
- Screen recorders, input injectors, and clipboard snoopers are trivial.

You may still want to run on these devices (your users include pentesters, tinkerers, and kids with unlocked bootloaders) — but with a higher risk score.

### 2. Android Signals (Combine Several)

```kotlin
fun rootSignals(ctx: Context): List<String> {
    val signals = mutableListOf<String>()

    // 1. Common su binaries
    val suPaths = listOf(
        "/system/bin/su", "/system/xbin/su", "/sbin/su",
        "/system/app/Superuser.apk", "/vendor/bin/su",
    )
    if (suPaths.any { File(it).exists() }) signals += "su_binary"

    // 2. Magisk / SuperSU package names
    val rootPackages = listOf(
        "com.topjohnwu.magisk", "eu.chainfire.supersu",
        "com.koushikdutta.rommanager", "com.noshufou.android.su",
    )
    if (rootPackages.any { isInstalled(ctx, it) }) signals += "root_package"

    // 3. Test-keys build
    if (Build.TAGS?.contains("test-keys") == true) signals += "test_keys"

    // 4. Writable system partitions
    val rwDirs = listOf("/system", "/system/bin", "/system/xbin")
    if (rwDirs.any { File(it).canWrite() }) signals += "system_rw"

    return signals
}
```

Each signal is independently bypassable. Report the **set** of signals, not a boolean.

### 3. iOS Signals

```swift
func jailbreakSignals() -> [String] {
    var signals: [String] = []

    // 1. Known jailbreak files
    let paths = [
        "/Applications/Cydia.app",
        "/Library/MobileSubstrate/MobileSubstrate.dylib",
        "/bin/bash", "/usr/sbin/sshd", "/etc/apt",
        "/private/var/lib/apt/",
    ]
    if paths.contains(where: { FileManager.default.fileExists(atPath: $0) }) {
        signals.append("jb_file")
    }

    // 2. Sandbox escape: can we write outside our container?
    let probe = "/private/jb_probe_\(UUID().uuidString)"
    if (try? "x".write(toFile: probe, atomically: true, encoding: .utf8)) != nil {
        signals.append("sandbox_rw")
        try? FileManager.default.removeItem(atPath: probe)
    }

    // 3. Fork allowed (only jailbroken iOS allows fork)
    if fork() >= 0 { signals.append("fork_allowed") }

    // 4. Known URL schemes
    if let url = URL(string: "cydia://package/com.example"),
       UIApplication.shared.canOpenURL(url) { signals.append("cydia_scheme") }

    return signals
}
```

The `fork()` and sandbox-write checks are the hardest to bypass without kernel patches — the file-path checks are trivial to hide.

### 4. Library Options

- Android: `RootBeer`, `dtx-free` style checks. Read their source, fork, and rename before shipping — stock names are what jailbreak-hiders target.
- iOS: `IOSSecuritySuite`, `DTTJailbreakDetection`. Same caveat.
- Don't trust a single "is rooted?" function. Combine N signals with weights.

### 5. Treat as Risk Score, Not Verdict

Bad pattern:

```kotlin
if (isRooted) { finish(); return } // attacker patches the method, done.
```

Better pattern:

```kotlin
val signals = rootSignals(ctx)
riskScore += signals.size * 10
riskScore += if (attestationVerdict != STRONG) 20 else 0
// Send score + signals to server; let the server decide.
```

The server may:

- Allow read-only usage.
- Block money movement / key operations / document export.
- Require step-up MFA.
- Silently flag for fraud review.

### 6. Business Policy First

Before writing a single check, get written agreement on policy:

- "We allow login on rooted devices, but not transactions over $X."
- "We allow all operations with warning, with extra logging."
- "We refuse to run at all on jailbroken devices."

Each of these is defensible; each has different UX and legal implications. Don't decide this in code review.

### 7. UX

- If you block, tell the user **why** in plain language ("This app requires an unmodified device for security reasons"). Don't hide behind a generic error.
- Provide a support channel for false positives.
- Never ship a hard block without a feature flag to roll back.

## Checklist

- [ ] Root / jailbreak detection combines multiple independent signals.
- [ ] Results are reported as a score + signal list, not a boolean.
- [ ] Server makes the final decision for sensitive operations.
- [ ] Business policy for rooted/jailbroken devices is documented and agreed in advance.
- [ ] Detection libraries are forked / renamed, not used stock.
- [ ] Blocked users get a clear explanation and a support path.
- [ ] A feature flag exists to disable enforcement remotely.
