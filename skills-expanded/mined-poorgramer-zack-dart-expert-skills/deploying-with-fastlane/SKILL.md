---
name: "deploying-with-fastlane"
description: "Automates Flutter iOS and Android deployment using Fastlane. Use when setting up `fastlane match` for iOS certificate and provisioning profile management, automating TestFlight uploads via `upload_to_testflight`, pushing Android releases to Google Play via `upload_to_play_store`, auto-incrementing build numbers, writing Fastfile lanes for Flutter release workflows, integrating Fastlane with GitHub Actions or Codemagic, or configuring App Store Connect API Key and Google Play Service Account JSON credentials."
metadata:
  last_modified: "2026-04-01 14:35:00 (GMT+8)"
---

# Flutter combined with Fastlane Best Practices (CI/CD - Deployment)

## Goal
Implements Fastlane for iOS/Android building, code signing, and deployment. [Fastlane](https://fastlane.tools/) is an open-source Ruby script toolset. Although it is not a cloud CI platform (like GitHub Actions), it can **run on top of any CI platform**. It is widely recognized as the ultimate tool for handling the tedious compilation, certification, and submission processes for iOS/Android.

## Instructions

### 1. Separation of Responsibilities
In Flutter development, the best way to combine tools is:
*   **Flutter CLI (`flutter build`)**: Responsible for compiling Dart code into native iOS projects or Android Bundles (AAB).
*   **Fastlane ((`build_app` / `gym`, `upload_to_play_store` / `supply`, `deliver`))**: Takes over subsequent Xcode/Gradle building, handling complex "Code Signing" and pushing to stores (TestFlight / Google Play Console).

### 2. Solving iOS Certificate Pain Points: `fastlane match` (⭐️ Absolutely Essential)
The most painful part of iOS development is syncing `Certificates` and `Provisioning Profiles` when a new team member joins.

`fastlane match` solution: **Encrypt all certificates and centrally manage them in a private Git Repo.**

#### 2.1 Environment Setup & Usage
1. Create a Private GitHub Repository (e.g., `ios-certificates`).
2. Run `fastlane match init` in the terminal to align with the repository URL.
3. Run `fastlane match appstore`, which will automatically connect to the Apple Server, revoke unused certificates, generate brand new ones, and **encrypt and push them to the Git Repo.**

#### 2.2 Match in the CI Environment
On any fresh CI machine, you only need one lane in your Fastfile:
```ruby
lane :beta do
  # 🌟 The machine instantly automatically downloads, decrypts, and installs all certificates!
  match(type: "appstore", readonly: is_ci) 
  
  # Start building
  gym(workspace: "Runner.xcworkspace", scheme: "Runner") 
end
```

### 3. Auto-Incrementing Version Numbers
App Store requires that the Build Number (e.g., the `123` in `1.0.0+123`) increments with every upload.

**Best Practice**: Do not update this manually. Let Fastlane fetch the latest number from the store and increment it.

#### 3.1 Android Incrementing
Use plugins, directly read/write `pubspec.yaml`, or use Fastlane's native API:
```ruby
lane :release_android do
  # Fetch the current latest version number from Google Play
  play_track_version = google_play_track_version_codes(
    package_name: "com.example.app",
    track: "production"
  ).max
  
  new_build_number = (play_track_version || 0) + 1
  # Combine with a script to write back to pubspec.yaml or gradle
end
```

#### 3.2 iOS Incrementing
iOS has an excellent built-in action:
```ruby
lane :release_ios do
  # 🌟 Automatically fetch the latest number from App Store Connect and add 1
  increment_build_number(
    build_number: latest_testflight_build_number + 1 
  )
end
```

### 4. Push to Store (Play Store & App Store)
Once the Fastfile is configured, your deployment process is simplified to a single command.

#### 4.1 Push Android to Google Play Console
Requires setting up a `Google Play Service Account JSON` key.

```ruby
# android/fastlane/Fastfile
lane :deploy_beta do
  # 1. (Done externally) run flutter build appbundle --release
  
  # 2. Automatically upload to internal testing track
  upload_to_play_store(
    track: 'internal',
    aab: '../build/app/outputs/bundle/release/app-release.aab',
    json_key: ENV['PLAY_STORE_JSON_KEY_PATH'] # 🌟 CI Variable
  )
end
```

#### 4.2 Push iOS to TestFlight
Requires setting up an `App Store Connect API Key`.

```ruby
# ios/fastlane/Fastfile
lane :deploy_testflight do
  # 1. Fetch API Key (Replaces traditional two-factor auth Apple accounts)
  app_store_connect_api_key(
    key_id: ENV['ASC_KEY_ID'],
    issuer_id: ENV['ASC_ISSUER_ID'],
    key_filepath: ENV['ASC_KEY_PATH']
  )

  # 2. Pull certificates
  match(type: "appstore")

  # 3. Build IPA in Xcode
  gym(workspace: "Runner.xcworkspace", scheme: "Runner")

  # 4. 🌟 Upload to TestFlight and automatically email testers
  upload_to_testflight(
    skip_waiting_for_build_processing: true
  )
end
```

## Constraints
*   Ensure that the Fastlane scripts are kept within the repository.
*   Once setup, CI simply calls `bundle exec fastlane deploy_testflight` to achieve full deployment automation.
