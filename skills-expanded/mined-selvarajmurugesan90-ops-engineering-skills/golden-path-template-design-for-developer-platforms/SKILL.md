---
name: golden-path-template-design-for-developer-platforms
description: >
  Designs golden-path scaffolding templates for new services — opinionated
  defaults (CI pipeline, Dockerfile, observability instrumentation, catalog
  registration, security baseline) with deliberate, documented escape hatches
  for legitimate edge cases. Use when a user asks to "design a golden path
  template," "create a new-service scaffolding template," "standardize how
  teams start new services," "tier our service templates," or "balance
  platform opinionation with team autonomy."
license: Apache-2.0
compatibility: "Claude Code, GitHub Copilot, OpenAI Codex, Cursor, Gemini CLI"
metadata:
  domain: internal-developer-platform
  maturity: stable
---

# Golden Path Template Design for Developer Platforms

## Purpose

A golden path is the platform team's answer to "how do I start a new
service" — a scaffolding template that produces a service with a working
CI pipeline, a Dockerfile, base observability instrumentation, catalog
registration, and a security baseline already wired in, so most teams
never have to make those decisions themselves. The operational risk is at
either extreme: a template with too many knobs turns into an unmaintainable
tangle of conditional logic that nobody fully understands, while a template
with *no* knobs and no sanctioned way to deviate turns into a walled path —
the first team with a genuinely different runtime or an unusual compliance
requirement either forks around the platform entirely (silently, with no
governance) or blocks on the platform team to special-case them. This skill
covers the design discipline that keeps a golden path a paved road with
clearly marked exits: tiering templates by complexity instead of one
monolithic template, making assumptions visible and overridable rather than
hardcoded, and documenting *how* a team deviates so escape hatches are a
sanctioned, tracked decision rather than an invisible fork.

## When to use

- Designing the first golden-path template for a platform, or splitting an
  existing monolithic "one template to rule them all" into tiers.
- A team asks for a legitimate deviation from the template (different
  language runtime, no datastore needed, an extra compliance control) and
  there's no documented process for handling it.
- The current template has accumulated so many optional parameters/`if`
  branches in its scaffolder steps that changing it risks breaking
  combinations nobody tests.
- Deciding what the template should hardcode vs. parameterize (base image
  version, CI runner size, observability agent version).
- Standing up governance for who owns the golden path and how other teams
  propose changes to it.
- A previously scaffolded service breaks after an unrelated template change,
  revealing the template has no versioning.

## Prerequisites & environment

- A software catalog or scaffolding engine to render the template —
  Backstage's Scaffolder (`scaffolder.backstage.io/v1beta3` `Template`
  manifests) or a Score-based workflow (`score.dev` workload spec plus
  `score-compose`/`humctl` to materialize platform-specific manifests) are
  the two most common substrates; the design principles here apply to
  either.
- Git hosting with branch protection and CODEOWNERS support (GitHub,
  GitLab) so template changes go through review, not direct pushes to the
  templates repo's default branch.
- An existing (even minimal) CI pipeline standard, base container image,
  and observability agent/library the platform already endorses — a golden
  path packages existing platform decisions, it doesn't invent them from
  scratch.
- A defined security baseline (e.g. required non-root Dockerfile `USER`,
  a mandatory SAST/secret-scan CI step, a minimum set of IAM permissions)
  that the template can encode as a default rather than each team deciding
  independently.
- Write access to wherever generated services land (a GitHub org/group, an
  artifact registry) for the templating engine's publish step.
- Agreement on ownership: a named platform team (or a specific sub-team)
  with the authority to merge template changes — see
  [platform-engineering-team-topology-and-operating-model](../platform-engineering-team-topology-and-operating-model/SKILL.md).

## Step-by-step guidance

1. **Tier templates by complexity instead of building one template with
   dozens of conditional parameters.** A single `golden-path-service`
   template that tries to handle "no datastore" and "postgres" and
   "dynamodb" and "with a queue" and "gRPC vs REST" via nested `if`
   parameters becomes unreadable and untestable. Split into tiers that
   compose:
   - **Tier 1 — minimal**: stateless service, CI, Dockerfile, health
     endpoint, catalog registration. No datastore, no queue.
   - **Tier 2 — standard**: tier 1 plus a provisioned datastore
     (Postgres or DynamoDB, chosen at scaffold time).
   - **Tier 3 — advanced**: tier 2 plus an async queue/event stream
     integration and any additional compliance controls a stateful,
     message-driven service needs.
   Each tier is its own `Template` manifest and skeleton directory, not a
   branch inside one template.

2. **Make assumptions visible and overridable, with sensible defaults —
   never silently hardcoded.** Runtime version and base image are the two
   most common sources of drift; parameterize them with a default so a
   team that doesn't care gets the platform's current recommendation, and
   a team that does care can pick a supported alternative:
   ```yaml
   apiVersion: scaffolder.backstage.io/v1beta3
   kind: Template
   metadata:
     name: golden-path-service-standard
     title: "Standard Service (Golden Path — Tier 2: API + Datastore)"
     description: >
       CI, Dockerfile, observability, catalog registration, and a
       provisioned datastore. Use golden-path-service-minimal if the
       service has no persistent state.
     tags: [golden-path, tier-2]
   spec:
     owner: group:platform-team
     type: service
     parameters:
       - title: Service identity
         required: [name, owner, runtime]
         properties:
           name:
             type: string
             title: Service name
             pattern: '^[a-z][a-z0-9-]{2,40}$'
           owner:
             type: string
             title: Owning team (catalog Group)
           runtime:
             type: string
             title: Runtime
             enum: [go1.22, node20, python3.12]
             default: go1.22
           datastore:
             type: string
             title: Datastore engine
             enum: [postgres14, dynamodb]
             default: postgres14
     steps:
       - id: fetch-base
         name: Fetch golden-path skeleton (tier 2)
         action: fetch:template
         input:
           url: ./skeleton-standard
           values:
             name: '${{ parameters.name }}'
             owner: '${{ parameters.owner }}'
             runtime: '${{ parameters.runtime }}'
             datastore: '${{ parameters.datastore }}'
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
   `runtime` and `datastore` are overridable within a supported set — the
   template does not let a team type an arbitrary runtime string, which
   would defeat the point of a paved road.

3. **If Score is the templating substrate instead of Backstage**, encode
   the same tiering as separate `score.yaml` skeletons with parameterized
   `metadata.name` and `resources` blocks, materialized per-tier via
   `score-compose init --file score-standard.yaml` or `humctl score deploy
   -f score-standard.yaml`; see
   [humanitec-score-workload-specification](../humanitec-score-workload-specification/SKILL.md)
   for the workload-spec authoring details this skill doesn't repeat.

4. **Document escape hatches explicitly — never silently block anything
   outside the parameter list.** Ship a `DEVIATIONS.md` at the root of
   every skeleton that spells out the tradeoff of forking, e.g.:
   ```markdown
   # Deviating from the golden path

   ## Different base image / Dockerfile
   Edit `Dockerfile` directly after scaffolding. You lose automatic
   base-image bumps from `golden-path-service-standard` version updates —
   subscribe to #platform-golden-path-changes to track upstream CVE fixes
   you'll now need to apply manually.

   ## Different runtime not in the supported enum
   File an RFC (see CONTRIBUTING.md in the templates repo) proposing the
   platform team add support. Do not hand-edit the generated CI pipeline
   to run an unsupported runtime without the platform team's SLA
   coverage — CI infra for unlisted runtimes isn't maintained.

   ## Unusual compliance requirement (e.g. FedRAMP-scoped service)
   Use golden-path-service-advanced's `compliance-fedramp` overlay
   (see skeleton-advanced/overlays/) rather than modifying the security
   baseline in place — overlays are reviewed by security and stay
   upgradable.
   ```
   This turns "we went off-template" into a tracked, intentional decision
   with a known cost, instead of an invisible fork the platform team
   discovers only when the service breaks during a platform-wide upgrade.

5. **Version the template itself and stamp generated services with the
   version that created them**, so a template change doesn't silently
   affect services already scaffolded:
   ```yaml
   # in skeleton-standard/catalog-info.yaml.njk, filled at scaffold time
   metadata:
     annotations:
       idp.acme.com/golden-path-template: golden-path-service-standard@2.3.0
   ```
   Tag the templates repo per release (`git tag
   golden-path-service-standard-v2.3.0`) and pin `fetch:template`'s `url`
   to a ref when you need a specific tier version to keep tracking a known
   good state rather than always `main`.

6. **Set up governance: a named owner and a change-proposal process.**
   The platform team owns and merges changes to the templates repo
   (`CODEOWNERS` entry: `/templates/ @acme-corp/platform-team`), but any
   team can open an RFC-style pull request proposing a new tier, a new
   parameter, or a new default — reviewed against the same bar as any
   platform change (does it stay a paved road, does it add an escape
   hatch instead of a special case). Reject PRs that add a one-off
   conditional for a single team's need; redirect those to the
   `DEVIATIONS.md` fork path instead.

7. **Publish the template's own metadata into the catalog** as a
   discoverable entity (Backstage templates are themselves catalog
   entities) so teams can find "which golden path fits my service" instead
   of asking the platform team directly.

8. **Before making a tier the mandatory default, validate it end-to-end**
   — see
   [golden-path-template-validation-and-testing](../golden-path-template-validation-and-testing/SKILL.md)
   for the CI pipeline that scaffolds a real instance and proves it builds,
   deploys, and passes a smoke test before you point new-service creation
   at it.

## Best practices

- **Tier by genuine complexity boundaries** (stateless / stateful / async),
  not by team or org unit — a template tiered around org politics rather
  than technical shape reintroduces the "walled path" problem one level
  down.
- **Prefer a small enum of supported values over a free-text parameter**
  for anything the platform has to operate long-term (runtime, base image,
  datastore engine) — a free-text `runtime: string` with no validation
  looks flexible but produces services the CI fleet and observability
  stack were never built to support.
- **Keep the skeleton a set of files with placeholders, not scaffolder
  logic with deep conditionals** — a `fetch:template` skeleton diffed in a
  PR is far easier for another engineer to review than branching logic
  embedded in scaffolder `steps`.
- **Publish the escape-hatch path with the same visibility as the golden
  path itself** — a `DEVIATIONS.md` buried in a wiki nobody reads produces
  the same silent-fork outcome as having no escape hatch at all.
- **Stamp every scaffolded service with the template name and version that
  created it** — without it, a template regression or a mandatory security
  upgrade has no way to find which live services need it.
- **Review golden-path changes for "does this reduce the need for an
  escape hatch" as a first-class review criterion**, not just "does this
  work" — a change that quietly narrows what's supported pushes more
  teams toward undocumented forks.
- **Treat the golden path as a recommendation with teeth, not a
  requirement with no appeal** — pair the design with a documented
  exception process (RFC) so refusing a request is a traceable decision,
  not just platform-team fiat.

## Common pitfalls

- **Symptom:** The golden-path template has grown a `useQueue: boolean`,
  a `datastoreType: enum`, a `authMode: enum`, and a dozen nested `if`
  conditions in its scaffolder steps, and nobody is confident which
  combinations actually produce a working service.
  **Fix:** Split into explicit tiers (minimal/standard/advanced), each
  its own template and skeleton, so every published template is a tested,
  known-good combination rather than one of an untested combinatorial
  space.

- **Symptom:** A team with a genuinely different compliance requirement
  hand-edits the generated Dockerfile and CI pipeline outside the
  template's parameters, and the platform team only discovers this months
  later during an org-wide base-image CVE remediation.
  **Fix:** Ship a `DEVIATIONS.md` documenting the sanctioned way to
  deviate and its cost (losing auto-upgrades), and require an annotation
  or catalog tag marking a service as "deviated from golden path" so the
  platform team's upgrade sweeps can find it proactively instead of by
  surprise.

- **Symptom:** A template change (e.g. bumping the default Postgres
  version) is merged directly to `main`, and every service scaffolded
  starting that day silently gets the new default with no announcement,
  breaking a downstream migration assumption for one team.
  **Fix:** Version the template, stamp generated services with the
  version, and treat a default-changing update as a minor/major version
  bump communicated through the same channel as any platform change — see
  [golden-path-template-validation-and-testing](../golden-path-template-validation-and-testing/SKILL.md)
  for canary-rolling template changes before they become the default.

- **Symptom:** The platform team makes the golden path the *only* way to
  create a new service on day one, with no exception process, and teams
  with legitimate edge cases either quietly stop using the platform or
  escalate loudly, souring the whole rollout.
  **Fix:** This is a specific documented rollout failure mode — pair the
  template's launch with an explicit, fast exception/RFC path from day
  one, not an afterthought added after the first blowup; see
  [idp-adoption-rollout-and-change-management-strategy](../idp-adoption-rollout-and-change-management-strategy/SKILL.md)
  for sequencing a mandatory-golden-path rollout without stifling
  legitimate edge cases.

- **Symptom:** Two teams independently build near-identical "custom"
  services because neither knew a tier already covered their case, since
  the templates aren't discoverable outside the platform team's own
  memory.
  **Fix:** Register each template tier as its own discoverable catalog
  entity with a clear description of what it covers, rather than leaving
  template selection as a Slack-thread negotiation with the platform team.

## Worked example

**Scenario:** `acme-corp`'s platform team has one golden-path template
covering every new service, with 9 boolean/enum parameters and a
scaffolder pipeline full of `if: ${{ parameters.useQueue }}` branches. A
team building a new fraud-detection service needs Kafka consumption and a
stricter security baseline than the template supports, and is about to
hand-roll their own pipeline outside the platform entirely.

1. The platform team splits the monolith into three templates:
   `golden-path-service-minimal` (stateless, CI, Dockerfile, catalog
   registration only), `golden-path-service-standard` (adds Postgres/
   DynamoDB, shown in step 2 above), and `golden-path-service-advanced`
   (adds a Kafka producer/consumer skeleton and a `compliance-strict`
   overlay).
2. Each becomes its own `Template` manifest with its own skeleton
   directory (`skeleton-minimal/`, `skeleton-standard/`,
   `skeleton-advanced/`), removing all cross-tier conditionals from the
   scaffolder steps.
3. The fraud-detection team scaffolds from
   `golden-path-service-advanced`, selecting `runtime: go1.22` and
   getting the Kafka skeleton and stricter baseline by default — no fork
   needed, because the tier now genuinely covers their shape of service.
4. A separate ask (a team wanting Rust, not in any tier's `runtime` enum)
   goes through the RFC process documented in `DEVIATIONS.md`: they file
   a PR against the templates repo proposing `rust1.78` be added to
   `golden-path-service-minimal`'s enum, which the platform team reviews
   and merges as a `v3.0.0` bump.
5. Every service scaffolded after the split carries an
   `idp.acme.com/golden-path-template: golden-path-service-advanced@1.0.0`
   annotation, so when a Kafka client library CVE surfaces six months
   later, the platform team queries the catalog for that annotation to
   find every affected service instead of guessing.
6. Before `golden-path-service-advanced@1.0.0` becomes the default choice
   surfaced to all teams, it runs through the scaffold-build-deploy-smoke-
   test CI pipeline described in
   [golden-path-template-validation-and-testing](../golden-path-template-validation-and-testing/SKILL.md).

## Cross-references

- [golden-path-template-validation-and-testing](../golden-path-template-validation-and-testing/SKILL.md) — testing a template design like this one end-to-end before publishing it broadly or promoting it to the default.
- [humanitec-score-workload-specification](../humanitec-score-workload-specification/SKILL.md) — the Score workload spec as an alternative templating substrate for the same tiering and parameterization principles.
- [idp-adoption-rollout-and-change-management-strategy](../idp-adoption-rollout-and-change-management-strategy/SKILL.md) — sequencing a golden path's rollout so it doesn't become mandatory-with-no-exceptions from day one, a documented failure mode this skill's escape-hatch design exists to prevent.
- [platform-engineering-team-topology-and-operating-model](../platform-engineering-team-topology-and-operating-model/SKILL.md) — who the "platform team" that owns and governs the golden path actually is, organizationally.
