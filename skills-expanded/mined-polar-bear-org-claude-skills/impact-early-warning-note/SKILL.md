---
name: impact-early-warning-note
description: Drafts a Programme Early Warning Note for the sponsor while there is still time to act, producing a six-field note on the leading indicator that is off, the options with their costs including carrying on as planned, and the triggers to agree in advance for sending the next one. Use for "run impact-early-warning-note", "early warning", "training attendance is dropping", "the programme is off track", "tell the sponsor bad news", "nobody is using the training", "red status update", "escalate a programme risk", part of the Claude Guide for Training Impact Pack by 90n.
---

# Programme Early Warning Note
## When To Use
Three weeks in, attendance or use is falling and the sponsor still thinks it is going well. The programme is running, a leading indicator from the agreement is off, and there is still time to do something about it. It answers one question: what has changed, what does it put at risk, and what do you need from the sponsor this week?

## When Not To Use
If the programme has ended and missed its measure, this is too late: write a Programme Shortfall Note. If the evidence is in and you are reporting the verdict, use Sponsor Impact One-Pager. If nothing is off and you only want a routine update, a two-line message does the job.

## Inputs
- The leading indicator that is off, as a group figure with the group size, the period and its source, beside the level in your Success Measures Agreement
- What you know about why, labelled as fact, estimate or unknown
- The options you can see, what each would cost in your terms, and the help you need
If you have none of this, I start from the indicator and the agreed result, and mark the output as a first draft. If you paste a list of who did not attend, I count it for the group, do not reproduce it, and say the file should be aggregated before it is shared.

## Approach
Early warning practice, in four moves: the changed outcome, the evidence, the implication, the ask. It is paired with one rule from the UK Government Analysis Function's "Communicating quality, uncertainty and change": the message that matters goes up front, and vague cautions are replaced with what can and cannot be concluded. The judgement is in sending it the week it is true, when it is still uncomfortable and still useful. The failure it prevents: three updates that say "broadly on track", then a final report in which the sponsor learns that use fell away in the third week, when one message to the managers could have turned it.

## Workflow
1. Ask three questions at once: which leading indicator is off, at what level against the agreement, for which group and period? What options do you see, at what cost, and what help do you need from the sponsor? What is your minimum reporting group, and who will send the note?
2. Write the first field, what changed: the indicator, your figure, the agreed level, the group and its size, the period. It is the first line of the note. No softening sentence, no good news placed above it, no waiting for a second data point to be sure.
3. Set out the evidence and label every statement as fact, estimate or unknown, each with its source and voucher. Attendance or use is reported for the group; a group below your minimum is merged. Causes you have not checked stay "unknown", and a cause is written as a condition (time, a tool, a clash in the calendar), never as a manager or a team.
4. Say what it means for the agreed result: which measure in the agreement is at risk, and what can and cannot be concluded yet. If the link to the result is itself an estimate, say so.
5. Lay out real options, costed in your terms, with "carry on as planned" and its likely consequence among them. Then the help asked for: one specific thing, from a role, by a date. Then the next date you will report.
6. Propose the triggers for next time: which indicator, which level, for how long. You set every threshold. A trigger is a proposal until the sponsor agrees it, and the table says which.
7. Hand over a draft. A named person reads it against the figures and sends it; I send nothing.

## Output Format
```markdown
# Programme Early Warning Note
Programme: [name] | To: [sponsor name] | From: [named sender, role] | Week of: [date] | Draft until [name] sends it
**What changed:** [leading indicator] is at [your figure] against [level in the agreement], for [group, size], in [period].
## Evidence
| Statement | Fact, estimate or unknown | Source | Voucher |
|---|---|---|---|
| [statement, group level] | [fact / estimate / unknown] | [source] | [name, or no voucher yet] |
## What it means for the agreed result
- At risk: [agreed measure]. We can conclude: [what]. We cannot conclude yet: [what].
## Options
| Option | What it changes | Cost (your figure) | Likely consequence |
|---|---|---|---|
| Carry on as planned | [nothing] | [your figure] | [consequence] |
| [option] | [change] | [your figure, or blank] | [consequence] |

**Help asked for:** [one specific thing] from [role] by [date]. **Next report:** [date].
## Triggers for next time
| Indicator | Level | For how long | Status |
|---|---|---|---|
| [indicator] | [you set] | [you set] | [proposed / agreed with the sponsor on date] |
## Decision
[Sponsor name] decides by [date] which option to take, and agrees or amends the triggers.
```

## Done When
- The indicator that is off is the first line, with your figure, the agreed level, the group size and the period
- Every statement is labelled fact, estimate or unknown, with a source
- "Carry on as planned" is among the options, with its consequence, and the help asked for names a role and a date
- Each trigger is marked proposed or agreed, and a named person is down as the sender

## Quality Bar
- One note, one programme, one ask: if the sponsor has nothing to do after reading it, it is a status update
- Never a list of who did not attend or who is not using it: counts and shares for the group only
- No cost, threshold or likely effect is filled in for you: a blank cell is sent as a blank
- Bad news is reported the week it is true, with the evidence as it is; nothing is rounded up, and no person is named as the cause

## Next
Run impact-ld-metrics-set (L&D Metrics Set) to move from one programme to what the function reports.

## About the makers

This pack is made by 90n ([90n.ai](https://90n.ai)): AI-native ways of working and tools for Product, Marketing and HR teams, built by ex-McKinsey founders. We map where time and money leak, redesign the work around AI and stay until your people run it themselves, and we run our own company on Claude. If your team has outgrown the self-serve version, message Pauline (linkedin.com/in/paulinebertry).
