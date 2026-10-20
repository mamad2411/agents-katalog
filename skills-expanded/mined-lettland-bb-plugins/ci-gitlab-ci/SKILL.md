---
name: ci-gitlab-ci
description: Use when writing or reviewing GitLab CI pipelines — .gitlab-ci.yml structure, runners, artifacts/caches, glab CLI, headless Claude.
metadata:
  added: 2026-05-18
  last_reviewed: 2026-05-18
  type: ci
  status: active
  invokes_shell: false
  shell_reviewed: valksor 2026-05-17
  related:
    - ci-github-actions
    - security
---

# GitLab CI

**Iron Law: parent-child pipelines for monorepos. Tag runners; don't trust the default. CI variables masked AND protected for prod.**

**Base image default:** Debian (`*-slim`, `*-trixie-slim`, `distroless-debian`). Alpine only when image size dominates and you've verified musl-libc compat (cgo, glibc-only wheels, DNS resolver edge cases). Long-form rationale: `Skill(infra-docker-images)`.

## `.gitlab-ci.yml` skeleton

```yaml
stages: [build, test, deploy]

default:
  image: debian:trixie-slim
  timeout: 30m
  interruptible: true # cancel on new push to the same ref

variables:
  FF_USE_FASTZIP: "true" # faster artifact upload
  CI_DEBUG_TRACE: "false" # NEVER set true with secrets in env

workflow:
  rules: # gate the whole pipeline
    - if: $CI_PIPELINE_SOURCE == "merge_request_event"
    - if: $CI_COMMIT_BRANCH == $CI_DEFAULT_BRANCH
    - if: $CI_COMMIT_TAG

test:
  stage: test
  image: node:22-slim # Debian-slim; node:22-alpine only after musl/cgo audit
  cache:
    key: { files: [package-lock.json] }
    paths: [node_modules/]
  script: [npm ci, npm test]
  artifacts: { when: always, reports: { junit: report.xml }, expire_in: 1 week }
```

| Key                   | Meaning                                                |
| --------------------- | ------------------------------------------------------ |
| `stages:`             | sequential phases; jobs in same stage run parallel     |
| `rules:`              | replaces `only/except` (deprecated)                    |
| `needs:`              | DAG dependencies — skip stage ordering when not needed |
| `interruptible: true` | cancel when superseded — saves minutes                 |
| `dependencies:`       | which prior jobs' artifacts to download (default: all) |
| `extends:`            | YAML reuse — share base configs across jobs            |

## `rules:` (not `only/except`)

```yaml
rules:
  - if: $CI_COMMIT_BRANCH == "main"
    when: on_success
  - if: $CI_COMMIT_TAG
    when: on_success
  - if: $CI_PIPELINE_SOURCE == "merge_request_event"
    changes: ["src/**/*", "tests/**/*"]
  - when: never # explicit catch-all
```

`only:` / `except:` still work but are deprecated. Use `rules:` everywhere — composable, evaluatable, supports `changes:` (skip jobs when no relevant files moved).

## Parent-child pipelines (mandatory for monorepos)

A monolithic `.gitlab-ci.yml` for a monorepo loads slowly, runs every job on every push, and blocks the UI. Split per project:

```yaml
# .gitlab-ci.yml (parent)
include:
  - local: services/api/.gitlab-ci.yml
    rules: [{ changes: ["services/api/**/*"] }]
  - local: services/web/.gitlab-ci.yml
    rules: [{ changes: ["services/web/**/*"] }]

# Or dynamically trigger child pipelines:
api-pipeline:
  trigger:
    include:
      - artifact: services/api/generated.yml
        job: gen-api
    strategy: depend
```

`strategy: depend` makes the parent wait on child status. Without it, the parent passes the moment children are triggered.

## Runners

| Type                               | Use for                                         |
| ---------------------------------- | ----------------------------------------------- |
| Shared (gitlab.com)                | OSS, low-volume; pay per minute                 |
| Group/project specific             | Your hardware, tag-controlled                   |
| Self-managed K8s / Docker executor | Default; good isolation                         |
| Self-managed shell executor        | Last resort — runs as runner user, no isolation |

```yaml
deploy:
  tags: [aws, prod] # only runners with BOTH tags pick this up
  script: terraform apply
```

Tag everything non-generic. Untagged jobs land on `shared` runners (paid) or whichever picks first — non-deterministic.

## Artifacts vs caches

|                             | Artifact                             | Cache                                        |
| --------------------------- | ------------------------------------ | -------------------------------------------- |
| Purpose                     | Pass data between jobs in a pipeline | Speed up dependency install across pipelines |
| Stored on                   | GitLab server                        | Runner-local (or distributed cache)          |
| Lifetime                    | `expire_in` (default 30d)            | Until evicted / key changes                  |
| Auto-downloaded by next job | Yes (per `dependencies:` / `needs:`) | If key matches                               |

```yaml
build:
  artifacts: { paths: [dist/], expire_in: 1 week, when: on_success }
  cache: { key: { files: [package-lock.json] }, paths: [node_modules/], policy: pull-push }
test:
  needs: [build] # DAG — no need for stage gating
  cache: { key: { files: [package-lock.json] }, paths: [node_modules/], policy: pull }
```

`policy: pull` on downstream consumers avoids redundant upload churn.

## CI/CD variables — masked AND protected

In Settings → CI/CD → Variables, set per variable:

| Flag            | Effect                                                    |
| --------------- | --------------------------------------------------------- |
| Masked          | hidden in job logs (≥8 chars, no special chars)           |
| Protected       | only available on protected branches/tags (prod)          |
| Expand variable | `$VAR` references are expanded (off for raw secrets)      |
| File            | mounted as a file, `$VAR` is the path (kubeconfigs, keys) |

Prod secrets: masked + protected + protected branch. Without "protected", feature branches read them. Never `echo $SECRET`, `set -x`, or `CI_DEBUG_TRACE` near secrets — it dumps every variable.

## `glab` CLI (think `gh` but for GitLab)

```bash
glab auth login --hostname gitlab.com
glab mr create --title "..." --target-branch main      # also: list, view, merge, note
glab pipeline status                                    # current branch's pipeline
glab ci view                                            # interactive TUI for the pipeline
glab ci trace <job-id>                                  # stream a job's logs
glab variable set DEPLOY_KEY "..." --masked --protected
```

`glab` mirrors `gh` (`<noun> <verb>`, `--json` output, repo auto-scoped). PAT or OIDC auth.

## Headless Claude in pipelines

```yaml
claude-review:
  image: node:22-slim # Debian-slim; node:22-alpine only after musl/cgo audit
  # FORK SAFETY: fork MR pipelines also see $ANTHROPIC_API_KEY unless either
  # "Run pipelines for fork MR" is off OR the source_project filter below is applied.
  rules:
    - if: $CI_PIPELINE_SOURCE == "merge_request_event" && $CI_MERGE_REQUEST_SOURCE_PROJECT_ID == $CI_PROJECT_ID
  variables: { ANTHROPIC_API_KEY: $ANTHROPIC_API_KEY } # masked + protected
  timeout: 10m
  script:
    - npm install -g @anthropic-ai/claude-code@<exact-semver>
    # Diff-size guard: cap on BYTES (line count misses minified/generated files); also notify MR on skip so reviewers know review was skipped, not silently passed
    - git diff $CI_MERGE_REQUEST_DIFF_BASE_SHA...HEAD > diff.patch
    - BYTES=$(wc -c < diff.patch); if [ "$BYTES" -gt 250000 ]; then glab mr note $CI_MERGE_REQUEST_IID --message "AI review skipped (diff $BYTES bytes > 250 kB cap)"; exit 0; fi
    - claude -p "Review this diff. Flag bugs and security issues." < diff.patch > review.md
    - glab mr note $CI_MERGE_REQUEST_IID --message "$(cat review.md)"
```

Pin the package to an exact semver — not a range (`^`/`~`) and not `latest`. `ANTHROPIC_API_KEY` masked + protected.

## Anti-patterns

- Monolithic `.gitlab-ci.yml` for a 20-service monorepo; untagged jobs hitting wrong runner fleet
- Prod variables masked but NOT protected (feature branch reads them); `CI_DEBUG_TRACE: "true"` near secrets
- `only:`/`except:` in new code instead of `rules:`; artifacts without `expire_in`
- Cache key without lockfile hash; `dependencies:` defaulting to "all artifacts" when one job needs none
- Headless Claude without `timeout:` or diff-size cap; fork-MR pipelines without `target_project` filter

## Red flags

| Thought                            | Reality                                                                                   |
| ---------------------------------- | ----------------------------------------------------------------------------------------- |
| "Shared runners are free"          | gitlab.com gives 400 min/mo. Hit it and you pay or wait.                                  |
| "Masked is enough"                 | A feature branch can still read the value into a payload and POST it offsite. Protect it. |
| "Parent-child is overkill"         | Until your monorepo pipeline graph won't render in the UI.                                |
| "Everyone uses the default runner" | Until a shell-executor job runs unsandboxed on a build host. Tag and isolate.             |

## Hand-off

GitHub equivalents: `Skill(ci-github-actions)`. Secret scanning / SBOM / dep provenance: `Skill(security)`.
