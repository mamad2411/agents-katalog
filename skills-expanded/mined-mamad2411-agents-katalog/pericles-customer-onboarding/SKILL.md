---
name: pericles-customer-onboarding
version: 2026.06.0
description: >
  How to onboard a CUSTOMER into Pericles end-to-end from public bill-of-lading
  data: create the parent company and all its branded subsidiaries as
  Organizations with their business info, pull each subsidiary's shipments,
  carriers, and suppliers from ImportYeti via Apify, and seed BOTH the relational
  Supplier/Carrier/Shipment tables (the path Atlas + the position mocker read) and
  the OrganizationContext rollup (the path monitoring reads). Use this WHENEVER you
  onboard a trial/customer, wire the ImportYeti→Apify scrape, build the BOL→table
  seeder, or change how a tenant's org hierarchy and supply-chain data get created.
doctrine_refs: [§5 (external data via the adapter seam), §7; Atlas PRD; pericles-erp-adapter]
depends_on: [pericles-yetiscraper-mcp-apify, pericles-data-model, pericles-tenant-isolation, pericles-atlas-ui, pericles-atlas-mocker]
last_reconciled: 2026-06-26
---

# Pericles Customer Onboarding (build skill)

Onboarding turns a real company into a populated Pericles tenant. For the Atlas
MVP the source is **public US customs bill-of-lading data** (ImportYeti via Apify),
so a customer renders on the map and in monitoring WITHOUT a live ERP. The output
is a complete tenant: the parent company, its branded subsidiaries, and each
subsidiary's suppliers, carriers, and shipments.

Everything here is REAL data — real importers, real foreign suppliers, real
carriers and lanes. (Position-over-time is the only thing simulated downstream;
that's `pericles-atlas-mocker`, which rides on the tables this skill seeds.)

## When to use this skill

Onboarding a trial or customer; wiring or changing the ImportYeti→Apify scrape;
building/altering the BOL→`Supplier`/`Carrier`/`Shipment` seeder; or changing how
a tenant's organization hierarchy is created.

## The pipeline (end to end)

1. **Parent customer org** — find-or-create the top-level `Organization` (e.g.
   Helios Technologies) with `customer_type='customer'` and business info.
2. **Scrape** — pull BOL rows per branded subsidiary slug from ImportYeti via
   Apify (`integrations/bol/client.ts`), or load a fixture offline.
3. **Subsidiaries** — split rows by importer (consignee) and create one child
   `Organization` per brand under the parent (`pericles-data-model` Rule 5).
4. **Relational tables** — per subsidiary, seed `Supplier` (geocoded origin),
   `Carrier` (by SCAC), and `Shipment` rows. **This is the path Atlas + the
   mocker read.**
5. **Context rollup** — per subsidiary, upsert `OrganizationContext`
   (plants/suppliers/lanes JSON). **This is the path monitoring reads.**

Entry point: `onboardCustomerFromBol()` in `integrations/bol/onboard.ts` runs all
five. CLI: `npm run bol:seed`.

## Two data paths — reconciled (was an open question)

Atlas and `pericles-atlas-mocker` read the **relational** `Supplier`/`Shipment`
tables directly (`Supplier.latitude/longitude` = route origin,
`Shipment.destination_port` = US discharge port). The monitoring pipeline reads
the **`OrganizationContext`** JSON rollup. These are different shapes for
different consumers. **Onboarding writes both, from the same rows** — the
relational seeder (`seed-tables.ts`) and the context transformer
(`transformer.ts`) never diverge because they consume one row set. Do NOT make
Atlas read `OrganizationContext`, and do NOT drop the relational seed — each
consumer keeps its path.

## Org & subsidiary model

A customer is usually a holding company whose operating units are separately
**branded importers** (Helios → Sun Hydraulics, Faster, …). Each brand is its own
tenant: a child `Organization` (`customer_type='subsidiary'`,
`parent_organization_id` = the customer). The parent is a rollup node — never
written with a child's suppliers/shipments. Rows are split by `consignee_slug`
(stable) falling back to `consignee_name`.

## Pulling from ImportYeti (Apify scrape)

Mechanics and cost live in `pericles-yetiscraper-mcp-apify`; the essentials:

- **Actor**: a row-level ImportYeti BOL actor (default
  `jungle_synthesizer~importyeti-bill-of-lading-scraper`; override with
  `APIFY_BOL_ACTOR`). Row-level, NOT aggregate-only — Pericles needs one record
  per shipment.
- **Input**: `{ companies: string[], suppliers: string[], maxItems }` where
  `companies` are importer **slugs** from `importyeti.com/company/<slug>` and
  `suppliers` are foreign-supplier slugs. The actor's default cap is 50 — set
  `maxItems` higher for a real pull.
- **Auth/cost**: `APIFY_TOKEN`; pay-per-event makes a trial pull cost cents.
- **Normalization**: `client.ts` maps `target_*` (US importer) and
  `counterparty_*` (foreign supplier), skips the per-company `summary` row, and
  defensively captures vessel name / value when the actor provides them.
- **Geocoding**: Google Geocoding cached in KeyValueStore, namespaced per org;
  keyless installs degrade to the offline gazetteer. Unplaceable rows are
  skipped, never thrown (`pericles-external-feeds`).
- **At scale**: scraping is a TRIAL path. For production, prefer a licensed
  customs feed (CBP AMS) with redistribution rights over scraping.

See `references/scrape-inputs.md` for slug discovery and the verified trial sets.

## Trial slug sets (verified)

- **Helios Technologies** (the chosen first trial — balanced China/Italy lanes,
  clean standalone-brand slugs): `sun-hydraulics`, `faster`, `enovation-controls`,
  `balboa-water-group`, `daman-products`.
- **Allient Inc.** (deferred): do **NOT** scrape the slug `allient` — the parent
  renamed from Allied Motion Technologies (Aug 2023) and that slug is unreliable.
  Use the brand slugs: `allied-motion-technologies`, `globe-motors`,
  `motor-products`, `tci`, `spectrum-controls`, `allied-motion-changzhou`.
- **Sea-freight only**: BOL/AMS covers ocean shipments. Air and truck lanes won't
  appear — set expectations in trial copy.

## How to run it

```bash
# Onboard Helios end-to-end (parent + subsidiaries + tables + context):
npm run bol:seed -- --customer-name="Helios Technologies" --seed-tables -v \
  --company=sun-hydraulics,faster,enovation-controls,balboa-water-group,daman-products

# Onboard under an existing parent org id:
npm run bol:seed -- --org-id=<parent-uuid> --seed-tables --company=sun-hydraulics -v

# Offline dry run from a fixture (no network, gazetteer geocoder, no writes):
npm run bol:seed -- --customer-name="Helios Technologies" --fixture=./fixtures/bol.json --stub --dry-run
```

Library: `onboardCustomerFromBol({ customerName | parentOrganizationId,
businessInfo?, companies, suppliers?, maxItems?, rows?, geocoder?, dryRun? })`.

## Idempotency & tenant isolation (non-negotiable)

- **Idempotent**: parent matched by `(name, parent=null)`; child by `(parent,
  name)`; Supplier/Shipment by deterministic id `BOL-{SUP,SHP}-<org8>-<slug>`;
  Carrier by unique SCAC. Re-running an onboard UPDATES in place — never
  duplicates.
- **Tenant-scoped**: every `Supplier`/`Shipment` write carries `organization_id`
  (the subsidiary's). The parent is verified to exist before any child write. The
  geocode cache is namespaced per org. See `pericles-tenant-isolation`.

## What this forbids

- **No fabricated entities** — never invent importers, suppliers, carriers, or
  shipments to fill a tenant. Onboard only what the customs data shows.
- **No parent pollution** — never write a child's suppliers/shipments onto the
  parent rollup org.
- **No cross-tenant bleed** — a subsidiary's rows belong to that subsidiary's org
  only; never reuse another tenant's geocode cache or rows.
- **No wrong-slug scrapes** — e.g. the `allient` slug; use the brand slugs.
- **No silent feed failure** — a single unplaceable/garbage row is skipped, not
  fatal; a whole failed pull surfaces an error.

## Verification

- `npm run type-check` + the BOL adapter tests (`seed-tables.test.ts`,
  `sync-service*.test.ts`): seeder writes org-scoped Supplier/Carrier/Shipment,
  links shipments to supplier+carrier, is idempotent, and skips unplaceable rows.
- Offline: run the CLI with `--fixture --stub --dry-run` and confirm one child
  per brand and the table counts.
- Live: onboard Helios, open Atlas, confirm suppliers/ports render and (with
  `pericles-atlas-mocker`) vessels move along their lanes; spot-check an
  InfoWindow against the importer's ImportYeti page.

## Existing standards (read alongside)

`pericles-yetiscraper-mcp-apify` (scrape mechanics + cost), `pericles-data-model`
(org hierarchy, Supplier/Carrier/Shipment), `pericles-erp-adapter` (the adapter
template the BOL adapter follows), `pericles-atlas-ui` + `pericles-atlas-mocker`
(the consumers of the seeded tables), `pericles-tenant-isolation`.

## Open questions

- `value_usd` and full container manifests are usually absent from BOL rows —
  Shipment value/containers stay sparse until an ERP/forwarder feed
  (`pericles-erp-adapter`) enriches them.
- Vessel name/IMO appear on some actors but not all; the seeder captures them when
  present, else null. Decide a canonical enrichment source for live tracking
  (`pericles-atlas-mocker` live-feed contract).
- Production data source: move trials off scraping to a licensed CBP AMS feed with
  redistribution rights before customer GA.

## Changelog

- 2026.06.0 — Initial skill + the relational seeder (`seed-tables.ts`), the
  customer orchestrator (`onboard.ts`, find-or-create parent), `seedRelationalTables`
  wired through subsidiary sync, vessel/value fields captured from ImportYeti, and
  the `bol:seed` CLI extended with `--customer-name` / `--seed-tables`.
