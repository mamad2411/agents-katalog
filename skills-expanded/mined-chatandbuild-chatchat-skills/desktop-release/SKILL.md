---
id: desktop-release
name: Desktop Release
description: Use this skill when planning or executing desktop application releases, including repeatable builds, signing, packaging, release candidates, rollout checks, and cross-platform production readiness.
category: DevOps
---

# Desktop Release

Ship desktop versions safely with clear release gates, artifact verification, and rollback paths.

## When to Use

- You are preparing a new desktop app version for users.
- You need a reliable signing/notarization/package workflow.
- You want pre-release checks for installers and auto-update channels.

## Release Engineering Patterns

**Reproducible builds.** Build only from tagged commits (e.g. `v1.2.3`). Use deterministic environment variables, lockfiles, and CI to ensure identical artifacts across runs. Avoid building from arbitrary branches or uncommitted changes.

**Code signing.** macOS: Sign with Apple Developer ID and hardened runtime; use `codesign --deep` only when necessary. Windows: Use Authenticode with an EV or standard code-signing certificate; sign all executables and installers. Linux: GPG-sign packages and provide detached `.asc` files for distro maintainers.

**Notarization (macOS).** Use `xcrun notarytool submit` for Apple notarization. Store credentials in keychain or environment; avoid hardcoding. Wait for notary completion before stapling (`xcrun stapler staple`). Gatekeeper requires notarization for apps distributed outside the Mac App Store.

**Build tooling.** electron-builder: Configure `mac.identity`, `win.certificateFile`, `linux.executableName`; use `afterSign` hooks for notarization. electron-forge: Use `@electron-forge/maker-*` makers and `@electron-forge/publisher-*` publishers; integrate notarization via `afterSign` in `forge.config.js`.

## Auto-Update Channel Management

**Squirrel (macOS/Windows).** Host `RELEASES` manifest and delta/full nupkg files. Ensure `RELEASES` lists correct version, filename, and SHA1. Clients parse this manifest to decide which files to fetch.

**electron-updater.** Configure `provider` (generic, GitHub, S3, etc.), `channel` (stable/beta/alpha), and `updaterCacheDirName`. Use `allowDowngrade: false` unless you need rollback. Set `autoDownload` and `autoInstallOnAppQuit` per product requirements.

**Staged rollout.** Use percentage-based rollout (e.g. 5% -> 25% -> 50% -> 100%) by serving different `latest.yml` or equivalent manifests to subsets of users. Implement server-side logic or CDN rules to vary response by user segment. Monitor crash rates and error telemetry before increasing percentage.

## Common Pitfalls

- **Expired certificates.** Code signing certs expire; notarization requires valid Apple Developer credentials. Check expiry before release and renew proactively.
- **Notarization timeout.** Large binaries or Apple service delays can cause timeouts. Retry with `--wait`; consider splitting very large apps.
- **Wrong auto-update manifest.** `latest.yml` or `RELEASES` pointing to a previous version causes clients to skip updates or fetch wrong binaries. Validate manifest contents before publishing.
- **Missing checksums.** Installers without SHA256/SHA512 or detached signatures break integrity verification. Always publish checksums and signatures alongside artifacts.
- **Single-OS testing.** Behavior differs across Windows/macOS/Linux. Test install, upgrade, and uninstall on each target OS; use clean VMs or CI runners per platform.

## Workflow

1. Freeze release scope and confirm versioning/changelog.
2. Build reproducible artifacts per platform from a tagged commit.
3. Perform signing/notarization for each target OS.
4. Validate installers and first-run flows on clean environments.
5. Test upgrade paths from at least one prior stable version.
6. Publish artifacts and update metadata for auto-update channels.
7. Roll out in stages and monitor crash/error telemetry.

## Release Checklist

- [ ] Checksums and signatures verified for all artifacts.
- [ ] Changelog reflects user-visible changes and known issues.
- [ ] Auto-update manifest points to correct binaries.
- [ ] Rollback steps are documented and tested.

## Output Format

Return:

- **Release plan:** Scope, version, gating criteria, and timeline.
- **Artifact matrix:** Table with columns: platform, architecture, file path, size, checksum (SHA256), signature status, notarization status (macOS).
- **Validation results:** Install/upgrade test outcomes per OS; first-run and auto-update verification; any failures or known issues.
- **Remaining risks:** Unresolved items, mitigations, and acceptance criteria for go/no-go.
- **Rollout/rollback instructions:** Staged percentage steps, manifest rollback procedure, and telemetry thresholds for abort.

## Constraints

- Do not publish unsigned or unverified binaries.
- Keep release notes aligned with actual shipped commit.
- Avoid full rollout before canary/staged validation.