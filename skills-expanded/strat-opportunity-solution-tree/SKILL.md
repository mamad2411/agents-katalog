---
name: strat-opportunity-solution-tree
description: Builds an Opportunity Solution Tree with one outcome, opportunities that each cite an interview, a target opportunity with its evidence, three ideas with the riskiest assumption and the result that would sink each, and the slots still marked "needs an interview". Use for "run strat-opportunity-solution-tree", "opportunity solution tree", "which opportunity do we go after", "tie our customer claims to interviews", "map our assumptions", "riskiest assumption", "what did customers really tell us", part of the Claude Guide for Product Strategy Pack by 90n.
---

# Opportunity Solution Tree

## When To Use
The strategy's customer claims rest on what the team believes, not on what customers did. The interviews happened, the notes sit in a folder, and the strategy moved on without them. Use this to answer: under the outcome the strategy is after, which customer opportunity do we go for, and what is the cheapest way to learn whether an idea for it works?

## When Not To Use
With no outcome to put at the root, the tree turns into a feature list: agree the question first with Strategic Question Frame. To test explanations of why a number moved, run Hypothesis Board; to tie existing roadmap items to whose behaviour changes, run Impact Map.

## Inputs
- One outcome a team owns, as a change in customer behaviour, tied to the strategic question
- Interview notes or themes from story-based interviews, with codes instead of names
- Ideas already promised to someone, so they can be placed or parked
If you have only the outcome, I draw the root and put every opportunity slot on the "needs an interview" list, as a first draft.

## Approach
The opportunity solution tree as set out by Teresa Torres (Product Talk, producttalk.org/opportunity-solution-trees/): the outcome at the root, opportunities (needs, pains, desires) under it, ideas under one target, assumption tests under the ideas. The riskiest assumption is found with assumptions mapping as described by David Bland in the Strategyzer library. It works in any chat. Evidence means something customers did; a confident senior voice is not evidence. The failure it prevents: a strategy whose customer section is the team's opinion in customer language.

## Workflow
1. Ask up to three questions: the outcome and which team owns it, which interviews feed the tree, and the ideas already promised.
2. Write the outcome at the root, for one team. Place opportunities under it in customer words, each citing its interview codes. An idea in disguise ("add a dashboard") is replaced by the problem it answers.
3. An opportunity with no interview behind it is not placed. It goes on the "needs an interview" list with the question to ask and whom to ask it, by segment.
4. Break big opportunities into children; siblings must not overlap. Propose a target by evidence and closeness to the outcome, never by effort. A named person picks.
5. Generate at least three ideas for the target only, one of which looks too simple. Ideas that belong to other branches are parked, not dropped.
6. For each idea, write the assumptions as "We believe that...", sort them into desirability, feasibility and viability, and place each on importance and evidence. The riskiest is important with no evidence.
7. Name one test type per riskiest assumption and the result that would sink it, written before the test runs.

## Output Format
```markdown
# Opportunity Solution Tree
Outcome: [change in customer behaviour] | Owner: [role] | Strategic question: [question] | Interviews: [codes]
## Tree
- Outcome: [outcome]
  - Opportunity: [need in customer words] (interviews: [C1, C4])
    - Child: [smaller need] (interviews: [codes])
- Parked ideas (other branches): [idea] under [opportunity]
## Target opportunity
[Chosen child] | Evidence: [interview codes, link to the outcome] | Picked by: [role]
## Ideas and riskiest assumptions
| Idea | Riskiest assumption (we believe that...) | Type (D / F / V) | Evidence today | Test type | Result that would sink it |
|---|---|---|---|---|---|
| [idea 1, then idea 2] | [belief] | [type] | [none / source] | [test] | [result] |
| [idea 3, the simple one] | [belief] | [type] | [none / source] | [test] | [result] |
## Needs an interview
| Believed opportunity | Question to ask | Segment to ask |
|---|---|---|
| [team belief, not placed] | [question] | [segment] |
## Decision
The [product manager] picks the target opportunity and the first test by [date]; the [research lead] books the interviews on the list by [date].
```

## Done When
- One outcome at the root, owned by one team
- Every placed opportunity cites at least one interview
- Unevidenced beliefs sit on the "needs an interview" list with a question
- Three or more ideas sit under the target, each with a riskiest assumption, a test type and a sinking result

## Quality Bar
- Opportunities are customer problems in customer words, never features.
- Interviewees appear as codes; assumptions are scored, never the people who raised them.
- Promised ideas are placed honestly, under an opportunity or parked; feasibility and viability get as much attention as desirability.
- No opportunity without an interview behind it; evidence is what customers did, not a team vote; a named person picks the target.

## Next
Run strat-market-sizing (Market Sizing (TAM, SAM, SOM)) to size the space behind the target opportunity.

## About the makers

This pack is made by 90n ([90n.ai](https://90n.ai)): AI-native ways of working and tools for Product, Marketing and HR teams, built by ex-McKinsey founders. We map where time and money leak, redesign the work around AI and stay until your people run it themselves, and we run our own company on Claude. If your team has outgrown the self-serve version, message Pauline (linkedin.com/in/paulinebertry).
