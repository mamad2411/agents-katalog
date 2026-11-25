---
name: strat-needs-based-segments
description: Draws Needs-Based Segments as job statements with circumstance and trigger, the current alternative, a size signal from aggregate data, an underserved check and the choice of which segment the strategy serves first and which it does not. Use for "run strat-needs-based-segments", "needs-based segmentation", "segment customers by needs", "jobs to be done segments", "which segment do we serve first", "which segment is underserved", "our users means four groups", "who is the strategy for", part of the Claude Guide for Product Strategy Pack by 90n.
---

# Needs-Based Segmentation

## When To Use
"Our users" means four groups and the strategy tries to serve all of them, so it serves none of them well. Use this when the strategy has to name its customer, to answer: which jobs are customers trying to get done, in which circumstances, where does today's alternative fail them, and which group comes first?

## When Not To Use
With no customer conversations at all, every segment here is a guess with a name: hold the interviews first, or accept a draft marked hypothesis. To work inside one chosen segment and one outcome, run Opportunity Solution Tree; to turn a segment into a market range, run Market Sizing (TAM, SAM, SOM). Never use this for personas of individuals or lists of named customers.

## Inputs
- Interview notes or themes, with codes instead of names
- Aggregate data: account counts by plan, usage bands, as an export or through an analytics connector kept read only
- What customers use today instead of the product, if known
If you have none of this, I start from your own description of the groups and mark every segment "hypothesis", as a first draft.

## Approach
Jobs to be done as set out by Clayton Christensen, Taddy Hall, Karen Dillon and David Duncan (Harvard Business Review, 2016, hbr.org/2016/09/know-your-customers-jobs-to-be-done): customers hire a product to make progress in a circumstance, and the circumstance explains the choice better than their attributes. So segments are drawn around jobs, and plan or role is only a proxy. It works in any chat. The failure it prevents: the "segment" that is a label on a plan tier, which tells the strategy nothing about what to do for it.

## Workflow
1. Ask up to three questions: which product or market the strategy covers, what evidence exists (interviews, feedback, aggregates), and the minimum group size below which segments merge (you set it).
2. Write each candidate job as verb + object + context, with no product in it. Test it: would the job still exist if the product vanished? "And" in a statement usually means two jobs, so split it.
3. Add the circumstance and the trigger (when it happens, what just happened), then the current alternative, including a spreadsheet, a colleague or doing nothing.
4. Size signal from aggregate data only: a count or band with its source and date, or "no data". Never a list of who.
5. Underserved check: the job is frequent and the alternative is poor. Mark each segment underserved, served or overserved, with the evidence. Overserved is a finding too: it is where the product does more than the job asks.
6. Mark each segment "evidenced" (interview themes behind it) or "hypothesis", and merge any group below your minimum.
7. Close on the choice: propose which segment the strategy serves first and which it does not serve, with what each excluded segment loses. The owner chooses.

## Output Format
```markdown
# Needs-Based Segments
Scope: [product or market] | Evidence: [interview set, date; data source, date] | Group minimum: [n, set by the user]
## Segments
| Segment | Job statement | Circumstance and trigger | Current alternative | Size signal (source, date) | Status |
|---|---|---|---|---|---|
| [short name] | [verb + object + context] | [when, what just happened] | [incl. doing nothing] | [count or band, or "no data"] | [evidenced / hypothesis] |
## Underserved check
| Segment | How often the job occurs (source) | Where the alternative breaks | Verdict |
|---|---|---|---|
| [segment] | [frequency] | [gap, with interview codes] | [underserved / served / overserved] |
## Served first, and not served
| Segment | Proposal | Reason | What this segment loses |
|---|---|---|---|
| [segment] | [serve first / later / not served] | [evidence] | [consequence] |
## Decision
The [product leader] chooses by [date] which segment the strategy serves first and confirms the segments it does not serve.
```

## Done When
- No job statement names a product or a feature
- Every segment has a circumstance, an alternative and a sourced size signal or "no data"
- Every segment is marked evidenced or hypothesis
- Groups below the minimum are merged
- One segment is proposed as first and at least one as not served

## Quality Bar
- Segments describe jobs and circumstances, never people; no personas of individuals, no lists of named customers.
- Aggregates only; counts below the minimum are merged, not shown. A size signal is a sourced count, not a market size.
- A choice of first segment with no "not served" line is not a choice.
- Segments without interview evidence are marked hypothesis; a named person chooses which segment is served first.

## Next
Run strat-opportunity-solution-tree (Opportunity Solution Tree) to map what the chosen segment told you under one outcome.

## About the makers

This pack is made by 90n ([90n.ai](https://90n.ai)): AI-native ways of working and tools for Product, Marketing and HR teams, built by ex-McKinsey founders. We map where time and money leak, redesign the work around AI and stay until your people run it themselves, and we run our own company on Claude. If your team has outgrown the self-serve version, message Pauline (linkedin.com/in/paulinebertry).
