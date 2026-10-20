---
name: spa-fallback-fastapi-mount
description: Serve a built Vite/React SPA from FastAPI with asset mounting, catch-all routing, and path-traversal protection.
category: fastapi
version: 1.0.0
version_origin: extracted
tags: [fastapi, spa, static-files, security, routing]
source_type: extracted-from-git
source_url: https://github.com/jamiepine/voicebox.git
source_ref: main
source_commit: 476abe07fc2c1587f4b3e3916134018ebacd143d
source_project: voicebox
confidence: high
imported_at: 2026-04-18T00:00:00Z
---

# SPA fallback FastAPI mount

## When to use
You have one FastAPI process that in some deployments (Docker, web mode) also serves the built SPA, and in other deployments (desktop sidecar, API-only) does not ship the SPA. The mount must be a no-op when the frontend directory is absent.

## Steps
1. Detect the built frontend at startup (e.g. `Path(__file__).resolve().parent.parent / "frontend"`). If `frontend_dir.is_dir()` is false, return — keep API-only deployments clean.
2. Mount hashed assets from `frontend/assets/` under `/assets` using `StaticFiles`. Vite emits content-hashed filenames here, so long-term caching is safe.
3. Register a catch-all route **last**: `@app.get("/{full_path:path}")`. Because FastAPI resolves routes in registration order, all API routes must be added before this — register it only from inside `_mount_frontend` invoked after `register_routers(app)`.
4. Inside the catch-all, resolve the requested path under the frontend directory (`file_path = (frontend_dir / full_path).resolve()`). Guard with `file_path.is_relative_to(frontend_dir)` to reject path-traversal (`../../etc/passwd`). If the resolved file exists and is inside the frontend dir, serve it; otherwise serve `index.html` so client-side routes like `/voices`, `/settings` work.
5. Always return `index.html` with `media_type="text/html"` on the fallback — some static file helpers default to `application/octet-stream` for unrecognized extensions.

## Counter / Caveats
- If you mount before registering API routers, the catch-all will swallow `/api/...` requests. Always mount last.
- `is_relative_to` is only available in Python 3.9+. If you need broader support, compare `resolved.parts[: len(root.parts)] == root.parts`.
- Do not set `html=True` on `StaticFiles` for the whole frontend — it conflicts with the explicit catch-all and hides 404s.
- When the frontend emits new assets, old hashed files remain in cache but `index.html` does not — make sure `index.html` is served with short TTL (via your reverse proxy) so clients pick up new builds.

Source references: `backend/app.py` (`_mount_frontend`).
