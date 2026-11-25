---
name: local-ci-precheck
description: "Runs CI's lint, typecheck, architecture-audit, drift and bundle-size checks locally in parallel, catching workspace-package issues and stale generated artifacts (dep-graph) in 30 seconds instead of 5 minutes. Use before opening or pushing to a PR."
user-invocable: true
disable-model-invocation: true
---

# /local-ci-precheck

Mirror of the CI workflow's blocking checks (`lint`, `typecheck`, `architecture-audit`, drift, bundle size), run in parallel from your shell. Designed for the workflow gap that bit us hard in commits `e928d65`/`65e99ac`/`a1c2db2` (April 2026): pre-existing lint and typecheck errors on `main` were invisible because (a) the CI workspace-symlink cache bug ate them and (b) `pnpm typecheck` wasn't part of the pre-commit hook. By the time CI told us, three separate fixes had to land in a chicken-and-egg PR stack.

This skill closes that gap: run it before push, get the same red/green CI gives you — without burning a full GitHub Actions cycle.

## When to invoke

- **Before `git push` on a feature branch** — catches what CI would catch
- **After a non-trivial refactor** that touched multiple workspaces
- **After bumping a shared package** (rialto, types, config) that downstream packages consume
- **Before merging a PR** — final sanity that nothing drifted since the last CI run

## What it runs

In parallel, from the repo root:

| Step | Command                                                                                                                | Mirrors CI job              |
| ---- | ---------------------------------------------------------------------------------------------------------------------- | --------------------------- |
| 1    | `pnpm install --frozen-lockfile`                                                                                       | `prepare`                   |
| 2    | `pnpm lint`                                                                                                            | `lint`                      |
| 3    | `pnpm check:knip` (own lane; memory-heavy, skip with `--skip-knip`)                                                    | `lint` (knip step)          |
| 4    | `pnpm typecheck`                                                                                                       | `typecheck`                 |
| 5    | `pnpm build --filter @mbe/cli... && pnpm --filter @mbe/cli start check-adr && pnpm --filter @mbe/cli start check-deps` | `architecture-audit`        |
| 6    | dep-graph regen + `git diff --exit-code` (see Drift lane)                                                              | `build` / `integrity` drift |
| 7    | `pnpm turbo run size:check --filter='...[origin/main]'` (affected packages only; see Size lane)                        | `build` bundle size budgets |

Steps 2–7 run in parallel after step 1 completes. `scripts/__tests__/local-ci-precheck-mirror.test.mjs` fails when a `pnpm` command in CI's `lint`, `typecheck` or `architecture-audit` job is missing from this file. Total time on a warm cache: ~30s (vs ~5 min for a CI round-trip); the size lane measured 18.5 s for a branch touching `apps/hospitality`, build included.

## Invocation

```bash
# Full check (default)
/local-ci-precheck

# Just typecheck (fastest single check; what catches most refactor breaks)
/local-ci-precheck --typecheck-only

# Just lint (catches custom rule violations like require-rfc-7807-errors)
/local-ci-precheck --lint-only

# Skip install (if you just installed)
/local-ci-precheck --skip-install

# Just the drift lane (after dependency or shared-package changes)
/local-ci-precheck --drift-only

# Skip the size lane (e.g. a rialto change that rebuilds every consuming app)
/local-ci-precheck --skip-size

# Skip the knip lane (memory-heavy locally; a chained run was killed with exit 137 on 2026-10-25)
/local-ci-precheck --skip-knip
```

Implementation pattern (Bash):

```bash
#!/usr/bin/env bash
set -euo pipefail

cd "$(git rev-parse --show-toplevel)"

if [[ "${1:-}" != "--skip-install" ]]; then
  echo "→ pnpm install --frozen-lockfile"
  pnpm install --frozen-lockfile
fi

# Run the three blocking checks in parallel; fail-fast on any.
fail=0
{
  pnpm lint 2>&1 | sed 's/^/[lint] /' &
  lint_pid=$!
  # knip is its own lane, never chained onto lint: CI runs it as a separate step.
  knip_pid=""
  if [[ " $* " != *" --skip-knip "* ]]; then
    pnpm check:knip 2>&1 | sed 's/^/[knip] /' &
    knip_pid=$!
  fi
  pnpm typecheck 2>&1 | sed 's/^/[typecheck] /' &
  type_pid=$!
  ( pnpm build --filter @mbe/cli... && \
    pnpm --filter @mbe/cli start check-adr && \
    pnpm --filter @mbe/cli start check-deps ) 2>&1 | sed 's/^/[arch-audit] /' &
  arch_pid=$!

  ( set -e
    pnpm build --filter "@mbe/cli..." >/dev/null
    pnpm graph >/dev/null
    pnpm generate:dep-graph >/dev/null
    git diff --exit-code --stat -- \
      docs/architecture/dependency-graph.md \
      infrastructure/worker/dep-graph.json
  ) 2>&1 | sed 's/^/[drift] /' &
  drift_pid=$!

  # Affected packages + dependents only; turbo builds what size:check needs.
  # An empty affected set (docs-only change) runs nothing and exits 0.
  size_pid=""
  if [[ " $* " != *" --skip-size "* ]]; then
    pnpm turbo run size:check --filter='...[origin/main]' 2>&1 | sed 's/^/[size] /' &
    size_pid=$!
  fi

  wait $lint_pid || fail=1
  [[ -z "$knip_pid" ]] || wait $knip_pid || fail=1
  wait $type_pid || fail=1
  wait $arch_pid || fail=1
  wait $drift_pid || fail=1
  [[ -z "$size_pid" ]] || wait $size_pid || fail=1
}

if (( fail )); then
  echo ""
  echo "✗ /local-ci-precheck: at least one CI-blocking check failed."
  echo "  Fix above before pushing — these will block PR merge."
  exit 1
fi

echo ""
echo "✓ /local-ci-precheck: all CI-blocking checks pass."
```

## Output guarantees

- Exits **0** when CI would pass — push with confidence.
- Exits **1** when CI would block — fix before pushing.
- Each line is prefixed with `[lint]`, `[knip]`, `[typecheck]`, `[arch-audit]`, `[drift]`, or `[size]` so parallel output is readable.

## Drift lane

CI's Build job regenerates `infrastructure/worker/dep-graph.json`; it fails the PR if the committed artifacts don't match. This lane catches that locally:

1. `pnpm graph` regenerates `docs/architecture/dependency-graph.md`; `pnpm generate:dep-graph` regenerates `infrastructure/worker/dep-graph.json`. `git diff --exit-code` on both — any delta means the committed graphs are stale.

**When it matters:** after adding/removing a workspace package, changing any `dependencies`/`devDependencies`. The pre-commit hook does NOT regenerate the dep graphs — this lane is the only local gate.

**Working-tree semantics:** when nothing drifted, the regenerated graph files are byte-identical — the tree is untouched. When drift exists, the two graph files are left **regenerated in place** (that is the fix — stage and commit them).

**Caveat:** run `nvm use` first — a Node version mismatched with CI (`.nvmrc` pins 22) can produce false generated-artifact drift (see `.claude/rules/gotchas.md`).

## Size lane

`Check bundle size budgets` (`pnpm size:check`) was the most frequent failing CI step: 9 of 40 failed `ci.yml` runs, 2026-11-06 to 11-08 (#8522). This lane runs whatever each affected package's `size:check` script runs, exactly as CI does:

1. **Chunk coverage**, `apps/hospitality` only (`scripts/check-chunk-coverage.mjs`, chained before `size-limit`): every built chunk ≥ 5 KB raw needs a `size-limit` entry or an allowlist reason. A new lazy import that produces a new chunk fails here: `1 built chunk(s) have no size-limit budget and no allowlist entry`.
2. **Budgets** (`size-limit`), every package with a `size:check` script: a package over its configured limit.

`--filter='...[origin/main]'` limits it to packages changed since `origin/main` plus their dependents, so a rialto change also checks the apps that consume it. Fix a chunk-coverage failure by adding a `size-limit` entry in the app's `package.json` (preferred) or an allowlist entry with a reason.

## Why this isn't just "run pnpm lint && pnpm typecheck"

- Parallelism — three checks at once, not three sequential waits.
- Same install path as CI (`--frozen-lockfile`) so a stale lockfile gets caught here, not in CI.
- Includes the architecture-audit step which most devs forget about.
- Standardized prefix output — when any check fails you immediately see which one.
- Forces no model invocation (`disable-model-invocation: true`) — this is a side-effect-y check the user runs themselves; Claude shouldn't fire it mid-conversation as guesswork.

## Pairs with

- The `pre-push` Bash hook in `.claude/settings.json` — that hook auto-fires this on `git push`, but you can run `/local-ci-precheck` manually anytime mid-iteration without committing.
- `/site-audit` — covers the runtime/UX dimension; this covers the build-time/types dimension.
- `/ci-monitor` — for after the push, when you need to check what CI is doing on the remote.

## Future enhancements

- **Test job too** — currently skipped because tests can be slow; add `--include-tests` flag.
- **Smart filtering** — only run the workspaces affected by HEAD vs. origin/main.
- **Coverage delta** — flag PR-level coverage drops once a coverage gate workflow exists.
