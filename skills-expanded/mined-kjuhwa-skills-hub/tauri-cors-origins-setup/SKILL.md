---
name: tauri-cors-origins-setup
description: Allow a FastAPI backend to accept requests from the full range of Tauri webview origins on macOS, Windows, and Linux, plus Vite dev.
category: fastapi
version: 1.0.0
version_origin: extracted
tags: [fastapi, cors, tauri, desktop-apps, cross-platform]
source_type: extracted-from-git
source_url: https://github.com/jamiepine/voicebox.git
source_ref: main
source_commit: 476abe07fc2c1587f4b3e3916134018ebacd143d
source_project: voicebox
confidence: high
imported_at: 2026-04-18T00:00:00Z
---

# Tauri CORS origins setup

## When to use
A FastAPI sidecar talks to a Tauri webview in dev and in production across all three desktop platforms. You keep seeing CORS errors that only reproduce on one OS, or only in dev.

## Steps
1. Seed the allowed origins list with dev + every Tauri webview origin form:
   - `http://localhost:5173` and `http://127.0.0.1:5173` (Vite dev server)
   - `http://localhost:<server_port>` and `http://127.0.0.1:<server_port>` for the backend's own port, in case the frontend is embedded behind it
   - `tauri://localhost` (Tauri on macOS)
   - `https://tauri.localhost` (Tauri on Windows/Linux in most versions)
   - `http://tauri.localhost` (Tauri on Windows in some builds)
2. Accept runtime extension via an env var like `VOICEBOX_CORS_ORIGINS="https://..., https://..."`. Split on comma, strip each entry, and extend the default list. This lets power users run with a reverse proxy or remote access without a rebuild.
3. Install `CORSMiddleware` with `allow_origins=` the computed list, `allow_credentials=True`, `allow_methods=["*"]`, `allow_headers=["*"]`. Because Tauri origins are not wildcardable (scheme varies), do NOT use `allow_origins=["*"]` — wildcards are incompatible with `allow_credentials=True` per spec.
4. Keep the CORS setup in a single `_configure_cors(app)` helper invoked by the app factory. New dev ports or platform quirks land in one place.

## Counter / Caveats
- The three `tauri.localhost` variants are all real — different Tauri versions and platforms use different schemes. Don't drop any of them "to clean up" until you've tested the matrix.
- `allow_origins=["*"]` with `allow_credentials=True` silently disables credentials in modern browsers. Use the explicit list even if it feels long.
- If you add a new origin via the env var on production, remember it must include the scheme (`https://example.com`, not `example.com`).
- In dev, Vite's port may change if 5173 is taken; consider adding 5174/5175 or reading Vite config to extend the list.

Source references: `backend/app.py` (`_configure_cors`).
