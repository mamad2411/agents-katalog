---
name: update-dependencies
description: Use when dependencies, SDKs or toolchains need updating in any app (npm, NuGet, Gradle, Swift, GitHub Actions, Xcode, JDK, .NET, Node), when a Dependabot pull request fails or is a major version, or on request ("update dependencies"). Moves everything to the latest stable version safely, one ecosystem at a time.
---

# Update dependencies

Goal: every app on the **latest stable** versions, without breaking anything. Stable means a final release: no alpha, beta, RC, preview, snapshot or nightly.

## What is automatic

`.github/dependabot.yml` opens pull requests every week (monthly for the website and GitHub Actions):

* **Patch and minor** updates are grouped per app, wait 5 days after release (7 for Android), and **merge on their own** once every required check is green (`dependabot-auto-merge.yml`).
* **Security** updates are grouped per app and opened as soon as an advisory appears.
* **Major** updates come one per pull request and wait for a person: follow section 3.

So most of the time there is nothing to do. This skill is for what the bot cannot do.

## 1. See what is out of date

| App | Command (from the app's folder) |
|---|---|
| Web app, back office, website | `npm outdated` |
| Backend | `dotnet list package --outdated` |
| Android | Open the Dependabot pull requests, or check each version in `gradle/libs.versions.toml` on Google Maven and Maven Central |
| iOS | No third-party packages yet. Check Xcode, SwiftLint, XcodeGen and Maestro versions |
| Workflows | Action tags in `.github/workflows/*.yml` |

Toolchains are not covered by Dependabot. Check them each quarter:

| Toolchain | Where it is set |
|---|---|
| Node | `node-version` in workflows, README |
| .NET SDK | `dotnet-version` in workflows, `TargetFramework` in `.csproj` |
| JDK | `java-version` in workflows |
| Gradle wrapper | `apps/android/gradle/wrapper/gradle-wrapper.properties` |
| Android Gradle Plugin, compile and target SDK | `libs.versions.toml`, `app/build.gradle.kts` (Google raises the required target SDK every year) |
| Xcode and iOS deployment target | `runs-on: macos-*` in workflows, `apps/ios/project.yml` |

## 2. Patch and minor updates by hand

When a grouped Dependabot pull request fails, or you update outside the bot:

1. One app per branch: `chore/deps-<app>`.
2. Update: `npm update` (npm), edit versions (NuGet `.csproj`, Gradle `libs.versions.toml`).
3. Run the app's checks (`make ci`, `npm run lint && npm test`, `dotnet test`).
4. If a check fails, find the one package that caused it, pin it to its previous version with a comment, and open an issue for it. Do not hold back the rest.

## 3. Major updates

One major update per pull request:

1. Read the release notes and migration guide end to end. Note breaking changes that touch this repo.
2. Check the platform skill first: Android has `agp-9-upgrade` for the Android Gradle Plugin; the web skills cover React and Vite.
3. Make the change, then fix every compiler warning (warnings are errors in this repo).
4. Run the full checks for every app that uses it; for shared things (design tokens, backend API) run the apps that depend on them too.
5. If the upgrade changes how the system is built (a new framework, minimum OS version, a new build tool), write an ADR (`architecture-decisions`).
6. Update versions mentioned in READMEs and tutorials.

## 4. After every update

* `node scripts/security-audit.mjs`: no new findings.
* All required checks green, including **Dependency review**.
* Commit messages: `chore(deps): <app> <package> <old> → <new>`.

## Rules

* Never pin to an old version without a comment and an issue explaining why.
* Never mix a dependency update with feature work in one pull request.
* Keep the iOS and Android apps on comparable minimum OS versions, and the web apps on the same React and Vite majors.
