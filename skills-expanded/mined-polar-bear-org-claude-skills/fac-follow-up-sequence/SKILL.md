---
name: fac-follow-up-sequence
description: Drafts the five messages a trainer sends after a session, each with one job, a date the trainer sets, a sender line and an opt-out, short enough to read on a phone. Use for "run fac-follow-up-sequence", "follow-up email after training", "post-training follow-up", "after the workshop emails", "training reinforcement messages", "what to send participants after a session", "nothing happened after the session", "check-in message after training", part of the Claude for Trainers and Facilitators Pack by 90n.
---

# Post-Session Follow-Up Sequence

## When To Use
The session went well, and then nothing happened. Use this before the day, or the evening after it, to line up the few messages that keep the session alive in the weeks when people are back under their normal workload. It answers one question: what reaches participants after the day, when, from whom, and what is each message for?

## When Not To Use
If you need the recall questions themselves, run Spaced Retrieval Plan; this sequence only leaves a slot for them. If you need the full record of what a workshop produced and decided, run Session Summary and Decisions, and let the first message link to it. Messages to participants' managers belong in Manager Briefing Note.

## Inputs
- What happened in the session: the learning points, one or two specific moments from the room, and where the material lives.
- The action plan page and the practice task, if you used them.
- A sample of a message you have written, so the drafts sound like you, and who is able to message participants.
If you have none of this, I start from the session title, its date and one thing people practised, and mark the output as a first draft.

## Approach
Grossman and Salas's 2011 review of training transfer names follow-up among the work-environment factors with the most consistent links to transfer, and Salas, Tannenbaum, Kraiger and Smith-Jentsch's 2012 review of the science of training treats what happens after a session as part of the training. Neither tells you what to write, so the craft is yours: one job per message. The failure this prevents is the single long email sent the next morning with the slides, a thank you, a survey link and "let me know how you get on", which does five jobs badly and is the last anyone hears.

## Workflow
1. Ask at most three questions: over how many weeks do you want to stay in touch, who can send messages to participants (you, or someone inside the organisation), and which of the action plan page, the practice task and recall questions did you use?
2. Lay out five messages with one job each: (1) the record of the day, (2) a nudge on the action plan, (3) the practice task and the peer partner, (4) a short check-in, (5) a close-out. Drop a message whose job does not exist for this session, and say which one was dropped and why.
3. Give each message a date as `[days after the session]` that you set, a subject line and a body that fits a phone screen. If a message needs scrolling, it has two jobs.
4. Write each to its job. Message 1 carries one specific true moment from the room and where the material lives. Message 2 asks only "has your situation come up yet?" Message 3 restates the task, its window and the partner conversation. Message 4 asks what did you try and what got in the way. Message 5 reports what the group said in aggregate and what happens next.
5. Add the sender line. External trainers often cannot message participants, so each message names who sends it, with a one-line cover note for that person. A point about contact lists or data rules is flagged: check with a qualified adviser.
6. Put an opt-out line on every message, and mark the slot "recall question from the Spaced Retrieval Plan goes here" where the two are used together. No recall question is written in this sequence.
7. Match the voice to your pasted sample and hand the drafts over. You read them, change what is not true to the room, and send. Nothing is sent by Claude.

## Output Format
```markdown
# Follow-Up Sequence
Session: [title] | Date: [date] | Runs for: [weeks] | Replies: voluntary, read as themes
## The sequence
| # | Job | Send on | Sender | Subject line |
|---|---|---|---|---|
| 1 | Record of the day | [days after the session] | [trainer / named person inside] | [subject] |
| 2 | Nudge on the action plan | [days after the session] | [sender] | [subject] |
| 3 | Practice task and peer partner | [days after the session] | [sender] | [subject] |
| 4 | Short check-in | [days after the session] | [sender] | [subject] |
| 5 | Close-out | [days after the session] | [sender] | [subject] |
## Message [number]: [job]
[Body, phone length. One job only.]
Recall slot: [recall question from the Spaced Retrieval Plan goes here, or "not used"]
Opt-out line: [how to stop receiving these]
Cover note for the sender: [one line, if the sender is not the trainer]
## Checks
- [ ] Every date is one I set
- [ ] The moment in message 1 really happened
- [ ] The close-out reports themes, not people
## Decision
[Trainer] decides which messages go out and on which dates, and [sender inside the organisation] confirms they will send them, by [date].
```

## Done When
- Each message has one job, a date you set, a subject line, a sender and an opt-out line.
- Every body fits a phone screen without scrolling past the ask.
- Message 1 carries a moment that really happened, taken from your notes.
- The recall slots are marked and left empty, or filled from the Spaced Retrieval Plan.

## Quality Bar
- No message says "just checking in". Each asks one thing or gives one thing.
- No guilt: a participant who has not started reads the same message as one who has.
- The close-out reports only what the group said in aggregate, with small groups left out.
- No claim that the sequence makes anything stick; it keeps a door open.
- Claude drafts and you send; replies are voluntary, read as themes, and never used to track who answered.

## Next
Run fac-spaced-retrieval-plan (Spaced Retrieval Plan) to write what goes in the recall slots.

## About the makers

This pack is made by 90n ([90n.ai](https://90n.ai)): AI-native ways of working and tools for Product, Marketing and HR teams, built by ex-McKinsey founders. We map where time and money leak, redesign the work around AI and stay until your people run it themselves, and we run our own company on Claude. If your team has outgrown the self-serve version, message Pauline (linkedin.com/in/paulinebertry).