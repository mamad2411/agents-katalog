---
name: service-scorecards-and-maturity-model-design
description: >
  Designs service scorecards and maturity models — production-readiness,
  security posture, and ownership/on-call coverage checks — as implemented
  in Cortex Scorecards, OpsLevel Rubrics, or Backstage tech-insights, and
  how to weight/tier multiple checks into a single score without teams
  gaming it. Use when a user asks to "design a production-readiness
  scorecard," "set up a Cortex Scorecard or OpsLevel Rubric," "weight
  scorecard checks," "define maturity levels/tiers for services," or "stop
  teams from gaming their scorecard score."
license: Apache-2.0
compatibility: "Claude Code, GitHub Copilot, OpenAI Codex, Cursor, Gemini CLI"
metadata:
  domain: internal-developer-platform
  maturity: stable
---

# Service Scorecards and Maturity Model Design

## Purpose

A scorecard is a platform team's attempt to answer, at a glance and at
scale, "is this service actually production-ready, secure, and owned by
someone who'll get paged when it breaks" — without a human auditing every
service by hand. Done well, it turns tribal knowledge ("everyone knows
`checkout-api` doesn't really have an on-call rotation") into a queryable,
enforceable signal. Done poorly, it becomes a number teams learn to
optimize directly instead of the underlying practice it was meant to
proxy — a team adds a stub `runbook.md` with one sentence in it, the
"has a runbook" check goes green, and the service is exactly as
operationally fragile as before. This skill covers designing the checks,
the weighting/tiering scheme that combines them into a score or maturity
level, and the structural choices that make gaming the score harder than
actually improving the practice it measures — as implemented in
Cortex Scorecards, OpsLevel Rubrics, or a Backstage tech-insights-based
equivalent.

## When to use

- Standing up a new production-readiness, security-posture, or
  ownership/on-call scorecard from scratch in Cortex, OpsLevel, or
  Backstage.
- Deciding how to combine several individual checks (has an on-call
  rotation, has a runbook, passes a vulnerability scan, has an SLO
  defined) into one overall score or maturity tier (Bronze/Silver/Gold or
  similar).
- A scorecard already exists but most services are stuck at the lowest
  tier indefinitely, or conversely every service shows 100% with no
  differentiation — either signals a design problem, not a compliance
  problem.
- Reviewing a scorecard rubric before or after a security or reliability
  incident to check whether the check that should have caught the gap
  actually would have (and if not, why the rubric didn't flag it).
- Investigating a service that shows a high scorecard score but had a
  preventable incident — deciding whether a check needs to become
  stricter or more evidence-based rather than assuming the tooling is
  broken.

## Prerequisites & environment

- A catalog tool with scorecard/rubric support already populated with
  service metadata — Cortex (`cortex.yaml` + Scorecard rules), OpsLevel
  (`opslevel.yml` + Rubric Checks), or Backstage with the
  `@backstage/plugin-tech-insights-backend` fact-retriever/check model —
  see
  [no-code-idp-service-catalog-tools-port-cortex-opslevel](../no-code-idp-service-catalog-tools-port-cortex-opslevel/SKILL.md)
  for choosing and standing up one of these.
- Machine-queryable data sources for each check, not just self-reported
  fields: a PagerDuty/Opsgenie API for on-call schedule depth, a
  vulnerability scanner's (Snyk/Trivy/Dependabot) findings API for
  security checks, an SLO/observability tool's config for latency/error
  budgets, and the catalog's own metadata for ownership.
- Agreement from the stakeholders who own each category (SRE/platform for
  production-readiness, security for posture, engineering leadership for
  ownership/on-call) on what "passing" actually means for their category
  — a scorecard designed unilaterally by the platform team without their
  input tends to measure what's easy to query, not what those
  stakeholders actually care about.
- A place the score is visible to the teams being scored (a catalog page,
  a dashboard) and, ideally, to leadership — a scorecard nobody sees
  provides no incentive, positive or perverse.
- Familiarity with the org's existing DX/adoption measurement practice,
  since a scorecard is itself a metric subject to the same vanity-metric
  and gaming risks — see
  [developer-experience-measurement-and-platform-adoption](../developer-experience-measurement-and-platform-adoption/SKILL.md).

## Step-by-step guidance

1. **Start from the operational risk each category represents, not from
   what's easiest to query.** Three common categories and the risk each
   answers:
   - **Production readiness** — will this service degrade gracefully and
     recover from a bad deploy or dependency outage (health checks,
     rollback capability, defined SLOs).
   - **Security posture** — is this service's attack surface and
     dependency chain actively monitored and patched (vulnerability
     scanning enabled, no criticals open past a grace period, secrets not
     hardcoded).
   - **Ownership / on-call coverage** — will a human who can actually fix
     it be paged when it breaks (a real rotation, an escalation policy,
     not just a Slack channel with a stale pinned message).
   Write down the risk each check answers *before* writing the check
   itself — a check with no clear risk behind it is a candidate for being
   cut, not added.

2. **Prefer machine-verifiable checks over self-attestation wherever a
   data source exists.** A checkbox a team ticks themselves ("we have a
   runbook: yes/no") is the single easiest thing to game; a check that
   queries an actual system is not:
   ```yaml
   # Cortex Scorecard rule — self-attested (weak)
   - title: Has a runbook
     expression: "entity.hasMetadataField('has_runbook')"   # team just sets this true

   # Cortex Scorecard rule — machine-verified (strong)
   - title: Has a runbook
     expression: "entity.hasDocument('runbook') && entity.documents('runbook').last_updated_days_ago() < 180"
   ```
   The stronger version checks both that a runbook document actually
   exists in the linked docs system *and* that it was updated recently
   enough to be plausibly still accurate — closing the "stub file from
   two years ago" gap the weaker version leaves open.

3. **Weight checks by blast radius, not equally.** A production-readiness
   scorecard that gives "has a README" the same weight as "has automated
   rollback on failed health check" produces a score where a team can
   offset a genuinely dangerous gap with several trivial, easy passes.
   Weight by consequence of the gap, and keep the weighting visible and
   justified:
   ```yaml
   name: Production Readiness
   rules:
     - title: Has a README with an architecture overview
       expression: "entity.hasDocument('readme')"
       weight: 1
     - title: Has a defined and tracked latency SLO
       expression: "entity.hasMetadata('slo.latency_p99_ms')"
       weight: 3
     - title: Automated rollback wired to a health-check alarm
       expression: "entity.hasMetadata('deploy.auto_rollback_enabled') && entity.metadata('deploy.auto_rollback_enabled') == true"
       weight: 5
     - title: No open critical vulnerabilities older than 30 days
       expression: "entity.vulnCount('critical', olderThanDays=30) == 0"
       weight: 5
   ```

4. **Gate top tiers on specific critical checks, not just a weighted-sum
   threshold.** A blended score lets a team hit "Gold" by acing everything
   *except* the one check that actually matters, if enough low-weight
   checks compensate numerically. Require specific high-consequence
   checks to independently pass before a tier is awarded at all, on top
   of the weighted sum:
   ```yaml
   levels:
     - name: Bronze
       min_score: 0
     - name: Silver
       min_score: 40
       required_rules: ["Has a defined and tracked latency SLO"]
     - name: Gold
       min_score: 80
       required_rules:
         - "Automated rollback wired to a health-check alarm"
         - "No open critical vulnerabilities older than 30 days"
   ```
   This mirrors OpsLevel's Rubric levels and Cortex's rule-level
   assignment: a service failing a `required_rules` entry is capped below
   that tier regardless of its total weighted score.

5. **Verify on-call coverage checks depth, not mere existence.** "Has a
   PagerDuty schedule" is true for a schedule with one person who's
   "always on" and has been on vacation, unreachable, for two weeks — that
   is not coverage:
   ```yaml
   - title: On-call rotation has at least 2 rotating members and an escalation policy
     expression: >
       entity.pagerDutySchedule().rotationMembers().length >= 2 &&
       entity.pagerDutySchedule().hasEscalationPolicy()
     weight: 4
   ```

6. **Implement the same scorecard concept in OpsLevel via a Rubric of
   Checks with category weighting**, if OpsLevel is the chosen tool
   instead of Cortex:
   ```hcl
   resource "opslevel_rubric_check_has_service_config" "slo_defined" {
     name     = "Latency SLO defined and tracked"
     enabled  = true
     category = opslevel_rubric_category.production_readiness.id
     level    = opslevel_level.silver.id
     filter   = opslevel_filter.production_services.id
   }

   resource "opslevel_rubric_check_alert_source_usage" "no_critical_vulns" {
     name      = "No open critical vulnerabilities > 30 days"
     enabled   = true
     category  = opslevel_rubric_category.security.id
     level     = opslevel_level.gold.id
   }
   ```
   Keep category weighting and level assignment identical in intent to
   the Cortex version in step 4 — same required-check-per-level gating,
   different vendor syntax.

7. **Build in anti-gaming detection, not just anti-gaming intent.** Track
   score volatility and timing as its own signal: a service that jumps
   from Bronze to Gold in the week before a quarterly business review, or
   whose score consistently spikes right before a reporting deadline and
   drifts back down after, is a service worth a manual spot-check, not
   necessarily a genuine improvement. Periodically (e.g. quarterly)
   manually audit a random sample of high-scoring services against the
   actual practice a check claims to verify (open the linked runbook and
   read it, not just confirm the link resolves).

8. **Review and version the rubric itself like code**, with an owner per
   category and a change-review process — a scorecard whose rules never
   change as practices mature calcifies into either an unattainable bar
   nobody clears or a rubber-stamp everyone clears trivially. Re-baseline
   entry-level requirements to reality on rollout (see the phased
   rollout pattern in
   [no-code-idp-service-catalog-tools-port-cortex-opslevel](../no-code-idp-service-catalog-tools-port-cortex-opslevel/SKILL.md)),
   then raise the bar incrementally on a published cadence.

## Best practices

- Anchor every check to a specific, named operational risk it answers;
  cut checks that exist only because a data source happened to be easy to
  query.
- Prefer machine-verified checks (query a real system) over
  self-attested checkbox fields wherever a data source exists at all —
  self-attestation should be the fallback for the rare check with no
  automatable source, not the default.
- Weight checks by consequence, and gate the top maturity tier on
  specific required checks in addition to a weighted-sum threshold, so a
  genuinely dangerous gap can't be numerically offset by unrelated easy
  passes.
- Treat the scorecard itself as an artifact to measure for gaming signal
  — track score volatility and spot-audit high scorers — rather than
  trusting a green check forever once it's been achieved once.
- Make category ownership explicit (security owns the security category's
  rules, SRE owns production-readiness) so rule changes go through the
  people who understand the risk, not solely the platform team.
- Publish the rubric's rules and weights openly to the teams being
  scored — an opaque scoring formula invites suspicion and gaming far
  more than a transparent one that's simply demanding.
- Re-baseline and phase in new requirements rather than launching a
  rubric where every service instantly fails — an unattainable bar on
  day one teaches teams to ignore the scorecard entirely, the same
  adoption failure covered in
  [idp-adoption-rollout-and-change-management-strategy](../idp-adoption-rollout-and-change-management-strategy/SKILL.md).

## Common pitfalls

- **Symptom:** A team's "has a runbook" check goes green the same day a
  one-line stub file (`# Runbook\nTODO`) is committed, and the check
  never verifies content or freshness again.
  **Fix:** Replace existence-only checks with the machine-verified
  pattern from step 2 (freshness threshold, minimum content signal like a
  linked doc's word count or required section headings) — a check that
  only confirms a file exists is trivially gameable and should be treated
  as a placeholder, not a finished check.

- **Symptom:** A service scores "Gold" overall on the production-
  readiness scorecard, then has a multi-hour outage because it had no
  automated rollback and the on-call engineer paged had left the company
  two months earlier — both gaps the rubric nominally covered.
  **Fix:** This is the blended-weighted-sum failure mode from step 4 — the
  service likely offset those two high-consequence gaps with enough
  low-weight passes (README, tags, naming convention) to clear the
  threshold anyway. Add both failed checks to `required_rules` for the
  tier the service was awarded, so a critical gap caps the tier
  regardless of the weighted total, and audit other "Gold" services for
  the same blind spot.

- **Symptom:** Scorecard compliance across the org climbs from 40% to 95%
  in the two weeks before a leadership review, then quietly drifts back
  down to 60% the following month.
  **Fix:** This spike-and-decay pattern is a strong gaming signal, not a
  genuine improvement — cross-reference with
  [developer-experience-measurement-and-platform-adoption](../developer-experience-measurement-and-platform-adoption/SKILL.md)'s
  guidance on treating a metric the team started optimizing directly as
  compromised; spot-audit a sample of the newly-passing services against
  the actual underlying practice, and consider tracking score volatility
  itself as a dashboard metric so a future spike is visible in real time
  rather than only in hindsight.

- **Symptom:** An "on-call coverage" check passes because a PagerDuty
  schedule technically exists, but it has exactly one person on it who
  has been unreachable (long leave, left the team) for weeks.
  **Fix:** Check rotation depth and escalation policy presence (step 5),
  not mere schedule existence — a schedule with one permanent member is
  functionally the same as no coverage the moment that person is
  unavailable.

- **Symptom:** Two years after launch, every service in the catalog still
  shows Bronze because the entry bar (SLOs defined, on-call rotation
  live) was set at "fully mature" from day one, and teams stopped
  checking the scorecard because it never moves regardless of real
  improvement.
  **Fix:** Re-baseline the entry tier to what's realistically true today
  for most services, and raise the bar incrementally per step 8 as each
  prior tier's adoption becomes routine — an unattainable rubric produces
  the same disengagement as no rubric at all, just with extra dashboard
  real estate.

## Worked example

**Scenario:** A platform team is rolling out a Cortex Production
Readiness scorecard across 80 services. An earlier, informal spreadsheet-
based audit found: most services have a README, about a third have any
kind of SLO defined, on-call rotations exist for high-tier services but
several are single-person, and two services had a runbook stub with no
real content that nobody had opened in over a year.

**Design decisions applied from this skill:**
1. Categories: Production Readiness (SLOs, rollback, health checks),
   Security Posture (vuln scanning, no aged criticals), Ownership
   (rotation depth, escalation policy) — each mapped to a named risk from
   step 1.
2. Runbook check upgraded to the machine-verified version from step 2
   (existence + freshness), directly closing the stub-file gap the
   earlier informal audit found.
3. Weighting applied per step 3: README weight 1, SLO weight 3, automated
   rollback weight 5, no-aged-criticals weight 5.
4. Tier gating per step 4 — Gold requires both `automated rollback` and
   `no aged criticals` as `required_rules`, not just a high weighted sum.
5. On-call check upgraded per step 5 to require ≥2 rotation members and
   an escalation policy, directly targeting the single-person-schedule
   finding from the informal audit.

**Rollout:** Bronze entry bar set to "README + any on-call schedule at
all" (what ~90% of services already clear), avoiding the unattainable-
bar pitfall. Silver requires the SLO check and 2-person rotation depth,
targeted for month three once teams have had time to define SLOs. Gold
(requiring both hard-gated checks) is explicitly framed as a 6-month
target, not a launch-day expectation.

**Quarter-two review:** Score volatility tracking (step 7) flags one
service whose score jumped from 45 to 92 in the ten days before a
leadership all-hands. A spot-audit finds its "runbook" doc passed the
freshness check because a script had been auto-touching the file's
timestamp weekly without changing its content — a gaming pattern the
freshness check alone didn't catch. The check is tightened to also
require a minimum meaningful diff (not just a touched mtime) between
audits, closing that specific loophole for the next cycle.

## Cross-references

- [no-code-idp-service-catalog-tools-port-cortex-opslevel](../no-code-idp-service-catalog-tools-port-cortex-opslevel/SKILL.md) — standing up Cortex Scorecards or OpsLevel Rubrics as a product decision, and the phased-rollout/re-baselining pattern referenced in step 8 here.
- [developer-experience-measurement-and-platform-adoption](../developer-experience-measurement-and-platform-adoption/SKILL.md) — the general vanity-metric and Goodhart's-law risk a scorecard score is itself subject to, and the paired activity/outcome measurement discipline that also applies to scorecard compliance percentages.
- [idp-adoption-rollout-and-change-management-strategy](../idp-adoption-rollout-and-change-management-strategy/SKILL.md) — sequencing a new or tightened scorecard rollout so it doesn't repeat the mandatory-adoption failure modes covered there.
- [platform-engineering-team-topology-and-operating-model](../platform-engineering-team-topology-and-operating-model/SKILL.md) — assigning category ownership (security, SRE, engineering leadership) for scorecard rules as part of the platform team's broader operating model.
