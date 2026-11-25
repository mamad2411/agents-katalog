---
name: slo-sli-and-error-budget-design
description: >
  Guides choosing good Service Level Indicators (request-based ratios vs.
  window-based aggregates), setting realistic Service Level Objectives
  backed by data instead of arbitrary "five nines" targets, writing an
  error-budget policy that defines what happens when the budget is spent
  (freezing non-essential launches), and designing multi-window,
  multi-burn-rate alerting so budget exhaustion pages on-call before users
  notice. Use when a user asks to "define an SLO/SLI for a service", "set
  an error budget", "decide what happens when we blow our error budget",
  "write a burn-rate alert", or "stop every minor blip from paging us."
license: Apache-2.0
compatibility: "Claude Code, GitHub Copilot, OpenAI Codex, Cursor, Gemini CLI"
metadata:
  domain: site-reliability-engineering
  maturity: stable
---

# SLO/SLI and Error Budget Design

## Purpose

Without an explicit, numeric target for "reliable enough," reliability
work has no stopping point and no shared language with product: engineers
default to chasing the highest reliability technically possible, product
pushes for the fastest possible ship velocity, and every outage becomes an
argument instead of a data point. Service Level Objectives (SLOs), backed
by Service Level Indicators (SLIs) that actually reflect user experience,
turn "is this reliable enough" into a measurable question, and the error
budget (the allowed unreliability implied by the SLO) turns "should we
slow down and fix reliability, or keep shipping features" into a policy
decision made in advance rather than an argument during an incident. This
skill covers choosing SLIs that mean what you think they mean, setting an
SLO from evidence rather than aspiration, writing an error-budget policy
with real teeth, and alerting on budget *burn rate* — not just breach at
the end of the window — so a fast-burning incident pages someone while
there's still budget left to save.

## When to use

- Defining an SLI/SLO for a new or existing service, endpoint, or critical
  user journey (checkout, login, search).
- A team argues about whether a given outage "matters" with no shared
  definition of acceptable reliability.
- Deciding what happens when a service exceeds its error budget — whether
  launches should freeze, and who has authority to override that.
- Alerts page on every minor blip, or conversely an SLO is breached for
  days before anyone notices — both point to missing/incorrect burn-rate
  alerting.
- Reviewing whether an existing SLO target (often picked with no data,
  e.g. "99.99%") is actually achievable or meaningful given current
  architecture and dependency reliability.

## Prerequisites & environment

- A metrics pipeline that can compute request-level success/failure and
  latency at the right measurement point (ideally load balancer/edge/CDN,
  not just application-level 200 OK, which misses client timeouts and
  upstream failures) — see the
  [Prometheus and Grafana monitoring stack](../../../observability-and-platform-extras/skills/prometheus-and-grafana-monitoring-stack/SKILL.md)
  skill for the underlying scrape/PromQL/alerting mechanics; this skill
  assumes that stack (or an equivalent) is already in place.
- A defined list of critical user journeys for the service (not every
  internal endpoint needs its own SLO).
- At least 4-6 weeks of historical latency/success data to set a
  data-informed target rather than guessing.
- Product/business stakeholder buy-in — an error-budget policy that
  freezes launches only works if product agrees to it *before* the budget
  is spent, not during the argument that follows.
- A paging tool (PagerDuty, Opsgenie, Grafana OnCall, or equivalent) wired
  to receive burn-rate alerts — see
  [incident-response-and-on-call-management](../incident-response-and-on-call-management/SKILL.md).

## Step-by-step guidance

1. **Pick the SLI type per user journey.**
   - **Request-based SLI** (preferred whenever you have per-request
     telemetry): the ratio of "good" events to total valid events over a
     rolling window.
     ```
     availability_sli = good_requests / valid_requests
     # good_requests: status not in {5xx} AND latency < threshold
     # valid_requests: excludes requests the user/client aborted before
     #                 the server could respond (not the server's fault)
     ```
   - **Window-based SLI** (use when you can't count individual requests —
     batch jobs, cron pipelines, systems with no per-request telemetry):
     the fraction of fixed time windows (e.g. every 1 minute) that meet a
     bar, rather than a fraction of requests.
     ```
     window_sli = good_windows / total_windows
     # a "good" 1-minute window: e.g. the batch job's queue depth stayed
     # below N, or the daily job completed before its deadline
     ```
   - Measure as close to the user as possible: a server-side 200 OK ratio
     that excludes timeouts, connection resets, and client-observed
     errors looks healthy while users are actually failing.

2. **Set the SLO from evidence, with room for a budget to exist.**
   Pull 90 days of the chosen SLI and look at the actual achieved
   reliability, not the aspirational one. Set the target below what's
   realistically achievable with current architecture, high enough to
   matter to users, and low enough that a budget genuinely exists to
   spend. Common allowed-downtime table for a 30-day rolling window:

   | SLO      | Allowed downtime / 30 days | Allowed downtime / 90 days |
   |----------|---------------------------:|---------------------------:|
   | 99%      | 7h 18m                     | 21h 54m                    |
   | 99.9%    | 43m 50s                    | 2h 11m                     |
   | 99.95%   | 21m 54s                    | 1h 5m 42s                  |
   | 99.99%   | 4m 23s                     | 13m 9s                     |
   | 99.999%  | 26s                        | 1m 19s                     |

   A target of **100%** is not a valid SLO — it implies zero error budget,
   which means every single failed request is a policy violation, which
   makes the policy meaningless (see Common pitfalls).

3. **Compute the error budget and burn rate.**
   ```
   error_budget = (1 - SLO) * total_valid_requests_in_window
   burn_rate    = observed_error_rate / (1 - SLO)
   # burn_rate of 1.0 = consuming the budget exactly on schedule to hit 0
   #   right at the end of the window
   # burn_rate of 14.4 against a 30-day window exhausts the ENTIRE
   #   budget in about 1 hour if sustained
   ```

4. **Write an error-budget policy with explicit thresholds and actions.**
   Draft this with product/eng leadership *before* it's needed:

   | Budget consumed (rolling 30d) | Action |
   |---|---|
   | 0-50% | Normal operation. Ship features as planned. |
   | 50-75% | Reliability review required before any launch with material availability/latency risk (new dependency, schema migration, traffic-shifting change). |
   | 75-100% | Freeze non-essential feature launches. Only bug fixes, security patches, and reliability work may deploy. |
   | >100% (budget exhausted) | Mandatory incident postmortem (see [blameless-postmortem-and-root-cause-analysis](../blameless-postmortem-and-root-cause-analysis/SKILL.md)) and leadership sign-off required to resume feature launches, even after the rolling window recovers. |

   Wire the freeze into the deployment pipeline itself where possible
   (a gate that blocks non-reliability-labeled deploys once budget crosses
   75%) rather than relying on people remembering — see
   [environment-promotion-strategy](../../../devops/skills/environment-promotion-strategy/SKILL.md)
   for how to add pipeline gates.

5. **Alert on burn rate with multiple windows, not on breach at the end
   of the period.** Checking "did we breach 99.9% this month" on the last
   day of the month means you find out a month late. Use short + long
   window pairs so a fast, severe burn pages immediately while a slow,
   sustained burn creates a lower-urgency ticket:

   ```promql
   # Fast-burn (page): would exhaust a 30-day budget in ~1 hour if
   # sustained. Requires both a 5m and a 1h window to agree, so a single
   # noisy minute doesn't page.
   (
     sum(rate(http_requests_total{job="checkout",status_code=~"5.."}[5m]))
       / sum(rate(http_requests_total{job="checkout"}[5m]))
     > 14.4 * (1 - 0.999)
   )
   and
   (
     sum(rate(http_requests_total{job="checkout",status_code=~"5.."}[1h]))
       / sum(rate(http_requests_total{job="checkout"}[1h]))
     > 14.4 * (1 - 0.999)
   )

   # Slow-burn (ticket, not page): would exhaust the budget in ~5 days if
   # sustained. Confirmed over 6h and 3d windows.
   (
     sum(rate(http_requests_total{job="checkout",status_code=~"5.."}[6h]))
       / sum(rate(http_requests_total{job="checkout"}[6h]))
     > 6 * (1 - 0.999)
   )
   and
   (
     sum(rate(http_requests_total{job="checkout",status_code=~"5.."}[3d]))
       / sum(rate(http_requests_total{job="checkout"}[3d]))
     > 6 * (1 - 0.999)
   )
   ```
   Route the fast-burn alert to page primary on-call immediately
   (`severity: critical`); route the slow-burn alert to a ticket/Slack
   channel for the service owner to investigate within the business day
   (`severity: warning`).

6. **Review quarterly.** Compare the SLO against actual support-ticket
   volume, churn signals, and whether the budget was ever meaningfully
   spent. An SLO nobody ever comes close to burning is probably stricter
   than users need (over-investment in reliability); a budget
   permanently at 0% means the target is unrealistic for current
   architecture — fix the architecture or relax the target deliberately,
   don't just ignore the breach.

## Best practices

- Limit each service to a handful of SLOs (typically one availability and
  one latency SLO per critical user journey) — a service with 20 SLIs
  produces noise, not clarity, and nobody reviews them.
- Prefer SLIs measured at the edge/load balancer over pure
  application-log-derived metrics; the edge sees timeouts and connection
  failures the app process never gets a chance to log.
- Express the SLO and its policy in a written, versioned document (plain
  markdown or a machine-readable format like OpenSLO) checked into the
  same repo as the service, not a slide deck that goes stale.
- Give the error-budget policy an explicit, named owner/approver for the
  "freeze" and "override the freeze" decisions — a policy with no
  enforcement path is a suggestion, not a policy.
- Use burn-rate alerts (not static threshold-on-breach alerts) so
  detection scales with severity: a total outage should page in minutes,
  not wait for a slow-moving monthly average to cross a line.
- Recompute the SLO's realism whenever a major dependency or
  architecture change lands — an SLO calibrated against the old
  architecture may no longer be achievable (or may now be too loose).

## Common pitfalls

- **Symptom:** The SLO is set to 100% (or effectively 99.999%+ with no
  data behind it), and every single failed request or transient blip
  triggers an "SLO violation" conversation.
  **Fix:** There is no such thing as a 100% SLO in practice — pick a
  target below the historically observed baseline so a real error budget
  exists to spend on both operational noise and calculated risk-taking.

- **Symptom:** The SLI shows 99.98% success measured at the application
  server, but users are filing tickets about failed checkouts.
  **Fix:** The SLI is measuring the wrong thing — likely excluding
  timeouts, load-balancer 5xxs, or client-side failures that never reach
  the app's own logs. Move the measurement point to the edge/load
  balancer, or explicitly fold client-observed failures (via RUM/synthetic
  checks) into the "valid requests" denominator.

- **Symptom:** The team only discovers an SLO breach when someone
  manually checks the dashboard at month-end, days after the incident
  that caused it.
  **Fix:** No burn-rate alerting exists — only an end-of-window
  threshold check. Add multi-window, multi-burn-rate alerts (step 5)
  so a fast burn pages within the hour and a slow burn tickets within
  the day.

- **Symptom:** The error-budget policy document says launches freeze at
  75% budget consumption, but the last three times that happened, product
  shipped anyway with no pushback.
  **Fix:** The policy has no enforcement mechanism — it's a suggestion.
  Wire the freeze into an automated pipeline gate keyed off the current
  burn-rate/budget-remaining metric (see
  [environment-promotion-strategy](../../../devops/skills/environment-promotion-strategy/SKILL.md)),
  and name an explicit approver for any override.

- **Symptom:** Ten different SLIs are defined for one service and nobody
  can say, off the top of their head, what any of them currently read.
  **Fix:** Consolidate to the vital few — one availability and one
  latency SLO per critical user journey is usually enough. Retire the
  rest or fold them into recording rules used only for deep debugging.

## Worked example

**Service:** `checkout-service`. **User journey:** completing a purchase.

- **SLI:** proportion of checkout requests, measured at the load
  balancer, that return a non-5xx status *and* complete in under 300ms,
  divided by all checkout requests the load balancer accepted (excludes
  requests the client cancelled before the LB could respond).
- **SLO:** 99.9% over a trailing 30-day window — chosen because 90 days
  of historical data showed the service already achieving 99.92-99.95%
  most months, leaving a believable, non-zero budget while still
  representing a real commitment above the observed floor.
- **Error budget:** 43m 50s of allowed "bad" time per 30-day window
  (from the table in step 2).
- **Burn-rate alerts:** the PromQL pair from step 5, with the fast-burn
  rule routed to PagerDuty as `severity: critical` (pages primary
  checkout on-call) and the slow-burn rule routed to the `#checkout-eng`
  Slack channel as `severity: warning`.
- **Error-budget policy:** the table from step 4, with the "freeze
  non-essential launches" gate implemented as a required GitHub Actions
  check (`error-budget-status`) that queries current burn against the
  SLO and fails any PR labeled `feature` (but not `bugfix`/`security`)
  when consumption exceeds 75%. The VP of Engineering is the named
  approver for overriding the gate.
- **Outcome:** three months in, a botched schema migration burns 60% of
  the budget in two days. The fast-burn alert pages on-call within 40
  minutes of the regression starting; the pipeline gate automatically
  blocks the next feature PR; the incident goes through the postmortem
  process (see cross-references) with the resulting action items
  reviewed by the same VP before the freeze is lifted.

## Cross-references

- [incident-response-and-on-call-management](../incident-response-and-on-call-management/SKILL.md) — burn-rate alerts are the primary signal that pages on-call; escalation and severity handling live there.
- [blameless-postmortem-and-root-cause-analysis](../blameless-postmortem-and-root-cause-analysis/SKILL.md) — error-budget exhaustion should trigger the same structured postmortem process as any other significant incident.
- [capacity-planning-and-load-testing](../capacity-planning-and-load-testing/SKILL.md) — load/stress test results tell you whether a target SLO is even achievable under peak demand before you commit to it.
- [Prometheus and Grafana monitoring stack](../../../observability-and-platform-extras/skills/prometheus-and-grafana-monitoring-stack/SKILL.md) — underlying PromQL, recording rules, and Alertmanager routing mechanics used to implement the burn-rate alerts above.
- [environment-promotion-strategy](../../../devops/skills/environment-promotion-strategy/SKILL.md) — how to wire the error-budget freeze into an actual pipeline gate rather than a policy nobody enforces.
