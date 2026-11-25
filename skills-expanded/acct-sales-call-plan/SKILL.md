---
name: acct-sales-call-plan
description: Prepares a sales call plan with the meeting objective from the customer's side, the advance you want and a fallback advance, what you know against what you assume, a three-part run of show and the people in the room by role. Use for "run acct-sales-call-plan", "sales call plan", "call prep", "pre-call plan", "meeting prep for a customer", "prepare my customer meeting", "what is my goal for this meeting", "my meetings end with let's touch base", part of the Claude for Account Executives Pack by 90n.
---

# Sales Call Plan

## When To Use
Your meetings keep ending with "let's touch base next month". Run this before any customer meeting, in person, on video or by phone. It answers one question: at the end of this meeting, what will the customer have agreed to do themselves, and by when?

## When Not To Use
To write the discovery questions themselves, run Discovery Call Questions. If you know nothing about the account yet, start with Account Research Brief. A relationship visit with no deal in play needs an agenda, not an advance.

## Inputs
- The context: who asked for the meeting and why, the format and the planned length.
- What you know about the account: your research brief, notes, last exchanges, the stage in your CRM.
- The people attending on both sides, by name and job role.
If you have none of this, I start from the account name and the reason for the meeting, and mark the output as a first draft. In Projects (beta) the plan sits beside the account's earlier notes.

## Approach
Huthwaite International's research on sales calls separates a call that moves the sale forward, where the customer commits to something that gives you access to something new, from one where every action stays on your side and you become, in their words, a free consultant (huthwaiteinternational.com). I build the meeting around that customer commitment, the advance, with a smaller fallback. The failure it prevents: the pleasant meeting that changes nothing in the deal.

## Workflow
1. I ask at most three questions: what stage is the deal at, what would make this meeting a success for you, and what would make it one for the customer.
2. I write the objective in one sentence from the customer's side: what they will have understood or decided when they leave, not what you will have presented.
3. I word the advance as "[who on their side] does [what] by [date]": bringing in another decision maker, preparing their figures, opening a validation step. "They will think about it" and "we will talk again" leave every action with you, so I refuse them as objectives.
4. I word a fallback advance, smaller but still an action by the customer, for the case where the first is not ripe.
5. I split two columns: what you know, with its source, and what you assume. Each assumption becomes a question to ask in the meeting.
6. I build the run of show in three parts: opening and an objective shared with the customer, discovery, proposing the next step. For a short call, discovery is two questions.
7. I list the people in the room by job role on both sides, who says what on yours, and the documents to bring or share on screen.

## Output Format
```markdown
# Sales Call Plan
[Account] · [date] · [in person / video / phone] · [length]
## Objective
[What the customer will have understood or decided when they leave]
## Advances
| Advance | Who on their side | Does what | By when |
|---|---|---|---|
| Target | [role] | [action] | [date] |
| Fallback | [role] | [action] | [date] |
## Known and assumed
| I know (source, date) | I assume (question to verify) |
|---|---|
| [fact] ([source]) | [assumption] ([question]) |
## Run of show
1. Opening and shared objective: [cues]
2. Discovery: [key questions]
3. Proposing the next step: [target advance]
## People and documents
[Roles on both sides] · [documents to bring]
## Decision
[You] confirm the target advance and the fallback before the meeting, by [date].
```

## Done When
- The target and the fallback are each an action by the customer, with a role and a date.
- Every fact has its source and every assumption has its question.
- The run of show fits the planned length.

## Quality Bar
- "We will talk again" is never an objective, however it is dressed.
- People appear by name, job role and role in the decision, never by character or "type".
- Cues, not a text to recite: you say it in your own words.
- No fact about the customer is added to your sources.
- What you know is sourced and what you assume is marked; you run the meeting as yourself.

## Next
Run acct-discovery-questions (Discovery Call Questions) to prepare the questions for this meeting.

## About the makers

This pack is made by 90n ([90n.ai](https://90n.ai)): AI-native ways of working and tools for Product, Marketing and HR teams, built by ex-McKinsey founders. We map where time and money leak, redesign the work around AI and stay until your people run it themselves, and we run our own company on Claude. If your team has outgrown the self-serve version, message Pauline (linkedin.com/in/paulinebertry).
