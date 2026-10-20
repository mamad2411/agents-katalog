---
name: complete-idp-deployment-on-k3s-from-scratch
description: >
  Sequences a lightweight Internal Developer Platform deployment on K3s
  for edge, on-prem, and development contexts where a full Backstage
  footprint isn't justified: K3s install → a resource-right-sized IDP
  choice (slimmed single-replica Backstage vs. a hosted no-code catalog
  tool) → a thin golden-path template → minimal-governance self-service →
  lightweight scorecards, all explicitly scoped to small teams and
  constrained hardware rather than restating the full cloud/enterprise
  build. Use when a user asks to "set up a lightweight internal developer
  platform," "run Backstage or a service catalog on K3s," "build a
  dev-team-sized IDP without enterprise overhead," "stand up a platform
  for an edge or small on-prem deployment," or "decide whether a full
  Backstage is overkill for our team size."
license: Apache-2.0
compatibility: "Claude Code, GitHub Copilot, OpenAI Codex, Cursor, Gemini CLI"
metadata:
  domain: internal-developer-platform
  maturity: stable
---

# Complete IDP Deployment on K3s from Scratch

## Purpose

Every other "complete deployment" skill in this repo assumes a platform
team big enough to run a multi-replica Backstage backend, a dedicated
approval workflow with a named approver, and a full scorecard rubric. That
assumption is wrong for a 3-person team standing up a K3s cluster on a
handful of edge devices or a single dev VM — and pretending otherwise
produces a platform nobody has the headcount to operate. This skill scopes
an IDP deliberately to what a small team or resource-constrained
environment can actually run and maintain, following K3s's own "thinnest
viable platform" ethos into the tooling choices above it: fewer moving
parts, an explicit choice between self-hosting a slimmed Backstage or
paying for a hosted no-code catalog instead, and governance that's
present but proportionate — not the multi-week approval-workflow buildout
the AWS/Azure/GCP/OCI variants assume.

## When to use

- A small platform team (often one person, part-time) standing up a
  service catalog and golden path for a handful of teams, not an
  enterprise-wide rollout.
- Deploying an IDP alongside K3s on edge devices, a single on-prem VM
  cluster, or a developer's local/CI environment where node resources are
  genuinely constrained (a Raspberry Pi cluster, a 2-vCPU/4GB dev VM).
- Deciding whether a full Backstage build is justified yet, or whether a
  hosted no-code catalog tool gets the same practical benefit for far less
  operational cost at the current team size.
- Standing up a pilot/proof-of-concept IDP cheaply before committing to
  one of the full cloud-specific builds in this repo.

## Prerequisites & environment

- One or more nodes meeting K3s's own minimum sizing (K3s itself is
  light, but Backstage's Node.js backend and its Postgres — even a small
  one — add real memory pressure on top; budget at least 2 vCPU/4GB free
  beyond what K3s and other workloads already consume before assuming
  self-hosted Backstage fits).
- `kubectl` and `helm` ≥ 3.8 if the self-hosted-Backstage path is chosen;
  none of that is needed if the no-code SaaS path is chosen instead.
- A decision, made explicitly and revisited as the team grows, between
  self-hosting a slimmed Backstage and paying for a hosted no-code catalog
  (Port, Cortex, or OpsLevel) — this is the single biggest branch point in
  this skill and should not default silently to "Backstage because that's
  what the big skills use."
- If self-hosting: a Node.js/Yarn toolchain to build the (still-real,
  just resource-constrained) Backstage app.
- No assumption of a dedicated platform-approvals channel or a named
  full-time approver — plan the self-service phase's governance around
  whoever the team actually has, even if that's the same person writing
  the golden-path template.

## Step-by-step guidance

**Phase 1 — Install K3s, sized to the actual hardware.** Decide the
datastore/HA model up front: a single-server install with the embedded
SQLite datastore is genuinely fine for dev/edge/small-team use and avoids
running a separate etcd cluster the team has no capacity to operate; only
move to the embedded-etcd HA model (3 server nodes) if uptime actually
requires it. Size node resource requests deliberately against real
hardware, not a cloud default — an edge device or small VM has no
node-autoscaling safety net. See
[lightweight-kubernetes-k3s](../../../kubernetes-platform/skills/lightweight-kubernetes-k3s/SKILL.md)
for the datastore decision, install commands, and air-gapped install path
if the site has no direct internet access.

**Phase 2 — Choose the IDP's shape deliberately: slimmed Backstage vs.
hosted no-code catalog.** This is the phase with no equivalent in the
cloud-specific skills, because at cloud/enterprise scale the answer is
already "Backstage." At K3s scale, weigh both honestly:
- **Slimmed Backstage**: a single-replica backend (no HA, since the
  cluster itself likely isn't HA either), a small in-cluster Postgres
  instance sized to actually fit alongside K3s and other workloads on the
  available nodes, and a reduced plugin set (catalog + TechDocs + a
  minimal scaffolder, skip anything requiring its own backend service).
  Still real infrastructure the team must patch and operate. Chart
  packaging follows
  [helm-chart-authoring](../../../kubernetes-platform/skills/helm-chart-authoring/SKILL.md);
  any unavoidable custom logic follows
  [backstage-plugin-development](../backstage-plugin-development/SKILL.md).
- **Hosted no-code catalog** (Port, Cortex, or OpsLevel): no infrastructure
  to run at all on the constrained cluster — the catalog lives in the
  vendor's SaaS, and K3s only needs to expose whatever webhook/agent the
  tool requires to discover services. This is very often the right answer
  for a small team, precisely because it removes an entire self-hosted
  system from a team with no spare operational capacity. See
  [no-code-idp-service-catalog-tools-port-cortex-opslevel](../no-code-idp-service-catalog-tools-port-cortex-opslevel/SKILL.md)
  for evaluating and configuring this path, including its own guidance on
  when *not* to choose it.
Whichever is chosen, treat it as revisitable — a team of 3 choosing the
no-code path today should plan to reassess once headcount or catalog
complexity outgrows it, not treat the choice as permanent.

**Phase 3 — A thin golden-path template.** Author one golden-path
template, not a tiered set — a small team doesn't have the review capacity
several tiers assume. Keep its opinionated defaults genuinely minimal
(Dockerfile, a single CI workflow, catalog registration) and defer
anything elaborate until a second template is actually justified by real
demand. See
[golden-path-template-design-for-developer-platforms](../golden-path-template-design-for-developer-platforms/SKILL.md),
reading its tiering guidance as "here is the option to add tiers later,"
not a mandate to start with them.

**Phase 4 — Validate the template, scoped to what's actually running.**
Run the same scaffold-build-deploy-smoke-test-teardown pipeline as the
larger variants, but target the same constrained K3s cluster's own
ephemeral namespace rather than a separate cloud environment — there
usually isn't a separate environment to spare. See
[golden-path-template-validation-and-testing](../golden-path-template-validation-and-testing/SKILL.md).

**Phase 5 — Minimal-governance self-service.** Build the smallest
self-service surface that removes real toil: often just a Scaffolder
action (or, on the no-code path, the tool's own self-service action
feature) that creates a namespace and deploys the scaffolded service —
skip the multi-stage approval workflow the cloud-specific skills assume
unless there's a genuine reason for it at this scale (e.g., real budget
exposure). Still make whatever gate exists an explicit, auditable step
rather than an informal Slack message, and still keep policy rules
external and reviewable even if there's only one rule. See
[platform-self-service-api-and-workflow-design](../platform-self-service-api-and-workflow-design/SKILL.md),
applying its state-machine pattern at reduced scope rather than skipping
it — "minimal governance" is not the same as "no governance."

**Phase 6 — Lightweight scorecards.** Track a small number of
machine-verifiable checks (has a Dockerfile from the golden path, has a
health endpoint, is registered in the catalog) rather than the full
production-readiness/security/on-call rubric the cloud variants build —
a scorecard with more categories than the team has bandwidth to act on
just becomes another unread dashboard. See
[service-scorecards-and-maturity-model-design](../service-scorecards-and-maturity-model-design/SKILL.md).

**Phase 7 — Operate at the "thinnest viable platform" size, deliberately,
not by accident.** A K3s-scale platform "team" is often one person
wearing the platform hat part-time; make that explicit rather than
pretending it's a dedicated team, and reassess scope as the org grows. See
[platform-engineering-team-topology-and-operating-model](../platform-engineering-team-topology-and-operating-model/SKILL.md)
for the thinnest-viable-platform sizing discipline this phase applies
literally, and
[idp-adoption-rollout-and-change-management-strategy](../idp-adoption-rollout-and-change-management-strategy/SKILL.md)
for rolling out even a small platform without it feeling imposed.

## Best practices

- Default to the no-code SaaS path (Phase 2) unless there's a concrete
  reason to self-host — the operational cost of a self-hosted Backstage,
  even slimmed down, is easy to underestimate on a team with no spare
  capacity, and "we already know Backstage" is not by itself a strong
  enough reason at this scale.
- Back up K3s's datastore (SQLite file or embedded etcd snapshot)
  regardless of which HA model was chosen in Phase 1 — a single-server
  install with no backup turns any node failure into a full rebuild. See
  the backup guidance in
  [lightweight-kubernetes-k3s](../../../kubernetes-platform/skills/lightweight-kubernetes-k3s/SKILL.md).
- Resist adding a second golden-path template tier or a second scorecard
  category just because the enterprise variants have one — add complexity
  only when a real, current need justifies the added review/maintenance
  burden, per the thinnest-viable-platform discipline.
- Revisit the Phase 2 decision on a schedule (e.g., every two quarters),
  not only when something breaks — a team that's quietly outgrown its
  no-code catalog's self-service action limits, or a slimmed Backstage
  that's quietly become the bottleneck, both benefit from a deliberate
  re-check rather than limping along.
- Size Backstage's own pod resource requests/limits explicitly if
  self-hosting — an unset or default request on a genuinely small node can
  starve K3s's own control-plane components, unlike on a cloud cluster
  with headroom to spare.

## Common pitfalls

- **Symptom:** The self-hosted Backstage backend (Phase 2) gets OOMKilled
  repeatedly on a small edge node, and restarts don't fix it.
  **Fix:** This is usually a Phase 1/Phase 2 sequencing gap — the node was
  sized for K3s alone, without budgeting the extra memory a Node.js
  backend and even a small Postgres instance need on top. Either move
  Backstage's Postgres to a smaller footprint (or an external managed
  instance if one is available, even at this scale) or reconsider the
  no-code path from Phase 2 rather than continuing to fight the same
  node's memory ceiling.

- **Symptom:** A single-server K3s node (embedded SQLite datastore, no HA)
  fails, and the platform — catalog, scaffolder, everything — is
  unrecoverable because there was no datastore backup.
  **Fix:** This is a direct consequence of skipping the backup step in
  Phase 1 while treating single-server K3s as "good enough" without also
  treating its lack of HA as a real risk to plan around. Take periodic
  snapshots regardless of the HA model chosen, and store them off the
  node they're backing up.

- **Symptom:** A K3s-scale platform quietly accumulates the same
  multi-stage approval workflow, several golden-path tiers, and a full
  scorecard rubric the enterprise variants use — and the one-person
  platform team spends more time maintaining platform tooling than the
  small team of developers it serves would have spent doing the manual
  work directly.
  **Fix:** This is scope creep past what Phase 3/5/6 recommend for this
  scale. Cut back to the thinnest viable version deliberately — one
  template tier, a minimal self-service gate, a handful of scorecard
  checks — and treat any expansion as something that must be justified by
  a real, current need, not copied wholesale from a bigger deployment's
  skill.

- **Symptom:** The team decides mid-year to switch from the no-code SaaS
  path to self-hosted Backstage (or vice versa) and discovers there's no
  clean migration path for the catalog's existing service metadata.
  **Fix:** Because Phase 2 is a real architectural fork, not a config
  toggle, plan the export/import path (or accept a manual
  re-registration effort) before committing to either option, and revisit
  the choice on the schedule recommended above rather than waiting until
  outgrowing one path forces an unplanned, lossy switch.

## Worked example

**Scenario:** "Riverside Robotics" runs a 3-person platform effort
(part-time, alongside other duties) supporting 8 developers across two
edge-deployed product lines, on a K3s cluster spanning 4 small on-prem
nodes.

1. **Phase 1:** A single-server K3s install (embedded SQLite) runs across
   3 of the 4 nodes as agents, with the 4th as the server; a cron job
   snapshots the SQLite datastore nightly to a separate on-prem NAS.
2. **Phase 2:** After weighing both options, the team picks the hosted
   no-code path — OpsLevel — since none of the 3 part-time platform people
   have capacity to operate a self-hosted Backstage; K3s only runs a small
   webhook receiver OpsLevel uses for service discovery.
3. **Phase 3:** One golden-path template is authored: a Dockerfile, a
   single GitHub Actions workflow, and an OpsLevel registration call —
   no tiers.
4. **Phase 4:** A validation pipeline scaffolds a test service, builds,
   deploys to an `ephemeral-validation` namespace on the same K3s cluster,
   curls `/healthz`, and tears down.
5. **Phase 5:** Self-service is a single OpsLevel self-service action that
   creates the K3s namespace and applies the scaffolded manifest — no
   multi-stage approval, but every invocation is logged and reviewed
   weekly by the platform rotation.
6. **Phase 6:** A 4-check scorecard (Dockerfile present, health endpoint
   present, catalog-registered, CI passing) is tracked in OpsLevel
   directly.
7. **Phase 7:** The platform "team" is explicitly named as a rotating
   part-time duty among the 3 volunteers, reassessed every two quarters
   against actual ticket/support volume.

## Cross-references

- [lightweight-kubernetes-k3s](../../../kubernetes-platform/skills/lightweight-kubernetes-k3s/SKILL.md) — Phase 1.
- [no-code-idp-service-catalog-tools-port-cortex-opslevel](../no-code-idp-service-catalog-tools-port-cortex-opslevel/SKILL.md) — Phase 2 no-code path.
- [helm-chart-authoring](../../../kubernetes-platform/skills/helm-chart-authoring/SKILL.md), [backstage-plugin-development](../backstage-plugin-development/SKILL.md) — Phase 2 self-hosted path.
- [golden-path-template-design-for-developer-platforms](../golden-path-template-design-for-developer-platforms/SKILL.md) — Phase 3.
- [golden-path-template-validation-and-testing](../golden-path-template-validation-and-testing/SKILL.md) — Phase 4.
- [platform-self-service-api-and-workflow-design](../platform-self-service-api-and-workflow-design/SKILL.md) — Phase 5.
- [service-scorecards-and-maturity-model-design](../service-scorecards-and-maturity-model-design/SKILL.md) — Phase 6.
- [platform-engineering-team-topology-and-operating-model](../platform-engineering-team-topology-and-operating-model/SKILL.md), [idp-adoption-rollout-and-change-management-strategy](../idp-adoption-rollout-and-change-management-strategy/SKILL.md) — Phase 7.
- [complete-idp-deployment-on-prem-from-scratch](../complete-idp-deployment-on-prem-from-scratch/SKILL.md) — the heavier self-hosted variant to graduate to once the team and workload outgrow K3s-scale.
