# LocalityMapper - top-level orientation

## What this is

A transit-travel-time visualizer for apartment hunting. Restart of an older prototype. See `README.md` for the user-facing description.

## Repository layout

```
backend/         # FastAPI app, uv-managed Python
web/             # Vite + React web app
mobile/          # Expo + React Native mobile app
shared/          # JS package: API client, tile math, color fn, URL state
fixtures/        # Recorded development data
docs/adr/        # Architecture decision records (numbered, append-only)
```

Each component has its own `CLAUDE.md` and `AGENTS.md` with run commands, conventions, and gotchas. Read the relevant one before working in that directory.

## Standing practices

- **Test-driven development.** New code starts with a failing test. Smoke tests required at scaffold time. See ADR 0008. Use the `/tdd` skill when starting a new feature.
- **Architecture decisions are recorded.** Every load-bearing decision goes in `docs/adr/NNNN-short-name.md` using `docs/adr/template.md`. ADRs are append-only; supersede via a new ADR rather than editing.
- **Cost discipline.** Grid calculation goes through the configured r5py grid engine or the static development client. Avoid tight loops against live engines.
- **Grid API first.** The main app uses `/travel-time-grid`; the obsolete point-to-point `/durations` and `/route-detail` paths have been removed. See ADR 0013.
- **Shared logic lives in `shared/`.** Anything used by both web and mobile (API client, tile math, color, URL codec) lives there with unit tests. Do not duplicate.

## Locked technical choices

Read the ADRs for full context. Quick reference:

| Concern | Choice | ADR |
|---|---|---|
| Repo shape | Monorepo (pnpm + uv) | 0001 |
| Backend | Python + FastAPI | 0002 |
| Routing | r5py grid engine | 0013 |
| Web / mobile | React + Vite / Expo + RN | 0004 |
| Map display | MapLibre + OSM | 0005 |
| Caching | Engine-owned for grid path | 0013 |
| Aggregation | Max duration across destinations | 0008 |

## Issue workflow

Work is tracked as GitHub issues on `maxvaisto/LocalityMapper`. Issues are tracer-bullet vertical slices. Each PR closes one issue. Branch names: `<issue-number>-<short-slug>`.

## Out of scope for v1

- User accounts and saved searches (deferred to v2).
- Realtime GTFS-RT integration (deferred).
- Auto-recompute on map pan/zoom (click-to-recompute only; see ADR 0008 / issue #5).
- Cities outside Finland (would require a different grid engine/provider).
