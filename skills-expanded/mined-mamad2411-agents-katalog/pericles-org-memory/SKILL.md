---
name: pericles-org-memory
version: 2026.05.0
description: >
  How to build Organizational Memory — the customer's persistent context (documents,
  strategic customers/product lines, history) behind MCP, plus the §9 per-tenant
  cross-customer signal. Use this WHENEVER you ingest customer data, build retrieval
  (vector / knowledge graph), or design the privacy-preserving learning signal. Encodes
  ingestion + injection screening, vector+graph behind MCP, retrieval scoping, and the
  differential-privacy signal (OM Phase 1). Mostly net-new; OrganizationContext is the
  structured ERP slice that exists today.
doctrine_refs: [§5, §9; Security §2, §5; OM PRD]
depends_on: [pericles-mcp-layer, pericles-tenant-isolation, pericles-prompts, pericles-data-model]
last_reconciled: 2026-05-28
---

# Pericles Organizational Memory (build skill)

Organizational Memory (OM) is what makes impact analysis context-rich: the customer's
strategic customers, product lines, uploaded documents, and event history. The
Industry Pack absorbs sector defaults, but OM is where the **customer-specific** context
lives. Most of OM is **net-new**; the structured ERP slice already exists as
`OrganizationContext` (`pericles-data-model`, populated by `pericles-erp-adapter`).

## When to use this skill

Ingesting customer documents/context; building vector or knowledge-graph retrieval;
designing the cross-customer learning signal; wiring OM into impact analysis.

## Ingestion (with injection screening)

Customer-supplied content (documents, strategic customers, product lines) is **untrusted**
(`pericles-prompts`). At ingestion: screen for prompt-injection patterns (attempts to
redefine the assistant, reveal prompts, etc.), flag suspicious content in the Admin
Portal for tenant review (flags don't block ingestion), then index. Store per tenant;
`organization_id` on every record (`pericles-tenant-isolation`).

## Retrieval: vector + knowledge graph behind MCP

OM retrieval (semantic search + entity/relationship graph) sits **behind MCP**
(`pericles-mcp-layer`) so the backing stores are swappable and access is audited and
tenant-scoped. Skills query OM through the MCP server, never a hard-coded vector/graph
client (`pericles-tech-stack`). Every retrieval is logged
(`knowledge_sources_queried`).

## §9 — cross-customer signal (Phase 1, privacy-preserving)

The cross-customer learning signal is **architected now, not retrofitted** (§9, elevated
to OM Phase 1). Extract signal **per tenant** (every confirmed event, effective Plan,
Validation decision) with formal **differential-privacy budgets**; aggregate only
through the privacy budget; **no customer-identifying context ever leaves a tenant**.
Per-tenant budget exhaustion **halts** aggregation (never fail-open)
(`pericles-tenant-isolation`).

## What this forbids

Ingesting customer content without injection screening or `organization_id` scoping;
hard-coding a vector/graph store instead of going through MCP; any cross-tenant query
for aggregation outside the §9 DP pipeline; letting customer-identifying context leave a
tenant; treating retrieved OM content as trusted instructions.

## Verification

Ingested records are tenant-scoped and injection-screened; retrieval goes through MCP,
is logged, and never crosses tenants; the cross-customer signal is per-tenant with a DP
budget that halts on exhaustion; impact analysis can cite OM context for an event.

## Existing standards (read alongside)

Organizational Memory PRD + Doctrine §9 (Notion); `OrganizationContext` (the existing
structured slice); `pericles-mcp-layer`, `pericles-prompts`.

## Open questions

- Embedding model + vector store choice (behind MCP) — confirm (`pericles-tech-stack`
  notes `@mastra/libsql`/`@mastra/memory` as candidates).
- The DP budget mechanism (per-tenant epsilon) — define with the platform team (Ops §8).

## Changelog

- 2026.05.0 — Initial draft from the OM PRD + Doctrine §9; distinguished the existing
  OrganizationContext slice from the net-new OM layer.
