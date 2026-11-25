---
name: ride-hailing-maps-master
description: >-
  Master hub for building Uber/Careem-style ride-hailing & on-demand mobility super-apps AND for
  professional maps design + integration. Use for rider/driver apps, real-time driver-rider matching
  & dispatch, live GPS tracking, ETA/routing/turn-by-turn navigation, geocoding/places/addressing,
  surge & dynamic pricing, trip lifecycle + fares/payouts, super-app (rides+delivery+pay) architecture,
  and map rendering (Mapbox GL/MapLibre/Google Maps) with custom styling, markers, polylines, camera,
  clustering & performance. Bundles 8 specialized skills (in skills/<name>/GUIDE.md).
---

# Ride-Hailing & Maps — Master Hub (Uber/Careem-grade)

Build production **on-demand mobility** platforms and **master maps** end-to-end: matching, dispatch,
live tracking, routing/ETA, geocoding, surge pricing, trip+payments, and beautiful, fast maps.

## How to use this hub

1. Start with **ride-hailing-architecture** (services, trip state machine, geo backbone).
2. Add matching/dispatch, live-tracking, routing, pricing as the feature needs.
3. For the map UI itself use **maps-rendering-design**; for addresses **geocoding-places-addressing**.
4. Build the apps with **`cross-platform-apps-master`**; money with **`payments-master`**.

## Bundled skills

- **ride-hailing-architecture** ⭐ — Rider/driver/dispatch services, the trip state machine, real-time
  backbone (WS/MQTT), geo-indexing (H3/S2), data model, idempotency, multi-city/tenant.  
  → `skills/ride-hailing-architecture/GUIDE.md`
- **realtime-matching-dispatch** ⭐ — Driver↔rider matching, supply/demand balancing, H3 spatial search,
  batched ETA-weighted assignment, offer/accept flow, reassignment, anti-starvation.  
  → `skills/realtime-matching-dispatch/GUIDE.md`
- **live-location-tracking** ⭐ — GPS ingestion pipeline, location smoothing/snap-to-road, driver
  presence + fan-out to riders, WebSocket/MQTT scale, battery & accuracy trade-offs.  
  → `skills/live-location-tracking/GUIDE.md`
- **maps-rendering-design** ⭐ — Map UI mastery: Mapbox GL JS v3 / MapLibre / Google Maps, custom styles,
  markers/polylines, camera animation, clustering, 3D, dark mode, RTL/Arabic labels, performance.  
  → `skills/maps-rendering-design/GUIDE.md`
- **routing-navigation-eta** ⭐ — Directions/Routes APIs (Google Routes, Mapbox Directions, OSRM/Valhalla),
  turn-by-turn navigation, traffic-aware ETA, route matrix, optimization, snap-to-roads.  
  → `skills/routing-navigation-eta/GUIDE.md`
- **geocoding-places-addressing** — Geocoding/reverse, autocomplete/Places, MENA addressing (landmarks,
  pin-drop, what3words-style), saved places, accuracy & cost control.  
  → `skills/geocoding-places-addressing/GUIDE.md`
- **surge-dynamic-pricing** — Fare model, zone/time surge, dynamic pricing signals, upfront vs metered,
  fairness/caps, fare estimate vs final reconciliation.  
  → `skills/surge-dynamic-pricing/GUIDE.md`
- **superapp-careem-model** — Super-app architecture: rides + delivery + payments/wallet under one
  identity, module/service boundaries, shared location/maps, mini-apps.  
  → `skills/superapp-careem-model/GUIDE.md`

## Pairs well with

`cross-platform-apps-master` (rider/driver apps), `payments-master` (fares/payouts/wallet),
`marketplace-master` (delivery dispatch), `backend-api-master` (GPS/GIS/PostGIS), `systems-platforms-master`
(data/realtime infra), `communications-master` (driver/rider chat & notifications).

## Note

Bundled skills use `GUIDE.md` so only this master appears in Cursor's skills list.
