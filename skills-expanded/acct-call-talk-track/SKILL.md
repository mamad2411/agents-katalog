---
name: acct-call-talk-track
description: Prepares a call talk track in keywords, with an opener that asks permission, the reason for the call in one sentence, two discovery questions, the ask with two time slots, answers to two common brush-offs and a 20-second voicemail. Use for "run acct-call-talk-track", "talk track", "call script", "call opener", "what do I say on a sales call", "voicemail script", "they said send me something", "we already have a supplier", part of the Claude for Account Executives Pack by 90n.
---

# Call Talk Track

## When To Use
You call less than you should because you do not know what to say after hello. Run this before a call block, for one contact or for a handful with the same reason. It answers: what to say, in what order, and how to react to the two brush-offs you hear most, without reading a text aloud.

## When Not To Use
For full discovery in a booked meeting, run Discovery Call Questions: here two questions are enough. If you have no true reason for the call yet, run Reason to Call first; a track with no reason is a pitch.

## Inputs
- The person you are calling (name, job role, account) and your reason for the call, with its source.
- What you want from the call: usually a short meeting.
- Two time slots you can offer.
If you have none of this, I start from the person's job role and your offer in one sentence, and mark the output as a first draft.

## Approach
A permission-based opening, then the reason for the call in one sentence: common practice, described here generically. The judgment is simple. The person was not expecting you, so asking whether now is a good time is the only fair way to begin, and a no is an answer. You get keywords, not sentences. The failure it prevents: the long recited monologue that ends with "send me something".

## Workflow
1. I ask at most three questions: who you are calling, what the true reason is, and what you will ask for at the end.
2. Opener: who you are and your company, then "is now a bad time?". If it is, you ask when to call back, note it, and hang up. No pushing past it.
3. The reason in one sentence, built from your sourced reason for this person. If it takes two sentences it is not ready.
4. Two open questions about their situation. You note the answers for the meeting; you do not answer them yourself.
5. The ask: a short meeting, with your two slots.
6. The two brush-offs, each in three moves: acknowledge, one question to understand, one light next step. "Send me something": what would be worth sending, and to answer which question? "We already have a supplier": what would have to change for a second look to be worth 20 minutes? If the answer is no, you accept it and thank them.
7. A voicemail of about 20 seconds: your name, the reason, how to reach you. No pressure, no invented deadline. I also flag the phone rules to verify for the contact's country, such as do-not-call lists: check with a qualified adviser.

## Output Format
```markdown
# Call Talk Track
Calling: [name, job role, account] · Reason: [one sentence, source] · Goal: [short meeting]
## Run of the call, in keywords
| Moment | Keywords (say it your way) |
|---|---|
| Opener | [who I am] · [is now a bad time?] · if yes: [when to call back] |
| Reason | [one sentence] |
| Questions | [question 1] · [question 2] |
| Ask | [short meeting] · [slot 1] · [slot 2] |
## Brush-offs
| What you hear | Acknowledge | Question to understand | Light next step |
|---|---|---|---|
| "Send me something" | [keywords] | [question] | [step] |
| "We already have a supplier" | [keywords] | [question] | [step] |
## Voicemail (about 20 seconds)
[Name] · [reason] · [how to reach you]
## After the call
[What you note: answers to the two questions, the agreed step, or the no]
## Decision
[You] decide who you call, on which day, and what goes into the CRM after each call.
```

## Done When
- The opener asks permission and covers the case where the time is wrong.
- The reason fits one sentence and rests on a true fact.
- Each brush-off has a question and a light next step, and a no is accepted.
- The voicemail can be said in about 20 seconds.

## Quality Bar
- Keywords, not full sentences: you talk the way you talk.
- No manipulation technique, no false urgency, no trick question.
- The track stays inside accounts you own; it is not a script for calling strangers at volume.
- Claude makes no call and dials no number; you speak in your own words and you accept a no.

## Next
Run acct-sales-call-plan (Sales Call Plan) to prepare the meeting the call earned.

## About the makers

This pack is made by 90n ([90n.ai](https://90n.ai)): AI-native ways of working and tools for Product, Marketing and HR teams, built by ex-McKinsey founders. We map where time and money leak, redesign the work around AI and stay until your people run it themselves, and we run our own company on Claude. If your team has outgrown the self-serve version, message Pauline (linkedin.com/in/paulinebertry).
