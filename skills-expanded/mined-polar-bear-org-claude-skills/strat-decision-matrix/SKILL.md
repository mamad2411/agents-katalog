---
name: strat-decision-matrix
description: Builds a Decision Matrix with criteria and weights agreed and dated before any score, pass or fail gates, a plain consequence table per option, scores with one line of evidence and a confidence mark, and a weight sensitivity check. Use for "run strat-decision-matrix", "weighted decision matrix", "compare the options on criteria we agree first", "agree the weights before we score", "who gains and who bears the cost", "would the leader change if this weight doubled", "is it too close to call", part of the Claude Guide for Product Strategy Pack by 90n.
---

# Decision Matrix

## When To Use
The decision meeting goes to whoever argues loudest, and the option that wins is the one with the most senior voice behind it. Use this when the options are distinct and you need to answer: on criteria everyone agreed before seeing a score, which option comes out ahead, and how fragile is that lead?

## When Not To Use
If the table holds one real option and two smaller copies of it, run Strategic Options first. The matrix compares and never recommends: when the comparison is done and someone has to ask for a call, write the Recommendation Memo.

## Inputs
- The option set with do nothing included, candidate criteria and the non-negotiables
- Who owns the decision, by role
- The evidence per option: interview themes, usage data, cost estimates, each with its source
If you have none of this, I start from the option names and four draft criteria for you to change, and mark the output as a first draft.

## Approach
A weighted decision matrix is common public practice with no single originator, and here it comes after a plain comparison of consequences. The order is the method: criteria, definitions, scale ends and weights are fixed and dated before any option is scored, so nobody tunes a weight toward a favourite. The consequence table comes before any number because a total hides who pays. The failure it prevents is the matrix filled in after the decision, with "strategic fit" weighted up until the expected option wins.

## Workflow
1. Ask at most three questions: who owns the decision, which criteria matter and which are non-negotiable, and what scale and weight total to use.
2. Agree criteria, definitions, what the low and high ends of the scale mean, and the weights. Date the agreement before any option is scored. Check that no two criteria count one benefit twice; if they do, merge them.
3. Apply the gates. A non-negotiable (safety, a legal duty, a promise to customers) is pass or fail, never a weight. A failed option is out, with the reason written down. On legal points, check with a qualified adviser.
4. Write the consequence table before any number: per option, who gains, who bears the cost or the effort, and who has not been consulted, using sourced facts, ranges and stated unknowns. Groups appear by role or segment.
5. Score each option per criterion with one line of evidence and a confidence mark. No evidence means a low-confidence mark, never a quiet middle score.
6. Compute the weighted totals, then double and halve each weight in turn and note whether the leader changes. Flag criteria where all options tie, and the gap between first and second. A small gap with low confidence is written as "too close to call", with the evidence that would separate the two.

## Output Format
```markdown
# Decision Matrix
**Decision:** [question] | **Owner:** [role] | **Criteria and weights agreed on:** [date, before scoring]
## Criteria and weights
| Criterion | Definition | Low end means | High end means | Weight |
|---|---|---|---|---|
| [criterion] | [definition] | [low] | [high] | [weight] |
## Gates (pass or fail)
- [Non-negotiable]: [option] [passes / fails], [reason and source]
## Consequences
| Option | Who gains | Who bears the cost or effort | Not yet consulted | Unknowns |
|---|---|---|---|---|
| [option] | [role or segment] | [role or segment] | [role] | [unknown] |
## Scores
| Option | Criterion | Score | Evidence (one line, source) | Confidence | Weighted |
|---|---|---|---|---|---|
| [option] | [criterion] | [score] | [evidence] | [high / low] | [score x weight] |
## Totals and sensitivity
- [Option]: weighted total [total]; leader changes if a weight is doubled or halved: [no / yes, on criterion]
- Ties on [criteria]. Gap between first and second: [gap]. Verdict: [clear lead / too close to call]
## Decision
[Role of the decision owner] makes the call, or asks for [evidence] on [criterion], by [date].
```

## Done When
- Criteria and weights carry a date earlier than the first score
- Every failed gate has a reason, and the consequence table is filled before the scores
- Every score has a line of evidence and a confidence mark
- The sensitivity result, the ties and any close finish are stated plainly

## Quality Bar
- No criterion rates a sponsor, team or individual, and there is no "stakeholder support" score; options are scored, never people
- Weights are not reopened once scores are visible; a change is a new dated version with the reason
- The matrix compares and carries no recommendation line
- Cost and impact figures come from the user with a source, or are marked as an assumption
- The highest total is an input to the call, not the call; the owner decides, and no figure is invented.

## Next
Run strat-strategic-bets (Strategic Bets) to write, for the option the owner chooses, what would have to be true and what would prove it wrong.

## About the makers

This pack is made by 90n ([90n.ai](https://90n.ai)): AI-native ways of working and tools for Product, Marketing and HR teams, built by ex-McKinsey founders. We map where time and money leak, redesign the work around AI and stay until your people run it themselves, and we run our own company on Claude. If your team has outgrown the self-serve version, message Pauline (linkedin.com/in/paulinebertry).
