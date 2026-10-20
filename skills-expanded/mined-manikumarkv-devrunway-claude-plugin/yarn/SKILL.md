---
name: yarn
description: Yarn Berry (v4) conventions — .yarnrc.yml, workspaces, PnP vs node-modules linker, yarn dlx, and zero-install strategy. Load when working with yarn.lock or .yarnrc.yml.
user-invocable: false
stack: package-manager/yarn
paths:
  - "yarn.lock"
  - ".yarnrc.yml"
  - ".yarn/**"
---

Full standards in [yarn.md](yarn.md). Always-on summary:

**Version:** Always use Yarn Berry (v4) for new projects — `yarn set version stable`.

**Linker strategy (pick one, document in `.yarnrc.yml`):**
- `node-modules` — drop-in compatibility; familiar, but loses Yarn's deduplication benefits
- `pnp` (Plug'n'Play) — fastest, strictest; requires editor integration; default in Berry

**Workspaces:**
- Declared in root `package.json` under `"workspaces"`
- Cross-package deps use `"workspace:^"` — pinned to local, replaced with version on publish
- Run scripts across workspaces: `yarn workspaces foreach -A run build`

**Key commands:**
- `yarn` — install all dependencies
- `yarn add <pkg>` — add to current package
- `yarn add <pkg> --dev` — add as devDep
- `yarn dlx <pkg>` — one-off execution (like npx)
- `yarn workspace <name> add <pkg>` — add to a specific workspace
- `yarn install --immutable` — CI install (errors on lockfile mismatch)

**Never:**
- Mix npm or pnpm commands in a Yarn project
- Commit `.yarn/cache/` without a zero-install decision (see yarn.md)
- Edit `yarn.lock` manually

**Related skills:** CI layer (`--immutable` in pipeline)
