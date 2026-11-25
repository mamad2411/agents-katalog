---
name: pericles-atlas-mocker
version: 2026.06.0
description: >
  How to give Atlas live-looking motion — moving vessel dots and progressing
  sea-route lines — for the investment/interest MVP, WITHOUT a paid carrier or
  AIS feed. Use this WHENEVER you build or change shipment position simulation,
  the ShipmentPositionFeed seam, voyage/route geometry, or the Atlas live vessel
  layer. The data under the motion is REAL (BOL-seeded suppliers, carriers,
  vessels, lanes); only position-over-time is synthesized, behind one interface
  that swaps to real Terminal49 + AISstream data with a config flip.
doctrine_refs: [§5 (data access via the feed seam), §7; Atlas PRD; pericles-external-feeds]
depends_on: [pericles-atlas-ui, pericles-customer-onboarding, pericles-external-feeds, pericles-data-model]
last_reconciled: 2026-06-26
---

# Pericles Atlas Mocker (build skill)

The MVP exists to win investment and interest. A static map of historical BOL
rows doesn't sell; a map with **vessels moving along their lanes** does. This
skill builds that motion as a **mock implementation of the future real tracking
feed** — same interface, same output shape — so the demo is convincing now and
the swap to live data later is a config flip, not a rewrite.

**Simulate the motion, not the data.** Suppliers, carriers, vessel names, BOL
numbers, products, and lanes are real (seeded by `pericles-customer-onboarding`
from the BOL adapter). Only each shipment's position-over-time is synthesized.

## When to use this skill

Building or changing: the `ShipmentPositionFeed` seam, the mock feed, voyage/
sea-route geometry, the `/api/shipments/positions` endpoint, the Atlas live
vessel layer, or wiring the future `LivePositionFeed`.

## The seam (non-negotiable)

One interface, two implementations — Atlas and the API depend ONLY on the
interface:

```
ShipmentPositionFeed.getPositions(shipments, now?) → PositionUpdate[]
  • MockPositionFeed  — interpolate along a precomputed sea-route at simulated,
                        time-compressed progress.  (built)
  • LivePositionFeed  — Terminal49 (status/ETA) + AISstream (lat/lon),
                        normalized to the SAME PositionUpdate.  (TODO)
```

`PositionUpdate` carries `{ position, bearing, status, percent, covered_km,
remaining_km, eta, vesselName, polyline, source }`. The `covered_km /
remaining_km / percent` triple matches the route-progress shape required by
`pericles-atlas-ui`. Swapping mock→live (`TRACKING_MODE=live`) changes **no UI
and no schema**.

## How to do it

1. **Origin = real supplier coordinates** (`Supplier.latitude/longitude`,
   already seeded). **Destination = the BOL destination port**, resolved to
   coordinates. Unresolved either side → skip that shipment (graceful degrade,
   never throw — `pericles-external-feeds`).
2. **Line = a sea-route arc**, not a straight line. Route origin→destination
   through the correct canals/straits (Panama, Suez, Gibraltar, Malacca) with
   great-circle legs (`searoute.ts`). Straight lines that cross continents fail
   the realism bar.
3. **Clock = anchored, then staggered.** Anchor voyage timing on the row's real
   arrival date when present; otherwise synthesize a deterministic, staggered
   departure so the fleet spreads across phases (some departing, some mid-ocean,
   some arriving) instead of marching in lockstep.
4. **Sampling is pure + deterministic.** Position is a function of (plan, now).
   No cron, no DB writes — Atlas polls `/api/shipments/positions` and the dots
   move with the wall clock. `TRACKING_TIME_COMPRESSION` makes them visibly move
   during a pitch; `TRACKING_LOOP` wraps completed voyages so the map never goes
   static.
5. **Render layer** (`useShipmentPositions` hook → Atlas): the sea-route
   polyline + a vessel marker rotated by `bearing`. Every dot's InfoWindow shows
   the REAL supplier/carrier/BOL — only its position is simulated.

## What this forbids

- **No fabricated entities.** Never invent suppliers, carriers, vessels, BOL
  numbers, or lanes to fill the map. Mock motion over real rows only.
- **No implying the feed is live.** Label simulated motion in internal/demo and
  diligence copy. `PositionUpdate.source` and the API `meta.source` carry
  `'mock'` for exactly this. Getting caught implying live data is the only way
  this bites.
- **No second data path.** The mock writes nothing the live feed wouldn't; both
  emit `PositionUpdate`. Don't let the mock special-case Atlas.
- **No bypassing the seam.** Atlas/API import from `integrations/tracking`, never
  the mock class directly.

## Verification

- `npm run type-check` + the tracking unit tests (`searoute.test.ts`,
  `mock-feed.test.ts`): sea-route threads the right canal, distance is monotonic
  and exceeds the straight line, sampling is deterministic, progress advances and
  loops within [0,1], unroutable rows are skipped.
- Manual: seed a trial tenant (Helios slug set), open Atlas, confirm dots move
  along canal-routed arcs and InfoWindows show real BOL detail.

## The swap to real data

Add `live-feed.ts` implementing `ShipmentPositionFeed` from Terminal49 (status/
ETA webhooks; free tier = 10 active containers) + AISstream (free AIS WebSocket;
needs a Node proxy, can't go browser-direct), behind the doctrine's untrusted-
feed + timeout rules (`pericles-external-feeds`). Flip `TRACKING_MODE=live`. See
`references/live-feed-contract.md`. Live positions likely persist last-known
state — that's when the optional `Shipment` position columns get added (not
needed for the mock).

## Existing standards (read alongside)

`pericles-atlas-ui` (the map + route-progress shape), `pericles-customer-onboarding`
(seeds the real rows this animates), `pericles-external-feeds` (untrusted feeds,
graceful degrade), `pericles-yetiscraper-mcp-apify` (the BOL source).

## Open questions

- Whether the live feed persists last-known position on `Shipment` (adds
  `current_lat/lng`, `position_status`, `position_updated_at`) or stays
  compute-on-read like the mock. Deferred until `LivePositionFeed`.
- Whether to unify the two route sources in Atlas (the legacy
  `generateCurvedPath` bezier vs the feed's sea-route polyline) once the live
  layer is the default — currently both render; the feed polyline is canal-accurate.
- Sea-route fidelity: the gazetteer router covers the trial's dominant lanes;
  a full searoute/Pandana graph is post-MVP if coverage gaps appear.

## Changelog

- 2026.06.0 — Initial skill + implementation: `ShipmentPositionFeed` seam,
  `MockPositionFeed`, sea-route geometry, voyage planner, `/api/shipments/positions`,
  `useShipmentPositions` hook, Atlas live vessel layer.
