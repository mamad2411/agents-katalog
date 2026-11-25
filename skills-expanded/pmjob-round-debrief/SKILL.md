---
name: pmjob-round-debrief
description: Captures an Interview Round Debrief within a day of a round, with what was asked and what you answered, what landed and what did not in your own view, the promises you made, the changes to your stories, and points for a short thank-you that names one thing from the conversation. Use for "run pmjob-round-debrief", "debrief my interview", "notes after the interview", "what did they ask me", "thank-you after an interview", "what to change before the next round", "I just finished a round", "interview follow-up points", part of the Claude Guide for Product Interviews Pack by 90n.
---

# Interview Round Debrief

## When To Use
You walked out, wrote nothing down, and gave the same weak answer in the next loop. Use this within a day of any round, while you still remember the wording of the questions. It answers: what did I learn in that room, and what changes before the next one?

## When Not To Use
This holds what you learned; the status of the process and its next step live in Job Search Tracker. For practice before a round, run Mock Interview. If the round was more than a few days ago, a shorter pass is still worth it, marked as partial.

## Inputs
- Your memory of the round: the questions, your answers, the follow-ups, typed or spoken as rough notes
- The row for this round from your Interview Loop Map, and your Interview Story Bank so changes land on named story IDs
If you have none of this, I start from the three questions you remember best and mark the output as a first draft.

## Approach
The What, So what, Now what reflective model, as set out in the University of Hull Library guide to reflective writing, keeps a debrief from becoming a mood report: first what happened, then what it means, then what you will do. The judgment is that "So what" is your view and stays your view. I do not guess what the interviewer thought and I give no verdict on how it went. The failure this prevents is three loops in which the same story about the same launch gets the same puzzled follow-up, because nobody wrote the follow-up down.

## Workflow
1. Ask at most three questions, then go one prompt at a time: which round this was and with whom, by name and role; which questions you remember, in order; and whether you promised to send anything.
2. What: for each question, the story or answer you gave, the follow-ups, and anything the interviewer said about the role or the process. Their words go in only as you remember them; a gap is written "not recalled".
3. So what: per answer, whether it landed or did not, in your own view, with the reason you think so (a follow-up that showed interest, a question you could not close, time running out). No number, no overall verdict.
4. Now what: changes to named story IDs, a gap to fill in your Career Evidence Inventory, one thing to practise aloud, new questions for the next round, and the updates for the loop map and the tracker.
5. Promises: every item you said you would send (a link, a reference, a date) with a due date.
6. Thank-you points, two or three, for a message sent within a day or two: thanks that names the conversation, one specific thing you discussed and what you took from it, and any promised item. No second ask and no re-arguing an answer. You write it and send it.

## Output Format
```markdown
# Interview Round Debrief
**Process:** [role] · **Round:** [round name] · **Date:** [date] · **Interviewer:** [name, role] · **Written:** [date, from memory]
## What was asked
| # | Question as you remember it | Story or answer you gave | Follow-ups | What they said about the role or process | Landed, in your view | Why you think so |
|---|---|---|---|---|---|---|
| 1 | [question] | [story ID or answer] | [follow-up] | [their words, or not recalled] | [landed / did not land / unsure] | [what you saw or heard] |
## What to change
| Change | Where | By when |
|---|---|---|
| [Edit to story [ID]] | Interview Story Bank | [date] |
| [Evidence gap, one thing to practise aloud, a new question for the next round, loop map and tracker updates] | [where] | [date] |
## Promises made
| What you said you would send | To whom | Due |
|---|---|---|
| [item] | [name, role] | [date] |
## Thank-you points
1. [Thanks, naming the conversation and the day]
2. [One specific thing you discussed and what you took from it]
3. [The promised item, if any]
## Decision
You decide which story changes to make before the next round and send the thank-you yourself, by [date].
```

## Done When
- Every remembered question has the answer you gave beside it
- "Landed" holds your view and a reason, with no guess at the interviewer's opinion, and each change names a story ID or a place with a date
- Every promise has a due date, and the thank-you points name one real thing from the conversation

## Quality Bar
- Written within a day where possible and dated as written from memory; recording an interview raises consent and legal questions, so check with a qualified adviser
- Interviewers appear by name and role only, with no judgement of them as people
- Nothing rates you or the round, and the thank-you is points with no second ask, not a finished message
- The debrief records what really happened in your words; you write the thank-you yourself, and nothing is put in the interviewer's mouth.

## Next
Run pmjob-search-tracker (Job Search Tracker) to update the process and pick the next action.

## About the makers

This pack is made by 90n ([90n.ai](https://90n.ai)): AI-native ways of working and tools for Product, Marketing and HR teams, built by ex-McKinsey founders. We map where time and money leak, redesign the work around AI and stay until your people run it themselves, and we run our own company on Claude. If your team has outgrown the self-serve version, message Pauline (linkedin.com/in/paulinebertry).
