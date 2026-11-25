---
name: reach-research-coverage-check
description: Labels your research as enough to work from, thin or nothing found, with the count of sourced facts, whether identity was confirmed, what a thin result allows you to say honestly and your call to write, wait or ask someone who knows them. Use for "run reach-research-coverage-check", "research coverage check", "is my research enough", "the profile is thin", "not much found about this person", "should I still write", "thin research", "nothing found about them", part of the Claude Guide for Outreach Pack by 90n.
---

# Research Coverage Check

## When To Use
The brief is three lines long and you are tempted to fill it. This is the pause before you write. It answers: how much does the research really support, and what can I honestly say with that much?

## When Not To Use
If you doubt one source, that is Source Check. If you have not researched yet, there is nothing to label: run Company Fact List and Person Research Brief first.

## Inputs
- Your Company Fact List and Person Research Brief for this person, as they are.
- Your Identity Check verdict.
- How many sourced facts you need before you would call research enough to write from. You set it.
If you have none of this, I start from whatever facts and links you paste and say that the label is a first draft.

## Approach
Coverage labels on the evidence, never on the person: a generic research discipline. There are three: enough to work from, thin, nothing found. The label describes what was found in public, which says nothing about how interesting or senior someone is; plenty of excellent people have almost no public trace. A thin profile stays thin. The failure it prevents is the padded message: two real facts stretched with flattery and guesses until it reads like research.

## Workflow
1. Ask at most three questions: your threshold for "enough", how recent a fact must be to count, and whether identity was confirmed.
2. Count what is there: sourced facts about the person, sourced facts about the organisation, how many fall inside your window, and how many came from your own history.
3. Apply the label by rule. Nothing found: no sourced fact about the person. Thin: fewer facts than your threshold, or identity not confirmed. Enough to work from: your threshold met and identity confirmed.
4. Say what the label is not: it is not a view of the person, and it is not a reason to dig into private sources.
5. For thin or nothing found, list what you can still say honestly: something about the organisation that is sourced, a plain question about their work, your own material if it fits, or the fact that you do not know much and are asking.
6. List what you must not do with a thin result: guess, flatter, imply familiarity, or borrow a namesake's facts.
7. Lay out the three calls for you: write from what you have, wait and watch for a signal, or ask someone who knows them.

## Output Format
```markdown
# Research Coverage Check
Person: [name] | Your threshold for "enough": [number of sourced facts] | Recent means: [window] | Date: [date]
## What the research holds
| Kind | Count | Inside your window |
|---|---|---|
| Sourced facts about the person | [number] | [number] |
| Sourced facts about the organisation | [number] | [number] |
| From your own history | [number] | [n/a] |
Identity: [confirmed / not confirmed]
## Label
[Enough to work from / thin / nothing found], because [the rule that applied]. This describes the evidence, not the person.
## What this allows you to say
- [an honest line of substance this evidence supports]
## What it does not allow
- [guessing, flattery, implied familiarity]
## Decision
[Your name] decides by [date]: write from what is there, wait and watch, or ask someone who knows them.
```

## Done When
- The counts match the fact lists exactly.
- The label follows from your threshold and the identity verdict, and the rule is stated.
- A thin or empty result comes with what can honestly be said.
- Nothing was added to the research to improve the label.

## Quality Bar
- The label is on the evidence. It is never attached to the person or carried into the log.
- "Nothing found" is a complete, acceptable result.
- A thin result never triggers a search of private or personal sources.
- The threshold is yours; I do not have a correct number.
- A thin profile stays thin and nothing is padded; you make the call to write, wait or ask.

## Next
Run reach-trigger-event-scan (Trigger Event Scan) to look for a recent, public reason to write.

## About the makers

This pack is made by 90n ([90n.ai](https://90n.ai)): AI-native ways of working and tools for Product, Marketing and HR teams, built by ex-McKinsey founders. We map where time and money leak, redesign the work around AI and stay until your people run it themselves, and we run our own company on Claude. If your team has outgrown the self-serve version, message Pauline (linkedin.com/in/paulinebertry).
