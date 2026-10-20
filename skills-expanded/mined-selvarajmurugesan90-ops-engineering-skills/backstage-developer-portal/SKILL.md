---
name: backstage-developer-portal
description: >
  Guides building an internal developer portal with Backstage — authoring
  catalog-info.yaml to register services in the software catalog, setting
  up TechDocs for docs-as-code, writing Software Templates to scaffold
  new services, and understanding the plugin architecture. Use when a
  user asks to "register a service in Backstage", "write a catalog-
  info.yaml", "set up TechDocs", "create a Backstage software template
  for scaffolding new repos", "add a Backstage plugin", or "build an
  internal developer portal."
license: Apache-2.0
compatibility: "Claude Code, GitHub Copilot, OpenAI Codex, Cursor, Gemini CLI"
metadata:
  domain: observability-and-platform-extras
  maturity: stable
---

# Backstage Developer Portal

## Purpose

As an organization grows past a handful of services, "which team owns
this repo," "what's the on-call runbook for this API," and "what's the
standard way to spin up a new service" stop being answerable by asking
around and start requiring a system of record. Backstage (a CNCF
graduated project originated at Spotify) provides that system: a
**software catalog** where every service, API, and resource is described
by a `catalog-info.yaml` and rendered with ownership, links, and
relationships; **TechDocs** for versioned, docs-as-code documentation
rendered from Markdown living next to the code it describes; **Software
Templates** that scaffold new services from a golden-path template
instead of copy-pasting an existing repo; and a **plugin architecture**
that lets the portal surface CI status, cost, on-call, and security
posture from other tools in one place. The operational payoff is
concrete: faster onboarding (a new engineer can self-serve "how do I
create a new service" instead of asking a senior engineer), and clearer
ownership (an incident responder can find the owning team and runbook
for any service without a tribal-knowledge lookup) — but only if the
catalog stays accurate, which means catalog registration must be
enforced as part of the service creation path, not left as an optional
afterthought.

## When to use

- Registering a new or existing service, API, or resource in the
  Backstage software catalog.
- Setting up TechDocs so a repo's Markdown documentation renders inside
  the portal, versioned alongside the code.
- Writing a Software Template so new services are scaffolded from a
  golden path (standard CI config, standard Dockerfile, standard
  catalog registration) instead of manual copy-paste.
- Adding or evaluating a Backstage plugin (CI/CD status, cost insight,
  security scorecards, on-call/incident data) to surface more signal in
  the portal.
- Auditing catalog accuracy/ownership coverage — finding services with
  no registered owner, stale `lifecycle`, or missing links.
- Deciding what belongs in the catalog as a `Component` vs. an `API`
  vs. a `Resource`, or how to model relationships (`dependsOn`,
  `providesApis`) between them.

## Prerequisites & environment

- A running Backstage instance (self-hosted, deployed via the
  `@backstage/create-app` scaffold and typically run in Kubernetes/on a
  container platform) — Backstage is a framework you deploy and extend,
  not a SaaS product; budget for ongoing app maintenance (Node.js/
  TypeScript upgrades, plugin version compatibility) as part of adopting
  it.
- A source-control integration configured (GitHub App, GitLab
  integration, or Bitbucket) so the catalog can discover
  `catalog-info.yaml` files across repos and TechDocs can pull
  Markdown from them.
- A catalog discovery mechanism decided up front: either a
  `catalog.locations` static list of repos, or (preferred at scale) a
  `Location`/discovery processor that scans an org for
  `catalog-info.yaml` files automatically so registration isn't a
  manual per-repo portal-admin task.
- TechDocs requires a documentation generator (MkDocs is the default)
  and a storage backend for generated static sites (local disk for
  dev, cloud object storage — S3/GCS/Azure Blob — for production).
- Software Templates require the Scaffolder plugin (bundled by
  default) and write access (via the source-control integration's
  credentials) to create new repositories in the target
  organization/group.
- An ownership model already agreed (teams/groups defined as catalog
  `Group` entities) before rolling out mandatory catalog registration —
  registering a service with no valid `owner` reference is a common
  early failure mode.

## Step-by-step guidance

1. **Author a `catalog-info.yaml` for an existing service** and commit
   it to the service's repo root:
   ```yaml
   apiVersion: backstage.io/v1alpha1
   kind: Component
   metadata:
     name: payments-api
     description: Handles payment authorization and settlement
     annotations:
       github.com/project-slug: acme-corp/payments-api
       backstage.io/techdocs-ref: dir:.
     tags:
       - payments
       - java
     links:
       - url: https://runbooks.internal/payments-api
         title: On-call runbook
   spec:
     type: service
     lifecycle: production
     owner: group:payments-team
     system: payments
     providesApis:
       - payments-api-rest
     dependsOn:
       - resource:payments-db
   ```

2. **Register the corresponding `API` entity** if the service exposes
   one, so consumers can discover it and its contract:
   ```yaml
   apiVersion: backstage.io/v1alpha1
   kind: API
   metadata:
     name: payments-api-rest
     description: REST API for payment authorization
   spec:
     type: openapi
     lifecycle: production
     owner: group:payments-team
     definition:
       $text: ./openapi.yaml
   ```

3. **Model ownership as `Group` entities**, not free-text owner names,
   so relationships (which humans are on which team) are queryable:
   ```yaml
   apiVersion: backstage.io/v1alpha1
   kind: Group
   metadata:
     name: payments-team
   spec:
     type: team
     children: []
     members:
       - jane.doe
       - alex.smith
   ```

4. **Wire up catalog discovery** so new `catalog-info.yaml` files are
   picked up without manual portal-admin steps, in `app-config.yaml`:
   ```yaml
   catalog:
     providers:
       github:
         acmeCorpOrg:
           organization: 'acme-corp'
           catalogPath: '/catalog-info.yaml'
           schedule:
             frequency: { minutes: 30 }
             timeout: { minutes: 3 }
   ```

5. **Enable TechDocs** for a service by adding an `mkdocs.yml` and a
   `docs/` folder to the repo alongside `catalog-info.yaml`
   (`backstage.io/techdocs-ref: dir:.` already points at it):
   ```yaml
   # mkdocs.yml
   site_name: 'Payments API'
   nav:
     - Home: index.md
     - Architecture: architecture.md
     - Runbook: runbook.md
   plugins:
     - techdocs-core
   ```
   Configure the TechDocs backend to publish generated sites to cloud
   storage in production rather than local disk:
   ```yaml
   techdocs:
     builder: 'external'    # generate in CI, not on-demand in the portal
     publisher:
       type: 'awsS3'
       awsS3:
         bucketName: '<TECHDOCS_BUCKET>'
   ```
   Generating docs in CI (`techdocs-cli generate`) rather than
   on-demand in the running Backstage instance keeps the portal
   responsive and avoids running arbitrary repo-provided build steps
   inside the portal's own runtime.

6. **Write a Software Template** so new services are scaffolded
   consistently instead of copy-pasted:
   ```yaml
   apiVersion: scaffolder.backstage.io/v1beta3
   kind: Template
   metadata:
     name: golden-path-service
     title: New Backend Service (Golden Path)
     description: Scaffolds a new service with standard CI, Dockerfile, and catalog registration
   spec:
     owner: group:platform-team
     type: service
     parameters:
       - title: Service details
         required: [name, owner]
         properties:
           name:
             title: Service name
             type: string
           owner:
             title: Owning team
             type: string
     steps:
       - id: fetch
         name: Fetch golden-path skeleton
         action: fetch:template
         input:
           url: ./skeleton
           values:
             name: '${{ parameters.name }}'
             owner: '${{ parameters.owner }}'
       - id: publish
         name: Create repository
         action: publish:github
         input:
           repoUrl: 'github.com?owner=acme-corp&repo=${{ parameters.name }}'
       - id: register
         name: Register in catalog
         action: catalog:register
         input:
           repoContentsUrl: '${{ steps.publish.output.repoContentsUrl }}'
           catalogInfoPath: '/catalog-info.yaml'
     output:
       links:
         - title: Repository
           url: '${{ steps.publish.output.remoteUrl }}'
   ```
   The `skeleton/` directory (referenced by `fetch:template`) contains
   the actual golden-path files (Dockerfile, CI pipeline config,
   pre-filled `catalog-info.yaml`) with Nunjucks-style `${{ values.* }}`
   placeholders — this is what makes every scaffolded service arrive
   already registered in the catalog, not registered as an afterthought.

7. **Add a plugin to surface external signal** in the portal, e.g. the
   Kubernetes plugin (shows live pod/deployment status for a
   `Component`) or a cost-insights plugin fed by the same allocation
   data used for Kubernetes showback:
   ```yaml
   # catalog-info.yaml annotation wiring a Component to its cluster resources
   metadata:
     annotations:
       backstage.io/kubernetes-id: payments-api
   ```

8. **Enforce catalog registration in the golden path**, not as an
   optional step: require `catalog-info.yaml` presence as a CI check
   (or a required file in the Software Template output) so new
   services can't ship without being discoverable in the portal.

## Best practices

- **Model ownership as `Group` entities with real membership**, not a
  free-text `owner: "payments-team"` string with no corresponding
  `Group` — orphaned owner references silently break catalog
  relationship views (who's on this team, what does this team own).
- **Generate TechDocs in CI, not on-demand inside the running
  Backstage instance**, for both performance and security — on-demand
  generation runs arbitrary repo-provided build steps inside the
  portal's runtime.
- **Enforce catalog registration as part of the golden path** (a CI
  check requiring `catalog-info.yaml`, or built into the Software
  Template output) rather than a best-effort ask — a catalog that's
  only 60% populated is worse than no catalog, since engineers stop
  trusting it as the source of truth.
- **Use `system` and `dependsOn`/`providesApis` relationships**, not
  just flat `Component` entities, so the catalog can answer "what
  breaks if this API goes down" rather than only "what exists."
- **Keep Software Templates thin wrappers around a skeleton repo**, not
  a monolithic template with deeply nested conditional logic — a
  skeleton that's just files with placeholders is far easier for
  other engineers to maintain than a complex scaffolder action
  pipeline.
- **Version-pin Backstage core and plugin packages together** and
  upgrade deliberately — Backstage ships frequent releases, and
  mismatched core/plugin versions are a common source of breakage.
- **Treat the catalog as read-mostly by humans, write-mostly by CI/
  automation** (discovery processors, Software Template registration)
  — manual catalog edits through the UI drift from what's actually true
  in the repos.

## Common pitfalls

- **Symptom:** A service shows up in the catalog with `owner:
  unknown` or a broken owner reference, and nobody can tell who's
  responsible for it during an incident.
  **Fix:** The `catalog-info.yaml`'s `spec.owner` references a group
  that was never registered as a `Group` entity, or uses a free-text
  name instead of `group:<name>`/`user:<name>` entity-reference syntax.
  Register the `Group` entity first, then reference it correctly.

- **Symptom:** TechDocs pages show stale content, or fail to render
  entirely with a build error visible only in the portal's server
  logs.
  **Fix:** Docs were being generated on-demand inside the Backstage
  instance (`techdocs.builder: 'local'`) and a repo's `mkdocs.yml`/
  Markdown had a build error, or the generated site was never
  published anywhere durable. Switch to `builder: 'external'`,
  generate in CI with `techdocs-cli generate`, and publish to cloud
  storage so builds are visible in CI logs and independent of the
  portal's own uptime.

- **Symptom:** Catalog discovery is enabled, but a newly created repo's
  `catalog-info.yaml` never appears in the portal.
  **Fix:** The discovery processor's schedule hasn't run yet (default
  intervals can be 30+ minutes), or the file isn't at the expected
  `catalogPath`, or the GitHub App/integration lacks read access to the
  new repo (e.g. it's in an org the integration wasn't granted access
  to). Check the discovery processor's schedule and confirm the
  integration's access scope includes the repo.

- **Symptom:** A Software Template successfully creates a new
  repository, but the service never appears in the catalog.
  **Fix:** The template's steps ended at `publish:github` without a
  `catalog:register` step, so the new `catalog-info.yaml` exists in
  the repo but was never registered with the running catalog. Add the
  `catalog:register` action (step 6) as the template's final step so
  scaffolding and registration always happen together.

- **Symptom:** Engineers stop trusting the catalog and start asking
  around again instead of checking Backstage.
  **Fix:** Catalog registration was optional and coverage drifted well
  below 100% of active services, so the catalog frequently doesn't
  have the answer. Make registration mandatory in the golden path
  (a CI gate requiring `catalog-info.yaml`) and run a periodic audit
  for services missing from the catalog (cross-reference the source-
  control org's repo list against registered `Component`s).

## Worked example

**Scenario:** A platform team is rolling out Backstage for a 40-team
engineering org. Today, "who owns this service" and "how do I spin up a
new one" are answered by asking in Slack, and there's no central
documentation index.

1. Deploy Backstage via `@backstage/create-app`, configure the GitHub
   integration, and enable the GitHub discovery provider (step 4)
   scanning the `acme-corp` org every 30 minutes for
   `catalog-info.yaml` files.
2. Register the org's team structure as `Group` entities first (step
   3), since every subsequent `Component`'s `owner` field depends on
   these existing.
3. Backfill `catalog-info.yaml` for the 15 most critical existing
   services manually (step 1-2), prioritized by the incident-response
   team's list of "services we get paged for" — this seeds the catalog
   with the highest-value entries before chasing full coverage.
4. Set up TechDocs (step 5) for those same 15 services, generating in
   CI and publishing to an S3 bucket, so each service's on-call runbook
   and architecture doc is discoverable from its catalog entry.
5. Build the `golden-path-service` Software Template (step 6) wrapping
   the platform team's existing standard CI pipeline and Dockerfile,
   with `catalog:register` as the final step so every newly scaffolded
   service is catalog-registered by construction.
6. Add a CI check across the org's repos requiring a `catalog-info.yaml`
   at the root for any repo tagged `production` (step 8), giving teams
   a 60-day grace period to backfill before the check becomes blocking.
7. After rollout, add the Kubernetes plugin (step 7) so each
   `Component`'s catalog page shows live pod status, closing the loop
   between "who owns this" and "is it healthy right now" in one place.

## Cross-references

- [prometheus-and-grafana-monitoring-stack](../prometheus-and-grafana-monitoring-stack/SKILL.md)
- [kubecost-cost-visibility](../kubecost-cost-visibility/SKILL.md)
