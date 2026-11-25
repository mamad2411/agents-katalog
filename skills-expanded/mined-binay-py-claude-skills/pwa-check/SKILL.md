---
name: pwa-check
description: Check whether a web app installs as a PWA and works offline, and say exactly what to fix. Opens it in a throwaway headless Chrome/Edge, asks Chrome for its own installability verdict over the DevTools Protocol, validates the manifest (name, start_url and scope, display, id, colors, 192/512 icons with their real pixel sizes, maskable icon, screenshots for the richer install dialog), apple-touch-icon, HTTPS and viewport, checks the service worker (registered, controls the page, fetch handler, scope, cache versioning), then goes offline and reloads start_url and a second page. Works on a live URL or a local build folder. Use when the user asks "why won't my app install", "make this a PWA", "is my manifest right", "check my service worker", "does it work offline", "add to home screen doesn't work", or after adding a manifest or service worker.
---

# pwa-check

`scripts/pwa-check.mjs` is zero-dependency Node 22+. It starts its own headless Chrome / Edge / Brave / Chromium with a temporary profile (never the user's browser or logins) and removes it afterwards. Set `BROWSER=/path/to/chrome` if none is found. It only reads; folder mode serves the folder read-only on a random `127.0.0.1` port.

```
node pwa-check.mjs https://app.example.com          # live site (https, or http://localhost:5173)
node pwa-check.mjs ./dist                            # build folder
node pwa-check.mjs ./dist --spa                      # host answers unknown routes with index.html (most SPA hosting)
node pwa-check.mjs ./dist --start /app/              # open this page first (app under a sub-path)
node pwa-check.mjs <target> --page2 /settings        # second in-scope page for the offline test (default: first in-scope link)
node pwa-check.mjs <target> --json                   # full result on stdout
```

Takes 10–25 s. Exit code 0 = installs and works offline, 1 = won't install or broken offline, 2 = could not run.

## Reading the report
- **Chrome's own verdict** comes from `Page.getInstallabilityErrors` in the running browser, so it reflects that Chromium version's rules. It answers "can desktop Chrome/Edge install this right now".
- **WON'T INSTALL**: blockers (no manifest link, manifest 404 or invalid JSON, no name, display `browser`, no usable icon, plain http). Fix these first.
- **BROKEN OFFLINE / ON LAUNCH**: it may install, but start_url returns an error, there is no service worker, the worker has no (or an empty) fetch handler, doesn't control the page or start_url, or start_url shows the browser's offline error / a blank page when offline.
- **WARNINGS**: things the docs require or recommend that Chrome tolerates today: missing 192/512 icons, declared icon size not matching the file, no maskable icon, `"purpose": "any maskable"`, no screenshots (basic instead of richer install dialog), no `id`, start_url outside scope, missing colors/description/apple-touch-icon, unversioned cache names, old caches never deleted, a second page that fails offline (no navigation fallback).
- Every problem line has a `fix:` line. Apply it, rebuild, and re-run the same command to confirm. After deploying, run it against the live URL too: hosting (SPA fallbacks, content types, redirects) often differs from the folder.

## Workflow
- Point folder mode at the **build output** (`dist/`, `build/`, `out/`), not the source folder. Dev servers and `vite-plugin-pwa` usually disable the service worker in development.
- If the report says start_url returns 404 in folder mode and the real host serves `index.html` for every route, re-run with `--spa`.
- For a new PWA: add `manifest.webmanifest` (name, short_name, description, id `/`, start_url `/`, scope `/`, display `standalone`, theme_color, background_color, icons 192 + 512 with purpose `any`, a separate 512 `maskable` icon, one `wide` and one `narrow` screenshot), link it with `<link rel="manifest">` on every page, add a 180×180 `apple-touch-icon`, then a service worker that precaches the app shell, answers navigations network-first with a cache fallback, puts a version in the cache name, and deletes old caches in `activate`. With a bundler, prefer Workbox / vite-plugin-pwa (`injectManifest` or `generateSW`) so precache entries carry revisions.

## Criteria used (checked against web.dev, developer.chrome.com, MDN and Chromium source, Nov 2026)
- Chrome needs: HTTPS or localhost; a manifest with name or short_name, start_url, display `standalone`/`fullscreen`/`minimal-ui` (or that as the first `display_override` value), and a square PNG/SVG/WebP icon of at least 144 px with `sizes` set and purpose `any`. web.dev and MDN list 192 and 512 icons as required. `prefer_related_applications: true` only blocks install on Android.
- A service worker is **no longer an install requirement** (dropped for menu install in Chrome 108 mobile / 112 desktop; current Chromium has no service-worker installability error). It is still what makes the app work offline, so its absence is reported under offline, not install.
- Richer install dialog: screenshots 320–3840 px, long side ≤ 2.3× the short side, PNG or JPEG, same aspect ratio per form_factor; `wide` for desktop, `narrow` (or no form_factor) for mobile.

## Limits
- **iOS Safari can't be tested here.** Only the iPhone/iPad tags are checked (apple-touch-icon size and type); "Add to Home Screen" behavior must be checked on a real device. Firefox and Safari install UIs aren't tested either.
- The automatic install prompt also depends on user engagement (a click and ~30 s on the page); that and `beforeinstallprompt` aren't simulated.
- Offline uses DevTools network emulation on the page **and** on the service worker (page-only emulation lets a network-first worker reach the network). The browser's own service-worker update check isn't covered; in folder mode any other request reaching the server is reported as a leak.
- Cache-versioning advice is a static reading of the current sw.js; it can't compare deploys.
- A `serviceWorker.register()` that runs more than ~8 s after load or only after a click isn't seen. Pages behind a login can't be checked (the throwaway profile has no cookies).
