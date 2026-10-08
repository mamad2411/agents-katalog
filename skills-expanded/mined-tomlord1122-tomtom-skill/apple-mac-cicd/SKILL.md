---
name: apple-mac-cicd
description: Establish GitHub Actions macOS CI/CD for signing, notarization, GitHub Releases, and auto-updates. Use when setting up Apple app release pipelines, Developer ID signing, notarization, DMG/ZIP distribution, Sparkle (native), or electron-updater (Electron). Trigger phrases include "mac release CI", "notarize app", "auto-updater", "GitHub Actions macOS".
---

# Apple macOS CI/CD & Auto-Updater

Expert workflow for shipping signed, notarized macOS apps via GitHub Actions with automatic updates. Grounded in the **Cometrans** (native Swift) and **Cometode** (Electron) repos in this workspace.

## Reference Projects

| App | Stack | Release trigger | Auto-update |
|-----|-------|-----------------|-------------|
| Cometrans | Swift CLI → `.app` + DMG | `workflow_dispatch` with version input | Sparkle-ready build numbers (not wired yet) |
| Cometode | Electron + Svelte | Push tag `v*` | `electron-updater` + `latest-mac.yml` |

Read the reference files when implementing:
- [Cometrans pattern](references/cometrans-pattern.md)
- [Cometode pattern](references/cometode-pattern.md)
- [GitHub secrets](references/github-secrets.md)
- [Auto-updater guide](references/auto-updater.md)

## Thinking Process

### Step 1: Identify App Type

**Goal:** Pick the correct release and updater stack.

**Decision Matrix:**

| App type | Build tool | CI runner | Updater |
|----------|-----------|-----------|---------|
| Native Swift / SwiftPM | `build_dmg.sh` or Xcode | `macos-26` (pin Xcode via `DEVELOPER_DIR`) | Sparkle + appcast |
| Electron + electron-builder | `pnpm build:mac` | `macos-latest` | electron-updater + GitHub Releases |

**Decision Point:** State "This is a [native|electron] app; updater will use [Sparkle|electron-updater]."

### Step 2: Apple Developer Prerequisites

**Goal:** Ensure signing and notarization credentials exist before touching CI.

**Checklist:**
- [ ] Apple Developer Program membership
- [ ] **Developer ID Application** certificate (not Mac App Store)
- [ ] `.p12` exported and base64-encoded for CI
- [ ] App-specific password at [appleid.apple.com](https://appleid.apple.com) (for notarytool)
- [ ] Team ID from developer.apple.com

**Actions:**
1. Run `bash /mnt/skills/user/apple-mac-cicd/scripts/validate-secrets.sh` to audit local env
2. Configure GitHub repo secrets (see [github-secrets.md](references/github-secrets.md))

### Step 3: Local Build Script

**Goal:** One script produces reproducible signed artifacts locally and in CI.

**Native (Cometrans pattern):**
- `build_dmg.sh` builds Swift release, assembles `.app`, codesigns with `--options runtime`, creates DMG
- `CFBundleVersion` derived as `major*10000 + minor*100 + patch` for Sparkle semver comparison
- `NOTARIZE=1` triggers `scripts/notarize.sh` via `xcrun notarytool submit --wait` + `stapler staple`

**Electron (Cometode pattern):**
- `electron-builder.yml`: `hardenedRuntime: true`, `notarize: true`, `publish: github`
- mac targets: **dmg + zip** (zip required for electron-updater)
- Entitlements in `build/entitlements.mac.plist` (JIT, unsigned executable memory for Electron)

### Step 4: GitHub Actions Release Workflow

**Goal:** CI builds, signs, notarizes, and publishes to GitHub Releases.

**Native workflow shape** (Cometrans `.github/workflows/release.yml`):
1. `prepare` job — resolve version, create/push tag
2. `build` job — import P12 to ephemeral keychain, run `./build_dmg.sh`, upload artifacts
3. `release` job — download artifacts, `softprops/action-gh-release` with DMG + sha256

**Electron workflow shape** (Cometode `.github/workflows/release.yml`):
1. Trigger on `push: tags: ['v*']`
2. Sync `package.json` version from tag
3. `pnpm build:mac` with signing env vars
4. Upload `dist/*.dmg`, `dist/*.zip`, `dist/*.blockmap`, **`dist/latest-mac.yml`** (critical for auto-update)

**Required secrets by stack:**

| Secret | Native | Electron |
|--------|--------|----------|
| `APPLE_DEVELOPER_ID_P12_BASE64` | ✓ | — |
| `APPLE_DEVELOPER_ID_P12_PASSWORD` | ✓ | — |
| `KEYCHAIN_PASSWORD` | ✓ | — |
| `DEVELOPER_ID_APPLICATION` | ✓ | — |
| `CSC_LINK` | — | ✓ (base64 p12) |
| `CSC_KEY_PASSWORD` | — | ✓ |
| `APPLE_ID` | ✓ | ✓ |
| `APPLE_APP_SPECIFIC_PASSWORD` | ✓ | ✓ |
| `APPLE_TEAM_ID` | ✓ | ✓ |

### Step 5: Auto-Updater Integration

**Goal:** Users receive updates without manual DMG downloads.

**Electron (Cometode — fully wired):**
- `electron-updater` reads `latest-mac.yml` from GitHub Releases
- `electron-builder.yml` `publish.provider: github` must match repo owner/name
- Main process: `autoUpdater.autoDownload = true`, check on startup + every 4h
- Release workflow **must** attach `latest-mac.yml`, `.zip`, and `.blockmap`
- Only enable in production (`if (!is.dev)`)

**Native (Cometrans — build-number ready, Sparkle pending):**
- `build_dmg.sh` already sets `CFBundleVersion` for Sparkle comparison
- To complete: add Sparkle SPM dep, `SUFeedURL` in Info.plist, EdDSA signing key
- CI must generate/sign appcast XML and publish alongside DMG on each release
- See [auto-updater.md](references/auto-updater.md)

### Step 6: CI Workflow for PRs

**Goal:** Catch build breaks before release.

**Native:** `ci.yml` on push/PR — `swift build -c release && swift test` on `macos-26`

**Electron:** Add `ci.yml` with `pnpm typecheck && pnpm build` (no signing needed for CI)

### Step 7: Release & Verify

**Goal:** Ship and confirm auto-update works end-to-end.

**Release checklist:**
- [ ] Bump version in source (`version.txt` or `package.json`)
- [ ] Tag `vX.Y.Z` (Electron) or run workflow_dispatch (Cometrans)
- [ ] CI completes signing + notarization
- [ ] GitHub Release contains all required assets
- [ ] Install previous version, confirm updater finds new release
- [ ] `spctl -a -vv -t install` passes on downloaded artifact

**Verify notarization locally:**
```bash
xcrun stapler validate Cometrans-1.0.0.dmg
# or
spctl -a -vv -t install dist/cometode-1.0.0-arm64.dmg
```

## Usage

### Validate secrets are configured locally

```bash
bash /mnt/skills/user/apple-mac-cicd/scripts/validate-secrets.sh
```

### Scaffold a release workflow

```bash
bash /mnt/skills/user/apple-mac-cicd/scripts/scaffold-release-workflow.sh \
  --type electron \
  --app-name MyApp \
  --output .github/workflows/release.yml
```

**Arguments:**
- `--type` — `native` or `electron` (required)
- `--app-name` — artifact stem, e.g. `Cometrans` (required)
- `--output` — workflow file path (default: `.github/workflows/release.yml`)

## Present Results to User

When helping set up macOS CI/CD, report:
1. **App type** and chosen updater
2. **Secrets** still missing (run validate script output)
3. **Files created/modified** with paths
4. **Release steps** — how to trigger first release
5. **Auto-update status** — wired or remaining steps

## Troubleshooting

**"No signing certificate configured" in CI**
- Verify `APPLE_DEVELOPER_ID_P12_BASE64` / `CSC_LINK` secret is set and decodes to valid P12

**Notarization fails with invalid credentials**
- Regenerate app-specific password; confirm `APPLE_TEAM_ID` matches certificate

**Gatekeeper blocks app despite CI success**
- Ensure `--options runtime` on codesign (native) or `hardenedRuntime: true` (Electron)
- Confirm stapler ran: `xcrun stapler validate <artifact>`

**electron-updater finds no updates**
- Release must include `latest-mac.yml`, `.zip`, `.blockmap`
- `publish.owner` / `publish.repo` in electron-builder.yml must match GitHub repo
- App must be built in production mode (not dev)

**Sparkle shows wrong version order**
- Use numeric `CFBundleVersion` (Cometrans formula: `major*10000 + minor*100 + patch`)
- Never use semver strings in `CFBundleVersion`
