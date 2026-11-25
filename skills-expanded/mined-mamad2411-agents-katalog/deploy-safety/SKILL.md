---
name: deploy-safety
description: Deploy-path safety checklist for any change touching vite.config.js, netlify.toml, GitHub Pages CI, or code that builds a shareable/public URL. Use whenever editing build config or writing any code that constructs a link a client or the public will click.
---

# Deploy-Path Safety

This app deploys to two targets that serve from different roots: Netlify (primary, root `/`) and GitHub Pages (secondary, `/creative-companion/`). This entire bug class is invisible in local dev — `npm run dev` always serves from root — and only breaks on a real deployed subpath or a real public deep link.

## Non-negotiable

- **`vite.config.js`'s `base` must never be `'./'`.** Relative asset URLs resolve against the *current route*. A deep link like `/c/:portalId` then requests `/c/assets/index-*.js`, misses, gets the SPA rewrite to `index.html`, and the browser tries to parse HTML as JavaScript — a blank page on every client link, invisible if you only ever test the root route.
- **Every public/shareable URL goes through `publicUrl()`/`routePath()`** (`src/lib/appPaths.js`). Never `window.location.origin`, never a raw `location.pathname`, never a hand-built `/f/` or `/c/` string anywhere else — any of those breaks the moment the app is served from a subpath.
- **SPA fallback must exist on both targets** — `netlify.toml` + `public/_redirects` for Netlify, `dist/404.html` (copied from `index.html` in CI) for Pages. Without it a deep link 404s instead of loading the shell.

## Before shipping a change here

- If you touched `vite.config.js`, `netlify.toml`, `_redirects`, or the Pages CI workflow: build with both `GITHUB_PAGES` unset and `GITHUB_PAGES=true`, and confirm the `base` differs correctly between them.
- If you added a new public route or a new place that builds a link to one: confirm it uses `appPaths.js`, then actually test it as a deep link (not just from in-app navigation) — the failure only shows up on a fresh load at that path, not on a client-side route change.
