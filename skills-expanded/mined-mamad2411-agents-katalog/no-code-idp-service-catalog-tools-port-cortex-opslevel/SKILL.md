---
name: no-code-idp-service-catalog-tools-port-cortex-opslevel
description: >
  Evaluates and configures no-code/low-code internal developer portal
  platforms — Port, Cortex, and OpsLevel — as alternatives to hand-rolling
  a Backstage instance. Use when the user asks "should we buy or build our
  internal developer portal," "Port vs Cortex vs OpsLevel," "no-code
  service catalog alternative to Backstage," "evaluate a catalog/scorecard
  SaaS tool," or wants to model a service catalog, self-service action, or
  maturity scorecard in one of these three products.
license: Apache-2.0
compatibility: "Claude Code, GitHub Copilot, OpenAI Codex, Cursor, Gemini CLI"
metadata:
  domain: internal-developer-platform
  maturity: stable
---

# No-Code IDP Service Catalog Tools: Port, Cortex, OpsLevel

## Purpose

Every platform team eventually needs a service catalog, ownership map, and
maturity scorecard — but building that on top of Backstage means owning a
Node.js/TypeScript application, its plugin ecosystem, its upgrade cadence,
and its frontend, indefinitely, with an engineering team that could
otherwise be building golden paths instead of portal infrastructure. Port,
Cortex, and OpsLevel solve the same problem as commercial, hosted products:
you model entities and rules through their UI/API/config files instead of
writing React plugins and Backstage backend modules. The operational
decision this skill supports is not "which tool has more features" but
"does our team have the in-house frontend/platform engineering capacity to
justify owning a framework, or is buying 12-18 months of catalog/scorecard
value faster and cheaper than building it" — and, once bought, how to model
the catalog and scorecards correctly in whichever product is chosen.

## When to use

- A platform team is scoping a service catalog / internal developer portal
  project and needs a genuine buy-vs-build comparison before committing
  engineering headcount.
- Someone asks specifically "Port vs Cortex vs OpsLevel" or "what's the
  difference between a Cortex scorecard and a Backstage plugin."
- A team already running Backstage is hitting the ceiling of in-house
  frontend capacity and is considering migrating catalog/scorecard
  functionality to a SaaS product.
- Modeling a new entity type, relation, or self-service provisioning action
  in Port; a `cortex.yaml` descriptor or Scorecard rule in Cortex; or a
  service descriptor, Rubric, or Check in OpsLevel.
- Assessing vendor lock-in risk before standardizing catalog metadata on
  one of these three proprietary schemas.

## Prerequisites & environment

- An organizational account with one (or a trial of each) of: Port
  (`app.getport.io`, org/workspace admin access), Cortex
  (`app.getcortexapp.com`, an API key with catalog-write scope), or
  OpsLevel (workspace admin access, an API token for `opslevel-cli` or the
  Terraform provider).
- For Cortex: the `cortex.yaml` descriptor lives in each service's repo and
  is registered via the Cortex GitHub/GitLab integration or a CI step
  calling the Cortex CLI (`cortex catalog apply`, or later CLI names as
  the CLI is renamed) or the ingestion API.
- For OpsLevel: `opslevel-cli` (or the `opslevel` Terraform provider,
  version pinned e.g. `~> 1.0`) with a workspace API token
  (`OPSLEVEL_API_TOKEN`) scoped to catalog and rubric management.
- For Port: an org-level API client (`PORT_CLIENT_ID` /
  `PORT_CLIENT_SECRET`) with permission to create Blueprints and
  Self-service Actions; a webhook endpoint, GitHub Actions workflow, or
  Kafka topic to back each self-service action's execution.
- Existing source-of-truth data (a repo list, an ownership spreadsheet, a
  CMDB export) to seed the initial catalog import — none of these tools
  discover services from nothing without at least a GitHub/GitLab org
  integration or a bulk import file.

## Step-by-step guidance

1. **Frame the decision before touching any tool.** Answer three questions
   first: (a) does the org have spare frontend/platform engineering
   capacity to build and *maintain* a Backstage instance for years, not
   just stand one up once; (b) how much of what's needed is genuinely
   bespoke logic (a custom plugin calling an internal system) versus
   generic catalog/scorecard/self-service functionality all three vendors
   already ship; (c) how many teams/services need onboarding in the first
   quarter — a SaaS tool with a hosted UI and vendor-run upgrades gets a
   catalog live in days, Backstage in weeks to months. If the answer to
   (a) is "no" and (b) is "mostly generic," buying is the operationally
   correct default.

2. **Model the catalog in Port using Blueprints and relations.** A
   Blueprint is a JSON-schema-like entity type definition; relations link
   blueprints together (e.g. a `service` belongs to a `team`):
   ```json
   {
     "identifier": "service",
     "title": "Service",
     "icon": "Microservice",
     "schema": {
       "properties": {
         "language": { "type": "string", "enum": ["go", "typescript", "python"] },
         "tier": { "type": "string", "enum": ["tier-1", "tier-2", "tier-3"] },
         "repo_url": { "type": "string", "format": "url" }
       },
       "required": ["language", "tier"]
     },
     "relations": {
       "owning_team": {
         "target": "team",
         "required": true,
         "many": false
       }
     }
   }
   ```
   Create the `team` blueprint first (identifier `team` must exist before
   `service` can declare a relation to it), then bulk-ingest entities via
   the Port API (`POST /v1/blueprints/service/entities`) from your
   existing repo/ownership data.

3. **Add a Port self-service action for a provisioning workflow**, backed
   by a GitHub Actions workflow dispatch:
   ```json
   {
     "identifier": "scaffold_new_service",
     "title": "Scaffold new service",
     "trigger": {
       "type": "self-service",
       "operation": "CREATE",
       "userInputs": {
         "properties": {
           "service_name": { "type": "string" },
           "language": { "type": "string", "enum": ["go", "typescript"] }
         },
         "required": ["service_name", "language"]
       }
     },
     "invocationMethod": {
       "type": "GITHUB",
       "org": "<GITHUB_ORG>",
       "repo": "platform-scaffolder",
       "workflow": "scaffold.yml",
       "reportWorkflowStatus": true
     }
   }
   ```
   `reportWorkflowStatus: true` streams the workflow run's success/failure
   back into Port's action run history, so a developer isn't left guessing
   whether their scaffold request actually completed.

4. **Register a service in Cortex via `cortex.yaml`** committed at the
   repo root (this is Cortex's equivalent of Backstage's
   `catalog-info.yaml`, but with scorecards as a first-class concept
   rather than a separate plugin):
   ```yaml
   openapi: 3.0.1
   info:
     x-cortex-tag: checkout-api
     x-cortex-type: service
     x-cortex-owners:
       - type: group
         name: checkout-team
     x-cortex-git:
       github:
         repository: org/checkout-api
     x-cortex-domain-parents:
       - tag: checkout-domain
     x-cortex-custom-metadata:
       language: go
       tier: "1"
   ```

5. **Define a Cortex Scorecard** as a set of YAML rules with tiered
   levels — this is what replaces a bespoke Backstage scorecard plugin:
   ```yaml
   name: Production Readiness
   description: Minimum bar for a service to run in production.
   rules:
     - title: Has an on-call rotation configured
       expression: "entity.hasPagerDutyOncall()"
       level: Bronze
       weight: 1
     - title: Has a documented runbook
       expression: "entity.hasDocument('runbook')"
       level: Silver
       weight: 2
     - title: p99 latency SLO defined and tracked
       expression: "entity.hasMetadata('slo.latency_p99_ms')"
       level: Gold
       weight: 3
   ```
   Services must pass all rules at a level (and below) to be badged at
   that level; Cortex evaluates this continuously from ingested metadata,
   not as a one-time manual audit.

6. **Populate the OpsLevel catalog via `opslevel.yml` or Terraform**, not
   manual UI entry, so the catalog is diffable and PR-reviewable like the
   `cortex.yaml`/Port-blueprint approaches above:
   ```yaml
   apiVersion: opslevel.com/v1
   kind: service
   metadata:
     name: checkout-api
   spec:
     description: Checkout and payment processing service
     lifecycle: production
     tier: tier_1
     owner: checkout-team
     tags:
       - key: language
         value: go
   ```

7. **Define OpsLevel maturity via a Rubric of Checks**, OpsLevel's
   analogue to a Cortex Scorecard:
   ```hcl
   resource "opslevel_rubric_check_has_documentation" "runbook" {
     name     = "Has a runbook"
     enabled  = true
     category = opslevel_rubric_category.production_readiness.id
     level    = opslevel_level.silver.id
     document_type    = "runbook"
     document_subtype = "markdown"
   }
   ```
   Levels (Bronze/Silver/Gold-equivalent, named per org) roll up into an
   org-wide maturity report, the same operational output as the Cortex
   scorecard above and the Port scorecard/action combination.

8. **Decide the metadata source of truth deliberately.** If the org later
   migrates vendors or adds Backstage alongside the SaaS tool, whichever
   schema (Blueprint, `cortex.yaml`, `opslevel.yml`) was chosen first
   becomes the de facto system of record — plan a one-time export/import
   path (all three expose a catalog export API) rather than assuming
   metadata portability "just works" across vendors.

## Best practices

- Treat the initial catalog population as a one-time bulk import from
  existing source control/ownership data, not a mandate for every team to
  hand-enter YAML — low initial friction is the entire value proposition
  of buying versus building.
- Keep `cortex.yaml` / `opslevel.yml` / Port entity-ingestion definitions
  in the same repo as the service they describe and apply them via CI, not
  through manual UI edits — otherwise the catalog silently drifts from
  the code it claims to describe, the same failure mode as an unmaintained
  Backstage `catalog-info.yaml`.
- Model scorecards/rubrics around outcomes the org actually enforces (an
  on-call rotation exists, an SLO is defined) rather than copying a
  vendor's example rubric verbatim — an unenforced scorecard becomes
  decoration within a quarter.
- Start self-service actions (Port) / workflows narrow and specific (e.g.
  "scaffold a Go service") rather than one generic "create anything"
  action — narrow actions have a tractable owning team and clear success
  criteria; a catch-all action accumulates unowned edge cases.
- Budget for vendor lock-in explicitly: none of these three schemas
  (Port Blueprints, `cortex.yaml`, `opslevel.yml`) are portable to each
  other or back to Backstage `catalog-info.yaml` without a translation
  script — decide this is acceptable before, not after, a year of catalog
  data accumulates in one vendor's format.
- Re-evaluate the buy decision at renewal against actual usage (how many
  teams use scorecards weekly, how many self-service actions fired last
  quarter) rather than renewing on autopilot — a SaaS catalog nobody
  consults is the same failure mode as an abandoned Backstage instance,
  just with a recurring invoice instead of a maintenance backlog.
- When bespoke plugin logic genuinely is required (a custom internal tool
  integration none of the three vendors' action/webhook model can express),
  that is the signal to reconsider Backstage for that specific capability
  — not necessarily for the whole catalog.

## Common pitfalls

- **Symptom:** Six months in, the catalog in Port/Cortex/OpsLevel has
  accurate service names but every `tier`/`owner` field is stale or
  missing for anything created after the initial bulk import.
  **Fix:** Wire catalog updates into the same CI pipeline that deploys the
  service (a CI step calling the ingestion API, or a `cortex.yaml`/
  `opslevel.yml` file the pipeline validates on every merge to main),
  so metadata changes are enforced by the same process as a code change,
  not a separate manual chore.

- **Symptom:** A team picks a SaaS catalog tool specifically because "it's
  no-code," then spends months building custom webhook relays and Lambda
  glue to replicate a Backstage plugin's behavior inside the vendor's
  self-service action model.
  **Fix:** That is a sign the actual requirement was bespoke integration
  logic, which is exactly what Backstage's plugin architecture is for —
  re-run the buy-vs-build decision for that specific capability instead of
  forcing it through a no-code action.

- **Symptom:** A Cortex Scorecard or OpsLevel Rubric shows most services
  stuck at the lowest tier indefinitely, and teams have stopped checking
  it.
  **Fix:** The rules were likely set at an unattainable bar on day one
  (e.g. requiring SLOs before any service has them) or never re-baselined;
  set the entry tier to what's realistically true today, and raise the bar
  incrementally as adoption of the next criterion actually happens — see
  [service-scorecards-and-maturity-model-design](../service-scorecards-and-maturity-model-design/SKILL.md).

- **Symptom:** Two teams register the same service twice — once via a
  Cortex GitHub integration auto-discovery and once via a manually
  committed `cortex.yaml` with a different `x-cortex-tag` — producing
  duplicate catalog entries.
  **Fix:** Pick one registration mechanism per entity type org-wide
  (auto-discovery *or* explicit descriptor file, not both) and document it
  as the platform team's convention, the same discipline required for
  Backstage `catalog-info.yaml` discovery.

- **Symptom:** A Port self-service action's GitHub Actions workflow fails
  silently from the developer's point of view — Port shows "success"
  because the workflow was *triggered*, not because it *completed*.
  **Fix:** Set `reportWorkflowStatus: true` (Port) or the equivalent
  status-callback option, and design the backing workflow to post an
  explicit failure state back to the tool rather than only relying on
  GitHub's own run status, which the catalog tool doesn't poll by default
  in every configuration.

## Worked example

**Scenario:** A 40-engineer platform team at a mid-size SaaS company is
deciding how to stand up a service catalog for 120 microservices. They have
one platform engineer with light frontend experience and no dedicated
frontend team. They need: an ownership map, a production-readiness
scorecard, and a self-service "scaffold new service" action — all live
within one quarter.

**Decision:** No in-house frontend capacity to own a Backstage instance for
years (criterion a fails) and all three needs are generic catalog/
scorecard/self-service functionality (criterion b confirms buy). They pilot
Cortex for 3 weeks against 10 pilot services.

`cortex.yaml` committed to `org/checkout-api`:
```yaml
openapi: 3.0.1
info:
  x-cortex-tag: checkout-api
  x-cortex-type: service
  x-cortex-owners:
    - type: group
      name: checkout-team
  x-cortex-git:
    github:
      repository: org/checkout-api
  x-cortex-custom-metadata:
    language: go
    tier: "1"
```

Scorecard rule added for "Production Readiness," Bronze level requiring an
on-call rotation and a `cortex.yaml` file present at all (so services with
no descriptor at all are visibly Tier-0/unscored rather than silently
absent). After the pilot, all 10 services reach Bronze within a week
because the bar was set to what already existed; Silver (runbook required)
is added in month two once every pilot team has one. The self-service
scaffold need is deferred to a simple internally-hosted `cookiecutter`
template invoked by CI for now, since Cortex's action model at evaluation
time was thinner than the Port/OpsLevel equivalents — illustrating that the
three vendors are not feature-identical and the specific gap (self-service
actions) should be weighed per-vendor, not assumed solved by "buying a
catalog tool" in the abstract.

## Cross-references

- [service-scorecards-and-maturity-model-design](../service-scorecards-and-maturity-model-design/SKILL.md) — the scorecard/rubric design principles (what to measure, how to tier) that apply regardless of which of these three tools' scorecard feature implements them.
- [golden-path-template-design-for-developer-platforms](../golden-path-template-design-for-developer-platforms/SKILL.md) — how these tools' self-service actions/scaffolding compare to and can wrap Backstage Software Templates or a standalone scaffolding CLI.
- [idp-adoption-rollout-and-change-management-strategy](../idp-adoption-rollout-and-change-management-strategy/SKILL.md) — the adoption and change-management implications of the buy-vs-build decision covered in step 1 here.
