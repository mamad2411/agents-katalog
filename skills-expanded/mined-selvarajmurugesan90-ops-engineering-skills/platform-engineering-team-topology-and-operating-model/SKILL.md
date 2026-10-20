---
name: platform-engineering-team-topology-and-operating-model
description: >
  Structures a platform engineering team using Team Topologies concepts —
  the platform team as a fundamental team type serving stream-aligned
  teams via X-as-a-Service interactions, run as an internal product with
  the "thinnest viable platform" as a sizing discipline. Use when a user
  asks to "structure our platform team," "decide what belongs on the
  platform vs application teams," "apply Team Topologies to platform
  engineering," "size the platform team," "stop the platform team from
  becoming a ticket queue," or "run the platform like a product."
license: Apache-2.0
compatibility: "Claude Code, GitHub Copilot, OpenAI Codex, Cursor, Gemini CLI"
metadata:
  domain: internal-developer-platform
  maturity: stable
---

# Platform Engineering Team Topology and Operating Model

## Purpose

A platform team with no deliberate operating model tends to drift toward
one of two failure shapes: it becomes a ticket queue that every other
team routes infrastructure requests through, turning "self-service" into
"self-service by filing a request and waiting," or it builds an ever-
expanding platform that tries to anticipate every team's need in advance,
becoming a bottleneck to change and a single point of organizational
failure. Team Topologies (Skelton & Pais) frames the fix structurally: a
platform team is one of four fundamental team types, existing specifically
to reduce the cognitive load of stream-aligned teams (the teams that
actually build and own user-facing value) by providing internal services
those teams can consume with minimal cognitive overhead — X-as-a-Service
interaction, not "collaborate on everything" or "hand off tickets."
Sizing the platform to the "thinnest viable platform" (TVP) — the minimum
that measurably reduces cognitive load, not the maximum a platform team
can imagine building — and running it with real product-management
discipline (a roadmap, a backlog, direct customer feedback) is what keeps
a platform team from drifting into either failure shape. This skill covers
that structural and operating-model design.

## When to use

- Standing up a platform engineering function for the first time and
  deciding its scope, team boundaries, and interaction model with
  application teams.
- The platform team has become a bottleneck — every infrastructure change
  routes through a ticket queue with multi-week turnaround — and the org
  wants to restructure toward genuine self-service.
- Deciding whether a new capability (e.g. a service mesh, a new CI
  runner type) belongs on the platform team's roadmap or should stay with
  the stream-aligned team that needs it.
- A platform team's roadmap has grown to include speculative capabilities
  nobody has asked for yet, and needs a sizing discipline to push back on
  scope creep.
- Diagnosing why application teams have started building unofficial,
  duplicated infrastructure tooling of their own ("shadow platforms")
  instead of using the sanctioned platform.

## Prerequisites & environment

- Familiarity with Team Topologies' four fundamental team types
  (stream-aligned, platform, enabling, complicated-subsystem) and its
  three interaction modes (collaboration, X-as-a-Service, facilitating) —
  this skill assumes that vocabulary rather than re-deriving it.
- An honest inventory of what stream-aligned teams currently have to do
  themselves that a platform could absorb — provisioning a new
  environment, wiring CI from scratch, setting up observability — as the
  starting input for scoping the platform, not a list of technologies the
  platform team finds interesting.
- Organizational willingness to treat the platform as having internal
  "customers" (the stream-aligned teams) with real product-management
  practices applied to it — a roadmap, a backlog, a feedback loop — rather
  than as a cost-center infrastructure function run purely on inbound
  requests.
- Executive sponsorship for the platform team's staffing and mandate,
  since "thinnest viable platform" sizing decisions and pushing back on
  scope creep both require organizational backing, not just the platform
  team's own judgment.

## Step-by-step guidance

1. **Define the platform's boundary around cognitive load actually
   removed from stream-aligned teams, not around every possible internal
   tool.** For each candidate capability, ask: does a stream-aligned team
   currently have to understand and operate this themselves, and would
   absorbing it into the platform measurably reduce what they need to
   know to ship? A capability that's already simple for stream-aligned
   teams, or one only a single team needs, is a weak candidate for
   platform investment regardless of how technically interesting it is
   to build.

2. **Size to the "thinnest viable platform" (TVP): start with the minimum
   surface that removes real cognitive load, and expand only from
   demonstrated need.** A TVP for a first platform investment is
   typically much smaller than what a platform team would design if asked
   to build "the ideal platform" from scratch:
   ```markdown
   # TVP scope, quarter 1 (illustrative)
   In scope: CI pipeline template, container registry with automated
   scanning, one golden-path scaffolding tier, catalog registration.
   Explicitly out of scope (revisit only if demand is demonstrated):
   multi-cluster failover, a custom internal PaaS UI, cost-allocation
   dashboards, a bespoke secrets-rotation service.
   ```
   This mirrors the golden-path tiering discipline in
   [golden-path-template-design-for-developer-platforms](../golden-path-template-design-for-developer-platforms/SKILL.md)
   — start narrow, expand from evidence, not speculation.

3. **Default the platform's interaction mode with stream-aligned teams to
   X-as-a-Service**, meaning teams consume the platform via a
   well-documented API, self-service portal, or golden path with minimal
   ongoing collaboration required — not a standing weekly sync, and not a
   ticket queue where every request needs a platform engineer's manual
   action.
   ```markdown
   # Interaction mode by platform capability
   - Environment provisioning: X-as-a-Service (self-service API/portal,
     see platform-self-service-api-and-workflow-design)
   - New capability onboarding (e.g. a team's first golden-path adoption):
     Facilitating, time-boxed (platform engineer pairs with the team for
     the first onboarding, then hands off to self-service)
   - A genuinely novel, cross-cutting architectural change (e.g.
     introducing service mesh org-wide): Collaboration, time-boxed,
     explicitly not the platform's default mode
   ```
   Reserve **collaboration** mode for genuinely novel, time-boxed work
   (a new capability being co-designed, an unusual integration), and
   **facilitating** mode for helping a team ramp up on something the
   platform already offers — neither should become the default steady-
   state interaction, or the platform reverts to being a ticket queue in
   disguise.

4. **Structure internal sub-teams around the platform's own distinct
   "as-a-service" surfaces**, rather than one undifferentiated platform
   team responsible for everything:
   ```markdown
   # Example sub-team structure, ~12-engineer platform org
   - Golden Paths & Scaffolding (3 eng): owns templates, catalog
   - Infrastructure Provisioning (4 eng): owns self-service API, Resource
     Definitions/Terraform modules
   - Developer Portal (3 eng): owns Backstage/portal instance, plugins
   - Platform SRE (2 eng): owns the platform's own reliability/on-call
   ```
   Each sub-team should be small enough to own its surface with a clear,
   nameable API contract to the rest of the org — matching the
   stream-aligned team's own preference for a small number of
   well-defined services over one large team with unclear ownership
   boundaries.

5. **Run the platform with real product-management practices**, not
   purely inbound-ticket-driven work: maintain a public roadmap,
   prioritize a backlog against actual demand signal (see
   [developer-experience-measurement-and-platform-adoption](../developer-experience-measurement-and-platform-adoption/SKILL.md)),
   and hold a recurring feedback loop with representative stream-aligned
   teams (an advisory council, office hours, a quarterly survey) — treat
   internal developers as customers whose retention and satisfaction
   matter, the same posture an external product team takes toward paying
   customers.

6. **Push back on scope creep using the TVP discipline as the explicit
   criterion**, not team capacity alone. When a request or an internally
   generated idea proposes expanding the platform, require it to name
   which stream-aligned team's cognitive load it removes and what
   evidence (a ticket pattern, a survey finding, a repeated Slack
   question) supports the need — an idea that can't answer this stays out
   of scope regardless of how good it sounds.

7. **Watch for "shadow platform" formation as a diagnostic signal.** If
   multiple stream-aligned teams have independently built similar
   infrastructure tooling outside the sanctioned platform, that's evidence
   either the platform's scope is too narrow (a real need going unmet) or
   its interaction mode is too slow/collaborative (teams found it faster
   to build their own than to wait on or coordinate with the platform
   team) — investigate which, rather than assuming the shadow tooling is
   simply non-compliance to be shut down.

8. **Reassess team boundaries as the org and platform mature**, since
   Team Topologies treats team boundaries as something to evolve
   deliberately over time, not a static org chart drawn once — a
   capability that started as a stream-aligned team's bespoke tool can
   graduate into the platform once multiple teams need it, and a platform
   capability that's fully commoditized (e.g. a fully self-service,
   zero-touch capability) may need less dedicated ownership than it did
   at launch.

## Best practices

- Scope every platform investment against "does this remove real
  cognitive load from a stream-aligned team," not "is this technically
  interesting to build" or "did someone ask for it once."
- Default to X-as-a-Service as the platform's steady-state interaction
  mode; treat collaboration and facilitating modes as deliberate,
  time-boxed exceptions, not the normal way stream-aligned teams get
  things done.
- Start at the thinnest viable platform and expand only against
  demonstrated demand — the same tiering/expand-from-evidence discipline
  applied to golden paths in
  [golden-path-template-design-for-developer-platforms](../golden-path-template-design-for-developer-platforms/SKILL.md)
  applies to the platform team's own scope.
- Run the platform with a visible roadmap and backlog prioritized against
  real demand signal, not purely reactive to whichever team escalated
  loudest this week.
- Structure sub-teams around distinct, nameable "as-a-service" surfaces
  with clear ownership, rather than one undifferentiated team where
  responsibility for any given capability is unclear.
- Treat shadow-platform formation as a diagnostic signal about the
  platform's scope or responsiveness, not simply a compliance problem to
  shut down.
- Revisit team boundaries periodically — a topology drawn once at launch
  and never revisited will eventually mismatch the org's actual needs.

## Common pitfalls

- **Symptom:** Every infrastructure request from a stream-aligned team
  goes through a ticket, waits days to weeks for a platform engineer to
  action it manually, and stream-aligned teams describe the platform team
  as "the people we file tickets to," not a self-service capability.
  **Fix:** This is a platform team stuck in an implicit "collaboration on
  everything" or ticket-relay interaction mode rather than X-as-a-Service.
  Identify the highest-volume ticket categories and convert them into a
  genuine self-service API or golden-path capability, scoped narrowly to
  those categories first, rather than adding more platform engineers to
  process the same ticket queue faster.

- **Symptom:** The platform team's roadmap includes a dozen speculative
  capabilities ("a unified secrets-rotation service," "a custom internal
  PaaS UI") that no stream-aligned team has specifically requested or is
  currently blocked without, while real, cited pain points sit
  unaddressed.
  **Fix:** Apply the TVP discipline from step 6 — require every roadmap
  item to name the specific cognitive load it removes and the evidence
  behind that need; deprioritize or shelve anything that can't.

- **Symptom:** Three different stream-aligned teams have each built their
  own ad hoc CI pipeline template and deployment scripts that duplicate
  most of what the platform team's golden path is supposed to provide.
  **Fix:** This is shadow-platform formation (step 7) — before treating it
  as non-compliance, investigate whether the sanctioned golden path
  genuinely doesn't cover their case (a scope gap — expand the golden path,
  see
  [golden-path-template-design-for-developer-platforms](../golden-path-template-design-for-developer-platforms/SKILL.md))
  or whether the platform team was simply too slow/hard to engage with
  (an interaction-mode problem — move that capability further toward
  X-as-a-Service).

- **Symptom:** A single platform team of 15 engineers owns catalog,
  golden paths, infrastructure provisioning, observability tooling, and
  the CI runner fleet, with no internal sub-boundaries — any given
  request's actual owner is unclear even to other engineers on the same
  team, and cross-cutting changes require coordinating the whole team.
  **Fix:** Split into sub-teams around distinct as-a-service surfaces
  (step 4) with clear, nameable ownership — this doesn't necessarily mean
  separate reporting lines, but it does mean a request for "fix the
  scaffolding template" and a request for "provision a new database" have
  different, identifiable owners rather than landing on the same
  undifferentiated backlog.

- **Symptom:** The platform team measures its own success purely by
  uptime and ticket-closure SLA, and is surprised when an org-wide
  developer survey shows low satisfaction with the platform despite both
  metrics looking healthy.
  **Fix:** Uptime and ticket SLA measure operational health, not product
  value delivered to internal customers — add the customer-facing
  measurement practices in
  [developer-experience-measurement-and-platform-adoption](../developer-experience-measurement-and-platform-adoption/SKILL.md),
  and treat the platform team's product-management discipline (roadmap,
  backlog, customer feedback loop) as core to its operating model, not
  optional polish.

## Worked example

**Scenario:** A 250-engineer product organization has a 6-person
"DevOps team" that everyone routes infrastructure requests through via a
shared ticket queue — new environment provisioning, CI runner changes,
DNS records — with a median turnaround of 9 business days. Three product
teams have started maintaining their own Terraform modules and CI
templates because "it's faster than waiting on DevOps."

1. **Reframe as platform engineering, not a ticket-processing function.**
   Leadership names the team's mandate explicitly: reduce stream-aligned
   teams' cognitive load via self-service, not process their requests
   faster.
2. **Audit ticket volume by category** over the last two quarters: 40% are
   new-environment provisioning requests, 25% are DNS/routing changes,
   20% are CI runner configuration, 15% miscellaneous.
3. **Scope a thinnest-viable-platform**: a self-service provisioning API
   covering exactly the top two categories (environment provisioning,
   DNS/routing) — explicitly deferring a broader "infrastructure-as-a-
   service" vision the team had been informally discussing for a year.
4. **Default interaction mode set to X-as-a-Service** for the new API;
   the team commits to a facilitating engagement (pairing, one week) for
   each of the three teams currently running shadow Terraform, to migrate
   them onto the sanctioned self-service path rather than simply telling
   them to stop.
5. **Sub-team split**: the 6-person team divides into a 4-person
   Infrastructure Provisioning group (owns the new self-service API and
   Resource Definitions) and a 2-person Platform SRE group (owns the
   provisioning API's own reliability, since a self-service API that's
   frequently down is worse than the ticket queue it replaces).
6. **Product-management practice**: a public roadmap is published showing
   what's shipped, in progress, and explicitly out of scope for now (CI
   runner self-service, deferred to next quarter based on ticket volume
   evidence), plus a monthly office-hours session for direct feedback.
7. **Result after two quarters**: environment provisioning turnaround
   drops from 9 days to same-day self-service; the three shadow-Terraform
   teams migrate onto the sanctioned path during their facilitated
   onboarding week, closing the shadow-platform gap without a mandate.

## Cross-references

- [golden-path-template-design-for-developer-platforms](../golden-path-template-design-for-developer-platforms/SKILL.md) — the tiering and expand-from-evidence discipline this skill's "thinnest viable platform" sizing principle mirrors, applied to team scope rather than template scope.
- [idp-adoption-rollout-and-change-management-strategy](../idp-adoption-rollout-and-change-management-strategy/SKILL.md) — sequencing how a newly-scoped platform capability actually gets adopted, once this skill has determined what the platform team should build and how it should engage.
- [developer-experience-measurement-and-platform-adoption](../developer-experience-measurement-and-platform-adoption/SKILL.md) — the customer-facing measurement practices a platform team run as a product, per this skill, needs in place of (or alongside) purely operational metrics like uptime and ticket SLA.
