---
name: pericles-mcp-layer
version: 2026.05.0
description: >
  How to access data through MCP — the target data-access layer for Pericles (§5). Use
  this WHENEVER you add a NEW data source (ERP, vector store, knowledge graph, external
  feed) or design how a Skill reaches data. Encodes the "new sources via MCP, existing
  inline grandfathered" rule, portability (swap stores behind MCP), audit symmetry
  (MCP access logged like any invocation), and tenant scoping enforced at the MCP
  boundary. .mcp.json holds exactly one server today (apify-importyeti) — this layer is
  still close to greenfield.
doctrine_refs: [§5; Security §2; Manifest Spec]
depends_on: [pericles-doctrine, pericles-tenant-isolation, pericles-skill-authoring]
last_reconciled: 2026-05-28
---

# Pericles MCP Layer (build skill)

MCP (Model Context Protocol) is the **target data-access layer** (§5): Skills reach
external data through MCP servers rather than per-Skill integration code. This makes
data sources portable (swap the store without touching Skills), keeps access auditable
in one place, and lets the platform enforce tenant scoping at the data boundary. **The
repo's `.mcp.json` holds exactly one server — `apify-importyeti`, the ImportYeti/Apify
BOL source (`pericles-yetiscraper-mcp-apify`). Everything else is still greenfield.**

## When to use this skill

Adding any NEW data source; choosing where a vector store / knowledge graph / ERP /
feed lives; designing a Skill's `knowledge_sources`; reviewing whether an integration
should be inline or behind MCP.

## The rule (§5)

- **New data sources go through MCP**, registered in `.mcp.json` / the registry, not
  inlined in a tool's `execute()`.
- **Existing inlined integrations are grandfathered** — the 10 monitoring tools'
  NOAA/GDELT/NVD/etc. calls and the SAP adapter keep working until rewritten; do not
  refactor them opportunistically (`pericles-external-feeds`, `pericles-erp-adapter`).
- A Skill's manifest declares its `knowledge_sources`; MCP-backed sources reference the
  server, inline ones are marked `grandfathered_inline` (`pericles-skill-authoring`).

## Why MCP (the three properties to preserve)

1. **Portability** — vector DB, knowledge graph, and ERP are swappable behind a stable
   MCP interface. No Skill hard-codes Pinecone/Neo4j/a specific ERP (`pericles-tech-stack`).
2. **Audit symmetry** — data access through MCP is logged like any invocation
   (`knowledge_sources_queried`, `pericles-observability`); there's one place to answer
   "what did this Skill read."
3. **Tenant scoping at the boundary** — the MCP layer enforces `organization_id`
   scoping so a shared platform Skill cannot leak across tenants
   (`pericles-tenant-isolation` guarantee 5).

## Security constraints

- Custom Skills may egress **only** to registered MCP servers — never arbitrary network
  destinations (`pericles-tenant-isolation`, `pericles-security-threat-model`).
- MCP responses are **untrusted data**: boundary-mark them and validate against schemas
  before use (`pericles-prompts`). A poisoned MCP response must not become instructions.
- Egress to a non-allowlisted destination is a P0.

## What this forbids

Inlining a NEW data source instead of registering an MCP server; a Skill hard-coding a
specific store/provider; treating MCP responses as trusted; Custom-Skill egress outside
registered MCP servers; bypassing tenant scoping at the MCP boundary.

## Verification

New sources are MCP-registered and appear in `.mcp.json`/registry; manifests declare
MCP-backed `knowledge_sources`; MCP access is logged and tenant-scoped; swapping a
backing store requires no Skill change; non-allowlisted egress is blocked and alarmed.

## Existing standards (read alongside)

Doctrine §5 + Skills Security Spec (Notion); `.mcp.json`; `.claude/rules/13-infrastructure.md`.

## Open questions

- Which sources migrate first (Org Memory vector/graph stores are the strongest
  candidates since they're net-new — `pericles-org-memory`).
- Whether the registry or `.mcp.json` is the source of truth for registered servers —
  decide with the platform team.

## Changelog

- 2026.05.0 — Initial draft from Doctrine §5; grounded in the empty `.mcp.json`
  (greenfield) and the grandfathered inline integrations.
