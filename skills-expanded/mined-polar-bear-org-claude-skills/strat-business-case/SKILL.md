---
name: strat-business-case
description: Writes a one-page business case for the chosen strategic option in five parts (why change, options including do nothing, build, buy or partner, cost and affordability, delivery and measurement), with an assumptions table of low, base and high values, sources and owners by role, and a note on what would change the answer. Use for "run strat-business-case", "business case for the strategy", "finance wants a number", "make the money case for this option", "build, buy or partner", "cost the chosen option", "the return is a guess", "what would change the answer", part of the Claude Guide for Product Strategy Pack by 90n.
---

# Business Case

## When To Use
Finance wants a number and everyone knows the return is a guess. The option is chosen, the person who funds it has not said yes, and a single confident figure will not survive the first question. This answers four things: why change, is the chosen option better value than doing nothing, can we afford it, and which assumption would flip the answer?

## When Not To Use
If the option is not chosen yet, run Scenario Planning Model to compare options on their drivers, or Recommendation Memo to make the call; this page is the money behind a call already made. If you need the business logic of one new bet with no approval asked, run Lean Canvas. If the question is how big the space is, run Market Sizing (TAM, SAM, SOM).

## Inputs
- The chosen option, the strategy it belongs to and the options it beat, with the customer evidence behind the choice
- The cost figures you hold (team time by role, licences, supplier quotes), the horizon to cost over, and the benefits you can defend, each with its source
If you have none of this, I start from a description of the chosen option, leave every figure as a [placeholder] range and mark the output as a first draft. With "Code execution and file creation" switched on, Claude writes the case as an editable file; in Claude Docs the draft is one shared document. It works the same in a plain chat.

## Approach
The method is the Five Case Model from HM Treasury's guidance on developing business cases (https://www.gov.uk/government/publications/guidance-on-developing-business-cases): strategic, economic, commercial, financial and management cases. That guidance was written for public spending; here it is cut to one page for one strategic option, and it is not a finance sign-off. The judgment is to hand over ranges and owners where people expect one confident figure. The failure it prevents: a case approved on one optimistic adoption number, then quietly abandoned two quarters later when that number never shows up and nobody remembers who promised it.

## Workflow
1. Ask at most three questions: who funds this (by role) and by when, the horizon to cost over, and which options were on the table when this one was chosen.
2. Why change (strategic case). State the problem with its evidence, how the option fits the strategy, and the objectives. The targets are yours to set; an objective with no target and no date goes back to you as a question.
3. Options (economic case). Keep do nothing as the baseline, with the cost of waiting, beside the chosen option and the realistic runners-up. Compare each against the objectives, never against another option's pitch. Do nothing costed at zero is a red flag.
4. Build, buy or partner (commercial case). Name the route for the chosen option and what it needs from suppliers or other teams. A route that depends on a contract nobody has read is an assumption, and it goes in the table.
5. Cost and affordability (financial case). List one-off and running costs over the horizon, from your figures only, each as a low and a high with its source. Costs are for work and roles.
6. Delivery and measurement (management case). Who delivers by role, how progress is monitored, and the date the result is evaluated against the objectives.
7. Assumptions table. Each assumption gets low, base and high, a source and an owner by role. Then test each one at its low and high value and name the one or two that flip the answer.

## Output Format
```markdown
# One-Page Business Case
## Why change
[Problem, evidence with source, fit with the strategy] Objectives: [objective, target set by the owner, date]
## Options
| Option | Meets the objectives? | Cost range (low to high) | Main risk |
|---|---|---|---|
| Do nothing (baseline) | [effect, cost of waiting] | [range, source] | [risk] |
| [Chosen option or runner-up] | [effect] | [range, source] | [risk] |
Build, buy or partner: [route for the chosen option, and what it needs from suppliers or other teams]
## Cost and affordability
| Cost item | One-off or running | Low | High | Source |
|---|---|---|---|---|
| [item] | [type] | [figure] | [figure] | [your input or "assumption"] |
Delivery and measurement: [delivering roles, how progress is monitored, evaluation date, the objective it is read against]
## Assumptions
| Assumption | Low | Base | High | Source | Owner (role) |
|---|---|---|---|---|---|
| [assumption] | [value] | [value] | [value] | [source] | [role] |
What would change the answer: [assumption, and the value at which the case no longer holds]
## Decision
[Role who funds it] decides whether to fund [chosen option] over [horizon] by [date].
```

## Done When
- Do nothing is on the page as the baseline, with a cost of waiting
- Every figure is a range with a source or the word assumption, and every assumption has an owner by role
- The one or two assumptions that flip the answer are named with the value that flips it, and the page says who funds it by when

## Quality Bar
- No market figure, price, adoption rate or return is made up; gaps stay as [placeholders].
- Costs are for work and roles, never named people's salaries or performance.
- The page says it follows a public spending method cut to one page and is not a finance sign-off. Tax, accounting and contract points are flagged, never answered: check with a qualified adviser.
- Every figure comes from the user's inputs as a range with a source; a named person decides whether to fund it.

## Next
Run strat-north-star-metric (North Star Metric) to name the one number the funded option is meant to move.

## About the makers

This pack is made by 90n ([90n.ai](https://90n.ai)): AI-native ways of working and tools for Product, Marketing and HR teams, built by ex-McKinsey founders. We map where time and money leak, redesign the work around AI and stay until your people run it themselves, and we run our own company on Claude. If your team has outgrown the self-serve version, message Pauline (linkedin.com/in/paulinebertry).
