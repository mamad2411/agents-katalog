---
name: monorepo-management
description: Sets up and maintains monorepos - workspace tooling choice, package boundaries, affected-only builds and tests, remote caching, shared config, versioning and code ownership. Use when creating or restructuring a monorepo, adding a package or app to one, CI is slow because everything rebuilds, imports cross package boundaries, or choosing between Nx, Turborepo, Bazel, pnpm, Gradle, Go or Cargo workspaces. Not for splitting a monolith into services.
license: MIT
---

# Monorepo Management

A monorepo only works if two things stay true: **package boundaries are enforced by tooling, and CI does work proportional to the change, not to the repo.** Without both, a monorepo becomes a slow, tangled monolith with extra config.

## When to use

- Creating a monorepo, or moving several repos into one.
- Adding a new app or package to an existing workspace.
- CI time grows with repo size; every PR rebuilds and retests everything.
- Packages import each other's internals; changes in one break others unexpectedly.
- Choosing or replacing workspace tooling.

Not for: breaking a monolith into deployable services (see the large-scale-migrations skill). A monorepo is about where code lives, not how it is deployed.

## Does a monorepo fit?

| Signal | Monorepo helps | Monorepo hurts |
| --- | --- | --- |
| Shared code | Many packages share libraries, types, config | Projects share little |
| Change shape | Changes often span several packages (API + client) | Changes stay inside one project |
| Teams | Teams accept shared tooling and conventions | Teams need different toolchains, release cadences, access controls |
| Tooling budget | Someone owns build/CI tooling | Nobody has time to maintain the build system |
| Access control | Code can be visible to all contributors | Parts must be hidden from some contributors |

If most answers are on the right, keep separate repos and share code through versioned packages.

## Choosing tooling

Start with the lightest tool that gives you affected builds and caching for your stack. Add a heavier one only when you hit its limits.

| Tool | Best for | Affected / caching | Cost |
| --- | --- | --- | --- |
| npm / pnpm / yarn workspaces | JS/TS, linking local packages | None by themselves (pnpm `--filter` can select changed packages) | Lowest |
| Turborepo | JS/TS task orchestration on top of workspaces | Content-hash task cache, local and remote; filter by git range | Low |
| Nx | JS/TS (plus plugins for other stacks), larger orgs | Project graph, `nx affected`, local and remote cache, boundary lint rules | Medium |
| Bazel | Polyglot, very large repos, hermetic builds | Fine-grained, remote cache and remote execution | High: needs dedicated owners |
| Gradle multi-project | JVM | Incremental builds, build cache (local/remote) | Medium |
| Go workspaces (`go.work`) | Several Go modules developed together | Go build cache; no affected detection | Low |
| Cargo workspaces | Rust crates | Shared `target/` and `Cargo.lock`; incremental compilation | Low |
| .NET solution (`*.sln`) + `Directory.Build.props` | .NET | Incremental builds; shared props and central package management | Low |

Defaults: JS/TS with fewer than ~50 packages: pnpm workspaces + Turborepo or Nx. JVM: Gradle. Polyglot at large scale with a platform team: Bazel.

## Workflow: structure the repo

1. **Pick a layout and stick to it.**
   ```
   apps/        # deployable things: web, api, workers
   packages/    # libraries consumed by apps (or libs/)
   tooling/     # shared config: eslint, tsconfig, build scripts
   ```
2. **Declare the workspace** in the tool's root file: `pnpm-workspace.yaml` (`packages:` globs), `"workspaces"` in root `package.json` (npm/yarn), `settings.gradle(.kts)` `include(...)`, `go.work` (`go work init`, `go work use ./svc`), `[workspace] members` in root `Cargo.toml`.
3. **Use workspace references for internal deps**, not published versions: `"@acme/ui": "workspace:*"` (pnpm, Yarn 2+; npm and Yarn 1 use a plain version range), `implementation(project(":lib"))` (Gradle), `path = "../lib"` or `workspace = true` (Cargo).
4. **One lockfile at the root.** Commit it. Never commit per-package lockfiles in a JS workspace.
5. **Centralize versions of third-party deps** where the tool supports it: Cargo `[workspace.dependencies]`, Gradle version catalogs (`gradle/libs.versions.toml`), .NET Central Package Management (`Directory.Packages.props`), pnpm catalogs (check that the installed pnpm version supports them). One version of each dependency across the repo prevents "works in package A, breaks in B".
6. **Share config through packages**: `tooling/tsconfig` with `tsconfig.base.json`, an ESLint config package, a shared Gradle convention plugin. Packages extend; they do not copy.

## Boundaries

Rules every repo needs, enforced by a tool that fails CI:

- **Import packages only through their public entry point.** No `@acme/ui/src/internal/button`. Set `"exports"` in each `package.json` so deep imports fail at resolution.
- **Dependency direction is one way.** Apps depend on packages; packages never depend on apps; low-level packages never depend on feature packages.
- **No cycles** between packages.

| Stack | Enforcement |
| --- | --- |
| JS/TS | `package.json` `exports`; Nx `@nx/enforce-module-boundaries` with project tags; `eslint-plugin-boundaries`; `dependency-cruiser`; ESLint `no-restricted-imports` |
| JVM | Gradle project dependencies (no dependency means no access); ArchUnit tests for package rules |
| Go | `internal/` directories are enforced by the compiler |
| Bazel | `visibility` attributes on targets |
| .NET | Project references; `internal` + `InternalsVisibleTo` only for tests |

## CI: work proportional to the change

1. **Compute affected projects** from the diff against the merge base: `nx affected -t lint test build`, `turbo run test --filter=...[origin/main]`, `pnpm --filter "...[origin/main]" test`. Newer Turborepo versions also offer `--affected`; check `turbo run --help`.
2. **Fetch enough history** for the diff: with GitHub Actions `actions/checkout`, set `fetch-depth: 0` (or fetch the base branch) or affected detection silently falls back to "everything" or "nothing".
3. **Include dependents, not just changed packages.** A change to `packages/ui` must test every app that uses it. Turborepo/pnpm filter syntax `...pkg` selects dependents; `nx affected` does this by default.
4. **Cache task outputs** keyed by inputs (sources, lockfile, env vars, tool versions). Declare outputs (`dist/**`, `build/`) and inputs precisely; a missing input gives wrong cache hits, which is worse than no cache.
5. **Turn on remote caching** so CI and developers share results (Nx and Turborepo offer hosted and self-hosted options; Gradle and Bazel support remote cache servers). Treat cache write access as sensitive: anyone who can write can poison builds. Let only CI on trusted branches write.
6. **Run a full build on main** periodically (nightly or on merge) to catch anything affected detection missed.
7. **Shard large test suites** across CI machines once affected-only is not enough.

## Versioning and releasing

| Model | When | How |
| --- | --- | --- |
| Single version (everything releases together) | Apps deployed together; internal-only packages | One version in root; tag the repo |
| Independent versions | Packages published to a registry for outside consumers | Changesets (`npx changeset`, then `changeset version` and `changeset publish`), Nx release, or similar |
| No versions (always head) | Internal packages consumed only inside the repo | `workspace:*`; apps deploy from a commit |

Prefer "no versions" for internal packages: it is the main benefit of a monorepo. Publishing to a registry is outward-facing: confirm with the user before running any publish command.

## Ownership

- Add a `CODEOWNERS` file (GitHub: root, `docs/` or `.github/`; GitLab: root, `docs/` or `.gitlab/`) mapping paths to teams, and require code-owner review on protected branches. On Azure DevOps, use branch policies with path-filtered required reviewers.
- Every package has an owner and a short README: purpose, public API, how to test.
- Keep root-level files (CI, lockfile, shared config) owned by the platform/tooling owners.

## Anti-patterns

- **Monorepo without affected builds** - CI time grows forever and developers start skipping it.
- **Deep imports into other packages** - every internal refactor becomes a cross-team breaking change.
- **Copy-pasted config** - twenty slightly different `tsconfig.json` files. Extend a shared base.
- **Multiple versions of the same dependency** - subtle runtime bugs (two React copies, two protobuf runtimes). Centralize versions.
- **Undeclared task inputs** - caches return stale outputs; builds "pass" with old code.
- **Shallow clones in CI** - affected detection compares against nothing.
- **Bazel without owners** - adopting a heavyweight build system nobody can maintain.

## Done when

- The workspace builds and tests from a clean clone with the documented root commands.
- Boundary rules run in CI and fail on a deep import or wrong-direction dependency.
- A PR touching one leaf package runs only that package and its dependents; a change to shared config runs everything.
- Task caching is on, with inputs and outputs declared; cache writes are limited to trusted CI.
- Every package has an owner in `CODEOWNERS` and a README.
