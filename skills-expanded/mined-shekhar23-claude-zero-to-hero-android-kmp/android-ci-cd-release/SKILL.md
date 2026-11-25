---
name: android-ci-cd-release
description: |
  Android CI/CD and release patterns - build validation, test pipelines, signing, versioning, flavors, Play rollout, release automation, and secrets handling. Use this skill whenever setting up GitHub Actions or other CI, preparing signed builds, managing release tracks, or automating checks for pull requests and production releases. Trigger on phrases like "CI", "CD", "GitHub Actions", "release", "signing", "versioning", "Play Console", "flavors", or "build pipeline".
---

# Android CI/CD and Release

## Core Principles

- Every pull request should prove the app still builds and the critical tests still pass.
- Release pipelines should be reproducible, minimal, and auditable.
- Signing material and secrets must never live in source control.
- Versioning strategy should be deterministic.
- Release automation should reduce manual risk, not hide critical decisions.

---

## Recommended Pipeline Layers

A healthy Android pipeline usually has three levels:

1. **PR validation**
   - dependency resolution
   - lint/static analysis
   - unit tests
   - assemble at least the main debug target

2. **Main branch validation**
   - everything in PR validation
   - instrumentation/UI tests if available
   - publishing of internal artifacts if needed

3. **Release pipeline**
   - signed bundle generation
   - release notes/changelog generation
   - upload to the correct store track
   - tagging and version tracking

---

## Minimum PR Checks

For most Android repos, the minimum CI checks are:

- Gradle wrapper validation
- build logic/config validation
- `lint`
- unit tests
- assemble debug or the main app variant

If the project is modular, add targeted jobs for changed modules only only when the optimization is clearly worth the added complexity.

---

## Versioning

Choose one strategy and keep it consistent.

### Simple app versioning

- `versionName` -> human-readable release version, e.g. `1.4.0`
- `versionCode` -> monotonically increasing integer for Play

### Good practices

- derive release metadata from tags or a release input
- never decrease `versionCode`
- keep version generation centralized, not scattered across scripts

For multi-flavor apps, keep flavor-specific suffixes explicit.

---

## Build Variants and Flavors

Use flavors only when there is a real business/runtime difference such as:
- dev / staging / production environments
- white-label distributions
- region-specific behavior

Do not create extra flavors for minor toggles that can live behind config flags.

CI should build the variants that matter most:
- debug for fast validation
- release for signing/publishing validation
- staging if it is the real pre-production target

---

## Signing

Signing keys, passwords, and service credentials must be injected at build time from secure CI secrets or an external secret manager.

Rules:
- never commit keystores or plaintext passwords
- decode/sign material only inside the CI job that needs it
- scope secrets to the smallest possible environment
- rotate credentials when team or environment ownership changes

---

## GitHub Actions Guidance

For GitHub Actions-based Android repos, a clean setup usually includes:
- one workflow for pull requests
- one workflow for release/tag builds
- shared Gradle caching
- JDK setup pinned to the project requirement
- explicit artifact upload for APK/AAB outputs when helpful

Typical job stages:
1. checkout
2. JDK setup
3. Gradle cache
4. lint/test/assemble
5. artifact upload or release publish

---

## Release Tracks

A common promotion path is:

```text
internal -> closed testing -> open testing -> production
```

Use staged rollouts for production when risk is non-trivial.

Recommended rules:
- internal for fast QA and developer validation
- closed testing for controlled user verification
- production rollout in stages for meaningful releases

---

## Changelog and Release Notes

Release notes should explain user-visible change, risk, and migration impact.

Good inputs:
- merged PR titles curated before release
- conventional commit summaries if the repo uses them
- manual notes for important operational details

Do not auto-publish raw commit noise directly to end users.

---

## Quality Gates

Useful gates before production:
- all required CI checks green
- release variant assembled successfully
- signing validated
- smoke test completed
- version bumped correctly
- mapping/proguard artifacts archived if needed

If the app uses Compose/UI tests or screenshot tests, run them on the branch or release path where they add the most confidence.

---

## Secrets and Configuration

Use environment-specific config without hardcoding secrets:

- local development -> `local.properties` or local env files
- CI -> encrypted secrets / secure variables
- runtime secrets -> backend-provided or remote config when appropriate

Do not embed production-only secrets in the APK if they can live on the server instead.

---

## Release Automation Boundaries

Good automation:
- generating signed artifacts
- attaching artifacts to a release
- uploading to test tracks
- tagging versions
- producing release metadata

Still keep human review for:
- production rollout approval
- major migration releases
- emergency rollback decisions

---

## Observability and Rollback

A release process is incomplete without rollback readiness.

Before rollout, ensure:
- crash reporting is active
- important analytics/health dashboards are monitored
- rollback or halt steps are documented
- previous stable artifact can be reproduced or retrieved quickly

---

## Checklist: Adding CI/CD

- [ ] Add PR workflow for lint, tests, and debug assemble
- [ ] Add release workflow for signed bundle generation and publishing
- [ ] Centralize `versionCode` and `versionName` strategy
- [ ] Inject signing and store credentials securely
- [ ] Define release tracks and rollout rules
- [ ] Document rollback and release verification steps