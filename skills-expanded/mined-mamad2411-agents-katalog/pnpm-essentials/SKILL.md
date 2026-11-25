---
name: pnpm-essentials
description: Use when working with pnpm — workspaces, lockfile, patching deps with `pnpm patch`, monorepo orchestration.
metadata:
  added: 2026-05-18
  last_reviewed: 2026-05-18
  type: runtime
  status: active
  invokes_shell: false
  shell_reviewed: "valksor 2026-05-17"
  related: [bun-essentials, node-essentials, typescript]
---

# pnpm Essentials

**Iron Law: pnpm for monorepos. `workspace:*` protocol for internal deps. Commit `pnpm-lock.yaml`. Patches via `pnpm patch`.**

**Versions:** Supported `9` · Current `11` · Next `12` — _Lockfile v9 (compact); `catalog:` protocol for shared dep versions in workspaces; `pnpm dlx` replaces `npx`; `onlyBuiltDependencies` whitelist for postinstall scripts._

## Why pnpm over npm / yarn / bun

|                                     | pnpm              | npm    | yarn classic            | bun         |
| ----------------------------------- | ----------------- | ------ | ----------------------- | ----------- |
| Disk usage (3 projects, same deps)  | 1× (shared store) | 3×     | 3×                      | 1× (shared) |
| Install speed                       | fast              | slow   | medium                  | fastest     |
| Workspaces support                  | first-class       | basic  | first-class             | first-class |
| Lockfile portability                | strict            | strict | strict                  | strict      |
| Strict dep resolution (no phantoms) | yes (default)     | no     | with PnP                | partial     |
| Active maintenance                  | yes               | yes    | classic: no, berry: yes | yes         |

**Disk-efficient global store + symlinks** is pnpm's superpower. Disk usage stays bounded even with 50 packages in a monorepo. The strict resolution model also catches "phantom dependency" bugs (importing a package you didn't declare).

## Workspaces

```yaml
# pnpm-workspace.yaml (at repo root)
packages:
  - "apps/*"
  - "packages/*"
  - "tools/*"
  - "!**/test-fixtures/**" # exclude
```

```json
// packages/ui/package.json
{
  "name": "@org/ui",
  "version": "1.0.0",
  "main": "./src/index.ts"
}

// apps/web/package.json
{
  "dependencies": {
    "@org/ui": "workspace:*",      // always the in-repo version
    "react": "^19.0.0"
  }
}
```

`workspace:*` (or `workspace:^`, `workspace:~`) is mandatory for internal deps. On publish, pnpm rewrites it to the actual published version. **Without it**, you might pull a stale npm-registry version even when an updated local one exists.

### Filtering — run scripts per workspace

```bash
pnpm -r run build                      # all workspaces
pnpm -F @org/web run dev               # only the web app
pnpm -F "./apps/**" run test           # glob pattern
pnpm -F @org/ui... build               # @org/ui AND its dependents
pnpm -F ...@org/ui build               # @org/ui AND its dependencies
pnpm -F "[origin/main]" run lint       # only workspaces changed since main
```

`...` is dependency-direction syntax: trailing dots = "and dependents", leading dots = "and dependencies". `[git-ref]` filters to changed packages — the killer feature for monorepo CI (only build what changed).

## Lockfile — `pnpm-lock.yaml`

- **Commit it.** Always. Required for reproducible installs.
- One lockfile per repo (even with workspaces) — at the root.
- Format is YAML; reads as a diff better than `package-lock.json`.
- `pnpm install --frozen-lockfile` in CI (CI sets this by default when CI=true) — fails if lockfile would change.
- Conflict in lockfile after a merge? Run `pnpm install` — pnpm regenerates it deterministically. Don't hand-merge.

### Lockfile vs `package.json` drift

| State                          | Meaning                                                                | Action                                                                                      |
| ------------------------------ | ---------------------------------------------------------------------- | ------------------------------------------------------------------------------------------- |
| `package.json` newer than lock | someone added a dep, forgot `pnpm install`                             | run `pnpm install`                                                                          |
| Lock newer than `package.json` | someone hand-edited `package.json` to remove dep without `pnpm remove` | run `pnpm install` (regenerates the lock); use `--lockfile-only` to skip node_modules write |
| CI fails `frozen-lockfile`     | local lockfile not committed                                           | commit `pnpm-lock.yaml`                                                                     |

## Patching dependencies — `pnpm patch`

When upstream has a bug, fork or wait — or patch it locally:

```bash
pnpm patch react@19.0.0
# pnpm copies react@19.0.0 to a temp dir and prints the path
# Edit files in that temp dir to apply your fix

pnpm patch-commit <PATH-FROM-PREVIOUS-COMMAND>   # macOS: /private/var/folders/...; Linux: /tmp/pnpm-patch-...
# pnpm writes patches/react@19.0.0.patch and updates package.json:
#   "pnpm": { "patchedDependencies": { "react@19.0.0": "patches/react@19.0.0.patch" } }
```

Commit `patches/` to the repo. On every `pnpm install`, patches re-apply automatically.

**Better than `patch-package`** (the old npm tool) because:

- Native pnpm command — no separate npm dep
- Auto-applies via the lockfile metadata, not a postinstall script
- Survives node_modules rebuild without re-running `patch-package`

**Rules:**

- Tie the patch to an **exact version** (`react@19.0.0`, not `react@^19`) — version bump = re-create the patch
- Keep patches small and well-commented — they're tech debt you must remove on upgrade
- Track them: `pnpm.patchedDependencies` in `package.json` is the source of truth

## Hoisting & strict resolution

pnpm creates a **non-flat** `node_modules`:

```
node_modules/
├── .pnpm/                        # actual packages in a content-addressable layout
│   ├── react@19.0.0/node_modules/react/
│   └── react-dom@19.0.0/node_modules/react-dom/...
└── react -> .pnpm/react@19.0.0/node_modules/react
```

This means **you can only `require`/`import` packages you've declared** in `package.json`. No phantom deps. This catches bugs that npm/yarn classic hide.

For packages misbehaving with strict resolution (Webpack plugins, some legacy tools), tune `.npmrc`: `public-hoist-pattern[]=*eslint*`, `public-hoist-pattern[]=*prettier*`. `shamefully-hoist=true` is the nuclear option (disables strict mode) — last resort, document why.

## Monorepo orchestration

### pnpm alone vs turbo / nx

| Tool                | Adds                                        | When                                          |
| ------------------- | ------------------------------------------- | --------------------------------------------- |
| `pnpm -r run build` | nothing — runs in dep order                 | small monorepos (<10 packages)                |
| **turbo**           | task cache (local + remote), parallel exec  | medium-large; tasks with clear inputs/outputs |
| **nx**              | task cache + generators + project graph viz | large monorepos with many app types           |

Start with `pnpm -r`. Add turbo when:

- Builds take >30s
- CI rebuilds the same thing across PRs
- You want remote caching (turbo + Vercel/turbo-remote-cache)

```json
// turbo.json
{
  "tasks": {
    "build": { "dependsOn": ["^build"], "outputs": ["dist/**"] },
    "test": { "dependsOn": ["build"], "outputs": [] },
    "lint": {}
  }
}
```

`^build` = dependencies built first; `outputs` = paths cached for replay.

### CI pattern for monorepos

```bash
# Install once at root
pnpm install --frozen-lockfile

# Only test/build packages affected by the PR
pnpm -F "...[origin/main]" run test
pnpm -F "...[origin/main]" run build
```

The `[origin/main]` filter + `...` ancestor-chasing = test only changed packages and their dependents.

## Anti-patterns

- Missing `workspace:*` on internal deps → pulls stale registry version; `shamefully-hoist=true` "to make it work" without documenting why
- `package-lock.json` AND `pnpm-lock.yaml` both committed; mixing `npm install` + `pnpm install` in same repo
- `pnpm install --no-frozen-lockfile` in CI to "fix" the build → silently drifts deps
- Manual `node_modules` surgery instead of `pnpm patch`; re-creating patches by hand; patching `^`-range versions
- Reaching for turbo/nx in a 3-package repo
- **Trusting `postinstall` lifecycle scripts from every transitive dep** — a compromised package runs arbitrary code as your user at install time. Two-part fix: run `pnpm install --ignore-scripts` everywhere (commit to a `.npmrc` line: `ignore-scripts=true`), THEN explicitly allowlist packages that legitimately need build steps in `package.json`: `"pnpm": { "onlyBuiltDependencies": ["esbuild", "sharp", ...] }`. Audit which packages need it: `pnpm install --ignore-scripts && pnpm rebuild` once; rebuild errors out for every package that needs a build step — add each named package to the allowlist after reading its install script (`cat node_modules/<pkg>/package.json | jq .scripts.install`)

## Red flags

| Thought                            | Reality                                                                  |
| ---------------------------------- | ------------------------------------------------------------------------ |
| "We don't need workspaces yet"     | One shared util later, you're copy-pasting files. Start with workspaces. |
| "Phantom deps are fine, they work" | Until the hoisting changes and they stop. pnpm catches them on day 1.    |
| "Let CI regenerate the lockfile"   | Then it's not a lockfile. Commit it.                                     |
| "We'll un-patch when we upgrade"   | Add it to your upgrade checklist or it lingers for years.                |

## Hand-off

Bun as unified pkg+runtime (often replaces pnpm + node + jest): `Skill(bun-essentials)`. Node runtime: `Skill(node-essentials)`. TS config in monorepos: `Skill(typescript)`.
