---
name: sveltekit-adapters
description: Use when selecting, configuring, or troubleshooting SvelteKit adapters for deployment to Node.js, static hosts, Vercel, Cloudflare, and other targets.
---

# SvelteKit Adapters

## Specialization

Expert guidance for SvelteKit adapter selection, configuration, and deployment. Covers `adapter-auto`, `adapter-node`, `adapter-static`, `adapter-vercel`, `adapter-cloudflare`, platform-specific `platform.env` access, and the constraints each adapter places on rendering modes and runtime APIs.

## Trigger Conditions

- Deploying a SvelteKit application to a specific hosting platform.
- Choosing the correct adapter for the target environment.
- Diagnosing runtime errors caused by adapter-incompatible APIs.
- Configuring environment variables and platform bindings for edge or serverless runtimes.
- Building a fully static site with `adapter-static`.

## Scope Boundaries

In scope:

- `@sveltejs/adapter-auto`: zero-config detection for supported platforms.
- `@sveltejs/adapter-node`: self-hosted Node.js server output.
- `@sveltejs/adapter-static`: fully static HTML export.
- `@sveltejs/adapter-vercel`: Vercel Functions and Edge Functions.
- `@sveltejs/adapter-cloudflare`: Cloudflare Workers and Pages.
- `svelte.config.js` adapter configuration.
- `platform.env` and `platform.context` for platform-specific bindings.
- `BODY_SIZE_LIMIT`, `ORIGIN`, and `ADDRESS_HEADER` node adapter options.
- Adapter compatibility matrix: which adapters support SSR, edge, and static.

Out of scope:

- Page rendering mode decisions (covered by `sveltekit-page-options`).
- CI/CD pipeline setup (covered by `ci-cd-workflows`).
- Load function implementation (covered by `sveltekit-load`).
- Container packaging for Node adapter output (separate concern).

## Inputs

- Target deployment platform.
- Rendering mode requirements (SSR, static, edge).
- Platform-specific bindings needed (KV, D1, R2, Vercel Blob, etc.).
- Environment variable strategy.
- Evaluation date in ISO format (`YYYY-MM-DD`).

## Required Outputs

| Output | Description |
|---|---|
| Adapter selection decision | Chosen adapter with documented rationale |
| `svelte.config.js` configuration | Correct adapter import and options |
| Platform binding access | `platform.env` typed access for applicable adapters |
| Environment variable plan | `$env/static/private`, `$env/dynamic/private`, or platform env usage |
| Adapters quality checklist | Pass/fail against the checklist below |

## Depth Modes

| Level | Intent | Exit Rule |
|---|---|---|
| L1 Orientation | Build output reaches the target platform | App deploys and responds to requests |
| L2 Practical Delivery | Correct adapter with platform bindings and env vars | SSR or static output verified; env vars accessible; platform bindings working |
| L3 Specialist Hardening | Optimise for cold start, edge latency, and bundle size | Bundle analysed; cold start measured; incompatible Node APIs removed |
| L4 Expert Standardisation | Adapter and deployment policy for a project | Adapter selection guide, platform env registry, and incompatibility matrix documented |

## Adapter Selection Guide

| Target Platform | Recommended Adapter | Notes |
|---|---|---|
| Vercel | `adapter-vercel` | Auto-detects Edge vs. Serverless per route |
| Cloudflare Pages / Workers | `adapter-cloudflare` | Use `platform.env` for KV, D1, R2 |
| Node.js server (self-hosted) | `adapter-node` | Produces `build/` with `index.js` entry |
| Netlify | `adapter-netlify` (community) | Not in `@sveltejs` org; verify currency |
| Fully static site | `adapter-static` | Requires all routes to be prerenderable |
| Unknown / multi-platform | `adapter-auto` | Detects at build time; not for production use in CI |

## Workflow

1. Identify the target deployment platform and runtime (Node.js, edge, static CDN).
2. Select the adapter using the guide above; reject `adapter-auto` for production CI builds.
3. Install the adapter package and update `svelte.config.js` with adapter import and options.
4. Audit page options: `adapter-static` requires all routes to have `prerender = true`; SSR routes require a server-capable adapter.
5. Configure environment variable access: use `$env/static/private` for build-time secrets, `$env/dynamic/private` for runtime secrets.
6. For edge adapters, audit load functions and actions for incompatible Node.js APIs (`fs`, `crypto`, `net`); replace with Web API equivalents.
7. Access platform-specific bindings through `event.platform.env` in load functions and actions; type via `App.Platform` augmentation.
8. Test the production build locally (`vite build` + adapter output) before deploying.
9. Run the adapters quality checklist.

## Adapters Quality Checklist

- [ ] Adapter matches the target deployment runtime; `adapter-auto` is not used in CI.
- [ ] `svelte.config.js` references the correct adapter with explicit options, not defaults.
- [ ] All routes rendered at runtime use a server-capable adapter; static-only routes use `prerender = true`.
- [ ] Secrets are accessed via `$env/static/private` or `$env/dynamic/private`; they are never exposed to the client.
- [ ] Edge adapter routes contain no Node.js-only APIs.
- [ ] `platform.env` is accessed through `App.Platform` typed interface augmentation.
- [ ] Production build output is tested locally before first deployment.

## Security Notes

- Never access `$env/static/public` or `$env/dynamic/public` for secrets; these are exposed to the browser.
- `$env/static/private` values are inlined at build time; do not use for secrets that rotate.
- For rotating secrets use `$env/dynamic/private` or platform secret manager bindings.

## L4 Coverage Matrix

| Requested Outcome | Skill Section |
|---|---|
| Adapter selection | Adapter Selection Guide |
| Configuration | Workflow steps 3–4 |
| Environment variables | Workflow step 5 + Security Notes |
| Edge API compatibility | Workflow step 6 |
| Platform bindings | Workflow step 7 |
| Quality validation | Adapters Quality Checklist |

## References

See [references/source-catalog.md](./references/source-catalog.md) for active source tracking.
