---
name: developer-experience-measurement-and-platform-adoption
description: >
  Measures developer experience and platform adoption using established
  frameworks (SPACE, DX Core 4) combining survey-based and telemetry-based
  methods, and distinguishes real signal from vanity metrics. Use when a
  user asks to "measure developer experience," "track platform adoption,"
  "set up a DX survey," "pick platform engineering metrics," "prove the
  platform team's impact," or "avoid vanity metrics like catalog entity
  count or login counts."
license: Apache-2.0
compatibility: "Claude Code, GitHub Copilot, OpenAI Codex, Cursor, Gemini CLI"
metadata:
  domain: internal-developer-platform
  maturity: stable
---

# Developer Experience Measurement and Platform Adoption

## Purpose

A platform team without a measurement system defaults to measuring what's
easiest to count — catalog entity count, portal logins, number of
templates published — none of which tell you whether developers are
actually more productive, or even whether they're using the platform
voluntarily versus because they were told to. Real developer-experience
(DX) measurement combines **perception** (how developers actually feel
about their workflow, which only a survey can capture) with **telemetry**
(what actually happened — deploy frequency, lead time, self-service
adoption rate, which only instrumentation can capture), because either
alone is misleading: a fast pipeline developers hate using is a technical
success and an adoption failure; a beloved tool nobody's telemetry shows
any usage of is co-signing anecdote. This skill covers building that
combined measurement system using established frameworks — the SPACE
framework (Forsgren et al.) and DX Core 4 (Nicole Forsgren/DX) — and
avoiding the vanity-metric trap that makes a platform team's dashboard
look good while telling them nothing about whether the platform is
actually working.

## When to use

- Standing up developer-experience measurement for a platform team that
  currently has no metrics, or only has raw usage counts (logins, page
  views, catalog entities) with no outcome signal behind them.
- A leadership request to "prove the platform team's impact" or justify
  continued platform investment with data.
- Deciding what to include in a quarterly developer survey, or whether an
  existing survey is actually measuring anything actionable.
- A dashboard shows platform usage climbing while informal feedback
  (Slack complaints, ticket volume) suggests developer sentiment is
  getting worse — reconciling the two signals.
- Designing telemetry for a golden path, self-service API, or scaffolding
  tool so its actual usage (not just its existence) is measurable.

## Prerequisites & environment

- A survey tool capable of anonymous or pseudonymous responses (an
  internal survey platform, or a lightweight tool like a Google Form/
  Typeform) — anonymity matters specifically for sentiment questions,
  where attribution suppresses honest negative feedback.
- Telemetry sources already emitting events the platform can query:
  CI/CD pipeline logs (deploy frequency, lead time), the software catalog's
  own audit log (template usage, self-service action invocations), and
  version-control provider APIs (time from repo creation to first merged
  PR, as a proxy for time-to-first-contribution).
- A place to route both signals together — a BI tool or a simple
  dashboard (Grafana, a internal wiki page updated quarterly) that plots
  survey sentiment trends alongside telemetry trends, not two disconnected
  reports nobody cross-references.
- Executive or platform-leadership buy-in to publish results even when
  they're unflattering — a measurement system whose negative results get
  suppressed before publication isn't measuring anything real.
- Familiarity with the specific metrics in SPACE (Satisfaction &
  well-being, Performance, Activity, Communication & collaboration,
  Efficiency & flow) and DX Core 4 (Speed, Effectiveness, Quality, Impact)
  well enough to select a representative subset per category rather than
  every metric either framework lists — neither framework prescribes
  tracking all of its dimensions at once.

## Step-by-step guidance

1. **Pick one metric from each SPACE or DX Core 4 category rather than
   trying to track everything either framework lists.** Both frameworks
   are explicitly designed as a set of *categories* to sample from, not an
   exhaustive checklist — an org tracking 20 metrics across both
   frameworks produces a dashboard nobody reads and a survey nobody
   finishes. A minimal, defensible starting set combining both
   frameworks' categories:
   - **Satisfaction** (SPACE): a survey question on overall developer
     satisfaction with the internal platform/tooling.
   - **Speed** (DX Core 4) / **Efficiency & flow** (SPACE): median lead
     time from commit to production deploy.
   - **Activity** (SPACE): self-service action/template usage counts —
     but paired with an outcome metric (see step 3), never reported
     alone.
   - **Quality** (DX Core 4): change failure rate (deploys requiring a
     hotfix or rollback within 24 hours).
   - **Impact** (DX Core 4): a survey question asking developers to rate
     how much platform tooling helps (or hinders) them shipping their
     actual work, not just whether they used it.

2. **Design the survey to capture perception, run quarterly, and keep it
   short.** A 25-question survey has a completion-rate problem long before
   it has an insight problem. A representative core (5–8 questions,
   Likert-scale plus one free-text):
   ```
   1. Overall, how satisfied are you with the internal developer platform? (1-5)
   2. How much friction did you experience starting a new service in the
      last quarter? (1-5, 1 = a lot of friction)
   3. When you needed a new environment/resource, how easy was it to get
      it without filing a ticket or asking another team? (1-5)
   4. How confident are you that a production deploy will go smoothly? (1-5)
   5. What's the single biggest source of friction in your day-to-day
      workflow right now? (free text)
   ```
   Run it on a fixed cadence (quarterly is common) so trend lines are
   comparable, and publish aggregate results back to the org — including
   when they're flat or worse than last quarter.

3. **Instrument telemetry so "activity" metrics are always paired with an
   outcome, never reported alone.** Template-usage count answers "is the
   golden path being used" but not "did it help" — pair it with a metric
   that closes the loop, e.g. time from repo creation to first successful
   production deploy for scaffolded vs. hand-rolled services:
   ```sql
   -- illustrative query against a CI/catalog events warehouse
   SELECT
     scaffolded_from_template IS NOT NULL AS used_golden_path,
     PERCENTILE_CONT(0.5) WITHIN GROUP (ORDER BY
       first_prod_deploy_at - repo_created_at) AS median_time_to_first_deploy
   FROM service_lifecycle_events
   WHERE repo_created_at >= DATE_TRUNC('quarter', CURRENT_DATE)
   GROUP BY used_golden_path;
   ```
   A shorter median for `used_golden_path = true` is real evidence the
   golden path helps; a flat or worse number despite high template-usage
   counts means the template is being used but isn't actually reducing
   friction — a finding the usage count alone would have hidden.

4. **Track self-service adoption as a rate against the addressable
   population, not a raw count.** "230 self-service actions triggered
   this quarter" means nothing without a denominator — 230 out of 40
   teams that could have used it looks very different from 230 out of
   400 teams, and a raw count trending up can simply reflect headcount
   growth rather than adoption:
   ```
   self_service_adoption_rate =
     distinct_teams_using_self_service_this_quarter / total_teams_onboarded
   ```

5. **Explicitly name and retire vanity metrics** the moment they're
   identified, rather than leaving them on a dashboard alongside real
   signal where they dilute it. Common vanity metrics in this domain:
   catalog entity count (measures data entry, not adoption or value),
   portal login count (measures traffic, not outcome — a developer
   logging in five times to find the same broken link isn't a success),
   number of templates published (measures platform-team output, not
   developer-facing value), Slack channel member count for
   `#platform-help` (measures visibility, not satisfaction — a channel
   full of unresolved complaints has high membership and terrible
   sentiment).

6. **Reconcile survey and telemetry signal explicitly when they
   disagree**, rather than reporting whichever one looks better. A rising
   self-service adoption rate alongside falling satisfaction scores is a
   real, investigable finding (e.g. developers use the self-service tool
   because the alternative is worse, not because it's good) — surface
   both numbers on the same report, side by side, and treat a disagreement
   as a prompt for qualitative follow-up (the free-text survey question,
   or targeted interviews) rather than picking the flattering one.

7. **Segment results by team/cohort where volume allows**, not just an
   org-wide aggregate — an org-wide satisfaction score can hide that one
   large, vocal team is dragging the average down while most teams are
   satisfied, or the reverse (broad quiet dissatisfaction masked by one
   enthusiastic pilot team's scores).

8. **Report trend, not snapshot**, in every readout — a single quarter's
   number without the prior quarter's for comparison invites
   over-interpretation of noise; publish a rolling chart, and treat a
   single-quarter change smaller than the survey's typical quarter-to-
   quarter variance as noise, not signal.

## Best practices

- Sample a handful of metrics across SPACE/DX Core 4 categories rather
  than exhaustively instrumenting every dimension either framework lists
  — both are explicitly frameworks for *choosing what to measure*, not
  mandatory checklists.
- Always pair an activity metric (usage count) with an outcome metric
  (time saved, failure rate, satisfaction) in the same report — an
  activity number reported alone is the single most common vanity-metric
  failure mode in this domain.
- Keep the survey anonymous and short, and publish results — including bad
  ones — on a fixed cadence; a survey whose negative results quietly
  disappear trains developers to stop answering honestly, or to stop
  answering at all.
- Report adoption as a rate against the addressable population (teams
  onboarded, services eligible), not a raw count that conflates growth
  with adoption.
- Treat a disagreement between survey sentiment and telemetry as a
  finding to investigate, not a discrepancy to resolve by picking the
  better-looking number.
- Retire a vanity metric the moment it's identified rather than leaving
  it on the dashboard "for context" — a vanity metric next to real
  signal doesn't add context, it dilutes attention from the number that
  matters.

## Common pitfalls

- **Symptom:** The platform team's quarterly report shows catalog entity
  count and portal login count both trending up, and leadership concludes
  the platform is succeeding — while a parallel employee survey shows
  developer satisfaction with tooling flat or declining.
  **Fix:** Catalog entity count and login count are activity/traffic
  metrics with no outcome attached — replace or supplement them with a
  paired outcome metric (time-to-first-deploy, change failure rate) and
  the satisfaction survey question from step 2, and report both signals
  together rather than leading with the metric that looks best.

- **Symptom:** A quarterly developer survey gets a 12% response rate, and
  the resulting "average satisfaction" number swings wildly quarter to
  quarter with no clear cause.
  **Fix:** Low response rate usually means the survey is too long, too
  frequent, or its results visibly go nowhere. Shorten it to the core
  question set (step 2), reduce cadence if quarterly is too frequent for
  the org's size, and — most importantly — publish what changed as a
  direct result of the last survey's feedback, so completing it visibly
  matters.

- **Symptom:** Self-service action usage is reported as "1,400 invocations
  this quarter," presented as clear evidence of platform success, but
  nobody can say whether that's 5 teams using it 280 times each or 200
  teams using it 7 times each — very different adoption stories.
  **Fix:** Report the adoption rate (distinct teams / addressable teams)
  alongside the raw count, and segment by team (step 7) so a concentrated-
  usage pattern isn't mistaken for broad adoption.

- **Symptom:** A metric the platform team optimizes for (e.g. "% of new
  services created via golden path") climbs to 95%, but developer
  satisfaction and time-to-first-deploy both stay flat or worsen.
  **Fix:** This is a sign the metric itself became the target rather than
  a genuine proxy for developer value — likely because golden-path usage
  became mandatory (see
  [idp-adoption-rollout-and-change-management-strategy](../idp-adoption-rollout-and-change-management-strategy/SKILL.md)
  for the adoption failure modes this produces) rather than earned.
  Re-anchor the metric set on the paired outcome metrics from step 3/4,
  and investigate the satisfaction free-text responses for what the
  compliance number is actually hiding.

- **Symptom:** Leadership asks the platform team to "prove ROI" with a
  single number, and the team reports a metric (e.g. "10,000 catalog page
  views") that sounds impressive but that nobody on the team can actually
  explain the business meaning of when asked a follow-up question.
  **Fix:** Any metric the team can't explain the causal story behind
  ("this number went up because X happened, which we believe caused Y
  developer outcome") shouldn't be the headline number — lead instead
  with a paired activity/outcome metric (step 3) that has a defensible
  causal story, even if it's a smaller, less flattering number.

## Worked example

**Scenario:** A platform team supporting 60 engineering teams has been
reporting "portal monthly active users" and "catalog entity count" to
leadership for a year. Both numbers have climbed steadily, but a recent
all-hands Q&A surfaced multiple developers complaining that "the platform
makes simple things take longer." The platform lead wants a measurement
system that would have caught this instead of hiding it.

1. The team retires "portal monthly active users" and "catalog entity
   count" as headline metrics — reclassified internally as diagnostic-only,
   not reported to leadership.
2. A quarterly survey ships with the 5-question core set from step 2,
   anonymous, response rate tracked as its own metric (baseline: 61% of
   the org in quarter one).
3. Telemetry is added for median time-to-first-production-deploy,
   segmented by whether the service was scaffolded from a golden path
   (step 3's query), and self-service adoption rate against the 60-team
   denominator (step 4).
4. Quarter one results: survey satisfaction averages 3.1/5 (below the
   informal 4-ish the team assumed based on the enthusiasm of the two
   pilot teams they talked to most). Telemetry shows golden-path-
   scaffolded services have a *higher* median time-to-first-deploy than
   hand-rolled ones for one specific tier — the `advanced` tier, whose
   Kafka skeleton turns out to require a manual, undocumented broker
   allowlist step nobody had flagged.
5. The disagreement between "self-service adoption is climbing" (people
   are using the advanced tier) and "satisfaction is mediocre" (step 6)
   prompts the team to read the free-text responses, several of which
   name the exact Kafka allowlist friction point.
6. The fix (automating the allowlist step) ships the following quarter;
   the same telemetry query shows time-to-first-deploy for
   `advanced`-tier services drop below the hand-rolled baseline, and the
   next survey cycle shows satisfaction move to 3.6/5 — a real, causally
   explainable trend line the team can defend to leadership, built from
   paired survey and telemetry signal rather than a raw usage count.

## Cross-references

- [idp-adoption-rollout-and-change-management-strategy](../idp-adoption-rollout-and-change-management-strategy/SKILL.md) — using this skill's measurement system to sequence and validate a rollout, rather than mandating adoption and inferring success from compliance percentages alone.
- [platform-engineering-team-topology-and-operating-model](../platform-engineering-team-topology-and-operating-model/SKILL.md) — treating the platform as an internal product means its team needs exactly this kind of customer-facing measurement system, not just uptime/ticket metrics.
- [golden-path-template-validation-and-testing](../golden-path-template-validation-and-testing/SKILL.md) — telemetry from validated golden-path scaffolds is the source data behind the paired activity/outcome metrics described in step 3 here.
