---
name: follow-lang-bun-migrate-from-nodejs
description: Move a Node.js project to Bun safely and reversibly
related:
  - follow-lang-bun
  - follow-lang-nodejs
  - resolve-errors
  - deep-research
  - improve
---

## Goal

Migrate a Node.js project to Bun without breaking the build, tests, or runtime behavior

## Scope

For an existing Node.js project (npm/pnpm/yarn) moving onto Bun — full migration or gradual adoption; read `/follow-lang-bun` for the target-state rules

## Execute

### 1. Prerequisites

1. `bun --version` shows a current supported release (see the Install And Setup step of [../../SKILL.md](../../SKILL.md))
2. Clean `git status` — commit before migrating

### 2. Replace The Package Manager

1. Run `bun pm migrate` first — it converts the existing lockfile into `bun.lock` preserving resolved versions
2. Then remove `node_modules` + the old lockfile (`package-lock.json`/`yarn.lock`/`pnpm-lock.yaml`) and run `bun install`
3. Declare `trustedDependencies` for packages relying on `postinstall` (esbuild, sharp, prisma, puppeteer) — `bun pm untrusted` lists blocked ones

### 3. Update Scripts

| old | new |
|-----|-----|
| `npm run dev` | `bun run dev` or `bun dev` |
| `npm install` | `bun install` |
| `npx <tool>` | `bunx <tool>` |
| `node index.js` | `bun index.js` |
| `node --watch` | `bun --watch` |
| `jest` / `vitest` (basic) | `bun test` |
| `ts-node`, `tsx` | remove — Bun runs TS directly |
| `dotenv` | remove — `.env` auto-loads |

1. Scripts with a `#!/usr/bin/env node` shebang → `bun run --bun <script>` to force Bun
2. `cross-env` can go when it only sets env vars (`KEY=v bun run x` works in the Bun shell)

### 4. Compatibility Checklist

1. `node:*` imports and Node globals (`process`, `Buffer`, `__dirname`, `require`) mostly work; migrating to ESM is still recommended
2. Native addons (`.node`, node-gyp) — Node-API is supported; packages relying on V8 internals may break
3. `import.meta.url` patterns work; `import.meta.dirname`/`filename` are provided
4. TypeScript — drop `module: "commonjs"`; use `bundler` resolution + `bun-types`
5. Test framework — most jest/vitest APIs map onto `bun:test` (`jest.mock` → `mock.module`)
6. Edge cases → check the official Node.js-compat doc via `/deep-research`

### 5. Gradual Adoption (optional)

1. `bun install` alone as just the package manager works — the runtime can stay `node`
2. `bun test` can be adopted separately; keep a `"start:node": "node dist/index.js"` fallback script

### 6. Verify

1. `bun run dev`, `bun test`, `bun run build`, `bunx tsc --noEmit` all pass
2. On failure → run `/resolve-errors`

### 7. Rollback

1. `bun.lock` doesn't conflict with npm — `npm install` regenerates the old lockfile from the committed `package.json`
2. The original lockfile stays in git history — revert anytime

## Rules

- Dependency health after migration → run `/improve deps` if versions drifted

## Expected Outcome

- Project runs, tests, builds, and typechecks on Bun with `bun.lock` committed
- Scripts, TS config, and test mocks migrated; no dead `dotenv`/`ts-node`/`cross-env` leftovers
