---
name: customer-support-ops
description: Customer support and service operations — ticket triage and prioritization, SLA design and response/resolution targets, CSAT, NPS (net promoter score) survey programs, CES measurement, knowledge base and macro design, escalation paths, support staffing and volume forecasting, QA scorecards for agents, deflection and self-service, churn-risk signals from support contacts. Use for designing or improving a customer support/service workflow.
---

# Customer Support Operations (triage, SLAs, quality, staffing, deflection)

## Triage: severity × impact, decided by rule not by mood

Every inbound ticket gets a priority from a written matrix — severity (broken for the customer?) ×
impact (how many customers / how much revenue?) — plus routing to the queue that can actually
resolve it. Triage done by whoever reads it first, on vibes, means priority tracks how angry the
customer sounded.

```
P1  service down / data loss / security — page someone, all-hands until mitigated
P2  core function broken, no workaround — same-business-day engagement
P3  degraded or has a workaround — normal queue
P4  question / feature request — normal queue, feeds the KB and product backlog
```

Escalation paths are named in advance: which tier owns what, what evidence must accompany a hand-off
(repro steps, account, logs), and who is paged for P1. An escalation that restarts diagnosis from
zero doubles resolution time.

## SLA design and the metrics that matter

```
first response time (FRT)  = ticket created → first human (not auto-ack) response
resolution time            = created → resolved, clock paused while pending-customer (say so)
SLA attainment             = tickets meeting target / tickets in period — per priority tier
first contact resolution   = resolved with no reopen and no additional agent contact / resolved
reopen rate                = reopened within N days / resolved  (the lie detector for "resolved")
backlog age                = distribution of open ticket ages, not just the count
```

Set targets per priority, from measured capability plus headroom — an SLA copied from a competitor's
marketing page is a promise chosen at random. Report percentiles (e.g. 90th) rather than averages:
an average FRT of 2h coexists comfortably with a tail of customers waiting three days.

## Quality: CSAT, CES, NPS — and QA scorecards

- **CSAT** (post-resolution, per ticket) measures the interaction. Report response rate alongside —
  20% response CSAT is a self-selected sample. **CES** (effort) predicts loyalty better for support
  interactions. **NPS** measures relationship, moves slowly, and is mostly not a support metric;
  don't hold agents to it.
- QA scorecard: sample tickets per agent per week, scored against written criteria (accuracy,
  completeness, tone, process adherence) with calibration sessions so two reviewers give the same
  ticket the same score. Uncalibrated QA is a popularity contest.
- Never target reopen-able metrics in isolation: pushing FRT alone produces fast useless replies;
  pushing handle time produces premature "resolved". Pair every speed metric with FCR/reopen and
  CSAT.

## Staffing and volume forecasting

```
forecast volume  = base (trailing weeks, same weekday/hour pattern) × seasonality
                   × known drivers (releases, campaigns, billing cycles)
agents needed    ≈ (volume × avg handle time) / (scheduled hours × occupancy)
                   — target occupancy ~75–85%; planned at 100% the queue explodes
                   the first bad Tuesday
```

Concurrency (chat) and shrinkage (meetings, training, breaks, absence — commonly 25–35% of paid
time) must be explicit inputs. Forecast at the interval level for scheduling, weekly for hiring.

## Deflection, knowledge base, churn signals

- KB articles are written from real ticket clusters — top drivers first — and each article's
  effectiveness is measured (views → tickets still filed on that topic). Deflection is only real if
  ticket volume for that driver drops; a well-read article with flat volume is decoration.
- Macros/templates for the top intents, but every macro leaves room for one sentence specific to the
  customer; a detected paste-job costs more goodwill than slow typing.
- Contact-driver taxonomy: tag every ticket with *why* the customer contacted. This is the highest
  value dataset support produces — it feeds product fixes, KB priorities, and staffing. Untagged
  tickets are burned information.
- Churn-risk signals worth piping to account owners: repeat contacts on the same issue, P1/P2 in the
  first 30 days, negative CSAT from a high-value account, "how do I export my data" questions.

## Failure modes

- SLA met on 95% of tickets while the 5% breach set contains every enterprise account (attainment
  unweighted by value).
- Resolved-on-first-touch pushed so hard agents resolve tickets the customer considers open; reopens
  and channel-switching hide the miss.
- Backlog "managed" by mass-closing stale tickets before the quarterly review.
- Agents graded on CSAT they can game (asking only happy customers to rate) or that punishes them
  for the product's faults.
- Deflection claimed from KB pageviews while contact volume per active customer is flat.

## Reviewer checklist

- [ ] Written triage matrix; priority assigned by rule, escalation paths named with hand-off evidence
- [ ] SLA targets per priority, from measured capability; attainment reported as percentiles
- [ ] Speed metrics paired with FCR/reopen and CSAT; no metric targeted alone
- [ ] CSAT reported with response rate; QA scores calibrated across reviewers
- [ ] Staffing model shows volume forecast, AHT, occupancy, and shrinkage assumptions explicitly
- [ ] Every ticket tagged with a contact driver; top drivers feed KB and product backlog
- [ ] Deflection claims backed by falling ticket volume on the driver, not article views

## Provenance

Standard support-operations practice (severity matrices, SLA/FCR/reopen definitions, Erlang-style
staffing inputs, contact-driver analysis). Numeric figures — occupancy 75–85%, shrinkage 25–35% —
are **derived, unverified** industry rules of thumb; replace with the team's own measured handle
times and shrinkage before publishing a staffing plan.
