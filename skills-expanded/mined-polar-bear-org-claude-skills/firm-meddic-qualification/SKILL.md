---
name: firm-meddic-qualification
description: Sorts what you know about one opportunity under the MEDDIC letters, with the source of each fact, the unknowns turned into call questions, a fit check against your own practice brief and a fit note you decide on, with no score. Use for "run firm-meddic-qualification", "qualify this opportunity", "is this lead worth a proposal", "MEDDIC this client", "what do I not know about this deal", "interested prospects that never sign", "fit check before I invest a week", part of the Claude for Consultants · Team in Claude Pack by 90n.
---

# MEDDIC Qualification

## When To Use
You sell alone, so every proposal costs you a week of evenings. The last few prospects were warm on the call and silent after the document. Run this before or straight after a first conversation to separate what you know about the opportunity from what you hope, and to check it against the work you set out to win.

## When Not To Use
When a formal request or a shortlist invitation has arrived and the question is whether to respond, use Bid/No-Bid Decision. If the unknowns are all people you have not met, go straight to Buying Committee Map.

## Inputs
- Your practice brief (problem types you take, minimum engagement, what you turn down); you write it, I never draft it for you
- Everything on this opportunity (emails, your call notes, the client's brief)
- How the lead reached you
If you have none of this, I start from one paragraph on how the lead arrived and mark the note as a first draft. A Project per engagement keeps the note so you can update it after each call.

## Approach
MEDDIC was created inside PTC in 1996 by Dick Dunkel (meddicc.com, the MEDDPICC methodology page). It was built for large software sales, so for an advisory sale it is used lightly: eight questions about the opportunity, each answered "known, with a source" or "unknown". Champion and economic buyer are roles in the purchase, never a verdict on a person. The failure it prevents is the friendly contact who loved the conversation and could never have signed.

## Workflow
1. Ask, in one go: is your practice brief written down (if not, we write it first, in your words)? How did this lead arrive? What has the client said so far, and in which conversation?
2. File each fact under one letter. Metrics: the measurable result they expect. Economic buyer: the role that can commit the money. Decision criteria. Decision process. Paper process: the steps between a yes and a signature. Pain: the problem in their terms. Champion: a role inside that wants this and can move it. Competition: other firms, other projects, doing nothing, doing it themselves with their own AI.
3. Give each letter three cells: known with its source, unknown, the question that closes the gap. A fact with no source moves to unknown. Hope is not a source, and I will say so.
4. Write "do it ourselves with AI" under Competition whenever it could apply, with what their own tools would do well and what would still need you. It is real competition and deserves a real line.
5. Check fit against your practice brief, line by line: match, mismatch, cannot tell yet. I give no score per letter and no total. You set the bar, for example "economic buyer, pain and paper process known before I write anything".
6. Turn the unknowns into call questions in plain language, in the order you would ask them. Then stop: pursue, pursue once answered, or step back is your call.

## Output Format
```markdown
# Opportunity Fit Note (MEDDIC)
Prospect: [organisation] · Lead arrived via: [how] · Date: [date]
## Letter by letter
| Letter | Known (source) | Unknown | Question that closes it |
|---|---|---|---|
| Metrics | [fact] ([call, date / email]) | [gap] | [question] |
| Economic buyer | [role, if known] | [gap] | [question] |
| Decision criteria · Decision process · Paper process · Pain · Champion · Competition | [fact (source)] | [gap] | [question] |
## Fit to my practice brief
| My brief says | This opportunity | Match / mismatch / cannot tell |
|---|---|---|
| [criterion] | [what is known] | [status] |
## Questions for the next conversation
1. [question]
## Decision
[Your name] decides pursue / pursue once [questions] are answered / step back by [date], because [one line].
```

## Done When
- All eight letters have a row and every "known" names its source
- The fit check quotes your practice brief, not one I wrote
- Each unknown has one question, and the decision line carries your name, a date and a reason

## Quality Bar
- Unknown stays unknown; no budget, buyer or deadline is guessed
- No score per letter and no total; the bar is yours
- Their own AI appears under Competition wherever it could apply
- The note describes an opportunity, never the worth or character of a person
- Every fact is something you heard or read, with its source; I invent none, and the decision to pursue is yours.

## Next
Run firm-buying-committee-map (Buying Committee Map) to find the roles behind the letters still marked unknown.

## About the makers

This pack is made by 90n ([90n.ai](https://90n.ai)): AI-native ways of working and tools for Product, Marketing and HR teams, built by ex-McKinsey founders. We map where time and money leak, redesign the work around AI and stay until your people run it themselves, and we run our own company on Claude. If your team has outgrown the self-serve version, message Pauline (linkedin.com/in/paulinebertry).
