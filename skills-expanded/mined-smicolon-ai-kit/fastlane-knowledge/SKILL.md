---
name: fastlane-knowledge
description: >-
  Provides Fastlane configuration patterns for Flutter apps including iOS and Android lanes,
  code signing with match, CI/CD integration with GitHub Actions, and environment management.
  Use when user asks about Fastlane setup, deployment automation, code signing, or CI/CD for mobile.
version: 1.0.0
---

# Fastlane for Flutter

Configure and use Fastlane for automated Flutter app deployment.

## Directory Structure

```
project/
├── ios/
│   └── fastlane/
│       ├── Fastfile          # iOS lanes
│       ├── Appfile           # App identifier config
│       ├── Matchfile         # Code signing config
│       └── metadata/         # App Store metadata
├── android/
│   └── fastlane/
│       ├── Fastfile          # Android lanes
│       ├── Appfile           # Package name config
│       └── metadata/         # Play Store metadata
└── Gemfile                   # Ruby dependencies
```

## Setup Commands

```bash
# Install Fastlane
gem install fastlane

# Initialize for iOS
cd ios && fastlane init

# Initialize for Android
cd android && fastlane init

# Initialize match (iOS code signing)
cd ios && fastlane match init
```

## iOS Fastfile Template

```ruby
default_platform(:ios)

platform :ios do
  before_all do
    setup_ci if ENV['CI']
  end

  desc "Build and upload to TestFlight"
  lane :beta do
    match(type: "appstore", readonly: true)

    build_app(
      workspace: "Runner.xcworkspace",
      scheme: "Runner",
      export_method: "app-store",
      output_directory: "./build"
    )

    upload_to_testflight(
      skip_waiting_for_build_processing: true
    )
  end

  desc "Deploy to App Store"
  lane :release do
    match(type: "appstore", readonly: true)

    build_app(
      workspace: "Runner.xcworkspace",
      scheme: "Runner",
      export_method: "app-store"
    )

    upload_to_app_store(
      submit_for_review: true,
      automatic_release: false,
      force: true
    )
  end
end
```

## Android Fastfile Template

```ruby
default_platform(:android)

platform :android do
  desc "Deploy to internal testing"
  lane :internal do
    upload_to_play_store(
      track: "internal",
      aab: "../build/app/outputs/bundle/release/app-release.aab",
      json_key_data: ENV["PLAY_STORE_JSON_KEY"]
    )
  end

  desc "Promote to beta"
  lane :beta do
    upload_to_play_store(
      track: "beta",
      track_promote_to: "beta"
    )
  end

  desc "Deploy to production"
  lane :release do
    upload_to_play_store(
      track: "production",
      aab: "../build/app/outputs/bundle/release/app-release.aab",
      json_key_data: ENV["PLAY_STORE_JSON_KEY"]
    )
  end
end
```

## Code Signing

### iOS with Match
```ruby
# Matchfile
git_url("git@github.com:company/certificates.git")
storage_mode("git")
type("appstore")
app_identifier(["com.company.app"])
```

### Match Commands
```bash
# Create new certificates/profiles
fastlane match appstore
fastlane match development
fastlane match adhoc

# Use existing (CI)
fastlane match appstore --readonly
```

### Android Keystore
```bash
# Generate upload keystore
keytool -genkey -v -keystore upload-keystore.jks \
  -keyalg RSA -keysize 2048 -validity 10000 -alias upload
```

## GitHub Actions Integration

### Required Secrets
- `MATCH_PASSWORD` - Match encryption password
- `MATCH_GIT_AUTH` - Base64 encoded Git credentials
- `ASC_KEY_ID` - App Store Connect API Key ID
- `ASC_ISSUER_ID` - App Store Connect Issuer ID
- `ASC_KEY_CONTENT` - App Store Connect API Key content
- `PLAY_STORE_JSON_KEY` - Google Play service account JSON
- `KEYSTORE_BASE64` - Base64 encoded Android keystore
- `KEYSTORE_PASSWORD` - Android keystore password
- `KEY_PASSWORD` - Android key password
- `KEY_ALIAS` - Android key alias

## Common Lanes

| Lane | Platform | Description |
|------|----------|-------------|
| `beta` | iOS | TestFlight upload |
| `release` | iOS | App Store submission |
| `internal` | Android | Internal testing track |
| `beta` | Android | Beta track |
| `release` | Android | Production release |

## Environment Variables

```bash
# iOS
export MATCH_PASSWORD="your-match-password"
export APP_STORE_CONNECT_API_KEY_ID="your-key-id"
export APP_STORE_CONNECT_API_ISSUER_ID="your-issuer-id"
export APP_STORE_CONNECT_API_KEY_CONTENT="-----BEGIN PRIVATE KEY-----\n..."

# Android
export PLAY_STORE_JSON_KEY='{"type":"service_account",...}'
```

For complete Fastlane configuration, use the `/fastlane-setup` command.
