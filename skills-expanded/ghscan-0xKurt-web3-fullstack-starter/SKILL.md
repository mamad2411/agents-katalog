---
name: turborepo-pnpm
description: Monorepo build system. pnpm workspace commands, Turborepo task pipeline,
  caching, filtering, adding packages.
docs:
  - https://turbo.build/repo/docs
  - https://pnpm.io/workspaces
  - https://pnpm.io/filtering
---

# Turborepo + pnpm — Best Practices

## Reference docs
- Turborepo: https://turbo.build/repo/docs
- turbo.json config: https://turbo.build/repo/docs/reference/configuration
- pnpm workspaces: https://pnpm.io/workspaces
- pnpm filtering: https://pnpm.io/filtering

## pnpm commands

```bash
pnpm --filter contracts build                  # run in one package
pnpm --filter '@web3-fullstack-starter/shared' build         # quote names with @ or /
pnpm -r build                                  # run in all packages
pnpm --filter backend add viem                 # add dep to one package
pnpm --filter backend add @web3-fullstack-starter/shared     # adds workspace:* automatically
pnpm install                                   # always use pnpm, never npm/yarn
```

## Turborepo task graph (turbo.json)

```json
"build": { "dependsOn": ["^build"] }   // ^ = run deps first (shared before frontend)
"dev":   { "cache": false, "persistent": true }
"test":  { "dependsOn": ["^build"] }
```

## Caching

- Turborepo hashes inputs and caches outputs defined in `outputs`.
- `cache: false` for dev servers and side-effectful scripts.
- Add env vars that affect build output to the task's `env: []` array.
- Clear cache: `turbo clean` or delete `.turbo/`

## Adding a new package

1. Create `packages/mypackage/` with `package.json` (`"name": "@web3-fullstack-starter/mypackage"`)
2. `packages/*` glob in `pnpm-workspace.yaml` already covers it
3. `pnpm install` from root to link it
4. Add to `turbo.json` if custom task config needed

## Common mistakes

- Using npm/yarn instead of pnpm — breaks workspace symlinks
- Forgetting quotes around `@web3-fullstack-starter/` filter names on some shells
- Expecting dev tasks to run in dependency order — they're parallel. Build deps first.
- Not adding build-affecting env vars to turbo.json `env` — cache returns stale output
