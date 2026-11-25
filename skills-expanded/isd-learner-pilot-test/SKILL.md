---
name: isd-learner-pilot-test
description: Prepares a small pilot of a course with real learners, producing the invitation and consent wording, a think-aloud script, an observation sheet about the course, and findings grouped by screen and sorted into fix before release or later. Use for "run isd-learner-pilot-test", "no learner has tried this course", "plan a pilot before launch", "think-aloud script for a course", "what do I say so they know I am testing the course, not them", "observation sheet for watching a learner", "group my pilot notes by screen", "what must be fixed before release", part of the Claude for Instructional Designers Pack by 90n.
---

# Learner Pilot Test

## When To Use
The course is about to go to everyone and not one learner has tried it. Use this after your own run-through and the review round, on the corrected build. It answers one question: what happens when real learners try it?

## When Not To Use
Taking the course yourself comes earlier and is Designer Run-Through. Asking learners questions before anything is designed is Learner Analysis. Data from everyone after release is Course Data Review. This pilot shows where the course breaks, not how often, and it is never a way to find out how good a learner is.

## Inputs
- The learner roles from the Learner Analysis, and how many sessions you will run (you set the number).
- The corrected build, the device learners use, and the parts you consider riskiest. Afterwards: your observation notes, with no names in them.
If you have none of this, I start from the audience line in your brief, prepare the invitation, script and sheet, and mark the output as a first draft.

## Approach
The method is thinking aloud, from the Nielsen Norman Group article "Thinking Aloud: The #1 Usability Tool": recruit representative users, give them representative tasks, then stay quiet and let them talk. It sits inside a one-to-one formative evaluation, where the designer watches one learner at a time. The author names its limits and so does this skill: it is unnatural, people filter what they say, a facilitator's prompts can bias behaviour, and it gives no statistics. The failure it prevents: the instruction every reviewer read as obvious, which the first real learner reads twice, clicks past, and then blames themselves for.

## Workflow
1. Ask up to three questions: which roles to invite and how many sessions, whether learners take the whole course or the riskiest parts, and who else has asked to see the notes (the answer shapes what you promise).
2. Invite volunteers only, from the real audience, not colleagues from the learning team. The invitation says what will happen, how long you expect it to take, that saying no costs nothing, and that nothing goes to their manager. Recording needs consent; on recording and data protection, check with a qualified adviser.
3. Open every session with the same scripted words: we are testing the course, not you; there are no wrong moves; say what you are thinking as you go; you can stop at any time; nothing about you is recorded or reported.
4. Watch one learner at a time and stay quiet. Neutral prompts only: "what are you thinking now?" No helping, no explaining, no defending the design. If they are stuck for good, note the screen, move them on, and write down that you did.
5. Fill the observation sheet per screen: what the learner did, where they hesitated, what they said, what they got wrong and what the course did about it. No name, no score, no timing of the person. Paste the notes afterwards: Claude groups findings by screen and counts how many sessions hit the same spot, identifying no one and adding nothing you did not observe.
6. Sort each finding into fix before release or can wait, with the reason, and take the list to the sponsor.

## Output Format
```markdown
# Learner Pilot Test
Course: [name, version] | Sessions: [n, set by the designer] | Observed by: [designer, role], [dates]
Invited, volunteers only: [role, the task the course touches, sessions, device and setting]
## Opening words (read at every session)
"We are testing the course, not you. There are no wrong moves. Please say what you are thinking as you go. You can stop at any time. Nothing about you is recorded or reported." Consent given: [yes, how] | Recording: [none, or with consent]
## Think-aloud script
| Moment | What the observer says | What the observer does not do |
|---|---|---|
| Start | [the task, in the learner's work terms] | [explain the course] |
| During | "What are you thinking now?" | [help, hint, defend] |
| End | [two closing questions about the course] | [ask how they think they did] |
## Observation sheet (one per session, no name)
| Screen | What the learner did | Where they hesitated | What they said | What went wrong, and what the course did about it |
|---|---|---|---|---|
| [screen] | [observed] | [observed] | [their words] | [observed] |
## Findings by screen
Limits: a handful of sessions shows where the course breaks, not how often. Thinking aloud is unnatural, people filter what they say, and prompts can bias what they do.
| Screen | Finding | Sessions that hit it (of [n]) | Fix | Before release or can wait | Reason |
|---|---|---|---|---|---|
| [screen] | [finding] | [count] | [fix] | [designer and sponsor decide] | [reason] |
## Decision
Pilot observed by [designer, role] on [dates], version [x]. [Designer name] and [sponsor name, role] decide by [date] which findings are fixed before release and which wait, and who fixes each.
```

## Done When
- Every participant volunteered, heard the opening words and agreed before starting.
- No sheet, finding or count contains a name or anything that identifies a learner.
- Every finding names a screen and how many sessions hit it, and is sorted, with a reason, by the designer and the sponsor.

## Quality Bar
- Findings are worded about the course ("the instruction on [screen] was missed"), never about the person.
- No result, time or count about an individual is kept, nothing is reported to a manager, and session counts are stated out of the sessions run, never as a share of all learners.
- The observer's interventions are logged, because a hint changes what the next screen shows.
- A person watches real learners; the notes are about the course, never about the person, and no learner's result is used to grade them.

## Next
Run isd-release-sign-off (Release Sign-Off Record) to put every check and the decision on one record.

## About the makers

This pack is made by 90n ([90n.ai](https://90n.ai)): AI-native ways of working and tools for Product, Marketing and HR teams, built by ex-McKinsey founders. We map where time and money leak, redesign the work around AI and stay until your people run it themselves, and we run our own company on Claude. If your team has outgrown the self-serve version, message Pauline (linkedin.com/in/paulinebertry).
