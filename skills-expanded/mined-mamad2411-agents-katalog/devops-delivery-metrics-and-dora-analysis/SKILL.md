---
name: devops-delivery-metrics-and-dora-analysis
description: >
  Measures and interprets the DORA four keys — deployment frequency, lead
  time for changes, mean time to restore (MTTR), and change failure rate —
  including how to compute each one correctly, common measurement
  pitfalls (vanity metrics, gaming the numbers, misclassifying a
  rollback), and how to use the results to drive process improvement
  rather than individual blame. Use when the user asks to "set up DORA
  metrics," "measure our deployment frequency/lead time," "what's our
  change failure rate," "are we an elite/high/medium/low performer," or
  "use delivery metrics to improve, not to blame the team."
license: Apache-2.0
compatibility: "Claude Code, GitHub Copilot, OpenAI Codex, Cursor, Gemini CLI"
metadata:
  domain: devops
  maturity: stable
---

# DevOps Delivery Metrics and DORA Analysis

## Purpose

The DORA (DevOps Research and Assessment) four keys — deployment
frequency, lead time for changes, mean time to restore, and change failure
rate — give a small, well-validated set of metrics that correlate software
delivery performance with organizational outcomes, in place of vague
impressions ("we feel slow") or vanity metrics (lines of code, number of
commits) that don't actually predict delivery capability. Measured
correctly, they surface *where* the delivery pipeline is actually
constrained — batch size, test reliability, deployment risk, incident
recovery — so improvement effort goes to the real bottleneck. Measured or
used carelessly, the same four numbers become a scoreboard that teams
learn to game, or a blame instrument pointed at individuals for something
that is almost always a systemic, cross-team property.

## When to use

- Setting up delivery-performance measurement for a team or organization
  for the first time.
- A stakeholder asks "are we a high/elite performer" or wants to compare
  teams' DORA numbers against each other or against industry benchmarks.
- Deciding what to improve next in the delivery pipeline, and wanting
  data on where the actual bottleneck is (build speed vs. review time vs.
  deployment risk vs. incident recovery) rather than guessing.
- Suspecting the current numbers are being gamed or don't reflect reality
  (e.g., deploy frequency is high but nothing meaningful is actually
  shipping, or change failure rate looks good only because failures
  aren't being classified as failures).
- A leader wants to use DORA metrics in a way that risks becoming a blame
  tool pointed at individual engineers or teams rather than a systemic
  improvement signal.

## Prerequisites & environment

- A source of truth for deploy events — the CI/CD platform's own deploy
  history (GitHub Actions/GitLab CI/Jenkins deployment job records, an
  Argo CD sync history) rather than a manually-maintained spreadsheet
  that will drift out of date.
- A source of truth for incidents and their resolution timestamps (an
  incident-management tool or at minimum a consistent log with declared/
  resolved times) — see
  [incident-response-and-on-call-management](../../../site-reliability-engineering/skills/incident-response-and-on-call-management/SKILL.md).
- A consistent definition, agreed across teams, of what counts as "a
  change" and "a deployment to production" before comparing any numbers —
  teams that deploy a monolith once a day and teams that deploy 50
  independent microservices are not directly comparable without care.
- Enough historical commit/PR/deploy timestamp data (ideally several
  months) to compute lead time and deployment frequency trends rather
  than a single noisy data point.
- Executive/leadership buy-in on using the metrics for systemic
  improvement, agreed *before* rollout — this materially changes whether
  teams report honestly or start gaming the numbers.

## Step-by-step guidance

1. **Define deployment frequency as how often code successfully reaches
   production, not how often a pipeline runs.** Count production deploy
   events specifically (not staging, not every CI run), from the CI/CD
   platform's own deploy record:
   ```
   deployment_frequency = count(production deploy events) / time_period
   ```
   A team deploying continuously (multiple times per day) and a team
   batching into one deploy every two weeks show up very differently
   here even with identical total code volume — this metric measures
   batch size and release cadence, not raw productivity.

2. **Define lead time for changes as commit-to-production time**, not
   ticket-created-to-done or idea-to-production (which conflates product
   discovery time with delivery-pipeline time):
   ```
   lead_time_for_change = deploy_timestamp - first_commit_timestamp
                            (for the commits included in that deploy)
   ```
   Measure the *median* (and a high percentile like p85/p90) across many
   changes, not a single change's time, since lead time is typically
   right-skewed (most changes are fast, a few are very slow and drag the
   mean).

3. **Define MTTR as the time from a production incident's detection/
   declaration to its resolution**, specifically for user-facing
   degradation caused by a deployed change (not scheduled maintenance,
   not an unrelated third-party outage):
   ```
   mttr = incident_resolved_timestamp - incident_declared_timestamp
   ```
   Pull declared/resolved timestamps from the incident-management system
   used in
   [incident-response-and-on-call-management](../../../site-reliability-engineering/skills/incident-response-and-on-call-management/SKILL.md),
   not from memory after the fact — post-hoc timestamp reconstruction is
   a common source of inaccurate MTTR data.

4. **Define change failure rate as the percentage of deploys that require
   remediation** — a hotfix, rollback, or a patch specifically caused by
   the deploy itself — over total deploys in the period:
   ```
   change_failure_rate = deploys_requiring_remediation / total_deploys
   ```
   Agree in advance on what counts as "requiring remediation": a
   rollback definitely counts; a same-day unrelated bug report probably
   doesn't; a hotfix specifically addressing a bug introduced by that
   deploy does. Write this definition down and apply it consistently —
   see step 6 for the most common way this metric gets gamed instead of
   measured honestly.

5. **Compute all four together and read them as a system, not four
   independent scores.** A team that improves deployment frequency by
   batching less risk per deploy, while lead time and change failure
   rate stay flat or improve, is genuinely improving; a team whose
   deployment frequency rises while change failure rate also rises is
   just shipping the same defects faster, not actually improving
   delivery performance.

6. **Watch for the classic ways these metrics get gamed, deliberately or
   not**, and correct for them rather than reporting the raw (misleading)
   number:
   - Deploy frequency inflated by deploying trivial/no-op changes just to
     move the number (a config comment change counted the same as a real
     feature deploy).
   - Change failure rate kept artificially low by not classifying a
     rollback as a "failure" if it happened quickly, or by quietly
     patching forward instead of formally rolling back so the incident
     is never logged against that deploy.
   - Lead time measured from ticket creation instead of first commit,
     making it look worse (or better) than actual delivery-pipeline
     performance by including product/planning time that isn't part of
     the engineering delivery pipeline at all.
   - MTTR measured only for incidents that got formally declared,
     undercounting degraded-but-not-declared incidents that took just as
     long to actually fix.

7. **Present the numbers as a team/system-level improvement signal, not
   an individual scorecard.** Never rank individual engineers by these
   metrics, and be explicit about that when introducing the measurement —
   the four keys describe the health of a delivery *system* (pipeline,
   process, architecture), which is a shared, cross-functional property,
   not an individual's output.

8. **Use the specific number to target the specific bottleneck** rather
   than a generic "improve everything" push:
   - High lead time, low deploy frequency → look at batch size, review
     turnaround, and pipeline speed; see
     [pipeline-failure-triage-and-recovery](../pipeline-failure-triage-and-recovery/SKILL.md)
     if flaky CI is inflating lead time.
   - High change failure rate → look at test coverage, staging fidelity,
     and progressive-delivery practices; see
     [blue-green-canary-deployments](../blue-green-canary-deployments/SKILL.md).
   - High MTTR → look at observability, rollback speed, and incident
     process; see
     [incident-response-and-on-call-management](../../../site-reliability-engineering/skills/incident-response-and-on-call-management/SKILL.md)
     and
     [blameless-postmortem-and-root-cause-analysis](../../../site-reliability-engineering/skills/blameless-postmortem-and-root-cause-analysis/SKILL.md).

## Best practices

- Automate metric collection from the CI/CD and incident-management
  systems' own event data — a manually-maintained spreadsheet drifts out
  of date and invites disputes over what actually happened.
- Report trends over rolling windows (e.g., trailing 4-13 weeks), not a
  single period's snapshot — all four metrics are noisy week to week,
  especially for lower-volume teams.
- Agree on and document the exact definitions (what counts as "a
  deployment," "a change requiring remediation," an "incident") across
  all teams being measured before comparing any numbers between them.
- Pair change failure rate and MTTR together when discussing risk — a
  team with a higher change failure rate but very fast MTTR (via
  progressive delivery and fast rollback) may carry less real user-facing
  risk than a team with a lower change failure rate but slow MTTR.
- Introduce DORA metrics with an explicit, stated commitment that they
  will not be used to rank or evaluate individuals, and hold to that
  commitment — trust, once broken here, causes teams to quietly
  optimize for the metric instead of for real delivery performance.
- Use the metrics to start a conversation about the specific bottleneck
  (step 8), not to declare a team's overall competence via a single
  elite/high/medium/low label.

## Common pitfalls

- **Symptom:** Deployment frequency looks impressively high, but the
  team's actual feature/fix throughput hasn't visibly changed.
  **Fix:** Check whether the count includes trivial/no-op deploys
  inflating the number (step 6); if so, either exclude them from the
  metric or accept that deploy frequency alone doesn't measure delivered
  value — pair it with lead time and change failure rate rather than
  reading it alone.

- **Symptom:** Change failure rate stays suspiciously low even though the
  team has clearly had several rough production incidents recently.
  **Fix:** Check how "requiring remediation" is being classified (step
  4/6) — a common cause is patching forward instead of formally logging
  a rollback/hotfix against the triggering deploy, which hides real
  failures from the metric. Fix the classification rule, not the number.

- **Symptom:** After introducing DORA metrics, engineers start batching
  smaller changes into fewer, larger deploys, and lead time and
  deployment frequency both quietly get worse instead of better.
  **Fix:** This is a sign the metrics are being perceived as a
  performance evaluation tool rather than a systemic improvement signal —
  revisit how the metrics were introduced and reaffirm they inform
  process changes, not individual/team scorecards (step 7); investigate
  whether a specific gate (e.g., an onerous manual approval) is driving
  the batching behavior.

- **Symptom:** Two teams' DORA numbers are compared directly in a
  leadership review, and the team with a monolithic, higher-risk
  architecture looks bad next to a team running independent
  microservices with much smaller per-deploy blast radius.
  **Fix:** DORA numbers are only meaningful compared against a team's own
  trend over time, not directly against a different team with a
  materially different architecture and deploy unit — present trends,
  not cross-team leaderboards.

- **Symptom:** Lead time is measured from Jira ticket creation to
  production, and it looks terrible, but investigation shows most of that
  time is tickets sitting in a backlog before anyone starts coding.
  **Fix:** Redefine lead time as commit-to-production (step 2) to isolate
  the engineering delivery pipeline's actual performance; track
  backlog/planning time as a separate, product-side metric if it matters,
  but don't conflate the two.

## Worked example

**Scenario:** A platform team wants to know why releases "feel slow" and
sets up DORA measurement for the `checkout-api` service over a trailing
8-week window.

1. **Deployment frequency**: pulled from the CI/CD platform's deploy job
   history, filtered to production-only successful deploys: median of
   1.2 deploys/day, trending flat over 8 weeks.
2. **Lead time for changes**: computed as `deploy_timestamp -
   first_commit_timestamp` for each deployed change set, median 6 hours,
   but p90 is 3.5 days — investigation shows the p90 tail is almost
   entirely PRs waiting on a single required manual reviewer who is often
   unavailable, not a slow pipeline.
3. **Change failure rate**: 9% of deploys in the window required a
   hotfix or rollback, using an agreed definition (any deploy followed
   within 24 hours by a hotfix/rollback targeting the same service
   counts) applied consistently rather than judgment-called per incident.
4. **MTTR**: median 22 minutes for incidents tied to a bad deploy, pulled
   from the incident tool's declared/resolved timestamps — fast, because
   the team already uses blue/green deploys with automated rollback.
5. **Reading the system, not four isolated numbers**: deploy frequency
   and MTTR are both healthy; the real bottleneck is the long tail of
   lead time caused by reviewer bottleneck, and a change failure rate of
   9% is higher than the team would like given how fast MTTR already is
   (meaning most of the "damage" from a bad deploy is already well
   contained — the real lever is reducing how often a bad deploy happens
   at all).
6. **Action, not blame**: the finding is presented as "our review process
   has a single point of failure inflating lead time's tail, and our
   change failure rate suggests test coverage gaps in the checkout
   pricing module specifically" — routed to
   [pipeline-failure-triage-and-recovery](../pipeline-failure-triage-and-recovery/SKILL.md)
   and a targeted test-coverage improvement, not reported as "the
   checkout team is slow."

## Cross-references

- [ci-cd-pipeline-design](../ci-cd-pipeline-design/SKILL.md) — the pipeline
  structure (stages, gates, parallelization) whose speed and reliability
  directly drive lead time and deployment frequency.
- [pipeline-failure-triage-and-recovery](../pipeline-failure-triage-and-recovery/SKILL.md) —
  flaky/failing CI is a common hidden driver of inflated lead time;
  fixing flakiness improves the metric at its root cause.
- [incident-response-and-on-call-management](../../../site-reliability-engineering/skills/incident-response-and-on-call-management/SKILL.md) —
  the incident process that produces the declared/resolved timestamps
  MTTR is computed from.
- [blameless-postmortem-and-root-cause-analysis](../../../site-reliability-engineering/skills/blameless-postmortem-and-root-cause-analysis/SKILL.md) —
  the blameless framing this skill insists on applying to delivery
  metrics as well as to incidents.
