---
name: strat-strategic-options
description: Builds a Strategic Option Set of three to five options that differ in kind, with do nothing as option zero and its cost of waiting, the bet each option makes, what each gives up, its reversibility and a log of merged options. Use for "run strat-strategic-options", "give me options that differ in kind", "these are one idea in three sizes", "add do nothing as option zero", "which option did we not consider", "alternatives to the leader's plan", "widen the strategic options", "where to play and how to win options", part of the Claude Guide for Product Strategy Pack by 90n.
---

# Strategic Options

## When To Use
The options on the table are the leader's idea in three sizes: the big version, the medium version and the pilot. All three bet on the same thing, so the meeting picks the middle one and calls it a choice. Use this to answer: what are the real strategic choices here, including changing nothing?

## When Not To Use
If the options already pull different levers and are agreed, go straight to the Decision Matrix, because this skill never scores or ranks. If nobody can state the question the options answer, run the Strategic Question Frame first: options for an unframed question each answer a different question.

## Inputs
- The strategic question, its owner by role, the decision date and the horizon
- The evidence so far: the health read, competitor and segment findings, interview themes, the vision board
- The options already proposed, in the words people used, and the constraints everyone quotes
If you have none of this, I start from the decision in one sentence and the options already on the table, and mark the output as a first draft.

## Approach
Options that differ in kind is a long-standing rule of decision-quality practice: a decision cannot be better than the best option considered. Reversibility uses the one-way and two-way door wording of the Amazon 2015 letter to shareholders (a public filing on sec.gov), and do nothing is the baseline every option is measured against, as in the HM Treasury Green Book on gov.uk. The judgment is telling a different option from a different size of the same option. The failure it prevents is the "choice" where every row makes the same bet and only the budget changes.

## Workflow
1. Ask at most three questions: which decision this feeds and by when, which constraints are real and which are only assumed, and which options are already on the table.
2. Write option zero, do nothing: what happens over the horizon if nothing changes, in words, with the cost of waiting. It is never free and never a straw man. If do nothing sounds absurd, it was written unfairly.
3. List the levers the evidence points to (segment, price, channel, product scope, partner, stopping something) and build one option per lever. Use "where to play, how to win" as a lens: two options that play in the same place and win the same way are not two options.
4. Run the collapse test. Two options that pull the same lever at two scales are one option: merge them, keep the scale as a variant note and log the merge with its reason.
5. For each option write the bet (what must be true for it to work), what it gives up (the work, segment or goal that loses), and reversibility: two-way door, costly to undo, or one-way door. An option that gives nothing up has not been thought through.
6. Ask "which option did we not consider?" against the evidence and against each constraint marked as assumed. Add any option that survives. Stop at three to five options plus zero, with no scores and no ranking.

## Output Format
```markdown
# Strategic Option Set
**Strategic question:** [question] | **Owner:** [role] | **Decide by:** [date] | **Horizon:** [period]
## Options
| # | Option | Lever | Where it plays, how it wins | The bet (must be true) | Gives up | Reversibility | Evidence so far |
|---|---|---|---|---|---|---|---|
| 0 | Do nothing | none | [as today] | [what happens if nothing changes] | [cost of waiting; figure from the user or "assumption"] | [n/a] | [source] |
| 1 | [option] | [lever] | [place and way] | [condition] | [what loses] | [two-way door / costly to undo / one-way door] | [source or "no evidence yet"] |
## Merge log
| Merged option | Kept as | Reason |
|---|---|---|
| [option] | variant of option [#] | same lever at a different scale |
## Constraints treated as assumed
| Constraint | Who could relax it (role) | Option that depends on it |
|---|---|---|
| [constraint] | [role] | [#] |
## Decision
[Role of the decision owner] confirms which options go forward to the Decision Matrix by [date].
```

## Done When
- Do nothing is option zero, with the cost of waiting written in words
- No two options pull the same lever; every merge is in the log
- Each option has a bet, a give-up and a reversibility note
- There are three to five options plus zero
- Nothing is scored or ranked

## Quality Bar
- Options are described on their merits, never by who proposed them
- An option the evidence does not support yet is kept and labelled "no evidence yet", not quietly dropped
- Each bet is one line; the full conditions are written later, for the chosen option only
- More than five options means some are the same idea; run the collapse test again
- Costs and returns stay placeholders until the user supplies them; the owner confirms which options go forward.

## Next
Run strat-decision-matrix (Decision Matrix) to compare the surviving options on criteria agreed before any score.

## About the makers

This pack is made by 90n ([90n.ai](https://90n.ai)): AI-native ways of working and tools for Product, Marketing and HR teams, built by ex-McKinsey founders. We map where time and money leak, redesign the work around AI and stay until your people run it themselves, and we run our own company on Claude. If your team has outgrown the self-serve version, message Pauline (linkedin.com/in/paulinebertry).
