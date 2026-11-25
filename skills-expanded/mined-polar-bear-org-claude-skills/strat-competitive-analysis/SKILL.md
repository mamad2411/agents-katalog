---
name: strat-competitive-analysis
description: Builds a Competitive Analysis with a landscape by the customer's job where every cell has a source and a read date, win and loss themes from buyer interviews kept apart from sales-reported reasons, where you differ and what not to copy. Use for "run strat-competitive-analysis", "competitive analysis", "competitor landscape", "the competitor has it", "win loss analysis", "why do we lose deals", "should we copy this feature", "what do buyers compare us with", part of the Claude Guide for Product Strategy Pack by 90n.
---

# Competitive Analysis

## When To Use
"The competitor has it" is setting the roadmap. A lost deal turns into a feature request with a date, and nobody has checked what buyers were really choosing between. Use this in a strategy cycle to answer three things: what do customers compare us with, why do we win and lose, and which gaps are worth closing at all?

## When Not To Use
With no public pages and no buyer conversations, this is guessing about rivals: talk to recent won and lost buyers first. To describe your own customers by what they need, run Needs-Based Segmentation; to count the space, run Market Sizing (TAM, SAM, SOM). This skill sets up no weekly watch.

## Inputs
- The alternatives buyers really compare you with, including a spreadsheet, an agency and doing nothing
- Public pages you name or paste for each one (product, pricing, docs, changelog)
- Win and loss interview notes with codes instead of names, and sales-reported reasons if you keep them
If you have none of this, I start from the alternatives you name, mark every cell "no source" and label the output a first draft.

## Approach
Competitive landscape and win/loss analysis are activities listed in the Pragmatic Institute public product framework (pragmaticinstitute.com/product/framework/); the page gives no steps, so the steps here are this guide's practice. Rows are drawn by the customer's job, so a workaround sits beside a named product. With web search, Claude in Chrome or the built-in browser, Claude reads the public pages you name and dates each one; pasted pages in a plain chat work the same. The failure it prevents: a strategy rebuilt around one person's memory of one lost deal.

## Workflow
1. Ask up to three questions: which alternatives buyers compare you with for which job, which pages and notes are in bounds, and how many interviews a theme needs before it counts as a pattern (you set the threshold).
2. Build the landscape by the customer's job. Rows are named products, workarounds and doing nothing; the steps of the job are the columns. Leave out any product buyers never mention, however loud it is in the market.
3. Source every cell: a link and the date it was read, or "not public" or "no source". Pricing only as published. A plausible guess in one cell costs the whole table its credit.
4. Code the buyer notes: one reason per line, with an interview code and won or lost. Sales-reported reasons go in their own column and are never merged in.
5. Count themes across interviews. Below your threshold a theme is a "single signal". Read buyer reasons beside sales reasons; the gap between the two is often the finding.
6. Write "where we differ" by job step, each line backed by a theme or a link. Then "what not to copy", each with a reason: off-strategy, table stakes cheap to match, or a job our customers do not have.

## Output Format
```markdown
# Competitive Analysis
Customer job: [job] | Pages read on: [date] | Pattern threshold: [n interviews, set by the user]
## Landscape by job
| Alternative | [Job step 1] | [Job step 2] | Pricing as published | Source, date read |
|---|---|---|---|---|
| [Product / workaround / doing nothing] | [from source] | [from source] | [price or "not public"] | [link, date or "no source"] |
## Win and loss themes
| Theme in buyers' words | Won or lost | Interview codes | Pattern or single signal | Sales-reported too? |
|---|---|---|---|---|
| [reason] | [won / lost] | [B1, B4] | [pattern / single signal] | [yes / no] |
## Where we differ
| Job step | Our position | Backed by |
|---|---|---|
| [step] | [better / worse / same, in what way] | [theme or link] |
## What not to copy
- [feature or move]: [off-strategy / table stakes cheap to match / a job our customers do not have]
## Decision
The [product leader] decides by [date] which gaps go into the strategic options and signs off the "what not to copy" list.
```

## Done When
- Workarounds and doing nothing appear as rows, and every cell has a link and a read date, or says "not public" or "no source"
- Buyer reasons and sales-reported reasons sit in separate columns
- Themes below the threshold are marked single signal
- Each "what not to copy" line carries a reason

## Quality Bar
- Buyers appear as interview codes; public company information only, and no tracking or profiling of competitor employees.
- Describe what a source says, never who is "better" overall; no disparagement.
- A feature tick-list is not a difference; a difference names the job step it changes.
- Never invent a competitor's price, feature or result; win and loss reasons come from buyers the team talked to, and a named person decides which gaps matter.

## Next
Run strat-needs-based-segments (Needs-Based Segmentation) to decide which customers the strategy serves first.

## About the makers

This pack is made by 90n ([90n.ai](https://90n.ai)): AI-native ways of working and tools for Product, Marketing and HR teams, built by ex-McKinsey founders. We map where time and money leak, redesign the work around AI and stay until your people run it themselves, and we run our own company on Claude. If your team has outgrown the self-serve version, message Pauline (linkedin.com/in/paulinebertry).
