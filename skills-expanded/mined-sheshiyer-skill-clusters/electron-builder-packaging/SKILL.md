---
name: electron-builder-packaging
description: "Package and distribute an Electron app — electron-builder/Forge, per-OS installers (dmg/nsis/AppImage/deb), code signing (Apple Developer ID + notarization, Windows Authenticode), and native-module rebuilds. USE WHEN configuring builds, signing, notarizing, or producing installers for macOS/Windows/Linux."
cluster: electron
version: 1.0.0
origin: "skill-clusters (original)"
---

# Electron Builder & Packaging

Turning the app into signed, installable artifacts per OS. Two main tools: **electron-builder**
(declarative `build` config, most common) and **Electron Forge** (plugin-based). Pick one.

## Targets per OS

| OS | Installers | Signing |
|---|---|---|
| macOS | `dmg`, `zip` | **Apple Developer ID** + **notarization** (required for Gatekeeper) |
| Windows | `nsis`, `msi`, `appx` | **Authenticode** code-signing cert (EV reduces SmartScreen friction) |
| Linux | `AppImage`, `deb`, `rpm`, `snap` | optional (repo/GPG) |

## macOS signing + notarization (the gotcha)

- Sign with a **Developer ID Application** cert, enable the **hardened runtime**, and provide
  entitlements (e.g. JIT/`allow-unsigned-executable-memory` only if truly needed).
- **Notarize** (`notarytool`) and **staple** the ticket — unnotarized apps are blocked on modern macOS.
- electron-builder runs this if `afterSign`/`notarize` + Apple API key creds are configured.

## Windows

- Sign the installer **and** the app `.exe` with an Authenticode cert; timestamp it.
- NSIS one-click vs assisted; per-machine vs per-user install.

## Native modules

- Native addons must match **Electron's ABI** — electron-builder runs `electron-rebuild` /
  uses prebuilds at pack time. Mismatch → "module did not self-register" at runtime (`electron-core`).
- Keep `asar` on, but `asarUnpack` native `.node` binaries and other files needing real paths.

## CI

- Build the matrix on real (or VM) macOS/Windows/Linux runners; inject signing certs/keys via CI secrets, never commit them.
- Output a versioned feed for `electron-auto-update`.

## Guardrails

- Always sign **and** (macOS) notarize before distributing — and before enabling auto-update.
- Keep signing keys in CI secrets / a vault; never in the repo.
- Match native modules to Electron's ABI; `asarUnpack` binaries.
- Version artifacts to feed `electron-auto-update`.
