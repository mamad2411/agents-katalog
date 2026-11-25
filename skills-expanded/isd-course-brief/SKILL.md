---
name: isd-course-brief
description: Drafts a course brief from a training request, with the request restated as a performance problem, a fixed and open table, a "course, job aid or neither" line with reasons, and a reply the requester can sign. Use for "run isd-course-brief", "course brief", "can you just make it a course", "training request intake", "is this really a training problem", "they already chose the format", "push back on a course request", "course or job aid", "questions for the requester", part of the Claude for Instructional Designers Pack by 90n.
---

# Course Brief

## When To Use
"Can you just make it a course?" has arrived, with the format, the audience and the date already chosen. Use this before you accept any of the three. It answers one question: what is actually going wrong on the job, and is a course the thing that fixes it?

## When Not To Use
If the requester has already agreed the problem and a course is the right call, skip to Learner Analysis. If you need the sponsor and an expert in a room to find the actions and the practice, that is Action Mapping Workshop; this brief stops at one gap line and a go or no-go.

## Inputs
- The request as it reached you (email, ticket or call notes, in the requester's own words) and anything the requester already watches that shows the problem: a report, an audit finding, complaints, error logs.
- What you have been told is fixed: date, audience, format, length, budget, mandatory or not.
If you have none of this, I start from one sentence of the request and mark the output as a first draft, with every cause tagged as an assumption.

## Approach
Performance consulting intake, the first stage of the Human Performance Technology model as set out on the University at Buffalo page "Human performance technology (HPT)": performance analysis, then cause analysis, then intervention selection. The judgment is yours: a format is never a problem, and only a skill or knowledge cause points to a course. The failure it prevents: a polished module on a procedure people already know, shipped on time, while the form they need is still three clicks deep and the error rate does not move. In Claude Docs (beta) the brief can be a document the requester signs; a plain conversation works too.

## Workflow
1. Ask at most three questions: what are people doing now that they should do differently, where does the requester see that today, and who signs this brief? Every other question goes on the list for the requester.
2. Split the request in two. What was asked: the format, the length, the date. What is wrong: the gap between what people do and what they should do, in the requester's words. If the request holds only the first half, say so plainly and do not invent the second. Then write the performance analysis line: `[role] currently [do X], should [do Y], seen in [measure the requester already watches]`. A role and a task, never a named person or a team's shortfall. No measure means the line says "no measure named".
3. Run the cause analysis. Sort each likely cause into skill or knowledge, unclear expectation, missing tool or information at the moment of work, process or incentive. Tag each one evidence (and where it came from) or assumption. You judge which assumptions are worth one phone call before anything is built.
4. Write the intervention line: course, job aid, or neither (a process or manager fix), one reason each, and what would change the answer. A course is recommended only where a skill or knowledge cause has evidence behind it. Then fill the fixed and open table (date, audience, format, length, budget, mandatory or not) with who fixed each; the date is recorded as fixed or open only, and no schedule is worked out here.
5. Draft the reply: four or five sentences the requester can sign or correct, restating the gap, the recommendation and the open questions. You read it, change what you disagree with, and send it yourself.

## Output Format
```markdown
# Course Brief
Request from: [role] | Received: [date] | Brief drafted by: [role] | Status: [first draft / agreed]
## The request and the gap
Asked: [format, length, date as requested] | Wrong: [the gap in the requester's words, or "not stated"]
[role] currently [do X], should [do Y], seen in [measure the requester already watches].
## Likely causes
| Cause | Type | Evidence or assumption | Points to |
|---|---|---|---|
| [cause] | [skill or knowledge / unclear expectation / missing tool or information / process or incentive] | [evidence: source] or [assumption] | [course / job aid / manager or process fix] |
## Course, job aid or neither
| Option | Recommended | Reason | What would change the answer |
|---|---|---|---|
| Course | [yes / no / partly] | [one reason] | [finding that would reverse it] |
| Job aid | [yes / no / partly] | [one reason] | [finding] |
| Neither | [yes / no] | [the process or manager fix, and who owns it] | [finding] |
## Fixed and open
| Item | Fixed or open | Value as given | Fixed by |
|---|---|---|---|
| [date / audience / format / length / budget / mandatory, one row each] | [fixed / open] | [as given by the requester] | [role] |
## Questions for the requester
1. [question, and what the answer would change]
## Reply to sign
[Four or five sentences: the gap, the recommendation, what is still open.]
## Decision
[Requester, by role] signs or corrects this brief by [date]; [designer] decides whether a course goes ahead.
```

## Done When
- The gap line names a role, a current behaviour, a wanted behaviour and a measure, or says which of these is missing.
- Every cause carries a type and an evidence or assumption tag.
- All three options have a reason, including the ones not recommended, and the reply can be signed as it stands.

## Quality Bar
- The format the requester chose never appears as the problem, and the audience line is quoted as given; describing the learners is a later job.
- "Mandatory" claims that rest on a regulation are marked for the requester: check with a qualified adviser.
- A "neither" recommendation names who owns the other fix, and no figure appears that the requester did not supply; missing values stay in brackets.
- Claude restates the request; you decide whether a course is the answer, and the requester signs the brief.

## Next
Run isd-learner-analysis (Learner Analysis) to find out who will actually take it.

## About the makers

This pack is made by 90n ([90n.ai](https://90n.ai)): AI-native ways of working and tools for Product, Marketing and HR teams, built by ex-McKinsey founders. We map where time and money leak, redesign the work around AI and stay until your people run it themselves, and we run our own company on Claude. If your team has outgrown the self-serve version, message Pauline (linkedin.com/in/paulinebertry).
