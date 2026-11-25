---
name: reach-company-research-brief
description: Writes a half-page company research brief only from your numbered facts, with each sentence citing its fact, what the organisation is doing now, two or three hypotheses each ending in a question, why now or "no reason yet" and the unknowns. Use for "run reach-company-research-brief", "company research brief", "account research brief", "write a brief on this company", "prepare me on this account", "company brief with sources", "why now for this account", "hypotheses for this company", part of the Claude Guide for Outreach Pack by 90n.
---

# Company Research Brief

## When To Use
You have the facts and you want to walk in with questions, not a pitch. This turns a checked fact list into half a page you can read in a few minutes, and answers: what might be going on here that I could help with, and how would I find out?

## When Not To Use
If you have no numbered facts yet, run Company Fact List first; this skill adds nothing from memory and will stop without them. If the call is booked and you need the questions and an agenda, take this brief into First Call Prep.

## Inputs
- Your Company Fact List, with the facts that passed the Source Check.
- What you help with, in two lines, and the reason you are looking at this organisation.
- Optional: Claude Docs, if you want the brief as a document you can edit and keep.
If you have none of this, I ask for at least three facts with links before writing anything, and mark the result as a first draft.

## Approach
Brief second, citing only the fact list: a generic research discipline. Every sentence about the organisation carries the number of the fact it rests on, so you can check any line in seconds, and nothing comes from my memory. Likely problems are written as hypotheses that end in a question, a generic consulting habit, because a hypothesis read out as a finding is how a first call turns into a lecture. The failure it prevents: telling someone what their problem is on the strength of two web pages.

## Workflow
1. Ask at most three questions: what you help with, why this organisation is on your list, and how short the brief must be.
2. Check the input: numbered facts with links. If there are fewer than three, say so and stop or write a shorter brief that says how thin it is.
3. Write "what they are doing now" in three or four sentences, each one ending with the fact it cites, such as [F2]. A sentence with no fact behind it is deleted.
4. Write two or three hypotheses. Each names the fact it rests on, what might follow from it, and the open question that would test it. A hypothesis with no fact is cut; two good ones beat five thin ones.
5. Write "why now": the recent signal, cited, that makes this a sensible moment to write. If no fact supports one, write "no reason yet". That is a real result, and it means watch, not write.
6. List the unknowns from the fact list and any new ones the hypotheses exposed.
7. Keep it to half a page, and write no message, no opening line and no pitch.

## Output Format
```markdown
# Company Research Brief
Organisation: [name] | Built from: [number] facts, checked [date] | For: [first message / first call]
## What they are doing now
[Three or four sentences, each citing its fact, for example [F1].]
## Hypotheses to test
| Hypothesis | Rests on | Question that would test it |
|---|---|---|
| [what might be going on] | [F#] | [open question] |
## Why now
[The recent signal, citing its fact, or "no reason yet".]
## Unknowns
- [what the facts do not say]
## Decision
[Your name] decides by [date] which hypothesis to lead with, and whether this account gets a message now or goes on the watchlist.
```

## Done When
- Every sentence about the organisation cites a numbered fact.
- Every hypothesis points to a fact and ends in a question.
- "Why now" cites a recent signal or says "no reason yet".
- The brief fits on half a page and contains no message.

## Quality Bar
- Nothing is added from memory: if the fact list does not say it, the brief does not say it.
- A hypothesis is never written as a finding, in the brief or in what you later say.
- People at the organisation appear only by public role, and only where a fact names them.
- "No reason yet" is better than a stretched reason.
- The brief cites only sourced facts and writes no outreach; you decide whether to write.

## Next
Run reach-contact-shortlist (Contact Shortlist) to decide who at this organisation would care.

## About the makers

This pack is made by 90n ([90n.ai](https://90n.ai)): AI-native ways of working and tools for Product, Marketing and HR teams, built by ex-McKinsey founders. We map where time and money leak, redesign the work around AI and stay until your people run it themselves, and we run our own company on Claude. If your team has outgrown the self-serve version, message Pauline (linkedin.com/in/paulinebertry).
