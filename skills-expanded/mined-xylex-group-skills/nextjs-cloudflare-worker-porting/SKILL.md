---
name: nextjs-cloudflare-worker-porting
description: Port existing Next.js projects to Cloudflare Workers using the current OpenNext and Wrangler workflow. Use when Codex needs to make a Next.js app Worker-compatible, migrate it off another host, add or repair Cloudflare adapter files, audit runtime incompatibilities, fix preview or deploy failures, or validate that local dev, preview, environment variables, middleware, caching, and deployment behavior still match production expectations on Workers.
---

# Next.js Cloudflare Worker Porting

Port the real app instead of describing a generic migration. Inspect the existing Next.js project, identify the smallest set of runtime-sensitive changes needed for Cloudflare Workers, implement them, and validate with the most production-like local gate available.

## Quick Start

1. Inspect the current app before editing:
   - Check `package.json`, lockfile, `next.config.*`, `middleware.*`, `app/` vs `pages/`, existing `wrangler.*`, and any host-specific config.
   - Find Node-only assumptions such as filesystem writes, child processes, native binaries, custom servers, or middleware that depends on unsupported Node APIs.
2. Read [references/workflow.md](references/workflow.md) for the concrete migration sequence, including install and approval steps.
3. Read [references/runtime-notes.md](references/runtime-notes.md) when the app uses middleware, server env vars, image optimization, ISR, caching, or CI/build secrets.
4. Use current docs before making adapter-level claims:
   - Use Context7 for Next.js runtime and env behavior.
   - Use Cloudflare docs for Wrangler and Workers-specific behavior.
5. Make the smallest coherent patch set, then validate with `preview` before trusting `dev`.

## Migration Workflow

### 1. Choose the configuration path

- Prefer automatic Wrangler detection when the project has no meaningful existing Wrangler configuration and the user wants the lightest migration path.
- Prefer explicit manual configuration when the repo already has Worker bindings, multiple environments, CI deployment scripts, or existing Cloudflare infrastructure that should stay declarative in-repo.

### 2. Normalize the Cloudflare contract

Add or repair the files and scripts Cloudflare expects:

- `@opennextjs/cloudflare` dependency
- dependency approval step when the package manager requires it
- `wrangler` devDependency
- `open-next.config.ts`
- `wrangler.jsonc` or `wrangler.toml`
- `preview`, `deploy`, and usually `cf-typegen` scripts in `package.json`

Do not invent alternate output paths unless the repo already has a deliberate custom setup. The default Worker entrypoint is `.open-next/worker.js`, the default assets directory is `.open-next/assets`, and the Wrangler `name` should match the app or package name instead of a placeholder.

### 3. Audit runtime-sensitive app code

Focus on behavior that commonly breaks after a host change:

- Middleware assumptions
- Build-time versus runtime environment variable access
- Route handlers and server actions that rely on unsupported Node features
- Image optimization setup
- Cache and ISR expectations
- Background or deferred work expectations

When you find a risky seam, fix the actual code path instead of only documenting the limitation.

### 4. Keep env and generated artifacts aligned

- If new environment variables are required, update `.env`, `.env.local`, and `.env.example` with comments and dummy values.
- If Wrangler bindings change, regenerate any Worker env type artifacts the repo relies on.
- Keep local `.env*` usage aligned with Next.js development, and keep production runtime vars in the Cloudflare dashboard.
- Remove stale host-specific configuration only when the Cloudflare replacement is clearly in place.

### 5. Validate like production

- Use the project's package manager consistently.
- Prefer the Worker-runtime preview gate over `next dev` for migration confidence.
- If the repo has tests that exercise routes, auth, ISR, or middleware, run the narrowest relevant subset after the port.
- If deployment scripts exist, verify them instead of only proving ad hoc local commands.

## Execution Rules

- Preserve the existing app shape unless Cloudflare compatibility forces a change.
- Prefer additive fixes over rewrites.
- Keep config explicit when the repo already values checked-in deployment configuration.
- Treat preview failures as higher signal than dev-server success.
- Do not claim a feature is unsupported without checking current docs first.
- When the app still cannot run on Workers because of a hard runtime dependency, state the exact blocker and where it lives.
