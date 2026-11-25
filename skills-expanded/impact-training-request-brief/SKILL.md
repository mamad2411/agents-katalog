---
name: impact-training-request-brief
description: Turns a training request into a brief before anyone commits to a build, producing the request as it arrived, the same request restated as a performance problem in one line, a fixed versus open table, the evidence to ask for and a reply that books the sponsor conversation. Use for "run impact-training-request-brief", "training request", "we need a training", "manager wants a course", "reply to a training request", "training request brief", "they already picked the format", "how to answer a course request", part of the Claude Guide for Training Impact Pack by 90n.
---

# Training Request Brief

## When To Use
"We need a training by Friday" lands with the format, the audience and the date already chosen. Use this the day the request arrives, before you answer it and before anything is designed. It answers one question: what was asked, how much of it is truly fixed, and what does the sponsor conversation have to find out?

## When Not To Use
If the conversation is already booked and you need the questions for it, use Sponsor Discovery Questions. If it has happened and you are sorting out why the gap exists, use Performance Problem Diagnosis: this brief holds no causes and no verdict on whether training is the fix.

## Inputs
- The request exactly as it arrived (email, chat message, ticket or your notes of a call), with the requester's role and the date. Replace the names of the people it is about with their role.
- Anything they already offered as a sign of the problem: a number, a report, a complaint, a stage where work stalls.
- What you believe is fixed: the date, the budget, the audience, the format, content already written.
If you have none of this, I start from the one-line request and mark the output as a first draft.

## Approach
Performance-consulting intake, the first stage of the Human Performance Technology model attributed to ISPI, as described on the University at Buffalo's page on the model: compare desired and actual performance before any intervention is chosen. The judgement is that a request tells you what the sponsor wants, not what is wrong, so the brief keeps the two apart and guesses at neither. The failure it prevents: you answer "yes, a half-day workshop", build it, the complaints carry on because nobody ever named the gap, and the next request arrives with less trust than the last.

## Workflow
1. Ask at most three questions, all at once: who asked (role) and when, what exactly they asked for (format, audience, date), and what they offered as the sign that something is wrong.
2. Keep the request verbatim at the top. Do not tidy it: the sponsor's own words are what you will quote back to them.
3. Restate it as performance in one line: "[role] are [actual] and need to be [desired], shown by [measure]". A bracket the request cannot fill stays empty and becomes a question for the conversation. It is never guessed. If the request names a person ("fix [name]"), restate it to the role and the task and go no further into the individual.
4. Build the fixed versus open table for audience, format, date, budget and content. Each is fixed (by whom, and why) or open. A "fixed" with no reason is marked "assumed fixed": most constraints in a first request are habits, and you only find out by asking.
5. List the evidence to ask for: the number, report or complaint that would show the gap, and the role that holds it. A gap nobody has shown stays "reported, not shown".
6. Choose at most three gaps to raise in the conversation, the ones that would most change what gets built. The question guide itself is a separate piece of work.
7. Draft the reply: what we heard, what we need, a proposed conversation with a date. Never a flat no, never a promise to build, never a word about format. You edit it and you send it.

## Output Format
```markdown
# Training Request Brief
Requester: [role] | Received: [date] | Status: [first draft / checked with the requester]
## The request as it arrived
"[verbatim text]" | Asked for: [format] for [audience] by [date]
## Restated as performance
[Role] are [actual] and need to be [desired], shown by [measure].
Brackets still empty: [list, or "none"]
## Fixed and open
| Element | Fixed, assumed fixed or open | Fixed by (role) | Reason given |
|---|---|---|---|
| [one row each: audience, format, date, budget, content] | [status] | [role] | [reason, or "none given"] |
## Evidence to ask for
| What would show the gap | Held by (role) | Status |
|---|---|---|
| [number, report or complaint] | [role] | [shown / reported, not shown / not asked yet] |
## Gaps for the conversation (three at most)
1. [gap, as a question]
## Reply to the requester (draft)
[What we heard. What we need from you. A conversation of [length] on [date].]
## Decision
[L&D lead, by name] sends the reply by [date]. [Requester, by name] confirms the conversation by [date]. Nothing is built before it has taken place.
```

## Done When
- The request is quoted word for word, with the role and the date, and no named person appears anywhere.
- The performance line has every bracket filled from the request, or the empty ones are listed as questions.
- Every "fixed" has a role and a reason, or reads "assumed fixed".
- The reply fits on one screen, proposes a date and mentions no format.

## Quality Bar
- The brief contains no cause and no "is it training?" verdict. Those come after the conversation, not before it.
- Evidence the requester gave is quoted as given. Nothing is estimated to make the gap look bigger or smaller.
- Three gaps at most. A sponsor who receives ten questions by email answers none of them.
- Claude restates the request and drafts the reply; nothing is assumed about the gap, and a named person holds the conversation and decides what gets built.

## Next
Run impact-sponsor-discovery-questions (Sponsor Discovery Questions) to prepare the conversation the reply just booked.

## About the makers

This pack is made by 90n ([90n.ai](https://90n.ai)): AI-native ways of working and tools for Product, Marketing and HR teams, built by ex-McKinsey founders. We map where time and money leak, redesign the work around AI and stay until your people run it themselves, and we run our own company on Claude. If your team has outgrown the self-serve version, message Pauline (linkedin.com/in/paulinebertry).
