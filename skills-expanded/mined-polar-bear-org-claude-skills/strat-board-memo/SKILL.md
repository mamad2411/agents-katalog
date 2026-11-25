---
name: strat-board-memo
description: Writes the product section of the board papers in one or two pages read ahead, with the questions for the board first as real forks, progress against plan, the few metrics that matter with base, period and source, the roadmap as horizons with confidence instead of dates, and risks with the response and an owner by role. Use for "run strat-board-memo", "board memo for product", "product section of the board papers", "board pre-read", "the chief executive needs the product update by Friday", "questions for the board", "roadmap for the board without dates", "cut the dashboard down for the board", part of the Claude Guide for Product Strategy Pack by 90n.
---

# Board Memo

## When To Use
The chief executive needs the product section by Friday, and the last one was a dashboard dump nobody discussed. Use this for one or two pages the board reads ahead. It answers: are we on plan, which few numbers show it, what could go wrong, and what do we want the board's view on?

## When Not To Use
If the readers are the leaders inside the company who steer the roadmap, Roadmap Review Deck fits better. If you need one call made on one choice, Recommendation Memo asks for it; this memo reports and puts questions to the board, it does not argue for a single option.

## Inputs
- The plan or targets the board last saw, and current results from an export or a connector (read only)
- The current roadmap, and any dated commitment already made, with who made it
- The top risks with what is being done, the questions for the board, the send date and the page limit
If you have none of this, I start from the plan and the questions you want answered, leave every figure as [placeholder] and mark the output as a first draft.

## Approach
The board pre-read with questions first follows Pete Flint's public essay at NFX (https://www.nfx.com/post/how-to-run-an-early-stage-board-meeting): send the material ahead, show performance against target, and bring two or three questions so the meeting goes to forks in the road, not updates. The judgment is in what gets left out. The failure this prevents: thirty metrics, no question, a roadmap with dates the board writes down, and a meeting that fills the silence with its own agenda. In Claude Docs the memo is one shared document. It works the same in a plain chat.

## Workflow
1. Ask at most three questions: the two or three questions for the board, the send date (you set it), and the page limit (one or two pages).
2. Put the questions for the board first. Each is a real fork: the options, the current lean, and what the board's view would change. A question with one acceptable answer is an update, so it moves down.
3. Write progress against plan: each plan item with target, result, base and period. Behind plan is said in the first line, with the reason in terms of the work and the market.
4. Pick the few metrics that matter (you choose; three to five is a starting point). Each carries value, base, period, comparison and source. Everything else is an appendix link.
5. Show the roadmap as horizons with confidence, not dates. Dated commitments are carried over from the roadmap one by one, each with the role that made it; none is added here. Then list the risks with the response and an owner by role; people topics stay as roles and hiring needs.
6. Cut to the page limit: trim progress detail before questions or risks. Mark every disclosure, legal or board-duty point with "check with a qualified adviser".

## Output Format
```markdown
# Board Memo: Product
**Period:** [period] | **On plan:** [yes / behind / ahead, one line] | **Send by:** [date]
## Questions for the board
1. [question]: options [A, B]; current lean [option]; what your view would change: [placeholder]
## Progress against plan
| Plan item | Target | Result | Base and period | Source |
|---|---|---|---|---|
| [item] | [value] | [value] | [counted over, period] | [source] |
## The metrics that matter
| Metric | Value | Base | Period | Comparison | Source |
|---|---|---|---|---|---|
| [metric] | [value] | [base] | [period] | [value, period] | [source] |
## Roadmap by horizon
| Horizon | Theme or outcome | Confidence | Dated commitment, if any (date, role that made it) |
|---|---|---|---|
| [Now / Next / Later] | [theme] | [high / medium / low: why] | [none / date, role] |
## Risks
- [risk]: [what we are doing]; owner: [role]
## Points for an adviser
- [disclosure, legal or board-duty point]: check with a qualified adviser
## Decision
[Chief executive] approves the memo for the board papers by [date]; the board gives its view on each question at the meeting of [date].
```

## Done When
- The questions come first, each a real fork with options and a lean
- Every figure has a base, a period and a source
- The roadmap shows horizons and confidence, with any date tied to the role that committed to it
- The memo fits the page limit, with detail behind an appendix link

## Quality Bar
- No dashboard dump: only the metrics you picked, and behind plan is stated in the first line, never buried
- No named-employee performance; people appear as roles and hiring needs
- Disclosure, legal and board-duty points are flagged, never answered: check with a qualified adviser
- Every figure carries its source and period; the chief executive signs what goes to the board.

## Next
Run strat-decision-record (Strategy Decision Record) to keep what was decided, and why, once the board has given its view.

## About the makers

This pack is made by 90n ([90n.ai](https://90n.ai)): AI-native ways of working and tools for Product, Marketing and HR teams, built by ex-McKinsey founders. We map where time and money leak, redesign the work around AI and stay until your people run it themselves, and we run our own company on Claude. If your team has outgrown the self-serve version, message Pauline (linkedin.com/in/paulinebertry).
