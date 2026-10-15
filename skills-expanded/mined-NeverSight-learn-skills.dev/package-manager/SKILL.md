---
name: package-manager
description: Wouters Media projects prefer pnpm as the package manager. Use pnpm commands in instructions, scripts, and documentation. npm and yarn remain valid alternatives when a project does not use pnpm.
---

# Package Manager

## Preference

**Use `pnpm` as the default package manager** in Wouters Media projects. It is faster than npm, uses less disk space via content-addressable storage, and enforces strict dependency isolation in monorepos.

```bash
# ✅ PREFERRED
pnpm install
pnpm add <package>
pnpm run build
pnpm --filter <workspace> dev

# ✅ ALSO VALID — when the project uses npm
npm install
npm run build
```

## Detecting Which Manager to Use

Check the project root for a lockfile:

| File present       | Use        |
| ------------------ | ---------- |
| `pnpm-lock.yaml`   | `pnpm`     |
| `package-lock.json`| `npm`      |
| `yarn.lock`        | `yarn`     |
| `bun.lockb`        | `bun`      |

When in doubt, check `package.json` for an `engines.pnpm` or `packageManager` field.

## Monorepo Workspaces

In monorepos using `pnpm-workspace.yaml`, always use the `--filter` flag to target a specific package:

```bash
# Run dev server for a specific app
pnpm --filter docs dev
pnpm --filter web build

# Add a dependency to a specific workspace
pnpm --filter web add react-query

# Run a command in all workspaces
pnpm -r build
```

## Installing Dependencies

```bash
# Install all dependencies (respects lockfile)
pnpm install

# Add a runtime dependency
pnpm add zod

# Add a dev dependency
pnpm add -D typescript

# Add a dependency to a specific workspace
pnpm --filter web add react-query
```

## Do Not

- Do **not** commit `node_modules/`.
- Do **not** mix package managers in the same project (e.g. running `npm install` in a pnpm project generates a second lockfile).
- Do **not** delete and recreate the lockfile without a documented reason — it contains resolved versions that ensure reproducible installs.
