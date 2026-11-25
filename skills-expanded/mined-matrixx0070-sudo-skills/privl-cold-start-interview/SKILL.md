---
name: privl-cold-start-interview
version: 1.0.0
description: Run a structured intake interview to build a first data-processing picture for an org with no privacy program — surface data flows, systems, vendors, and legal bases from zero.
author: matrixx0070
tags: [privacy, legal, intake, interview, data-mapping, ropa, discovery]
capabilities: []
---

## When to use

Use this when an organization has no existing privacy documentation and you must build the baseline from a blank page: no records of processing (RoPA), no data map, no vendor list. It is the discovery conversation that feeds every later artifact — RoPA, PIAs, DPAs, DSAR readiness.

**Not for:** organizations that already have a data map you can review (go straight to privl-reg-gap-analysis), assessing a single new use case (privl-use-case-triage), or answering a live request. If a RoPA exists, validate it rather than re-interview.

## Method

1. Frame the goal: you are mapping *what personal data exists, why, where, and who touches it* — not judging yet.
2. Walk the data lifecycle with the interviewee: collection points → purposes → storage systems → internal access → external sharing → retention → deletion.
3. For each flow capture: data categories, subject types (customers, employees, children), volume/scale, and any sensitive/special-category data.
4. Enumerate systems and vendors: SaaS tools, sub-processors, analytics, payment, cloud region(s). Ask "where does the data physically live?" for transfer exposure.
5. Probe legal footing per purpose: why are you allowed to do this? Note where no basis is articulated.
6. **Decision point:** flag every flow with no owner, no retention rule, or undocumented cross-border transfer as a gap for follow-up.
7. **Attorney-escalation gate:** if the interview surfaces active sensitive-data processing, children's data, or transfers with no mechanism, note it for counsel — do not opine on legality.

## Example

> **Org:** 30-person SaaS, no privacy docs.
> Interview surfaces: signup + support + a Facebook pixel (undisclosed), data in US + EU cloud, HR data in a third-tool, no retention policy anywhere.
> **Output:** 6 processing flows mapped, 4 vendors, 3 gaps (pixel undisclosed, no retention, EU→US transfer without SCCs). Routed transfer gap to counsel.

## Pitfalls

- Accepting "we don't collect much" — shadow collection (pixels, logs, backups) is universal.
- Interviewing only IT and missing HR/marketing data flows.
- Recording systems but not the *purpose* — purpose drives lawful basis.
- Letting the interview become a legal opinion; you are gathering facts.

## Output format

```
COLD-START MAP — <org> | date
Flow: <collection → purpose → system → sharing → retention>
  data: <categories> | subjects: <type> | scale: <n> | sensitive: <y/n>
Systems/vendors: <list + region>
Basis (stated): <per purpose or "none articulated">
Gaps: <no-owner | no-retention | transfer | undisclosed>
For counsel: <items>
```

## Reference

- **GDPR Art. 30** records of processing — the RoPA fields this interview populates.
- **GDPR Art. 6/9** lawful bases and special-category conditions to probe per purpose.
- **Chapter V** international transfers (SCCs/adequacy) — capture data location for later analysis.
- Escalate active sensitive/children's-data or unmechanized transfers to an attorney.
