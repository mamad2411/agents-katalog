---
name: firm-win-loss-review
description: Reviews one engagement won or lost, covering what was supposed to happen, what happened, why (process, what could not be known then, the client's own change, chance), where it was really decided, the client's feedback in their words with permission, a sound call with a bad outcome kept, and each change as a concrete edit with an owner and a date, blameless. Use for "run firm-win-loss-review", "I lost the pitch", "why did I win this one", "review a lost proposal", "after action review of this pursuit", "what should I change next time", "post-mortem on this opportunity", part of the Claude for Consultants · Team in Claude Pack by 90n.
---

# Win/Loss Review

## When To Use
"They went in another direction." You close the email, feel bad for an afternoon and change nothing. Or you win, and credit a proposal that the client barely read. Working alone, no one will make you look back. Run this within a week or two of the outcome, on one pursuit, to find where it was really decided and what you will do differently.

## When Not To Use
While the opportunity is still open, review nothing; use Client Decision Brief or Proposal Follow-Up Emails. To check a delivery estimate against past projects, use Outside View Check.

## Inputs
- Your plan as it stood: fit note, proposal, dates, what you expected at each stage
- What happened stage by stage, and the client's decision
- Feedback from the client, if any, and whether they agreed that it may be used
If you have none of this, I start from your recollection, label it as recollection and list the records worth finding. A Project keeps your reviews in one place.

## Approach
The After Action Review comes from the US Army (Training Circular 25-20): what was supposed to happen, what happened, why the difference, what to sustain and what to improve. A no-hindsight check is added: judge each call by what could be known when it was made, and keep apart process, missing information, the client's own change and chance. One outcome proves little. The failure it prevents is rewriting a sound decision as a mistake because it lost, or a weak one as skill because it won.

## Workflow
1. Ask, in one go: what was the outcome, and when did you hear? What did you expect at each stage? Did the client give feedback, and did they agree to it being used here?
2. What was supposed to happen: the plan as it stood then, taken from records and not from memory. Anything from memory is labelled recollection.
3. What happened: a timeline by stage (intake, discovery, thinking, proposal, presentation, follow-up, decision) with dates and facts. Client feedback appears only in their words and with their agreement; otherwise "no feedback given".
4. Why the difference: sort each gap into one of four causes. Process (how you qualified, asked, wrote, presented). Not knowable then. The client's own change. Chance. Then mark the stage where it was really decided, which is often discovery, weeks before any document.
5. Apply the no-hindsight check to your main calls. For each, was it sound given what you knew? A sound call with a bad outcome is kept. A weak call that happened to work is listed for change.
6. Sustain and improve: write each change as a concrete edit, such as a new go or no-go criterion, a question added to your discovery page or a line in your proposal template, with a date. Then read once for blame and rewrite any sentence about someone's character, yours included, as a point about process.

## Output Format
```markdown
# Engagement Review
Pursuit: [client role and work] · Outcome: [won / lost / no decision] · Reviewed: [date]
## Plan against what happened
Supposed to happen (the plan then, from records): [plan]
| Stage | Date | What happened | Record or recollection |
|---|---|---|---|
| [intake / discovery / thinking / proposal / presentation / follow-up / decision] | [date] | [fact] | [source] |
## Why the difference
| Gap | Cause (process / not knowable then / client's change / chance) | Evidence |
|---|---|---|
| [gap] | [cause] | [source] |
Really decided at: [stage and moment]
## Calls I made, judged on what I knew then
| Call | Sound at the time? | Keep or change |
|---|---|---|
| [call] | [yes / no, and why] | [keep / change] |
Client feedback: [their words, used with their agreement] or [no feedback given]
## Sustain and improve
| Change | Where it goes | By |
|---|---|---|
| [edit] | [criteria / question page / template] | [date] |
## Decision
[You] adopt or reject each change by [date], and apply the adopted ones to the next brief that arrives.
```

## Done When
- The four questions are answered in order
- On the timeline, records and recollection are kept visibly apart
- Every change is a concrete edit with a place and a date

## Quality Bar
- A sound call with a bad outcome is kept, not recast as an error
- Client feedback is quoted only as given; it is never paraphrased into quotation marks or made up to explain a loss
- No win rate or benchmark unless it is your own, and no sentence that blames a person, you included
- Their words only and with permission, about the pursuit and never about people; I invent no reason for the outcome, and you decide what changes.

## Next
Run firm-ai-brief-review (AI-Written Brief Review) to start the next engagement by reading its brief with what you learned.

## About the makers

This pack is made by 90n ([90n.ai](https://90n.ai)): AI-native ways of working and tools for Product, Marketing and HR teams, built by ex-McKinsey founders. We map where time and money leak, redesign the work around AI and stay until your people run it themselves, and we run our own company on Claude. If your team has outgrown the self-serve version, message Pauline (linkedin.com/in/paulinebertry).
