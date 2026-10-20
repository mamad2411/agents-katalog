---
name: pericles-custom-skill
version: 2026.05.0
description: >
  How customers (and partners) author Custom Skills that extend Pericles for their
  tenant — without forking the platform or escaping the sandbox. Use this WHENEVER you
  build the Custom Skill authoring/review/runtime surfaces, define the sandbox, or
  review a Custom Skill for activation. Encodes §8 extend-never-override, tenant-
  namespace binding, the four-stage review, the sandbox constraints (MCP-only egress,
  no direct DB, allow-listed libs, no direct Execution Node), and lifecycle.
doctrine_refs: [§8; Security Spec §6, §8; Manifest Spec]
depends_on: [pericles-skill-authoring, pericles-tenant-isolation, pericles-security-threat-model, pericles-mcp-layer]
last_reconciled: 2026-05-28
---

# Pericles Custom Skill (build skill)

Standard and Enterprise customers can extend Pericles for their tenant with **Custom
Skills**. The whole value of the platform — one engine, one doctrine — survives only if
these extensions **extend, never override** (§8), stay inside a tight sandbox, and pass
human review before activation. Custom Skills are the highest-risk surface in the
product (`pericles-security-threat-model`); build them conservatively.

## When to use this skill

Building the Custom Skill authoring/review/runtime surfaces; defining the sandbox or
allow-lists; reviewing a Custom Skill for activation; debugging a Custom Skill
incident.

## Identity & namespacing (§8)

A Custom Skill ID **includes the tenant slug**: `custom/<tenant-slug>/<name>@<version>`.
The Skill Registry resolves `tenant/<active>` → `platform` and **can never reach
`tenant/<other>`** (`pericles-tenant-isolation` guarantee 4, `pericles-skill-registry`).
A platform-visibility manifest may not reference a tenant Skill; tenant-depends-on-
platform is the supported extension pattern. **Extend, never override** — a Custom Skill
cannot shadow or replace a platform Skill by ID.

## The sandbox (these are absolutes)

A Custom Skill runs untrusted customer code. It MUST:

- Resolve **only** within `tenant/<active>` + `platform`.
- Reach data **only via MCP** (`pericles-mcp-layer`) — **no direct DB / Prisma access**.
- Have **no filesystem / env / secret access** outside its declared `knowledge_sources`.
- Import **only allow-listed libraries** (the platform team maintains the list).
- **Never invoke an Execution Node directly** — consequential actions go through the
  platform's supervisor/executor path (`pericles-execution-node`).
- Have no network egress outside **registered MCP servers** (non-allowlisted egress is P0).

A sandbox escape, exfiltration, or unauthorized egress is **P0**
(`pericles-security-threat-model`).

## The four-stage review (gates activation)

A Custom Skill cannot be activated for a tenant until it has passed, in order:

1. **Static review** — manifest validation + sandbox-policy check (imports, declared
   `knowledge_sources`, no platform-overriding IDs, no direct DB/Execution-Node calls).
2. **Security review** — threat-model walkthrough against
   `pericles-security-threat-model`; egress allowlist, prompt-injection posture
   (`pericles-prompts`), and capability minimization.
3. **Eval review** — the Skill's `eval_criteria` runs against a tenant-supplied
   reference set; standard promotion gate applies (`pericles-evals-scorers`) — every
   scorer above threshold, no scorer regressing >5%.
4. **Customer sign-off** — the tenant Admin explicitly activates (audited as a
   permission-elevating action — `pericles-admin-portal-ui`).

Reviews are tracked in the manifest `provenance` with links. Failing any stage blocks
activation; a Skill in `draft` or `poc` is not invokable in production.

## Lifecycle & change management

Custom Skills follow the same `draft → poc → published → deprecated → retired`
lifecycle (`pericles-skill-authoring`). Any material change re-runs the four stages.
Post-promotion tamper of a Custom Skill version is P0 (`pericles-tenant-isolation`).

## Express shape: not available

Custom Skills are a Standard/Enterprise feature (`pericles-deployment-shapes`). Express
tenants extend only through configuration; no code-bearing extensions.

## What this forbids

A Custom Skill that shadows a platform Skill ID (§8); reaching outside the tenant
namespace; direct DB / filesystem / secret access; non-allow-listed imports; invoking
an Execution Node directly; egress beyond registered MCP servers; activation without
all four review stages passed; silent re-activation after a material change.

## Verification

Resolver tests confirm `custom/<other>` is unreachable; sandbox tests confirm a
malicious Custom Skill cannot read the DB, the filesystem, env, or non-MCP network;
allow-list violations fail static review; an unreviewed Skill cannot reach `published`;
activation writes an audit-log entry; a P0 runbook is wired.

## Existing standards (read alongside)

Doctrine §8; Skills Security Spec §6/§8; Skill Manifest Spec (lifecycle); `pericles-
security-threat-model`, `pericles-tenant-isolation`, `pericles-mcp-layer`,
`pericles-admin-portal-ui`.

## Open questions

- The exact sandbox runtime (V8 isolate, separate process, container) and how it
  enforces imports + filesystem isolation — define before any Custom Skill ships.
- The library allow-list contents and update cadence — platform-team owned, reviewed
  quarterly.
- Whether Custom Skill review can be partner-delegated (links to
  `pericles-partner-marketplace`).

## Changelog

- 2026.05.0 — Initial draft from Doctrine §8 + Skills Security Spec; tied to the
  security-threat-model and registry resolution rules.
