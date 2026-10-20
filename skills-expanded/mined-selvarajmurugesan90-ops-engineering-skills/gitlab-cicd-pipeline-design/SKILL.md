---
name: gitlab-cicd-pipeline-design
description: >
  Authors and troubleshoots .gitlab-ci.yml pipelines — stages, the
  modern rules: syntax (and legacy only/except), includes for shared
  templates, and GitLab-specific runner/executor configuration. Use when
  the user asks to "write a .gitlab-ci.yml," "fix a GitLab pipeline rule
  that isn't triggering," "add a shared CI template with include," "set up
  a GitLab runner," or "convert only/except rules to the rules: syntax."
license: Apache-2.0
compatibility: "Claude Code, GitHub Copilot, OpenAI Codex, Cursor, Gemini CLI"
metadata:
  domain: cicd-tooling
  maturity: stable
---

# GitLab CI/CD Pipeline Design

## Purpose

GitLab CI/CD pipelines are defined entirely in one file, `.gitlab-ci.yml`,
executed by GitLab Runners (shared, group, or project-specific) against a
`stages:`/`rules:` model that differs in specifics from GitHub Actions or
Jenkins even though the underlying pipeline concepts overlap (see
[ci-cd-pipeline-design](../../../devops/skills/ci-cd-pipeline-design/SKILL.md)
for the vendor-neutral version). This skill covers GitLab-specific
mechanics: the `stages:`/`rules:` trigger model (and why `rules:` has
superseded the legacy `only:`/`except:`), `include:` for sharing pipeline
templates across projects, and runner/executor configuration
specifics.

## When to use

- A project needs its first `.gitlab-ci.yml`, or an existing one has a
  job that isn't running (or runs) when expected.
- Migrating legacy `only:`/`except:` job keywords to the modern `rules:`
  syntax.
- Sharing pipeline logic across multiple projects via `include:` (local,
  project, remote, or template includes) rather than duplicating YAML.
- Diagnosing why a job is stuck `pending` (no runner picks it up) or fails
  only on certain runners.
- Designing merge-request pipelines (`merge_request_event`) alongside
  branch/tag pipelines without running both redundantly on the same
  commit.

## Prerequisites & environment

- GitLab 15+ recommended: the `rules:` keyword and modern `workflow:`
  block are fully mature from GitLab 13+, but 15+ is assumed here for
  current defaults and deprecation warnings around `only:`/`except:`.
- At least one available GitLab Runner registered against the project,
  group, or instance, with an executor type understood (`shell`, `docker`,
  `docker+machine`, `kubernetes`) — job `tags:` must match a runner's
  configured tags or the job stays `pending` forever.
- Project or group maintainer access to configure CI/CD variables
  (**Settings → CI/CD → Variables**, marked "Protected"/"Masked" as
  appropriate) and to register runners.
- For `include:` of remote/template files: network access from the GitLab
  instance to the include source (for `include: remote:`), or access to
  the referenced project (for `include: project:`).

## Step-by-step guidance

1. **Declare `stages:` explicitly** — job execution order follows stage
   order, and jobs within the same stage run in parallel by default:
   ```yaml
   stages:
     - lint
     - test
     - build
     - deploy
   ```

2. **Use `workflow:` to control whether a pipeline runs at all**, before
   worrying about individual job rules — this avoids running duplicate
   pipelines for the same commit (once as a branch pipeline, once as a
   merge-request pipeline):
   ```yaml
   workflow:
     rules:
       - if: '$CI_PIPELINE_SOURCE == "merge_request_event"'
       - if: '$CI_COMMIT_BRANCH == "main"'
       - if: '$CI_COMMIT_TAG'
   ```

3. **Use `rules:` on each job, not the legacy `only:`/`except:`.** `rules:`
   evaluates a list of conditions top-to-bottom and uses the first match,
   supporting `changes:`, `if:`, and `exists:` in combination —
   expressiveness `only:`/`except:` can't match:
   ```yaml
   deploy-staging:
     stage: deploy
     rules:
       - if: '$CI_COMMIT_BRANCH == "main"'
         changes:
           - src/**/*
     script:
       - ./deploy.sh staging
   ```
   `only:`/`except:` still parses and runs in current GitLab, but new
   pipelines should use `rules:` — it's the only mechanism that gets new
   condition types going forward, and mixing both styles in the same
   project is a common source of confusing, hard-to-predict trigger
   behavior.

4. **Use `changes:` for monorepo path filtering** so an unrelated change
   doesn't trigger a full pipeline:
   ```yaml
   test-backend:
     stage: test
     rules:
       - if: '$CI_PIPELINE_SOURCE == "merge_request_event"'
         changes:
           - backend/**/*
     script:
       - cd backend && npm ci && npm test
   ```

5. **Share pipeline templates across projects with `include:`** —
   `local` for same-repo files, `project`/`remote` for cross-repo/
   cross-instance shared templates, `template` for GitLab's built-in
   templates:
   ```yaml
   include:
     - project: 'platform/ci-templates'
       ref: 'v2.1.0'
       file: '/templates/node-service.yml'
     - local: '/.gitlab/ci/deploy.yml'
   ```
   Pin `ref:` to a tag for a `project:` include, the same versioning
   discipline as a Jenkins shared library or GitHub Actions reusable
   workflow — an unpinned `ref: main` include means every consumer's
   pipeline changes the moment the template repo's `main` branch changes.

6. **Configure caching keyed on lockfile hash**, scoped per-job or shared:
   ```yaml
   test:
     stage: test
     cache:
       key:
         files: [package-lock.json]
       paths:
         - node_modules/
     script:
       - npm ci
       - npm test
   ```

7. **Match `tags:` to actual runner capabilities** — a job with
   `tags: [docker, linux]` only runs on a runner registered with both
   tags; a mismatch leaves the job `pending` indefinitely with no error
   message beyond the pending state itself:
   ```yaml
   build:
     stage: build
     tags: [docker]
     script:
       - docker build -t myapp:$CI_COMMIT_SHORT_SHA .
   ```

8. **Gate production deploys with `environment:` and `when: manual`**,
   giving GitLab's UI a visible "play" button and (with a protected
   environment) restricting who can trigger it:
   ```yaml
   deploy-production:
     stage: deploy
     rules:
       - if: '$CI_COMMIT_BRANCH == "main"'
         when: manual
     environment:
       name: production
       url: https://app.example.com
     script:
       - ./deploy.sh production
   ```

## Best practices

- Standardize on `rules:` across the project; don't mix `only:`/`except:`
  and `rules:` in the same `.gitlab-ci.yml` — the interaction between the
  two legacy and modern mechanisms on different jobs is a frequent source
  of "why did this job run/not run" confusion.
- Set `workflow:rules` once at the top of the file to prevent duplicate
  branch + merge-request pipelines firing for the same commit, rather than
  trying to fix it job-by-job.
- Pin `include:` refs to tags for cross-project templates; treat the
  template repo like any other shared library with semantic versioning
  and a changelog.
- Use protected environments (**Settings → CI/CD → Environments**) plus
  `when: manual` together for production deploys — `when: manual` alone
  only adds a button, it doesn't restrict *who* can press it without a
  protected environment's approval rules.
- Use `needs:` to express real job dependencies within/across stages for
  a DAG-style pipeline (jobs start as soon as their specific `needs:` are
  done, not only after the whole previous stage finishes) when
  stage-by-stage sequencing is unnecessarily slow.
- Emit JUnit reports via `artifacts: reports: junit:` so failures surface
  in the merge request UI directly rather than only in job logs.

## Common pitfalls

- **Symptom:** A job that should run on merge requests runs twice — once
  as a "detached" merge request pipeline, once again as a branch pipeline
  after merge, and both look like separate, sometimes contradictory
  states in the merge request widget.
  **Fix:** Add a top-level `workflow:rules:` block that picks exactly one
  pipeline source per commit context (`merge_request_event` OR
  `$CI_COMMIT_BRANCH == "main"`), rather than letting both branch and
  merge-request pipelines trigger unconditionally.

- **Symptom:** A job sits in `pending` status indefinitely with no runner
  ever picking it up, and no clear error is shown.
  **Fix:** Check that the job's `tags:` match a registered, active
  runner's tags exactly (**Settings → CI/CD → Runners** to see available
  runners and their tags) — a job with a tag no runner advertises stays
  pending forever rather than failing loudly.

- **Symptom:** Converting `only: [main]` to `rules: - if:
  '$CI_COMMIT_BRANCH == "main"'` changes behavior unexpectedly — the job
  now also runs (or stops running) on merge request pipelines.
  **Fix:** `only:`/`except:` and `rules:` have different implicit
  defaults for pipeline source; when migrating, be explicit about which
  `CI_PIPELINE_SOURCE` values a job should match rather than assuming a
  1:1 semantic translation, and check pipeline behavior on both a branch
  push and an MR event after migrating.

- **Symptom:** A remote/project `include:` pointed at a template repo's
  `ref: main` silently changes every consuming project's pipeline the
  moment someone merges to that template repo's `main`.
  **Fix:** Pin `ref:` to a specific tag (`ref: 'v2.1.0'`) for any
  cross-project include, and roll out template changes via a version bump
  in each consumer, not a floating branch reference.

- **Symptom:** `deploy-production` has `when: manual` but any developer
  with basic project access can trigger it, bypassing an intended
  approval step.
  **Fix:** `when: manual` alone only adds a manual trigger button — pair
  it with a **protected environment** (Settings → CI/CD → Environments)
  restricted to specific users/groups/roles to actually gate *who* can
  press it, mirroring the manual-approval-gate guidance in
  [ci-cd-pipeline-design](../../../devops/skills/ci-cd-pipeline-design/SKILL.md).

## Worked example

**Scenario:** A monorepo with a `backend/` and `frontend/` directory needs
path-filtered pipelines (only test what changed), a shared lint template
pulled from a central templates project, and a manually-gated production
deploy restricted to a protected environment.

`.gitlab-ci.yml`:
```yaml
stages: [lint, test, build, deploy]

workflow:
  rules:
    - if: '$CI_PIPELINE_SOURCE == "merge_request_event"'
    - if: '$CI_COMMIT_BRANCH == "main"'

include:
  - project: 'platform/ci-templates'
    ref: 'v2.1.0'
    file: '/templates/eslint.yml'

test-backend:
  stage: test
  tags: [docker]
  rules:
    - changes:
        - backend/**/*
  cache:
    key: { files: [backend/package-lock.json] }
    paths: [backend/node_modules/]
  script:
    - cd backend && npm ci && npm test

test-frontend:
  stage: test
  tags: [docker]
  rules:
    - changes:
        - frontend/**/*
  cache:
    key: { files: [frontend/package-lock.json] }
    paths: [frontend/node_modules/]
  script:
    - cd frontend && npm ci && npm test

build-image:
  stage: build
  tags: [docker]
  rules:
    - if: '$CI_COMMIT_BRANCH == "main"'
  script:
    - docker build -t myapp:$CI_COMMIT_SHORT_SHA .

deploy-production:
  stage: deploy
  tags: [docker]
  rules:
    - if: '$CI_COMMIT_BRANCH == "main"'
      when: manual
  environment:
    name: production
    url: https://app.example.com
  script:
    - ./deploy.sh production $CI_COMMIT_SHORT_SHA
```
With `production` configured as a protected environment restricted to the
release-managers group, a change to only `frontend/` skips
`test-backend` entirely, and `deploy-production` waits for both a `main`
merge and an authorized manual trigger.

## Cross-references

- [ci-cd-pipeline-design](../../../devops/skills/ci-cd-pipeline-design/SKILL.md) — vendor-neutral stage/gate/caching concepts this file implements in GitLab's specific syntax.
- [github-actions-centralized-reusable-workflows](../github-actions-centralized-reusable-workflows/SKILL.md) — the closest GitHub Actions analog to GitLab's `include: project:` shared-template pattern.
- [secure-cicd-gates](../../../devsecops/skills/secure-cicd-gates/SKILL.md) — designing the severity/blocking policy for scan jobs added into this pipeline's stages.
