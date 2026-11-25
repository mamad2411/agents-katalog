---
name: pericles-cross-customer-learning
version: 2026.05.0
description: >
  How to activate cross-customer learning — the §9 Phase 2 step that turns per-tenant
  signal into aggregated platform intelligence WITHOUT letting any customer-identifying
  context leave a tenant. Use this WHENEVER you build the aggregation pipeline, the
  differential-privacy budget, or surfaces that consume aggregated insight. Encodes the
  Phase 1 (extract) / Phase 2 (aggregate) split, per-tenant DP budgets, halt-on-
  exhaustion, and the prohibition on identifying context ever leaving a tenant.
doctrine_refs: [§9; Security §2; Ops §8]
depends_on: [pericles-org-memory, pericles-tenant-isolation, pericles-mcp-layer]
last_reconciled: 2026-05-28
---

# Pericles Cross-Customer Learning (build skill)

§9 is architected from day one but **activates in two phases**: Phase 1 (per-tenant
signal extraction with DP guarantees) is MVP and lives in `pericles-org-memory`. Phase 2
— the actual aggregation that produces platform-wide intelligence — is **post-MVP** and
is what this skill governs. The privacy contract is non-negotiable: **no customer-
identifying context ever leaves a tenant, for any reason, including "anonymized" debugging**.

## When to use this skill

Building the aggregation pipeline, the per-tenant differential-privacy budget mechanism,
or any surface that consumes aggregated cross-customer insight (e.g. "platform-wide
trends," sector benchmarks).

## Phase 1 vs Phase 2

- **Phase 1 (MVP, in `pericles-org-memory`)** — per tenant, extract structured signal
  from every confirmed event, effective Plan, and Validation decision. Sit on the
  signal; do **not** aggregate yet.
- **Phase 2 (this skill, post-MVP)** — turn that per-tenant signal into platform
  intelligence by aggregating **only through a formal differential-privacy mechanism**
  with **per-tenant budgets**.

Shipping Phase 2 before the DP mechanism is built and audited is a doctrine violation.

## The per-tenant differential-privacy budget

Each tenant has a privacy budget (epsilon, ε). Every aggregation query against the
tenant's signal **debits** the budget by a calibrated amount; the platform must keep
queries below ε. **Exhaustion halts aggregation** for that tenant until the budget
refreshes per policy — **never fail-open**, never widen ε to "make a query work." The
budget mechanism is independent of any single Skill (`pericles-mcp-layer` enforces
access; this skill enforces accounting).

## Aggregation rules

- Aggregations are **statistical**, not record-level (counts, distributions, calibrated
  noise). Never produce an output that lets a tenant or event be reidentified.
- No output may contain a tenant identifier, an organization name, a supplier name, or
  any string that could be a re-identifier — even indirectly. Strip aggressively;
  prefer suppression to debate.
- Aggregated outputs are themselves recorded with their (ε, query, result) tuple so
  reviewers can replay the privacy accounting.

## Surfaces that consume aggregated insight

A platform-wide "trends" surface or sector-benchmark feature reads **only** the
post-aggregation outputs — never the per-tenant signal stores directly. Treat the
aggregation layer like an external MCP source from a Skill's perspective: typed,
audited, untrusted-by-default (`pericles-prompts`).

## What this forbids

Activating Phase 2 without the DP mechanism + audit; cross-tenant queries that bypass
the aggregation layer; widening ε to satisfy a query (failing-open); producing outputs
that could re-identify a tenant/event; per-tenant signal leaving the tenant in raw form;
debugging by reading another tenant's signal (`pericles-tenant-isolation`).

## Verification

DP budgets debit on every aggregation and halt on exhaustion; aggregated outputs are
suppression-tested for re-identifiers; (ε, query, result) tuples are recorded and
auditable; surfaces consume only post-aggregation outputs; tests fail a query that
would re-identify a tenant.

## Existing standards (read alongside)

Doctrine §9; Skills Security Spec §2; Ops Spec §8 (open question on DP mechanism);
`pericles-org-memory`, `pericles-tenant-isolation`.

## Open questions

- The concrete DP mechanism (Laplace/Gaussian noise per query class, per-tenant ε
  values, refresh policy) — define with the platform + privacy team before any Phase 2
  build.
- Whether aggregation is gated to Standard/Enterprise tenants (consent flow) or
  platform-wide — decide with GTM + privacy.

## Changelog

- 2026.05.0 — Initial draft governing §9 Phase 2 activation; per-tenant DP budgets,
  halt-on-exhaustion, statistical-only outputs, audited accounting.
