---
name: ldg-run-the-learner-walkthrough
description: Prepares a learner walkthrough of a draft course, with a plan for a handful of volunteers from the role, the tasks and think-aloud prompts, an observation sheet about the draft, an issue list ranked by severity, the fix list and the release call. Use for "run ldg-run-the-learner-walkthrough", "course pilot test", "usability testing", "test the course with learners", "learner run-through", "think aloud test", "user test my e-learning", "where do learners get lost", part of The Complete Claude Guide for L&D Pack by 90n.
---

# Run the Learner Walkthrough

## When To Use
The course looked right in review and the first real learner got lost on screen three. Reviewers know the subject, so they read past the gaps a newcomer falls into. Use this on a draft, before release, to watch a few people from the role work through it and see where the draft loses them.

## When Not To Use
For a desk check of facts, alignment and accessibility against sources, use Check the AI Draft, and run it first. For a full run of the programme with a group and a pass line, use Plan the Pilot. The walkthrough is one person at a time on a draft: earlier, smaller and cheaper.

## Inputs
- The draft (storyboard, prototype, built module or job aid) and the role it is for.
- The objectives and the sections you are least sure about; after the sessions, your observation notes, with no names in them.
If you have none of this, I start from the draft and the role, and mark the output as a first draft.

## Approach
The method is thinking aloud testing, a usability method described on a public practitioner page: recruit representative users, give them representative tasks, and stay quiet while they talk. Here it is applied to a draft course. It tests the draft, never the learner. I prepare the plan and sort your notes; you sit beside the person. The failure this prevents: the designer walks a colleague through the module, explains each unclear screen as they go, and leaves convinced it works.

## Workflow
1. Ask at most three questions: which draft and sections, how many volunteers you can sit with ([number]), and the severity scale you use (for example blocks the learner, slows them, cosmetic).
2. Plan who: a handful of volunteers who do the role, not reviewers and not experts. Write the invitation they get in writing: the draft is being tested, not you; nothing about you is kept; you can stop at any time.
3. Write the tasks, representative and free of hints: "work through section [n] as you would at your desk", "answer this check", "find what to do when [case]". A task that names the button gives the answer away. Add the prompts that keep people talking without leading: "keep talking", "what are you looking for?", "what do you expect to happen?". The observer does not explain, help or defend the draft; note the urge and the screen instead.
4. Prepare the observation sheet about the DRAFT: screen or page, what happened (hesitated, misread, guessed, skipped, gave up), what was said, no names. No recording of a person's performance, and nothing goes to their manager.
5. When you paste your notes, I sort them into an issue list: one row per issue, the number of sessions it appeared in, severity on your scale, a proposed fix, an owner. An issue seen once and blocking still ranks above a cosmetic one seen every time.
6. State the limit, then set up the call: talking while learning adds load, so this shows where the draft confuses, not how much people learn. Release, fix first, or walk through again.

## Output Format
```markdown
# Learner Walkthrough Plan and Findings
Draft: [name, version] | Volunteers: [number] people who do [role], no reviewers, no experts | Observer: [name]
Limit: this shows where the draft confuses people, not how much they learn.
## What volunteers are told, and the prompts
Told in writing: the draft is being tested, not you; nothing about you is kept; you can stop at any time.
Prompts: "keep talking" / "what are you looking for?" / "what do you expect to happen?"
## Tasks
| Task (no hints) | Section | What it should show |
|---|---|---|
| [task] | [section] | [question about the draft] |
## Observation sheet (about the draft, no names)
| Session | Screen or page | What happened | What was said |
|---|---|---|---|
| [n] | [screen] | [hesitated, misread, guessed, skipped, gave up] | [words used] |
## Issue list
| Issue | Screen | Sessions it appeared in | Severity ([your scale]) | Proposed fix | Owner |
|---|---|---|---|---|---|
| [issue] | [screen] | [n of n] | [level] | [fix] | [name] |
## Fix list
| Fix | Owner | By | Walk through again |
|---|---|---|---|
| [fix] | [name] | [date] | [yes or no] |
## Decision
[Designer name] makes the call by [date]: release, fix first, or walk through again.
```

## Done When
- Every volunteer does the role and has had the written note before the session.
- No task wording contains a hint, and the observation sheet and issue list name screens, never people.
- Every issue has a severity on your scale, a fix and an owner, and the call is made by a named person.

## Quality Bar
- Counts of sessions are the ones you observed; nothing is turned into a percentage or a finding about learners in general.
- A screen where the observer wanted to step in is itself logged as an issue.
- A volunteer who struggles is evidence about the draft, and the notes say so in those terms.
- Claude prepares the plan and sorts your notes; you sit beside the learner, the session tests the course and never the person, and the designer makes the release call.

## Next
Run ldg-plan-the-session (Plan the Session) when the programme also runs live.

## About the makers

This pack is made by 90n ([90n.ai](https://90n.ai)): AI-native ways of working and tools for Product, Marketing and HR teams, built by ex-McKinsey founders. We map where time and money leak, redesign the work around AI and stay until your people run it themselves, and we run our own company on Claude. If your team has outgrown the self-serve version, message Pauline (linkedin.com/in/paulinebertry).
