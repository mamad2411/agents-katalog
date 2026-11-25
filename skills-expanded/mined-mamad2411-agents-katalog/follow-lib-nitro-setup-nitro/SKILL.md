---
name: follow-lib-nitro-setup-nitro
description: Install Nitro — vite plugin, dev/build, portable .output, preset basics
argument-hint: "[preset]"
related:
  - follow-lib-nitro
  - follow-tool-vite
  - run-dev
  - run-build
  - resolve-errors
---

## Goal

Install Nitro into the Vite pipeline — build to a portable `.output/` that runs on any runtime

## Scope

first-time Nitro setup in a Vite-based app — routes/handlers → `define-routes`; deploy per provider → `deploy-preset`

## Execute

### 1. Install

```bash
bun i -D nitro
```

### 2. Configure Vite Plugin

```ts
import { nitro } from 'nitro/vite'

export default defineConfig({
  plugins: [frameworkPlugin(), nitro(), UnoCSS(), frameworkCompiler()],
})
```

- nitro v3 `nitro()` **does not accept a `preset` option** — set it via the `NITRO_PRESET` env or `nitro.config.ts`
- pick one method (env or config file) — never set conflicting values

```ts
process.env.NITRO_PRESET ??= 'bun'   // in vite.config.ts before defineConfig
```

### 3. Nitro Config (optional)

`nitro.config.ts` for server options (`routeRules`, `storage`, `prerender`, `srcDir`) — details in the docs; app-level wiring via `defineNitroConfig`

### 4. Dev And Build

1. `bun run dev` — nitro dev server via the vite pipeline (HMR + server auto-reload)
2. `bun run build` → `.output/server/index.mjs` + `.output/public/`
3. Run output: `bun .output/server/index.mjs` (preset `bun`) — no dependency on the dev toolchain

### 5. Verify

1. `/run-dev` — API routes respond
2. `/run-build` → `.output/` generated, `bun .output/server/index.mjs` really serves
3. fail → `/resolve-errors` max 3 rounds

## Rules

- `.output/` is generated — never commit, add to `.gitignore`
- `nitro()` v3 does not accept `preset` in options
- use `/follow-lib-nitro` for the overview; latest presets → `deploy-preset` workflow

## Expected Outcome

- `bun run build` → `.output/` ready to run
- Dev server HMR works fully for client+server
