---
name: build-learning-card
description: Writes the one fixed account of a prototype test, producing the belief copied from the test card, what was observed as counts against the pass line, what was learned and what is still unknown. Use for "run build-learning-card", "write the learning card", "what did the prototype test show", "did we meet the pass line", "sum up the user sessions for the decision", "the story of the test keeps changing", "what do we still not know after testing", part of the Claude for Product Builders Pack by 90n.
---

# Prototype Learning Card

## When To Use
The test is over and the story of what happened changes each time someone tells it. By the third retelling, "two people got stuck" has become "users loved it". This card answers one question: read against the pass line you set before the build, did the belief hold, and what do we still not know?

## When Not To Use
If you still need to work out what happened task by task, run Usability Test Findings first; the card only sums up a round that has been read. If the question is which option to choose and who chooses, that belongs on Build, Change or Stop Decision. With no dated pass line there is nothing to read against: say so on the card instead of writing one now.

## Inputs
- The test card as written before the build: the belief, the measure, the pass line and its date
- The findings from the sessions: how many ran, on which prototype version, and the counts per task
- The version log, if the prototype changed between rounds
If you have none of this, I start from the belief and your session notes and mark the output as a first draft, with the verdict left "unclear".

## Approach
The Learning Card from Strategyzer (strategyzer.com/library/capture-customer-insights-and-actions-with-the-learning-card), read against the dated test card. Its four statements run in a fixed order: what we believed, what we observed, what we learned, what we will do. The judgment is keeping the second box clean. The moment an opinion lands in "we observed", the card becomes a victory lap and nobody can check it against the sessions.

## Workflow
1. Ask three questions: what the test card said, word for word, with its pass line and date; how many sessions ran, with whom (real target users or not) and on which version; and who will read this card.
2. Fill "We believed" by copying the belief, the measure and the pass line from the test card, with the date. Do not tidy the wording. A belief reworded after the test always turns out to have been right.
3. Fill "We observed" with what happened and nothing else: sessions run, the version each round saw, counts as "[n] of [N]" beside the pass line. Rounds on different versions get separate rows and are never added together. Sessions with colleagues or the leaders who asked are listed apart and do not count.
4. Fill "We learned": the pass line was met, not met or unclear, and what that says about the belief. "Unclear" is a real answer when too few sessions ran or the measure was not captured. Nothing softer than those three words.
5. Add a fifth box: what we still do not know. Scale, real data, people outside the group tested, anything the prototype faked. This is the box readers skip and engineers read first.
6. Fill "We will" with one action and an owner role. The build, change or stop choice itself is not made here; the card feeds the decision page.

## Output Format
```markdown
# Prototype Learning Card
Prototype: [name] | Round(s): [n] | Written by: [role] | Date: [date]
## We believed
[Belief, copied word for word from the test card] | Measure: [behaviour] | Pass line: [threshold], set on [date]
## We observed
| Round | Prototype version | Sessions with real target users | Result on the measure | Pass line |
|---|---|---|---|---|
| [1] | [version label] | [N] | [n] of [N] [behaviour] | [threshold] |
Not counted: [pilot or colleague sessions, and why]
## We learned
Pass line: [met / not met / unclear]. [What that says about the belief, in two sentences.]
## We still do not know
- [What the prototype faked or could not show]
- [Who was not tested]
## We will
[One action] | Owner: [role] | By: [date]
## Decision
[The decision owner, by role] accepts this card as the agreed account of the test, or names what is missing, by [date].
```

## Done When
- The belief and pass line match the test card word for word, with its date
- Every number in "We observed" traces to a session and names the version seen
- The verdict is one of met, not met or unclear
- "We still do not know" has at least one line, and "We will" has an owner role

## Quality Bar
- No adjectives in "We observed": counts and versions only. Quotes go in the findings, not here.
- Counts across the round only. No participant is described, named or compared with another.
- A missing number stays in [brackets]; it is never estimated from memory.
- The card does not recommend build, change or stop.
- Observations come from real sessions and are read against the pass line set before testing; nothing is invented and the bar does not move.

## Next
Run build-decision-memo (Build, Change or Stop Decision) to put the card in front of the person who decides.

## About the makers

This pack is made by 90n ([90n.ai](https://90n.ai)): AI-native ways of working and tools for Product, Marketing and HR teams, built by ex-McKinsey founders. We map where time and money leak, redesign the work around AI and stay until your people run it themselves, and we run our own company on Claude. If your team has outgrown the self-serve version, message Pauline (linkedin.com/in/paulinebertry).
