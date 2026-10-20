---
name: athena-auth-cloudflare-worker
description: Inspect, explain, or replicate the `athena-auth` Cloudflare Worker deployment pattern. Use when Codex needs to take a project from no Wrangler setup to a Worker that fronts an app running inside a Cloudflare Container, wire `wrangler.jsonc`, `worker/src/index.ts`, Durable Object container bindings, `.dev.vars` and Wrangler secrets, generated Worker env types, and validate the deploy flow with current Cloudflare docs plus `wrangler deploy --dry-run`.
---

# Athena Auth Cloudflare Worker

**Not** the Athena JS D1/R2 edge client adapter. For `createClient({ db: { d1 }, storage: { r2 } })`, hybrid billing, or `packages/athena-js/src/cloudflare/**`, use `$athena-js-cloudflare-edge-adapter`.

Use this skill when the target shape is the same one used in `athena-auth`:

1. A Cloudflare Worker is the public entrypoint.
2. The Worker starts or proxies to a Cloudflare Container.
3. The container runs the real app server.
4. Wrangler owns routing, vars, secrets, observability, container bindings, and deployment.

Read [references/athena-auth-layout.md](references/athena-auth-layout.md) first to understand the exact repo pattern.
Read [references/replication-checklist.md](references/replication-checklist.md) when you need to build or migrate another project to the same shape.

## Workflow

1. Verify current Cloudflare guidance before writing commands or config.
2. Read the target repo's existing runtime entrypoint, Dockerfile, package manager, and deployment files.
3. Compare that repo against the `athena-auth` reference layout.
4. Add the missing Cloudflare pieces in this order:
   `Dockerfile` -> `wrangler.jsonc` -> `worker/src/index.ts` -> `.dev.vars.example` -> generated Worker types -> package scripts / tsconfig wiring.
5. Split config correctly:
   non-secret defaults in `wrangler.jsonc`,
   secrets via `wrangler secret put`,
   local secret mirrors in `.dev.vars`,
   generated type surface in `worker-configuration.d.ts`.
6. Validate the deploy path before stopping:
   `wrangler --version`,
   `wrangler whoami`,
   `wrangler check`,
   `wrangler types worker/worker-configuration.d.ts --include-runtime false`,
   `wrangler deploy --dry-run`.

## Non-negotiable rules

- Use current Cloudflare docs, not memory, for Wrangler flags and config fields.
- Prefer `wrangler.jsonc` over TOML unless the repo already standardizes on TOML.
- Keep secrets out of `wrangler.jsonc` and source files.
- Regenerate Worker types immediately after any binding or `vars` change.
- Keep the container port, Worker proxy port, and app server port aligned.
- Fail early in the Worker when required secrets like `DATABASE_URL` or `JWT_SECRET` are missing.
- Preserve the repo's real package manager and task runner instead of forcing a new one.

## Decision points

### When the target app is already Dockerized

- Reuse the existing image build if it already starts the real server cleanly.
- Only add the minimal Cloudflare Worker and Wrangler layer around it.

### When the target app is not Dockerized yet

- Create the Dockerfile first.
- Expose one stable internal app port.
- Make the Worker container bridge target that port only.

### When the target app already has a Worker

- Inspect whether it is plain fetch logic or the container pattern.
- If migrating to the `athena-auth` shape, update bindings, secrets, and generated types together in one pass.

## Validation target

Do not stop after a static edit. End with a validated deploy-shaped result or a precise blocker such as missing Cloudflare auth, unavailable account resources, or an app server that still cannot boot inside the container image.
