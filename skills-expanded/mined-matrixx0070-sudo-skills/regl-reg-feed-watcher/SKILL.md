---
name: regl-reg-feed-watcher
version: 1.0.0
description: Stand up a monitored watchlist of regulatory feeds so new rules, notices, and guidance surface the day they publish instead of weeks later.
author: matrixx0070
tags: [regulatory, legal, monitoring, rulemaking, feeds, compliance]
capabilities: []
---

## When to use

Use this when a matter, product, or business line is exposed to one or more regulators and you need to know the moment they act. Reach for it to build the initial watchlist, to add a newly relevant agency, or to audit whether an existing feed is still catching everything.

**Not for:** reading a single already-known rule (use regl-policy-diff), managing a comment deadline you already have (use regl-comments), or producing the weekly rollup (use regl-gaps digest). If a hit turns out to demand a legal position, escalate to an attorney rather than interpreting it yourself.

## Method

1. Map exposure first: list the agencies, dockets, and statutory topics that actually touch the business. A feed you cannot tie to a real exposure is noise.
2. For each source, record the canonical publication channel — Federal Register / official gazette page, agency rulemaking docket, guidance library, or press/enforcement page. Prefer the primary official source over aggregators.
3. Classify each expected item by lifecycle stage so triage is fast: advance notice (ANPRM), proposed rule (NPRM), final rule, guidance, or enforcement action.
4. Set a check cadence proportional to risk — daily for active dockets, weekly for dormant ones.
5. **Decision point:** on each hit, capture docket ID, stage, publication date, and any comment-close date, then route it — diff-worthy to regl-policy-diff, deadline-bearing to regl-comments.
6. Deduplicate: the same rule appears in multiple channels. Key on docket/RIN, not headline.

## Example

> Exposure: consumer-lending product, US. Watchlist: CFPB rulemaking docket, FTC rules page, state AG consumer pages. Cadence: CFPB daily, others weekly. Hit on 2026-06-30: NPRM, RIN 3170-AB00, comment closes 2026-08-29. Routed to regl-comments (deadline) and regl-policy-diff (impact).

## Pitfalls

- Watching aggregators only — they lag and drop items; anchor on the official docket.
- No exposure link, so the list bloats and real hits drown.
- Keying on titles, not docket/RIN, so re-publications look like new rules.
- Treating a hit as a legal conclusion instead of routing it for analysis.

## Output format

```
WATCHLIST — <matter/business line>
Source | Agency | Channel (official URL) | Stage watched | Cadence
---
NEW HIT: <docket/RIN> | Stage: <ANPRM|NPRM|Final|Guidance|Enforcement>
Published: <date> | Comment closes: <date or n/a>
Routed to: <regl-comments | regl-policy-diff> | Attorney review: <yes/no>
```

## Reference

**Rulemaking lifecycle:** ANPRM (optional early signal) → NPRM (proposed rule + comment period opens) → public comments → final rule (with response to comments) → effective date, sometimes phased. Guidance and enforcement actions sit outside notice-and-comment but still shift obligations.

**Comment-period mechanics:** comment windows are typically 30–60 days from Federal Register publication, occasionally extended; the docket ID/RIN is the stable key across channels.

**Policy-diff method:** every hit is a candidate delta against current policy — capture stage and dates now so downstream diffing has clean inputs. Attorney-escalation gate: any hit that implies a new legal obligation or litigation risk goes to counsel before the business relies on it.
