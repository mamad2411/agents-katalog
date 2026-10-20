# AGENTS.md (api)

Orientation for an agent working in this service. `README.md` is the full
reference — HTTP contract, every config variable, the measured numbers
behind the planner's tuning knobs. This file is a map to where things live
and the invariants worth knowing before you change them; it does not
repeat what the README already covers in depth.

Also read the root [`AGENTS.md`](../AGENTS.md) — the commit convention,
the "no `Co-Authored-By: Claude`" rule, and the cross-project platform
facts apply here too.

## The RAPTOR planner

Journey planning lives in `src/transit/`:

- `raptor.ts` / `raptorReverse.ts` — the forward and reverse RAPTOR search.
  `/plan`'s `departAfter` path runs a forward search then re-anchors and
  re-runs reverse at the resulting arrival (see README's
  [Planning](../api/README.md#planning) section); `arriveBy` runs reverse
  directly.
- `manager.ts` — `IndexManager`, which owns the built `TimetableIndex`,
  rebuilds it on every detected feed swap (polling the `gtfs.sqlite`
  symlink), and swaps the whole `AppBundle` (index, footpaths, calendar,
  translations, route lookups) into place in one synchronous step so a
  request can never see one route handler on the old feed and another on
  the new one.
- `buildWorker.ts` — the index build runs in a worker thread, not inline,
  because it's a few seconds of synchronous CPU work over ~85 MB of typed
  arrays and would otherwise stall every in-flight request on each swap.
- `rank.ts` — the effort-based ordering `/plan` applies after search
  (duration + walk weight + transfer penalty), plus the two post-search
  filters (no-transit-leg, walk-share).
- `footpaths.ts` — derives walking connections (there's no `transfers.txt`
  in the feed) from a straight-line prefilter, then Valhalla or a
  straight-line fallback.

The index is rebuilt from SQLite on every feed swap; there is deliberately
no on-disk cache of it.

## Realtime and the keyless vocabulary

`src/realtime/` resolves the Ministry of Transport's SIRI-SM feed (or a
keyless fallback) onto scheduled trips. The vocabulary an agent needs:

- `MOT_SIRI_KEY` + `MOT_SIRI_BASE_URL` — the ministry's own keyed feed.
  Both or neither; one without the other is a misconfiguration that warns
  and leaves realtime off (never a half-enabled state).
- **`keyless`** — realtime with no MOT key, reading the same national data
  through a feed that needs no credential. `REALTIME_KEYLESS_SOURCE` (env
  var) picks which one, typed as `KeylessSource` in `src/config.ts`:
  `"open-bus"` (default — the Public Knowledge Workshop's per-minute
  snapshot, positions ~1 minute old), `"stride"` (their database, 13–23
  minutes of ETL lag on a weekday), or `"off"`. `STRIDE_ENABLED=false`
  predates `REALTIME_KEYLESS_SOURCE` and is still honored as a synonym for
  `off` when the new variable is unset.
- Neither keyless feed carries ETAs, only vehicle positions — predictions
  are derived from a vehicle's distance along its scheduled trip
  (`src/realtime/match.ts`'s `predictFromDistance`), unlike SIRI-SM's own
  `predictFromCalls`.
- `wiring.ts`'s `createRealtimeResolver` closes over the *live* index via a
  getter, not a captured reference — trip-index lookups (`TripLookup`) are
  only valid against the `TimetableIndex` they were built from, and a feed
  swap invalidates them.

`GET /meta`'s `realtime` block and `GET /vehicles` are how this surfaces
externally; see the README for the full response shapes and the
Stride-position-suppression rule (Stride's lag is tolerable for a delay
estimate, not for a moving dot on a map).

## `GEOCODER=google|photon` and its cost model

`src/config.ts`'s `resolveGeocoderConfig` picks who answers
`/geocode/search` and `/geocode/place`; reverse geocoding always goes
through Photon regardless (`src/geocode/composite.ts`). Photon
(self-hosted, OpenStreetMap-based) is free but misses many businesses and
addresses; Google (Places API (New) + Geocoding API) is metered.

The cost controls, all in `src/geocode/google.ts` and `src/config.ts`, and
all worth preserving if you touch this path:

- **Session tokens** tie a typed search to its one resolve, so a session
  bills at most 12 autocomplete calls instead of one bill per keystroke.
- **No per-suggestion Place Details** — a position is only fetched once,
  for the result actually picked.
- **The `location` field mask** on Place Details keeps the call in the
  cheaper Essentials SKU rather than Pro.
- **`GOOGLE_MAPS_DAILY_REQUEST_LIMIT`** is a hard per-process daily ceiling
  on billable calls (autocomplete + place + reverse); `0` disables it, but
  the default is a real cap, not a suggestion.
- Client-side debounce and caching in `app/` reduce call volume further —
  see `app/AGENTS.md` if you're touching the search UI.

This is exactly the kind of per-request-cost feature the root
[deployment rule](../AGENTS.md#hard-won-platform-facts) exists for — any
new metered integration needs an equivalent ceiling before it ships.

## The rail bake

`api/assets/rail-geometry.json` is committed, pre-baked track geometry —
the MOT feed has no `shapes.txt` rows for rail. `npm run bake:rail`
(`src/rail/bakeMain.ts`) rebuilds it from OpenStreetMap via Overpass. Do
not hand-edit the JSON. If you change the bake, the pitfalls that cost
real detours to work out (see `src/rail/bake.ts` and `README.md`'s
[Train track lines](README.md#train-track-lines) section for the measured
numbers):

1. **Junction tracks matter.** `service=crossover/siding/spur/yard` ways
   connect the network; excluding them fragments it into islands.
2. **Snap a station to every nearby track, not just the nearest.** A
   station on a multi-track section needs all of them, or one direction
   strands.
3. **Forbid sharp turns at switches.** The routing is edge-based; without
   a turn-angle limit, OSM's switch-stub geometry reads as a U-turn.
4. The bake refuses to write when a pair is unroutable, a routed line
   exceeds 3× the straight-line distance, or the Overpass data looks stale
   (over 30 days old) — `--force` overrides the first two, never the
   underlying data problem.

## Configuration fails at boot, not at request time

Every config value in `src/config.ts` — ports, timeouts, `TZ`, the
transfer-margin numbers, `GEOCODER`, the six realtime numeric settings —
is validated eagerly at module load. An invalid value throws immediately
at process start, naming the bad value, rather than silently falling back
to a default or degrading a feature at first use. This holds **even for
settings whose feature is off** — a malformed `REALTIME_POLL_SECONDS`
fails boot even with no `MOT_SIRI_KEY` set at all, because a real
misconfiguration should be loud regardless of which features are active.

Two settings deliberately still *degrade* rather than fail boot — Valhalla
and Photon connection failures are runtime degrades (straight-line
walking, empty geocode results), not boot failures, because those are
reachability problems with a separate process, not malformed config. Don't
conflate the two: a new *env var* validation belongs in the fail-at-boot
category; a new *upstream service* failure belongs in the degrade
category. When in doubt, follow the existing split in `src/config.ts`.
