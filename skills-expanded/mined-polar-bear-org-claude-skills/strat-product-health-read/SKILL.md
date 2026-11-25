---
name: strat-product-health-read
description: Builds a Product Health Read before a strategy cycle, with four lenses (usage, quality, revenue signals, feedback), a source, date range and query on every line, the change since last period with tracking changes flagged, and the list of what the data cannot tell. Use for "run strat-product-health-read", "health read of the product", "what is true about the product today", "check the numbers before planning", "is last quarter's deck still right", "what changed since last period", "what can the data not tell us", part of the Claude Guide for Product Strategy Pack by 90n.
---

# Product Health Read

## When To Use
Planning starts from last quarter's deck and nobody has checked what is true today. The strategic question is agreed, and the room is about to argue from figures that are three months old. This skill answers: what is the product's real state now, with a source for each line, and what can we not tell?

## When Not To Use
This skill reads today's state; it sets no target and picks nothing. If you need measures and change-course thresholds for the bets, run Strategy KPIs. If you need the one number the product is steered by, run North Star Metric. For a single metric question, a direct query in your analytics tool is faster.

## Inputs
- The Strategic Question Frame, or the goal the product is meant to serve this period.
- Read-only connectors to analytics, tickets and support (for example Amplitude, Linear or Intercom), or an export from each with its date range.
- Your metric definitions, the last deck or review, and any tracking change, launch or incident you already know about.
If you have none of this, I start from the last deck you can paste, list what to pull, and mark the output as a first draft.

## Approach
The read follows HEART and the goals, signals, metrics process (Rodden, Hutchinson and Fu, Google, CHI 2010: https://research.google/pubs/measuring-the-user-experience-on-a-large-scale-user-centered-metrics-for-web-applications/). Goals come first, so the read is not whatever the dashboard happens to show, and HEART serves as lenses, not a scorecard. Claude reads the connected tools and changes nothing in them; with pasted exports it works the same in a plain chat. The failure it prevents: a strategy built on a retention drop that was really an event definition changed mid-period.

## Workflow
1. Ask at most three questions: which goal should the read serve, which tools or exports can I read, and what period counts as "now" and as "last period"? Also take the minimum group size below which you want groups merged.
2. Write the goal beside each signal before any number goes in. A signal with no goal behind it is left out, however good it looks.
3. Read four lenses. Usage: adoption, engagement, retention. Quality: bugs, incidents, task success. Revenue signals: only what you can share. Feedback: themes and volume. Aggregates only.
4. Put the source, the date range and the query or filter on every line. A number with no source is dropped, not rounded into a sentence.
5. Show the change since last period as direction and size. Where a definition, an event or the tracking setup changed, say so beside the number, because that comparison may not hold.
6. Write the unknown list: what the data cannot tell and what would answer it (a query, a customer call, a role to ask). It is never empty; an empty list means I stopped looking.
7. Write the headline last and put it first: three things that are true, and one that differs from the last deck.

## Output Format
```markdown
# Product Health Read
**Headline:** [three true things] | [one thing that differs from the last deck]
Period: [dates] | Compared with: [dates] | Goal read: [goal]
## Four lenses
| Lens | Goal it reads | Signal | Value now | Change since last period | Source, date range, query |
|---|---|---|---|---|---|
| Usage | [goal] | [signal] | [value] | [direction and size] | [tool, dates, filter] |
| Quality | [goal] | [signal] | [value] | [direction and size] | [tool, dates, filter] |
| Revenue signals | [goal] | [signal] | [value or "not shared"] | [direction] | [source, dates] |
| Feedback | [goal] | [theme] | [volume] | [direction] | [tool, dates, tag] |
## Definition and tracking changes
- [metric]: [what changed, when] | [comparable with last period / not comparable]
## What the data cannot tell
| Gap | Why | What would answer it |
|---|---|---|
| [what we cannot tell] | [missing data or access] | [query, customer call, role to ask] |
## Decision
[Product lead role] confirms which gaps to close before the strategy work goes on, and which figures replace the last deck's, by [date].
```

## Done When
- Every number carries a source, a date range and a query or filter.
- Each lens has at least one signal, or says why it has none.
- Every tracking or definition change sits beside the number it affects.
- The list of what the data cannot tell is not empty, and each gap names what would answer it.

## Quality Bar
- Goals before metrics: no signal appears without the goal it reads.
- Aggregates only. No per-user or per-employee line, and groups below the minimum size you set are merged.
- Revenue signals are yours to share or withhold; "not shared" is a valid cell. The read proposes no target, no cause and no fix.
- Every number has a source, a date range and a query; unknowns stay unknown, and the product lead decides what the read means.

## Next
Run strat-issue-tree (Issue Tree) to split the strategic question into parts the read can help answer.

## About the makers

This pack is made by 90n ([90n.ai](https://90n.ai)): AI-native ways of working and tools for Product, Marketing and HR teams, built by ex-McKinsey founders. We map where time and money leak, redesign the work around AI and stay until your people run it themselves, and we run our own company on Claude. If your team has outgrown the self-serve version, message Pauline (linkedin.com/in/paulinebertry).
