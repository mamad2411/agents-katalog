---
name: operational-excellence-layers
description: Audit and improve a team's or business's operations with the 5 Layers of Operational Excellence, built inside-out - Standardization, then Automation, then Measurement, then Continuous Improvement, then Innovation. Each layer has concrete practices (6–12 per ring), a maturity score and a rule that you do not build an outer layer on a weak inner one. Use when the user asks for an operations audit, wants to know why automation or dashboards are not paying off, is setting up SOPs/processes for a team or practice, or asks "where do we start improving operations". Pairs with `sop`, `process-to-teammate-system`, `workflow-optimizer`, `kpi-dashboard-framework`.
---

# 5 Layers of Operational Excellence

Source: uploaded infographic "5 Layers of Operational Excellence" by Eric
Partaker, drawn as concentric rings with "Start Here" pointing at the centre.
**[Certain]** the layers and practices are transcribed from the image; the
scoring model and sequencing rule are added here.

## The principle
Start at the centre. Automating a process that is not standardised
automates the chaos. Measuring a process that is not automated measures
noise. Most failed "digital transformation" projects skipped a ring.

## The five rings (inside → out)

| Ring | Layer | Practices (from the source) |
|---|---|---|
| 1 | **Standardization** | Write clear processes · Create checklists · Define roles · Document best practices · Train consistently · Build repeatable systems |
| 2 | **Automation** | Use smart tools · Connect your tools · Minimize manual errors · Automate recurring tasks · Set up triggers & workflows · Eliminate manual steps |
| 3 | **Measurement** | Define key metrics · Track performance · Set up dashboards · Tie metrics to decisions · Share results with your team · Compare results to goals |
| 4 | **Continuous improvement** | Gather feedback · Spot bottlenecks · Run regular reviews · Align team on fixes · Run retrospectives · Improve weekly · Document key learnings · Adjust systems · Repeat what works |
| 5 | **Innovation** | Host idea sessions · Encourage bold thinking · Prioritize high-impact tests · Run quick experiments · Run small pilots · Involve your customers · Learn from failures · Protect time to explore · Track ideas in motion · Recognize & reward progress · Share what you learn · Scale what works |

## Maturity scoring (per practice)

| Score | Meaning |
|---|---|
| 0 | Not done |
| 1 | Done ad hoc, depends on one person |
| 2 | Done, documented, not consistent |
| 3 | Done consistently, owned, reviewed |

Layer score = average of its practices (0–3). **Gating rule:** a layer
counts as "in place" only at ≥ 2.0, and you do not invest in ring N+1
while ring N is below 2.0. The priority is always the innermost ring
under 2.0.

## Audit procedure
1. Pick one process (not the whole company): e.g. "new client onboarding", "monthly reporting", "surgical-kit ordering".
2. Score all practices for rings 1–3 from evidence (a document, a tool, a dashboard); "we sort of do it" = 1.
3. Find the innermost ring under 2.0. That is the only ring you work on this month.
4. Produce three actions for that ring, each with an owner, a date and the evidence that will prove it is done.
5. Re-score in 30 days. Rings 4–5 are only scored once rings 1–3 are ≥ 2.0.

## Output format
```
Process: [name]
Ring scores: Standardization x.x | Automation x.x | Measurement x.x | CI x.x | Innovation x.x
Innermost gap: [ring] — because [lowest-scoring practices with evidence]
Actions (30 days):
1. [action] — owner — date — evidence of done
2. ...
3. ...
Do NOT start yet: [outer-ring ideas parked, and why]
```

## Honest limits
- The graphic presents the rings as universal. Small teams (1–5 people) can run rings 1 and 3 together; a checklist plus one metric beats a separate automation project.
- "Innovation" as a separate ring can become an excuse to postpone it forever. Keep 5–10 % of time for it even while inner rings are being fixed, but do not scale an experiment until rings 1–3 are in place for that process.

Run with `/opex-audit [process]`.
