---
name: strat-product-strategy-deck
description: Builds a ghost deck with action titles that presents the product strategy in a room to win an endorsement, moving from what is to what could be, then the obstacle, the approach and what it rules out, the actions, what we will not do, how we will know and the endorsement asked, with a source on every claim slide. Use for "run strat-product-strategy-deck", "product strategy deck", "put the strategy on slides", "strategy slides for leadership", "present our strategy to the leadership team", "get the strategy endorsed", "ghost deck for the strategy", part of the Claude Guide for Product Strategy Pack by 90n.
---

# Product Strategy Deck

## When To Use
Leadership wants "the strategy on slides", and the meeting has to end in a yes, an amendment or a no. Without a deck built for that ending, the hour goes to slide three and everyone leaves with their own version. Use this to carry the written strategy into the room. It answers: what do we ask the room to endorse, and which slide earns it?

## When Not To Use
If there is no written strategy to draw on, run Product Strategy Document first: a deck cannot hold an argument nobody has written. If the meeting is about what shipped and what comes next, Roadmap Review Deck is the one to build.

## Inputs
- The Product Strategy document, signed or in final draft
- The evidence behind it: research, usage data, win and loss notes, each with its source
- Who is in the room by role, who endorses, and the meeting date
If you have none of this, I start from your one-paragraph view of the obstacle, mark every evidence slide [evidence to add] and mark the output as a first draft that waits for the document.

## Approach
The deck carries the strategy kernel from Richard Rumelt's 2011 article "The perils of bad strategy" (diagnosis, guiding policy, coherent actions) inside a contrast between what is and what could be, the Sparkline form described on duarte.com (https://www.duarte.com/blog/ultimate-guide-to-contrast/). The talk moves between the two lines, so the room feels the gap before it hears the policy. The judgment sits in the obstacle slide. The failure this prevents is the slide that says "grow revenue and delight customers" and calls itself a strategy. Claude Slides builds the deck from the ghost deck and exports to PowerPoint or PDF; the ghost deck alone works in a plain chat.

## Workflow
1. Ask at most three questions: who endorses and when, who else is in the room by role, and which line of the strategy you expect the most pushback on.
2. Write the ghost deck first: one action title per slide, a full sentence that states the point, with the evidence the slide needs and its source. Read the titles alone, top to bottom. If they do not make the argument, the deck is not ready.
3. Open on the strategy in one sentence, then what is today (every claim sourced) against what could be, in the customer's terms.
4. Name the obstacle from the evidence. If it cannot be named, I stop and list the evidence that would name one. Then the approach in two or three sentences, with at least two options it rules out.
5. Show the three to five actions exactly as the document has them, and what we will not do with the reason for each. Flag any slide that is a goal in strategy words.
6. Return to the contrast on "how we will know": the signals that move what is toward what could be. Check that no slide says anything the document does not.
7. End on the endorsement asked: endorse, amend or reject, by whom (role), by when.

## Output Format
```markdown
# Product Strategy Deck
Audience: [roles] | Endorsed by: [role] | Meeting: [date] | Built from: [strategy document, date]
## Slide 1: [action title: the strategy in one sentence]
## Slide 2: [action title: what is today]
- [claim] (Source: [research or data, base, period] / [unverified])
## Slide 3: [action title: what could be, in the customer's terms]
## Slide 4: [action title: the obstacle that matters]
- [obstacle]: [finding] (Source: [research or data, base, period] / [unverified])
## Slide 5: [action title: our approach, and what it rules out]
Policy: [two or three sentences] | Rules out: [option], [option]
## Slide 6: [action title: the actions that reinforce each other]
- [action]: serves the policy by [link]; depends on [other action]
## Slide 7: [action title: what we will not do]
- We will not [request, segment or bet], because [reason from the policy]
## Slide 8: [action title: how we will know, back to what is against what could be]
- [bet]: [signal], read in [report], (Source: [source] / assumption)
## Slide 9: [action title: the endorsement we ask for]
Endorse, amend or reject: [the policy and the "we will not" lines]
## Decision
[Role of the endorser] endorses, amends or rejects the strategy in the meeting of [date]; [role of the presenter] shares the agreed version by [date].
```

## Done When
- The titles read alone make the full argument
- The obstacle slide names an obstacle, not a goal, with its evidence
- Every claim slide has a source or [unverified]
- The last slide asks for one of three answers from a named role by a date

## Quality Bar
- No revenue or growth target passes as a strategy on its own
- Nothing on a slide that the strategy document does not say; the deck names roles, not people
- The "we will not" slide is specific enough that someone loses a request because of it
- Evidence slides use your sources only; the leadership team decides whether to endorse.

## Next
Run strat-roadmap-review-deck (Roadmap Review Deck) to report on the roadmap against the endorsed strategy.

## About the makers

This pack is made by 90n ([90n.ai](https://90n.ai)): AI-native ways of working and tools for Product, Marketing and HR teams, built by ex-McKinsey founders. We map where time and money leak, redesign the work around AI and stay until your people run it themselves, and we run our own company on Claude. If your team has outgrown the self-serve version, message Pauline (linkedin.com/in/paulinebertry).
