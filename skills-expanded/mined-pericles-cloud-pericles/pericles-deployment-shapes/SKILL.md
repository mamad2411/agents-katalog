---
name: pericles-deployment-shapes
version: 2026.05.0
description: >
  How Pericles ships as three deployment shapes — Express, Standard, Enterprise — on one
  engine (§7). Use this WHENEVER a feature differs by shape: tenancy, configuration,
  auth/SSO, governance, audit access, pack upgrades, or Custom Skills. Encodes what
  varies (topology, governance, admin surface) and what NEVER varies (the engine and the
  Skills), so you never fork the codebase per shape.
doctrine_refs: [§7; Industry Pack Spec §3; Ops §6]
depends_on: [pericles-doctrine, pericles-tenant-isolation, pericles-admin-portal-ui]
last_reconciled: 2026-05-28
---

# Pericles Deployment Shapes (build skill)

One engine serves a $400M manufacturer and a $5B pharma. The difference between them is
**topology, governance, and admin surface — never the engine or the Skills** (§7). If a
feature needs a per-shape code fork, you're doing it wrong; make it configuration.

## When to use this skill

Any feature that should behave differently for Express vs Standard vs Enterprise; pack
upgrade behavior; auth/SSO; audit scope; Custom Skill availability; residency/compliance.

## What varies vs what doesn't

**Varies (configuration & topology):** tenancy/isolation topology, auth/SSO options,
governance controls, admin-surface depth, audit retention/access, pack-upgrade policy,
Custom Skill availability, data residency, compliance modes.

**Never varies:** the Mastra runtime, the Skill Registry, the Skills themselves, the
data model, the doctrine. A Skill behaves identically across shapes; the shape decides
what's enabled and how it's governed.

## The three shapes

| Dimension | Express | Standard | Enterprise |
|---|---|---|---|
| Buyer | mid-market, self-serve | mid-market+ | large/regulated |
| Pack upgrades | **auto** on the 7-day soak after promotion | explicit admin action | explicit admin action |
| Audit access | 30-day, filter-only | 90-day filterable + lineage + export | + authenticated API, extended retention |
| Auth / SSO | Google OAuth | Google OAuth + SSO | enterprise SSO (SAML/OIDC), SCIM |
| Custom Skills | no | yes (reviewed) | yes (reviewed) |
| Compliance | baseline | baseline+ | HIPAA BAA, validated-systems mode, residency (e.g. pharma) |

(Pack-upgrade behavior is from Industry Pack Spec §3; audit access from Ops §6 /
`pericles-observability`.)

## How to implement a shape difference

1. Default the behavior in config keyed by shape (and tenant `OrganizationSettings`),
   not in branched code.
2. Gate availability (e.g. Custom Skills, audit API) by shape + RBAC tier
   (`pericles-admin-portal-ui`).
3. Keep the Skill/runtime path identical; only the surrounding governance/config changes.
4. Local dev uses the same `docker-compose` (Postgres, pgAdmin, Mastra) regardless of
   shape.

## What this forbids

Forking the codebase or a Skill per shape (§7, §10); a Skill that behaves differently by
shape beyond what config/governance dictates; auto-upgrading packs outside Express;
exposing Enterprise-only controls (audit API, SSO) to lower shapes.

## Verification

Shape differences are config/governance, not code forks; the same Skills/registry/engine
run in every shape; pack-upgrade, audit, auth, and Custom-Skill availability match the
table; one `docker-compose` dev path.

## Existing standards (read alongside)

Doctrine §7; Industry Pack Spec §3; Ops §6; `docker-compose.yml`;
`.claude/rules/13-infrastructure.md`.

## Open questions

- Concrete tenancy topology per shape (shared DB + row scoping vs isolated DB for
  Enterprise) — define with the platform team.
- Validated-systems mode + HIPAA BAA mechanics for the pharma Enterprise motion — define
  with `pericles-compliance-audit` before Wave 3.

## Changelog

- 2026.05.0 — Initial draft from Doctrine §7; shape matrix reconciled with Industry Pack
  §3 (pack upgrades) and Ops §6 (audit access).
