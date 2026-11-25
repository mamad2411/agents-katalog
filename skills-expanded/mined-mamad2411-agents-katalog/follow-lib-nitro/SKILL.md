---
name: follow-lib-nitro
description: Use Nitro as a server engine — vite plugin, presets (bun/node/cloudflare/deno), portable .output, deploy providers
argument-hint: "[scope]"
related:
  - follow-tool-vite
  - follow-solid-framework
  - follow-service-cloudflare
  - deep-research
  - run-dev
---

## Goal

Use Nitro (https://nitro.build) as the production server layer of a web app — build into a portable `.output/` that runs on any runtime (Bun, Node, Cloudflare Workers, Deno, edge providers)

## Scope

When a project needs:

- A portable production server — `bun .output/server/index.mjs` / `node .output/server/index.mjs`
- Deploying to a provider via a preset — https://nitro.build/deploy
- A server engine for a meta-framework (TanStack Start, Analog, Nuxt already use Nitro)

## Execute

### 1. Install

> Goal: add nitro to the Vite pipeline

```bash
bun i -D nitro
```

### 2. Configure Vite Plugin

> Goal: put `nitro()` in the correct plugins order

```ts
import { nitro } from 'nitro/vite'

export default defineConfig({
  plugins: [frameworkPlugin(), nitro(), UnoCSS(), frameworkCompiler()],
})
```

- Nitro v3 `nitro()` **does not accept a `preset` option** — set the preset via the `NITRO_PRESET` env var or `nitro.config.ts`:
  ```ts
  process.env.NITRO_PRESET ??= 'bun'   // in vite.config.ts before defineConfig
  ```
- Pick one method (env or config file) — never set conflicting values

### 3. Pick Preset

> Goal: choose the preset by deploy target

| Preset | Output | Run/Deploy |
|---|---|---|
| `bun` | `.output/server/index.mjs` | `bun .output/server/index.mjs` |
| `node-server` | `.output/server/index.mjs` | `node .output/server/index.mjs` |
| `cloudflare-module` | Worker module | `wrangler deploy` — https://nitro.build/deploy/providers/cloudflare |
| `deno-server` | `.output/server/index.ts` | `deno run` |
| `vercel` / `netlify` / etc. | provider bundle | provider CLI |

- Statics in `.output/public/` are served automatically
- Full preset list: https://nitro.build/deploy — do `/deep-research` to confirm the latest preset names before use

### 4. Cloudflare Bindings (if preset cloudflare-*)

> Goal: env bindings accessible in handlers

1. Declare `d1_databases`/`kv_namespaces`/`r2_buckets` in `wrangler.jsonc`
2. Code reads them via `env.*` — generate types with `wrangler types` → `worker-configuration.d.ts`
3. Follow `/follow-service-cloudflare` for deploy/secrets/rollback

### 5. Custom Server Entry (optional)

> Goal: wrap the fetch handler when middleware/custom logic is needed

```ts
export default {
  fetch(request: Request, env: unknown, ctx: unknown) {
    // pre-processing → delegate to framework handler
  },
}
```

### Workflows

| Topic | Workflow |
|-------|----------|
| Install + vite plugin + dev/build + `.output` | `workflows/setup-nitro/SKILL.md` |
| Routes/handlers/api/websockets/tasks | `workflows/define-routes/SKILL.md` |
| Storage/cache/routeRules/prerender | `workflows/config-storage/SKILL.md` |
| Middleware/plugins/hooks/runtimeConfig | `workflows/config-middleware/SKILL.md` |
| Deploy per preset/provider | `workflows/deploy-preset/SKILL.md` |

## Rules

- `nitro()` v3 does not accept `preset` in options — use the `NITRO_PRESET` env var or `nitro.config.ts`
- `.output/` is a generated artifact — never commit it
- Secrets always via env/`wrangler secret` — never hardcode in config
- Check https://nitro.build or `/deep-research` for the latest preset names and provider docs
- See best-practices/ for recommended patterns and pitfalls

## Expected Outcome

- `bun run build` → `.output/` ready to run per the chosen preset
- The server works on the target runtime without code changes
