---
name: fac-session-time-budget
description: Tests a session against the minutes it really has, producing the usable minutes, a four-way sort of the content, real activity times, a total per outcome and a cut list with a reason for each item. Use for "run fac-session-time-budget", "too much content for the time", "everything must go in", "cut content from a training", "how long does this activity really take", "session timing", "the deck is too long for the slot", "what do I tell the sponsor we cut", part of the Claude for Trainers and Facilitators Pack by 90n.
---

# Session Time Budget

## When To Use
The sponsor's deck was built for a day, the slot was built for a morning, and everything "must go in". Use this when you have a plan or an agenda and a pile of content, and you suspect the sums do not work. It answers: what fits, what moves, and what do I say to the person who asked for the slide?

## When Not To Use
This skill tests and trims a flow; it does not design one. If there is no flow yet, start with Training Session Plan or Workshop Agenda. Cutting slides inside a deck that already fits is the job of Training Slide Outline.

## Inputs
- The slot with its fixed times: arrival, breaks, opening, close.
- The outcomes, the full list of content items and activities people want in, and your own timings for any activity you have run before.
If you have none of this, I start from the slot, the outcomes and the content list and mark the output as a first draft.

## Approach
Cognitive load theory (Sweller, van Merriënboer and Paas, 2019): working memory is limited, so what does not serve the task competes with what does. The theory gives no minutes and no slide count, which is why every duration here is your own number. The sort is by outcome, not by who asked for the slide. The failure this prevents: every item kept "briefly", a trainer talking faster each hour, the break shortened, and the practice gone.

## Workflow
1. Ask at most three questions: what is the slot and what is fixed inside it, which outcomes must the session reach, and how much slack do you want to hold back?
2. Work out the usable minutes: the slot minus arrival, breaks, opening and close, minus `[slack]` you set. Show the subtraction line by line, because the sponsor usually budgets against the slot.
3. Sort every content item into one of four. Must practise: people need to do it in the room. Must know: needed from memory to do the task. Look up: needed sometimes, so it goes to the handout. Cut: serves no outcome. An item with no outcome is cut however senior its owner.
4. Cost each activity at its real time: setup, the work, moving people, the harvest. You supply or confirm every figure; I never supply a norm. An unknown is marked "to time in a dry run", not guessed.
5. Add it up per outcome and against the usable minutes. Where the total is over, show the gap in minutes.
6. Propose what moves, in this order: cut, then look up, then must know delivered before the session. Practice is the last thing touched, and only by your decision.
7. Write the cut list: each item with a destination (handout, follow-up message, pre-read, not covered) and a one-line reason the sponsor can accept, written about the outcome and never about the quality of their slide.

## Output Format
```markdown
# Session Time Budget
Session: [title] | Outcomes: [outcome 1] / [outcome 2]
## Usable minutes
Slot [minutes] - arrival [minutes] - breaks [minutes] - opening [minutes] - close [minutes] - slack [minutes, set by the trainer] = [usable minutes]
## Content sort
| Item | Outcome it serves | Sort (must practise / must know / look up / cut) | Why |
|---|---|---|---|
| [item] | [outcome or none] | [sort] | [reason] |
## Activity cost
| Activity | Setup | The work | Moving people | Harvest | Total | Figure from |
|---|---|---|---|---|---|---|
| [activity] | [minutes] | [minutes] | [minutes] | [minutes] | [minutes] | [trainer / to time in a dry run] |
## Budget by outcome
| Outcome | Practice | Must know | Total |
|---|---|---|---|
| [outcome] | [minutes] | [minutes] | [minutes] |

All outcomes [minutes] against usable [minutes] | Gap: [minutes over or under]
## Cut list
| Item | Moves to (handout / follow-up message / pre-read / not covered) | Reason the sponsor can accept |
|---|---|---|
| [item] | [destination] | [one line about the outcome] |
## Decision
[Trainer] makes the cut by [date] and takes the cut list to [sponsor] by [date].
```

## Done When
- The subtraction from slot to usable minutes is visible, with the slack you set.
- Every item has one sort and an outcome, or is on the cut list with a destination.
- Every activity total includes setup, moving and harvest, each figure says where it came from, and the total is at or under the usable minutes or the gap is shown.

## Quality Bar
- No invented durations, buffers or rules of thumb; a missing figure stays a placeholder.
- Practice is the last thing trimmed, and the plan says so if it was.
- Nothing is cut silently: every removed item has somewhere to go or the words "not covered".
- Claude does the arithmetic and shows what does not fit; you make the cut and take it to the sponsor.

## Next
Run fac-group-activity-bank (Group Activity Bank) to choose the activities for the minutes that survived.

## About the makers

This pack is made by 90n ([90n.ai](https://90n.ai)): AI-native ways of working and tools for Product, Marketing and HR teams, built by ex-McKinsey founders. We map where time and money leak, redesign the work around AI and stay until your people run it themselves, and we run our own company on Claude. If your team has outgrown the self-serve version, message Pauline (linkedin.com/in/paulinebertry).