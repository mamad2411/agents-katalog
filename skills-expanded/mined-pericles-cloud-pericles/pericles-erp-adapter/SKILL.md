---
name: pericles-erp-adapter
version: 2026.05.1
description: >
  How to build an ERP adapter that turns a customer's ERP into Pericles
  OrganizationContext. Use this WHENEVER you add or change an ERP integration (SAP
  S/4HANA exists; Dynamics 365, Epicor Kinetic, Infor CloudSuite are Wave 1). Encodes
  the adapter anatomy (client, types, transformer, sync-service, mock), the mapping to
  OrganizationContext, real-time ERP tools, mock mode, and that new adapters belong
  behind MCP (§5) while the SAP one is grandfathered.
doctrine_refs: [§5; Industry Pack Spec §1, §6]
depends_on: [pericles-mcp-layer, pericles-data-model, pericles-tenant-isolation]
last_reconciled: 2026-05-28
---

# Pericles ERP Adapter (build skill)

An ERP adapter connects a customer's ERP, pulls supply-chain master data, and
transforms it into Pericles `OrganizationContext` (plants, warehouses, suppliers,
shipping lanes, risk preferences) — the substrate the monitoring pipeline and impact
analysis depend on. **The SAP S/4HANA adapter is already scaffolded**
(`backend/src/integrations/sap/`); use it as the template. Dynamics 365, Epicor Kinetic,
and Infor CloudSuite are Wave-1 net-new (Industry Pack Spec §6).

## When to use this skill

Adding/changing an ERP adapter; mapping ERP data to `OrganizationContext`; wiring a new
ERP into onboarding (auto-derive footprint).

## Adapter anatomy (from the SAP adapter)

```
integrations/<erp>/
  types.ts          # ERP API types (SAP: OData entities — BusinessPartner, Plant, ShippingLane)
  client.ts         # connection + auth (SAP: OAuth 2.0 + OData) + fetch
  transformer.ts    # ERP shape → OrganizationContextData (the canonical target)
  sync-service.ts   # scheduled/triggered sync of ERP data
  mock-api.ts       # mock data for dev (SAP ships Levi Strauss test data)
  index.ts          # exports (SAP: transformSAPDataToOrganizationContext)
```

The canonical transform target (matching Prisma `OrganizationContext`):
`{ plants, warehouses, suppliers, shipping_lanes, risk_preferences }`. Every adapter's
`transformer` must produce exactly this shape, regardless of the source ERP — that's
what keeps the rest of the platform ERP-agnostic.

## Real-time tools vs sync

Two access modes coexist:
- **Sync** (`sync-service.ts`) populates `OrganizationContext` on a schedule / on
  connect (onboarding auto-derives the geographic footprint).
- **Real-time** Mastra tools for point queries (SAP: `sapGetMaterialStockTool`,
  `sapGetShippingLanesTool`) used during analysis. These follow `pericles-mastra-tool`
  (org_id input, timeout).

## Branded subsidiaries: one context per child org

A customer is often a **parent holding company whose operating units are
separately-branded companies**, each with its own supply chain
(`pericles-data-model`, `pericles-tenant-isolation`). Model each subsidiary as a
**child `Organization`** (`parent_organization_id`) and seed **one
`OrganizationContext` per child org** — never flatten several brands' suppliers /
plants / lanes into the parent's single context (that erases the brand boundary and
the per-tenant scope). The parent is a rollup node; access flows ancestor →
descendant. The BOL adapter is the reference:
`syncBolContextForSubsidiaries(parentOrgId)` splits rows per importer and
find-or-creates one child org + context per brand, idempotent on
`[parent_organization_id, name]` (`backend/src/integrations/bol/sync-service.ts`).

## MCP & grandfathering (§5)

New ERP adapters should expose their data **behind MCP** (`pericles-mcp-layer`) so the
ERP is swappable and access is audited/tenant-scoped. The existing SAP adapter is
**grandfathered inline** — keep it working; don't rewrite it as part of adding a new
adapter. The Industry Pack references adapters by version
(`adapters/sap-s4hana@…`, `…dynamics-365@…`, `…epicor-kinetic@…`,
`…infor-cloudsuite@…` — `pericles-industry-pack`).

## Mock mode

Every adapter ships a mock (`mock-api.ts`) so development needs no live ERP
(`npm run mock:create` / `mock:reset`; SAP: `npx tsx src/scripts/sync-sap-erp.ts --test`).
Don't require production ERP credentials for local dev.

## What this forbids

A transformer that emits anything other than the canonical `OrganizationContext` shape;
storing ERP data without `organization_id` scoping; flattening multiple branded
subsidiaries into one parent `OrganizationContext` instead of one child org per brand;
a new adapter that bypasses MCP without grandfather justification; requiring live ERP
creds for dev (ship a mock); holding ERP secrets anywhere but the configured secret store.

## Verification

`transformer` output matches `OrganizationContext`; sync populates plants/warehouses/
suppliers/lanes per org; real-time tools validate `organization_id` + use timeouts;
mock mode works without live creds; the adapter is referenceable by version in a pack.

## Existing standards (read alongside)

`backend/src/integrations/sap/*` + `backend/docs/SAP_S4HANA_INTEGRATION.md`,
`SAP_USAGE_GUIDE.md`, `ORGANIZATION_CONTEXT.md`; Industry Pack Spec §6.

## Open questions

- Whether the SAP adapter is rewritten behind MCP in Wave 1 or stays grandfathered while
  Dynamics/Epicor/Infor are built MCP-first — decide with the platform team.
- Auth/secret handling per ERP (OAuth vs API key) — standardize in the secret store.

## Changelog

- 2026.05.1 — Added the branded-subsidiary rule: seed one `OrganizationContext` per child
  org, never flatten brands into the parent (BOL `syncBolContextForSubsidiaries` is the
  reference). Grounded in `pericles-data-model` / `pericles-tenant-isolation`.
- 2026.05.0 — Initial draft using the existing SAP adapter as the template; canonical
  OrganizationContext transform target; MCP-for-new / grandfather-SAP.
