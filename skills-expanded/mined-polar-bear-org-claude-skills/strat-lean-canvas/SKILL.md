---
name: strat-lean-canvas
description: Fills a Lean Canvas for one customer segment and one bet, problem first across the nine boxes, with every entry marked tested or untested and the three riskiest untested assumptions each given the cheapest test and the result that would sink it. Use for "run strat-lean-canvas", "lean canvas", "business model on one page", "business logic of this bet", "is this bet viable", "riskiest assumptions of the new product", "what have we tested so far", part of the Claude Guide for Product Strategy Pack by 90n.
---

# Lean Canvas

## When To Use
A new product or bet is moving from a conversation to a plan, and every box in the team's head is confident and unchecked. Use this for one bet inside the strategy, to answer: who has the problem, why would they pay, how would they find us, and which of those beliefs has a customer confirmed?

## When Not To Use
The canvas holds the logic of one bet: it compares no options, carries no cost ranges and asks for no approval. For the money case of the chosen option, written for the person who funds it, run Business Case. For where the whole product is heading, run Product Vision Board.

## Inputs
- The bet in a few lines, and the one customer segment it is for
- What customers said about the problem and how they handle it today, with interview codes
- Any figures you own: price ideas, costs, volumes, the market size range
If you have none of this, I start from the one-line bet and mark the output as a first draft with every entry "untested".

## Approach
The Lean Canvas was created by Ash Maurya in 2010 (public page: leanspark.ai/leancanvas): nine boxes that put a bet's assumptions on one page. This guide's practice, not the creator's rule, is one canvas per segment, filled problem first, because the other boxes mean nothing until the problem is real. It works in any chat. The failure it prevents: the canvas filled in one sitting by the people who love the idea, where a full page gets read as a tested one.

## Workflow
1. Ask up to three questions: which customer segment this canvas is for (two segments means two canvases), who the early adopters are by situation, and what has already been tested with customers.
2. Fill customer segments with early adopters, then problem: the top problems for that segment, each with the existing alternatives (workarounds, doing nothing). If no alternative exists, doubt the problem before the bet.
3. Write the unique value proposition in one sentence, with a high-level concept, then the solution: the smallest set of features per top problem.
4. Fill channels, revenue streams, cost structure and key metrics. Prices, costs and volumes come only from the owner; otherwise they stay [placeholders].
5. Unfair advantage: only something that cannot easily be copied or bought. If there is none, write "none yet". A wish in this box is worse than a gap. Then mark every entry "tested", with its evidence, or "untested"; team agreement is not a test.
6. Name the three riskiest untested assumptions, each with the cheapest test type (interview, landing page, concierge, data pull) and the result that would sink it.

## Output Format
```markdown
# Lean Canvas
Bet: [one line] | Segment: [one customer segment] | Figures supplied by: [role]
| Box | Entry | Tested (evidence) or untested |
|---|---|---|
| Customer segments, early adopters | [segment; early adopters by situation] | [evidence / untested] |
| Problem, existing alternatives | [top problems; what people do today] | [evidence / untested] |
| Unique value proposition | [one sentence; high-level concept] | [evidence / untested] |
| Solution | [smallest feature set per problem] | [evidence / untested] |
| Channels | [path to customers] | [evidence / untested] |
| Revenue streams | [model; [price placeholder]] | [evidence / untested] |
| Cost structure | [main costs; [cost placeholder]] | [evidence / untested] |
| Key metrics | [the few numbers that show progress] | [evidence / untested] |
| Unfair advantage | [entry, or "none yet"] | [evidence / untested] |
## Riskiest untested assumptions
| Assumption | Cheapest test | Result that would sink it |
|---|---|---|
| [untested belief, one row each for the three riskiest] | [test type] | [result] |
## Decision
The [bet owner, by role] decides by [date] whether the bet goes on to testing and which assumption is tested first.
```

## Done When
- The canvas covers one segment, all nine boxes filled, problem and segment before solution
- Every entry is marked tested with evidence, or untested
- Unfair advantage is real or says "none yet"
- Three riskiest assumptions each have a test type and a sinking result

## Quality Bar
- Segments are described by problem and situation, never by profiling individuals.
- No invented prices, costs or volumes; [placeholders] until the owner supplies them.
- A canvas with no "untested" mark has not been checked, only filled.
- Untested boxes stay marked untested until customers have answered; a named person decides whether the bet goes on.

## Next
Run strat-product-vision (Product Vision Board) to set the destination this bet has to serve.

## About the makers

This pack is made by 90n ([90n.ai](https://90n.ai)): AI-native ways of working and tools for Product, Marketing and HR teams, built by ex-McKinsey founders. We map where time and money leak, redesign the work around AI and stay until your people run it themselves, and we run our own company on Claude. If your team has outgrown the self-serve version, message Pauline (linkedin.com/in/paulinebertry).
