---
name: okr-planning
description: OKR planning and review — objectives vs key results vs initiatives, outcome not output, writing measurable KRs with baseline and target, why 3-5 key results maximum, leading vs lagging indicators, cascading vs aligning OKRs across teams, quarterly cycle, scoring and grading, mid-quarter check-in, committed vs aspirational OKRs, KR ownership, and anti-patterns like vanity metrics, task lists disguised as KRs, and sandbagging.
---

# OKR Planning (objectives, key results, and the review cycle)

## Three distinct objects — most bad OKRs confuse two of them

```
Objective  = qualitative, directional, memorable. Where are we trying to get to?
Key Result = measurable evidence the objective happened. metric: baseline → target
Initiative = the work you will do to move a KR. A project. Never a KR.
```

Test every line: if it can be marked "done", it is an initiative; if it can only be measured, it may be
a KR. "Ship the referral programme" is an initiative; "referral-sourced signups from 4% → 12% of new
signups" is the KR it serves. Objectives without KRs are slogans; KRs with no initiative are wishes.

## Outcome, not output

A KR should describe a change outside your team — user behaviour, revenue, quality, retention, cost —
not the volume of work the team emitted. Ten shipped features are output; the retention or conversion
change they cause is the outcome. Output KRs are attractive because they are controllable, which is why
they never falsify the strategy: you can hit all of them and learn nothing.

## Writing a measurable KR

Each KR needs the metric, its exact definition and data source, a baseline measured *before* the
quarter, a target, and one named owner. Missing baselines are the most common defect — without one,
nobody can say at review whether the target was ambitious, trivial or already met. Prefer metrics
already in a trusted dashboard; a KR whose measurement must first be built will not be measured, and
rates beat raw counts, which drift with volume.

Keep to roughly 3–5 KRs per objective and few objectives per team; the limit is the point, because OKRs
are a prioritisation instrument and a list of twelve is a list of none. Routine matters — uptime,
support SLA, compliance — are health metrics you watch, not OKRs you push.

Lagging indicators (revenue, retention, NPS) confirm the result but move too late to steer inside a
quarter. Leading indicators (activation rate, time-to-first-value, pipeline created) move early and are
actionable but are only proxies — a proxy optimised in isolation is how a team hits its leading KR while
the lagging one worsens. Pair them: one lagging KR to prove the objective, one leading KR actionable
next week, and the causal assumption between them written down so the review can test it.

## Cascading vs aligning

Mechanical cascading — each manager copying their boss's KR one level down — duplicates work and strips
teams of the judgement that makes OKRs useful. Align instead: teams draft their own OKRs, each linked
explicitly to the company objective it serves, with cross-team dependencies declared as commitments
owned on both sides. An unowned dependency is the standard cause of a KR missed for outside reasons.

## Committed vs aspirational, scoring, and the review rhythm

Declare the type up front. **Committed** means the team is expected to deliver in full, and a miss is a
serious signal demanding explanation and replanning. **Aspirational** (stretch) targets sit beyond the
known plan, so partial attainment is expected — grading them like committed work is what teaches teams
to sandbag. Never mix grading standards in one review, and never quietly convert a stretch target into
a promise made outside the team.

- **Weekly check-in**: value vs target, confidence, what changed, what is blocked — the metric, not a
  status parade. **Mid-quarter**: reforecast, kill initiatives not moving their KR, and if the world
  changed, change the OKR explicitly and record why instead of pretending.
- **End of quarter**: score each KR on a normalised scale (commonly 0–1.0 by linear attainment from
  baseline to target), then discuss; the score starts the conversation, it is not the verdict. Record
  what was learned about the causal assumption. Keep scores out of individual compensation — pay-linked
  OKRs produce conservative targets and creative measurement.

## Anti-patterns

- **Task lists disguised as KRs** — "launch X, hire Y, migrate Z": roadmap items in costume.
- **Vanity metrics** — cumulative totals that only rise (signups to date, page views, followers), so
  they cannot fail and therefore cannot inform a decision.
- **Sandbagging** — targets set below the existing trend, hit at 100%, teaching nobody anything.
- **No baseline**, so the result is unfalsifiable; **unowned KRs**, owned by "the team" and therefore
  by nobody; **too many**, so nothing is deprioritised; **set and forget**, written in week one and
  reopened in week thirteen; **undefined metric**, where "active users" means three things; **gaming**,
  where the KR moves and the outcome does not — guard that with a paired counter-metric.

## Reviewer checklist

- [ ] Objectives qualitative and directional, with no metric smuggled into the objective line
- [ ] Every KR an outcome with metric, definition, data source, baseline, target, single owner
- [ ] Baselines measured before the quarter started; 3–5 KRs per objective
- [ ] Routine health metrics (uptime, SLA, compliance) kept out of the OKR set
- [ ] Leading and lagging KRs both present, causal assumption written down
- [ ] Initiatives listed separately, each mapped to the KR it should move
- [ ] Each OKR labelled committed or aspirational and graded on its own standard
- [ ] Alignment to a company objective stated, cross-team dependencies owned on both sides, and
      check-in cadence plus mid-quarter reforecast scheduled
- [ ] No vanity metrics, task-list KRs or unowned KRs; counter-metrics named where gameable

## Provenance

Standard OKR practice as commonly taught (objective/KR/initiative separation, outcome orientation,
leading-lagging pairing, align-not-cascade, committed vs aspirational grading, quarterly cycle with
mid-cycle reforecast). The KR count range and the 0–1.0 scoring convention are **derived, unverified**
conventions, not empirical findings; replace any numeric threshold with the project's own measured
values before treating it as a target. No study, vendor benchmark or statistic is cited.
