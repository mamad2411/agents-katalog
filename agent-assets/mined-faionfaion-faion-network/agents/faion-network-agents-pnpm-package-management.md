# pnpm Package Management

## Summary

**One-sentence:** Produces a pnpm-managed Node.js project config (.npmrc + pnpm-workspace.yaml + package.json packageManager pin + CI workflow) enforcing frozen lockfile, no shameful hoist, and only-allow pnpm.

**One-paragraph:** pnpm uses a content-addressable store and symlinked node_modules for strict dependency isolation. This methodology produces the config files that wire a project to pnpm correctly: .npmrc (strict-peer-dependencies, frozen-lockfile, engine-strict), pnpm-workspace.yaml (for monorepos), root package.json with a pinned packageManager field, a preinstall hook (only-allow pnpm) to block npm/yarn drift, and a CI workflow using pnpm/action-setup with store cache.

**Ефективно для:**

- All new Node.js/TypeScript projects unless org policy mandates npm/yarn.
- Monorepos with 3+ packages — pnpm workspaces are faster and first-class.
- CI pipelines where install time matters; pnpm + store cache shaves minutes.
- Projects with phantom-dependency bugs (imports work locally, fail in CI).

## Applies If (ALL must hold)

- All new Node.js/TypeScript projects unless org policy requires npm/yarn.
- Monorepos with 3+ packages: pnpm workspaces are faster and first-class.
- CI pipelines where install time matters; pnpm + store cache shaves minutes.
- Projects with phantom-dependency bugs (imports work locally, fail elsewhere).
- Container builds wanting layer-cached deps via pnpm fetch.

## Skip If (ANY kills it)

- React Native projects pinned to npm/yarn by Metro/Expo (Expo SDK <= 50 had pnpm rough edges).
- One-file scripts where npm exec/bunx is lighter.
- Deploy targets with configs expecting package-lock.json that cannot be updated.
- Hosting platforms that refuse to honour the packageManager field.

## Prerequisites

| Artefact | Format | Source |
|----------|--------|--------|
| Project root path + node_modules layout | directory | filesystem |
| Node.js >= 16.9 | binary on PATH | developer machine + CI |
| Target pnpm major version | semver string | team decision (default: latest LTS major) |

## Assumes Loaded

| Methodology | Why |
|-------------|-----|
| [[trunk-based-ci-gates]] | CI workflow runs on trunk-based gate; this methodology produces the install step inside that gate |

## Content (load on demand)

| File | Depth | What's inside | Est. tokens |
|------|-------|---------------|-------------|
| `content/01-core-rules.xml` | essential | 6 testable rules with rationale + source | 1200 |
| `content/02-output-contract.xml` | essential | JSON Schema draft-07 + valid/invalid examples + forbidden patterns | 900 |
| `content/03-failure-modes.xml` | essential | 5 antipatterns with symptom/root-cause/fix | 800 |
| `content/04-procedure.xml` | essential | 6-step procedure | 900 |
| `content/06-decision-tree.xml` | essential | Routing tree → conclusion(ref=rule-id) | 600 |

## Task Routing

| Sub-task | Model | Rationale |
|----------|-------|-----------|
| `audit-existing-config` | sonnet | scan .npmrc, package.json, lockfile shape — judgment on what to keep |
| `emit-config-files` | haiku | mechanical template rendering once the audit decided values |
| `classify-outdated-deps` | sonnet | patch/minor/major risk classification of pnpm outdated -r --format json |

## Templates

| File | Purpose |
|------|---------|
| `templates/npmrc` | Strict .npmrc — engine-strict, frozen lockfile, no shameful hoist |
| `templates/pnpm-workspace.yaml` | Workspace definition for apps/packages/tools layout |
| `templates/ci-pnpm.yml` | GitHub Actions workflow with pnpm store cache + frozen lockfile install |
| `templates/dockerfile-pnpm` | Multi-stage Dockerfile using pnpm fetch for layer caching |
| `templates/artefact.json` | Sample artefact metadata consumed by validator |

Files the packer does not ship standalone have their bodies inlined under `## Template Contents` at the end of this file - read them there, do not fetch the path.

## Scripts

| File | Purpose | When to call |
|------|---------|--------------|
| `scripts/validate-pnpm-package-management.py` | Validate output artefact against the JSON Schema in `content/02-output-contract.xml` | CI on each artefact change; pre-commit; agent self-check |

## Related

- [[trunk-based-ci-gates]]
- [[trunk-based-dev-patterns]]
- [[practices-js-ts-stack]]

## Decision tree

See `content/06-decision-tree.xml`. The tree maps observable signals (input shape, environment context, risk level) to a concrete conclusion, each leaf referencing a rule from `01-core-rules.xml`. Use it when in doubt about which rule applies to the current context.

## Template Contents

Bodies of the templates above that the packer does not ship as standalone files, inlined here so they are deliverable.

### `templates/npmrc`

```text
strict-peer-dependencies=true
auto-install-peers=true
prefer-frozen-lockfile=true
engine-strict=true
# shamefully-hoist intentionally unset (defaults to false)
# node-linker=hoisted is ONLY acceptable with an inline comment naming the native add-on
```

### `templates/pnpm-workspace.yaml`

```yaml
packages:
  - 'apps/*'
  - 'packages/*'
  - 'tools/*'
```

### `templates/ci-pnpm.yml`

```yaml
name: CI
on: [push, pull_request]

jobs:
  build:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v4
      - name: Install pnpm
        uses: pnpm/action-setup@v4
        with:
          version: 9
      - name: Setup Node.js with pnpm store cache
        uses: actions/setup-node@v4
        with:
          node-version: '20'
          cache: 'pnpm'
      - name: Install (frozen lockfile)
        run: pnpm install --frozen-lockfile
      - name: Build changed packages only
        run: pnpm --filter '...[origin/main]' build
      - name: Test changed packages only
        run: pnpm --filter '...[origin/main]' test
      - name: Lint all packages
        run: pnpm -r lint
```

### `templates/dockerfile-pnpm`

```text
FROM node:20-alpine AS base
RUN corepack enable
WORKDIR /app

FROM base AS deps
COPY pnpm-lock.yaml ./
RUN pnpm fetch

FROM deps AS build
COPY . .
RUN pnpm install --frozen-lockfile --offline
RUN pnpm -r build

FROM base AS runtime
COPY --from=build /app/dist /app/dist
COPY --from=build /app/node_modules /app/node_modules
CMD ["node", "dist/main.js"]
```

### `templates/artefact.json`

```json
{
  "package_manager": "pnpm@9.1.0",
  "npmrc_shamefully_hoist": false,
  "npmrc_strict_peer_dependencies": true,
  "npmrc_engine_strict": true,
  "ci_frozen_lockfile": true,
  "preinstall_only_allow": true,
  "workspace_packages": [
    "apps/*",
    "packages/*"
  ],
  "lockfile_committed": true
}
```
