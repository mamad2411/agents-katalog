---
name: setup-monorepo-tooling
description: Sets up and tunes a monorepo — pnpm-workspace layout, an acyclic internal package graph wired with the workspace: protocol, a cached task pipeline (Turborepo/Nx/Bazel) with dependsOn + inputs/outputs and remote cache, affected/changed-only CI runs, shared extended base configs, and Changesets versioning — so CI rebuilds only what changed.
when_to_use: Converting to or fixing a monorepo — CI rebuilds everything, circular package deps, drifting per-package tooling, duplicated shared code. NOT the CI workflow file itself (cicd-pipeline-author), one package's bundler/build config (configure-bundler-build), or the npm publish step (publish-package-registry).
---

## When to Use

Reach for this skill when the problem is **repo-level orchestration and package boundaries**, not one package's build:

- "Our CI rebuilds/tests every package on every PR even when one file changed"
- "Convert this repo into a monorepo" / "split this app into packages"
- "We have a circular dependency between two internal packages"
- "Each package has its own drifting tsconfig/eslint — unify them"
- "Stop copy-pasting this util across three apps — make it a shared package"
- "Turbo/Nx cache never hits" or "the affected graph is wrong"

NOT this skill:
- Writing the GitHub Actions / GitLab CI workflow file itself → cicd-pipeline-author (this skill defines the `turbo run` command it calls, not the YAML)
- One package's bundler/output config (tsup/Vite/esbuild, dual ESM+CJS, externals) → configure-bundler-build
- Actually publishing a package to npm (auth, provenance, `npm publish`) → publish-package-registry (this skill sets up Changesets version PRs; that skill does the registry push)
- Repo-wide lint/format/pre-commit hook *content* → setup-lint-format-precommit
- Pinning the Node/pnpm/toolchain versions themselves → pin-toolchain-versions

## Steps

1. **Pick the orchestrator by scale — default to pnpm workspaces + Turborepo.** Don't reach for Nx or Bazel unless a row below forces it.

   | Tool | Use when | Cost / friction |
   |---|---|---|
   | **pnpm workspaces + Turborepo** | JS/TS monorepo, you want caching + affected runs with near-zero config — **the default** | Tiny `turbo.json`; no codegen, no plugins |
   | Nx | You need code generators/scaffolding, an enforced module-boundary lint rule, or rich project-graph tooling | Heavier config, `nx.json` + project.json or inferred targets, more to learn |
   | Bazel / Buck2 | Polyglot at scale (JS + Go + Java + protos), hermetic builds, thousands of targets | High: BUILD files everywhere, steep ramp — only worth it at large org scale |
   | Lerna (alone) | — | Legacy; for new repos use pnpm + Turbo/Changesets instead |

   Use **pnpm** as the package manager regardless (strict, fast, disk-efficient, first-class `workspace:` protocol). Commit `pnpm-lock.yaml`.

2. **Lay out the workspace and declare it.** `apps/*` = deployables (not published), `packages/*` = shared libs (publishable or internal). Root is private.

   ```yaml
   # pnpm-workspace.yaml
   packages:
     - "apps/*"
     - "packages/*"
   ```
   ```jsonc
   // package.json (root) — root is NOT published
   { "name": "@acme/root", "private": true, "packageManager": "pnpm@9.12.0" }
   ```
   Name every internal package under one scope: `@acme/ui`, `@acme/config`, `@acme/api-client`. The scope makes ownership and the dependency graph legible at a glance.

3. **Wire internal deps with the `workspace:` protocol — never a version range.** In a consumer's `package.json`:
   ```jsonc
   "dependencies": { "@acme/ui": "workspace:*" }
   ```
   `workspace:*` symlinks the local source so changes are picked up instantly; at publish time Changesets/pnpm rewrites it to the real version. Run `pnpm install` from the root once — it links everything. A range like `"^1.0.0"` instead would silently pull the *registry* copy, defeating the monorepo.

4. **Keep the package graph acyclic and explicit.** Cycles break topological build order and caching. Enforce it, don't hope:
   - **Direction:** `apps → packages → packages`. Apps depend on packages; packages never depend on apps. Leaf utils depend on nothing internal.
   - Every cross-package import must correspond to a declared `dependency` in that package's `package.json` — no reaching into a sibling's `../other-pkg/src`. Set `eslint-plugin-import/no-relative-packages` (or Nx's `enforce-module-boundaries`) to ban it.
   - Detect cycles in CI: `pnpm dlx madge --circular --extensions ts,tsx packages apps` must exit 0. Turbo also errors on a cyclic task graph.

5. **Define the task pipeline with dependsOn + inputs/outputs — this is what makes caching work.** A task's cache key = its declared `inputs` + its dependencies' outputs; get these wrong and you get false hits (stale) or zero hits (no speedup).

   ```jsonc
   // turbo.json
   {
     "$schema": "https://turbo.build/schema.json",
     "tasks": {
       "build": {
         "dependsOn": ["^build"],                       // build deps first (topo order)
         "inputs": ["src/**", "tsconfig.json", "package.json"],
         "outputs": ["dist/**"]                          // MUST list outputs or cache restores nothing
       },
       "test":  { "dependsOn": ["build"], "outputs": ["coverage/**"] },
       "lint":  { "dependsOn": [] },
       "dev":   { "cache": false, "persistent": true }   // never cache long-running dev servers
     }
   }
   ```
   `^build` = "build all internal dependencies first"; `build` (no caret) = "this package's own build". Add `"globalDependencies": ["tsconfig.base.json", ".env"]` so a base-config change busts every cache. Anything generated must appear in `outputs` or the cache restore is empty and reruns do real work.

6. **Turn on remote cache so CI and teammates share results.** Local cache only helps the same machine. `npx turbo login && npx turbo link` (Vercel Remote Cache) or self-host with a `TURBO_TOKEN` + `TURBO_API` env in CI. Now a build artifact produced on one PR/runner is reused everywhere — the single biggest CI-time win.

7. **Run affected/changed-only in CI.** Replace "build everything" with a graph-filtered command so untouched packages are skipped (cache hit) or never scheduled:
   - **Turbo:** `turbo run build test lint --filter='...[origin/main]'` — runs only packages changed since `main` plus everything that depends on them.
   - **Nx:** `nx affected -t build test lint --base=origin/main`.
   - Require `fetch-depth: 0` (full history) in CI checkout or the merge-base is wrong and the filter degrades to "run everything." This is the most common reason affected runs silently rebuild all.

8. **Share one base config; extend per package — don't copy.** A single source of truth in a `@acme/config` package, extended by every other package:
   ```jsonc
   // tsconfig.base.json (root)  → strict, composite for project refs
   { "compilerOptions": { "strict": true, "composite": true, "declaration": true } }
   // packages/ui/tsconfig.json
   { "extends": "../../tsconfig.base.json", "include": ["src"], "compilerOptions": { "outDir": "dist" } }
   ```
   Same pattern for ESLint flat config and Prettier: define once in `@acme/config`, `import`/`extends` it everywhere. Per-package files hold only the genuine deltas (paths, env). (The lint/format/hook *content* itself → setup-lint-format-precommit.)

9. **Add Changesets for versioning/release intent.** `pnpm add -Dw @changesets/cli && pnpm changeset init`. Workflow: contributor runs `pnpm changeset` (records which packages changed + semver bump + a user-facing note); CI runs `changeset version` to bump versions, rewrite `workspace:*` → real versions, and update CHANGELOGs, opening a "Version Packages" PR. Set `"linked"`/`"fixed"` groups in `.changeset/config.json` only if packages must move in lockstep. The actual `npm publish` after merge is publish-package-registry's job.

## Common Errors

- **Missing `outputs` in `turbo.json`.** Cache key matches → "cache hit" → but `dist/` is never restored, so downstream tasks see no artifacts and fail or rebuild. Every task that emits files must declare `outputs`.
- **Shallow CI checkout (`fetch-depth: 1`).** `--filter='...[origin/main]'` / `nx affected --base` can't compute a merge-base and falls back to running everything. Use `fetch-depth: 0`.
- **Version range instead of `workspace:*` for an internal dep.** Pulls the published registry copy instead of local source; edits don't propagate and you debug a stale version. Always `workspace:*` (or `workspace:^`) for internal deps.
- **No `dependsOn: ["^build"]`.** Packages build in arbitrary order and a consumer compiles against a missing/old `dist/` of its dependency — flaky "module not found" that vanishes on rerun (warm cache). Declare the topo dependency.
- **Caching `dev`/`watch`/`start`.** Persistent tasks have no terminal output to cache; mark them `"cache": false, "persistent": true` or Turbo waits forever / serves stale.
- **Circular package dependency.** `@acme/a` ↔ `@acme/b` makes topological ordering impossible and silently corrupts incremental builds. Break it by extracting the shared piece into a third leaf package. Gate with `madge --circular` in CI.
- **Reaching into a sibling via relative path** (`import x from "../../other-pkg/src/util"`). Bypasses the declared graph, so affected-detection and caching miss the edge. Import via the package name and add the `dependency`; ban relative cross-package imports with lint.
- **Hoisting/phantom deps.** A package uses something it never declared but that happens to be hoisted to the root `node_modules`. Works locally, breaks when published or with stricter installs. pnpm's strict layout surfaces these — fix by adding the real `dependency`; don't reach for `shamefully-hoist`.
- **Base config changes that don't bust the cache.** Edit `tsconfig.base.json`, rerun, get stale cached builds. List shared base files in Turbo `globalDependencies` (or each task's `inputs`).
- **A `changeset` not added with a PR.** The release PR then ships no version bump / empty changelog for that change. Add a CI check that PRs touching `packages/**` include a `.changeset/*.md` (or are explicitly marked no-release).

## Verify

1. **Cache hit on rerun (the core proof):** `turbo run build` once (cold), then **again with no changes** → second run reports `FULL TURBO` / every task `cache hit, replaying logs` and finishes in ~seconds. If it rebuilds, `outputs`/`inputs` are wrong.
2. **Affected graph is correct:** edit one file in a single leaf package, then `turbo run build --filter='...[origin/main]' --dry=json` (or `nx affected:graph`) → the task list includes that package **and only its dependents**, not the whole repo.
3. **Targeted invalidation:** change a file in `@acme/ui` → on next run `@acme/ui` and its consumers rebuild while unrelated packages stay cache-hit. Change `tsconfig.base.json` → **everything** rebuilds (global dep busted).
4. **Acyclic graph:** `pnpm dlx madge --circular --extensions ts,tsx packages apps` exits 0; `turbo run build` reports no cyclic-dependency error.
5. **Internal linking real:** `pnpm why @acme/ui` (from a consumer) resolves to the local workspace path, not a registry version; grep confirms `workspace:` on every internal dep.
6. **Boundaries enforced:** a relative cross-package import (`../other-pkg/src/...`) fails lint; an undeclared import fails install/typecheck under pnpm's strict layout.
7. **Remote cache shared:** run `turbo run build` on a clean checkout / second machine (or fresh CI runner) with the remote cache configured → cache hits sourced remotely, no local rebuild.
8. **Release intent works:** `pnpm changeset` then `pnpm changeset version` bumps only the listed packages, rewrites their `workspace:*` to concrete versions, and updates each CHANGELOG.

Done = a no-op rerun is `FULL TURBO` (cache hit), the affected filter rebuilds exactly the changed packages plus their dependents (not the repo), the package graph is acyclic with all internal deps on `workspace:` and enforced boundaries, base configs are extended (not copied), and the remote cache is shared across machines/CI.
