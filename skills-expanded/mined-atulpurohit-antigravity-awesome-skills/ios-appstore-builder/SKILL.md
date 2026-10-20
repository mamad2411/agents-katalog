---
name: ios-appstore-builder
description: "Prepare, configure, and publish iOS apps to the Apple App Store. Covers certificates, provisioning profiles, TestFlight, App Store submission, and review guidelines."
category: mobile
tags: ['ios', 'app-store', 'xcode', 'deployment', 'certificate']
complexity: advanced
risk: medium
compatibility: [claude-code, antigravity, gemini-cli, cursor, copilot, codex-cli, autohand, kiro]
source: antigravity-official
version: "1.0.0"
date_added: "2026-07-10"
last_updated: "2026-07-10"
---

# iOS App Store Builder

## Purpose
Guide the complete process of preparing and publishing iOS applications to the Apple App Store, including code signing, metadata, and review compliance.

## Operating Mode
You are an **iOS deployment specialist**. You navigate Apple's certificate system, App Store Connect, and review guidelines with precision.

## The Process

### 1️⃣ Prerequisites Checklist
- [ ] Apple Developer Account active ($99/year)
- [ ] App ID registered in Developer Portal
- [ ] Bundle ID matches in Xcode project
- [ ] All required capabilities added (push notifications, In-App Purchase, etc.)
- [ ] Privacy manifest (PrivacyInfo.xcprivacy) included

### 2️⃣ Code Signing Setup
```bash
# Via Xcode (recommended for beginners)
# Xcode → Project → Signing & Capabilities
# ✅ Automatically manage signing (for development)

# For CI/CD: Use Fastlane Match for consistent signing
# Gemfile
gem 'fastlane'

# Matchfile
git_url("https://github.com/your-org/certificates")
type("appstore")
app_identifier(["com.example.MyApp"])
username("apple@example.com")

# Generate and store certificates
bundle exec fastlane match appstore
```

### 3️⃣ Fastlane for Automated Builds
```ruby
# Fastfile
platform :ios do
  desc "Run tests"
  lane :test do
    run_tests(
      scheme: "MyApp",
      devices: ["iPhone 15 Pro"],
      clean: true
    )
  end

  desc "Build and upload to TestFlight"
  lane :beta do
    increment_build_number(xcodeproj: "MyApp.xcodeproj")
    
    build_app(
      scheme: "MyApp",
      configuration: "Release",
      export_method: "app-store",
      output_directory: "./build",
    )
    
    upload_to_testflight(
      skip_waiting_for_build_processing: true,
      changelog: "Bug fixes and performance improvements"
    )
  end

  desc "Submit to App Store"
  lane :release do
    capture_screenshots
    
    deliver(
      submit_for_review: true,
      automatic_release: false,
      force: true,
      metadata_path: "./fastlane/metadata",
      screenshots_path: "./fastlane/screenshots",
      precheck_include_in_app_purchases: false,
    )
  end
end
```

### 4️⃣ App Store Metadata Requirements
```
Required:
- App Name (30 chars max)
- Subtitle (30 chars max)
- Description (4000 chars max)
- Keywords (100 chars, comma-separated)
- Support URL
- Marketing URL (optional)
- Privacy Policy URL (required if collecting data)

Screenshots required (all sizes or latest):
- iPhone 6.9" (1320 × 2868px) — Required for iPhone
- iPhone 6.5" (1284 × 2778px)
- iPad Pro 13" (2064 × 2752px) — If universal app
- iPad Pro 12.9" (2048 × 2732px)
```

### 5️⃣ App Review Guidelines Compliance
```
Critical checks before submission:
✅ Privacy nutrition label accurately reflects data collection
✅ App works on latest iOS without crashes
✅ All features fully functional (no "coming soon" placeholders)
✅ Sign in with Apple if using other social logins
✅ In-App Purchase for digital content (no external payment links)
✅ No private API usage
✅ IDFA (advertising tracking) properly disclosed
✅ Permissions have usage descriptions in Info.plist
✅ Age rating set appropriately
```

### 6️⃣ CI/CD with GitHub Actions
```yaml
# .github/workflows/ios-release.yml
name: iOS Release
on:
  push:
    tags: ['v*']

jobs:
  release:
    runs-on: macos-latest
    steps:
      - uses: actions/checkout@v4
      
      - name: Setup Ruby
        uses: ruby/setup-ruby@v1
        with:
          ruby-version: '3.2'
          bundler-cache: true
      
      - name: Install certificates via Match
        run: bundle exec fastlane match appstore --readonly
        env:
          MATCH_PASSWORD: ${{ secrets.MATCH_PASSWORD }}
          GITHUB_TOKEN: ${{ secrets.CERTIFICATES_REPO_TOKEN }}
      
      - name: Build and Upload to TestFlight
        run: bundle exec fastlane beta
        env:
          APP_STORE_CONNECT_API_KEY_ID: ${{ secrets.ASC_KEY_ID }}
          APP_STORE_CONNECT_API_ISSUER_ID: ${{ secrets.ASC_ISSUER_ID }}
          APP_STORE_CONNECT_API_KEY: ${{ secrets.ASC_PRIVATE_KEY }}
```

## Outputs
1. Code signing configuration guide
2. Fastlane setup for automated deployment
3. Metadata and screenshot requirements
4. App Review checklist
5. CI/CD pipeline for automated releases
6. TestFlight beta testing workflow
