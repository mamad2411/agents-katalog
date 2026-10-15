---
name: macos-release-readiness
description: Audit macOS app release readiness including app bundle identity, signing, notarization, sandboxing, hardened runtime, permissions, keychain, app support data, launch agents, login items, menu bar, Dock behavior, file associations, universal builds, auto-update, crash logs, backup, uninstall, and support diagnostics. Use when shipping or reviewing macOS desktop apps and utilities.
---

# macOS Release Readiness

Use this skill to make macOS apps feel native, trustworthy, supportable, and safe to update.

## Workflow

1. Identify distribution channel, app type, privileged capabilities, data locations, update mechanism, and support posture.
2. Read `references/macos-release-systems.md`.
3. Audit identity/signing/notarization, sandbox/permissions, local data, keychain, login/background behavior, updates, backup, uninstall, and diagnostics.
4. Separate release blockers from product polish and support improvements.
5. Produce a macOS readiness matrix with proof needed for each high-risk area.

## Guardrails

- Do not hide login items, launch agents, background helpers, screen recording, accessibility, file access, or network behavior.
- Do not store secrets in plist/json/plain local files when platform secure storage is appropriate.
- Do not ship auto-update without signature verification and recovery path.

## Output format

```text
macOS context:
Distribution/update model:

Readiness matrix:
- Identity/signing:
- Permissions/sandbox:
- Data/backup/uninstall:
- Updates/diagnostics:
- Native UX:

Blockers:
- <blocker> -> proof required

Support diagnostics:
- <field/log/user action>
```
