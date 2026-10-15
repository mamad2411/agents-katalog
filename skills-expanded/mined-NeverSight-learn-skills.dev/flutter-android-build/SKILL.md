---
name: flutter-android-build
description: Use when creating a new Flutter project, setting up Android build config, or when you need a proven version matrix to build Flutter Android APK/AAB successfully on CI or locally. Covers Gradle/AGP/Kotlin/Java version pairing, config templates, GitHub Actions workflows, and 10 common error patterns with fixes.
---

# Flutter Android Build — Never-Fail Formula

> **Purpose:** Ensure every Flutter Android build succeeds on CI (GitHub Actions) and locally.
> This skill is complementary to `flutter-android-build-triage` (which fixes broken builds).
> This skill **prevents** builds from breaking by using the correct version matrix upfront.

---

## 1. The Golden Version Matrix

This is the **tested, proven** combination. Pin these versions and builds will succeed.

```
┌──────────────────────────────────────────────────────────────┐
│  COMPONENT           │  VERSION         │  NOTES             │
├──────────────────────────────────────────────────────────────┤
│  Flutter             │  stable (latest) │  Always latest     │
│  Dart SDK            │  ^3.13.0         │  Match Flutter     │
│  Java (JDK)          │  17 (Temurin)    │  NOT 11, NOT 21    │
│  Kotlin              │  2.4.0           │  settings.gradle   │
│  AGP (Android Gradle)│  9.1.0           │  settings.gradle   │
│  Gradle              │  9.3.1           │  wrapper props     │
│  compileSdk          │  flutter.compileSdkVersion  │ Auto   │
│  minSdk              │  flutter.minSdkVersion      │ Auto   │
│  targetSdk           │  36              │  Play Store req    │
│  desugar_jdk_libs    │  2.1.4           │  For notifications │
│  NDK                 │  flutter.ndkVersion          │ Auto   │
│  GH Actions Java     │  temurin 17      │  setup-java        │
└──────────────────────────────────────────────────────────────┘
```

### Why These Specific Versions?

| Pairing | Why it works |
|---------|-------------|
| **Java 17 + Gradle 9.3.1** | Gradle 9.x requires Java 17-26. Java 17 is the minimum safe choice. |
| **Gradle 9.3.1 + AGP 9.1.0** | AGP 9.1 requires Gradle >= 9.0. Gradle 9.3.1 satisfies this. |
| **AGP 9.1.0 + Kotlin 2.4.0** | AGP 9.x ships with Kotlin Gradle Plugin support. |
| **Java 17 + sourceCompatibility 17 + jvmTarget 17** | All three MUST match. Mismatch = compilation error. |
| **coreLibraryDesugaring 2.1.4** | Required by `flutter_local_notifications` for Java 8+ API on older Android. |

### Version Landmines — DO NOT

| Mistake | Why it breaks |
|---------|--------------|
| Java 21 + Gradle < 8.5 | Gradle can't run on Java 21 below 8.5 |
| AGP 9.3 + Gradle < 9.5 | AGP 9.3 requires Gradle >= 9.5 |
| Kotlin 2.1 + Gradle 9.3 | Kotlin 2.1 only tested up to Gradle 8.6 |
| `isMinifyEnabled = true` with Flutter | R8 crashes on missing Play Core classes |
| Java 11 + AGP 8+ | AGP 8+ requires Java 17 minimum |
| Groovy `build.gradle` + Flutter 3.29+ | Flutter now defaults to Kotlin DSL `.kts` |

### AGP → Gradle Minimum Version

| AGP Version | Minimum Gradle |
|-------------|---------------|
| 8.0–8.4 | 8.0 |
| 8.5–8.7 | 8.7 |
| 8.8–8.9 | 8.10 |
| 9.0–9.1 | 8.9 |
| 9.2 | 9.2 |
| 9.3+ | 9.5 |

---

## 2. Config Templates (Copy-Paste)

### 2.1 `android/settings.gradle.kts`

```kotlin
pluginManagement {
    val flutterSdkPath =
        run {
            val properties = java.util.Properties()
            file("local.properties").inputStream().use { properties.load(it) }
            val flutterSdkPath = properties.getProperty("flutter.sdk")
            require(flutterSdkPath != null) { "flutter.sdk not set in local.properties" }
            flutterSdkPath
        }

    includeBuild("$flutterSdkPath/packages/flutter_tools/gradle")

    repositories {
        google()
        mavenCentral()
        gradlePluginPortal()
    }
}

plugins {
    id("dev.flutter.flutter-plugin-loader") version "1.0.0"
    id("com.android.application") version "9.1.0" apply false
    id("org.jetbrains.kotlin.android") version "2.4.0" apply false
}

include(":app")
```

### 2.2 `android/build.gradle.kts` (project-level)

```kotlin
allprojects {
    repositories {
        google()
        mavenCentral()
    }
}

val newBuildDir: Directory =
    rootProject.layout.buildDirectory
        .dir("../../build")
        .get()
rootProject.layout.buildDirectory.value(newBuildDir)

subprojects {
    val newSubprojectBuildDir: Directory = newBuildDir.dir(project.name)
    project.layout.buildDirectory.value(newSubprojectBuildDir)
}
subprojects {
    project.evaluationDependsOn(":app")
}

tasks.register<Delete>("clean") {
    delete(rootProject.layout.buildDirectory)
}
```

### 2.3 `android/app/build.gradle.kts`

```kotlin
plugins {
    id("com.android.application")
    id("dev.flutter.flutter-gradle-plugin")
}

android {
    namespace = "com.example.yourapp"  // ← CHANGE THIS
    compileSdk = flutter.compileSdkVersion
    ndkVersion = flutter.ndkVersion

    compileOptions {
        isCoreLibraryDesugaringEnabled = true
        sourceCompatibility = JavaVersion.VERSION_17
        targetCompatibility = JavaVersion.VERSION_17
    }

    defaultConfig {
        applicationId = "com.example.yourapp"  // ← CHANGE THIS
        minSdk = flutter.minSdkVersion
        targetSdk = 36
        versionCode = flutter.versionCode
        versionName = flutter.versionName
    }

    signingConfigs {
        create("release") {
            val ksFile = System.getenv("KEYSTORE_FILE")
            if (ksFile != null && file(ksFile).exists()) {
                storeFile = file(ksFile)
                storePassword = System.getenv("KEYSTORE_PASSWORD") ?: ""
                keyAlias = System.getenv("KEY_ALIAS") ?: ""
                keyPassword = System.getenv("KEY_PASSWORD") ?: ""
            }
        }
    }

    buildTypes {
        release {
            val ksFile = System.getenv("KEYSTORE_FILE")
            signingConfig = if (ksFile != null && file(ksFile).exists()) {
                signingConfigs.getByName("release")
            } else {
                signingConfigs.getByName("debug")
            }
            // CRITICAL: R8 MUST be disabled for Flutter
            isMinifyEnabled = false
            isShrinkResources = false
        }
    }
}

kotlin {
    compilerOptions {
        jvmTarget = org.jetbrains.kotlin.gradle.dsl.JvmTarget.JVM_17
    }
}

dependencies {
    coreLibraryDesugaring("com.android.tools:desugar_jdk_libs:2.1.4")
}

flutter {
    source = "../.."
}
```

### 2.4 `android/gradle/wrapper/gradle-wrapper.properties`

```properties
distributionBase=GRADLE_USER_HOME
distributionPath=wrapper/dists
zipStoreBase=GRADLE_USER_HOME
zipStorePath=wrapper/dists
distributionUrl=https\://services.gradle.org/distributions/gradle-9.3.1-all.zip
```

### 2.5 `pubspec.yaml` (relevant section)

```yaml
environment:
  sdk: ^3.13.0

dependencies:
  flutter_local_notifications: ^22.3.0  # Requires coreLibraryDesugaring
  # ... your other packages
```

---

## 3. GitHub Actions Workflows

### 3.1 Debug APK (`.github/workflows/build-debug-apk.yml`)

```yaml
name: Build Debug APK

on:
  push:
    branches: [ main ]
  workflow_dispatch:

jobs:
  build:
    runs-on: ubuntu-latest
    defaults:
      run:
        working-directory: android  # adjust if Flutter project is in subfolder

    steps:
      - uses: actions/checkout@v4

      - name: Setup Java 17
        uses: actions/setup-java@v4
        with:
          distribution: 'temurin'
          java-version: '17'

      - name: Setup Flutter
        uses: subosito/flutter-action@v2
        with:
          channel: 'stable'

      - run: flutter doctor -v
      - run: flutter pub get
      - run: flutter analyze
      - run: flutter test

      - name: Build debug APK
        run: flutter build apk --debug

      - uses: actions/upload-artifact@v4
        with:
          name: debug-apk
          path: build/app/outputs/flutter-apk/app-debug.apk
          retention-days: 7
```

### 3.2 Release AAB Signed (`.github/workflows/build-release-aab.yml`)

```yaml
name: Build Release AAB

on:
  push:
    branches: [ main ]
  workflow_dispatch:

jobs:
  build:
    runs-on: ubuntu-latest
    defaults:
      run:
        working-directory: android

    steps:
      - uses: actions/checkout@v4

      - name: Setup Java 17
        uses: actions/setup-java@v4
        with:
          distribution: 'temurin'
          java-version: '17'

      - name: Setup Flutter
        uses: subosito/flutter-action@v2
        with:
          channel: 'stable'

      - run: flutter doctor -v
      - run: flutter pub get
      - run: flutter analyze
      - run: flutter test

      - name: Decode release keystore
        env:
          KEYSTORE_BASE64: ${{ secrets.KEYSTORE_BASE64 }}
        run: echo "$KEYSTORE_BASE64" | base64 -d > /tmp/release.jks

      - name: Build release AAB (signed)
        env:
          KEYSTORE_FILE: /tmp/release.jks
          KEYSTORE_PASSWORD: ${{ secrets.KEYSTORE_PASSWORD }}
          KEY_ALIAS: ${{ secrets.KEY_ALIAS }}
          KEY_PASSWORD: ${{ secrets.KEY_PASSWORD }}
        run: flutter build appbundle --release

      - uses: actions/upload-artifact@v4
        with:
          name: release-aab
          path: build/app/outputs/bundle/release/app-release.aab
          retention-days: 30
```

---

## 4. Common Build Errors & Fixes

### Error 1: `Unsupported class file major version XX`
**Cause:** Java version too new for Gradle.
**Fix:** Use Java 17 + Gradle 9.3.1.

### Error 2: `Could not resolve com.android.tools.build:gradle`
**Cause:** AGP version incompatible with Gradle.
**Fix:** Check AGP→Gradle minimum versions in Section 1 table.

### Error 3: `R8: Missing class com.google.android.play.core.*`
**Cause:** Flutter auto-enables R8 for release. R8 needs Play Core classes.
**Fix:** Add `isMinifyEnabled = false` and `isShrinkResources = false` in `buildTypes.release`.

### Error 4: `Core library desugaring failed`
**Cause:** Missing desugar dependency (needed by `flutter_local_notifications`).
**Fix:** Both: (1) `isCoreLibraryDesugaringEnabled = true` in compileOptions, (2) `coreLibraryDesugaring("com.android.tools:desugar_jdk_libs:2.1.4")` in dependencies.

### Error 5: `Namespace not specified`
**Cause:** AGP 8+ requires namespace in android block.
**Fix:** Add `namespace = "com.example.yourapp"` in `android {}`.

### Error 6: `XML parsing: unescaped '&'`
**Cause:** `&` in AndroidManifest must be `&amp;`.
**Fix:** Replace `&` with `&amp;` in all XML attributes.

### Error 7: `Kotlin compilation: Unresolved reference`
**Cause:** Kotlin version mismatch or missing import.
**Fix:** Ensure Kotlin version in settings.gradle.kts matches what AGP expects.

### Error 8: `flutter_local_notifications: Plugin requested incompatible Kotlin API version`
**Cause:** Plugin compiled with newer Kotlin than project uses.
**Fix:** Use Kotlin 2.4.0+ (latest stable).

### Error 9: `Sentry: Incompatible version with Kotlin X.X`
**Cause:** Sentry Flutter SDK version doesn't match Kotlin version.
**Fix:** Use `sentry_flutter: ^9.28.0` for Kotlin 2.4 compatibility.

### Error 10: `Execution failed for task ':app:mergeDebugResources'`
**Cause:** Resource conflict or missing resource.
**Fix:** Run `flutter clean && flutter pub get && flutter build apk --debug`.

---

## 5. Verification Checklist

Before pushing, verify:

```bash
# 1. Clean build
flutter clean

# 2. Get dependencies
flutter pub get

# 3. Analyze (no errors)
flutter analyze

# 4. Run tests (all pass)
flutter test

# 5. Build debug APK
flutter build apk --debug

# 6. Build release AAB (if signed)
flutter build appbundle --release
```

---

## 6. Quick Diagnosis Flowchart

```
Build failed?
  |
  +- "Unsupported class file major version"
  |   --> Java version too high. Use Java 17.
  |
  +- "Could not resolve com.android.tools.build:gradle"
  |   --> AGP/Gradle mismatch. Check matrix in Section 1.
  |
  +- "R8: Missing class"
  |   --> Add isMinifyEnabled = false in buildTypes.release.
  |
  +- "Core library desugaring"
  |   --> Add coreLibraryDesugaring dependency + flag.
  |
  +- "Namespace not specified"
  |   --> Add namespace = "..." in android {} block.
  |
  +- "XML parsing: unescaped"
  |   --> Replace & with &amp; in AndroidManifest.xml.
  |
  +- "Kotlin compilation error"
  |   --> Check Kotlin version matches AGP. Use 2.4.0.
  |
  +- "Plugin requested incompatible Kotlin API"
  |   --> Upgrade Kotlin or downgrade plugin.
  |
  +- Unknown error
      --> flutter clean && flutter pub get && flutter build apk --debug
          (90% of unknown errors are stale caches)
```

---

## 7. Tips for Any Flutter Project

1. **Never modify Flutter's auto-generated Gradle files** unless you know exactly what you're doing.
2. **Use Kotlin DSL (.kts)** — Flutter 3.29+ defaults to it. Groovy files cause more issues.
3. **Pin your versions in settings.gradle.kts** — don't use `latest` for AGP/Kotlin.
4. **Always set `isMinifyEnabled = false`** for Flutter release builds until Flutter officially supports R8.
5. **Use `flutter.compileSdkVersion`** instead of hardcoding — it auto-updates with Flutter.
6. **CI should match local** — same Java version, same Flutter channel.
7. **Run `flutter analyze` before build** — catches errors before Gradle even starts.
8. **`flutter clean` is free** — use it liberally when builds fail mysteriously.
9. **Never commit `local.properties`** — it contains machine-specific paths.
10. **Test on real devices** — CI builds APK but can't verify runtime behavior.

---

## 8. Related Skills

- **`flutter-android-build-triage`** — Fix a build that's already broken (diagnose from error output).
- **`android-release-signing`** — Verify and fix Android release signing for Play Store.
- **`gh-actions-expo-apk-build`** — Build Expo/React Native APK on GitHub Actions (different framework).
