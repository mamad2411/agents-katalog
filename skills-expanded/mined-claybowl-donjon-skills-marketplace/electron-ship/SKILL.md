---
name: electron-ship
description: >
  Use this skill whenever the user wants to ship a web app (Node + Vite +
  React, or similar) as a desktop Electron app — covering port, packaging,
  code signing, notarization, and automatic updates. Triggers on phrases
  like "ship as electron", "make this a desktop app", "electron packaging",
  "code sign electron", "notarize", "electron auto-update", "electron-updater",
  "release pipeline", "github releases electron", "dmg", "exe installer",
  or "AppImage". Also triggers on anxiety signals like "I've never shipped
  a desktop app" or "is auto-update hard?" — the skill is designed to
  calibrate expectations and walk each phase. Use proactively whenever
  Electron is mentioned; most users underestimate the cross-phase planning
  needed and the skill bundles copy-paste configs.
metadata:
  version: 0.1.0
  author: Donjon Intelligence Systems
license: MIT
---

# Electron Ship — A Field Guide for Desktop App Distribution

Everything needed to turn a web application (Node + Vite + React, or similar) into a signed, auto-updating desktop Electron app. The guide walks through four phases end-to-end, with references and copy-paste examples for each.

## Calibration — what you're actually in for

Shipping an Electron app has a reputation for being hard. Most of that reputation is earned by **three one-time setup tasks** that compound into a wall:

1. Apple Developer Program enrollment + Mac code signing + notarization
2. Windows code signing (EV cert, usually via a cloud signing service)
3. Release CI/CD pipeline (matrix build, sign, notarize, publish to GitHub Releases)

**Once those three tasks are done, releasing a new version is one command.** That isn't marketing — it's the literal workflow: `npm version patch && git push --follow-tags`. This skill walks you through each task once so "the hard part" becomes "the done part."

Special note for first-timers who are nervous about auto-update specifically: the polling + delta-download + prompt-to-restart dance is a library call, not a system you build. The hard parts all live upstream in signing + CI. Fix those once and the auto-update layer works.

## The four phases

```
┌──────────┐    ┌───────────┐    ┌──────────┐    ┌──────────┐
│   Port   │ ─▶ │  Package  │ ─▶ │   Sign   │ ─▶ │  Update  │
└──────────┘    └───────────┘    └──────────┘    └──────────┘
  scaffold     electron-builder  Apple/Windows  electron-updater
  + wire        config + icons     certs + CI    + GH Releases
```

Do them in order. You can't meaningfully sign before packaging works; you can't ship auto-update before signing works. Resist the urge to start at the end.

## Phase 1: Port — Get a running Electron binary

**Goal:** `pnpm dev` opens a window; the app works; a local package step produces a `.dmg`/`.exe`.

### The one rule that saves weeks

**Fork a scaffold. Do not hand-wire Electron from scratch.** Scaffolds have already solved the main/renderer/preload split, Vite integration, HMR, IPC boundary, and CI. Starting from scratch means rediscovering every one of those problems.

See `references/scaffold-selection.md` for the decision matrix. Short version:

| Existing stack | Recommended scaffold |
|---|---|
| React + Vite + Tailwind + shadcn | `luanroger/electron-shadcn` |
| React + Vite (plain) | `electron-vite/electron-vite-react` |
| Vue + Vite | `electron-vite/electron-vite-vue` |
| Svelte / Solid / other | `alex8088/electron-vite` base |
| Canonical / large / plugin-heavy | `electron/forge` |

### The 60-minute first-run path

1. Clone the chosen scaffold to a scratch directory. `pnpm install && pnpm dev`. Confirm the baseline app window opens.
2. Run the scaffold's package step end-to-end (usually `pnpm package` or `pnpm make`). Confirm a `.dmg` / `.app` / `.exe` appears in `dist/` or `out/`. If this step fails, fix your toolchain (Xcode CLTs, Python, node-gyp) before proceeding.
3. Create an `electron-port` branch in the real repo.
4. Copy the existing Vite + React source into the scaffold's `src/renderer/`. Reconcile imports and Tailwind config.
5. If the app has a local Express/Fastify/Koa server, spawn it as a child process in `src/main/main.ts` on `app.whenReady()`, kill it on `app.on('before-quit')`. (For a type-safe alternative, see `electron-trpc`.)
6. Replace hardcoded filesystem paths with `app.getPath('userData')` for mutable data, `process.resourcesPath` for bundled read-only assets.
7. Rebuild native modules if present: `pnpm add -D @electron/rebuild && pnpm rebuild`. Add to postinstall.
8. Smoke test: app window opens → UI renders → hits `/api/health` (or equivalent) → 200.
9. Commit to the `electron-port` branch. Push. You have a baseline.

### Three porting gotchas that always bite

1. **Hardcoded paths.** `./data/app.db` works in dev, breaks once packaged. Fix: `path.join(app.getPath('userData'), 'data', 'app.db')`.
2. **Native modules against wrong Node ABI.** `better-sqlite3`, `keytar`, `bcrypt`, `node-pty`, anything with `binding.gyp`. Fix: `@electron/rebuild`, every install.
3. **CORS between dev renderer and dev server.** Dev renderer on `:5173`, server on `:3100`. Enable CORS in dev only, or load renderer through the server's origin in prod.

## Phase 2: Package — Configure electron-builder

**Goal:** a production installer for each target platform, generated from config.

The key file is `electron-builder.yml` (or the `build` block in `package.json`). The three fields that matter most:

- **`appId`** — reverse-DNS identifier. **Never change this after shipping** — users with older versions won't upgrade cleanly.
- **`productName`** — the user-facing app name. Shows in Finder / Start Menu.
- **`publish.provider`** — where auto-update assets live. Default: `github`.

A complete working config is in `assets/electron-builder.yml`. Full configuration reference with platform-specific targets, icons, and entitlements: `references/packaging.md`.

**On installer targets for Windows:** use `nsis` or `nsis-web`, **not** `msi`. MSI installers fight with electron-updater and cause UAC loops.

## Phase 3: Sign — Platform certificates + CI

This is the part that sounds scariest and is actually the most deterministic. You do it once; you maintain it yearly.

### macOS signing

**Required:** Apple Developer Program ($99/yr) + Developer ID Application cert + app-specific password for notarization.

**Why:** Since macOS 10.15 (Catalina), apps distributed outside the App Store must be signed AND notarized. Without both, users see "Apple could not verify this app is free of malware." Most will not click through.

**The flow:**
1. Enroll in Apple Developer Program (1–3 business days).
2. Create a Developer ID Application certificate; install in Keychain.
3. Export as `.p12` file; base64-encode for CI.
4. Generate an app-specific password for notarization.
5. Set five GitHub secrets: `MAC_CERTIFICATE`, `MAC_CERTIFICATE_PASSWORD`, `APPLE_ID`, `APPLE_APP_SPECIFIC_PASSWORD`, `APPLE_TEAM_ID`.
6. CI imports cert into a temporary keychain, runs `electron-builder --mac`, which signs + notarizes + staples in one pass.

Full walkthrough with GitHub Actions YAML: `references/macos-signing.md`.

### Windows signing

**Required:** EV code signing certificate. Recommended path: cloud signing service like **SignPath** (~$150/yr small orgs).

**Why:** Without EV signing, Windows SmartScreen warns users until cert reputation builds (weeks, thousands of installs). With EV, reputation is immediate.

**Three paths:**

| Path | Cost | Pain | Recommended for |
|---|---|---|---|
| Cloud signing (SignPath / Certum / DigiCert KeyLocker) | $150–400/yr | Low | Most teams |
| Self-hosted EV hardware token (DigiCert / Sectigo) | $300–500/yr | Medium (need self-hosted Windows runner) | Teams with existing infra |
| Standard (OV) cert | $80–150/yr | Low budget, high UX pain | Avoid for new apps |

Full walkthrough including SignPath integration: `references/windows-signing.md`.

### Linux

Signing is not required. Optional GPG signature for power users. Skip for v1.

## Phase 4: Update — electron-updater + GitHub Releases

**Goal:** users on v1.0.0 automatically see v1.0.1 when you publish it. Download in the background; install on quit.

### The mental model (three moving parts)

1. **Your app** has `electron-updater` embedded. On launch (default) or on a timer, it polls a feed URL.
2. **The feed** is a set of JSON manifests + binary files, hosted on GitHub Releases. `electron-builder` writes the manifests automatically when it publishes.
3. **electron-updater** reads the feed, sees a newer version, downloads the delta, verifies the signature against the current cert, prompts the user to restart.

That's the whole system.

### Minimum viable wiring

```typescript
// src/main/main.ts
import { autoUpdater } from 'electron-updater';
import log from 'electron-log';

autoUpdater.logger = log;
log.transports.file.level = 'info';

app.whenReady().then(() => {
  // ...create window...
  autoUpdater.checkForUpdatesAndNotify();
});
```

```yaml
# electron-builder.yml
publish:
  provider: github
  owner: your-username
  repo: your-repo
  private: true   # or false for public repos
```

**Then cut a release:**

```sh
npm version patch   # bumps package.json + creates git tag v1.0.1
git push --follow-tags
```

CI (complete workflow in `assets/release.yml`) builds on macOS + Windows in parallel, signs, notarizes, publishes to GitHub Releases. ~15–25 minutes later a release is live. `electron-updater` picks up the new version on next app launch.

Full walkthrough with private-repo handling, alternative hosts (S3, Hazel), and channels: `references/auto-update.md`.

### Test the pipeline before real users hit it

The most-skipped step and the source of most "auto-update doesn't work" tickets:

1. Build and sign v1.0.0 via your real CI. Publish.
2. Install v1.0.0 on a clean VM or second machine. Launch. Confirm it works.
3. Build and publish v1.0.1 via your real CI.
4. Launch the installed v1.0.0 app. Wait 30–60 seconds.
5. Confirm update prompt → download → restart as v1.0.1.

If all five steps pass, your pipeline is real. Skip this at your peril — subtle misconfiguration only shows up here, not in local `pnpm dev`.

## The five failure modes that bite in the wild

When auto-update breaks in production, it's almost always one of these. Full triage guide in `references/failure-modes.md`.

1. **Update not detected.** Feed URL wrong, or new release not marked "latest" on GitHub.
2. **Download fails.** Private repo + missing `GH_TOKEN` at runtime, corporate firewall, CDN block.
3. **Install fails / signature mismatch.** Cert rotated between versions — electron-updater refuses. Fix: stable cert across releases.
4. **Version mismatch.** `package.json` version ≠ git tag. Feed reports stale version. Fix: use `npm version` to bump + tag atomically.
5. **Windows UAC loop.** Wrong installer target (`msi` instead of `nsis`). Fix: switch to `nsis`.

## Rollback strategy

`electron-updater` does not natively support downgrades. Plan for **forward-fix, not rollback**:

- **Primary:** ship v1.0.2 that fixes v1.0.1's bug. Users get a real fix within a release cycle.
- **Secondary:** unpublish the bad GitHub Release. New installs fall back to the previous "latest"; users already on the bad version stay on it until v1.0.2 ships.
- **Never:** try to force downgrade. electron-updater will fight you, and users will end up with broken installs.

Treat every release as if you can't un-ship it. Run the test-pipeline steps on every major version.

## Cost reality check

Annual recurring costs for a signed, auto-updating Electron app:

| Setup | Annual cost |
|---|---|
| Mac only | $99 (Apple Developer Program) |
| Mac + Windows (cloud signing) | ~$250 ($99 Apple + ~$150 SignPath) |
| Mac + Windows (self-hosted EV token) | ~$400 ($99 Apple + ~$300 EV cert) |
| Linux only | $0 |

First-year setup can include one-time costs: a Windows hardware token if self-hosting, or enrollment delays with Apple.

## What's explicitly not in scope

- **Mac App Store distribution.** Different sandbox, different signing, different update model. See Apple's docs.
- **Staged rollouts.** Possible but requires custom feed manipulation. Defer until you have 10,000+ users.
- **Self-hosted update servers** (Hazel, custom S3). GitHub Releases handles 95% of cases.
- **Native OS features** (tray, menu bar, deep links, protocol handlers). Scaffolds usually provide patterns; orthogonal to shipping.

## References

Read each when you're in the corresponding phase.

| File | When to read |
|---|---|
| `references/scaffold-selection.md` | Phase 1 — picking the right starter |
| `references/packaging.md` | Phase 2 — electron-builder config deep dive |
| `references/macos-signing.md` | Phase 3 — Apple Developer, cert, notarization flow |
| `references/windows-signing.md` | Phase 3 — EV cert, SignPath, SmartScreen reputation |
| `references/auto-update.md` | Phase 4 — electron-updater + GitHub Releases complete setup |
| `references/failure-modes.md` | Any phase — triage guide for the five common failures |

## Copy-paste examples

Starting points — edit appId / owner / repo and go.

| File | Purpose |
|---|---|
| `assets/electron-builder.yml` | Full electron-builder config with signing + publishing |
| `assets/release.yml` | GitHub Actions workflow for matrix build + sign + notarize + publish |
| `assets/entitlements.mac.plist` | macOS entitlements plist required for notarization |
