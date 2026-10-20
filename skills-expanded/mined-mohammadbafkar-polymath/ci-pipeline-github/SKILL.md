---
name: ci-pipeline-github
description: Author a GitHub Actions workflow — lint/test/build/deploy with caching, concurrency control, OIDC for cloud auth, minimal permissions.
---

# ci-pipeline-github

> Write a `.github/workflows/*.yml` that's correct, fast, and secure.

## When to use

- A new repo needs CI.
- An existing workflow is slow, leaky, or sprawling.

## Inputs

- Language + framework.
- Deploy target (registry, k8s, serverless, …).
- Existing convention (other workflows in the repo to mirror).

## Project localization

Before the procedure, resolve the project snapshot — glob
`${POLYMATH_DATA_DIR:-$HOME/.polymath/data}/polymath-core/project-context.json` (newest
wins; absent → skip and use built-in defaults). Then apply (contract:
`polymath-core:project-context`):

- `conventions_docs`: read role `deployment` — pipeline standards and
  branch-to-environment mapping there override the generic layout
  below.

## Procedure

1. **Scope per workflow** — separate files for separate triggers. `ci.yml` for PRs + main, `deploy.yml` for tags, `nightly.yml` for cron. Don't shove everything into one workflow with branchy `if`s.
2. **Triggers**:
   - PRs: lint + test + build (no deploy).
   - main: same + publish artifacts.
   - tags `v*`: release.
3. **`permissions:` declared explicitly** at the workflow level (default to `contents: read`). Each job overrides as needed.
4. **`concurrency:`** to cancel superseded runs on the same ref. Saves runner minutes and avoids out-of-order deploys.
5. **Cache** — language-aware caches (`actions/setup-node` with `cache: 'pnpm'`, `actions/setup-python` with `cache: 'pip'`, `actions/cache` keyed on lock files for Go modules).
6. **OIDC for cloud auth** — never store long-lived cloud credentials as secrets. Use the cloud provider's GitHub OIDC trust for `aws-actions/configure-aws-credentials@v4`, `google-github-actions/auth@v2`, `azure/login@v2`.
7. **Pin actions by SHA** for security-critical actions; floating `@v4` for trusted first-party is acceptable.
8. **Fail fast** — set `fail-fast: false` only when matrix jobs are genuinely independent and you want signal across all.

## Output

```yaml
name: ci

on:
  pull_request:
  push:
    branches: [main]

permissions:
  contents: read

concurrency:
  group: ci-${{ github.workflow }}-${{ github.ref }}
  cancel-in-progress: true

jobs:
  test:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v4
      - uses: actions/setup-node@v4
        with:
          node-version: '20'
          cache: 'pnpm'
      - run: corepack enable && pnpm install --frozen-lockfile
      - run: pnpm lint
      - run: pnpm test --reporter=dot

  build:
    needs: test
    runs-on: ubuntu-latest
    permissions:
      id-token: write    # OIDC for cloud login
      contents: read
    steps:
      - uses: actions/checkout@v4
      - uses: docker/setup-buildx-action@v3
      - uses: aws-actions/configure-aws-credentials@v4
        with:
          role-to-assume: arn:aws:iam::123456789012:role/github-actions
          aws-region: us-east-1
      - uses: docker/build-push-action@v6
        with:
          context: .
          push: ${{ github.ref == 'refs/heads/main' }}
          tags: 123456789012.dkr.ecr.us-east-1.amazonaws.com/refund:${{ github.sha }}
          cache-from: type=gha
          cache-to: type=gha,mode=max
```

## Quality bar

- `permissions:` declared at workflow level; jobs grant the minimum.
- No `AWS_ACCESS_KEY_ID` / `GCP_SERVICE_ACCOUNT_KEY` in secrets — use OIDC.
- Concurrency-grouped to cancel superseded runs.
- Cache configured for the language.
- Build outputs only push on main / tags, not on PRs.

## Anti-patterns to avoid

- `secrets.AWS_ACCESS_KEY_ID` for cloud auth.
- One workflow with 8 `if: github.event_name == …` branches.
- `actions/checkout@master` (use pinned versions).
- Running deploy on every PR.
