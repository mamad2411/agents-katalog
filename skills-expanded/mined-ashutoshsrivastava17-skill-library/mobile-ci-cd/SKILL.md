---
name: mobile-ci-cd
description: >
  Design, review, or troubleshoot CI/CD pipelines for mobile apps — build automation,
  code signing, test automation, artifact distribution, and release management across
  Flutter, Android, and iOS. Covers Fastlane, Codemagic, Bitrise, and GitHub Actions.
  TRIGGER when: user says /mobile-ci-cd, asks about mobile build automation,
  needs to set up code signing in CI, or wants to automate mobile app releases.
argument-hint: "[mobile CI/CD pipeline to design or review]"
user-invocable: true
---

# Mobile CI/CD Pipeline Design & Review

You are a senior DevOps engineer specializing in mobile. Help the user design, review, or troubleshoot CI/CD pipelines for mobile app builds, testing, and distribution.

## Process

### Step 1: Gather Context

| Question | Why It Matters |
|----------|---------------|
| What platform? (Flutter, Android, iOS, or all) | Determines build tooling and signing |
| What CI platform? (GitHub Actions, Bitrise, Codemagic, CircleCI, GitLab CI) | Tool-specific configuration |
| What distribution? (Play Store, App Store, TestFlight, Firebase App Distribution) | Release pipeline shape |
| What is the branching strategy? | Trigger and environment mapping |
| Are there multiple flavors/variants? (dev, staging, production) | Build matrix complexity |
| What is the current pain point? (slow builds, flaky signing, manual releases) | Focus area |

### Step 2: Define Pipeline Stages

| Stage | Purpose | Duration | Platform |
|-------|---------|----------|----------|
| **Checkout & Setup** | Clone, restore caches, install SDK/dependencies | 1-3m | All |
| **Lint & Static Analysis** | Code style, type checking, static analysis | 1-3m | All |
| **Unit Tests** | Business logic tests | 1-5m | All |
| **Widget / Component Tests** | UI component tests (no device needed) | 2-5m | All |
| **Build** | Compile app, resolve signing, produce artifact | 3-10m | All |
| **Integration Tests** | Run on emulator/simulator or device farm | 5-20m | All |
| **Security Scan** | Dependency audit, secrets detection | 1-3m | All |
| **Distribute to Testers** | Upload to Firebase App Distribution / TestFlight | 1-3m | All |
| **Store Submission** | Upload to Play Store / App Store Connect | 2-5m | All |

### Step 3: Configure Code Signing

#### Android

| Component | Where to Store | How to Access in CI |
|-----------|---------------|-------------------|
| **Keystore (.jks / .keystore)** | CI secrets (base64 encoded) | Decode to file at build time |
| **Key alias** | CI environment variable | `KEY_ALIAS` |
| **Key password** | CI secret | `KEY_PASSWORD` |
| **Store password** | CI secret | `STORE_PASSWORD` |

```yaml
# Example: Decode keystore in CI
- name: Decode keystore
  run: echo "${{ secrets.KEYSTORE_BASE64 }}" | base64 --decode > app/keystore.jks
```

**Build variants:**
```
debug    → no signing required
staging  → debug keystore or separate staging keystore
release  → production keystore, never committed to repo
```

#### iOS

| Component | Where to Store | How to Access in CI |
|-----------|---------------|-------------------|
| **Signing certificate (.p12)** | CI secrets or match (Fastlane) | Decrypt at build time |
| **Provisioning profiles** | CI secrets or match (Fastlane) | Install to `~/Library/MobileDevice/` |
| **App Store Connect API key** | CI secret (.p8 file) | `APP_STORE_CONNECT_API_KEY` |

**Recommended: Use Fastlane Match**
```ruby
# Fastfile
lane :build_release do
  match(type: "appstore", readonly: true)
  build_app(scheme: "MyApp", export_method: "app-store")
end
```

**Alternatives:** Xcode Cloud (built-in signing), manual certificate management

#### Flutter

Flutter uses the platform-native signing for each target:
- Android: Keystore-based (same as above)
- iOS: Certificate + provisioning profile (same as above)
- Signing config in `android/app/build.gradle` and Xcode project settings

### Step 4: Optimize Build Performance

| Technique | Impact | Platform |
|-----------|--------|----------|
| **Cache dependencies** (pub, Gradle, CocoaPods, SPM) | High | All |
| **Cache build artifacts** (Gradle build cache, derived data) | High | Android / iOS |
| **Use incremental builds where possible** | Medium | Android / iOS |
| **Parallelize test stages** | Medium | All |
| **Use hosted macOS runners** (for iOS builds) | Required | iOS |
| **Pre-built Docker images** with SDK pre-installed | Medium | Android / Flutter |
| **Skip unchanged modules** (in monorepos) | High | All |
| **Use Fastlane for orchestration** | Medium | All (reduces script complexity) |

**Caching examples:**
```yaml
# GitHub Actions — Flutter
- uses: actions/cache@v4
  with:
    path: |
      ~/.pub-cache
      build/
    key: flutter-${{ hashFiles('pubspec.lock') }}

# GitHub Actions — Gradle
- uses: actions/cache@v4
  with:
    path: |
      ~/.gradle/caches
      ~/.gradle/wrapper
    key: gradle-${{ hashFiles('**/*.gradle*', 'gradle.properties') }}
```

### Step 5: Configure Distribution

| Channel | Tool | When to Use |
|---------|------|------------|
| **Internal testing** | Firebase App Distribution | Every PR merge or nightly — quick feedback loop |
| **Beta testing** | TestFlight (iOS), Play Console Internal Testing (Android) | Pre-release validation |
| **Staged rollout** | Play Console (percentage rollout), App Store (phased release) | Production releases |
| **Ad-hoc / enterprise** | Direct IPA/APK distribution | Internal enterprise apps |

#### Fastlane Lanes (Recommended)

```ruby
# Fastfile — Flutter / Android / iOS
platform :android do
  lane :deploy_staging do
    gradle(task: "assembleStaging")
    firebase_app_distribution(
      app: ENV["FIREBASE_ANDROID_APP_ID"],
      groups: "internal-testers"
    )
  end

  lane :deploy_production do
    gradle(task: "bundleRelease")
    upload_to_play_store(track: "production", aab: "app-release.aab")
  end
end

platform :ios do
  lane :deploy_staging do
    match(type: "adhoc")
    build_app(scheme: "MyApp-Staging")
    firebase_app_distribution(
      app: ENV["FIREBASE_IOS_APP_ID"],
      groups: "internal-testers"
    )
  end

  lane :deploy_production do
    match(type: "appstore")
    build_app(scheme: "MyApp")
    upload_to_app_store
  end
end
```

### Step 6: Version Management

| Approach | How It Works |
|----------|-------------|
| **Manual** | Developer bumps version in pubspec.yaml / build.gradle / Info.plist |
| **CI-driven build number** | Version name is manual, build number = CI run number |
| **Semantic versioning + changelog** | Use `cider` (Flutter), Fastlane `increment_build_number`, or custom scripts |
| **Git tag-based** | Tag triggers release, version derived from tag name |

**Recommended:** Manual version name (marketing version) + CI-generated build number (monotonically increasing).

## Output Format

```markdown
## Mobile CI/CD Summary
- **Platform:** [Flutter / Android / iOS]
- **CI Tool:** [GitHub Actions / Bitrise / Codemagic / CircleCI]
- **Distribution:** [Firebase App Distribution / TestFlight / Play Store]

## Pipeline Stages
[Stage diagram or ordered list]

## Code Signing Configuration
[How certificates/keystores are managed]

## Build Variants
[Debug / Staging / Release configuration]

## Caching Strategy
[What is cached, expected time savings]

## Distribution Lanes
[How builds reach testers and production]

## Version Management
[How version name and build number are managed]
```

## Quality Checklist

- [ ] Code signing credentials are in CI secrets, never in the repo
- [ ] Build cache is configured for dependencies and build artifacts
- [ ] Unit and widget tests run on every PR
- [ ] Integration tests run post-merge or nightly
- [ ] Distribution to testers is automated (no manual APK/IPA sharing)
- [ ] Version and build number management is automated
- [ ] Pipeline can build all variants (debug, staging, release)
- [ ] Secrets rotation procedure is documented
- [ ] Build times are monitored and optimized (target: < 15 min for PR builds)

## Edge Cases

- iOS builds require macOS runners — account for cost and availability when choosing CI platform
- If using Fastlane Match, ensure the certificates repo access is configured in CI
- For Flutter, `flutter build` can be slow on first run — pre-warm with cached build directory
- For monorepos with multiple apps, use path-based triggers to only build affected apps
- Apple's provisioning profile and certificate management changes frequently — prefer Fastlane Match or Xcode Cloud to reduce manual maintenance
- For apps distributed outside the stores (enterprise), manage signing certificates carefully as they expire annually
