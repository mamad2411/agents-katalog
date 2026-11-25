---
name: golden-path-template-validation-and-testing
description: >
  Tests that a golden-path scaffolding template actually produces a
  working, deployable service — a CI pipeline that scaffolds a real
  instance, builds it, deploys it to an ephemeral environment, and runs a
  smoke test — before the template is published broadly or promoted to
  the default. Use when a user asks to "test a golden-path template before
  publishing it," "add CI for our Backstage scaffolder templates," "canary
  a new template version," "prove a template actually works end-to-end,"
  or "catch a broken golden path before teams start scaffolding from it."
license: Apache-2.0
compatibility: "Claude Code, GitHub Copilot, OpenAI Codex, Cursor, Gemini CLI"
metadata:
  domain: internal-developer-platform
  maturity: stable
---

# Golden Path Template Validation and Testing

## Purpose

A golden-path template that looks correct in review — valid YAML, sensible
parameters, a plausible skeleton — can still produce a service that
doesn't build, doesn't pass its own CI, or fails to deploy, because nobody
actually ran the template end-to-end before publishing it. The cost of
skipping this is not abstract: the first team to discover a broken golden
path is a real team trying to ship a real service, and the damage isn't
just their lost afternoon — it's the platform's credibility with every
team watching, at the exact moment adoption depends on the golden path
visibly working. This skill covers the validation discipline that belongs
between designing a template (covered in
[golden-path-template-design-for-developer-platforms](../golden-path-template-design-for-developer-platforms/SKILL.md))
and pointing new-service creation at it: a CI pipeline that scaffolds a
real instance from the template, builds it, deploys it to an ephemeral
environment, runs a smoke test, and tears it down — repeated for every
tier and, ideally, every supported parameter combination that's actually
shipped as a tested option.

## When to use

- A golden-path template (or a new tier of one) is about to be published
  or made the default choice for new-service creation, and nobody has
  verified end-to-end that scaffolding from it produces something that
  actually builds and deploys.
- A change to an existing template (a runtime version bump, a new default
  datastore, an updated CI skeleton) needs to be verified before it
  silently affects every service scaffolded after the merge.
- A team reports that a service scaffolded from the golden path didn't
  build/deploy correctly, and the platform team needs a repeatable way to
  reproduce and catch that class of failure earlier next time.
- Deciding how to roll out a template version change gradually (canary a
  new default to a subset of new-service creations) instead of flipping
  every team over at once.
- Setting up ongoing (not just pre-publish) validation so a template that
  worked at publish time doesn't silently rot as its dependencies age.

## Prerequisites & environment

- The templating substrate already in place — Backstage Scaffolder
  (`scaffolder.backstage.io/v1beta3` `Template` manifests) or a Score-based
  skeleton workflow; see
  [golden-path-template-design-for-developer-platforms](../golden-path-template-design-for-developer-platforms/SKILL.md)
  for the template structure this skill validates.
- CI runner capacity and permissions to: check out a freshly scaffolded
  repository, run its build, push a throwaway image to a registry, and
  deploy to an ephemeral namespace/environment — this is a real,
  if short-lived, deploy, not a dry parse of the template's YAML.
- An ephemeral deploy target dedicated to template testing (a
  `template-ci` Kubernetes namespace, or a disposable Humanitec/Score
  Environment) with a teardown mechanism (TTL-based namespace cleanup, or
  an explicit teardown CI job) so failed test runs don't accumulate
  orphaned infrastructure.
- A registry/catalog cleanup policy for the throwaway repositories and
  catalog entries this pipeline creates on every run (e.g. a `-template-ci-`
  naming prefix the cleanup job matches on, or a scheduled deletion job).
- A smoke-test convention every skeleton commits to — at minimum, a
  health endpoint (`/healthz` or equivalent) the pipeline can curl after
  deploy — otherwise "the service deployed" and "the service works" are
  conflated.

## Step-by-step guidance

1. **Scaffold a real instance from the template in CI**, driven the same
   way a developer would trigger it, not by hand-copying the skeleton.
   For Backstage, call the Scaffolder's own execution API rather than
   reimplementing template rendering:
   ```yaml
   # .github/workflows/validate-golden-path.yml
   name: Validate golden-path template
   on:
     pull_request:
       paths: ["templates/golden-path-service-standard/**"]
     schedule:
       - cron: "0 6 * * 1"   # weekly, to catch dependency rot even with no template change
   jobs:
     scaffold-build-deploy-smoketest:
       runs-on: ubuntu-latest
       steps:
         - name: Trigger scaffold via Backstage API
           run: |
             curl -X POST "$BACKSTAGE_URL/api/scaffolder/v2/tasks" \
               -H "Authorization: Bearer $BACKSTAGE_TOKEN" \
               -H "Content-Type: application/json" \
               -d '{
                 "templateRef": "template:default/golden-path-service-standard",
                 "values": {
                   "name": "template-ci-standard-'"${GITHUB_RUN_ID}"'",
                   "owner": "group:platform-team",
                   "runtime": "go1.22",
                   "datastore": "postgres14"
                 }
               }' > task.json
             echo "task_id=$(jq -r .id task.json)" >> "$GITHUB_ENV"
   ```

2. **Poll the scaffolder task to completion** and fail fast on a scaffold
   error, rather than proceeding to build a repository that was never
   fully created:
   ```bash
   until [[ "$(curl -s -H "Authorization: Bearer $BACKSTAGE_TOKEN" \
     "$BACKSTAGE_URL/api/scaffolder/v2/tasks/$task_id" | jq -r .status)" =~ ^(completed|failed)$ ]]; do
     sleep 5
   done
   status=$(curl -s -H "Authorization: Bearer $BACKSTAGE_TOKEN" \
     "$BACKSTAGE_URL/api/scaffolder/v2/tasks/$task_id" | jq -r .status)
   [[ "$status" == "completed" ]] || { echo "Scaffold failed"; exit 1; }
   ```

3. **Check out the freshly generated repository and run its own build**,
   exactly as the generated CI pipeline would — a template can render
   syntactically valid files that still don't compile, especially after a
   runtime-version bump:
   ```bash
   git clone "https://github.com/acme-corp/template-ci-standard-${GITHUB_RUN_ID}.git"
   cd "template-ci-standard-${GITHUB_RUN_ID}"
   docker build -t "template-ci:${GITHUB_RUN_ID}" .
   ```
   A failure here is the single most valuable signal this pipeline
   produces — it means the template renders something that doesn't even
   build, the sharpest form of "the golden path is broken."

4. **Deploy the built artifact to an ephemeral environment**, using
   whatever deploy mechanism the golden path itself wires in (this proves
   the generated deploy config works, not just the generated code):
   ```bash
   score-compose generate score.yaml -o compose.yaml
   docker compose -f compose.yaml up -d
   # or, for a Humanitec-backed golden path:
   humctl score deploy --app "template-ci-standard-${GITHUB_RUN_ID}" \
     --env template-ci --file score.yaml
   ```

5. **Run a real smoke test against the deployed instance**, not just a
   "the deploy command exited 0" check — hit the health endpoint and
   assert a real response:
   ```bash
   for i in $(seq 1 30); do
     code=$(curl -s -o /dev/null -w "%{http_code}" http://localhost:8080/healthz)
     [[ "$code" == "200" ]] && break
     sleep 2
   done
   [[ "$code" == "200" ]] || { echo "Smoke test failed: /healthz returned $code"; exit 1; }
   ```

6. **Tear down every resource this pipeline created**, on both success and
   failure paths, so a template-validation run never leaves an orphaned
   repository, catalog entry, or ephemeral deploy behind:
   ```bash
   docker compose -f compose.yaml down -v
   gh repo delete "acme-corp/template-ci-standard-${GITHUB_RUN_ID}" --yes
   ```
   Run teardown in a workflow `if: always()` step (GitHub Actions) or
   equivalent `after_script`/`finally` block, not only on the happy path —
   a failed smoke test that skips cleanup is exactly the run most likely
   to need re-investigation later, and an accumulating pile of
   `template-ci-*` repos/namespaces erodes trust in the pipeline itself.

7. **Run the full pipeline for every tier the template ships**, not just
   the one being changed — a change to a shared skeleton fragment (a
   common CI include, a shared Dockerfile base) can break a tier the PR
   author wasn't testing:
   ```yaml
   strategy:
     matrix:
       template: [golden-path-service-minimal, golden-path-service-standard, golden-path-service-advanced]
   ```

8. **Canary a template version change** before making it the default
   surfaced to every team — publish the new version under a distinct
   `metadata.name`/version tag, route a small subset of new-service
   requests (or a designated pilot team) to it first, and only flip the
   default once it has both passed this pipeline and produced at least
   one real, developer-scaffolded service without incident:
   ```yaml
   metadata:
     name: golden-path-service-standard
     annotations:
       idp.acme.com/template-version: "3.0.0-canary"
   ```
   This mirrors a canary release of application code — the same
   discipline, applied to the thing that produces services rather than a
   single service.

## Best practices

- Treat "the template renders" and "the template produces a working
  service" as two different claims requiring two different tests — schema/
  lint validation on the `Template` manifest catches the first, this
  skill's scaffold-build-deploy-smoke-test pipeline catches the second.
- Run this pipeline on a schedule (weekly, at minimum), not only on
  template PRs — a template with zero changes can still break when an
  upstream base image, runtime version, or dependency it pulls in drifts,
  and the first sign shouldn't be a developer's failed scaffold.
- Name every artifact this pipeline creates with a clearly identifiable,
  greppable prefix (`template-ci-*`) so cleanup, monitoring, and incident
  triage can all distinguish real services from validation runs at a
  glance.
- Make teardown unconditional (`if: always()`), not just a happy-path step
  — a validation pipeline that leaks resources on failure creates exactly
  the kind of untracked infrastructure a golden path is supposed to
  prevent.
- Version and canary template changes the same way a stream-aligned team
  would canary a risky application release — a template's "users" are
  every team who scaffolds from it, and a bad default deserves the same
  rollback discipline as a bad production deploy.
- Keep the smoke test meaningful (a real endpoint returning a real
  response), matching the same guidance given for `ValidateService` hooks
  in deployment pipelines generally — a smoke test that only checks the
  process started catches almost nothing.

## Common pitfalls

- **Symptom:** A template change passes code review (the diff looks
  reasonable) and is merged, but the next three teams who scaffold from it
  all hit the same build failure.
  **Fix:** Code review of a template's diff doesn't prove the rendered
  output builds — add the scaffold-build-deploy-smoke-test pipeline
  (steps 1–5) as a required check on template PRs, not just human review
  of the templating logic.

- **Symptom:** The validation pipeline is set up but only runs the
  `golden-path-service-standard` tier, and a shared skeleton fragment
  change silently breaks `golden-path-service-advanced` for months before
  anyone scaffolds from it and notices.
  **Fix:** Run the pipeline as a matrix across every published tier (step
  7), not just the tier a given PR appears to touch — shared fragments
  make cross-tier breakage easy to introduce without realizing it.

- **Symptom:** A new template version is made the default for all new
  services the same day it's merged, and a subtle issue (a
  misconfigured default resource limit) affects a dozen newly scaffolded
  services before anyone notices the pattern.
  **Fix:** Canary the version (step 8) — route a small number of
  scaffolds or a single pilot team to the new version first, and only
  promote it to the default after both the automated pipeline and at
  least one real developer-scaffolded service confirm it end-to-end.

- **Symptom:** The validation pipeline's ephemeral deploys and throwaway
  repositories accumulate in the cloud account and catalog over months,
  and nobody notices until a cost review flags dozens of unexplained
  `template-ci-*` resources.
  **Fix:** Make teardown (step 6) unconditional and add a scheduled
  sweep job matching the pipeline's naming convention as a backstop for
  any run where even the `if: always()` teardown itself failed (e.g. the
  runner was killed mid-job).

- **Symptom:** The smoke test only checks that the deploy command exited
  successfully, and a service that deploys but crash-loops immediately
  after is reported by the pipeline as "passed."
  **Fix:** Replace an exit-code-only check with an actual health-endpoint
  poll (step 5) with a real timeout and a real HTTP status assertion —
  "the deploy command succeeded" and "the service is actually serving
  traffic" are different facts, and only the second one matters to a
  developer relying on the golden path.

## Worked example

**Scenario:** The platform team is about to bump
`golden-path-service-standard`'s default Go runtime from `go1.21` to
`go1.22` and wants to verify this doesn't break anything before it becomes
the default every new Go service gets.

1. The change is opened as a PR against the templates repo, bumping the
   `runtime` parameter's `default` and the skeleton's `go.mod`/Dockerfile
   base image tag.
2. The PR triggers `validate-golden-path.yml`, which scaffolds
   `template-ci-standard-48213` from the *changed* template ref, using
   `runtime: go1.22` explicitly (not relying on the default alone, to test
   the exact value being changed).
3. `docker build` on the generated repository succeeds — the Dockerfile's
   base image update is compatible with the generated `go.mod`.
4. `score-compose generate` and `docker compose up` deploy it locally in
   the CI runner; the smoke test polls `/healthz` and gets `200` within
   4 seconds.
5. Teardown removes the throwaway GitHub repo and stops the compose stack,
   `if: always()`.
6. The matrix also runs `golden-path-service-minimal` and
   `golden-path-service-advanced` against the same runtime bump — both
   pass, confirming the shared Go-runtime skeleton fragment they inherit
   from wasn't broken by the change.
7. Rather than merging directly to the default, the platform team tags
   the change `golden-path-service-standard@3.1.0-canary`, asks one pilot
   team (`fraud-detection`) to explicitly opt into it for their next new
   service, and monitors that scaffold for a week before flipping
   `golden-path-service-standard`'s published default to `3.1.0`.

## Cross-references

- [golden-path-template-design-for-developer-platforms](../golden-path-template-design-for-developer-platforms/SKILL.md) — the tiering, parameterization, and versioning design this pipeline validates; read that first for the template structure being tested here.
- [humanitec-score-configuration-validation](../humanitec-score-configuration-validation/SKILL.md) — the equivalent validation discipline for a single Score workload spec, used inside step 4/5 when the golden path's deploy mechanism is Score-based.
- [idp-adoption-rollout-and-change-management-strategy](../idp-adoption-rollout-and-change-management-strategy/SKILL.md) — how the canary/pilot sequencing in step 8 fits into the platform's broader rollout and change-management approach.
