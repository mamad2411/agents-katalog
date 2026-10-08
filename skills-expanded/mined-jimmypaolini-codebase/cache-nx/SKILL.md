---
name: cache-nx
description: Manage and debug Nx task cache inputs, shared-globals, externalDependencies, and dependency-versions. Use when task cache hit rates are low, when tasks execute unnecessarily, when modifying nx.json, or when a task executes with stale dependency configurations.
license: MIT
---

# Cache Nx

This skill manages Nx task caching configurations to ensure optimal build times and prevent unnecessary cache invalidation.

## Task Cache Inputs

`nx.json`'s `shared-globals` reaches almost every lint target, directly or
through `default`, so whatever it names is an input to nearly every task in the
workspace. It holds `configuration/tsconfig.json` and nothing else, and that is
load-bearing rather than incidental.

**Never add a high-churn file to `shared-globals`.** It once named
`pnpm-lock.yaml`, `nx.json`, and `.github/workflows/*.yml`, and because a pull
request is built from the merge commit, every branch inherited their churn — so
every task in the workspace re-hashed on essentially every run and 🧑‍💻 Lint
Codebase never recorded a single cache hit. Nothing failed; the work was simply
repeated. **Nothing checks for this** — a run whose cache never hits is still a
green run, so the only signal is the duration, and re-adding one glob here
silently undoes the whole arrangement. See
[ADR 0007](../../docs/adr/0007-state-the-real-dependency-in-task-cache-inputs.md).

State the real dependency instead:

- **Tool versions** belong in a per-target `{"externalDependencies": [...]}`
  entry, which hashes the resolved versions of exactly those packages. This is
  what `typecheck` has always done with `typescript`; every lint target now
  names its own tools the same way. A tool added to a target's command must be
  added there too, or an upgrade of it will replay a stale cached result.
- **Python tools** need no entry: their targets already declare
  `{workspaceRoot}/pyproject.toml` and `{workspaceRoot}/uv.lock`.
- **Whole-lockfile sensitivity**, where a target genuinely depends on every
  dependency rather than a named few, is the `dependency-versions` namedInput.
  `build` uses it, because a bundle really does change when any dependency
  does. No lint target should need it.

**A task's own artifact must never be one of its inputs**, or it rewrites the
hash it was just cached under and can never hit its own cache. `.eslintcache/`
is excluded from `default` and from the `eslint` inputs for that reason, and a
project's `codometer-report.json` is subtracted from its own.
