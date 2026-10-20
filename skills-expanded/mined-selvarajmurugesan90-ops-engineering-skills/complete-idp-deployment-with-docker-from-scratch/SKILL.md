---
name: complete-idp-deployment-with-docker-from-scratch
description: >
  Sequences a small-scale, Docker Compose-based developer platform starting
  point for teams not running Kubernetes at all: a Compose-based service
  catalog (self-hosted Backstage or a hosted no-code tool) → Compose-based
  golden-path templates → Dapr sidecars in self-hosted/standalone mode for
  cross-service building blocks (state, pub/sub, service invocation) →
  a deliberately minimal self-service and scorecard layer. Framed
  honestly throughout as a starting point, not a full Internal Developer
  Platform — the skill states explicitly what's missing (multi-tenancy
  isolation, autoscaling, automated provisioning, self-healing) compared
  to the Kubernetes-based variants and when to graduate to one of them.
  Use when a user asks to "build a lightweight developer platform without
  Kubernetes," "set up a service catalog with Docker Compose," "add Dapr
  building blocks to a Compose-based stack," "avoid a full IDP until we
  actually need one," or "know what we're giving up by not using
  Kubernetes yet."
license: Apache-2.0
compatibility: "Claude Code, GitHub Copilot, OpenAI Codex, Cursor, Gemini CLI"
metadata:
  domain: internal-developer-platform
  maturity: stable
---

# Complete IDP Deployment with Docker from Scratch

## Purpose

Every other skill in this "complete deployment" set assumes Kubernetes —
for good reason, since Kubernetes' namespace/RBAC/quota primitives are
what make multi-tenancy, self-service provisioning, and autoscaling
tractable at platform scale. This skill is for teams that genuinely
aren't there yet: a handful of services, a small number of developers, and
Docker Compose as the only deployment substrate in production or
near-production use. The honest framing that runs through every phase
below: **this is a starting point, not an Internal Developer Platform.**
It gives a team a service catalog, a repeatable way to scaffold new
services, and Dapr's cross-service building blocks without requiring a
Kubernetes cluster — but it explicitly does not give them tenant
isolation beyond the OS/container boundary, autoscaling, self-healing, or
automated infrastructure self-service. Naming that gap plainly, and
naming the point at which a team should stop extending this and adopt one
of the Kubernetes-based variants instead, is this skill's actual job.

## When to use

- A small team or early-stage platform effort that has not adopted
  Kubernetes and has no near-term plan to, but still wants a service
  catalog and a repeatable scaffolding flow instead of ad hoc per-service
  setup.
- Standing up cross-service building blocks (shared state store, pub/sub,
  service-to-service calls) for a handful of Docker Compose-deployed
  services without adopting a message broker or service mesh outright.
- Evaluating whether a Compose-based approach is sufficient before
  investing in one of the Kubernetes-based IDP variants in this repo, or
  deciding when the team has actually outgrown this approach.
- Documenting, for a team already on this path, exactly what production
  guarantees they do not currently have (so an incident isn't the first
  time anyone realizes multi-tenancy or autoscaling was never built).

## Prerequisites & environment

- Docker Engine and Docker Compose v2 on every host this stack runs on;
  no Kubernetes assumption anywhere in this skill.
- A small, fixed number of hosts (this model does not scale past what a
  team can reason about and patch manually — if there's already a plan
  to run this across dozens of hosts, that's a signal to adopt one of the
  Kubernetes-based variants instead of scaling this one further).
- A decision, made explicitly, on the catalog's hosting model: a
  self-hosted Backstage via Compose (still real infrastructure to run and
  patch) or a hosted no-code catalog tool (no infrastructure to run at
  all) — see Phase 1.
- The Dapr CLI (`dapr init`) for self-hosted/standalone mode — this is a
  materially different Dapr operating mode than the Kubernetes
  sidecar-injection model most Dapr documentation (including this repo's
  own Dapr skill) assumes; flagged explicitly in Phase 3.
- No expectation of an automated, policy-gated self-service provisioning
  layer — Phase 5 below is intentionally manual/lightweight, and the gap
  versus the Kubernetes variants' Scaffolder-action-driven provisioning is
  named directly.

## Step-by-step guidance

**Phase 1 — A Docker Compose-based service catalog.** Choose between
self-hosting Backstage via Compose (a `docker-compose.yml` running the
Backstage app container alongside a Postgres container as its catalog
database — Backstage itself doesn't require Kubernetes to run, though most
of its own ecosystem tooling assumes it) or a hosted no-code catalog tool
that needs no infrastructure at all. At this scale, the hosted no-code
path is usually the more honest choice for the same reason it often is at
K3s scale — a small team running Compose in production almost certainly
has less spare operational capacity than a K3s-scale team, not more. See
[no-code-idp-service-catalog-tools-port-cortex-opslevel](../no-code-idp-service-catalog-tools-port-cortex-opslevel/SKILL.md)
for that path, and
[backstage-plugin-development](../backstage-plugin-development/SKILL.md)
for the self-hosted path's plugin/backend concepts if chosen (note that
skill's examples assume a Kubernetes-oriented deployment target for
Backstage's own hosting; the Compose deployment here still uses
Backstage's application code and plugin model identically — only the
container orchestration underneath differs).

**Phase 2 — Docker Compose-based golden-path templates.** Define one
scaffolding template whose *output* is a `docker-compose.yml` service
definition plus a `Dockerfile`, not a Helm chart or Kubernetes manifest —
this is the most concrete way this variant differs from every Kubernetes-
based one in this repo. Keep the template to a single tier; a Compose-
scale team doesn't have the review capacity multiple tiers assume. The
tiering and escape-hatch design principles still apply even though the
generated artifact type is different — see
[golden-path-template-design-for-developer-platforms](../golden-path-template-design-for-developer-platforms/SKILL.md)
for those principles, translating "Kubernetes manifest" to "Compose
service block" throughout. Validate the template the same way the other
variants do — scaffold a real instance, bring it up with `docker compose
up`, smoke-test it, and tear it down — adapting
[golden-path-template-validation-and-testing](../golden-path-template-validation-and-testing/SKILL.md)'s
pipeline shape to Compose rather than a Kubernetes ephemeral namespace.

**Phase 3 — Dapr sidecars in self-hosted/standalone mode for cross-
service building blocks.** Run Dapr via `dapr init` in self-hosted mode
and add a `daprd` sidecar container to each service's Compose block
(pointing at the app container's port via `--app-port`), rather than the
Kubernetes annotation-based sidecar injection
[dapr-distributed-runtime-configuration](../../../serverless-and-alternative-compute/skills/dapr-distributed-runtime-configuration/SKILL.md)
covers — **that skill's injection-annotation steps do not apply here**;
its state-store, pub/sub, and service-invocation *component YAML* and
resiliency-policy concepts do, unchanged, since Dapr's component model is
identical across hosted modes. Mount the same `components/` directory
into every service's `daprd` sidecar via a Compose volume so all services
share one component definition set. Validate the component configs (no
inline secrets, explicit scopes, bounded retries) the same way a
Kubernetes deployment would, per
[dapr-configuration-validation](../../../serverless-and-alternative-compute/skills/dapr-configuration-validation/SKILL.md).

**Phase 4 — A deliberately minimal scorecard.** Track a handful of
machine-verifiable checks (Dockerfile present, health endpoint present,
catalog-registered, Dapr component scoped correctly) rather than the full
rubric the Kubernetes variants build — same reasoning as the K3s variant:
a scorecard with more categories than the team can act on becomes noise.
See
[service-scorecards-and-maturity-model-design](../service-scorecards-and-maturity-model-design/SKILL.md),
applied at reduced scope.

**Phase 5 — Self-service, honestly scoped as manual/lightweight, not
automated provisioning.** State plainly to the team: there is no
Scaffolder-action-driven, policy-gated infrastructure self-service layer
in this variant, because there's no Kubernetes API or cloud SDK for such
an action to call — "self-service" here means a developer runs the golden-
path scaffolder to generate their Compose service block, opens a PR adding
it to the shared `docker-compose.yml` (or their own), and a teammate
reviews it manually. This is a materially different (and less automated,
less audited) governance model than
[platform-self-service-api-and-workflow-design](../platform-self-service-api-and-workflow-design/SKILL.md)'s
state-machine/policy-gate pattern — read that skill to understand
specifically what capability is being given up here, not to implement it
as-is; implementing its full pattern is usually a sign this variant has
been outgrown (see "What's missing" below).

## What's missing, compared to the Kubernetes-based variants

State this to the team as a running list, not a footnote:

- **No tenant isolation beyond the OS/container boundary.** There is no
  namespace, RBAC, or NetworkPolicy equivalent — every service on a given
  host can, by default, reach every other service's network ports. Compare
  to
  [multi-tenancy-and-team-workspace-design-for-idp](../multi-tenancy-and-team-workspace-design-for-idp/SKILL.md),
  none of which has an equivalent here.
- **No autoscaling and no self-healing.** A crashed container restarts
  per its `restart:` policy, if configured, but there is no horizontal
  scaling and no node-level rescheduling if a host fails outright.
- **No automated, policy-gated self-service infrastructure
  provisioning.** Phase 5 above is manual by design; there is no
  equivalent to the cloud variants' Scaffolder actions provisioning IAM
  roles or managed databases with a built-in approval workflow.
- **No managed database options wired in.** Any "database" this stack
  uses is another Compose container with the same durability and backup
  responsibilities as everything else here — there's no RDS/Cloud SQL/
  Flexible Server equivalent unless the team explicitly points a service
  at an external managed instance outside this Compose stack.
- **Single-host (or small, manually-coordinated multi-host) blast
  radius.** A host failure can take down every service on it
  simultaneously, with no scheduler moving workloads elsewhere.

## When to graduate off this variant

Move to
[complete-idp-deployment-on-k3s-from-scratch](../complete-idp-deployment-on-k3s-from-scratch/SKILL.md)
or a full cloud/on-prem Kubernetes variant once any of the following is
true: more than one team needs real isolation from another's workloads;
a service needs to scale horizontally in response to load; a host failure
has already caused (or is judged likely to soon cause) a multi-service
outage; or the manual PR-review self-service model in Phase 5 is
routinely too slow or too error-prone for the request volume. Treat
reaching any of these thresholds as the trigger to migrate, not a reason
to keep bolting ad hoc automation onto Compose.

## Best practices

- Say the "what's missing" section out loud to the team adopting this,
  not just in this document — the biggest risk of a Compose-based
  platform isn't that it's insufficient, it's that a team forgets it's
  insufficient until an incident makes it obvious.
- Keep the Phase 3 Dapr `components/` directory under version control
  and reviewed exactly like application code — it's shared across every
  service's sidecar, so an unscoped or secret-containing component
  affects every service on the host, not just one.
- Pin every image tag explicitly in the golden-path template's generated
  `docker-compose.yml` — there's no cluster-level image-pull policy or
  admission control here to catch an accidental `:latest` drift.
- Back up whatever Compose-hosted database(s) this stack runs, on an
  actual schedule, with a tested restore — there is no managed-service
  backup behind any of it.
- Re-evaluate the "when to graduate" thresholds on a fixed schedule (e.g.,
  quarterly), not only reactively after an incident exposes one of the
  missing capabilities above.

## Common pitfalls

- **Symptom:** Two services on the same Compose host can reach each
  other's ports even though only one was supposed to be reachable
  externally.
  **Fix:** This isn't a misconfiguration to patch — it's the "no tenant
  isolation" gap named above, working as (un)designed. If this actually
  matters, that's a signal to graduate to a Kubernetes-based variant with
  real NetworkPolicy support, not to attempt ad hoc `iptables` rules
  bolted onto Compose networking.

- **Symptom:** A Dapr sidecar fails to start with a component-loading
  error that looks identical to a Kubernetes Dapr issue, but the fix
  documented for Kubernetes (checking a `Scopes` annotation on the
  Deployment) doesn't apply.
  **Fix:** Confirm the `components/` directory is actually mounted into
  the `daprd` sidecar's Compose volume and that the CLI/sidecar version
  matches across all services — self-hosted mode's failure surface is
  different from the annotation-based Kubernetes injection most Dapr
  troubleshooting content (including
  [dapr-distributed-runtime-configuration](../../../serverless-and-alternative-compute/skills/dapr-distributed-runtime-configuration/SKILL.md))
  assumes.

- **Symptom:** The manual PR-review self-service model (Phase 5) becomes
  the bottleneck as the number of services grows, with new-service PRs
  sitting unreviewed for days.
  **Fix:** This is the expected failure mode of a manual governance model
  at growing scale, not a process tweak to optimize away — it's one of
  the named graduation triggers above. Treat it as the signal to begin
  planning a move to
  [complete-idp-deployment-on-k3s-from-scratch](../complete-idp-deployment-on-k3s-from-scratch/SKILL.md)
  rather than adding more manual reviewers.

- **Symptom:** A host running several services crashes, and every service
  on it goes down simultaneously with no automatic recovery beyond
  whatever `restart:` policy was set.
  **Fix:** This is the "no self-healing across hosts" gap, not a
  misconfigured restart policy (though confirm `restart: unless-stopped`
  or similar is actually set as a baseline). If simultaneous multi-service
  outages from a single host failure are unacceptable, that's a concrete,
  specific signal to graduate off this variant rather than adding
  ad hoc host-level HA scripting.

- **Symptom:** Someone runs `docker compose down -v` on the shared stack
  to "reset" a service, and it deletes the named volumes backing every
  other service's database on the same Compose file, not just the one
  intended.
  **Fix:** This is destructive and irreversible without a separate backup
  — `-v` removes named volumes for the whole Compose project, not a
  single service. Scope any reset to the specific service
  (`docker compose stop <service> && docker compose rm <service>`,
  and remove only that service's specific named volume if truly
  intended) rather than using project-wide `down -v` as a routine command,
  and keep backups of any stateful container's volume regardless.

## Worked example

**Scenario:** "Basecamp Analytics" is a 4-person engineering team running
6 internal services via Docker Compose on two VMs, with no Kubernetes
plans in the near term but real duplication pain from each service being
set up by hand.

1. **Phase 1:** The team picks a hosted no-code catalog (Cortex) over
   self-hosting Backstage, given they have no spare capacity to operate
   another stateful service.
2. **Phase 2:** One golden-path template is authored, producing a
   `Dockerfile` and a `docker-compose.yml` service block with health-check
   and `restart: unless-stopped` pre-filled; validated by scaffolding a
   test service, bringing it up locally, curling its `/healthz`, and
   tearing it down.
3. **Phase 3:** `dapr init` runs in self-hosted mode on both VMs; each
   service's Compose block gets a `daprd` sidecar with a shared
   `components/` directory defining a Redis-backed state store and a
   pub/sub component, mounted identically across all 6 services.
4. **Phase 4:** A 3-check scorecard (Dockerfile present, health endpoint
   present, catalog-registered) is tracked directly in Cortex.
5. **Phase 5:** New services are scaffolded from the Phase 2 template,
   added via PR to the shared `docker-compose.yml`, and reviewed manually
   by whichever teammate is free — explicitly documented as a stopgap.
6. Six months later, a second team joins and needs real isolation from the
   first team's workloads; Basecamp treats this as the graduation trigger
   and begins migrating to
   [complete-idp-deployment-on-k3s-from-scratch](../complete-idp-deployment-on-k3s-from-scratch/SKILL.md).

## Cross-references

- [no-code-idp-service-catalog-tools-port-cortex-opslevel](../no-code-idp-service-catalog-tools-port-cortex-opslevel/SKILL.md), [backstage-plugin-development](../backstage-plugin-development/SKILL.md) — Phase 1.
- [golden-path-template-design-for-developer-platforms](../golden-path-template-design-for-developer-platforms/SKILL.md), [golden-path-template-validation-and-testing](../golden-path-template-validation-and-testing/SKILL.md) — Phase 2.
- [dapr-distributed-runtime-configuration](../../../serverless-and-alternative-compute/skills/dapr-distributed-runtime-configuration/SKILL.md), [dapr-configuration-validation](../../../serverless-and-alternative-compute/skills/dapr-configuration-validation/SKILL.md) — Phase 3.
- [service-scorecards-and-maturity-model-design](../service-scorecards-and-maturity-model-design/SKILL.md) — Phase 4.
- [platform-self-service-api-and-workflow-design](../platform-self-service-api-and-workflow-design/SKILL.md) — Phase 5, referenced to show what's deliberately not implemented here.
- [multi-tenancy-and-team-workspace-design-for-idp](../multi-tenancy-and-team-workspace-design-for-idp/SKILL.md) — the isolation model this variant lacks.
- [complete-idp-deployment-on-k3s-from-scratch](../complete-idp-deployment-on-k3s-from-scratch/SKILL.md) — the graduation path once this variant is outgrown.
