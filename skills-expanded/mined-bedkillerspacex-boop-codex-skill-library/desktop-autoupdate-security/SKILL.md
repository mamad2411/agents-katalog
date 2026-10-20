---
name: desktop-autoupdate-security
description: >
  Secure desktop application auto-update: code signing, update manifest authenticity,
  HTTPS+pinning considerations, differential packages, rollback, privilege separation for
  updaters (Squirrel, Sparkle, MSIF/MSIX, electron-updater, Windows Update-like flows). Use
  when desktop autoupdate, update signature verification, Sparkle appcast, Squirrel releases,
  electron-builder publish, or preventing MITM update hijack on owned desktop apps — not for
  bypassing third-party app update protections.
---

# Desktop Autoupdate Security

## Scope And Authorization

- **In scope:** Desktop apps (Windows/macOS/Linux) you ship; update servers and signing keys you control.
- **Out of scope:** Intercepting or backdooring third-party updaters; distributing trojaned updates.
- Prefer staging update channels before production release rings.
- Protect code-signing certificates and notarization credentials; never commit them.
- Pair with `secrets-management-hygiene`, `code-quality-standards`, and release/CD skills.

## When To Use

- Designing or reviewing auto-update for Electron, Tauri, Qt, .NET, or native apps.
- Ensuring clients reject unsigned or rolled-back malicious packages.
- Moving from HTTP/unsigned feeds to signed manifests (Sparkle EdDSA/DSA, Authenticode, codesign).
- Least privilege for updater services vs main app.
- Incident response: suspected update pipeline compromise.

## Do Not Use As Primary

| Need | Skill instead |
| --- | --- |
| Mobile app store updates | mobile release skills |
| Container image signing (cosign) | supply-chain/container signing skills |
| Secrets/cert storage | `secrets-management-hygiene` |
| General malware reverse of third-party | binary-re skills (authorized) |
| Web CSP / download attribute | `download-attribute-security` |
| Code quality baseline | `code-quality-standards` |

## Threat model (updater)

| Threat | Control |
| --- | --- |
| MITM replaces package | TLS + **signature verify** of package/manifest with app-embedded pubkey |
| Compromised CDN alone | Signatures independent of transport; optional transparency/logging |
| Rollback to vulnerable version | Monotonic version / anti-rollback where product requires |
| TOCTOU replace after verify | Atomic swap; verify then install from immutable path |
| Updater runs as SYSTEM/root always | Split privileges; drop after install |
| Channel confusion (dev feed in prod) | Hard-code channel policy; separate keys optional |
| Server compromise | Offline signing; HSM/KMS; dual control |

## Workflow

### 1. Confirm scope and success criteria

1. Platforms, current updater stack (Sparkle, Squirrel.Windows, electron-updater, custom), and release rings.
2. Success: clients refuse unsigned/bad-sig updates; prod cannot point at unsigned channel without rebuild; signing keys in HSM/secure CI.
3. Define break-glass manual update path for outages.

### 2. Inventory update pipeline

1. Map: build → sign → upload → manifest/appcast → client check → download → verify → install → relaunch.
2. Locate public keys embedded in app and private keys in CI.
3. Check transport: HTTPS only? Certificate pinning? Cleartext fallback?

```bash
# Owned project probes
rg -n "electron-updater|autoUpdater|Sparkle|Squirrel|UpdateManager|appcast" .
rg -n "http://.*update|ALLOW_INSECURE|verifyUpdateCodeSignature|setFeedURL" .
```

### 3. Enforce signing and verification

| Platform | Typical controls |
| --- | --- |
| macOS | Developer ID codesign + notarization; Sparkle EdDSA signature on archive; Gatekeeper |
| Windows | Authenticode on installer/exe; strong update catalog signature; SmartScreen reputation |
| Linux | Signed packages (linter/repo sigs) or app-embedded sig over tarball; flatpak/OS tree policies |
| Electron | `electron-updater` with published signatures; never disable verify in prod builds |

1. Embed **public** verification material in the app; private key only in release signing environment.
2. Sign the **manifest** (URL + version + hash) and/or the artifact; verify before execute.
3. Reject downgrade unless intentional enterprise rollback channel with policy.

### 4. Harden transport and server

1. HTTPS with modern TLS; HSTS on update host.
2. Optional cert/public-key pinning with planned rotation (pin backup keys).
3. CDN: least privilege write; immutable artifact paths including version.
4. Separate dev/beta/prod feeds; prod builds compile-time default to prod feed.

### 5. Client updater behavior

```text
# Secure client algorithm (conceptual)
1. Fetch manifest over TLS
2. Verify manifest signature with embedded pubkey
3. Compare version to local (anti-rollback policy)
4. Download package to temp path
5. Verify package hash + signature
6. Hand off to privileged helper only for replace
7. Launch new binary; health check; else rollback package if supported
```

1. Do not run unsigned scripts from the update archive without verification.
2. Differential updates: verify base hash + patch signature, not only final size.
3. Log failures without leaking signing secrets.

### 6. Key management and CI

1. Offline or HSM signing for production; dual approval for release.
2. Rotate keys with multi-key trust or staged app releases that accept old+new.
3. CI secrets: OIDC to cloud KMS preferred over long-lived exported `.p12` on disk.
4. Incident: revoke, force bump min version, publish known-good build, notify users.

### 7. Verify and hand off

```bash
# Examples — owned artifacts
# macOS
codesign --verify --deep --strict /path/to/App.app
spctl --assess --type execute /path/to/App.app
# Windows (on a Windows admin host you own)
# Get-AuthenticodeSignature .\\Setup.exe
# openssl dgst -sha256 update.tar.gz  # compare to signed manifest
```

1. Negative tests: wrong sig, truncated body, HTTP downgrade, rollback version → all rejected.
2. Document ring rollout % and metrics: update success rate, sig failure rate, forced min version.

## Good / Bad

| Topic | Good | Bad |
| --- | --- | --- |
| Integrity | Signed manifest + artifact | HTTPS only, no signature |
| Keys | HSM/KMS + dual control | p12 in git |
| Channel | Prod pinned feed | User-switchable unsigned URL in release |
| Verify | Before execute | Install then hope |
| Rollback | Policy-controlled | Attacker serves old vulnerable |
| Privs | Limited helper | Always-on SYSTEM updater shell |

## Output Checklist

- [ ] Pipeline map and threat model reviewed
- [ ] Code signing and manifest verification enforced on all platforms
- [ ] HTTPS + no insecure verify bypass in prod
- [ ] Anti-rollback / min version policy decided
- [ ] Key storage, rotation, and dual control documented
- [ ] Negative verification tests pass
- [ ] Privilege separation for install step
- [ ] Incident revoke/force-upgrade plan
- [ ] Release rings and metrics in place
- [ ] Secrets redacted; `code-quality-standards` on updater code

## Rules

- Transport security is necessary but not sufficient—always verify signatures.
- Never ship a production build that can disable update verification via remote config alone without strong auth.
- Protect signing keys as production root of trust for every client.
- Authorized owned apps only; do not attack others’ update channels.
- Focus on desktop autoupdate security, not general malware development.
