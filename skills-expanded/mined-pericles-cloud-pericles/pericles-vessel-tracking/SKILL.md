---
name: pericles-vessel-tracking
version: 2026.08.0
description: >
  How to put REAL vessel positions on Atlas via AISstream — replacing
  MockPositionFeed's synthesized motion with live AIS reports, behind the
  existing ShipmentPositionFeed seam. Use this WHENEVER you build or change
  LivePositionFeed, the AIS WebSocket subscriber, MMSI resolution, the
  per-organization AISstream credential, or the mock→live switchover. Encodes
  the push/pull mismatch (AIS streams; Atlas polls), the MMSI identity gap (BOL
  gives vessel NAMES, AIS keys on MMSI), per-tenant key storage under
  Integrations, and the untrusted-feed rules that apply because AIS is
  unauthenticated public radio.
doctrine_refs: [§4 (pre_validation), §5 (data access), §11 (tenant isolation); pericles-external-feeds; pericles-security-threat-model]
depends_on: [pericles-atlas-mocker, pericles-atlas-ui, pericles-external-feeds, pericles-data-model, pericles-tenant-isolation]
last_reconciled: 2026-08-13
---

# Pericles Vessel Tracking — AISstream (build skill)

Atlas currently shows **real ships on real lanes at invented positions**
(`MockPositionFeed` — see `pericles-atlas-mocker`). This skill replaces the
position with a real one from **AISstream**, and nothing else. Suppliers,
carriers, lanes, ports and vessel names were already real; the mock exists
only because there was no position source.

**Build `LivePositionFeed`, do not build a second pipeline.** The seam already
exists and every consumer depends only on it:

```
ShipmentPositionFeed.getPositions(shipments, now?) → PositionUpdate[]
  • MockPositionFeed  — interpolated motion                    (built)
  • LivePositionFeed  — AIS lat/lon, same PositionUpdate shape (this skill)
```

`getPositionFeed()` in `backend/src/integrations/tracking/index.ts` already
throws on `TRACKING_MODE=live` with a message pointing here. Making that throw
go away is the whole job.

## When to use this skill

Building or changing: `live-feed.ts`, the AIS WebSocket subscriber, the
position cache, MMSI resolution, the AISstream credential in org Integrations
settings, or anything that decides whether Atlas shows `source: 'mock'` vs
`'live'`.

## The three problems this integration actually has

Everything below follows from these. Solve them in this order — each is a
prerequisite for the next.

### 1. AIS pushes; Atlas polls

AISstream is a **WebSocket that streams continuously**. `ShipmentPositionFeed`
is a **request/response call** (`getPositions()`), and Atlas polls
`GET /api/shipments/positions` (`frontend/src/lib/useShipmentPositions.ts`).
You cannot open a socket per request — the subscription must be sent within
**3 seconds** of connect, and the first position report for a given vessel may
be minutes away.

**Therefore:** a long-lived subscriber writes into a cache; `getPositions()`
reads the cache and never blocks on the network.

```
AISstream WS ──► AisSubscriber (one per org credential, process-lifetime)
                      │ validates + clamps each report
                      ▼
                 PositionCache  (MMSI → last known report + received_at)
                      ▲
                      │ synchronous read, no network
              LivePositionFeed.getPositions()  ──► PositionUpdate[]
```

The subscriber is a **process singleton**, for the same reason
`mockFeedSingleton` is: state must survive across requests. This is also why
the backend cannot go serverless (`CLAUDE.md`, Deployment).

Cache in memory for the hot path, and **mirror to `KeyValueStore`**
(`pericles-postgres-queue`) so a container restart doesn't blank Atlas for
however long it takes vessels to re-report. No Redis.

### 2. We have vessel NAMES; AIS has MMSIs

`Shipment` carries `vessel_name` and `vessel_code` — **no MMSI, no IMO**
(`backend/prisma/schema.prisma`, Vessel section). AISstream's
`FiltersShipMMSI` takes MMSI numbers and accepts at most **50**. Vessel names
are not unique, not stable, and not authoritative.

**Therefore:** resolution is a real subsystem, not a lookup you inline.

- Add a `VesselIdentity` table: `{ organization_id, vessel_name, mmsi, imo,
  confidence, resolved_at, source }`, unique on `(organization_id, vessel_name)`.
  Tenant-scoped like every other table (`pericles-tenant-isolation`) even
  though MMSI is public — the *interest* in a vessel is customer data.
- Resolve names → MMSI out-of-band (a scheduled job, not the request path).
  Seed from `ShipStaticData` messages, which carry both `ShipName` and MMSI:
  subscribe to a bounding box around a known lane, harvest the pairs, match on
  normalized name.
- **A name match is a hypothesis, not a fact.** Store `confidence` and require
  a threshold before a resolved MMSI drives a dot. A wrong match puts a
  customer's cargo on the wrong ocean — worse than showing nothing.
- Until an MMSI is resolved, that shipment has **no live position**. See the
  degradation rule below.

**The 50-MMSI cap is a hard architectural constraint.** A tenant with 200
tracked vessels needs either multiple subscriptions (one connection each) or
bounding-box subscriptions filtered client-side. Prefer MMSI filtering while
you fit — it is far cheaper than filtering a global firehose ("300 messages a
second" for a global subscription, and AISstream closes the connection if your
queue backs up).

### 3. AIS is unauthenticated public radio

Anyone with a transmitter can broadcast any MMSI, position, and ship name.
Spoofing and "dark" vessels are routine in this domain. Per
`pericles-external-feeds`, **treat every message as untrusted input**:

- Validate every message with a Zod schema before it touches the cache.
- Clamp/reject: latitude ∉ [-90, 90], longitude ∉ [-180, 180], and AIS's
  documented not-available sentinels (`TrueHeading` 511, lat 91, lon 181).
- **Drop any report whose MMSI is not in this org's resolved set.** A
  bounding-box subscription returns every vessel in the box, including ones
  belonging to other tenants' voyages. Admitting an unrequested MMSI to a
  tenant's cache is a cross-tenant leak (`§11`).
- Never let AIS text (`ShipName`) reach an LLM prompt unescaped — it is feed
  content like any other (`pericles-prompts`, `utils/prompt-safety.ts`).
- A position that jumps implausibly far since the last report (> ~50 kn
  implied speed) is a spoof or a bad decode. Reject it; do not average it in.

## The credential lives in org Integrations settings

The AISstream API key is **per organization**, configured in the UI, not an
env var. Reuse the existing machinery rather than inventing a parallel one:

| Piece | Where | Note |
|---|---|---|
| Storage | `DataSourceToolConfig` | `data_source: 'maritime'`, `tool_id: 'aisstream'`, `tool_name: 'AISstream'` |
| Write key | `PUT /api/organizations/:orgId/tool-configs/maritime/aisstream/api-key` | exists |
| Status | `GET …/api-key-status` | exists; returns configured-or-not, never the key |
| Test | `POST …/test-api-key` | extend: connect, subscribe, expect a message or `{"error": "Api Key Is Not Valid"}` |
| UI | `frontend/src/app/(portal)/manage/settings` → Integrations tab | add an AISstream card next to SAP |
| Tuning | `DataSourceToolConfig.config` JSON | bounding boxes, poll/staleness thresholds |

**Fix the storage before you put a real key in it.** `api_key_encrypted` is
currently **base64, not encryption** — `auth-server.ts` says so in a comment
("base64 encoded for basic obfuscation - in production use proper
encryption"). Base64 is not a security control. Before AISstream keys land
there, implement AES-256-GCM per `.claude/rules/11-security.md` with the key
from env, and migrate existing rows. Any other integration storing a real
credential inherits the same fix.

Rules that apply regardless: never log the key, never return it in an API
response (status only), never put it in a `PositionUpdate`.

## Mapping AIS → PositionUpdate

`PositionUpdate` does not change. That is the point of the seam — no UI
change, no schema change on the read path.

| PositionUpdate field | Live source |
|---|---|
| `position` | `Message.PositionReport.Latitude/Longitude` |
| `bearing` | `TrueHeading` if ≠ 511, else `COG` |
| `polyline` | **still `planSeaRoute()`** — AIS gives points, not intended routes |
| `percent` / `covered_km` / `remaining_km` | project the AIS point onto the planned polyline, then use the existing cumulative-distance math |
| `eta` | Terminal49 when it lands; until then derive from `remaining_km` and `SOG` (fall back to `oceanKmPerDay`) |
| `status` | from `NavigationalStatus` + progress: moored/anchored near destination → `arrived`; underway → `in_transit` |
| `vesselName` | keep the **BOL** name, not `ShipName` — ours is the customer's contract data; AIS text is untrusted and often garbage |
| `source` | `'live'` — only when the position genuinely came from AIS |

**Projecting onto the route is required, not optional.** The vessel will not
sit on your great-circle polyline; take the nearest point on the polyline and
its cumulative distance. Guard the degenerate case — a vessel far off-route
(diverted, or a bad match) should be flagged, not silently snapped to a
plausible-looking spot.

## Degradation: never silently lie about a position

Vessels report irregularly. Coastal AIS coverage is good; mid-ocean gaps of
hours are normal on a free tier. Decide per shipment, per request:

```
fresh AIS report (< STALE_AFTER_MS)   → live position,    source: 'live'
stale report                          → last known point, source: 'live', mark stale
no MMSI / never reported              → mock interpolation, source: 'mock'
```

`source` is already on `PositionUpdate` and already drives the "simulated
motion" labeling in the UI. **A mock dot must never claim `source: 'live'`** —
this is the diligence-critical property the field was added for, and a hybrid
fleet (some resolved, some not) is the normal state, not an edge case. Atlas
should show the distinction; a customer must be able to tell an observed
position from an inferred one.

Do not fail the whole request because one vessel is missing —
`getPositions()` already omits unresolvable shipments (`pericles-external-feeds`,
graceful degrade).

## Connection discipline

- **Reconnect with exponential backoff and jitter.** A tight reconnect loop
  against a beta service with no SLA is how you get an API key banned.
- Re-subscribe on every reconnect; a socket without a subscription in 3s is
  dead weight.
- Respect **max 1 subscription update per second**. Batch MMSI-set changes
  (a resolver job adding vessels one at a time will trip this).
- A new subscription **replaces** the old one — it is not merged. Always send
  the complete MMSI set.
- Watch for the queue-overflow disconnect: if you subscribe to a wide box and
  consume slowly, AISstream closes the connection. Filter narrowly, parse
  cheaply, never do DB writes inline in the message handler.
- One connection per org credential. Do not multiplex tenants over one socket
  — it makes the isolation rule above unenforceable.

## Observability

Per `pericles-observability`, this path must be legible when it silently
stops working (the likeliest failure — a socket that is open but delivering
nothing):

- connection state, last message received at, messages/sec
- per-org: vessels subscribed, vessels reporting, resolution coverage
  (`resolved MMSIs / tracked vessels`)
- rejected-message counts by reason (bad schema, out-of-range, unknown MMSI,
  implausible jump) — a spike in "unknown MMSI" means the subscription and the
  resolved set have drifted apart
- `last_success_at` / `last_error_at` / `last_error_message` on the
  `DataSourceToolConfig` row, which the settings UI already surfaces

## Testing

`pericles-testing`; Vitest, no network in unit tests.

- Feed recorded AISstream frames through the parser — including malformed
  ones, sentinel values, and an out-of-range spoof — and assert what reaches
  the cache.
- Cross-tenant: inject a report for an MMSI not in org A's resolved set;
  assert it never appears in org A's positions.
- Projection: a vessel exactly on route, off route, past the destination, and
  on the wrong side of the antimeridian.
- Degradation: fresh → stale → absent, asserting `source` flips to `'mock'`
  only in the absent case.
- The whole feed against a fake subscriber, no socket.

## Build order

1. Real encryption for `api_key_encrypted` (blocks everything else).
2. `VesselIdentity` + resolver job; measure coverage before building on it.
3. `AisSubscriber` + `PositionCache`, validation and tenant filtering included
   from the first commit — not bolted on later.
4. `live-feed.ts` implementing `ShipmentPositionFeed`; delete the throw in
   `getPositionFeed()`.
5. Integrations UI card + `test-api-key`.
6. Atlas labeling for live vs simulated.

Ship 1–3 before flipping any tenant to `TRACKING_MODE=live`. The mock stays —
it is the offline/demo path and the fallback for unresolved vessels, and
`pericles-atlas-mocker` remains the skill for it.

## Reference

Verbatim API facts (endpoint, subscription shape, message envelope, limits):
`references/aisstream-api.md`. Upstream: https://aisstream.io/documentation —
service is **beta, no SLA**, so treat availability as best-effort and never
let an AIS outage take down Atlas.
