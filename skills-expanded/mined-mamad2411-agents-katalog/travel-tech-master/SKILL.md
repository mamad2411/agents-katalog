---
name: travel-tech-master
description: >-
  Master hub for Travel & Tourism technology at staff/principal depth. Use to build OTAs, booking
  engines, tour operator/DMC/TMC systems, bed banks, and hotel tech — supplier/GDS/NDC/bed-bank API
  integration, the reliable booking saga (idempotency/compensation/PNR-voucher lifecycle), channel
  managers, supplier extranets, hotel/room mapping & deduplication, and B2B/B2C booking platforms.
  Grounded in real 2026 systems (Amadeus/Sabre, NDC 21.3, Hotelbeds/TBO/EAN, Booking.com connectivity,
  GIATA). Bundles 7 specialized skills (in skills/<name>/GUIDE.md). Use this for any travel-tech,
  tourism, OTA, GDS, channel manager, extranet, mapping, booking-saga, or B2B/B2C travel platform task.
---

# Travel & Tourism Technology — Master Hub

Build travel/tourism systems end-to-end: supplier integration (GDS, NDC, bed banks), the reliable booking
saga, channel managers, supplier extranets, hotel/room mapping, and B2B/B2C booking platforms.

## How to use this hub

This single skill bundles **all 7 travel-tech skills**. Each bundled skill's full instructions live in
`skills/<name>/GUIDE.md`.

**Workflow:**
1. **Always start with `travel-tech-architecture`** — the canonical model (Money/Offer/RatePlan/
   CancellationPolicy/Booking), the search→recheck→book→pay→confirm flow, glossary, and the 2026 standards map.
2. Match the request to one or more skills below and read its `GUIDE.md` before acting.
3. Combine skills — real builds span several (supplier integration + mapping + booking saga + B2B/B2C).

## The non-negotiables (every travel build)
- **Normalize everything** into one canonical model; supplier shapes die at the adapter boundary.
- **Cache search, never cache the booking price** — recheck before you charge.
- **Booking is a saga, not a transaction** — idempotent, compensable; never charge without a confirmed supplier ref.
- **Money = integer minor units + ISO-4217**; store net + markup + sell + FX; reconcile.

## Bundled skills

- **travel-tech-architecture** ⭐ — The foundation: ecosystem (GDS/NDC/bed banks/CRS/PMS/IBE/CM/extranet),
  canonical domain model, the universal booking flow, multi-currency/FX, PCI/PII scope, look-to-book, and the
  glossary (ARI, PNR/Order, VCC, BSP, OTA/NDC).
  → `skills/travel-tech-architecture/GUIDE.md`
- **supplier-api-integration** — Integrate GDS (Amadeus/Sabre/Travelport), NDC 21.3, and bed banks
  (Hotelbeds/TBO/EAN/WebBeds/GRN) via the adapter pattern: real Hotelbeds adapter, resilient fan-out, recheck,
  rate-limit/look-to-book governance, token pooling, sandboxes.
  → `skills/supplier-api-integration/GUIDE.md`
- **booking-orchestration** — The booking saga done right: state machine, idempotency (exactly-once book),
  compensation, recheck gate, payment↔supplier money ordering, "never retry book — reconcile via retrieve,"
  PNR/voucher/on-request/hold lifecycles, mid-office queue, reconciliation.
  → `skills/booking-orchestration/GUIDE.md`
- **mapping-system** — Dedupe the same hotel/room across suppliers into one canonical entity: GIATA
  Multicodes/Room-Mapping, blocking + weighted scoring (geo/name/address), auto/review/reject thresholds,
  review queue, provenance, false-merge defense. (Book the supplier's original code.)
  → `skills/mapping-system/GUIDE.md`
- **b2b-b2c-booking-platform** — The demand side (OTA/IBE, agent portal, tour operator/DMC): declarative
  pricing/markup engine, atomic agent credit/wallet, multi-currency, payments (3DS2/SCA in; VCC/BSP out),
  itineraries/vouchers, mid/back office, B2B API-out.
  → `skills/b2b-b2c-booking-platform/GUIDE.md`
- **channel-manager-system** — Distribute a property's ARI to OTAs (Booking.com/Expedia/Agoda) and pull
  reservations back: per-channel adapters, OpenTravel connectivity, pooled inventory with atomic decrement,
  derived rates/restrictions, durable change queue, delta+full reconcile, overbooking protection.
  → `skills/channel-manager-system/GUIDE.md`
- **extranet-system** — Supplier-facing portal to load inventory/rates/availability/content/promotions/
  contracts: contract→season→rateplan→calendar→allotment model, bulk calendar editor, allotment/release
  periods, hard validation gate, roles/approval, audit, publish into the CRS.
  → `skills/extranet-system/GUIDE.md`

## Pairs well with
`backend-api-master` (auth, integrations-pro, queues/webhooks, GIS maps), `payments-master` (PSPs, 3DS2/SCA,
wallets, VCC), `business-master` (accounting-finance for net/sell ledger, white-label per agency), `ui-master`
(charts/dashboards, RTL), and `documents-master` (vouchers/invoices/itineraries).

## Note

These bundled skills are intentionally not registered as separate Cursor skills (their files are `GUIDE.md`,
not `SKILL.md`) so only this master appears in the skills list. Read the relevant `GUIDE.md` on demand.
