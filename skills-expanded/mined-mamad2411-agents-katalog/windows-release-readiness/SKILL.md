---
name: windows-release-readiness
description: Audit Windows app release readiness including installer/MSIX identity, code signing, SmartScreen reputation, services, startup tasks, tray behavior, registry and file associations, notifications, credential storage, AppData/ProgramData, firewall prompts, auto-update, rollback, uninstall cleanup, crash logs, Microsoft Store certification, and support diagnostics. Use when shipping or reviewing Windows desktop apps and utilities.
---

# Windows Release Readiness

Use this skill to make Windows releases install cleanly, update safely, integrate predictably, and support users across diverse environments.

## Workflow

1. Identify distribution channel, installer type, privileges, background components, data locations, update path, and support posture.
2. Read `references/windows-release-systems.md`.
3. Audit package identity, signing/reputation, install/update/uninstall, startup/services, registry/file associations, notifications, credentials, data, firewall, crash logs, and Store certification if relevant.
4. Separate release blockers from enterprise/admin polish and support improvements.
5. Produce a Windows readiness matrix with proof needed for each high-risk area.

## Guardrails

- Do not request admin rights unless the product needs machine-wide changes.
- Do not hide services, startup tasks, scheduled tasks, firewall rules, drivers, or background agents.
- Do not leave credentials, sensitive logs, startup entries, or broken file associations after uninstall.

## Output format

```text
Windows context:
Distribution/update model:

Readiness matrix:
- Installer/package:
- Signing/reputation:
- OS integration:
- Data/credentials/uninstall:
- Updates/diagnostics:

Blockers:
- <blocker> -> proof required

Support diagnostics:
- <field/log/user action>
```
