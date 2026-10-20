---
name: android-proguard-r8-mapping
description: >
  Keep and use R8/ProGuard mapping files for owned Android apps: enable minify,
  archive mapping.txt per versionCode, upload to Play/Crashlytics, and deobfuscate
  stack traces. Use when release crashes are unreadable, CI must retain mappings, or
  configuring -keep rules safely — not for deobfuscating third-party apps without rights.
---

# Android ProGuard / R8 Mapping

## Scope And Authorization

- **In scope:** Apps you ship; crash pipelines you operate.
- **Out of scope:** Using leaked mappings to assist piracy of third-party apps.
- Treat mapping files as moderately sensitive (aid reverse engineering of your code).
- Pair keep-rules with `code-quality-standards`.

## When To Use

- Enabling R8 minify/shrink for release.
- Crash reports show `a.b.c.a()` with no source context.
- Setting up CI artifacts for `mapping.txt` / native debug symbols.
- Writing `-keep` rules without disabling obfuscation entirely.

## Do Not Use As Primary

| Need | Skill instead |
| --- | --- |
| DEX string triage (RE) | `android-dex-string-ids` |
| Play Integrity | `android-safetynet-play-integrity` |
| General pentest | `android-pentesting-tricks` |
| Implementation quality baseline | `code-quality-standards` |

## Domain Focus

| Artifact | Purpose |
| --- | --- |
| `mapping.txt` | Maps obfuscated names → original |
| `seeds.txt` / `usage.txt` | What was kept / removed (R8 outputs) |
| `-keep` rules | Preserve reflection/JNI/entry points |
| Play App Bundle deobfuscation | Upload mapping with each release |
| Native symbols | Separate NDK symbol packaging |

## Workflow

### 1. Confirm success criteria

1. Record applicationId, versionName/versionCode scheme, crash backend.
2. Success: every release mapping archived; sample crash deobfuscates; CI fails if mapping missing.
3. Owners for artifact retention (90+ days recommended).

### 2. Enable R8 and produce mapping

```gradle
android {
  buildTypes {
    release {
      minifyEnabled true
      shrinkResources true
      proguardFiles getDefaultProguardFile('proguard-android-optimize.txt'), 'proguard-rules.pro'
    }
  }
}
```

```bash
./gradlew :app:assembleRelease
# Typical path
ls app/build/outputs/mapping/release/mapping.txt
```

### 3. Archive per version

```bash
VER=$(grep versionCode app/build.gradle | head -1)
cp app/build/outputs/mapping/release/mapping.txt "artifacts/mapping-${VER}.txt"
# Upload to Play Console / Firebase Crashlytics / Sentry per their docs
```

1. Immutable storage keyed by `versionCode` + git SHA.
2. Never overwrite mapping for an already-shipped versionCode.

### 4. Keep rules (minimal)

```proguard
# Example — adjust to frameworks you use
-keepclassmembers class * implements android.os.Parcelable {
  public static final ** CREATOR;
}
# Keep JNI
-keepclasseswithmembernames class * { native <methods>; }
# Serialization / Gson / Moshi models often need explicit keeps
```

| Bad | Better |
| --- | --- |
| `-dontobfuscate` always | Targeted `-keep` |
| Keep entire packages “just in case” | Keep only reflective APIs |
| No rules + reflection crashes | Crash once, add precise keep |

### 5. Deobfuscate a stack trace

```bash
# retrace (ProGuard/R8 retrace)
retrace mapping.txt crash.txt
# Or upload mapping so console auto-deobfuscates
```

### 6. CI gate

```yaml
# Pseudocode CI step
- run: ./gradlew assembleRelease
- run: test -s app/build/outputs/mapping/release/mapping.txt
- run: upload-artifact mapping.txt
```

### 7. Hand off

1. Document path + retention + who can download mappings.
2. Include native symbol steps if NDK used.
3. On incident: fetch mapping for exact versionCode before analyzing.

## Good / Bad

| Topic | Good | Bad |
| --- | --- | --- |
| Retention | Mapping per versionCode | Lost mappings for prod builds |
| Rules | Minimal keeps | `minifyEnabled false` in prod forever |
| Security | Access-controlled artifacts | Public bucket of all mappings |
| Crashes | Retraced stacks | Guessing obfuscated frames |

## Output Checklist

- [ ] minify enabled for release
- [ ] mapping.txt produced and archived per version
- [ ] Crash backend upload automated
- [ ] Keep rules reviewed (minimal)
- [ ] Sample retrace works
- [ ] CI fails if mapping missing
- [ ] Access control on mapping store
- [ ] `code-quality-standards` applied

## Rules

- Owned apps only.
- Never ship without a retrievable mapping for that versionCode.
- Prefer precise `-keep` over disabling R8.
- Control access to mapping files.
- Coordinate native symbols separately from Java/Kotlin mapping.
