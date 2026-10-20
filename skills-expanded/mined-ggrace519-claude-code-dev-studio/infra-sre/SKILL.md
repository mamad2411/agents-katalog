---
name: infra-sre
description: SRE specialist. Owns SLOs, error budgets, incident response, postmortems, on-call rotation, and reliability engineering practice. Auto-invoked when setting up SLOs, responding to incidents, or improving reliability.
---

# SRE

Reliability is a feature with a budget. SLOs give you a number to reason about,
blameless postmortems keep you learning, and alert fatigue kills both.

## When to reach for this

- Defining SLIs/SLOs and error budgets for a service, or revising fictional ones
- Replacing threshold alerts with burn-rate alerting
- Setting up incident command, on-call rotation, or the postmortem process
- Planning game days, chaos experiments, or capacity drills

## Principles

1. **Measure what users feel.** SLIs are request success rate and latency at
   the edge the user touches — not CPU, not pod restarts. Express latency as
   "% of requests faster than X ms" so it composes into the same budget math.
2. **Pick targets you can defend, then do the math.** 99.9% over 30 days is
   43.2 minutes of full-outage budget; 99.99% is 4.3 minutes — less than one
   human-paged response. Every extra nine roughly 10×es the cost; default new
   services to 99.9% and earn stricter targets with evidence.
3. **Alert on burn rate, not raw thresholds.** Multi-window, multi-burn-rate:
   page at 14.4× over 1 h (2% of a 30-day budget gone in an hour), page at 6×
   over 6 h, ticket at 1× over 3 days. Each rule pairs a long window with a
   short one (1/12th) so alerts stop when the bleeding stops.
4. **The budget drives decisions.** Budget exhausted → reliability work
   pre-empts features until back in budget — agreed with product *before* the
   first breach, or the policy is theater. Budget to spare → ship faster, run
   chaos experiments.
5. **Blameless or useless.** Postmortems name contributing causes in the
   system, never people; people tell the truth only when it's safe. Every
   action item has an owner and a date, tracked to completion or explicitly
   rejected — an unowned action item is a wish.
6. **On-call must be sustainable.** Target < 2 pages per shift; every page is
   actionable and urgent or it gets demoted to a ticket. Rotation ≥ 4–6 people,
   handoff is written, and time-to-acknowledge is a watched metric.

## Burn-rate alert set (30-day window SLO)

| Severity | Burn rate | Long window | Short window | Budget consumed |
|---|---|---|---|---|
| Page | 14.4× | 1 h | 5 m | 2% in 1 h |
| Page | 6× | 6 h | 30 m | 5% in 6 h |
| Ticket | 1× | 3 d | 6 h | 10% in 3 d |

Fire only when **both** windows exceed the rate — the short window is the
"still happening" check that prevents stale pages.

A worked SLO/error-budget worksheet (SLI selection, budget math, alert rule
skeletons, budget policy template) is in
[`references/slo-worksheet.md`](references/slo-worksheet.md).

## Pitfalls

- SLOs copied from a blog instead of derived from user expectations and
  measured baseline — instantly either always-red or meaningless
- Availability measured at the load balancer while users fail at DNS/CDN — the
  SLI must cover the path users actually take
- Burn-rate alerts on a service with traffic too low for the math (a single
  failed request at 3 a.m. pages someone) — use longer windows or event-count
  guards
- Postmortems that end at "human error" — that's where the analysis starts,
  not stops
- Action items closed by writing them down; review the backlog of open
  postmortem items monthly or stop pretending to learn
- 100% as an implicit target because no one wrote down the SLO — then every
  blip is an argument

---
*Related: `infra-observability` (the signals SLIs are built from),
`infra-dr-backup` (RTO/RPO vs. SLO alignment), `infra-k8s` (rollout strategies
that protect the budget), `infra-finops` (cost of each extra nine) · domain
agent: `infra-architect` · output/ADR format: `playbook-conventions`*
