---
name: ci-github-actions
description: Use when writing or reviewing GitHub Actions workflows — triggers, caching, matrix builds, secrets/OIDC, @claude integration.
metadata:
  added: 2026-05-18
  last_reviewed: 2026-05-18
  type: ci
  status: active
  invokes_shell: false
  shell_reviewed: valksor 2026-05-17
  related:
    - ci-gitlab-ci
    - security
---

# GitHub Actions

**Iron Law: pin actions by SHA. Secrets via `${{ secrets.* }}` only. Fail-fast on matrix unless a cell is intentionally allowed to fail. NEVER use `pull_request_target` unless you've read GitHub's fork-poisoning docs end-to-end — it runs the PR's workflow with the base branch's secrets, which is a one-line supply-chain breach.**

## Workflow skeleton

```yaml
name: ci
on:
  push: { branches: [main] }
  pull_request:
  workflow_dispatch:
concurrency: # cancel superseded runs on the same ref
  group: ci-${{ github.ref }}
  cancel-in-progress: ${{ github.event_name == 'pull_request' }}
permissions: { contents: read } # principle of least privilege
jobs:
  test:
    runs-on: ubuntu-24.04
    timeout-minutes: 15
    steps:
      - uses: actions/checkout@<full-sha> # let Dependabot keep SHA fresh
      - uses: actions/setup-node@<full-sha>
        with: { node-version: "22", cache: "npm" }
      - run: npm ci && npm test
```

| Trigger                       | When to use                                                                                          |
| ----------------------------- | ---------------------------------------------------------------------------------------------------- |
| `push: branches: [main]`      | run on merges to default                                                                             |
| `pull_request:`               | run on PR open/sync/reopen — safe for fork PRs (no secrets)                                          |
| `pull_request_target:`        | **dangerous**: runs in base context with secrets. Only with strict path guards and code-review gates |
| `workflow_dispatch:`          | manual button in UI                                                                                  |
| `schedule: cron:`             | nightly builds, dep audits                                                                           |
| `workflow_run:`               | chain after another workflow                                                                         |
| `release: types: [published]` | publish artifacts on release                                                                         |

Set `permissions:` at workflow/job level; default grants too much. Start `contents: read`, grant more per job (e.g. `id-token: write` for OIDC).

## Pinning — by SHA, not tag

Tags are mutable (a maintainer or attacker re-points `v4` at malicious code). Pin actions by full commit SHA with a comment showing the version: `- uses: actions/checkout@<full-sha>   # v4.x.y`. Enable Dependabot (`.github/dependabot.yml` with `package-ecosystem: github-actions`) to keep SHAs fresh.

## Caching

`actions/setup-*` handles caching with `cache:` — prefer that. For custom paths, use `actions/cache`:

```yaml
- uses: actions/cache@<full-sha> # v4.x.y
  with:
    path: |
      ~/.cache/pip
      .venv
    key: ${{ runner.os }}-py-${{ hashFiles('**/uv.lock') }}
    restore-keys: ${{ runner.os }}-py-
```

| Language        | Key includes                                           | Path                                                    |
| --------------- | ------------------------------------------------------ | ------------------------------------------------------- |
| Node (npm/pnpm) | `hashFiles('**/package-lock.json')` / `pnpm-lock.yaml` | `~/.npm` or `~/.pnpm-store`                             |
| Python (uv/pip) | `hashFiles('**/uv.lock','**/requirements*.txt')`       | `~/.cache/pip`, `.venv`                                 |
| Go              | `hashFiles('**/go.sum')`                               | `~/go/pkg/mod`, `~/.cache/go-build`                     |
| Rust (cargo)    | `hashFiles('**/Cargo.lock')`                           | `~/.cargo`, `target/` (use `Swatinem/rust-cache@<sha>`) |
| Docker          | `cache-from: type=gha`                                 | layer-only                                              |

Cache key MUST include the lockfile hash; otherwise stale deps + cross-PR contamination. `restore-keys:` falls back to prefix match when exact key misses.

## Matrix builds

```yaml
strategy:
  fail-fast: true # cancel siblings on first failure (default; set false only for release matrices)
  matrix:
    os: [ubuntu-24.04, macos-15]
    node: [20, 22]
    include:
      - { os: ubuntu-24.04, node: 22, coverage: true } # cell-only extras
    exclude:
      - { os: macos-15, node: 20 } # skip uninteresting combos
```

**Cap the matrix.** `os × node × db × scenario` explodes; aim < 12 cells for PR jobs.

## Secrets & OIDC

```yaml
- env:
    PAT: ${{ secrets.GITHUB_TOKEN }}
    DEPLOY_KEY: ${{ secrets.DEPLOY_KEY }}
  run: |
    curl -H "Authorization: Bearer $PAT" https://api.example.com
```

Never inline secrets in `with:` or positional args (`set -x` leaks them); always via `env:`. Never `echo`/`cat`/`set -x` near a secret — GitHub auto-masks only known values. Use `environment: production` for prod deploys (required reviewers, restricted secrets). Prefer OIDC:

```yaml
permissions:
  id-token: write # required for OIDC
  contents: read
steps:
  - uses: aws-actions/configure-aws-credentials@<full-sha> # pin to a real SHA; never leave as `@main` or `@v4`
    with:
      role-to-assume: arn:aws:iam::123:role/ci-deploy
      aws-region: us-east-1 # no long-lived AWS_SECRET_ACCESS_KEY
```

Same pattern for GCP (Workload Identity Federation), Azure, Vault, npm (provenance/trusted publishers).

## Reusable workflows & composite actions

| Pattern                                        | When                                                       |
| ---------------------------------------------- | ---------------------------------------------------------- |
| **Reusable workflow** (`workflow_call`)        | shared job across repos; separate runners, own permissions |
| **Composite action** (`runs.using: composite`) | shared steps inside one job                                |

Extract shared CI to `org/.github/workflows/ci-shared.yml` and call:

```yaml
jobs:
  test:
    # path is <owner>/<repo>/<path-in-repo>: the special `.github` org-wide repo at myorg/.github
    # holds shared workflows under its own .github/workflows/, hence the doubled segment.
    uses: myorg/.github/.github/workflows/ci-shared.yml@<full-sha>
    # `secrets: inherit` passes ALL caller secrets; if the shared workflow is in another repo
    # and gets compromised, every secret leaks. Prefer an explicit allowlist:
    secrets:
      DEPLOY_KEY: ${{ secrets.DEPLOY_KEY }}
```

## `@claude` integration

Mention `@claude` in PR comments to trigger Claude on the diff. Install the Claude Code GitHub App, add `ANTHROPIC_API_KEY` to repo secrets, then:

```yaml
on:
  issue_comment:
    types: [created]
jobs:
  claude:
    # GUARDS (all required):
    #   (1) only PR comments (issue_comment fires on plain Issues too)
    #   (2) only trusted human commenters (OWNER/MEMBER/COLLABORATOR)
    #   (3) exclude GitHub Apps + bots — `[bot]` suffix is reserved for App actors;
    #       a poisoned bot comment thread otherwise gets through (2)
    if: >-
      github.event.issue.pull_request != null
      && contains(github.event.comment.body, '@claude')
      && !endsWith(github.event.comment.user.login, '[bot]')
      && (github.event.comment.author_association == 'OWNER'
          || github.event.comment.author_association == 'MEMBER'
          || github.event.comment.author_association == 'COLLABORATOR')
    runs-on: ubuntu-24.04
    permissions:
      contents: write
      pull-requests: write
    steps:
      - uses: actions/checkout@<full-sha> # pin to a real SHA
      - uses: anthropics/claude-code-action@<full-sha>
        with:
          anthropic_api_key: ${{ secrets.ANTHROPIC_API_KEY }}
```

The `if:` block is the security boundary, not the wrapper action. Pin both checkout and the Claude action by SHA.

## Anti-patterns

- `actions/checkout@v4` (tag) instead of SHA → supply-chain risk
- Secrets in `with:` or `run: echo $SECRET` → leaked in logs
- No `timeout-minutes`, no `concurrency:` group on PRs → stuck jobs + duplicate runs
- Matrix without `exclude:` → 60-cell PR run; cache key without lockfile hash → stale deps
- `permissions:` left at default; long-lived cloud secrets instead of OIDC
- `secrets: inherit` in reusable workflow calls (passes every secret); 800-line monolithic workflow files
- `pull_request_target` on user-controlled paths or without strict file-path filters

## Red flags

| Thought                                                       | Reality                                                                  |
| ------------------------------------------------------------- | ------------------------------------------------------------------------ |
| "Tag is fine, who hijacks actions?"                           | `tj-actions/changed-files` (2025). Pin SHAs.                             |
| "`pull_request_target` is the way to get secrets in fork PRs" | It's also the way to leak them. Read GitHub's fork-poisoning docs first. |
| "Matrix is cheap"                                             | 12 cells × 8 min × 50 PRs/day = 80 CI hours/day.                         |
| "We'll cache later"                                           | Cold installs make every PR 5 min slower. Cache on day 1.                |

## Hand-off

GitLab equivalents: `Skill(ci-gitlab-ci)`. Secret-scanning + dep-pinning beyond actions (SBOM, Sigstore): `Skill(security)`.
