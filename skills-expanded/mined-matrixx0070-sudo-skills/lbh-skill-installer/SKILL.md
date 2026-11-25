---
name: lbh-skill-installer
version: 1.0.0
description: Install a legal skill that has cleared the security gate — verify the pinned version, confirm integrity, record provenance, and enable it safely.
author: matrixx0070
tags: [legal, install, provenance, integrity, enable]
capabilities: []
---

## When to use

Use this once a candidate legal skill has a PASS verdict from `lbh-skills-qa` and the user wants it added to their hub. You perform the mechanical install: confirm the artifact matches what was reviewed, record where it came from, and enable it in a disabled-safe way.

**Not for:** vetting (that is `lbh-skills-qa` — never install an unreviewed skill), tuning behavior after install (`lbh-customize`), or removing one (`lbh-uninstall`).

## Method

1. Require the QA verdict. Refuse to proceed without a PASS or PASS-WITH-CONDITIONS for the exact `name@version`.
2. Resolve the pinned version. If the request says "latest", re-pin to a concrete version and confirm it matches the reviewed one; if it drifted, send it back to QA.
3. Verify integrity: the artifact's checksum matches the reviewed artifact. Any mismatch aborts the install.
4. Apply any PASS-WITH-CONDITIONS constraints (e.g. sandbox-only, no network) as install-time settings, not honor-system notes.
5. Install disabled-first, then enable explicitly, so a surprise is inert until the user opts in.
6. Record provenance: source URL, version, checksum, QA verdict, installer, timestamp — the audit trail that makes rollback and uninstall clean.

## Example

`saas-agreement-eu-review@2.1` passed QA with condition "no network". You confirm the registry artifact checksum equals the reviewed one, write the provenance record, apply a network-off constraint, install it disabled, then enable it. The user sees it live; the audit log shows exactly which version and checksum are running.

## Pitfalls

- Installing "latest" when QA reviewed a specific version. The running artifact must equal the vetted one, byte for byte.
- Skipping the checksum step, so a registry-side change slips in post-review.
- Enabling before the user asks. Install disabled-first; enabling is a separate, explicit act.
- Treating PASS-WITH-CONDITIONS as advice. Encode conditions as enforced settings or do not install.

## Output format

```
# Install Record — <name>@<version>
QA VERDICT: <PASS|PASS-WITH-CONDITIONS(...)> (required)
VERSION: pinned=<ver> matches-reviewed=<y/n>
INTEGRITY: checksum=<hash> match=<y/n>
CONDITIONS APPLIED: <sandbox-only | no-network | ...>
STATE: installed disabled -> enabled=<y/n>
PROVENANCE: source=<url> installer=<who> at=<ts>
```

## Reference

**Skill-vetting checklist (install link):** installation is gated on a QA PASS for the exact version; an install with no verdict on file is invalid.

**Security-review gate criteria:** PASS-WITH-CONDITIONS constraints (sandbox, no-network, no-write) must be enforced at install time; a checksum mismatch is treated as a failed gate and aborts.

**Versioning / rollback:** every install records `name@version` + checksum + provenance, so `lbh-auto-updater` can diff and `lbh-uninstall` / rollback can restore the exact prior state.
