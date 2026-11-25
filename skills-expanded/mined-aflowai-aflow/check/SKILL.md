---
name: check
description: Pre-commit quality checks — auto-fix formatting and lint, then validate build, typecheck, and tests pass. Run before committing.
disable-model-invocation: true
---

# /check — Pre-commit Quality Checks

Run this **before committing** to catch and auto-fix all quality issues. This mirrors exactly what CI runs, so if `/check` passes locally, CI will pass too.

## What blocks a merge (CI enforcement)

| Check              | Blocks merge?         | Local command                                       |
| ------------------ | --------------------- | --------------------------------------------------- |
| Format             | **Yes**               | `yarn format:check` (CI) / `yarn format` (auto-fix) |
| Typecheck          | **Yes**               | `yarn typecheck`                                    |
| Build              | **Yes**               | `yarn build`                                        |
| Tests              | **Yes**               | `yarn test`                                         |
| Schema determinism | **Yes**               | (CI only — runs build twice and diffs)              |
| **Lint**           | **Yes — errors only** | `yarn lint`                                         |

> **Lint warnings are non-blocking**: There is a pre-existing backlog of ESLint warnings. The lint CI job still runs and prints warnings, but only actual ESLint errors block PRs. Fix lint in new code you write; don't add to the backlog.

---

## Why CI fails when local passes

The most common reason: **`dist/` is gitignored**. CI starts with no built packages. When `yarn build` runs without topological ordering, apps try to compile before their internal dependencies (`@aflow/executor-runtime`, `@aflow/schemas`, etc.) have been built. The fix — `--topological` flag — is already applied to the root `build` script.

**If you see "Cannot find module '@aflow/...'" errors in CI but not locally**: your local `dist/` folders are stale artifacts from a previous build. Always run `/check` with a clean build to catch this.

---

## Step 1 — Auto-fix formatting

```bash
yarn format
```

Prettier will reformat all files in-place. Stage the formatting changes along with your code changes. CI runs `yarn format:check` — if files would change, the format job fails.

---

## Step 2 — Auto-fix lint issues

```bash
yarn lint --fix
```

ESLint will fix what it can automatically. Review remaining warnings — fix in new code, don't suppress. Warnings do **not** block merges, but lint errors still do.

Common lint issues:

- Unused imports -> remove them (or prefix with `_` if intentional)
- Floating promises -> add `void` or `await`
- Template expression issues -> use `String(n)` for numbers
- Implicit `any` -> add explicit type annotations

---

## Step 3 — Rebuild packages (topological)

```bash
yarn build
```

This uses `--topological` (already in package.json) so packages build in dependency order:
`lib` -> `schemas` -> `redis`, `payload-store`, `input-resolution` -> `executor-runtime`, `ai-client`, `database` -> apps

**If the build fails with "Cannot find module '@aflow/...'"**: a package's `dist/` is missing. Build it explicitly first:

```bash
yarn workspace @aflow/schemas build
yarn workspace @aflow/executor-runtime build
# then retry
yarn build
```

---

## Step 4 — Typecheck

```bash
yarn typecheck
```

Runs `tsc -b` across all packages. Fix all errors — CI is strict and will reject any type errors.

Common patterns:

```typescript
// 'error' is of type 'unknown' -> narrow it
} catch (err) {
  const message = err instanceof Error ? err.message : String(err);
}

// Parameter implicitly has 'any' type -> annotate
.map((img: { data: string; mimeType?: string }) => ...)

// Cannot assign undefined to optional prop -> omit instead
const obj: { foo?: string } = {};  // not { foo: undefined }
```

---

## Step 5 — Run unit tests

```bash
yarn test
```

Fix any failing tests before proceeding. Tests must pass for the PR to merge.

---

## Step 6 — Check for schema rebuild requirement

If you changed anything in `packages/schemas/src/`:

```bash
yarn workspace @aflow/schemas build
yarn typecheck
```

Schema changes require a rebuild — other packages import compiled output. This is the most common "works locally, fails CI" scenario.

---

## Full check sequence

**Default — the scoped check:** commit, then

```bash
yarn verify              # what a publication runs: scoped build, type-check, tests, lint, format
```

It measures the commits on `HEAD` against `origin/main`, building only the packages the change
reads and running only the tests it can reach. The repository-wide jobs below are CI's; run them
locally only to prove something CI cannot show you sooner.

**Option A — preflight script (full proof):** runs everything and prints a summary table:

```bash
yarn preflight           # format + build + typecheck + test + lint
yarn preflight:no-test   # same but skip tests (when infra is not running)
```

**Option B — manual step-by-step:**

```bash
yarn format && \
yarn lint --fix && \
yarn build && \
yarn typecheck && \
yarn test
```

Format, typecheck, build, and test must all exit 0 before committing. Lint warnings are okay, but lint errors are not.

---

## CI parity checklist

CI runs these jobs on every PR to `main`:

| CI Job               | Local equivalent                                           | Blocks merge? |
| -------------------- | ---------------------------------------------------------- | ------------- |
| `format`             | `yarn format:check`                                        | **Yes**       |
| `typecheck`          | `yarn build && yarn typecheck`                             | **Yes**       |
| `build`              | `yarn build`                                               | **Yes**       |
| `test`               | `yarn test` (with Postgres + Redis)                        | **Yes**       |
| `schema-determinism` | `yarn workspace @aflow/schemas build` (run twice, compare) | **Yes**       |
| `lint`               | `yarn lint`                                                | Errors only   |

> **Note**: The `test` CI job runs against real Postgres and Redis services. Suites that need the schema skip without it, so run `yarn db:migrate` against a throwaway database for a full local run. Integration tests (`./scripts/test-flows.sh`) require `yarn start` running locally.
