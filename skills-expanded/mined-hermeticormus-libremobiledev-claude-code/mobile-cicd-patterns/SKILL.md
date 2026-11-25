---
name: mobile-cicd-patterns
description: "Fastfile lanes for iOS and Android distribution, a GitHub Actions matrix for both platforms, Gradle signing config, and the secrets each platform needs. Use when building or fixing a mobile build and release pipeline."
---

# Mobile CI/CD Patterns

## Fastfile: iOS Distribution Lane

```ruby
# fastlane/Fastfile
default_platform(:ios)

APP_STORE_CONNECT_API_KEY = app_store_connect_api_key(
  key_id: ENV["APP_STORE_KEY_ID"],
  issuer_id: ENV["APP_STORE_ISSUER_ID"],
  key_content: ENV["APP_STORE_KEY_CONTENT"] # .p8 contents as base64
)

platform :ios do
  before_all do
    # Install match certs — readonly in CI
    match(
      type: "appstore",
      readonly: is_ci,
      api_key: APP_STORE_CONNECT_API_KEY
    )
  end

  desc "Run all tests"
  lane :test do
    run_tests(
      scheme: "MyApp",
      devices: ["iPhone 15 Pro"],
      clean: true
    )
  end

  desc "Build and upload to TestFlight"
  lane :beta do
    increment_build_number(
      build_number: ENV["BUILD_NUMBER"] || Time.now.strftime("%Y%m%d%H%M")
    )

    build_app(
      scheme: "MyApp",
      configuration: "Release",
      export_method: "app-store"
    )

    pilot(
      api_key: APP_STORE_CONNECT_API_KEY,
      skip_waiting_for_build_processing: true,
      changelog: "Build #{ENV["BUILD_NUMBER"]}"
    )
  end

  desc "Submit to App Store"
  lane :release do |options|
    build_app(scheme: "MyApp", configuration: "Release")

    deliver(
      api_key: APP_STORE_CONNECT_API_KEY,
      submit_for_review: true,
      automatic_release: false,
      skip_screenshots: true,
      force: true # Skip HTML confirmation
    )
  end

  error do |lane, exception|
    # Notify on failure (Slack, email, etc.)
    puts "Lane #{lane} failed: #{exception.message}"
  end
end
```

---

## Fastfile: Android Distribution Lane

```ruby
platform :android do
  desc "Build release APK/AAB and distribute"
  lane :beta do
    gradle(
      task: "bundle",
      build_type: "Release",
      properties: {
        "android.injected.signing.store.file" => ENV["KEYSTORE_PATH"],
        "android.injected.signing.store.password" => ENV["KEYSTORE_PASSWORD"],
        "android.injected.signing.key.alias" => ENV["KEY_ALIAS"],
        "android.injected.signing.key.password" => ENV["KEY_PASSWORD"]
      }
    )

    firebase_app_distribution(
      app: ENV["FIREBASE_APP_ID_ANDROID"],
      groups: "internal-testers",
      release_notes: "Build #{ENV["BUILD_NUMBER"]}"
    )
  end

  lane :deploy do
    gradle(task: "bundle", build_type: "Release")

    upload_to_play_store(
      track: "internal",
      aab: lane_context[SharedValues::GRADLE_AAB_OUTPUT_PATH],
      json_key_data: ENV["PLAY_STORE_JSON_KEY"]
    )
  end
end
```

---

## GitHub Actions: iOS + Android Matrix

```yaml
# .github/workflows/mobile-ci.yml
name: Mobile CI

on:
  push:
    branches: [main]
  pull_request:
    branches: [main]

jobs:
  ios:
    runs-on: macos-14
    steps:
      - uses: actions/checkout@v4

      - name: Set up Ruby
        uses: ruby/setup-ruby@v1
        with:
          ruby-version: '3.2'
          bundler-cache: true  # Caches gems

      - name: Cache CocoaPods
        uses: actions/cache@v4
        with:
          path: ios/Pods
          key: ${{ runner.os }}-pods-${{ hashFiles('ios/Podfile.lock') }}

      - name: Install pods
        run: cd ios && pod install

      - name: Run tests
        run: bundle exec fastlane ios test
        env:
          APP_STORE_KEY_ID: ${{ secrets.APP_STORE_KEY_ID }}
          APP_STORE_ISSUER_ID: ${{ secrets.APP_STORE_ISSUER_ID }}
          APP_STORE_KEY_CONTENT: ${{ secrets.APP_STORE_KEY_CONTENT }}
          MATCH_PASSWORD: ${{ secrets.MATCH_PASSWORD }}
          MATCH_GIT_BASIC_AUTHORIZATION: ${{ secrets.MATCH_GIT_BASIC_AUTHORIZATION }}

      - name: Upload to TestFlight
        if: github.ref == 'refs/heads/main'
        run: bundle exec fastlane ios beta
        env:
          BUILD_NUMBER: ${{ github.run_number }}
          APP_STORE_KEY_ID: ${{ secrets.APP_STORE_KEY_ID }}
          APP_STORE_ISSUER_ID: ${{ secrets.APP_STORE_ISSUER_ID }}
          APP_STORE_KEY_CONTENT: ${{ secrets.APP_STORE_KEY_CONTENT }}
          MATCH_PASSWORD: ${{ secrets.MATCH_PASSWORD }}
          MATCH_GIT_BASIC_AUTHORIZATION: ${{ secrets.MATCH_GIT_BASIC_AUTHORIZATION }}

  android:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v4

      - uses: actions/setup-java@v4
        with:
          java-version: '17'
          distribution: 'temurin'

      - name: Cache Gradle
        uses: actions/cache@v4
        with:
          path: |
            ~/.gradle/caches
            ~/.gradle/wrapper
          key: ${{ runner.os }}-gradle-${{ hashFiles('**/*.gradle*') }}

      - name: Set up Ruby
        uses: ruby/setup-ruby@v1
        with:
          ruby-version: '3.2'
          bundler-cache: true

      - name: Run tests
        run: ./gradlew test

      - name: Distribute beta
        if: github.ref == 'refs/heads/main'
        run: bundle exec fastlane android beta
        env:
          BUILD_NUMBER: ${{ github.run_number }}
          KEYSTORE_PATH: ${{ runner.temp }}/release.keystore
          KEYSTORE_PASSWORD: ${{ secrets.KEYSTORE_PASSWORD }}
          KEY_ALIAS: ${{ secrets.KEY_ALIAS }}
          KEY_PASSWORD: ${{ secrets.KEY_PASSWORD }}
          FIREBASE_APP_ID_ANDROID: ${{ secrets.FIREBASE_APP_ID_ANDROID }}
```

---

## Android: Gradle Signing Config

```groovy
// android/app/build.gradle
android {
    signingConfigs {
        release {
            storeFile file(System.getenv("KEYSTORE_PATH") ?: "release.keystore")
            storePassword System.getenv("KEYSTORE_PASSWORD")
            keyAlias System.getenv("KEY_ALIAS")
            keyPassword System.getenv("KEY_PASSWORD")
        }
    }
    buildTypes {
        release {
            signingConfig signingConfigs.release
            minifyEnabled true
            proguardFiles getDefaultProguardFile('proguard-android-optimize.txt'), 'proguard-rules.pro'
        }
    }
}
```

---

## Required Secrets per Platform

### iOS
- `APP_STORE_KEY_ID` — App Store Connect API key ID
- `APP_STORE_ISSUER_ID` — App Store Connect issuer ID
- `APP_STORE_KEY_CONTENT` — .p8 key content (base64 encoded)
- `MATCH_PASSWORD` — match repo encryption password
- `MATCH_GIT_BASIC_AUTHORIZATION` — base64 `user:token` for match git repo

### Android
- `KEYSTORE_PASSWORD` — keystore file password
- `KEY_ALIAS` — signing key alias
- `KEY_PASSWORD` — key password
- `KEYSTORE_BASE64` — base64 encoded keystore file (decode in CI step)
- `PLAY_STORE_JSON_KEY` — Google Play service account JSON (for upload_to_play_store)
