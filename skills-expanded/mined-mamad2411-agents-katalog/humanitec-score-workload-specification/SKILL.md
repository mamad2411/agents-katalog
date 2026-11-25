---
name: humanitec-score-workload-specification
description: >
  Authors platform-agnostic workload specifications using the Score open
  standard (score.dev) and wires them into Humanitec's Platform Orchestrator
  for environment-specific resource binding. Use when the user asks to
  "write a score.yaml," "define a Score workload," "set up Humanitec
  resource definitions," "make deployments platform-agnostic with Score,"
  or "deploy the same workload spec to dev/staging/prod without changing
  the app config."
license: Apache-2.0
compatibility: "Claude Code, GitHub Copilot, OpenAI Codex, Cursor, Gemini CLI"
metadata:
  domain: internal-developer-platform
  maturity: stable
---

# Humanitec Score Workload Specification

## Purpose

Application teams shouldn't need to know whether "staging" runs on a shared
Postgres RDS instance, a per-namespace CloudSQL database, or a local Docker
container — but without a shared abstraction, every environment difference
leaks into the app's deployment config, and every platform migration means
rewriting every service's manifests. Score (an open, vendor-neutral
specification at score.dev) solves this by letting a developer declare a
workload's containers and *abstract* resource dependencies (`postgres`,
`route`, `dns`) once, in a single `score.yaml`, without naming a concrete
cloud service; a separate implementation — `score-compose` for local
Docker Compose, `score-k8s` for plain Kubernetes, or Humanitec's Platform
Orchestrator for full environment-aware provisioning — resolves those
abstract resources into real infrastructure per target. This skill covers
writing a correct `score.yaml` and understanding how Humanitec's Resource
Definitions and Environments turn that same file into different concrete
infrastructure across dev/staging/prod.

## When to use

- Writing a new `score.yaml` for a service that needs to run identically
  (from the app team's perspective) across local dev, CI, and multiple
  cloud environments.
- Migrating a service's deployment config off environment-specific
  Kubernetes manifests or Helm values files and onto a portable Score spec.
- Setting up a Humanitec Resource Definition so an abstract `resources`
  entry in `score.yaml` (e.g. `type: postgres`) resolves to a real
  Terraform-provisioned database in a given environment.
- Explaining why the same `score.yaml` produces a local container on a
  laptop (`score-compose`), a plain Deployment/Service on a personal k8s
  cluster (`score-k8s`), and a fully wired cloud database + DNS record in
  production (Humanitec).
- Onboarding a new environment (e.g. a second region, or a new `staging-eu`)
  without asking every app team to change their workload spec.

## Prerequisites & environment

- The Score spec itself is implementation-agnostic; pin to a specific
  `apiVersion` (`score.dev/v1b1` is the current stable schema version as
  of this writing — check score.dev for the latest before assuming a
  newer `v1b2`/GA version hasn't shipped).
- For local resolution: `score-compose` (Docker Compose target) or
  `score-k8s` (plain Kubernetes target), both open-source CLIs maintained
  under the Score project — install via the project's release binaries or
  `brew install score-spec/tap/score-compose`.
- For Humanitec-orchestrated environments: a Humanitec organization, at
  least one Application and Environment created, `humctl` CLI installed
  and authenticated (`humctl login`), and an API token
  (`HUMANITEC_TOKEN`) scoped to the target Application.
- Resource Definitions for every abstract resource `type`/`class`
  combination the `score.yaml` references must already exist in the
  target Humanitec Environment — this is an operator/platform-team
  responsibility, not something the app team's `score.yaml` can create.
- A container registry the target environment can pull from, and image
  tags produced by the existing CI pipeline (Score references an `image`
  by tag/digest, it doesn't build one).

## Step-by-step guidance

1. **Write the workload's basic shape**: `apiVersion`, `metadata.name`, and
   one or more `containers` with an image reference, environment
   variables, and resource requests/limits:
   ```yaml
   apiVersion: score.dev/v1b1
   metadata:
     name: checkout-api
   containers:
     checkout-api:
       image: registry.example.com/checkout-api:1.4.2
       variables:
         LOG_LEVEL: info
         DB_CONNECTION: "${resources.db.connection}"
       resources:
         requests:
           cpu: "250m"
           memory: "256Mi"
         limits:
           cpu: "1"
           memory: "512Mi"
       files:
         - target: /etc/checkout-api/config.yaml
           content: |
             feature_flags:
               new_pricing: false
   ```
   `variables` values can reference `resources.<name>.<field>` — Score
   substitutes these at resolution time from whatever the target
   implementation actually provisions, which is the mechanism that keeps
   the file itself environment-agnostic.

2. **Declare abstract resources by `type`, not by concrete vendor** — this
   is the core of Score's portability:
   ```yaml
   resources:
     db:
       type: postgres
       params:
         version: "15"
     dns:
       type: dns
       params:
         host: "checkout.example.com"
     route:
       type: route
       params:
         host: "${resources.dns.host}"
         port: 8080
     cache:
       type: volume
   ```
   Nothing here says "RDS" or "CloudSQL" — the `postgres` type is resolved
   differently by each implementation: `score-compose` spins up a local
   `postgres` container, while Humanitec matches `type: postgres` (and
   optionally a `class`) against a Resource Definition bound in the
   current Environment.

3. **Validate and run locally with `score-compose`** before anything
   touches a real environment:
   ```bash
   score-compose init
   score-compose generate score.yaml -o compose.yaml
   docker compose -f compose.yaml up
   ```
   `score-compose generate` fails fast on a malformed spec (missing
   required fields, unknown resource `type` it doesn't have a built-in
   provisioner for) — this is the cheapest validation loop, run before any
   CI or Humanitec deploy.

4. **Run the same file against plain Kubernetes with `score-k8s`** for a
   team not using Humanitec at all:
   ```bash
   score-k8s generate score.yaml -o manifests.yaml
   kubectl apply -f manifests.yaml -n checkout
   ```
   `score-k8s` resolves `postgres`/`route`/etc. using its own default
   provisioners (e.g. a `postgres` resource becomes a StatefulSet + Service
   in-cluster) — good for teams who want Score's portability without
   adopting Humanitec's orchestration layer.

5. **Deploy through Humanitec with `humctl score deploy`**, which uploads
   the Score spec and creates a deployment against a specific
   Application/Environment:
   ```bash
   humctl score deploy \
     --app checkout \
     --env staging \
     --file score.yaml
   ```
   Humanitec resolves each `resources.*` entry against the Resource
   Definitions bound to the `staging` Environment, not the ones bound to
   `production` — same `score.yaml`, different concrete infrastructure.

6. **Define the Humanitec Resource Definition that resolves `type:
   postgres`** to a real Terraform module, scoped per environment type:
   ```yaml
   apiVersion: entity.humanitec.io/v1b1
   kind: Definition
   metadata:
     id: postgres-aws-rds
   entity:
     type: postgres
     driver_type: humanitec/terraform
     driver_inputs:
       source:
         path: "git::https://github.com/<ORG>/tf-modules//postgres-rds"
       variables:
         instance_class: "db.t3.medium"
         engine_version: "15"
   ```
   In `staging`, bind this Resource Definition with a smaller
   `instance_class`; in `production`, bind a different Resource Definition
   (or the same one with a larger override) — the app team's `score.yaml`
   never changes.

7. **Bind Resource Definitions per Environment**, not globally, so `dev`
   can resolve `postgres` to a lightweight container-based Postgres while
   `production` resolves the same `type` to RDS Multi-AZ:
   ```bash
   humctl score resources apply \
     --env dev \
     --res-def postgres-dev-local
   humctl score resources apply \
     --env production \
     --res-def postgres-aws-rds-multiaz
   ```
   This environment-level binding — not anything in `score.yaml` — is what
   makes the same workload spec produce a throwaway dev database and a
   production-grade Multi-AZ instance from identical application code.

8. **Reference dynamically resolved values back into the container**, e.g.
   a DB connection string Humanitec only knows after provisioning
   completes, using Score's `${resources.<name>.<output>}` interpolation
   shown in step 1 — never hardcode a host/port/credential into
   `variables` directly.

## Best practices

- Declare resources by their smallest sufficient `type` (`postgres`, not a
  vendor-specific type name) so the same spec stays portable across
  `score-compose`, `score-k8s`, and Humanitec — pushing vendor specificity
  into the Resource Definition, not the `score.yaml`.
- Pin `apiVersion` explicitly and check it into the same PR review as the
  application code — a `score.yaml` schema change (e.g. a new required
  container field between spec minor versions) should go through the same
  review as any other deployment-affecting change.
- Never hardcode secrets or connection strings into `containers.*.variables`
  — reference `${resources.<name>.*}` and let the Resource
  Definition/provisioner inject the real value (e.g. from a secret store)
  at resolution time, never at authoring time.
- Keep one `score.yaml` per deployable workload, not one shared across
  multiple services with conditional logic — Score intentionally has no
  templating/conditionals; if multiple services need different shapes,
  give each its own file (or generate them from a golden-path template,
  see cross-references).
- Test locally with `score-compose` before every Humanitec deploy, even to
  a low-risk `dev` environment — it catches schema errors in seconds
  without touching real infrastructure or waiting on a Terraform apply.
- Version Resource Definitions the same way as application code (in git,
  reviewed via PR) — a Resource Definition is platform-team-owned
  infrastructure-as-code, not a one-off console click, and a bad module
  reference in one Resource Definition can break every workload in an
  Environment that resolves to it.
- Keep the number of distinct resource `type`/`class` combinations a
  platform actually supports small and documented — an app team writing
  `type: mystery-queue` with no matching Resource Definition anywhere
  fails only at deploy time, not at authoring time (see pitfalls and the
  companion validation skill).

## Common pitfalls

- **Symptom:** `humctl score deploy` succeeds against `staging` but fails
  against `production` with "no resource definition matches type=postgres,
  class=default" even though the `score.yaml` is unchanged.
  **Fix:** The `production` Environment has no Resource Definition bound
  for that `type`/`class` combination — bindings are per-Environment, not
  global; confirm with `humctl score resources list --env production`
  before assuming the workload spec itself is broken.

- **Symptom:** A developer hardcodes `DB_HOST: postgres-prod.internal` into
  `containers.checkout-api.variables` "just to get it working," defeating
  the entire point of the abstract `resources` block.
  **Fix:** Replace with `${resources.db.host}` and let whichever
  implementation resolves the spec (Humanitec, `score-k8s`, or
  `score-compose`) inject the real value — a hardcoded host is invisible
  to Score and will silently point at the wrong environment's database the
  next time the same file is deployed elsewhere.

- **Symptom:** `score-compose generate` and `score-k8s generate` both
  produce working output for the same `score.yaml`, but the file fails
  validation only when submitted to Humanitec.
  **Fix:** Humanitec enforces additional constraints beyond the base Score
  schema (e.g. that every `resources.*.type` has a bound Resource
  Definition in the target Environment) that the open-source CLIs, which
  ship their own built-in default provisioners, don't need to enforce —
  run `humctl score deploy --dry-run` (or the org's CI validation gate; see
  [humanitec-score-configuration-validation](../humanitec-score-configuration-validation/SKILL.md))
  against the actual target Environment, not just local resolution, before
  assuming the spec is deploy-ready everywhere.

- **Symptom:** Two services end up with near-duplicate `score.yaml` files
  that differ only in `metadata.name` and `image`, and a shared config bug
  (e.g. missing `resources.requests`) has to be fixed in a dozen places.
  **Fix:** Generate `score.yaml` from a shared golden-path template with
  parameterized fields, rather than hand-copying between services — see
  [golden-path-template-design-for-developer-platforms](../golden-path-template-design-for-developer-platforms/SKILL.md).

- **Symptom:** A Resource Definition change (e.g. bumping the Terraform
  module's `instance_class` default) is applied directly against
  `production` and every workload resolving `type: postgres` there gets an
  unplanned resize on next deploy.
  **Fix:** Test Resource Definition changes against a non-production
  Environment's resource graph first and gate the change through review,
  the same as any other infrastructure-as-code change — see
  [humanitec-score-configuration-validation](../humanitec-score-configuration-validation/SKILL.md)
  for the dry-run/Resource Graph workflow.

## Worked example

**Scenario:** The `checkout-api` service needs to run identically (from the
app team's point of view) in a developer's local Docker environment, a
shared `staging` environment, and `production`, where `staging` uses a
small shared RDS instance and `production` uses Multi-AZ RDS with read
replicas — without the app team maintaining three different manifests.

`score.yaml` (single file, used everywhere):
```yaml
apiVersion: score.dev/v1b1
metadata:
  name: checkout-api
containers:
  checkout-api:
    image: registry.example.com/checkout-api:1.4.2
    variables:
      DB_CONNECTION: "${resources.db.connection}"
      LOG_LEVEL: info
    resources:
      requests: { cpu: "250m", memory: "256Mi" }
      limits: { cpu: "1", memory: "512Mi" }
resources:
  db:
    type: postgres
    params:
      version: "15"
  route:
    type: route
    params:
      host: checkout.example.com
      port: 8080
```

Local dev: `score-compose generate score.yaml -o compose.yaml && docker
compose -f compose.yaml up` — resolves `db` to a local `postgres:15`
container with no Humanitec involvement at all.

Staging deploy: `humctl score deploy --app checkout --env staging --file
score.yaml` — Humanitec resolves `type: postgres` against the
`postgres-staging-shared` Resource Definition (a small shared RDS
instance, `db.t3.small`, provisioned once and reused across services in
staging).

Production deploy: identical command with `--env production` — Humanitec
resolves the *same* `type: postgres` entry against
`postgres-production-multiaz` (RDS Multi-AZ, `db.r5.large`, with automated
failover), because that's the Resource Definition bound to the
`production` Environment. The app team changed nothing between the three
deploys; only the platform team's Environment-level Resource Definition
bindings differ.

## Cross-references

- [humanitec-score-configuration-validation](../humanitec-score-configuration-validation/SKILL.md) — validating this `score.yaml` and its target Resource Definitions before a real deploy, referenced above for dry-run/CI gating.
- [platform-self-service-api-and-workflow-design](../platform-self-service-api-and-workflow-design/SKILL.md) — Score as the developer-facing spec inside a larger self-service provisioning workflow.
- [golden-path-template-design-for-developer-platforms](../golden-path-template-design-for-developer-platforms/SKILL.md) — embedding a pre-filled, parameterized `score.yaml` in a scaffolding template so new services start from a correct spec instead of hand-copying one.
