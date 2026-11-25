---
name: humanitec-score-configuration-validation
description: >
  Validates Score workload specifications and Humanitec Resource Definitions
  before they reach a real deploy — schema validation, `--dry-run` resolution
  against a target Environment, policy checks on resource types/classes, and
  Resource Graph diffing for infrastructure-affecting changes. Use when a
  user asks to "validate a score.yaml before deploying," "check a Resource
  Definition change won't break production," "add a CI gate for Score specs,"
  "dry-run a Humanitec deploy," or "catch a missing Resource Definition
  before a developer's deploy fails."
license: Apache-2.0
compatibility: "Claude Code, GitHub Copilot, OpenAI Codex, Cursor, Gemini CLI"
metadata:
  domain: internal-developer-platform
  maturity: stable
---

# Humanitec Score Configuration Validation

## Purpose

A `score.yaml` that passes local `score-compose generate` can still fail —
or worse, silently misbehave — the moment it's deployed through Humanitec,
because Humanitec enforces constraints the open-source Score CLIs don't:
every abstract `resources.*.type`/`class` must resolve against a Resource
Definition actually bound to the target Environment, and a Resource
Definition change can alter what every workload referencing that `type`
provisions on its next deploy. Catching these problems at CI time — before
a developer's `humctl score deploy` fails in front of them, or before a
platform-team Resource Definition edit silently resizes every production
database — is what separates a validation gate from "we'll find out when
someone complains." This skill covers the validation layer that sits in
front of the authoring practices in
[humanitec-score-workload-specification](../humanitec-score-workload-specification/SKILL.md):
schema/lint checks, dry-run resolution, policy checks on resource
types/classes, and Resource Graph diffing for Resource Definition changes.

## When to use

- Adding a CI gate that validates every `score.yaml` change in a pull
  request before it merges, not just before it deploys.
- A developer's `humctl score deploy` fails against a specific Environment
  with a resource-resolution error, and the goal is to catch that class of
  failure earlier, in CI, for the next developer.
- A platform engineer is about to change a Resource Definition (e.g. bump a
  Terraform module version or a default `instance_class`) and needs to know
  which live workloads/Environments it will affect before applying it.
- Enforcing organizational policy on Score specs — e.g. "no workload may
  request `type: postgres` without `params.version` pinned," or "no
  container may run without `resources.limits` set."
- Setting up a pre-production Environment specifically for dry-running
  Score deploys before they reach staging or production.

## Prerequisites & environment

- `humctl` CLI installed and authenticated (`humctl login`), with an API
  token (`HUMANITEC_TOKEN`) scoped to at least read access on the
  Application/Environment being validated against.
- The Score JSON Schema (published at score.dev, versioned alongside the
  `apiVersion` the org has standardized on) for local/CI schema validation
  ahead of any Humanitec-specific call.
- `score-compose` and/or `score-k8s` installed for the fast, no-network
  first validation pass described in
  [humanitec-score-workload-specification](../humanitec-score-workload-specification/SKILL.md).
- A policy engine for org-specific rules beyond the base schema — Conftest
  (Open Policy Agent) is the common choice for checking YAML/JSON against
  Rego policies in CI; see
  [opa-gatekeeper-policy-authoring](../../../policy-and-governance-tooling/skills/opa-gatekeeper-policy-authoring/SKILL.md)
  for Rego authoring if the org already runs Gatekeeper for Kubernetes
  admission and wants to reuse the same policy language.
- A non-production Humanitec Environment (e.g. `ci-validate`) with a full
  set of Resource Definitions bound, dedicated to dry-run validation so CI
  checks don't need write access to `staging`/`production`.
- CI runner network access to the Humanitec API (`api.humanitec.io` or the
  org's private-cloud equivalent).

## Step-by-step guidance

1. **Validate schema shape first, locally, before any network call.**
   `score-compose generate` (or a standalone JSON Schema validator against
   the published Score schema) catches malformed YAML, missing required
   fields, and unknown top-level keys in milliseconds:
   ```bash
   score-compose generate score.yaml -o /dev/null
   echo "exit code: $?"
   ```
   A non-zero exit here means the file is malformed independent of any
   Humanitec-specific concern — fix this before running anything else.

2. **Add a CI job that runs schema validation on every pull request
   touching `score.yaml`**, so a broken spec never reaches review as
   "looks fine" (GitHub Actions example; the same job model applies to
   GitLab CI/Jenkins with equivalent syntax):
   ```yaml
   # .github/workflows/validate-score.yml
   name: Validate Score spec
   on:
     pull_request:
       paths: ["score.yaml"]
   jobs:
     validate:
       runs-on: ubuntu-latest
       steps:
         - uses: actions/checkout@v4
         - name: Install score-compose
           run: |
             curl -Lo score-compose.tar.gz \
               https://github.com/score-spec/score-compose/releases/latest/download/score-compose_linux_amd64.tar.gz
             tar -xzf score-compose.tar.gz
             sudo mv score-compose /usr/local/bin/
         - name: Validate schema
           run: score-compose generate score.yaml -o /dev/null
   ```

3. **Add org-specific policy checks with Conftest/Rego** for rules the base
   Score schema can't express — e.g. requiring resource limits, or banning
   an unpinned datastore version:
   ```rego
   # policy/score.rego
   package main

   deny[msg] {
     container := input.containers[name]
     not container.resources.limits
     msg := sprintf("container '%s' has no resources.limits set", [name])
   }

   deny[msg] {
     res := input.resources[name]
     res.type == "postgres"
     not res.params.version
     msg := sprintf("resource '%s' (type postgres) has no params.version pinned", [name])
   }
   ```
   ```bash
   conftest test score.yaml --policy policy/
   ```
   This runs in the same CI job as step 2, after schema validation passes
   — a spec can be schema-valid and still violate organizational policy.

4. **Dry-run resolve against the real target Environment**, which is the
   only way to catch a missing Resource Definition binding before a real
   deploy attempt:
   ```bash
   humctl score deploy \
     --app checkout \
     --env ci-validate \
     --file score.yaml \
     --dry-run
   ```
   `--dry-run` resolves every `resources.*` entry against Resource
   Definitions bound to `ci-validate` without provisioning or deploying
   anything — an error here (`no resource definition matches type=X,
   class=Y`) means the target Environment (or, more likely, `staging`/
   `production` with the same gap) has no binding for that resource, which
   `score-compose generate` alone would never catch.

5. **Before promoting a workload's first deploy to `staging`/`production`**,
   dry-run against those specific Environments too, not only
   `ci-validate` — Resource Definition bindings are per-Environment (see
   [humanitec-score-workload-specification](../humanitec-score-workload-specification/SKILL.md)),
   so a spec validating clean against `ci-validate` says nothing about
   whether `production` has the matching binding:
   ```bash
   humctl score deploy --app checkout --env production --file score.yaml --dry-run
   ```

6. **Before changing a Resource Definition, diff its Resource Graph impact**
   rather than editing and applying blind. List which Applications/
   Environments currently resolve the `type`/`class` you're about to
   change:
   ```bash
   humctl score resources list --env production --res-def postgres-aws-rds
   ```
   Every Application/Environment pair returned is a workload that will be
   affected the next time it deploys (or immediately, for Resource
   Definitions that reconcile continuously rather than only on deploy) —
   review that list before merging the Resource Definition change, the
   same review discipline as a database migration's blast radius.

7. **Gate the Resource Definition change itself through the same CI
   pipeline** — Resource Definitions are Terraform-driver YAML, so run
   `terraform validate`/`terraform plan` against the referenced module in
   CI before the Definition change merges, catching a broken module
   reference or an invalid variable before it becomes every workload's
   next-deploy failure:
   ```bash
   cd tf-modules/postgres-rds
   terraform init -backend=false
   terraform validate
   ```

8. **Fail the pipeline loudly and specifically**, echoing which check
   failed (schema, policy, or dry-run resolution) rather than a single
   generic "validation failed" — the fix differs completely depending on
   which layer caught the problem, and a developer debugging a failed CI
   check needs to know which one to look at first.

## Best practices

- Run checks in increasing cost/specificity order — local schema
  validation (milliseconds, no network) before policy checks (still
  local) before a Humanitec dry-run (a real API call against a real
  Environment) — so the fast, free checks catch the common case before
  paying for the expensive one.
- Keep a dedicated `ci-validate` Environment with a full set of Resource
  Definitions bound, separate from `staging`, so schema/dry-run checks in
  CI never need write credentials to an Environment real traffic depends
  on.
- Treat a Resource Definition change exactly like a schema migration: list
  affected workloads first (step 6), review the list, then merge — never
  edit-and-apply directly against `production`.
- Version-pin the Score JSON Schema and the Conftest policy bundle the
  same way application dependencies are pinned — an unpinned "latest"
  schema silently changing what's valid is its own source of CI flakiness.
- Make policy failures (step 3) point to the specific Rego rule and offending
  field, not just "policy check failed" — a developer fixing a violation
  needs to know which container or resource entry to change.
- Re-run the dry-run validation (step 4/5) as a required status check on
  the pull request, not a manual pre-merge ritual someone might skip under
  deadline pressure.

## Common pitfalls

- **Symptom:** `score-compose generate` and the Conftest policy check both
  pass in CI, but `humctl score deploy` still fails against `production`
  with "no resource definition matches type=redis, class=default."
  **Fix:** Schema and policy validation only check the shape/content of
  `score.yaml` itself — they say nothing about what's bound in a specific
  Environment. Add a dry-run step (step 4/5) against every Environment the
  spec will actually deploy to, not just schema/policy checks, as a
  required part of the same CI gate.

- **Symptom:** A platform engineer bumps a Resource Definition's Terraform
  module version to pick up a security patch, and a dozen unrelated
  services get an unplanned schema migration or connection-string change
  on their next deploy.
  **Fix:** Run `humctl score resources list --env <env> --res-def <id>`
  before merging any Resource Definition change to see every affected
  Application/Environment, and treat that list as required review context
  — the same discipline as checking a shared library's consumers before
  changing its public interface.

- **Symptom:** A `score.yaml` validates cleanly in every environment but a
  developer discovers weeks later that a required `resources.limits` was
  never actually enforced — half the fleet has no CPU/memory limits set.
  **Fix:** The base Score schema doesn't require resource limits; that's
  an organizational policy, not a spec requirement. Add it as an explicit
  Conftest/Rego rule (step 3) and make the CI job fail on it, rather than
  assuming schema-valid implies policy-compliant.

- **Symptom:** The CI validation job passes on a feature branch, but the
  same `score.yaml` fails during the actual `humctl score deploy` a
  developer runs from their laptop hours later.
  **Fix:** Confirm the CI job's `humctl` context (`HUMANITEC_TOKEN`,
  target Environment) matches exactly what the developer's local deploy
  targets — a CI dry-run against `ci-validate` doesn't guarantee
  `staging`/`production` has the same Resource Definition bindings; add
  environment-specific dry-run checks (step 5) rather than validating
  once and assuming it covers every target.

- **Symptom:** A Resource Definition's Terraform module reference is
  updated to a branch name (e.g. `//postgres-rds?ref=feature-branch`)
  instead of a tag, and it silently changes behavior when that branch is
  later force-pushed.
  **Fix:** Pin Resource Definition `source.path` module references to an
  immutable tag or commit SHA, and add a Conftest/Rego rule (or a
  pre-commit check) rejecting a `ref=` value that isn't a semver tag —
  treat this the same as pinning any other infrastructure-as-code module
  dependency.

## Worked example

**Scenario:** The `checkout-api` team submits a pull request adding a new
`resources.cache` entry (`type: redis`) to their `score.yaml`, targeting
`production`. The platform team wants this caught in CI before it reaches
a real deploy attempt, and also wants to know the blast radius before
changing the existing `postgres-aws-rds` Resource Definition to bump
`engine_version` for a CVE fix.

1. The PR's CI workflow runs `score-compose generate score.yaml -o
   /dev/null` — passes; the spec is schema-valid.
2. `conftest test score.yaml --policy policy/` runs next and fails:
   ```
   FAIL - score.yaml - resource 'cache' (type postgres) has no params.version pinned
   ```
   Wait — the rule fired on `cache`, not `db`, because the developer
   copy-pasted the `postgres` type by mistake instead of `redis`. This is
   exactly the class of error dry-run resolution wouldn't have caught
   either (it would have simply failed to find a `postgres`-class
   Definition matching whatever `class` was implied, with a less specific
   error). The developer fixes the `type` field to `redis` and the
   Conftest check now passes.
3. `humctl score deploy --app checkout --env ci-validate --file score.yaml
   --dry-run` runs and fails:
   ```
   Error: no resource definition matches type=redis, class=default
   ```
   The platform team adds a `redis-ci-validate` Resource Definition bound
   to `ci-validate` (and, separately, confirms `production` already has a
   `redis-aws-elasticache` Definition bound). Dry-run now passes against
   both `ci-validate` and `production`.
4. Separately, before bumping `postgres-aws-rds`'s `engine_version`, the
   platform engineer runs `humctl score resources list --env production
   --res-def postgres-aws-rds` and gets back 14 Applications — including
   `checkout-api`. They open the Resource Definition change as its own PR,
   list those 14 services in the description, and route it through the
   same review as any shared infrastructure change, rather than merging it
   alongside the `checkout-api` cache addition.

## Cross-references

- [humanitec-score-workload-specification](../humanitec-score-workload-specification/SKILL.md) — the `score.yaml` authoring practices and Resource Definition binding model this validation layer checks against.
- [golden-path-template-validation-and-testing](../golden-path-template-validation-and-testing/SKILL.md) — the equivalent end-to-end validation discipline applied to golden-path scaffolding templates rather than a single Score spec.
- [opa-gatekeeper-policy-authoring](../../../policy-and-governance-tooling/skills/opa-gatekeeper-policy-authoring/SKILL.md) — Rego policy-authoring detail if the org wants to share policy logic between Score-spec validation and Kubernetes admission control.
