---
name: pericles-partner-marketplace
version: 2026.05.0
description: >
  How partners (consultancies, ERP integrators, regional resellers) author, list, and
  sell Skills on Pericles — extending Custom Skill mechanics across tenants. Use this
  WHENEVER you build the marketplace, partner publishing, partner-scoped review, or
  partner activation surfaces. Encodes that partner Skills are still Custom Skills with
  tenant binding, the four-stage review applies per tenant, partner-published Skills
  are not platform Skills (no override of platform IDs), and commercial mechanics are
  out of scope (GTM-owned).
doctrine_refs: [§7, §8; Industry Pack Spec §5, §9]
depends_on: [pericles-custom-skill, pericles-skill-registry, pericles-tenant-isolation, pericles-admin-portal-ui]
last_reconciled: 2026-05-28
---

# Pericles Partner Marketplace (build skill)

Partners extend Pericles' reach: a consultancy bundles industry expertise as Skills; an
ERP integrator publishes adapters; a regional reseller localizes a pack. The
**engineering** substrate is the **Custom Skill** mechanism (`pericles-custom-skill`)
extended with publishing + activation flows. **Commercial mechanics** (revenue share,
SKUs, channel programs) are explicitly GTM-owned and out of scope (Industry Pack Spec
§9).

## When to use this skill

Building the marketplace surface, partner publishing, partner-scoped review, or
partner-activation flows; reviewing a partner-listed Skill.

## A partner Skill is still a Custom Skill

A partner-authored Skill enters a tenant's Stack as a **Custom Skill** in that tenant's
namespace (`custom/<tenant-slug>/<name>@<version>`). It must:

- Pass all sandbox constraints — MCP-only egress, no DB, allow-listed libs, no direct
  Execution Node, tenant-namespace-bound (`pericles-custom-skill`,
  `pericles-security-threat-model`).
- **Extend, never override** a platform Skill ID (§8). Partner-published does not mean
  platform-published.
- Pass the **four-stage review per activating tenant**: static, security, eval,
  customer sign-off. A partner cannot pre-grant activation across tenants.

The marketplace surfaces a **partner-curated catalog**; activation is still a per-
tenant decision audited by the tenant's Admin.

## Publishing flow

1. Partner authors a Skill in their **partner namespace** (a partner sandbox tenant).
2. Partner submits to the marketplace; platform runs static + security review.
3. On platform acceptance, the Skill is **listed**, not yet activated for any customer.
4. A customer Admin activates the listed Skill for their tenant; the four-stage review
   runs in that tenant's context (the partner can supply reference evals to speed it).

The partner namespace itself never resolves at runtime for end customers
(`pericles-skill-registry`); listing is a marketplace-layer concept, not a registry
shortcut.

## Trust & attribution

Each listing shows the partner identity, the Skill's `provenance` (architecture/security
review links), and `eval_criteria` results from the partner's reference set. Customers
see who they're trusting.

## What's NOT in scope

Pricing, revenue share, SKU model, co-sell motion, partner enablement programs — all
GTM-owned (Industry Pack Spec §9). This skill governs the engineering surface only.

## What this forbids

A partner Skill that bypasses the four-stage per-tenant review; partner-published Skills
that try to resolve as platform Skills or override platform IDs; cross-tenant activation
by partner action (only the tenant Admin activates for their tenant); leakage of one
customer's data to a partner via a partner Skill (sandbox + MCP scoping prevents this);
non-allowlisted egress.

## Verification

Listed Skills are partner-namespaced and unreachable as platform Skills; per-tenant
activation runs the four-stage review and writes an audit entry
(`pericles-admin-portal-ui`); partners cannot activate for tenants; partner identity +
provenance + eval results are visible at the listing.

## Existing standards (read alongside)

`pericles-custom-skill`, `pericles-skill-registry`, `pericles-tenant-isolation`,
`pericles-admin-portal-ui`; Industry Pack Spec §5/§9 (GTM scope boundary).

## Open questions

- Partner identity verification (basic KYC vs deeper enterprise vetting) — define with
  Legal + GTM.
- Whether platform-funded reviewers can act on a partner's behalf to speed activation
  (`pericles-custom-skill` open question).

## Changelog

- 2026.05.0 — Initial draft; partner Skills are Custom Skills with publishing +
  per-tenant activation; commercial mechanics deliberately out of scope.
