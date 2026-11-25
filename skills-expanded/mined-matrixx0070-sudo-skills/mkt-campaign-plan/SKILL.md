---
name: mkt-campaign-plan
version: 1.0.0
description: Produce an execution-ready marketing campaign brief covering objective, audience, positioning, channels, calendar, and success metrics.
author: matrixx0070
tags: [marketing, campaign, strategy, planning, brief, gtm]
capabilities: []
---

## When to use

Use this when you are launching a product, promotion, event, or awareness push and need one coherent brief that stakeholders can execute against — not scattered ideas in a thread.

**Not for:** a single asset (use mkt-draft-content), a month of routine posting (use mkt-content-calendar), or reporting on a campaign that already ran (use mkt-performance-report).

## Method

1. Clarify the goal. Fix the primary business objective (awareness, leads, revenue, retention) and one measurable target. Decision point: if no target is given, propose a default and label it an assumption.
2. Define the audience. Segment the market, write a primary and secondary persona (pains, triggers, objections), and state the core insight the campaign exploits.
3. Set positioning. Craft the single big idea, the value proposition, and the primary message with 2-3 proof points.
4. Select channels. Map each channel to a funnel stage (awareness/consideration/conversion) with rationale and a rough budget split. Decision point: drop any channel you cannot resource properly rather than spreading thin.
5. Build the calendar. Sequence phases (tease, launch, sustain, close) with dates, owners, and per-channel deliverables.
6. Define measurement. Set KPIs per objective plus leading and lagging indicators and a review cadence.
7. Flag risks and dependencies (assets, approvals, budget, timing).

## Example

Objective: 500 trial signups in 6 weeks for a new analytics tool. Insight: mid-market ops leads distrust "AI magic" and want proof. Big idea: "See the math." Channels: LinkedIn thought leadership (awareness, 40%), retargeting ads (consideration, 30%), founder-led webinar + email (conversion, 30%). Phases: tease (wk1), launch webinar (wk2), sustain (wk3-5), close offer (wk6). KPI: signups; leading indicator: webinar registrations.

## Pitfalls

- Vague objectives ("more awareness") with no number to judge success against.
- Listing every channel instead of the few you can execute well.
- Positioning that describes the product's features rather than the customer's changed state.
- A calendar with no owners, so nothing actually ships.

## Output format

```
Campaign: <name> — <one-line pitch>
Objective + target metric: <...>
Audience & personas: <primary / secondary>
Positioning: <big idea, value prop, key message + proof>

Channel plan:
| Channel | Funnel stage | Goal | Budget % | KPI |

Timeline:
| Phase | Dates | Deliverables | Owner |

Success metrics & review cadence: <...>
Risks & dependencies: <...>
```
