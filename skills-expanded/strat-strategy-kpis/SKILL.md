---
name: strat-strategy-kpis
description: Defines the KPIs for a strategy as one block per bet and strategic action, each with the goal, the signal and the metric (event, filter, window), leading and lagging indicators, a baseline with its source, a target left for the owner, a guardrail, and the review date with the threshold that would make the owner change course. Use for "run strat-strategy-kpis", "KPIs for our strategy", "how will we know the strategy is working", "leading and lagging indicators", "set a guardrail metric", "what would make us change course", "measures for each bet", "strategy scorecard", part of the Claude Guide for Product Strategy Pack by 90n.
---

# Strategy KPIs

## When To Use
Six months in, nobody can say whether the strategy is working, so direction shifts with whichever result was loudest last week. Use it when the bets and actions are written and before the first results arrive. It answers: where do we read each bet, what moves first, what must not get worse, and what reading on which date would make the owner change course?

## When Not To Use
If you need the one number for the whole product, run North Star Metric; a KPI here may point at one of its inputs and never redefines it. If the bet itself and its kill line are not written, run Strategic Bets first. For one quarter's targets, run Quarterly OKRs: these KPIs last the life of the bet.

## Inputs
- The bets and strategic actions, each with its owner by role
- The events you collect today and where they live, or a read-only analytics connector
- Any current values you trust, with their period and query
If you have none of this, I start from the list of bets, leave every baseline as "none yet" and mark the output as a first draft. The analytics connector is used read only, and the sheet works the same in a plain chat.

## Approach
Two public methods are combined. The goals, signals, metrics process (Rodden, Hutchinson and Fu, Google, CHI 2010: https://research.google/pubs/measuring-the-user-experience-on-a-large-scale-user-centered-metrics-for-web-applications/) sets the order: the goal, then the signal that shows it, then the metric. Signposts of change, a technique named in the US Government's Tradecraft Primer (2009: https://www.cia.gov/resources/csi/static/Tradecraft-Primer-apr09.pdf), adds the readings agreed in advance that tell you the plan is no longer holding. The judgment: start from the bet, not from the dashboard you already have. The failure it prevents: a metric chosen after the results came in, so the strategy is declared a success on the one chart that went up.

## Workflow
1. Ask at most three questions: which bets and actions this sheet covers, which data you can read today, and who owns each bet (by role) and sets its targets.
2. Open one block per bet and per strategic action. Inside a block the order is fixed: the goal in customer words, then the signal (what customers do when the goal is met), then the metric.
3. Define each metric by event, filter and window, the unit (accounts or users) and the owning team. "Engagement" alone is not a metric. Mark each indicator leading (moves within weeks) or lagging (confirms over quarters), and say which leading one is meant to predict which lagging one.
4. Record the baseline with its source, date range and query, read through the analytics connector or an export. Where an event is not collected, write "none yet" and the tracking change needed. Merge segments below the minimum size you set.
5. Leave the target for the owner; Claude never proposes one. Add one guardrail per metric: the number that must not get worse while the target moves.
6. Set the signposts: the review date and the threshold, written by the owner in advance, that would make the owner change course. A threshold nobody would act on is not a signpost.
7. Lock the sheet with a date. Anything added after results arrive goes to "found later", never into the claim that a bet is working.

## Output Format
```markdown
# Strategy KPI Sheet
Strategy: [name] | Covers: [bets and actions] | Locked on: [date, before results arrive]
## Bet or action: [name] | Owner: [role]
Goal: [in customer words] | Signal: [what customers do when the goal is met] | Points at north star input: [input name, or none]
| Type | Metric (event, filter, window) | Unit | Owning team | Baseline (source, date range, query) | Target | Guardrail |
|---|---|---|---|---|---|---|
| Leading | [definition] | [accounts or users] | [team] | [value with source, or "none yet"] | [set by the owner] | [metric and limit, set by the owner] |
| Lagging | [definition] | [accounts or users] | [team] | [value with source, or "none yet"] | [set by the owner] | [metric and limit, set by the owner] |
## Signposts
| Bet or action | Review date | Threshold that would make the owner change course | Set by (role), on (date) |
|---|---|---|---|
| [name] | [date] | [metric and reading, set by the owner] | [role, date] |
## Tracking gaps
- [Event not collected] | [tracking change needed] | [owning team] | [needed by date]
## Found later
- [Measure added after results arrived, with the date; not part of the success claim]
## Decision
[Owner of each bet, by role] sets the targets, guardrail limits and change-course thresholds by [date, before results arrive], and reads the sheet on [review date].
```

## Done When
- Every bet and strategic action has a block, and every metric traces back to a goal and a signal, in that order
- Every baseline has a source, date range and query, or reads "none yet" with the tracking change
- Every metric has an owning team and a guardrail
- Every bet has a review date and a change-course threshold set by its owner, and the sheet carries a lock date

## Quality Bar
- A metric names event, filter and window; a label from a dashboard is not a definition.
- Two indicators that would change a decision beat six filled in for completeness; an untested link between a leading and a lagging one is marked as an assumption.
- Team-level ownership and aggregate data only; no individual targets, no per-user tracking, small segments merged below the minimum you set.
- No invented baselines or targets; the owner sets targets and the change-course threshold before results arrive.

## Next
Run strat-impact-map (Impact Map) to tie each roadmap item to the behaviour change these measures read.

## About the makers

This pack is made by 90n ([90n.ai](https://90n.ai)): AI-native ways of working and tools for Product, Marketing and HR teams, built by ex-McKinsey founders. We map where time and money leak, redesign the work around AI and stay until your people run it themselves, and we run our own company on Claude. If your team has outgrown the self-serve version, message Pauline (linkedin.com/in/paulinebertry).
