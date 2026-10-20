---
name: entra-identity
description: "Enumerate and analyze Entra ID (Azure AD) in hybrid estates \u2014 tenant, users, roles, app/service-principal permissions, conditional-access posture, and on-prem to cloud trust. Read-only enumeration and analysis; active token or permission abuse is approval-gated."
version: "1.0.0"
author: redteam-ops
license: Apache-2.0
allowed-tools: Bash Read Write
---

# Entra Identity

> **Runtime: Claude Code.** Helper scripts are in this skill's `scripts/` directory; in commands below, `<skill-dir>` is the absolute skill path provided when the skill loads. `<active-engagement>` is the engagement folder path recorded in `~/.claude/engagements/active` (set by the engagement-setup skill) — read it before resolving paths. Active scope: `<active-engagement>/scope.yaml`. Write outputs to the engagement's numbered subfolders (01-recon, 03-evidence, 04-findings, 05-changes, 07-reports, logs/ — see that folder's CLAUDE.md). Tools are restricted to `Bash Read Write`; irreversible actions are governed by the F0RT1KA permission wall (`~/.claude/hooks/offensive-gate.py`) per the engagement's `autonomy.mode` — `gated` forces a Bash permission prompt, `supervised-auto` allows after a stage briefing.


CLOUD IDENTITY phase. Enumerate and analyze Entra ID (Azure AD) in hybrid estates — tenant,
users, roles, application/service-principal permissions, conditional-access posture, and
on-prem ↔ cloud trust. Read-only enumeration and analysis; any active token or permission abuse
is **approval-gated**.

## When to Use

- When the estate is hybrid (Entra-joined or synced) and the tenant is in scope.
- When asked to "enumerate the tenant", "check conditional access", or "map cloud roles / app permissions".

## Quick Reference

| Tool                       | Role |
| -------------------------- | ---- |
| `AzureHound`               | BloodHound graph for Entra (read-only collection) |
| `ROADtools` (`roadrecon`)  | tenant enumeration and offline analysis (read-only) |
| `az` CLI / Graph (read)    | read role/app/CA configuration with the available token |

Look for: over-privileged apps/service principals, weak or absent conditional access, dangerous
role assignments, and hybrid-trust paths (sync/federation, sync-account exposure).

## Procedure

1. **Scope first.** Confirm the tenant/domains are in scope (`--action active_scan` for authenticated reads). A tenant is shared infrastructure — be precise about what is authorized.
2. **Enumerate.** Run AzureHound/ROADtools collection with the available (low-privilege) identity — read-only.
3. **Conditional access + roles.** Review CA policies, privileged role assignments, and app/service-principal permissions and consent grants.
4. **Hybrid trust.** Map sync/federation (PHS/PTA/federation), sync-account exposure, and on-prem→cloud / cloud→on-prem paths.
5. **Plan, don't execute.** Flag abuse paths (token replay, illicit consent, CA gaps) with their reversibility. Active abuse is gated (`scope_check` `exploitation` + approval).
6. **Output.** A cloud-identity findings set feeding `ad-attack-paths` (hybrid chains) and the report. Write to `<active-engagement>`.

## Pitfalls

- **Tenant = shared infra.** Over-broad enumeration can touch unauthorized objects — scope tightly.
- **Tokens are sensitive and portable** — handle and redact them like credentials.
- **CA "gaps" need verification** — a policy may apply elsewhere; confirm before reporting.
- **Cloud logging is rich** (sign-in/audit) — expect detection and coordinate.

## Verification

- A tenant/CA/role/app inventory is produced and hybrid trust is mapped.
- No active abuse occurred without approval; tokens are handled as secrets.
