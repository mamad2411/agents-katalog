---
name: follow-lib-nitro-deploy-preset
description: Deploy Nitro with a preset — bun/node/cloudflare/deno/vercel/netlify + provider config, bindings, rollback
argument-hint: "[provider]"
related:
  - follow-lib-nitro
  - follow-service-cloudflare
  - run-build
  - resolve-errors
  - report
---

## Goal

Deploy the Nitro `.output` to a provider per preset — pick the preset, provider config, secrets/bindings, verify live

## Scope

the Nitro app's deploy path — run after `setup-nitro`; Cloudflare-specific deploy depth → `/follow-service-cloudflare` (`deploy-worker` workflow)

## Execute

### 1. Pick Preset

> Goal: preset matches the deploy target

| Preset | Output | Run/Deploy |
|---|---|---|
| `bun` | `.output/server/index.mjs` | `bun .output/server/index.mjs` |
| `node-server` | `.output/server/index.mjs` | `node .output/server/index.mjs` |
| `cloudflare-module` | Worker module | `wrangler deploy` |
| `deno-server` | `.output/server/index.ts` | `deno run` |
| `vercel` / `netlify` | provider bundle | provider CLI/git push |

- Set via the `NITRO_PRESET` env or `nitro.config.ts` `preset` — pick one method, never conflict
- Full list: https://nitro.build/deploy — presets are added often, check the latest first

### 2. Provider Config

> Goal: complete provider-specific wiring

1. **Cloudflare**: preset `cloudflare-module` + `wrangler.jsonc` (bindings/secrets) → `/follow-service-cloudflare` for d1/kv/r2 + deploy
2. **Vercel/Netlify**: the preset generates the provider layout — check `vercel.json`/`netlify.toml` requirements
3. **Self-host (bun/node)**: process manager (pm2/systemd/docker) + `PORT`/`HOST` env
4. Statics: `.output/public/` is served automatically on every preset — or a separate CDN

### 3. Secrets And Bindings

1. Secrets → env/`wrangler secret put`/provider dashboard — never in the config repo
2. Bindings (KV/D1/R2) → `wrangler.jsonc` + `wrangler types` → `worker-configuration.d.ts`
3. `runtimeConfig` overrides → `NITRO_*` env vars on the provider

### 4. Build, Deploy, Verify

1. `NITRO_PRESET=<target> bun run build` → inspect `.output/`
2. Deploy per the provider path → smoke test health/critical routes
3. Rollback path: keep the previous `.output` or the provider version
4. fail → `/resolve-errors` max 3 rounds → report URL + version

## Rules

- Preset is build-time — switching provider = rebuild with the new preset (not a runtime switch)
- Check preset maturity — test beta presets before production
- `.output/` is portable within the same preset — not across presets
- Secrets/env follow the provider mechanism — some presets have no `.env` loading

## Expected Outcome

- Build per the preset is correct + deploy succeeds on the target
- Bindings/secrets are accessible in handlers; rollback path ready
