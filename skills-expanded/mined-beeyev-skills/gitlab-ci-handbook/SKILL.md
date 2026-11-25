---
name: gitlab-ci-handbook
description: >-
  GitLab CI/CD knowledge base (GitLab 18+). Use whenever the user asks
  about, needs an explanation of, writes, reviews, optimizes, or debugs
  GitLab pipelines or .gitlab-ci.yml files:
  stages, jobs, rules and workflows, includes and templates, caching and
  artifacts, child and downstream pipelines, environments
  and deployments, or bash scripts running inside CI jobs, even if they
  only mention "pipeline" or "CI" in a GitLab context. Covers pipeline
  structure and refactoring, large or unreadable pipeline graphs, CI/CD
  best practices, debugging failed pipelines, CI security, and DevOps
  automation on GitLab.
license: MIT
metadata:
  author: Alexander Tebiev
  source: https://github.com/beeyev/skills
  homepage: https://github.com/beeyev/skills/tree/master/skills/gitlab-ci-handbook
  version: "1.3.0"
  category: devops
  keywords: >-
    gitlab, gitlab-ci, gitlab-ci.yml, ci-cd, continuous-integration,
    continuous-deployment, pipeline, pipelines, devops, gitlab-runner,
    caching, artifacts, docker, deployment, automation, yaml, bash,
    security, debugging
---

# GitLab CI Handbook

Curated GitLab CI/CD guidance, verified against GitLab 18.x. This file is
a router. Select the task bundle first and read every required reference
before acting. Then add topic references for the configuration under
review. When a reference points to another file for a safety or
correctness constraint, read that file too. Do not load unrelated files.

## Baseline

- Guidance targets GitLab 18+, Free tier, Linux runners, bash. Paid-tier
  or executor-specific requirements are flagged inline where they apply.
- For syntax not covered here, or when in doubt, check the official docs
  instead of guessing: keyword reference https://docs.gitlab.com/ci/yaml/,
  versioned archive https://archives.docs.gitlab.com/.

## Task bundles

File names in this table live under `references/`.

| Task | Read before acting |
|---|---|
| Focused question or explanation | The matching topic owner from Routing, plus every safety or correctness reference it names |
| Create a complete pipeline | `pipeline-structure.md`, `pipeline-selection.md`, `data-flow.md`, `execution-environment.md`, `bash-in-ci.md`, `security.md` |
| Add or modify a job | `pipeline-selection.md`, then every topic owner from Routing that matches the changed keywords; read `bash-in-ci.md` when adding or changing commands |
| Full review or audit | `pipeline-structure.md`, `pipeline-selection.md`, `data-flow.md`, `execution-environment.md`, `security.md`, `bash-in-ci.md`, and the validation section in `orchestration.md`; add `readability.md`, `informative-logging.md`, `developer-experience.md`, and `pipeline-ui.md` when reviewing maintainability, diagnostics, or graph navigability |
| Pipeline or job missing | `debugging.md`, `pipeline-selection.md`, and the validation section in `orchestration.md` |
| Runner, image, service, or pre-script failure | `debugging.md`, `execution-environment.md`; add `security.md` for authentication, protected resources, or runner trust |
| Script failure | `debugging.md`, `bash-in-ci.md`; add `data-flow.md` for cache, artifact, report, or dependency-transfer failures |
| Optimize a pipeline | `data-flow.md`, `execution-environment.md`, `orchestration.md`, `pipeline-selection.md` |
| Pipeline graph or UI is too large | `pipeline-ui.md`, `readability.md`; add `orchestration.md` for child pipelines or matrices, `pipeline-selection.md` when reducing conditional topology, and `data-flow.md` before changing `needs` |
| Deploy or environment work | `execution-environment.md`, `pipeline-selection.md`, `security.md` |
| Components or includes | `pipeline-structure.md`, `security.md`, and the validation section in `orchestration.md` |
| Downstream, child, or matrix pipeline | `orchestration.md`, `data-flow.md`, `pipeline-selection.md` |

## Routing

| Read | When the task involves |
|---|---|
| `references/pipeline-structure.md` | Creating or restructuring `.gitlab-ci.yml`; refactoring an oversized pipeline file safely; splitting config with `include`; CI/CD components (`include:component`), authoring and consuming them; `extends` vs anchors vs `!reference`; `default:` and hidden `.base` jobs; `spec:inputs`; repo layout for CI files; config merge/override questions |
| `references/pipeline-selection.md` | Which pipelines and jobs run: `workflow:rules`, job `rules`, `rules:changes` (symptoms: duplicate pipelines, job runs twice, job not triggering); reusable rule sets; tag release pipelines; scheduled jobs; manual gates; `only`/`except` deprecation |
| `references/data-flow.md` | Caching and cache keys, policies, misses; artifacts and reports; passing outputs between jobs; DAGs with `needs`; test sharding; checkout strategy (`GIT_DEPTH`); making a pipeline faster (measurement method and anti-patterns) |
| `references/execution-environment.md` | Runners and `tags:`; executors; choosing and pinning job images; private registry auth; sidecar `services:` (databases for integration tests); Docker image builds (dind); environments, review apps, `resource_group`; GitLab Pages |
| `references/orchestration.md` | Parent-child and multi-project pipelines; dynamic child pipelines; matrices (`parallel:matrix`); auto-cancel and retries (`interruptible`, `retry`); timeout budgeting; validating compiled configuration (CI Lint, `merged_yaml`, validation levels) |
| `references/pipeline-ui.md` | Pipeline graphs that are too wide, tall, dense, or slow to navigate; stage vs job-dependency views; mini graphs; grouped jobs; downstream cards; choosing native GitLab structure that keeps large pipelines understandable |
| `references/security.md` | Secrets storage and variable hygiene; fork MR pipelines; `CI_JOB_TOKEN` and its allowlist; OIDC `id_tokens` for cloud auth; runner isolation (privileged, shell executor); auditing third-party CI code |
| `references/debugging.md` | A failing or missing pipeline or job with a concrete symptom: error-text lookup, debug-in-runner-order, empty-variable confusions, predefined-variable traps |
| `references/bash-in-ci.md` | Writing or fixing `script:` / `before_script:` / `after_script:`; inline YAML vs `scripts/*.sh` decisions; `set -Eeuo pipefail`; required-env-var checks; quoting; shellcheck; why a multiline block didn't fail; how the runner executes commands |
| `references/readability.md` | Naming jobs, stages, variables, or CI files; commenting style; making a pipeline navigable for newcomers |
| `references/informative-logging.md` | What jobs should echo (versions, decisions) and must never echo (secrets); collapsible log sections; variable masking behavior |
| `references/developer-experience.md` | Designing pipelines whose failures are debuggable: `workflow:name` pipeline titles; job execution headers; actionable failure messages; surfacing test reports and artifact links in MRs; diagnostic artifacts; reproducing CI failures locally |

Secrets questions span two files: log exposure and masking in
`informative-logging.md`, storage, tokens, and the wider threat model in
`security.md`. Read both.

## Rules of engagement

When writing pipeline YAML or CI bash for a user:

1. Follow the structure rules (no god YAML, but don't over-decompose
   tiny pipelines): `pipeline-structure.md`.
2. Extract bash to `scripts/ci/*.sh` when the criteria in
   `bash-in-ci.md` say so; short wiring stays inline, it is a balance,
   not extraction by default. Default extracted scripts to
   `set -Eeuo pipefail`; deviate when the script deliberately handles
   those conditions. Use intent-revealing names: `bash-in-ci.md`,
   `readability.md`.
3. For a complete pipeline, define `workflow:rules` deliberately to
   prevent duplicate or unintended pipeline types; the verified pattern
   is in `pipeline-selection.md`. Do not replace an existing workflow
   when the user only asked for a job or config fragment.
4. Prefer a verified pattern from the pattern files
   (`pipeline-selection.md`, `data-flow.md`, `execution-environment.md`,
   `orchestration.md`) over inventing one; adapt names and rules to the
   project.
5. If available, validate generated config before handing it over, and
   say which level was reached (levels and their limits: end of
   `orchestration.md`). GitLab CI Lint for GitLab semantics,
   `shellcheck` for shell scripts. `yamllint` and `gitlab-ci-local` are
   useful local checks, but they do not prove GitLab will compile the
   same pipeline.

When modifying an existing pipeline:

6. Read the root file and every `include:local` file before touching
   anything; the pipeline is their merge, not the root file.
7. Match the project's conventions even when this handbook prefers
   otherwise: their `rules:` idioms (or legacy `only`/`except`, noting
   the deprecation in passing), their `.base-*` jobs, their naming and
   stage layout. Do not re-declare what `default:` already provides.
   In-repo consistency beats handbook preference for a small change;
   migrations are their own MR.
8. Make focused additions in the file where that domain lives; do not
   rewrite or reformat surrounding config. Extending `stages:` or
   `workflow:` is a separate, called-out change.
9. When asked to make a pipeline faster: measure first, change one
   bottleneck per round, report absolute numbers. Method and
   anti-patterns: end of `data-flow.md`.
