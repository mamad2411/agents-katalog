---
name: ci-cd-javascript
description: "Applies when creating or modifying CI/CD pipelines for JavaScript/TypeScript projects. Covers npm/yarn/pnpm caching, jest/vitest coverage, eslint linting, and tsc type checking."
---

# JavaScript / TypeScript CI/CD

## Setup and caching

Use `actions/setup-node@v4` with the `cache` parameter:

| Manager | `cache:` value | Lockfile for key |
|---------|---------------|-----------------|
| npm | `'npm'` | `package-lock.json` |
| yarn | `'yarn'` | `yarn.lock` |
| pnpm | `'pnpm'` | `pnpm-lock.yaml` |

Cache the **download cache**, not `node_modules`.

For pnpm, add `corepack enable` or install via `pnpm/action-setup` before `setup-node`.

## Install commands (frozen)

```bash
npm ci                         # npm
yarn install --immutable       # yarn
pnpm install --frozen-lockfile # pnpm
```

## Coverage

```bash
# Jest
npx jest --coverage --coverageReporters=cobertura --coverageThreshold='{"global":{"lines":80}}'

# Vitest (preferred for new projects — faster, native ESM/TS)
npx vitest run --coverage --coverage.reporter=cobertura --coverage.thresholds.lines=80
```

Output: Cobertura XML for upload.

## Linting and type checking

```bash
npx eslint .
npx tsc --noEmit               # TypeScript type check (no output)
```

For TypeScript projects, always run `tsc --noEmit` as a separate CI job.

## Dependency audit

```bash
npm audit --audit-level=high
# or: npx audit-ci --high
```

## JS/TS-specific gotchas

1. `npm ci` is faster than `npm install` in CI — it deletes `node_modules` and installs from lockfile.
2. For monorepos (workspaces), set `cache-dependency-path` to the root lockfile.
3. Set `NODE_ENV=production` for build steps to exclude devDependencies from bundles.
4. For Vitest, set `coverage.provider` to `v8` (fast, built-in) or `istanbul` (more accurate).
5. Use `--max-workers=2` for Jest in CI to avoid OOM on low-memory runners.

## Sources

- https://github.com/actions/setup-node
- https://vitest.dev/guide/coverage.html
