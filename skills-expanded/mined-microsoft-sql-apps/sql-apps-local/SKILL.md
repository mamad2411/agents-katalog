---
name: sql-apps-local
description: "Use when checking SQL Apps prerequisites, selecting SQL/workspace, or starting, resuming and stopping locally."
---

# Run SQL Apps locally

Resolve `../../scripts/sql-apps.mjs` relative to this skill, not cwd. Quote its
absolute path; `home` selects the app containing input `docs/...`.
Never run from plugin caches or silently rebind. Own lifecycle, not domain acceptance.

## Plan and approve

Run `guide`, then `setup plan --json` for prerequisites, restore/build, workspace,
terms and lifecycle. `role-based-data` (SQL, DAB, gateway) is the only profile.

`SQL_APPS_FOUNDATION_HOME` selects bootstrap tooling for planning/restore only.
After restore, re-run `setup plan`
through the pinned package and review changed approvals before continuing;
never use a foundation runtime fallback.

Present known effects together. Obtain approval before printed `setup approve`
and `setup run`; `setup resume` follows corrections.
Never manufacture a grant, bypass a blocker or treat failures as success. Unavailable controls capture
nothing; autonomy is not consent.

Progressive creation keeps one public origin; `creation status` is read-only.
Review `docs/reference/progressive-creation.md` for check/restart/owned-stop.
Setup grants remain separate; report milestones/new blockers, not repeated waits.

## Keep database alternatives actionable

Prefer **Azure SQL container -> Azure SQL directly -> SQL Server 2025 Express**.
Missing preview access/Docker: offer the next reviewed route while app work
continues. Endpoint routes need pinned host DAB and .NET/ASP.NET Core 8.0, not Docker.
Use `--sql-provider` and absolute nonsecret `--sql-target` JSON for planning and
approval. Keep saved targets sticky; never silently fail over, migrate data or
present empty/mock persistence as previous data. Diagnose unknown probes and
ownership mismatches instead of switching.

Azure: reuse an explicitly selected dev database or separately review
`setup azure-plan`/`azure-provision`: subscription/tenant, identity, exact-IP
firewall, free-only costs. Refusal never authorizes paid provisioning/publishing.
CLI installation/login remain explicit.

Express: supported Windows x64, SQL Server 2025 Express only. Inspect existing
instances; choose explicitly. Never upgrade, replace or install over
older/broken/unverified instances. Review `setup install-plan sql-express`,
including its pinned Microsoft installer and license/privacy acceptance.
`configure-express` (containment/TCP/restart) and `configure-express-auth`
(mixed-mode/restart) require separate administrator `grant --once` approvals; SA remains untouched.

## Missing tools and lifecycle

Review `setup install-plan <tool>` source, command, downloads, disk/privilege
effects and continuation. Execute unchanged only after approval. Never bootstrap
managers, overwrite versions, self-elevate, reboot, open firewalls or disable
security controls. Credentials belong in the user's terminal, never chat/source.

Run `workspace-check` before lifecycle commands. Resolve source/binding/provenance
mismatches through explicit application selection, never copied state.
Reuse only matching `/local/workspace` identity and `/health/ready`: checkout,
source, workspace, profile, authentication and SQL provider/target fingerprint
(or unchanged container identity). Liveness alone is insufficient.

`app` initializes SQL/DAB/gateway; `serve` reuses running dependencies; `stop`
stops only verified owned DAB. Preserve SQL data and credentials; never stop
unrelated processes. Recovery/destructive cleanup need separate approval.
Keep commands attached. Endpoint Ctrl+C stops gateway and host DAB, not SQL;
use `app` afterward. Container Ctrl+C leaves SQL/DAB running.
Examples require explicit selection; otherwise keep `selectedExamples: []`.

## Verify completion

Label early status URLs as creation. Ready requires current browser workflow and
required rendered browser review via `sql-apps-validation`; Usable is review pending.
Explain stop/resume. Simulation is not cloud authorization; publishing is optional.
