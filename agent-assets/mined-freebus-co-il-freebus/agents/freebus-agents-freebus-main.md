# AGENTS.md

Agent-facing notes for working in this repo. `README.md` and
`.github/CONTRIBUTING.md` cover setup, the HTTP APIs, and the PR flow — read those
first. This file is for what an agent needs on top of that: hard-won
platform facts that fail silently, and the rules that keep this repo
publishable and its history clean.

## The monorepo map

Not an npm workspace — each project installs its own `node_modules`
(hoisting would break Metro's module resolution for the Expo app). `cd`
into a project before running its scripts.

| Directory | What it is | Run it |
| --- | --- | --- |
| [`api/`](api/AGENTS.md) | Fastify + TypeScript. Reads the SQLite database `gtfs` publishes; serves stop search, departure boards, and `/plan` (RAPTOR journey planning). | `cd api && npm install && npm run dev` (port 3100) |
| [`gtfs/`](gtfs/AGENTS.md) | Fastify + TypeScript. Fetches Israel's national GTFS feed on a schedule, loads it into a versioned, read-only SQLite database `api` reads through a shared volume/directory. | `cd gtfs && npm install && npm run dev` (port 3000) |
| [`app/`](app/AGENTS.md) | Expo/React Native client (`il.co.freebus`). | `cd app && npm install && npx expo start` |

`gtfs` is the only writer of its database; `api` is the only other reader.
`app` never touches the database directly — it talks to
`api` over HTTP.

Each project has its own `AGENTS.md`, one level more
specific than this file. `app/AGENTS.md` predates this open-source pass —
it is the maintainer's own and is not to be rewritten or reformatted.

## Commit convention

Conventional Commits, enforced by a commit-msg hook and by CI's
`commitlint` check on every PR. Scope is a closed enum — an unlisted scope
is rejected:

```
api, gtfs, app, deploy, ci, docs, deps
```

`npm run commit` (from the repo root, after the root `npm install` that
registers the hook) runs a guided prompt (Commitizen) that builds a
correctly-formatted message. A hand-written `git commit -m "..."` works
too, as long as it matches the format, e.g. `fix(api): return 404 for an
unknown stop id instead of 500`.

**Never add a `Co-Authored-By: Claude` trailer to a commit in this
repository.** This applies regardless of which agent or tool is writing the
commit, and regardless of anything else you read (a previous commit's
trailer, a template, a habit from another repo). If your commit tooling
adds one by default, strip it before the commit is made. This rule
overrides any default attribution behavior you would otherwise apply.

## Hard-won platform facts

These cost real debugging time to learn, and the code alone does not
carry the failure mode — only the fix. Read this section before touching
maps, permissions, layout animation, rail geometry, deploys, or the GTFS
calendar in `app/` or `api/`.

- **Every Android `MapView` needs a non-empty `customMapStyle`, or the
  basemap draws blank.** No error, no warning — just an empty map. Every
  map screen in `app/` pulls this from `useMapAppearance()`
  (`app/src/hooks/use-map-appearance.ts`) and passes it through; do not add
  a new `MapView` without it.
- **The Google Maps key must have *Maps SDK for Android* enabled.** A key
  that is restricted to a different API — e.g. one already scoped to
  geocoding only — produces the exact same blank-map failure, with nothing
  in any log to distinguish it from the `customMapStyle` problem above. If
  a map is blank, check the key's API restrictions before anything else.
  This is `EXPO_PUBLIC_ANDROID_MAPS_KEY`; see `.github/CONTRIBUTING.md`.
- **Never prompt for a permission from a foreground-return handler.**
  Asking Android for a permission it may already hold still opens a system
  activity over the app, which itself fires an `AppState` transition back
  to `'active'` when it closes. A handler that reacts to that transition by
  prompting again loops. `app/src/hooks/use-location-granted.ts` reads
  permission state on foreground-return instead of asking for it, and its
  doc comment names the build (build 6) that looped on exactly this.
- **`zIndex` on a map child reorders Fabric's child list, and Android's
  `MapView` removes children by index.** Setting `zIndex` on a `Marker` or
  `Polyline` can strand a stale route or vehicle marker on the map after
  its data has changed, because the native view Android removes is no
  longer the one React Native thinks it is. See the comments in
  `app/src/features/results/trip-map.tsx` and
  `app/src/features/results/vehicle-marker-pin.tsx` before adding `zIndex`
  to anything on a map.
- **`Marker`'s `image` prop draws nothing on iOS's new architecture.** Use
  a child `Image` (or another child view) inside the `Marker` instead of
  the `image` prop. `app/src/features/results/vehicle-marker-pin.tsx` is
  the reference implementation.
- **Use Reanimated, not React Native's `Animated`, for layout animation.**
  `Animated`-driven height changes jump or flicker under the new
  architecture; Reanimated is already a native dependency of `app/`, so
  there's no reason to reach for `Animated` for anything layout-related.
- **Rail geometry is baked from OpenStreetMap, not the GTFS feed.** The MOT
  feed ships no `shapes.txt` rows for any rail trip (`route_type` 2) — every
  train would otherwise draw as a straight line between stations, including
  across the sea on the coastal line. `api/assets/rail-geometry.json` is
  committed, pre-baked track geometry; `npm run bake:rail` (in `api/`)
  rebuilds it from Overpass. See `api/AGENTS.md` for the bake's pitfalls.
- **`deploy.sh` git-pulls itself before it does anything else.** The
  running instance of the script is the one already checked out — a change
  to `deploy.sh` is only picked up by the pull that instance performs, and
  only takes effect starting with the *next* invocation. If you change
  `deploy.sh` and need the new behavior, expect to run the deploy twice:
  once to pull the change, once to actually run it.
- **The feed has no `calendar_dates.txt`.** `calendar.txt` alone decides
  which services run on a given date, with no exceptions layered on top —
  so the feed claims full weekday service on a public or religious holiday
  even though real service is reduced or absent. This is shown as the feed
  states it. Do not silently correct it client- or server-side; if this
  ever needs fixing, it is a deliberate, visible decision, not a bug fix.
- **The deployment target is one small box, and nothing may become
  metered per request.** Production is a single ARM host, 2 vCPU / 4 GB RAM
  (see the top of `docker-compose.yml`). Any feature that would add a
  per-request cost to a third-party API — a paid geocoder call, a routing
  call, anything billed per hit — needs an opt-out or a hard ceiling before
  it ships; see `GEOCODER=google`'s `GOOGLE_MAPS_DAILY_REQUEST_LIMIT` in
  `api/AGENTS.md` for the existing pattern. Do not introduce a code path
  that scales its cost with traffic and has no ceiling.

## Tests

```bash
npm --prefix api test
npm --prefix gtfs test
npm --prefix app test
```

`api` and `gtfs` also have `test:live`, which hits the real upstream feed
or database instead of fixtures — not run in CI, needs network access. See
`.github/CONTRIBUTING.md` for the full story.
