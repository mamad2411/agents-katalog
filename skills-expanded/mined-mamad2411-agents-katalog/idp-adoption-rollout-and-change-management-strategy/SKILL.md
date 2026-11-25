---
name: idp-adoption-rollout-and-change-management-strategy
description: >
  Sequences the rollout and change management of a new internal developer
  platform so teams actually adopt it voluntarily, addressing the
  well-documented failure mode of building a catalog, golden path, or
  self-service tool nobody asked for and nobody uses. Use when a user asks
  to "roll out our new IDP," "get teams to adopt the platform," "avoid
  building something nobody uses," "pick a pilot team for a new platform
  capability," "handle a team resisting the golden path," or "sunset the
  old way of doing things without breaking trust."
license: Apache-2.0
compatibility: "Claude Code, GitHub Copilot, OpenAI Codex, Cursor, Gemini CLI"
metadata:
  domain: internal-developer-platform
  maturity: stable
---

# IDP Adoption Rollout and Change Management Strategy

## Purpose

The most common way an internal developer platform fails is not a
technical one — it's a platform team building a catalog, a golden path, or
a self-service tool that is technically sound and that almost nobody
voluntarily uses, because it was designed and shipped without the
teams it's meant to serve ever being asked what friction they actually
have. This is a well-documented failure mode across the platform
engineering community: "build it and they will come" doesn't work for
internal tooling any more than it works for external products, and a
platform team that skips discovery, mandates adoption before it has any
proof the thing works, or kills trust with one bad forced migration can
spend years recovering credibility even after the tooling itself
improves. This skill covers the rollout and change-management sequence
that avoids that outcome: starting from real developer pain rather than a
platform team's assumption, proving value with a willing pilot before any
mandate, and treating a golden path's eventual default status as
something earned through demonstrated value rather than declared through
policy.

## When to use

- Planning the launch of a new platform capability — a service catalog, a
  golden-path template, a self-service provisioning API — before any code
  is written, not after.
- A platform capability already exists but adoption is stalled, and the
  team needs to diagnose whether the problem is the tooling or the
  rollout approach.
- Deciding whether and when to make a golden path or catalog registration
  mandatory, versus keeping it opt-in indefinitely.
- Planning to sunset an old way of doing things (a legacy deployment
  script, a manually-maintained spreadsheet of service owners) in favor
  of a new platform capability, without breaking teams who depend on the
  old path.
- A specific team is resisting adoption, and the platform team needs to
  distinguish "this team has a legitimate reason" from "this team just
  needs more support/communication."

## Prerequisites & environment

- Access to actual developers across multiple teams for discovery
  interviews or shadowing — this is a people/process prerequisite, not a
  tooling one, and it's the single most commonly skipped step.
- Executive or engineering-leadership sponsorship sufficient to protect
  the platform team's roadmap from being redirected by the loudest
  single request, and to eventually back a mandate once value is proven
  — sponsorship without proof of value is what produces a forced rollout
  with no trust behind it, so don't treat this as sufficient on its own.
- A communication channel developers actually read (not a wiki page
  nobody visits) for rollout announcements, office hours, and status
  updates — Slack/Teams channel, a recurring email digest, or a standing
  agenda item in an existing engineering-wide meeting.
- The measurement system from
  [developer-experience-measurement-and-platform-adoption](../developer-experience-measurement-and-platform-adoption/SKILL.md)
  already in place, or at least planned — a rollout without a way to
  measure whether it's working is flying blind on the exact question that
  matters most.
- A named pilot team (or two) willing to be first, ideally one with a
  real, current pain point the new capability actually addresses — not
  whichever team is easiest to reach.

## Step-by-step guidance

1. **Start from developer pain, not a platform-team assumption, before
   building anything.** Run structured discovery — interviews, shadowing
   a team's actual deploy process, or reviewing a quarter's worth of
   platform-support tickets — and write down the specific, recurring pain
   points in developers' own words before scoping any tooling:
   ```markdown
   # Discovery notes — new-service onboarding pain (interviews, 8 teams)

   - 6/8 teams: "the hardest part is remembering every place a new
     service needs to be registered (PagerDuty, cost tags, DNS)."
   - 4/8 teams: copy the Dockerfile and CI config from whichever service
     they worked on most recently, with no idea if it's still the
     recommended pattern.
   - 2/8 teams: have hit a broken build from a stale copied CI template
     within the last quarter.
   ```
   If the resulting scope doesn't map back to specific, cited pain points
   like these, that's a sign the project risks becoming exactly the
   "nobody asked for this" catalog.

2. **Ship the smallest version that addresses the top-cited pain point
   first**, not the full platform vision — a golden path covering only
   "register the new service everywhere it needs to be registered"
   (the top pain point above) ships and proves value in weeks; a golden
   path also trying to solve datastore provisioning, compliance tiering,
   and cost allocation on day one takes a year and risks nobody being
   left to advocate for it by the time it ships.

3. **Recruit a pilot team with a real, current need — not the easiest
   team to reach.** A pilot team that doesn't actually have the pain
   point being solved will use the tool half-heartedly and provide weak
   signal either way; a pilot team mid-way through solving that exact
   problem manually has both the motivation to engage seriously and the
   standing to credibly advocate for it afterward.

4. **Make the new capability opt-in during the pilot, with a real
   deadline for evaluating it — not an indefinite trial with no decision
   point.** Set an explicit checkpoint (e.g. "4 weeks, then we decide
   whether to expand, iterate, or shelve it") and hold it, rather than
   letting a pilot quietly run forever without ever being declared
   successful or not.

5. **Publish pilot results honestly, including what didn't work**, before
   expanding rollout — a rollout announcement that only lists wins reads
   as marketing, and developers who hear about a pilot's problems from a
   Slack DM instead of the platform team's own announcement lose trust in
   future announcements too:
   ```markdown
   # Golden-path pilot results (fraud-detection, payments-api — 4 weeks)

   Worked: both teams' new-service onboarding time dropped from ~3 days
   (waiting on manual PagerDuty/DNS/cost-tag registration) to same-day.

   Didn't work: the default CI runner size was too small for
   payments-api's test suite, causing timeouts — fixed by making runner
   size an overridable parameter (now in v1.1).

   Decision: expanding to opt-in availability org-wide next quarter, still
   not mandatory.
   ```

6. **Expand availability broadly while keeping adoption opt-in for
   existing services**, and reserve mandating anything for *new* work
   only, initially — e.g. "every new service scaffolds from the golden
   path starting next quarter" is a far lower-trust-risk mandate than
   "every existing service must migrate by next quarter," because it
   doesn't force a disruptive migration onto teams with working systems
   and no bandwidth.

7. **Only mandate migration of existing services after the capability has
   a track record, a documented exception process, and dedicated
   migration support** — see
   [golden-path-template-design-for-developer-platforms](../golden-path-template-design-for-developer-platforms/SKILL.md)
   for the escape-hatch design that has to exist before any mandate, and
   staff real platform-team time to help teams migrate rather than just
   issuing the deadline and leaving teams to figure it out alone.

8. **Sunset the old path on a published deprecation timeline with clear
   support boundaries, not an abrupt cutoff.** Announce the sunset date
   well in advance, keep the old path supported (bug-fixed, not
   feature-developed) through a defined window, and track migration
   progress visibly so stragglers get proactive outreach rather than
   discovering the old path is gone the day they need it:
   ```markdown
   # Deprecation: legacy-deploy-script.sh

   - 2026-08-01: New services may no longer use legacy-deploy-script.sh;
     golden-path-service-standard is now the only path for new services.
   - 2026-11-01: legacy-deploy-script.sh enters bug-fix-only support;
     no new features.
   - 2027-02-01: legacy-deploy-script.sh is removed. Migration office
     hours run weekly from 2026-08-01 through the removal date.
   ```

9. **Treat a team's resistance as a diagnostic signal, not an obstacle to
   route around.** Before escalating a holdout team to leadership,
   confirm whether their resistance reflects a genuine gap (their use
   case isn't actually covered, or the escape-hatch process is too slow)
   versus simple change-aversion — the fix differs completely, and
   escalating a legitimate gap as if it were mere resistance both fails
   to fix the real problem and burns trust with that team for future
   rollouts.

## Best practices

- Run discovery (step 1) before scoping any tooling — a rollout's
  legitimacy problem almost always traces back to skipping this step, not
  to insufficient marketing later.
- Ship the narrowest version that addresses the most-cited pain point
  first, and expand from a proven base rather than trying to launch the
  full platform vision at once.
- Keep new capabilities opt-in until a pilot has produced honest,
  published evidence of value — and publish the pilot's failures
  alongside its wins.
- Reserve mandates for new work first; treat mandating migration of
  existing, working services as a separate, higher-trust-risk decision
  requiring its own track record and dedicated support.
- Publish deprecation timelines for whatever the new platform replaces,
  with a defined support window — an abrupt cutoff of the old way of
  doing things is one of the fastest ways to convert "the platform is
  slow to adopt" into "the platform team can't be trusted."
- Distinguish a legitimate objection from simple resistance before
  escalating a holdout team — investigate first, escalate only if the
  investigation confirms it's warranted.
- Measure adoption and sentiment throughout (see
  [developer-experience-measurement-and-platform-adoption](../developer-experience-measurement-and-platform-adoption/SKILL.md))
  rather than declaring success based on a mandate's compliance percentage
  alone — a high compliance rate achieved by mandate says nothing about
  whether developers actually find the platform valuable.

## Common pitfalls

- **Symptom:** The platform team ships a fully-featured service catalog
  after months of build time, announces it org-wide, and six months later
  fewer than 10% of services are registered and the catalog's own usage
  telemetry shows almost no organic traffic.
  **Fix:** This is the canonical "nobody asked for this" failure — the
  catalog was built from the platform team's assumption of what's useful,
  not from discovery interviews establishing what pain developers
  actually have. There's rarely a marketing fix for this after the fact;
  the credible response is to run the discovery step (step 1) retroactively,
  narrow the catalog's scope to whatever pain it does address, and relaunch
  as a much smaller pilot with a team that has that specific pain, rather
  than re-announcing the same broad tool louder.

- **Symptom:** A golden path is declared mandatory for all new services
  before it has ever had a single successful production deploy from a
  real team, and the first team forced onto it hits a broken build in
  front of their own deadline.
  **Fix:** Don't mandate anything before it's been validated end-to-end
  (see
  [golden-path-template-validation-and-testing](../golden-path-template-validation-and-testing/SKILL.md))
  and proven with at least one voluntary pilot team's real usage — a
  mandate with zero proof behind it converts every rollout problem into a
  trust problem, because the first team affected has no choice but to be
  the platform's unpaid QA.

- **Symptom:** The platform team abruptly shuts off the old deployment
  script with two weeks' notice because "the golden path replaces it,"
  and several teams' releases break because they hadn't migrated yet and
  had no warning window matched to their own release calendar.
  **Fix:** Publish a deprecation timeline with a real support window
  (step 8) — bug-fix-only support for a defined period, then removal —
  announced far enough in advance that teams can plan their migration
  around their own release calendar, not the platform team's.

- **Symptom:** A team publicly resists adopting the golden path, and the
  platform team escalates them to their engineering director as
  "blocking platform adoption," only to discover afterward that the team's
  actual workload genuinely isn't covered by any existing tier.
  **Fix:** Investigate the specific objection (step 9) before escalating
  — if it's legitimate, treat it as a signal to extend the golden path
  (a new tier, per
  [golden-path-template-design-for-developer-platforms](../golden-path-template-design-for-developer-platforms/SKILL.md))
  rather than as resistance to overcome, and repair the relationship with
  that team explicitly since an unwarranted escalation is itself a trust
  cost.

- **Symptom:** Adoption metrics show 95% of new services registered in
  the catalog, reported to leadership as a rollout success, while
  informal feedback channels are full of complaints that registration is
  "just a box everyone checks to stop the CI gate from failing."
  **Fix:** A high compliance number produced by a hard gate (a required
  CI check, a blocking policy) measures compliance, not adoption or
  satisfaction — cross-check any mandate-driven metric against the
  sentiment survey in
  [developer-experience-measurement-and-platform-adoption](../developer-experience-measurement-and-platform-adoption/SKILL.md)
  before reporting it as evidence the platform is valued rather than
  merely enforced.

## Worked example

**Scenario:** A 300-engineer org has no service catalog and no golden
path; new-service onboarding is inconsistent and every team has its own
CI/Dockerfile conventions copy-pasted from whichever service they touched
last. The platform team (newly formed, 4 engineers) wants to fix this
without repeating a prior, failed attempt at a company-wide "DevOps
standards" mandate that was abandoned after widespread pushback two years
earlier.

1. **Discovery**: the platform team interviews 10 teams across 3 business
   units. The most-cited pain point (7/10 teams) is new-service
   registration overhead — PagerDuty, DNS, cost tagging — each done
   manually and inconsistently, sometimes forgotten entirely until an
   incident reveals a service has no on-call rotation.
2. **Narrow scope**: the first golden-path tier ships covering only CI,
   Dockerfile, and automated registration for PagerDuty/DNS/cost-tags —
   explicitly deferring datastore provisioning and compliance scorecards
   to later tiers, keeping the initial build to six weeks.
3. **Pilot**: `checkout-team`, one of the interviewed teams actively
   mid-onboarding a new service that week, pilots it voluntarily. Four
   weeks, explicit decision checkpoint scheduled in advance.
4. **Honest results**: onboarding time for the pilot service drops from
   roughly 3 days (waiting on manual PagerDuty/DNS setup) to same-day;
   one real problem surfaces (the default CI runner is too small for a
   Java service's test suite) and is fixed before wider rollout. Both are
   published to the engineering-wide Slack channel together.
5. **Broad opt-in rollout**: the golden path becomes available org-wide,
   still opt-in, with office hours advertised weekly. Adoption and
   satisfaction are tracked per
   [developer-experience-measurement-and-platform-adoption](../developer-experience-measurement-and-platform-adoption/SKILL.md).
6. **Mandate scoped narrowly**: after two quarters and demonstrated
   adoption climbing past 60% voluntarily, the platform team mandates the
   golden path for *new* services only — existing services are left
   opt-in indefinitely, avoiding the earlier failed mandate's core
   mistake of forcing a disruptive migration onto teams with working
   systems.
7. **Old-path sunset, if ever pursued**: explicitly deferred — the
   platform team decides existing hand-rolled CI configs aren't causing
   enough ongoing harm to justify a forced migration and its trust cost,
   revisiting the decision only if a future incident traces back to one.

## Cross-references

- [developer-experience-measurement-and-platform-adoption](../developer-experience-measurement-and-platform-adoption/SKILL.md) — the measurement system that tells this rollout whether it's actually working, distinct from a mandate's compliance percentage.
- [golden-path-template-design-for-developer-platforms](../golden-path-template-design-for-developer-platforms/SKILL.md) — the escape-hatch and tiering design that has to exist before any mandate discussed in steps 6-7 here is credible.
- [golden-path-template-validation-and-testing](../golden-path-template-validation-and-testing/SKILL.md) — proving a golden path actually works end-to-end, a prerequisite this skill assumes before any mandate.
- [platform-engineering-team-topology-and-operating-model](../platform-engineering-team-topology-and-operating-model/SKILL.md) — running the platform as an internal product, which is the organizational stance behind treating rollout as earned adoption rather than a policy mandate.
