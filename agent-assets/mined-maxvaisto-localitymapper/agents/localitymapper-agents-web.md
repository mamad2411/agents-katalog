# web

Vite + React web app. Plain JavaScript (JSDoc, not TypeScript; per ADR 0004).

## Commands

| Task | Command |
|---|---|
| Install deps | `pnpm install` (from repo root) |
| Run dev server | `pnpm dev` |
| Run tests | `pnpm test` |
| Build | `pnpm build` |

## MapLibre GL JS setup

- Map style uses inline OSM raster tiles (no API key needed). Defined as a plain object in `App.jsx`.
- MapLibre requires WebGL; jsdom cannot render it. **Always mock `maplibre-gl` in tests** with the pattern in `App.test.jsx`.
- CSS import (`maplibre-gl/dist/maplibre-gl.css`) must also be mocked in tests via `vi.mock('maplibre-gl/dist/maplibre-gl.css', () => ({}))`, and `css: false` is set in `vite.config.js` test options.
- React deduplication: web and mobile are kept on the same React major. If you see "Invalid hook call" in tests, check that `react`, `react-dom`, and test renderer packages resolve to the same React major.

## Consuming @localitymapper/shared

Imported as a workspace package (`workspace:*` in `package.json`):

```js
import { boundaryForCell, colorForDuration, fetchTravelTimeGrid } from '@localitymapper/shared'
```

- `boundaryForCell(h3CellId)` -> H3 polygon boundary for map rendering
- `colorForDuration(seconds)` -> HSL color string (green to red over 0-3600s); gray for null
- `fetchTravelTimeGrid({serviceArea, destinations, timeBucket, baseUrl})` -> cell-first travel-time grid

The web app should not call `/durations` or `/route-detail`; those obsolete point-to-point endpoints were removed. Selected cells show grid-derived durations only until the future sparse `POST /cell-route` feature exists.

## TDD

New code starts with a failing test. Use the `tdd` skill for any new feature area.
