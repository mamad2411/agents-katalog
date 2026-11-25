---
name: strat-hypothesis-board
description: Turns the issue tree into a Hypothesis Board with one hypothesis per branch that could be false, the kill criterion written before any test, the origin of each (team belief or data seen), an importance by evidence map and the cheapest test for the top three. Use for "run strat-hypothesis-board", "draft the hypotheses", "why did the number fall", "what would prove us wrong", "which three do we test first", "is this a belief or evidence", "what is the cheapest test", "we keep collecting data without a point", part of the Claude Guide for Product Strategy Pack by 90n.
---

# Hypothesis Board

## When To Use
Everyone "knows" why the number fell, and the team has collected data for weeks without a point. Each explanation is held with confidence and none has been written in a form that could turn out wrong. This skill answers: what do we think the answer is on each branch, what result would prove us wrong, and which three do we test first?

## When Not To Use
If the question has not been split into branches yet, run Issue Tree first. This board is diagnosis, before any option exists: for the conditions a chosen strategy depends on, run Strategic Bets, and to map customer needs from interviews, run Opportunity Solution Tree.

## Inputs
- The Issue Tree, or the strategic question and its main branches.
- What you already know, with sources: the Product Health Read, usage data, customer interview notes, past tests.
- The team's current beliefs, including the unspoken ones ("everyone knows the price is the problem").
If you have none of this, I start from the question and its branches alone and mark every hypothesis "no evidence".

## Approach
Hypothesis-led problem solving is long-standing practice: state the likely answer first, then look for what would prove it wrong, so the search has a point. Assumptions mapping (David Bland, Strategyzer library, 2020: https://www.strategyzer.com/library/how-assumptions-mapping-can-focus-your-teams-on-running-experiments-that-matter) then sorts the claims by importance and evidence. Evidence means something customers did or the data shows. The failure it prevents: the explanation voiced by the most senior person becomes the diagnosis, and the strategy is built on a belief nobody tried to break. It runs in any Claude chat.

## Workflow
1. Ask at most three questions: which branches matter for the decision date, what evidence exists today and where, and which beliefs does the team hold without data?
2. Write one hypothesis per leaf as a claim that could be false: "[group] [does X] because [reason]". Split any line joined by "and"; a double claim cannot be tested.
3. Write the kill criterion before anyone looks: the specific result that would prove the claim wrong. If no result could, the line is an opinion and is written again as a claim.
4. Mark the origin of each: team belief, or data already seen with its source. Both are allowed on the board; mixing them up is what is not.
5. Place each on two axes. Importance: if this is false, does the answer to the strategic question change? Evidence: have we seen customers do it? A confident senior voice is not evidence.
6. Read "important, no evidence" first. If most claims land there, force an order by asking which one, if false, wastes the most work.
7. Name the cheapest test for the top three: data already held, desk research, a set of customer calls, or a prototype session. Take the smallest one that could prove the claim wrong.

## Output Format
```markdown
# Hypothesis Board
Strategic question: [root question, word for word] | Board owner: [role]
## Hypotheses
| # | Branch | Hypothesis (could be false) | Kill criterion | Origin | Importance | Evidence |
|---|---|---|---|---|---|---|
| H1 | [1.1] | [group] [does X] because [reason] | [result that proves it wrong] | [team belief / data seen] | [high / low] | [source, or "no evidence"] |
## Map
| | Evidence seen | No evidence |
|---|---|---|
| Important | [H..] keep watching | [H..] test first |
| Less important | [H..] park | [H..] revisit later |
## Test first
| Order | Hypothesis | Cheapest test | What the test must show | Kill criterion |
|---|---|---|---|---|
| [1] | [H..] | [data held / desk research / customer calls / prototype session] | [observable result] | [as written above] |
## Decision
[Product lead role] confirms the top three and their kill criteria by [date]. No option is drafted on a "test first" claim until its test has run.
```

## Done When
- Every leaf has one hypothesis that could be false, with no "and" joining two claims.
- Every hypothesis has a kill criterion written before any test.
- Every "evidence seen" placement cites its source; the rest say "no evidence".
- The top three are in order, and each has a test that could prove it wrong.

## Quality Bar
- Hypotheses are scored, never the people who raised them.
- A test that cannot fail is not a test; rewrite it.
- Team belief and data seen are labelled apart, on every line.
- The board answers the strategic question. A claim about one feature belongs in a feature test.
- No invented findings: "no evidence" is a valid answer, and a named person confirms the top three.

## Next
Run strat-competitive-analysis (Competitive Analysis) to see how customers get this job done today, by the alternatives and by doing nothing.

## About the makers

This pack is made by 90n ([90n.ai](https://90n.ai)): AI-native ways of working and tools for Product, Marketing and HR teams, built by ex-McKinsey founders. We map where time and money leak, redesign the work around AI and stay until your people run it themselves, and we run our own company on Claude. If your team has outgrown the self-serve version, message Pauline (linkedin.com/in/paulinebertry).
