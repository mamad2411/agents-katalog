---
name: github-actions-monorepo
description: >
  Reusable CI/CD patterns with GitHub Actions for NestJS + React Native/Next.js monorepos.
  Invoke automatically when configuring CI pipelines, automatic deploys,
  branch protection, secrets, or approval environments on GitHub.
---

# GitHub Actions — Monorepo CI/CD

## Workflow structure

```
.github/
├── dependabot.yml          ← keeps pinned action SHAs (and their version comments) up to date
└── workflows/
    ├── ci.yml                ← lint + typecheck + tests + build (every PR)
    ├── deploy-staging.yml    ← automatic deploy when merging to develop
    └── deploy-production.yml ← deploy with manual approval when merging to main
```

`develop → staging` / `main → production` is **one** option, not the only one. Trunk-based
flows (every merge to `main` deploys to staging; production is promoted by a tag, a release or
a `workflow_dispatch`) work just as well — pick one and document it.

---

## Baseline for every workflow

- **Pin actions by full commit SHA**, with the release in a comment — a moving tag (`@vN`) can
  be re-pointed to different code. Placeholders below look like
  `actions/checkout@<full-commit-sha> # vX.Y.Z`. To get the SHA of a release:
  ```bash
  # The peeled ref (^{}) is the commit; use it when present (annotated tags)
  git ls-remote --tags https://github.com/actions/checkout 'refs/tags/vX.Y.Z*'
  ```
  Dependabot (below) then bumps both the SHA and the version comment.
- **Least-privilege token:** `permissions: contents: read` at the top of every workflow; grant
  more per job only where needed (e.g. `pull-requests: write` for a bot comment).
- **`concurrency`** per workflow + ref. CI may cancel superseded runs; deploys must not
  (`cancel-in-progress: false`) — a cancelled deploy can leave migrations half-applied.
- **`timeout-minutes` on every job** — the default (6 hours) burns minutes on a hung step.
- **Node 24 + pnpm:** `pnpm/action-setup` with no `version` reads the exact pnpm version from
  the root `package.json` `"packageManager"` field, so CI, Docker (corepack) and developers
  use the same one. Run it before `actions/setup-node` so `cache: pnpm` works.
- **Globally installed CLIs at a pinned version** (`npm i -g @railway/cli@<x.y.z>`,
  `npm i -g eas-cli@<x.y.z>`) — an unpinned install hands deploy tokens to whatever release
  was published last.

```yaml
# .github/dependabot.yml
version: 2
updates:
  - package-ecosystem: github-actions
    directory: /
    schedule:
      interval: weekly
```

---

## ci.yml — Quality pipeline

```yaml
name: CI

on:
  pull_request:
    branches: [main, develop]

permissions:
  contents: read

concurrency:
  group: ${{ github.workflow }}-${{ github.ref }}
  cancel-in-progress: true          # a newer push supersedes this PR run

jobs:
  quality:
    runs-on: ubuntu-latest
    timeout-minutes: 20
    steps:
      - uses: actions/checkout@<full-commit-sha> # vX.Y.Z

      - uses: pnpm/action-setup@<full-commit-sha> # vX.Y.Z — version from "packageManager"

      - uses: actions/setup-node@<full-commit-sha> # vX.Y.Z
        with:
          node-version: 24
          cache: pnpm

      - name: Install dependencies
        run: pnpm install --frozen-lockfile

      - name: Lint
        run: pnpm lint

      - name: Type check
        run: pnpm type-check

      - name: Unit tests
        run: pnpm test

      - name: Build
        run: pnpm build

      - name: Integration tests
        run: pnpm test:integration
        env:
          DATABASE_URL: ${{ secrets.TEST_DATABASE_URL }}
```

**Make sure "Type check" really covers every app.** In a turbo/pnpm monorepo
`pnpm type-check` only runs in packages that define a `type-check` script — an app
without one is silently skipped, and the step still passes. This hides real gaps:
- **Expo / React Native app:** its `build` is usually a no-op in CI and Jest (Babel)
  strips types, so without its own `"type-check": "tsc --noEmit"` its types are
  **never** checked in CI.
- **NestJS API:** `nest build` checks `src/` but not test files.

Give every app `"type-check": "tsc --noEmit"` and confirm the turbo summary lists all of
them (e.g. `Tasks: 5 successful, 5 total`). For an Expo app with typed routes, generate
the route types first — see `expo-router` §21.

**A local type-check that passes is not proof CI's will — framework-generated types.**
Some frameworks write types into gitignored folders only when their dev server or build
runs, and the app's `tsconfig` includes them. On a dev machine they exist; on CI's fresh
checkout they don't:
- **Next.js (App Router):** `next dev`/`next build` generate `.next/types` — including
  globals such as `RouteContext<'/api/x/[...path]'>`, `PageProps` and `LayoutProps`.
  Code using them passes `tsc --noEmit` locally and fails CI with `Cannot find name
  'RouteContext'`. Type the handler's context explicitly
  (`{ params: Promise<{ path: string[] }> }`) or run `next typegen` before `tsc` in the
  `type-check` script.
- **Expo Router typed routes:** same trap with `.expo/types` — `expo-router` §21.

Before pushing a change that touches such code, type-check the way CI does, without the
generated folder — e.g. a throwaway `tsconfig` **inside the app** (so `@types/*` still
resolve) that `extends` the real one and excludes `.next`:
`{ "extends": "./tsconfig.json", "exclude": ["node_modules", ".next"], "include": ["next-env.d.ts", "**/*.ts", "**/*.tsx"] }`.
Don't delete `.next` to test this while `next dev` is running — it breaks the dev server.

---

## Deploy order

Deploy in dependency order, enforced with `needs:` — never as parallel jobs:

```
migrate (expand-only, backwards compatible) → API → health check → frontends / OTA update
```

The API must never run against a schema it doesn't know, and clients must never reach an API
that doesn't have their endpoints yet. Migrations use the direct database connection (or a
session pooler), not a transaction pooler — see `dev-patterns:supabase-setup`.

**Railway GitHub App vs `railway up`.** If the Railway GitHub App is connected to the service,
Railway already builds and deploys on every push to its branch — a `railway up` in Actions
builds and deploys **a second time**, and the two race. Choose one:
- **GitHub App** (simplest): drop the `deploy-api` job and enable Railway's "wait for CI" so
  the API deploys only after the workflow's checks (including `migrate`) pass; keep the
  `health-check` job, which polls until the new version answers.
- **Deploy from Actions**: disconnect the GitHub App from the service and keep `deploy-api`.

The same applies to web frontends deployed by a host's own Git integration (e.g. Vercel).

## deploy-staging.yml — Automatic deploy

```yaml
name: Deploy Staging

on:
  push:
    branches: [develop]

permissions:
  contents: read

concurrency:
  group: ${{ github.workflow }}-${{ github.ref }}
  cancel-in-progress: false         # never cancel a deploy half-way

jobs:
  migrate:
    runs-on: ubuntu-latest
    timeout-minutes: 15
    environment: staging
    steps:
      - uses: actions/checkout@<full-commit-sha> # vX.Y.Z
      - uses: pnpm/action-setup@<full-commit-sha> # vX.Y.Z
      - uses: actions/setup-node@<full-commit-sha> # vX.Y.Z
        with:
          node-version: 24
          cache: pnpm
      - run: pnpm install --frozen-lockfile
      - name: Run migrations (staging)
        run: pnpm migrate            # e.g. supabase db push --db-url "$DATABASE_URL"
        env:
          DATABASE_URL: ${{ secrets.STAGING_MIGRATION_DATABASE_URL }}   # direct / session connection

  deploy-api:                        # only when the Railway GitHub App is NOT connected
    needs: migrate
    runs-on: ubuntu-latest
    timeout-minutes: 20
    environment: staging
    steps:
      - uses: actions/checkout@<full-commit-sha> # vX.Y.Z
      - run: npm i -g @railway/cli@<x.y.z>       # pinned CLI version
      - name: Deploy to Railway (staging)
        run: railway up --service api-staging --ci
        env:
          RAILWAY_TOKEN: ${{ secrets.RAILWAY_STAGING_TOKEN }}

  health-check:
    needs: deploy-api
    runs-on: ubuntu-latest
    timeout-minutes: 10
    steps:
      - name: Readiness check with retry
        run: |
          for i in $(seq 1 20); do
            curl --fail --silent --max-time 5 "https://<staging-api-host>/api/v1/health/ready" && exit 0
            sleep 15
          done
          echo "API not ready after 5 minutes" >&2
          exit 1

  ota-update:
    needs: health-check
    runs-on: ubuntu-latest
    timeout-minutes: 20
    environment: staging
    steps:
      - uses: actions/checkout@<full-commit-sha> # vX.Y.Z
      - uses: pnpm/action-setup@<full-commit-sha> # vX.Y.Z
      - uses: actions/setup-node@<full-commit-sha> # vX.Y.Z
        with:
          node-version: 24
          cache: pnpm
      - run: pnpm install --frozen-lockfile
      - run: npm i -g eas-cli@<x.y.z>            # pinned CLI version
      - name: Publish OTA update (staging)
        working-directory: apps/mobile
        run: eas update --channel staging --non-interactive --message "${{ github.sha }}"
        env:
          EXPO_TOKEN: ${{ secrets.EXPO_TOKEN }}
```

A readiness check that passes can still be answered by the **previous** deployment while the
new one rolls out. When that matters, expose the deployed commit SHA (e.g. in the live
response) and poll until it matches `${{ github.sha }}`.

---

## deploy-production.yml — Deploy with manual approval

Same jobs and `needs:` chain as staging, with production secrets and channel. Put
`environment: production` on the **first** job (`migrate`) so the approval gates the whole
chain:

```yaml
name: Deploy Production

on:
  push:
    branches: [main]

permissions:
  contents: read

concurrency:
  group: ${{ github.workflow }}-${{ github.ref }}
  cancel-in-progress: false

jobs:
  migrate:
    runs-on: ubuntu-latest
    timeout-minutes: 15
    environment: production     # blocks until manual approval on GitHub (see plan note below)
    steps:
      # ... as in staging, with PROD_MIGRATION_DATABASE_URL

  deploy-api:
    needs: migrate
    # ... as in staging, with --service api-production and RAILWAY_PRODUCTION_TOKEN

  health-check:
    needs: deploy-api
    # ... as in staging, against https://<production-api-host>/api/v1/health/ready

  ota-update:
    needs: health-check
    # ... as in staging, with --channel production

  notify-failure:
    needs: [migrate, deploy-api, health-check, ota-update]
    if: failure()
    runs-on: ubuntu-latest
    timeout-minutes: 5
    steps:
      - run: echo "Deploy failed — check logs and trigger rollback if necessary"
```

---

## Branch protection — configure on GitHub

```
Branch: main
  ✓ Require pull request reviews (minimum 1 approval)
  ✓ Require status checks to pass (CI required)
  ✓ Require branches to be up to date before merging
  ✓ Restrict direct pushes (no one pushes directly)

Branch: develop
  ✓ Require status checks to pass (CI required)
```

---

## Required GitHub secrets

| Secret | Description |
|---|---|
| `RAILWAY_STAGING_TOKEN` / `RAILWAY_PRODUCTION_TOKEN` | Railway deploy tokens, one per environment (only when deploying from Actions) |
| `TEST_DATABASE_URL` | Database for integration tests |
| `STAGING_MIGRATION_DATABASE_URL` | Staging database, direct / session connection for migrations |
| `PROD_MIGRATION_DATABASE_URL` | Production database, direct / session connection for migrations |
| `EXPO_TOKEN` | EAS access token for OTA updates |
| `SENTRY_AUTH_TOKEN` | For source map uploads |

Prefer environment secrets (scoped to `staging` / `production`) over repository secrets for
anything a deploy job uses. The health-check targets above are fixed, public URLs per
environment, so they are written in the workflow instead of stored as secrets — secrets that
nothing varies end up dead and stale. Use a secret only if the target URL genuinely varies per
environment/deploy, and periodically prune secrets no workflow reads.

---

## Production environment with manual approval

Configure at GitHub → Settings → Environments → `production`:

```
Required reviewers: [your user or team]
Wait timer: 0 minutes
```

This blocks the deploy until someone approves manually in the GitHub Actions UI.

**Plan note:** environments are available on public repositories on every plan, but for
**private** repositories, environments and their protection rules (required reviewers, wait
timer) depend on the organization's GitHub plan — check the current GitHub docs for yours.
Without required reviewers, gate production with a manual `workflow_dispatch` or a release tag
instead.

---

## Complete deploy flow

```
Developer opens PR
        ↓
CI runs (lint + typecheck + tests + build) — must pass
        ↓
Code review (minimum 1 approval)
        ↓
Merge to develop → automatic deploy to staging
        ↓
QA validates on staging
        ↓
PR from develop → main
        ↓
Manual approval (GitHub environment protection)
        ↓
CI runs again on main
        ↓
Deploy to production: migrations → API → health check → frontends / OTA (needs: chain)
        ↓
Automatic health check with retry (/api/v1/health/ready)
        ↓
✓ Deploy complete
```
