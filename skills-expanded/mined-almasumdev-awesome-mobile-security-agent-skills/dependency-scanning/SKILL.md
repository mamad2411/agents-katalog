---
name: dependency-scanning
description: Scanning mobile app dependencies for known vulnerabilities — Gradle Versions, Snyk, Dependabot, CocoaPods Audit, and npm audit. Use to keep the dependency surface patched.
---

# Dependency Scanning on Mobile

## Instructions

Most reported mobile CVEs live in dependencies — third-party SDKs, networking libs, image loaders, JSON parsers. A weekly cadence beats a one-off audit.

### 1. Inventory First

You can't scan what you can't see. Produce an SBOM per build:

- Android: CycloneDX Gradle plugin (`org.cyclonedx.bom`) produces `bom.json`.
- iOS: `cyclonedx-cocoapods` / `cyclonedx-swift` for SwiftPM.
- Flutter: `cyclonedx_dart` or parse `pubspec.lock`.
- React Native: `@cyclonedx/cdxgen` handles npm + native.

Archive the SBOM with the release artifact. You will want it the day a new CVE drops.

### 2. Gradle / Android

`gradle-versions-plugin` flags outdated direct dependencies:

```kotlin
// build.gradle.kts
plugins { id("com.github.ben-manes.versions") version "0.51.0" }

// Run: ./gradlew dependencyUpdates -Drevision=release
```

For CVEs, **OWASP Dependency-Check** or **Snyk**:

```kotlin
plugins { id("org.owasp.dependencycheck") version "11.1.0" }
dependencyCheck {
    failBuildOnCVSS = 7.0f // fail on high / critical
    suppressionFile = "config/owasp-suppressions.xml"
}
```

### 3. CocoaPods / SwiftPM

- `pod outdated` for CocoaPods outdated check.
- `bundler-audit` / custom script hitting the GitHub Security Advisory DB for CVEs.
- SwiftPM: Xcode 14+ shows a "Package Dependencies" pane; integrate Snyk / Socket for deeper checks.
- Carthage: dying, migrate.

### 4. Flutter / pub.dev

- `dart pub outdated` on every PR.
- Monitor `pubspec.lock` in review — large transitive changes often hide breaking updates.
- `pana` scores each package on health / maintenance; good signal for low-maintenance abandons.

### 5. React Native / npm

- `npm audit` / `pnpm audit` / `yarn npm audit` on every install.
- Pin via a lockfile (`package-lock.json` / `pnpm-lock.yaml`). Never `"^"`-float sensitive deps in production.
- Watch for **postinstall scripts** from dependencies — supply-chain attacks increasingly target these.
- `socket.dev` or `snyk` provides behavioral analysis (network access, file writes from a JS package).

### 6. GitHub Dependabot

Enable across platforms:

```yaml
# .github/dependabot.yml
version: 2
updates:
  - package-ecosystem: gradle
    directory: "/"
    schedule: { interval: weekly }
    groups:
      non-major: { update-types: [minor, patch] }
  - package-ecosystem: cocoapods
    directory: "/ios"
    schedule: { interval: weekly }
  - package-ecosystem: pub
    directory: "/"
    schedule: { interval: weekly }
  - package-ecosystem: npm
    directory: "/"
    schedule: { interval: weekly }
  - package-ecosystem: github-actions
    directory: "/"
    schedule: { interval: weekly }
```

Group non-major updates so you get one PR a week, not fifty.

### 7. Triage Policy

Not every HIGH CVE is exploitable in your app. Have a documented triage policy:

- **CVSS ≥ 9** or actively exploited in the wild → patch within 7 days, release out-of-band if needed.
- **CVSS 7–9** → patch within 30 days.
- **CVSS < 7** → next scheduled release.
- **Not applicable** (e.g., CVE in a code path you don't use) → document suppression with link to reasoning, review quarterly.

### 8. Transitive Dependency Attacks

The 2021–2024 wave of typosquat / account-takeover attacks on npm, PyPI, and RubyGems applies to mobile too. Defenses:

- Lockfile + integrity hashes (`--frozen-lockfile`, `pod install --deployment`).
- Block CI from installing from non-registry sources unless whitelisted.
- Review diffs on major dep bumps — not just semver; read the changelog.

### 9. Native Libraries (AAR / .framework / .xcframework)

Binary SDKs are a black box. Mitigations:

- Prefer SDKs that publish source.
- Pin versions by checksum (`sha256` in lockfile where supported).
- On major vendor upgrades, run the APK / IPA through MobSF to check for new permissions / classes.

### 10. Kotlin / Swift Version Churn

Bumping Kotlin or Swift often cascades into every dependency. Plan for this in the Gradle / Xcode upgrade issues — not every PR.

## Checklist

- [ ] An SBOM is generated per release build and archived with the artifact.
- [ ] OWASP Dependency-Check (or Snyk) fails the build on unsuppressed high/critical CVEs.
- [ ] `gradle-versions` / `pod outdated` / `dart pub outdated` / `npm audit` run on every PR.
- [ ] Dependabot is enabled for every ecosystem in the repo.
- [ ] Lockfiles are committed and CI uses `--frozen-lockfile` or equivalent.
- [ ] A triage policy with SLAs by CVSS is documented and followed.
- [ ] Binary SDKs are pinned by checksum where supported and re-scanned on upgrade.
- [ ] Suppression entries link to a rationale and have a review date.
