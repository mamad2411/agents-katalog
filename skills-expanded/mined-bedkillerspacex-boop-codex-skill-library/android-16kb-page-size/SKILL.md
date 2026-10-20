---
name: android-16kb-page-size
description: >
  Android 16 KB memory page size compatibility for owned apps: ELF segment alignment,
  NDK/AGP tooling, emulator testing, and Play requirements for native libraries. Use when
  preparing for devices with 16 KB pages, fixing misaligned .so loads, or verifying
  bundle native code — not for reverse-engineering third-party apps without authorization.
---

# Android 16 KB Page Size

## Scope And Authorization

- **In scope:** Android apps and native libraries you own or are contracted to ship.
- **Out of scope:** Patching others’ APKs for redistribution without rights.
- Test on 16 KB page emulators/devices before relying on production metrics.
- Pair build changes with `code-quality-standards`.

## When To Use

- Play Console / Android docs warn about **16 KB page size** support.
- App ships JNI/NDK `.so` files and must run on 16 KB devices.
- Crashes on boot with alignment / `dlopen` failures on new hardware/emulators.
- Upgrading AGP/NDK for alignment flags.

## Do Not Use As Primary

| Need | Skill instead |
| --- | --- |
| General Android pentest | `android-pentesting-tricks` |
| ProGuard/R8 mapping | `android-proguard-r8-mapping` |
| Play Integrity | `android-safetynet-play-integrity` |
| Implementation quality baseline | `code-quality-standards` |

## Domain Focus

| Topic | Detail |
| --- | --- |
| Page size | Historical 4 KB; newer devices may use 16 KB |
| ELF LOAD segments | Must be aligned to max page size expectations (tooling enforces 16 KB zip/ELF alignment) |
| Pure Java/Kotlin | Usually fine; risk is **native** code and prebuilt `.so` |
| Prebuilts | Third-party SDKs may ship misaligned binaries |
| Tooling | Recent NDK/AGP, `bundletool`, alignment checkers |

## Workflow

### 1. Confirm scope and success criteria

1. Record appId, minSdk, NDK version, list of `.so` ABIs (`arm64-v8a`, etc.).
2. Success: app installs and runs on 16 KB page emulator; native libs pass alignment checks; CI gate optional.
3. Inventory prebuilt SDKs with native code.

### 2. Inventory native libraries

```bash
# From built APK/AAB
unzip -l app-release.apk | rg '\.so$'
# Extract and check (readelf/llvm-readobj)
unzip -p app-release.apk lib/arm64-v8a/libfoo.so > /tmp/libfoo.so
llvm-readobj -l /tmp/libfoo.so | rg -i 'Align|LOAD'
```

1. Note any `Align` less than required for 16 KB when docs say so for your NDK generation.
2. Prefer rebuilding all native code from source under current NDK.

### 3. Upgrade toolchain and rebuild

```bash
# Android Gradle Plugin / NDK — use versions that document 16 KB support
# Example gradle bits (confirm current Google guidance for your AGP):
# android { packaging { jniLibs { useLegacyPackaging = false } } }
./gradlew :app:assembleRelease
```

1. Rebuild CMake/ndk-build targets cleanly.
2. Update prebuilt vendor SDKs to versions advertising 16 KB support.
3. Enable preferred compression/alignment options per current AGP release notes.

### 4. Test on 16 KB system image

```bash
# Use SDK Manager system image that supports 16 KB page size (API level per Google docs)
emulator -list-avds
# Boot AVD configured for 16 KB (device definition / advanced settings per docs)
adb install -r app-release.apk
adb logcat | rg -i 'dlopen|page size|alignment|UnsatisfiedLinkError'
```

1. Exercise all JNI entry features.
2. Test each ABI you ship.

### 5. Automate checks

```bash
# CI: fail if unexpected prebuilt .so without review
# Optional: script wrapping alignment verification tools from Android docs / NDK
./gradlew :app:check
```

1. Document exceptions for proprietary `.so` with vendor ticket IDs.
2. Re-check after every SDK upgrade.

### 6. Hand off

1. Note NDK/AGP versions and test device/emulator image IDs.
2. Track vendor SDKs lacking 16 KB builds as release blockers.
3. Monitor Play pre-launch reports for related crashes.

## Good / Bad

| Topic | Good | Bad |
| --- | --- | --- |
| Native | Rebuild with current NDK | Years-old prebuilt `.so` unknown origin |
| Test | 16 KB emulator/device | “Works on my 4 KB phone” only |
| SDKs | Vendor-confirmed builds | Ignore Play warnings |
| CI | Alignment/presence checks | Manual hope at release |

## Output Checklist

- [ ] Native libs inventoried per ABI
- [ ] Toolchain versions meet 16 KB guidance
- [ ] Prebuilts upgraded or exception ticketed
- [ ] 16 KB emulator/device test passed
- [ ] logcat clean of link/alignment errors
- [ ] CI check considered
- [ ] `code-quality-standards` on build scripts

## Rules

- Owned apps only.
- Prefer source rebuilds over hex-patching third-party `.so`.
- Verify on real 16 KB images, not assumptions.
- Track vendor native deps as first-class release risk.
- Keep symbols/mappings for crash triage (`android-proguard-r8-mapping`).
