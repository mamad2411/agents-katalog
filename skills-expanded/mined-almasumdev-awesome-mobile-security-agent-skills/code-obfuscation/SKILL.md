---
name: code-obfuscation
description: Code obfuscation on mobile — R8 / ProGuard on Android, SwiftShield and its limitations on iOS, and realistic expectations. Use when hardening release builds.
---

# Code Obfuscation

## Instructions

Obfuscation raises the cost of reverse engineering, it does not prevent it. Treat it as speed bumps, not walls.

### 1. What Obfuscation Actually Buys You

- Slows down static analysis with Jadx / Ghidra / Hopper.
- Strips logging and debug symbols from release builds (real value).
- Makes automated tooling (Frida scripts pattern-matching on class names) more brittle.

What it does **not** buy:
- Protection against dynamic instrumentation (Frida, Objection).
- Protection for anything the app actually needs to do — a debugger will see it.
- A substitute for server-side authorization.

### 2. Android: R8 in Release

R8 is the modern replacement for ProGuard and ships with AGP. Enable both shrinking and obfuscation for release:

```kotlin
// app/build.gradle.kts
android {
    buildTypes {
        release {
            isMinifyEnabled = true
            isShrinkResources = true
            proguardFiles(
                getDefaultProguardFile("proguard-android-optimize.txt"),
                "proguard-rules.pro",
            )
        }
    }
}
```

Common `proguard-rules.pro` hygiene:

```proguard
# Keep Kotlin metadata for reflection-heavy libs (Moshi, Retrofit)
-keep class kotlin.Metadata { *; }

# Retrofit + OkHttp
-keepattributes Signature, InnerClasses, EnclosingMethod
-keep,allowobfuscation,allowshrinking interface retrofit2.Call
-keep,allowobfuscation,allowshrinking class retrofit2.Response

# Models read via reflection (adjust to your package)
-keep class com.example.app.dto.** { *; }

# Strip logs in release
-assumenosideeffects class android.util.Log {
    public static *** d(...);
    public static *** v(...);
    public static *** i(...);
}
```

Pitfalls:
- Serialization libraries (Gson/Moshi/kotlinx-serialization) and reflection: every model read by reflection needs a `-keep`.
- JNI / native methods: keep the `native` method signatures exactly.
- DI frameworks (Hilt, Koin) usually ship their own consumer rules — don't duplicate.

### 3. Android: Strip Debug Symbols From Native Libs

```kotlin
android {
    packaging {
        jniLibs {
            useLegacyPackaging = false
        }
    }
    buildTypes {
        release {
            ndk { debugSymbolLevel = "none" } // or "symbol_table" for Play upload only
        }
    }
}
```

Upload symbols to Play separately so your crash reports remain readable.

### 4. iOS: Symbol Stripping

Swift doesn't have an R8. The standard hardening:

- In **Release** build settings:
  - `Strip Debug Symbols During Copy = YES`
  - `Strip Swift Symbols = YES`
  - `Deployment Postprocessing = YES`
  - `Symbols Hidden by Default = YES`
- Archive dSYMs separately and upload to your crash reporter.

### 5. SwiftShield and Friends — Read the Fine Print

SwiftShield renames Swift symbols post-build. Known issues:

- Can break Objective-C interop and `@objc` selectors.
- Can break `Codable`, `NSKeyedArchiver`, and any reflection-based serializer.
- Incompatible with some SDKs that assume class names at runtime.

Use it only if:
- You have a threat model (financial, DRM, gaming) that justifies the fragility.
- You have end-to-end UI tests that run against the obfuscated binary on every PR.
- You accept the maintenance cost.

For most apps, proper symbol stripping + release-mode `assert`/log removal is enough.

### 6. React Native / JavaScript

- Enable Hermes and `minify: true` in `metro.config.js` for release.
- Use `babel-plugin-transform-remove-console` to strip `console.*`.
- Do not rely on JS obfuscators (`javascript-obfuscator`) for secrets — they're trivially reversible.

### 7. Flutter / Dart

- Use `flutter build apk --obfuscate --split-debug-info=build/symbols/`.
- Upload the split debug-info directory to your crash reporter (Crashlytics / Sentry) so stack traces remain readable.
- Dart obfuscation renames symbols but the bytecode structure remains — it is still reverse-engineerable.

### 8. What to Actually Hide

Rank your concerns:

1. Nothing sensitive in the binary — no API keys, no hard-coded JWTs, no endpoints that only "security through obscurity" protects.
2. Strip logs and debug scaffolding from release.
3. Strip symbols / obfuscate names as a speed bump.
4. Only then consider paid RASP / commercial obfuscators, and only if a real threat model requires them.

## Checklist

- [ ] R8 (`isMinifyEnabled = true`) is on for release on Android.
- [ ] Consumer ProGuard rules for every reflection-heavy library are present.
- [ ] Native debug symbols are stripped from the release APK / AAB; symbols uploaded to Play.
- [ ] iOS release strips Swift & debug symbols; dSYMs uploaded to crash reporter.
- [ ] SwiftShield / similar is only used with a documented threat model and UI tests.
- [ ] Flutter release uses `--obfuscate --split-debug-info`; symbols uploaded.
- [ ] Nothing security-relevant relies on the name of a class remaining hidden.
