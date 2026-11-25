---
name: rc-sveltekit
description: Implements and reviews SvelteKit 2 apps with Svelte 5 and Bun — SSR load, form actions, hooks.server, cookies/sessions, adapter-node deploy, CSRF/CSP, and testing. Use when building or changing SvelteKit routes, SSR, forms, or VPS Bun adapters. Do not use for React/Next, Axum APIs alone (rc-axum), or plain static Svelte without Kit.
user-invocable: true
model: sonnet
effort: medium
---

# SvelteKit 2 + Svelte 5

Full-stack UI with SSR/SEO and progressive enhancement. Target: **SvelteKit 2.x**, **Svelte 5** (runes), **adapter-node** build run under **Bun ≥ 1.3**. Pair with `rc-axum` when the API is a separate Rust service.

## Core workflow

1. **Routes** — file-based `src/routes`; prefer server `load` for private/SEO data.
2. **SSR** — `+page.server.ts` for data that must hit the API with secrets; never put secrets in `PUBLIC_*`.
3. **Forms** — form actions + `fail()` for validation; progressive enhancement.
4. **Hooks** — `hooks.server.ts` for session → `event.locals`; keep locals in sync after actions that change cookies.
5. **Security** — CSRF (built-in), cookie flags, CSP. Read `references/security.md`.
6. **Deploy** — adapter-node, `HOST=127.0.0.1`, reverse proxy. Read `references/ssr-deploy.md`.
7. **Test** — Vitest + Playwright as needed. Read `references/testing.md`.

## Reference guide

| Topic | File | Load when |
| ----- | ---- | --------- |
| Load, actions, layout, env | `references/guide.md` | Building routes |
| CSRF, cookies, CSP, XSS | `references/security.md` | Auth/sessions/public pages |
| adapter-node, env, VPS | `references/ssr-deploy.md` | Deploy / SSR config |
| Unit & e2e tests | `references/testing.md` | Tests |

## Must do

- Use **Svelte 5** runes (`$state`, `$props`, `$derived`) in new components unless the repo is still Svelte 4.
- Server-only secrets via `$env/dynamic/private` or `$env/static/private` — never `PUBLIC_`.
- Same-origin API proxy in prod (Caddy `/api` → Axum) so the browser uses relative URLs.
- Type loads/actions with generated `./$types`.
- After mutating cookies in an action, update `event.locals` before subsequent loads in the same request.

## Must not do

- Fetch the public internet from `load` with browser cookies intended only for first-party API without understanding credential rules.
- Store access tokens in `localStorage` when httpOnly cookies are viable.
- Disable CSRF protection without a written threat-model exception.
- Ship `adapter-auto` to a raw VPS when **adapter-node** is the actual runtime.
- Put DB credentials in client-visible modules under `src/lib` imported by client components.

## Output template

1. Route files (`+page.server.ts`, `+page.svelte`, actions)
2. `hooks.server.ts` locals typing in `app.d.ts`
3. Env vars table (public vs private)
4. Tests + `bun run check` / `bun run test` / `bun run build`
5. Deploy notes (PORT, HOST, proxy paths)

## Runtime & package manager

Use **Bun** (≥ 1.3) for install, scripts, and production SSR:

| Action | Command |
| ------ | ------- |
| Install | `bun install` |
| Dev | `bun run dev` |
| Build | `bun run build` |
| Start | `bun run start` |

Do not default to Node/npm/yarn/pnpm in this stack — Bun is the runtime.

## Related skills

- `rc-axum` — Rust API + WebSocket
- `rc-a11y` — accessible UI
- `rc-seo` — meta/SSR SEO beyond Kit defaults
