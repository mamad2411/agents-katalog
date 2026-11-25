---
name: android-playstore-builder
description: "Build, sign, and publish Android apps to Google Play Store. Covers AAB builds, signing configs, Play Console, staged rollouts, and automated CI/CD."
category: mobile
tags: ['android', 'play-store', 'gradle', 'release', 'aab']
complexity: advanced
risk: medium
compatibility: [claude-code, antigravity, gemini-cli, cursor, copilot, codex-cli, autohand, kiro]
source: antigravity-official
version: "1.0.0"
date_added: "2026-07-10"
last_updated: "2026-07-10"
---

# Android Play Store Builder

## Purpose
Guide the complete process of building, signing, and publishing Android applications to the Google Play Store.

## Operating Mode
You are an **Android release engineer**. You configure proper signing, build releases, manage Play Console, and automate the deployment pipeline.

## The Process

### 1️⃣ Release Build Configuration
```groovy
// app/build.gradle (Groovy)
android {
    defaultConfig {
        applicationId "com.example.myapp"
        versionCode 42              // Increment for every release
        versionName "2.1.0"        // Human-readable version
    }

    signingConfigs {
        release {
            storeFile file(RELEASE_STORE_FILE)      // From gradle.properties
            storePassword RELEASE_STORE_PASSWORD
            keyAlias RELEASE_KEY_ALIAS
            keyPassword RELEASE_KEY_PASSWORD
        }
    }

    buildTypes {
        release {
            signingConfig signingConfigs.release
            minifyEnabled true
            shrinkResources true
            proguardFiles getDefaultProguardFile('proguard-android-optimize.txt'), 'proguard-rules.pro'
        }
    }
}
```

```kotlin
// app/build.gradle.kts (Kotlin DSL)
android {
    signingConfigs {
        create("release") {
            storeFile = file(properties["RELEASE_STORE_FILE"] as String)
            storePassword = properties["RELEASE_STORE_PASSWORD"] as String
            keyAlias = properties["RELEASE_KEY_ALIAS"] as String
            keyPassword = properties["RELEASE_KEY_PASSWORD"] as String
        }
    }

    buildTypes {
        release {
            signingConfig = signingConfigs.getByName("release")
            isMinifyEnabled = true
            isShrinkResources = true
        }
    }
}
```

### 2️⃣ Keystore Management
```bash
# Generate keystore (do this ONCE and keep it safe forever)
keytool -genkey -v -keystore my-release-key.jks   -alias my-key-alias   -keyalg RSA -keysize 2048   -validity 10000

# Store securely in:
# - Password manager (1Password, Bitwarden)
# - Encrypted cloud storage
# - NEVER commit to git

# gradle.properties (local, gitignored)
RELEASE_STORE_FILE=../keystore/my-release-key.jks
RELEASE_KEY_ALIAS=my-key-alias
RELEASE_STORE_PASSWORD=your_store_password
RELEASE_KEY_PASSWORD=your_key_password
```

### 3️⃣ Build AAB (Android App Bundle)
```bash
# Build release AAB
./gradlew bundleRelease

# Output: app/build/outputs/bundle/release/app-release.aab

# Build APK (for direct distribution/testing)
./gradlew assembleRelease

# Verify signing
apksigner verify --print-certs app-release.apk
```

### 4️⃣ Fastlane for Android
```ruby
# Fastfile
platform :android do
  desc "Deploy to Play Store internal track"
  lane :internal do
    gradle(
      task: 'bundle',
      build_type: 'Release',
      properties: {
        "android.injected.signing.store.file" => ENV["KEYSTORE_PATH"],
        "android.injected.signing.store.password" => ENV["KEYSTORE_PASSWORD"],
        "android.injected.signing.key.alias" => ENV["KEY_ALIAS"],
        "android.injected.signing.key.password" => ENV["KEY_PASSWORD"],
      }
    )

    upload_to_play_store(
      track: 'internal',
      aab: 'app/build/outputs/bundle/release/app-release.aab',
      release_status: 'draft',
      json_key: 'play-store-key.json',
    )
  end

  desc "Promote internal to production with staged rollout"
  lane :production do
    upload_to_play_store(
      track: 'internal',
      track_promote_to: 'production',
      rollout: '0.1',  # 10% rollout
      json_key: 'play-store-key.json',
    )
  end
end
```

### 5️⃣ Play Store Requirements
```
App Content Requirements:
✅ Target SDK must be ≥ Android 14 (API 34) for new apps (2024+)
✅ Privacy policy URL if collecting any personal data
✅ Data safety form filled accurately
✅ Age rating questionnaire completed
✅ Content rating certificate

Assets Required:
- App icon: 512×512px (PNG, no alpha for store listing)
- Feature graphic: 1024×500px
- Screenshots: at least 2 per device type
  - Phone: 320-3840px on any side
  - Tablet 7": optional
  - Tablet 10": optional
```

### 6️⃣ GitHub Actions CI/CD
```yaml
# .github/workflows/android-release.yml
name: Android Release
on:
  push:
    tags: ['v*']

jobs:
  release:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v4
      
      - uses: actions/setup-java@v4
        with:
          java-version: '17'
          distribution: 'temurin'
      
      - name: Decode Keystore
        run: echo "${{ secrets.KEYSTORE_BASE64 }}" | base64 -d > keystore.jks
      
      - name: Build Release AAB
        run: ./gradlew bundleRelease
        env:
          RELEASE_STORE_FILE: ../keystore.jks
          RELEASE_STORE_PASSWORD: ${{ secrets.KEYSTORE_PASSWORD }}
          RELEASE_KEY_ALIAS: ${{ secrets.KEY_ALIAS }}
          RELEASE_KEY_PASSWORD: ${{ secrets.KEY_PASSWORD }}
      
      - name: Upload to Play Store
        uses: r0adkll/upload-google-play@v1
        with:
          serviceAccountJsonPlainText: ${{ secrets.PLAY_SERVICE_ACCOUNT_JSON }}
          packageName: com.example.myapp
          releaseFiles: app/build/outputs/bundle/release/app-release.aab
          track: internal
```

## Outputs
1. Gradle signing configuration
2. Keystore generation and management guide
3. Fastlane deployment automation
4. Play Store listing requirements
5. CI/CD pipeline template
6. Staged rollout strategy
