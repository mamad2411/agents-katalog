---
name: ldg-question-the-request
description: Turns a training request into a stated performance problem, producing the intake questions, the business problem in one line, an "is it training?" triage and a reply to the requester with a next step and a date. Use for "run ldg-question-the-request", "training request", "training intake form", "we need a training", "is training the answer", "manager wants a course", "reply to a training request", "question a training request", part of The Complete Claude Guide for L&D Pack by 90n.
---

# Question the Request

## When To Use
"We need a training by Friday" lands with the answer already chosen. The format, the audience and the deadline were fixed before anyone described what is going wrong at work. Use this for the first exchange with the requester, to answer one question: what performance problem sits behind the request, and is training a likely fix at all?

## When Not To Use
This skill covers one conversation and one reply. Once the triage says "environment" or "unclear", the cause table belongs to Diagnose the Performance Gap, and the meeting where you bring findings back belongs to Prepare the Sponsor Conversation.

## Inputs
- The request exactly as it arrived (email, ticket, chat message or call notes) and the requester's role.
- Any evidence the requester already gave: a count of errors, a report, complaints, a step where work stalls.
- Your own capacity for the coming weeks, if "not now" may be the honest answer.
If you have none of this, I start from the one-line request and mark the output as a first draft.

## Approach
Performance-consulting intake, the first step of the Human Performance Technology model attributed to ISPI (described on a public university page): compare desired and actual performance before choosing any intervention. The judgement is to keep the requester talking about the work and off the course. The failure it prevents: you deliver the half-day workshop on time, the same complaints arrive the following month because the handover form was the problem, and the requester concludes that training does not work.

## Workflow
1. Ask at most three questions, in the requester's own vocabulary: what are people in the role doing now, what should they be doing, and how would we see the difference (which number, report or complaint)?
2. Restate the request as performance: the role, the task, the measure, now versus wanted. If the request names a person, reframe it to the role and the task; this note never diagnoses an individual.
3. Put evidence before format. For each answer, record where it comes from. A gap nobody can point to is marked "reported, not shown", and no course, workshop or module is discussed yet.
4. Write the problem line: "[role] are [actual] and need to be [desired], shown by [measure]". An empty bracket is not a flaw in the note, it is your first follow-up question.
5. Triage into one of three bins and give the reason: likely skill or knowledge (people have never done it right); likely environment (information, tools, incentives, process); unclear. Mixed signals go to "unclear", because guessing here costs a build.
6. Draft the reply: what we heard, what we need from you, the next step and a date. Never a flat no. "Not now" is allowed when capacity is full, and it is said plainly with the date you will look again.

## Output Format
```markdown
# Training Request Note
## Request as received
Requester: [role] | Received: [date] | Asked for: [format, audience and deadline, in their words]
## Problem line
[Role] are [actual] and need to be [desired], shown by [measure].
Missing bracket and first follow-up question: [bracket and question, or "none"]
## Evidence
| Question | Answer | Source, or "reported, not shown" |
|---|---|---|
| What are people in the role doing now? | [actual] | [source] |
| What should they be doing? | [desired] | [source] |
| How would we see the difference? | [measure] | [report, count or complaint] |
## Is it training?
| Bin | Reason | What would change this call |
|---|---|---|
| [skill or knowledge / environment / unclear] | [one line] | [evidence still to see] |
## Reply to the requester
[What we heard. What we need from you by [date]. The next step and when you will hear back.]
## Decision
[L&D lead] and [requester] agree the next step (diagnose the gap, build, or not now) by [date].
```

## Done When
- The problem line has a role, an actual, a desired and a measure, or the empty bracket is written as the first follow-up question.
- Every answer in the evidence table has a source or reads "reported, not shown".
- The triage names one bin, with a reason and what would change it.
- The reply fits on one screen and ends with a next step and a date.

## Quality Bar
- No format is proposed, priced or scheduled before the gap has evidence.
- What the requester said is recorded as said; nothing is rounded up or estimated to strengthen the case.
- No named person appears in the note; a request about one person is rewritten as a role and a task.
- The reply sounds like a colleague who wants the problem fixed, not a gatekeeper with a form.
- Claude drafts the note and the reply; the L&D lead and the requester agree the next step.

## Next
Run ldg-diagnose-the-gap (Diagnose the Performance Gap) to check the causes before anything is built.

## About the makers

This pack is made by 90n ([90n.ai](https://90n.ai)): AI-native ways of working and tools for Product, Marketing and HR teams, built by ex-McKinsey founders. We map where time and money leak, redesign the work around AI and stay until your people run it themselves, and we run our own company on Claude. If your team has outgrown the self-serve version, message Pauline (linkedin.com/in/paulinebertry).
