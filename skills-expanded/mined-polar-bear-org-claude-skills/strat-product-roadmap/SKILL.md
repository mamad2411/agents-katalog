---
name: strat-product-roadmap
description: Builds a now, next, later roadmap with items restated as problems and linked to a strategy action, ordered by cost of delay over duration, placed by horizon with a confidence note, dated commitments flagged with who made them, a "not on the roadmap" list and a one-screen executive cut. Use for "run strat-product-roadmap", "build our product roadmap", "now next later roadmap", "roadmap without dates", "every date becomes a promise", "order the roadmap by cost of delay", "what changed on the roadmap", "executive version of the roadmap", part of the Claude Guide for Product Strategy Pack by 90n.
---

# Product Roadmap (Now, Next, Later)

## When To Use
Every date becomes a promise and the board reads the roadmap as a commitment. Use this to build the standing board the strategy is delivered through: what problems the team is on now, next and later, in which order and why, how sure you are, and what is deliberately off it. It also shows what moved since the last version, so nobody has to guess.

## When Not To Use
This is the board itself, not the meeting about it. To report shipped against said and ask for one decision, use Roadmap Review Deck. To set the quarter's measures, use Quarterly OKRs. If nobody can say why half the items exist, run Impact Map first.

## Inputs
- The strategy actions the work should serve, and the current roadmap in any form (a paste, an export, or a tickets tool read through a read-only connector)
- Per item: what a week of delay costs, in money or in bands you define, and a duration from engineering
- The last version of the roadmap, and every dated commitment with the role that made it
If you have none of this, I start from your list of current work, mark every missing link, cost and duration as [to supply] and the output as a first draft.

## Approach
Two public methods, joined. Now-Next-Later, as Janna Bastow describes it at ProdPad (https://www.prodpad.com/glossary/now-next-later-roadmap/), replaces the timeline with three horizons where detail and certainty fall on purpose. CD3, cost of delay divided by duration, from Black Swan Farming (https://blackswanfarming.com/cost-of-delay-divided-by-duration/), sets the order, so a short item that is costly to delay goes ahead of a long one that is not. The failure it prevents is the dated chart that is wrong within weeks and then gets defended instead of updated. It works the same in a plain chat with a pasted list.

## Workflow
1. Ask at most three questions: which strategy actions this roadmap serves, how you define each confidence level, and which items carry a dated commitment and which role made it.
2. Rewrite every item as a problem or outcome and link it to a strategy action. An item with no link goes to a "why is this here?" list for the owner; I do not find it a link.
3. Set cost of delay per item with you: money per week where it can be priced, otherwise bands whose meaning you write down. Duration comes from engineering, never from me. A missing value stays [to supply].
4. Compute CD3 and sort, highest first. Flag every close call: a pair whose order flips if one estimate moves by one band. Those pairs are where the owner's judgment is needed, not the arithmetic.
5. Place by horizon test. Now needs an understood problem, a clear scope and a team. Next needs a shaped problem being validated. Later needs only the problem area, and stays short. Anything that fails its test moves down, with the reason.
6. Add a confidence note per item in your own definitions, with what would raise it. No dates beyond Now, except a commitment a named role made, flagged on that one item.
7. Write "not on the roadmap" with one reason each, what changed since the last version (moved, added, removed, each with its reason), and a one-screen executive cut in outcomes only.

## Output Format
```markdown
# Now-Next-Later Roadmap
**Serves:** [strategy actions] | **Owner:** [role] | **Version:** [date] | **Confidence levels:** [your definitions]
## Board
| Horizon | Problem or outcome | Strategy action | Cost of delay (source) | Duration (from engineering) | CD3 | Confidence | What would raise it |
|---|---|---|---|---|---|---|---|
| [Now / Next / Later] | [problem] | [action] | [value or band, who set it] | [weeks, or to supply] | [result] | [level] | [test, data pull or spike] |
Close call: [Item A] against [Item B], the order flips if [estimate] moves by one band.
## Dated commitments
- [item]: [date], made by [role] to [role]
## Not on the roadmap
- [item or request theme]: [reason, or the line of the strategy's no list it falls under]
## What changed since [last version date]
| Item | Change | Reason |
|---|---|---|
| [item] | [moved / added / removed] | [reason and its source] |
## Why is this here?
- [item with no strategy action]: question for [owner role]
## Executive cut
[One screen: the outcomes in Now, then one line each for the other two horizons. No feature names.]
## Decision
[Role of the roadmap owner] approves this version and rules on the close calls by [date]; [role] confirms or withdraws each dated commitment by [date].
```

## Done When
- Every item is a problem or outcome with a strategy action or a "why is this here?" flag
- Every cost of delay and duration came from the team or is marked [to supply]; close calls are listed
- Every item passes the test of the horizon it sits in and carries a confidence note
- The only dates are commitments, each with the role that made it, and every change since the last version has a reason

## Quality Bar
- A long Later is a backlog in disguise; keep it short and broad
- A precise-looking CD3 never hides a close call, and confidence never rests on customer evidence nobody collected
- Requests appear by need and theme, never by who asked; no capacity or productivity figure per person
- No date or commitment appears that a named person did not make; cost of delay and durations come from the team, never invented.

## Next
Run strat-quarterly-okrs (Quarterly OKRs) to set the quarter's measures for the work in Now.

## About the makers

This pack is made by 90n ([90n.ai](https://90n.ai)): AI-native ways of working and tools for Product, Marketing and HR teams, built by ex-McKinsey founders. We map where time and money leak, redesign the work around AI and stay until your people run it themselves, and we run our own company on Claude. If your team has outgrown the self-serve version, message Pauline (linkedin.com/in/paulinebertry).
