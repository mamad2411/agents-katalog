---
name: desktop-code-signing
description: Code-signing and notarization specialist. Owns signing keys, certificates, platform signing (Authenticode, Apple notarization, Linux repos), and CI integration. Auto-invoked when setting up, debugging, or rotating signing.
---

# Desktop Code Signing

An unsigned desktop app is a security warning; a mis-signed one is the same plus
panic. Key custody, timestamping, and rotation are ops work with hard external
deadlines — certificates expire whether or not the runbook exists.

## When to reach for this

- Setting up signing for a new platform or a new CI pipeline
- Debugging Gatekeeper rejections, SmartScreen warnings, or notarization failures
- A certificate is expiring, compromised, or changing issuer
- Deciding where signing keys live and which CI jobs may use them

## Principles

1. **Keys live in an HSM or cloud KMS, never on a laptop or in repo secrets as
   files.** CA/Browser Forum rules have required hardware-backed keys for Windows
   code-signing certs since mid-2023 — plan for HSM or a cloud signing service
   (Azure Trusted Signing, KMS-backed signers), not a `.pfx` in CI.
2. **Timestamp every signature (RFC 3161)** so builds remain verifiable after the
   certificate expires; an untimestamped signature dies with its cert.
3. **Notarization is mandatory on macOS** (10.15+): submit with
   `xcrun notarytool submit --wait`, then **staple** the ticket
   (`xcrun stapler staple`) so first launch passes Gatekeeper offline.
4. **Sign inside-out on macOS** — every nested binary, framework, and helper gets
   signed before the outer bundle; enable hardened runtime and list each required
   entitlement explicitly (notarization rejects the lazy alternatives).
5. **EV starts with SmartScreen reputation; OV earns it** through download volume.
   Budget for a warning-heavy launch window on a fresh OV cert.
6. **Write the rotation runbook before the first expiry**, including how the
   autoupdater handles a publisher-identity change — not during the outage.

## Signing matrix

| Platform | Artifacts | Mechanism | Sign with | Verify with |
|---|---|---|---|---|
| Windows | exe, dll, msi/msix | Authenticode (OV/EV) | `signtool` / AzureSignTool in CI | `signtool verify /pa /v` |
| macOS | .app, .pkg, .dmg | Developer ID + notarization | `codesign` → `notarytool` → `stapler` | `codesign --verify --deep --strict`; `spctl -a -vv` |
| Linux | deb, rpm, repo metadata | GPG | `debsign` / `rpmsign`; sign the repo metadata too | `rpm -K`; apt verifies via the repo keyring |

CI wiring checklist:

- [ ] Key access scoped to the release pipeline only (not PR builds)
- [ ] Signing step pulls from HSM/KMS; no key material in env vars or artifacts
- [ ] Timestamp server configured and failure treated as a build failure
- [ ] Post-sign verify step runs the platform verifier before publishing
- [ ] Rotation runbook: trigger date, owner, steps, updater-compatibility note

## Pitfalls

- Signing without a timestamp — every shipped build invalidates at cert expiry
- Notarizing but not stapling — installs fail Gatekeeper on offline machines
- Signing only the outer installer while nested helpers stay unsigned (macOS notarization rejects; Windows SmartScreen flags)
- Wide-open CI secrets: any branch build able to produce a signed binary
- Changing the signing identity without updating updater pinning — old installs refuse the new release

---
*Related: `desktop-autoupdate` (identity pinning in updaters), `desktop-installer`
(what gets signed per package format), `security-checklist` (key custody) ·
domain agent: `desktop-architect` · output/ADR format: `playbook-conventions`*
