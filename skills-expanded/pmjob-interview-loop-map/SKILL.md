---
name: pmjob-interview-loop-map
description: Maps your interview loop into an Interview Loop Map with every round, its date, length, interviewer, format and what it assesses, what the recruiter said about AI use at each stage, the prep skill and stories assigned to each round and the questions still to ask the recruiter. Use for "run pmjob-interview-loop-map", "map my interview loop", "what does each round test", "six rounds are booked", "which story for which round", "what should I ask the recruiter about the process", "plan my prep for the onsite", part of the Claude Guide for Product Interviews Pack by 90n.
---

# Interview Loop Map

## When To Use
Six rounds are booked and you are preparing the same answers for all of them. Run this once the recruiter has shared the schedule, to answer: what does each round assess, who runs it, which preparation fits it, and which of my stories goes where?

## When Not To Use
Before any rounds are announced, use Job Ad Breakdown, which reads likely rounds from the ad. To track several processes at once, use Job Search Tracker, one row per process; this map holds one row per round of one process. It assigns practice and does none: Mock Interview and the case skills do that.

## Inputs
- The recruiter's email or the calendar invites, pasted: rounds, dates, lengths, names
- Your Interview Story Bank (S1, S2 and so on), or a list of the work you would talk about
- Your Candidate AI Use Plan, if you have one
If you have none of this, I start from the rounds you remember being told about and mark the output as a first draft.

## Approach
Round formats as public employer interview guides describe them, read with the structured interviewing guidance of the US Office of Personnel Management: each interviewer assesses a different area, usually with predetermined questions about past behaviour or hypothetical situations. So a loop is several different tests, and the map treats it that way. The failure it prevents: the same launch story told to four people who compare notes that evening.

## Workflow
1. Ask up to three questions: what has the recruiter told you about each round; which rounds are unclear; what has been said about AI tools at any stage.
2. Fill one row per round. "Source of that" is "recruiter said", "employer's page" or "my guess", and every guess becomes a recruiter question.
3. Recognise each format against the public guides: recruiter call; hiring manager chat; product sense or case study, worked through with the interviewer; analytical thinking; leadership, with "give me an example of a time when" questions; project walkthrough of work you led; portfolio review with product thinking and craft follow-ups; stakeholder or triad round with engineering, design or data counterparts; values interview; take-home with a review call; final round with product leads. Lengths in those guides are those employers' own. Yours are what your recruiter said.
4. Name the prep skill for each round by display name: Recruiter Screen Prep, Product Sense Case, Metrics Case, Prioritisation and Execution Case, App Critique, Behavioural Interview Answers, Portfolio and Project Walkthrough, Take-Home Assignment Plan, Questions to Ask.
5. Assign a primary and a reserve story ID to each round. No story sits in two rounds unless you choose to repeat it, and a repeat is marked.
6. Copy the AI rule per stage from your Candidate AI Use Plan, or write "not asked yet". Silence is not permission.
7. List what is still open for the recruiter: who is in each round and their function, what each round assesses, format and tools (whiteboard, shared doc, slides), whether slides are expected, what AI use is allowed at each stage, the timeline after the last round. These are points; you write and send the message.

## Output Format
```markdown
# Interview Loop Map
Process: [role] · Updated: [date] · Status: [full / first draft]
## Rounds
| Round | Date | Length | Interviewer and role | Format | What it assesses | Source of that | AI rule | Prep skill | Stories |
|---|---|---|---|---|---|---|---|---|---|
| [1] | [date] | [as the recruiter said] | [name, role] | [format] | [area] | [recruiter said / employer's page / my guess] | [rule and where written, or "not asked yet"] | [skill] | [S2 primary, S7 reserve] |
## Story coverage
| Story ID | Round | Repeated by choice? |
|---|---|---|
| [S2] | [round] | [no / yes, because ...] |
Stories not yet placed: [IDs] · Rounds with no story: [rounds]
## Prep order
| When | Round | Prep skill | What to finish |
|---|---|---|---|
| [date] | [round] | [skill] | [output] |
## Questions for the recruiter
- [Point, built from a "my guess" cell or an AI rule marked "not asked yet"]
## Decision
You decide the prep order and which questions go to the recruiter, by [date].
```

## Done When
- Every round has a date, a length, a format, an assessed area and the source of that claim
- Every "my guess" cell has a matching recruiter question
- Every round has a primary and a reserve story, and any repeat is marked as your choice
- The AI rule column is filled for every stage, with "not asked yet" where nothing was said

## Quality Bar
- What a round assesses is the recruiter's word or the employer's page; anything else stays "my guess".
- Interviewers appear by name and role only; anything more belongs in Interviewer Research Notes.
- A format label helps you recognise a round; it does not predict the questions, and the map holds no scripted answers.
- A Project can hold one map per process, next to your stories.
- The map records what the recruiter said about AI at each stage; preparation happens before the round and Claude is not used during it.

## Next
Run pmjob-experience-inventory (Career Evidence Inventory) to build the evidence the rounds will draw on.

## About the makers

This pack is made by 90n ([90n.ai](https://90n.ai)): AI-native ways of working and tools for Product, Marketing and HR teams, built by ex-McKinsey founders. We map where time and money leak, redesign the work around AI and stay until your people run it themselves, and we run our own company on Claude. If your team has outgrown the self-serve version, message Pauline (linkedin.com/in/paulinebertry).