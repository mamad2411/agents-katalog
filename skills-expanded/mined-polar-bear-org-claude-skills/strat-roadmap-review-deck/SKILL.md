---
name: strat-roadmap-review-deck
description: Builds a roadmap review deck that opens on the ask, recaps the strategy, shows shipped against said from the last review, lays out Now, Next and Later by theme with confidence and a committed or aspirational label, gives the costed no list and the trade-off that moved the most, and ends on one decision. Use for "run strat-roadmap-review-deck", "roadmap review deck", "roadmap slides for leadership", "quarterly roadmap review", "show what we shipped against what we said", "roadmap without dates", "explain what we said no to", "our roadmap dates were read as promises", part of the Claude Guide for Product Strategy Pack by 90n.
---

# Roadmap Review Deck

## When To Use
The roadmap shown in March is quoted back in September as broken promises. Use this before a review with the leaders who steer the roadmap, when you have to show what happened to the last plan, what comes next with honest confidence, and what you are not doing. It answers: what changed, what did it displace, and what do we need you to decide?

## When Not To Use
This deck never orders or places items: if the board itself needs work, run Product Roadmap (Now, Next, Later) first and bring the result here. For the pages a board reads ahead of its meeting, use Board Memo.

## Inputs
- The roadmap from the last review, the Now items above all, and what happened to each
- The current roadmap as it stands, and the strategy document it serves
- The big requests since the last review, with the need behind each
If you have none of this, I start from your current Now list and the strategy in a paragraph, mark shipped against said as [to fill from the last review] and mark the output as a first draft.

## Approach
Now-Next-Later, from Janna Bastow's page at ProdPad (https://www.prodpad.com/glossary/now-next-later-roadmap/), replaces dates with horizons of falling certainty. Each item also carries a label from OKR practice at What Matters (https://www.whatmatters.com/faqs/okr-meaning-definition-example): committed, or aspirational. The judgment is in the costed no list, because a no with its displacement written down stops the next loud request from walking straight onto the board. The failure this prevents is the review that shows only the new plan, so nobody can see what was said last time. Claude Slides builds the deck from the ghost deck and exports to PowerPoint or PDF; the ghost deck alone works in a plain chat.

## Workflow
1. Ask at most three questions: the single decision or resource ask this review must end on, how you define high, medium and low confidence, and who decides and on what date.
2. Make slide 1 the ask, in one sentence. Then recap the strategy in one slide: the policy and the two or three outcomes the roadmap serves, from the strategy document. No strategy document: no slide, and I say so.
3. Shipped against said: every Now item from the last review with what happened (shipped, moved, dropped) and why, one line each. Moved and dropped items stay visible. Reasons are about the work and the market, never about a person.
4. Lay out the horizons as the roadmap has them, grouped by theme or outcome, not by team. Each item gets a confidence note in your definitions and a committed or aspirational label. Any date shown names the role that committed to it.
5. Build the costed no list: each big request by need and theme, the reason taken from the not-doing list or the roadmap's "not on the roadmap" lines where they exist, and what saying yes would displace. That displacement is the part only this deck adds.
6. Pick the trade-off that moved the most since the last review and show it with its evidence. Close on the one decision, with a date.

## Output Format
```markdown
# Roadmap Review Deck
Review date: [date] | Audience: [roles] | Decider: [role] | Last review: [date]
## Slide 1: [action title: the decision or ask in one sentence]
Ask: [decision or resource] | Owner: [role] | By: [date]
## Slide 2: [action title: the strategy this roadmap serves]
Policy: [one line] | Outcomes: [two or three] | Source: [strategy document, date]
## Slide 3: [action title: what happened to the Now items of the last review]
| Item | Said at the last review | What happened | Why |
|---|---|---|---|
| [item] | [Now, label] | [shipped / moved / dropped] | [reason, Source: [release note, ticket]] |
## Slide 4: [action title: the three horizons by theme]
| Theme | Horizon | Item (problem or outcome) | Confidence | Label |
|---|---|---|---|---|
| [theme] | [Now / Next / Later] | [item] | [high / medium / low: why] | [committed / aspirational] |
## Slide 5: [action title: what we are not doing, and what a yes would cost]
- [request, by need and theme]: [reason]; a yes displaces [item, horizon]
## Slide 6: [action title: the trade-off that moved the most]
- Moved: [item] | Displaced: [item] | Evidence: [finding] (Source: [document, base, period] / assumption)
## Decision
[Role of the decider] decides [the ask] in the review of [date]; [role of the roadmap owner] updates the roadmap and shares it by [date].
```

## Done When
- The deck opens and ends on the same single ask
- Every Now item from the last review appears on slide 3 with what happened
- Every item sits in one horizon with a confidence note and a label
- Every no has a reason and a displacement

## Quality Bar
- No dates on Next or Later unless a commitment requires one, and then that item alone is flagged with who made it
- Requests are shown by need and theme, never ranked by who asked
- A slip is explained by the work and the market, never by a person
- The order and placement of items come from the roadmap; this deck changes neither
- Claude lays out the trade-offs; you decide what goes on the roadmap and what is asked. No date appears that a named person did not commit to.

## Next
Run strat-board-memo (Board Memo) to write the product section the board reads ahead.

## About the makers

This pack is made by 90n ([90n.ai](https://90n.ai)): AI-native ways of working and tools for Product, Marketing and HR teams, built by ex-McKinsey founders. We map where time and money leak, redesign the work around AI and stay until your people run it themselves, and we run our own company on Claude. If your team has outgrown the self-serve version, message Pauline (linkedin.com/in/paulinebertry).
