---
name: impact-sponsor-discovery-questions
description: Prepares the question guide for the conversation you hold with a sponsor about a training request, producing six question blocks with evidence probes, lines for when the sponsor insists on the course, a blank notes template and a follow-up message. Use for "run impact-sponsor-discovery-questions", "questions to ask a sponsor", "is this a training problem", "stakeholder discovery questions", "sponsor insists on a course", "push back on a training request", "performance consulting questions", "what would success look like", part of the Claude Guide for Training Impact Pack by 90n.
---

# Sponsor Discovery Questions

## When To Use
You must ask a senior sponsor "is this a training problem?" without sounding like you are refusing. Use this once the conversation is booked and you have little time to prepare. It answers: what do I ask, in what order, and what do I say when the answer is "just build the course"?

## When Not To Use
If no conversation is booked yet, start with Training Request Brief, which drafts the reply that books it. For conversations with learners after the programme, use Learner Interview Guide: it carries consent rules this guide does not have. To turn the sponsor's idea of success into measures they sign, use Success Measures Agreement; this guide only asks the question.

## Inputs
- The request or your brief of it, with the sponsor's own wording.
- How many minutes you have, the roles in the room, what the sponsor has already fixed and the gaps you most need closed.
If you have none of this, I start from the one-line request and an assumed short meeting, and mark the output as a first draft.

## Approach
Performance consulting questions, ordered so the sponsor describes the work before anyone debates a course. The last block follows return on expectations as set out by Kirkpatrick Partners: agree with business stakeholders what the programme should accomplish before designing it. The judgement is that curiosity about the sponsor's problem is heard as help, and doubt about the sponsor's answer is heard as refusal. The failure it prevents: in the second minute you ask "are we sure training is the answer?", the sponsor repeats the deadline, and you leave with the same order and less goodwill.

## Workflow
1. Ask at most three questions, all at once: how many minutes you have and with which roles, what the sponsor has already fixed, and which gaps you most need closed.
2. Lay out six blocks in this order: why now; what people do today; what they should do instead; how anyone would see the difference (which number, report or complaint); what else has changed; what success would look like. Today comes before "should", and evidence before success, so that success ends up stated in a measure the sponsor already reads.
3. For each block write one opening question in the sponsor's language, reusing words from the request; one probe that asks for evidence ("what would I see if I stood next to them?"); and what to listen for, such as a figure, a named report, or "they just need to".
4. Size the guide to the minutes. Mark which blocks to drop first. "How anyone would see the difference" and "what success would look like" are dropped last: without them nothing can be proved later.
5. Write the lines for when the sponsor insists. Accept what is fixed (the date, the audience), then ask for one thing: one measure, one team to talk to, or a small first run. Never argue the format in the meeting. Offer two or three wordings per ask and let the user pick the ones that sound like them.
6. Add the notes template with three columns: what was said, the evidence offered, still unknown. It stays blank. If the user wants to rehearse, the rehearsal is marked as rehearsal and none of it enters the notes.
7. Draft the follow-up message with brackets where the conversation will supply the content: what I heard, what is still open, the next step and a date. The person fills it in afterwards and sends it.

## Output Format
```markdown
# Sponsor Discovery Guide
Conversation: [date] | Time: [minutes] | With: [sponsor role] | Already fixed: [date, audience, other]
## Question blocks
| Block | Opening question | Evidence probe | Listen for | Drop order |
|---|---|---|---|---|
| 1. Why now | [question in the sponsor's words] | [probe] | [signal] | [keep / drop first / drop second] |
| 2. What people do today | [question] | [probe] | [signal] | [drop order] |
| 3. What they should do instead | [question] | [probe] | [signal] | [drop order] |
| 4. How anyone would see the difference | [question] | [probe] | [signal] | keep |
| 5. What else has changed | [question] | [probe] | [signal] | [drop order] |
| 6. What success would look like | [question] | [probe] | [signal] | keep |
## If the sponsor insists on the course
| Accept as fixed | Ask for one thing | Line to say |
|---|---|---|
| [date, audience] | [one measure / one team to talk to / a small first run] | [wording you chose] |
## Notes (filled in by you, during or straight after)
| Block | What was said | Evidence offered | Still unknown |
|---|---|---|---|
| [block] | | | |
## Follow-up message (draft, you send it)
[What I heard. What is still open. The next step, and [date].]
## Decision
[L&D lead, by name] holds the conversation on [date] and sends the follow-up by [date]. [Sponsor, by name] confirms what is open and agrees the next step by [date].
```

## Done When
- All six blocks are present in order, each with an opening question, an evidence probe and what to listen for.
- The guide fits the minutes given, the drop order is marked, and each ask has a line the user would say aloud.
- The notes template is blank, and the follow-up message has brackets, not content.

## Quality Bar
- Questions are open and about the work. None contains its own answer, and none mentions a format, a duration or a platform.
- Questions concern the role and the task. If the sponsor names a team member, the next question goes back to what the role has to do.
- Probes ask for something that could be looked at afterwards: a report, a count, a complaint, a place to stand.
- Claude prepares the questions; a person holds the conversation, and nothing the sponsor did not say goes into the notes.

## Next
Run impact-performance-problem-diagnosis (Performance Problem Diagnosis) to turn the notes into causes with evidence.

## About the makers

This pack is made by 90n ([90n.ai](https://90n.ai)): AI-native ways of working and tools for Product, Marketing and HR teams, built by ex-McKinsey founders. We map where time and money leak, redesign the work around AI and stay until your people run it themselves, and we run our own company on Claude. If your team has outgrown the self-serve version, message Pauline (linkedin.com/in/paulinebertry).
