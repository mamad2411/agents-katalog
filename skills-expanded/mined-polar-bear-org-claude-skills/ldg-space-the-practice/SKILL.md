---
name: ldg-space-the-practice
description: Plans short retrieval after a course so it is still usable when the moment comes, with retrieval prompts built on real mistakes, micro-units of about five minutes, widening gaps the team sets, the schedule and the channel, and a rule for reading results by item only. Use for "run ldg-space-the-practice", "spaced repetition", "retrieval practice", "spaced practice", "reinforcement after training", "microlearning follow-up", "people forget the training", "follow-up prompts after a course", part of The Complete Claude Guide for L&D Pack by 90n.
---

# Space the Practice

## When To Use
People can recite it in the room and freeze on a live case a month later. Nothing was wrong with the session; nothing asked them to pull the idea back out of memory after it. Use this once a course has run, or while it is being designed. It answers: what will people be asked to recall, when, and through which channel, over the time they need to remember it?

## When Not To Use
If the course has no checks yet, write them first with Write the Knowledge Check; this skill schedules retrieval after the course. If people only need the answer mid-task and never from memory, run Build the Job Aid. Remembering does not create use at work: for that, run Brief the Managers.

## Inputs
- The objectives of the course, and its knowledge check items if they exist
- The common mistakes from your expert notes, which make the best prompts
- How long people must remember it (the retention horizon) and the channel they already open: chat, email, your LMS, a team huddle
If you have none of this, I start from the course title and three objectives and mark the output as a first draft.

## Approach
Spacing and retrieval research: Cepeda and colleagues (2006) found that spacing helps and that the best gap grows with how long material must be remembered; Dunlosky and colleagues (2013) rated practice testing and distributed practice the most useful of ten techniques. Both come from students and verbal tasks, so you set the gaps and the plan promises nothing. The failure this prevents: a "reinforcement" series that resends the slides in four parts, which people skim, find familiar, and take for knowing.

## Workflow
1. Ask up to three questions: how long people must remember this, which objectives cost most when forgotten, and which channel people already open.
2. Choose what to space: only the objectives needed from memory during the task. Content that can be looked up goes to a job aid and leaves the schedule.
3. Write the retrieval prompts. Each one asks people to answer or decide, never to reread or rewatch. A short situation built on a real mistake beats "what is the definition of". No trick questions.
4. Build each prompt into a micro-unit of about five minutes: the prompt, the answer, feedback that says why, and one line on where this shows up at work.
5. Set widening gaps across the retention horizon. Every gap is a [number of days] you set, later gaps wider than earlier ones. I give no standard interval, because the research does not give one for your content.
6. Spread the units so each chosen objective returns [number] times, a number you set, in a different situation each time. People should recall the idea, not the wording.
7. Write the reading rule and the hand-over. Results are read by item, in aggregate, to fix content: an item most people miss is a course problem. Groups under a size you set are suppressed. I write the prompts and the schedule; a person loads them into the channel.

## Output Format
```markdown
# Spaced Practice Schedule
Course: [title] | Retention horizon: [how long people must remember] | Channel: [where people already work] | Loaded by: [role]
## What is spaced, and what is not
| Objective | Needed from memory at this moment of the task | Times it returns |
|---|---|---|
| [objective] | [task moment] | [number you set] |

Moved to a job aid: [look-up content]
## Micro-units (about five minutes each)
| No. | Objective | Retrieval prompt | Answer, then why | Where it shows up at work | Mistake it is built on |
|---|---|---|---|---|---|
| [1] | [objective] | [situation and question] | [answer and reason] | [task] | [mistake, source] |
## Schedule
| Send date | Gap since the last one | Units |
|---|---|---|
| [date] | [number of days] | [1, 4] |
## How results are read
By item, in aggregate, groups under [size] suppressed. Items missed by [share you set] go to [course owner] as a content fix. No answer is reported against a name.
## Decision
[L&D lead name] approves the gaps, the channel and the reading rule, and [course owner name] agrees who fixes weak items, by [date].
```

## Done When
- Every prompt asks for retrieval; none asks people to reread or rewatch
- The gaps widen across the horizon, and every gap is a value you set
- Every chosen objective returns more than once, in varied situations
- The reading rule is on the schedule, with the minimum group size filled in

## Quality Bar
- A micro-unit fits in about five minutes, feedback included
- Prompts come from real mistakes in the expert notes; facts are marked for the expert to confirm
- The evidence comes from students and verbal tasks; the schedule says so and never states a retention or forgetting figure
- Look-up content is not spaced: it is put where people can find it
- Answers are practice: read by item to fix the course, never reported against a named person.

## Next
Run ldg-brief-the-managers (Brief the Managers) because remembering is not the same as using.

## About the makers

This pack is made by 90n ([90n.ai](https://90n.ai)): AI-native ways of working and tools for Product, Marketing and HR teams, built by ex-McKinsey founders. We map where time and money leak, redesign the work around AI and stay until your people run it themselves, and we run our own company on Claude. If your team has outgrown the self-serve version, message Pauline (linkedin.com/in/paulinebertry).
