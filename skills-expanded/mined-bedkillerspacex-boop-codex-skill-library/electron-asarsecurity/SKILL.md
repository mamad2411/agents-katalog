---
name: electron-asarsecurity
description: >
  Electron asar packaging integrity for owned apps: asar archives, integrity
  validation fuses, unpack directories, resource replacement attacks, and CI
  checks that shipped asar hashes match builds. Use when app.asar,
  asarIntegrity, onlyLoadAppFromAsar, or post-install tampering concerns.
---

# Electron asar Security

## Scope And Authorization

- **In scope:** Packaging and integrity of Electron apps you build and distribute.
- **Out of scope:** Tampering with third-party installed apps on user machines without authorization.
- Integrity helps detect post-build modification; it is not a DRM substitute.
- Protect code-signing certificates and notarization credentials as high-value secrets.
- Pair with `electron-fuses` and `electron-app-security`.

## When To Use

- Enabling asar packaging and integrity validation for production builds.
- Reviewing `asarUnpack` / `extraResources` for writable or replaceable paths.
- Investigating “modified client” / malware-on-top-of-app reports.
- CI gates that fail if integrity metadata is missing.
- Hardening against simple `app.asar` swap attacks on disk.

## Do Not Use As Primary

| Need | Skill instead |
| --- | --- |
| Full Electron security review | `electron-app-security` |
| Fuse bits (runAsNode, etc.) | `electron-fuses` |
| contextIsolation / preload | `electron-context-isolation` |
| Code signing generally | platform signing docs/skills |
| Implementation quality baseline | `code-quality-standards` |

## Domain Focus

| Area | Guidance |
| --- | --- |
| asar | Package app source into `app.asar`; avoid plain `app/` in prod |
| Integrity | Enable Electron asar integrity / related fuses for supported versions |
| Unpack | Minimize unpacked files; treat them as easier to patch |
| Resources | Ship resources read-only; don’t load JS from user-writable dirs |
| Updates | Signed update payloads; verify before replace |
| CI | Record asar hash per release artifact |

## Workflow

### 1. Confirm scope and success criteria

1. Electron version and packager (electron-builder, forge, custom).
2. Success: production artifacts use asar; integrity enabled where supported; unpack list justified.

### 2. Inventory packaging config

```bash
rg -n "asar|asarUnpack|extraResources|files" electron-builder.yml package.json forge.config.* 2>/dev/null
ls -la dist/ 2>/dev/null | head
```

1. Confirm whether `asar: false` exists (red flag for prod).
2. List unpacked globs (native modules often need unpack—document why).

### 3. Baseline tamper surface

1. After install, locate `app.asar` vs `app.asar.unpacked`.
2. Note permissions: can non-admin users overwrite app files?
3. Check if app loads scripts from `%APPDATA%` / user data without signature checks.

### 4. Enable asar + integrity

```json
// electron-builder fragment (illustrative)
{
  "asar": true,
  "asarUnpack": ["**/*.node"],
  "electronFuses": {
    "EnableEmbeddedAsarIntegrityValidation": true,
    "OnlyLoadAppFromAsar": true
  }
}
```

1. Align fuse names with the Electron major you ship—APIs evolve; verify against current Electron fuse docs.
2. `OnlyLoadAppFromAsar` blocks fallback to loose files when asar present.
3. Ensure native `.node` modules still load from unpacked paths intentionally.

### 5. CI and release evidence

```bash
# Hash the asar inside the built payload (path varies by platform)
sha256sum dist/win-unpacked/resources/app.asar
# Store digest next to SBOM / release notes (not a secret)
```

1. Gate release on integrity fuses flipped in the **final** binary (see `electron-fuses`).
2. Sign the installer/DMG/AppImage after packaging, not before.
3. Auto-update: verify signature + hash before replacing asar.

### 6. Verify with evidence

1. Clean install → confirm app runs.
2. Lab-only: modify a byte in `app.asar` (copy first) → expect refuse-to-start when integrity is on.
3. Confirm unpacked paths cannot supply alternate `main` entry.

### 7. Hand off

1. Document unpack exceptions and owners.
2. Runbook for “integrity failure on startup” (corrupt download vs tamper).
3. Coordinate with `electron-app-security` for loader paths outside asar.

## Good / Bad

| Topic | Good | Bad |
| --- | --- | --- |
| Packaging | asar + integrity fuse | Loose app directory in prod |
| Unpack | Only `.node` / known assets | Unpack entire `**/*` |
| Updates | Signed differential packages | HTTP overwrite of asar |
| Loading | Main from asar only | `require` user-selected JS |
| Evidence | Hash in CI artifacts | “Users won’t edit files” |

## Output Checklist

- [ ] asar enabled for production builds
- [ ] Integrity-related fuses enabled and verified on artifacts
- [ ] asarUnpack minimized and justified
- [ ] Release asar hashes retained
- [ ] Lab tamper test documented
- [ ] Update path verifies integrity
- [ ] Residual risk (admin-level attackers, memory patching) noted

## Rules

- Owned apps and authorized labs only.
- Integrity ≠ encryption of IP; don’t pretend otherwise.
- Keep signing keys out of CI logs.
- Pair fuse verification with this skill’s packaging checks.
- Never instruct end users to disable integrity for “support.”
