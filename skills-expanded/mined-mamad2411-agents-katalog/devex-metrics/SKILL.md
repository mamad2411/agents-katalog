---
name: devex-metrics
description: Define DORA + SPACE metrics for the team — what each measures, how to collect it, and the threshold that classifies elite/high/medium/low performance.
---

# devex-metrics

> Pin DORA (output) and SPACE (developer experience) metrics for a team. Output is a metric sheet with collection sources.

## When to use

- A platform team is starting to measure itself.
- An exec asks "how do we know we're improving DX?".
- A workflow needs a baseline before a platform investment.

## DORA — four output metrics

| Metric | Question | Source |
| ------ | -------- | ------ |
| Deployment Frequency | How often do we deploy to prod? | CI/CD logs, deployment system. |
| Lead Time for Changes | Time from commit → prod. | Git + deploy logs. |
| Change Failure Rate | % of deploys causing incident or rollback. | Incident tracker + deploy logs. |
| Mean Time to Restore | Time from incident open → resolved. | Incident tracker. |

Performance bands (Google DORA report; check the current year's report for latest cutoffs):

- **Elite**: multiple deploys per day; <1 day lead time; <5% CFR; <1 hour MTTR.
- **High**: weekly–monthly deploys; 1 day–1 week lead time; <10% CFR; <1 day MTTR.
- **Medium / Low**: longer than above.

## SPACE — developer experience

Five dimensions. Pick at most 2 metrics per dimension; otherwise the sheet becomes noise.

| Dimension | Example metric | Source |
| --------- | -------------- | ------ |
| Satisfaction | "Would you recommend our dev tools?" (NPS-style). | Survey, quarterly. |
| Performance | Code review depth & timeliness. | PR analytics. |
| Activity | PRs merged per week. | Git host. |
| Communication & Collaboration | Cross-team review participation. | Git host. |
| Efficiency & Flow | Time between "ready for review" and merge. | PR analytics. |

## Procedure

1. **Pick the team's North Star** from DORA. For most engineering orgs, Lead Time + Change Failure Rate is the right pair.
2. **Pick at most 2 SPACE metrics** to complement.
3. **Document collection** per metric: which system, how queried, what cadence.
4. **Set targets, not just observations.** "Lead time < 24h" beats "track lead time".

## Output

```text
DevEx metrics: <team>

DORA:
  - Lead Time for Changes        target: < 24h            source: GitHub + Deploy svc
  - Change Failure Rate          target: < 10%            source: PagerDuty + Deploy svc
  - Deployment Frequency         target: ≥ 1/day/service  source: Deploy svc
  - MTTR                          target: < 4h            source: PagerDuty

SPACE (lite):
  - Satisfaction (NPS)           target: ≥ +20            source: quarterly survey
  - Time to merge (P50)          target: < 4 working hrs  source: PR analytics

Review cadence: monthly platform-team retro. Move thresholds only with
incident or initiative evidence.
```

## Anti-patterns to avoid

- Tracking all five SPACE dimensions with 3 metrics each (information overload).
- DORA as a stack-ranking tool ("which team is elite?"). It's a self-improvement signal, not a comparison weapon.
- Setting "improve deploy frequency" as a goal without lead time + CFR; you can ship more by skipping review.
