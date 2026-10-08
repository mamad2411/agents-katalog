# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Commands

```bash
npm install                    # install dependencies (Node >=20)
npm run dev                    # dev server at http://localhost:5173
npm run dev:lan                # same, accessible over LAN (Wi-Fi IP)
npm run sync:avisor            # copy avisor_v5.html from Desktop → public/avisor.html + stamp version
npm run build                  # stamp version + tsc type-check + vite build → dist/
npm run preview                # serve dist/ with service worker (production-style test)
npx tsc --noEmit               # type-check only (no emit) — used by CI
npm run build:navaids          # parse ourairports-navaids.csv → public/data/navaids-us-vor.json
npm run build:faa              # import FAA Excel workbook → public/data/ JSON files
npm run stamp:version          # write public/build-meta.json version stamp
npm run verify:deploy          # assert deployed build-meta.json matches local
npm run tunnel                 # expose port 5173 via Tunnelmole public URL
npm run desktop:dev            # Tauri dev window (requires Rust)
npm run desktop:build          # Tauri installer → src-tauri/target/release/bundle/
npm run cap:sync               # mobile:prep + npx cap sync (Capacitor iOS/Android)
npm run cap:open:ios           # open Xcode (requires Mac)
npm run cap:open:android       # open Android Studio
```

**First-time data setup** (before `npm run dev`):
```bash
npm run build:navaids && npm run build:faa
npm run sync:avisor
```

`sync:avisor` expects the primary app file at `%USERPROFILE%\Desktop\avisor_v5.html` or the path in `$AVISOR_SRC`.

## Architecture

### Two distinct "apps" in one repo

**`public/avisor.html`** — the real flight planning app. This file is **not authored here**. It is a standalone single-file app (all HTML/CSS/JS inlined) that is developed separately and copied into the repo via `npm run sync:avisor`. The `copy-avisor.cjs` script applies post-processing patches on every copy: injects `showToast()`, replaces `alert()` calls, strips `console.log`, and applies pattern-leg/bearing fixes. Never edit `public/avisor.html` directly — changes will be overwritten on the next sync.

**`src/main.ts` + `index.html`** — the Vite shell / dev home. This is what Vite serves at `/`. It provides an online/offline status indicator, a build-version display, links to `avisor.html` and `airport-brief.html`, and an IndexedDB persistence demo. The shell is compiled into `dist/` for Capacitor mobile builds.

### Offline persistence (`src/lib/persist.ts`)

IndexedDB database `avisor-flight-v1` with two object stores:
- `kv` — key/value snapshots, used for persisting flight plan state (`saveFlightSnapshot` / `loadFlightSnapshot`)
- `events` — append-only log of in-flight updates (`appendFlightEvent` / `loadRecentEvents`, cursor traversed newest-first)

### Static data pipeline

FAA and OurAirports data lives in `public/data/` as pre-built JSON/CSV files. Build scripts in `scripts/` process raw sources:
- OurAirports CSVs (airports, runways, navaids, frequencies) — bundled for offline lookup
- FAA Excel workbook (via `import-faa-workbook.cjs`) — produces `faa-airports-db.json`, `faa-runways-by-ident.json`, `faa-frequencies-by-ident.json`, etc.

### Deployment split

Netlify serves **`public/` directly** (no build step) — that is the production web/PWA deployment. The `dist/` directory is for Capacitor (iOS/Android) and Tauri (desktop) native shell builds only.

### Dev server proxy

Vite proxies two aviation API namespaces to avoid CORS:
- `/awc-api/*` → `https://aviationweather.gov/api/*`
- `/faa-api/*` → `https://api.faa.gov/*`

Netlify mirrors these same redirect rules in `netlify.toml`.

### Environment variables

Copy `.env.example` to `.env` before running locally. CI injects these via secrets:
- `VITE_OPENAI_API_KEY` — OpenAI (AI briefing features)
- `VITE_WEATHER_API_KEY` — Weather API

### Multi-platform

| Target | Tool | Web root |
|---|---|---|
| Web / PWA | Netlify static | `public/` |
| iOS / Android | Capacitor 8 | `dist/` |
| Desktop | Tauri 2 | `dist/` |

Capacitor app ID is `com.avisor.app`. To hot-reload the native shell from Vite during Capacitor dev, uncomment the `server.url` block in `capacitor.config.ts` and set your LAN IP.
