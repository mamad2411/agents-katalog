---
name: pericles-atlas-ui
version: 2026.05.0
description: >
  How to build Atlas — the Google-Maps-style operational picture of suppliers,
  shipments, routes, and events. Use this WHENEVER you build or change the map, its
  layers, clustering, the filter bar, the events feed, or Atlas defaults. Encodes the
  Google Maps parity bar (map+satellite, smooth zoom/pan), the supplier/shipment/route/
  event layers with route progress, the full filter set, and Industry-Pack-driven
  defaults.
doctrine_refs: [§6, §7; Atlas PRD; Industry Pack Spec §1]
depends_on: [pericles-frontend-foundations, pericles-persona-layer, pericles-monitoring-pipeline]
last_reconciled: 2026-05-28
---

# Pericles Atlas UI (build skill)

Atlas is the map-first operational picture: where the customer's suppliers and shipments
are, how routes are progressing, and what risk events threaten them. It uses
`@react-google-maps/api`. **Atlas is net-new** (the Industry Pack Spec marks Atlas
defaults as a forward commitment); build it to the persona rule's non-negotiables.

## When to use this skill

Building/changing the map, layers, clustering, filters, the events feed, or Atlas
default presets.

## Map parity (non-negotiable, from the personas rule)

Mirror Google Maps: **map and satellite** views, smooth **zoom and pan at ≥60 FPS**.
A limited/stuttery map fails the bar.

## Layers (what must render)

- **Suppliers** — primary, secondary, tertiary (tiered styling).
- **Shipments** — origin → destination with **full routes**, including **distance
  covered and remaining** (e.g. `{ covered_km, remaining_km, percent }`).
- **Events** — risk events from the monitoring pipeline (`pericles-monitoring-pipeline`),
  placed and severity-styled (0.0–1.0).
- **Clustering** at low zoom so dense regions stay legible.

## Filter bar (full set required)

`transit` (air, maritime, rail, ground), `origin`, `destination`, `supplier`,
`goods type`, `supplier tier` (primary/secondary/tertiary), `timeliness` (on-time,
delayed, blocked). A partial filter set fails the requirement.

## Events feed

A live, tenant-scoped feed alongside the map (socket.io), filterable to the org's
footprint, clicking through to the event/incident detail (`pericles-intelligence-ui`).

## Industry-Pack defaults

Atlas ships sector defaults via the active Pack (`atlas_defaults`: `filter_preset`,
`severity_rules`, layer config — e.g. `industrial-mfg-default`). The customer doesn't
configure these; the Pack pre-sets them (`pericles-industry-pack`). On day one (after a
~30-min ERP connect) the map is pre-loaded with the customer's suppliers/shipments and
the feed filtered to their footprint.

## Persona & tenant

Persona shapes Atlas (default module, visible detail) via the Persona Layer
(`pericles-persona-layer`); data is tenant-scoped server-side
(`pericles-tenant-isolation`). Footprint is derived from ERP (`pericles-erp-adapter`).

## What this forbids

A map without satellite or with sub-60-FPS pan/zoom; missing route covered/remaining
metrics; a partial filter set; client-trusted `organization_id`; per-persona forked
Atlas variants; hard-coded sector defaults instead of Pack-driven presets.

## Verification

Map+satellite with smooth zoom/pan; suppliers (3 tiers), shipments with route progress,
and events all render; clustering works; the full filter set is present; the feed is
tenant-scoped and live; Pack presets drive defaults.

## Existing standards (read alongside)

`.cursor/rules/001-application/004-pericles-atlas-core-standards-auto.mdc`,
`008-pericles-user-personas-*`; Atlas PRD (Notion); `@react-google-maps/api`.

## Open questions

- Performance approach for very large supplier/shipment counts (clustering thresholds,
  viewport querying) — define with the platform team.
- Whether route geometry comes from the ERP, a routing service behind MCP, or is
  approximated — confirm.

## Changelog

- 2026.05.0 — Initial draft from the Atlas PRD + personas rule; grounded in
  @react-google-maps/api and the Industry Pack atlas_defaults.
