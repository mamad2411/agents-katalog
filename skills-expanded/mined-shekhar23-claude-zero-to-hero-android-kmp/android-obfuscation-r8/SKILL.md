---
name: android-obfuscation-r8
description: |
  R8 obfuscation and code shrinking for Android - R8 vs ProGuard, proguard-rules.pro patterns, keep rules for serialization (Gson/Moshi/kotlinx.serialization) and reflection-heavy libraries (Retrofit, Room, Koin, Firebase), mapping file management for crash deobfuscation, testing the release build, and debugging R8 issues with -printusage and -whyareyoukeeping. Use this skill whenever configuring shrinking/obfuscation, diagnosing release-only crashes, writing keep rules for a new library, or preparing a release build. Trigger on phrases like "ProGuard", "R8", "obfuscation", "minification", "keep rules", "proguard-rules", "release build crash", "mapping file", "shrinking", "minifyEnabled", or "-keep".
---

# Android R8 Obfuscation & Code Shrinking

## Overview

R8 is the default shrinker, obfuscator, and optimizer for Android release builds. It replaces ProGuard and is enabled automatically when `minifyEnabled = true`. R8 does three things: **shrinking** (removes unused classes/methods/fields), **obfuscation** (renames to short names like `a.b.c`), and **optimization** (inlines methods, removes dead code branches). All three happen in a single pass.

The most common mistake is shipping a release build without testing it — R8 regularly removes or renames things that are accessed only via reflection, breaking the app silently at runtime.

---

## R8 vs ProGuard

| | R8 | ProGuard |
|---|---|---|
| Default in AGP | Yes (since AGP 3.4) | No |
| Full mode | Yes (`r8.fullModeEnabled=true` in `gradle.properties`) | No |
| Speed | ~2x faster | Slower |
| Kotlin support | Native | Via keep rules |
| Compose support | Native | Limited |
| Use today | Always | Never — do not switch back |

R8 full mode enables more aggressive shrinking (inlining of interfaces, more dead-code elimination). It is recommended for new projects and enabled by default in AGP 8+.

```properties
# gradle.properties — enable full mode explicitly if not already default
android.enableR8.fullMode=true
```

---

## Enabling R8

```kotlin
// app/build.gradle.kts
android {
    buildTypes {
        release {
            isMinifyEnabled = true       // enables R8 shrinking + obfuscation
            isShrinkResources = true     // also remove unused resources
            proguardFiles(
                getDefaultProguardFile("proguard-android-optimize.txt"),  // Android defaults
                "proguard-rules.pro"                                       // your rules
            )
            signingConfig = signingConfigs.getByName("release")
        }
        // Create a minified debug variant to test R8 without a release signing config:
        create("releaseDebug") {
            initWith(getByName("debug"))
            isMinifyEnabled = true
            isShrinkResources = false
            proguardFiles(
                getDefaultProguardFile("proguard-android-optimize.txt"),
                "proguard-rules.pro"
            )
            matchingFallbacks += listOf("release")
        }
    }
}
```

Use the `releaseDebug` build type during development to test R8 without needing a release signing key. Never disable R8 to "fix" a release crash — write the correct keep rule instead.

---

## proguard-rules.pro Syntax Primer

```proguard
# Keep a class and all its members (name + members survive obfuscation):
-keep class com.example.model.UserDto { *; }

# Keep class name but allow member obfuscation:
-keepnames class com.example.model.UserDto

# Keep specific members on any class:
-keepclassmembers class com.example.model.** {
    <init>(...);       # constructors
    <fields>;          # all fields
    <methods>;         # all methods
}

# Keep all annotations (required for many reflection-based libs):
-keepattributes *Annotation*

# Preserve generic type signatures (required for Gson, Retrofit):
-keepattributes Signature

# Keep source file names and line numbers in stack traces:
-keepattributes SourceFile, LineNumberTable
-renamesourcefileattribute SourceFile

# Suppress specific warnings (use sparingly — investigate before silencing):
-dontwarn com.example.thirdparty.**
```

---

## Baseline Rules (Always Include)

These belong in every project's `proguard-rules.pro`:

```proguard
# Keep line numbers for readable crash reports
-keepattributes SourceFile, LineNumberTable
-renamesourcefileattribute SourceFile

# Keep annotations (required by many libraries)
-keepattributes *Annotation*

# Keep generic signatures (required by Gson, Retrofit, Moshi)
-keepattributes Signature

# Kotlin metadata (required for Kotlin reflection and kotlinx.serialization)
-keepattributes RuntimeVisibleAnnotations

# Keep Kotlin companion objects
-keepclassmembers class ** {
    public static ** Companion;
}

# Keep enum values (enums accessed by name are common in serialization)
-keepclassmembers enum * {
    public static **[] values();
    public static ** valueOf(java.lang.String);
}

# Parcelable (Android-generated code)
-keepclassmembers class * implements android.os.Parcelable {
    public static final android.os.Parcelable$Creator CREATOR;
}
```

---

## Rules by Serialization Library

### kotlinx.serialization (Recommended)

```proguard
# kotlinx.serialization — keep serializable classes and their companions
-keepattributes *Annotation*, InnerClasses
-dontnote kotlinx.serialization.AnnotationsKt

-keepclassmembers class kotlinx.serialization.json.** {
    *** Companion;
}
-keepclasseswithmembers class **$$serializer {
    *;
}

# Keep all @Serializable data classes in your project:
-keepclassmembers @kotlinx.serialization.Serializable class ** {
    *** Companion;
    *** INSTANCE;
    kotlinx.serialization.KSerializer serializer(...);
}
-keepclassmembers class ** {
    @kotlinx.serialization.Serializable *;
}
```

### Gson

```proguard
# Gson — keep all DTO classes used with TypeToken or fromJson/toJson
-keepattributes Signature
-keepattributes *Annotation*

# Keep your DTO package (adjust package to match your project):
-keep class com.example.**.dto.** { *; }
-keep class com.example.**.model.** { *; }

# Gson internals
-keepclassmembers,allowobfuscation class * {
    @com.google.gson.annotations.SerializedName <fields>;
}
-keep,allowobfuscation,allowshrinking class com.google.gson.reflect.TypeToken
-keep,allowobfuscation,allowshrinking class * extends com.google.gson.reflect.TypeToken
```

> Prefer kotlinx.serialization over Gson in new projects. Gson relies entirely on reflection and requires broader keep rules.

### Moshi

```proguard
# Moshi — keep all classes annotated with @JsonClass
-keepclasseswithmembers class * {
    @com.squareup.moshi.JsonClass *;
}
-keepclassmembers class * {
    @com.squareup.moshi.Json <fields>;
}
# Moshi generated adapters (JsonAdapter subclasses)
-keep class **JsonAdapter { *; }
-keepnames class **JsonAdapter
```

---

## Rules by Reflection-Heavy Library

### Retrofit

```proguard
# Retrofit interfaces must not be renamed (called by reflection at runtime)
-keep,allowobfuscation,allowshrinking interface retrofit2.Call
-keep,allowobfuscation,allowshrinking class retrofit2.Response
-keepclasseswithmembers interface * {
    @retrofit2.http.* <methods>;
}
# OkHttp (pulled in by Retrofit)
-dontwarn okhttp3.**
-dontwarn okio.**
-keepnames class okhttp3.internal.publicsuffix.PublicSuffixDatabase
```

### Room

```proguard
# Room — keep all @Entity, @Dao, @Database classes
-keep class * extends androidx.room.RoomDatabase
-keepclassmembers class * extends androidx.room.RoomDatabase {
    abstract *;
}
-keep @androidx.room.Entity class *
-keep @androidx.room.Dao interface *
-keepclassmembers @androidx.room.Dao interface * { *; }

# Room's generated _Impl classes must not be removed
-keep class **_Impl { *; }
-keep class **_Impl$* { *; }
```

### Koin

```proguard
# Koin uses reflection to resolve types by KClass — keep all injected classes
# Koin 3.x ships its own consumer rules, but add this as a safety net:
-keepnames class * {
    @org.koin.core.annotation.* *;
}
# If using Koin annotations:
-keep @org.koin.core.annotation.Single class *
-keep @org.koin.core.annotation.Factory class *
-keep @org.koin.core.annotation.KoinViewModel class *
```

### Firebase

```proguard
# Firebase ships its own consumer ProGuard rules via AAR — usually no manual rules needed.
# If you use Firebase Dynamic Links or Remote Config with custom data classes, keep them:
-keep class com.example.**.RemoteConfigModel { *; }

# Firebase Crashlytics — ensure mapping file upload is configured (see below)
# No additional keep rules needed — Crashlytics handles its own classes.
```

### Hilt / Dagger

```proguard
# Hilt / Dagger — generated component classes must not be removed
-keep class dagger.hilt.** { *; }
-keep class javax.inject.** { *; }
-keep @dagger.hilt.android.HiltAndroidApp class *
-keep @dagger.hilt.android.AndroidEntryPoint class *
# Hilt ships consumer rules — these are a safety net for edge cases
```

---

## Mapping Files: Crash Deobfuscation

R8 generates a `mapping.txt` file per build that maps obfuscated names back to originals. Without it, crash stack traces are unreadable.

### Location

```
app/build/outputs/mapping/<buildVariant>/mapping.txt
```

### Store Mapping Files Per Release

```kotlin
// app/build.gradle.kts
android {
    buildTypes {
        release {
            // Fail the build if mapping file isn't generated
            ndk {
                debugSymbolLevel = "FULL"
            }
        }
    }
}
```

Store `mapping.txt` alongside every release APK/AAB:
- In your release artifact storage (S3, GCS bucket, Artifactory)
- Tagged by `versionCode` and `versionName`
- For Google Play: upload via the Play Console (Release > App bundle explorer > Downloads)
- For Firebase Crashlytics: upload automatically via the Crashlytics Gradle plugin

```kotlin
// app/build.gradle.kts — Firebase Crashlytics auto-upload
plugins {
    id("com.google.firebase.crashlytics")
}

// The Crashlytics plugin automatically uploads mapping.txt on release builds.
// Disable only if you manage uploads manually:
// firebaseCrashlytics { mappingFileUploadEnabled = false }
```

### Deobfuscating a Stack Trace Manually

```bash
# Using the retrace tool bundled with the Android SDK:
java -jar $ANDROID_HOME/tools/proguard/lib/retrace.jar \
    app/build/outputs/mapping/release/mapping.txt \
    stacktrace.txt

# Or using the bundletool retrace:
retrace --mapping mapping.txt stacktrace.txt
```

---

## Testing Obfuscation: Release Build Smoke Checklist

Always run the following before shipping a release:

```bash
# Build a release APK or AAB (or use the releaseDebug variant locally):
./gradlew assembleRelease
# or
./gradlew bundleRelease
```

- [ ] App launches without crash
- [ ] Login / registration flow completes end-to-end
- [ ] All network API calls succeed (serialization not broken)
- [ ] Room database reads and writes work
- [ ] Deep links open the correct screen (class names in manifests are kept)
- [ ] Firebase / Crashlytics initialises (check Logcat for "Crashlytics initialized")
- [ ] In-app purchases or subscription screen loads (Play Billing classes kept)
- [ ] Any feature using `Class.forName()` or `Kotlin.reflect` works correctly
- [ ] Run Monkey test for 500 events: `adb shell monkey -p com.example.app 500`

---

## Debugging R8 Issues

### `-printusage`: See What Was Removed

```proguard
# Add to proguard-rules.pro temporarily (remove before shipping):
-printusage build/outputs/r8-usage.txt
```

After building, `r8-usage.txt` lists every class/method R8 removed. Search it for the class name in the crash to confirm it was stripped.

### `-whyareyoukeeping`: See Why Something Is Kept

```proguard
# Understand the keep chain for a specific class:
-whyareyoukeeping class com.example.notes.NoteDto
```

The build output will print the reason chain — useful when a class you expected to be removed is still present (or vice versa).

### `-verbose`: Full R8 Output

```proguard
-verbose
```

Enables detailed R8 logging during the build. Helps trace rule evaluation order.

### Common Release-Only Crash Patterns

| Symptom | Likely cause | Fix |
|---|---|---|
| `ClassNotFoundException` | Class removed by R8 | Add `-keep class com.example.Foo` |
| `NoSuchFieldException` | Field renamed/removed | Add `-keepclassmembers` for the field |
| `JsonDataException` / `SerializationException` | DTO fields renamed | Add keep rules for the DTO package |
| `NullPointerException` on reflection | Annotation removed | Add `-keepattributes *Annotation*` |
| Room crash on first DB access | DAO or `_Impl` class removed | Add `-keep class **_Impl { *; }` |
| Retrofit `IllegalArgumentException` | Interface method renamed | Add `@keepclasseswithmembers` for Retrofit interfaces |
| Koin `NoBeanDefFoundException` | Injected class renamed | Add `-keepnames` for injected classes |

### Checking APK Contents After R8

```bash
# Decompile the release APK to verify specific classes exist:
java -jar apktool.jar d app-release.apk -o apk-decompiled

# Or use dex2jar + JD-GUI for more readable output:
./d2j-dex2jar.sh app-release.apk
# Open resulting jar in JD-GUI and navigate to the package in question
```

---

## Library Consumer Rules

Well-maintained libraries ship their own consumer ProGuard rules inside the AAR. These are merged automatically — you do not need to duplicate them. Check if a library already bundles rules before writing your own:

```bash
# Unzip the AAR and look for proguard.txt:
unzip -p ~/.gradle/caches/.../library.aar proguard.txt
```

Libraries that ship their own rules: OkHttp, Retrofit, Moshi (with codegen), Room, WorkManager, Hilt, Firebase, Coil, Koin 3.x.

Libraries that do NOT ship sufficient rules and need manual rules: Gson, many lesser-known reflection-heavy libraries.

---

## Keep Rules Decision Tree

```
Does the library use reflection or code generation to access your classes?
├── Yes → Write keep rules for the classes it accesses
│         (DTOs, entities, annotated interfaces, @Serializable classes)
└── No  → R8 can safely rename/remove unused code — no rules needed

Is the class name referenced in AndroidManifest.xml, navigation XML, or a string?
├── Yes → The name must be kept: -keep class com.example.MyActivity
└── No  → R8 can rename it

Is the class instantiated via Class.forName() or Kotlin's KClass anywhere?
├── Yes → -keep or -keepnames the class
└── No  → R8 can handle it
```
