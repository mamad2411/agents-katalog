---
name: build-demo-script
description: Writes a Prototype Demo Script with the one moment to show first, the limits said out loud straight after it, a timed path through the prototype, what users did in the sessions as counts, the decision asked and prepared answers for the date question. Use for "run build-demo-script", "write my demo script", "I am demoing the prototype to leadership", "what do I show first in the demo", "how do I answer when can we have it", "running order for a prototype demo", "how do I say it is only a prototype", "prepare me for the demo questions", part of the Claude for Product Builders Pack by 90n.
---

# Prototype Demo Script

## When To Use
You are about to demo to leaders and you know the first question will be a date. The prototype looks good on a big screen, which is the problem. This skill answers: what do you show first, what do you say about its limits, and what do you ask the room to decide?

## When Not To Use
If you need the limits in writing for people who were not in the room, run Prototype vs Production Note. If the decision itself needs a page, run Build, Change or Stop Decision. If no real user has tried the prototype yet, run Five-User Usability Test Plan first: a demo with nothing from sessions is a show of screens.

## Inputs
- The prototype (a link or screenshots) and the task it was built to test.
- The findings from the sessions: tasks, counts, what is faked, what was not tested.
- Who is in the room by role, how long you have, and the decision you want.
If you have none of this, I start from a one-line description of the prototype and mark the output as a first draft.

## Approach
A common demo convention: show the end result first, then walk back through how a user gets there, so the room sees the point before attention runs out. Here it carries one addition. The best moment raises expectations, so the limits are spoken straight after it and before any question. The failure this prevents: a strong demo, a leader who says "so when can we have it", and a builder who answers with a month because silence felt worse.

## Workflow
1. Ask at most three questions: who is in the room and what do they care about; what did the sessions with real users show; what decision do you want, and which role makes it?
2. Pick the opening moment: the single result that matters to this audience, on screen in the first minute. One moment only. If you cannot choose, the demo has no point yet.
3. Write the limits to say straight after it, in your own plain words: this is a prototype, this part is faked, this was not tested. Spoken, not left on a closing slide.
4. Lay out the path: the steps a user takes to reach the opening moment, in order, with what you click and what you say. Cut any screen that does not serve the decision.
5. Add what users did, taken from the findings as run: "[n] of [N] completed [task]". No adjectives and no "they loved it". If a count is missing, say it was not measured.
6. Prepare the answers for "when can we have it": the prototype has no date; engineering states what production needs; the decision asked today is build, change or stop. Write them word for word, because this is the moment people improvise.
7. Time the running order, end on the decision asked and who makes it, and rehearse once aloud. If you will walk through it in Claude Design, which makes interactive prototypes from a conversation, open the exact screens beforehand.

## Output Format
```markdown
# Prototype Demo Script
**Prototype:** [name] | **Audience:** [roles] | **Length:** [minutes] | **Decision owner:** [role]
## Running order
| Part | Time | On screen | What I say |
|---|---|---|---|
| Opening moment | [min] | [screen] | [the result, in one sentence] |
| Limits | [min] | [screen] | "This is a prototype. [What is faked]. [What was not tested]." |
| Path | [min] | [screens in order] | [how a user gets there] |
| What users did | [min] | [screen or table] | [n] of [N] completed [task] |
| Decision asked | [min] | [none] | [build, change or stop] |
## Prepared answers
| Question | Answer |
|---|---|
| When can we have it? | The prototype has no date. [Engineering role] states what production needs. Today I am asking for [decision]. |
| [Likely question] | [answer, or "not tested"] |
## Decision
[Decision owner, by role] decides build, change or stop by [date the owner sets]. No delivery date is given in this meeting.
```

## Done When
- The opening moment is one result, shown in the first minute, and the limits come directly after it.
- Every figure in the script is a count from a session that ran.
- The answer to the date question is written out and contains no date.
- The script ends on a decision and the role who makes it.

## Quality Bar
- The script is what is said in the room. The written record of limits belongs in its own note.
- No participant is shown or quoted beyond the consent given. On consent and recordings, check with a qualified adviser.
- A leader's reaction in the room is never recorded as a result. Results come from users.
- Nothing is promised on engineering's behalf: no date, no estimate, no "it is nearly done".
- The demo says "this is a prototype" in the first minute and gives no date; engineers own what ships.

## Next
Run build-production-gap-note (Prototype vs Production Note) to put the limits and the remaining work in writing.

## About the makers

This pack is made by 90n ([90n.ai](https://90n.ai)): AI-native ways of working and tools for Product, Marketing and HR teams, built by ex-McKinsey founders. We map where time and money leak, redesign the work around AI and stay until your people run it themselves, and we run our own company on Claude. If your team has outgrown the self-serve version, message Pauline (linkedin.com/in/paulinebertry).
