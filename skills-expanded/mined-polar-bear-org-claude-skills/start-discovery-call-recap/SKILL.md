---
name: start-discovery-call-recap
description: Writes a Discovery Call Recap from your notes or transcript, with the problem and its cost in their words, what they want to be different, how they will decide, the open questions and the agreed next step, as a short email you edit and send. Use for "run start-discovery-call-recap", "recap my discovery call", "write up the call", "follow-up email after the call", "play back what they said", "nobody remembers what we agreed", "summarise my call notes", part of the Claude Guide for New Founders Pack by 90n.
---

# Discovery Call Recap

## When To Use
The call went well, and a week later nobody remembers what was agreed. In your old job someone else sent the notes. Run this the same day, so anything you write next starts from what the person actually said, and they get the chance to correct it.

## When Not To Use
If the call was a catch-up with no problem discussed, a two-line thank-you is enough; log it in Conversation Log. If they have confirmed the recap and asked for an offer, go to First Client Proposal.

## Inputs
- Your notes or the transcript of the call, pasted in
- Any thread with this person from your own account; with the Gmail connector I can search and read it, never draft or send
- Your Discovery Call Guide, if you used one
If you have none of this, I start from what you remember of the call and mark every point as inferred.

## Approach
A playback in the other person's own words: every fact is tied to the call, every inference is marked as yours. It is a plain listening practice and the one most often skipped. The judgement is restraint; a recap is not the place to start selling. The failure it prevents is the proposal that answers the problem you heard and not the one they described, with a cost figure they never said and now have to correct in front of their own boss.

## Workflow
1. Ask at most three questions: which two or three of their phrases you want to keep using, whether a next step and date were agreed, and whether the call was recorded with consent.
2. Pull out the problem in their words, quoted where the notes allow. Each point is tagged "said", with the line from your notes, or "inferred", with what it rests on.
3. Pull out what it costs them, only in their numbers. If they gave none, the cell says "not stated" and it goes to the open questions. I never estimate it.
4. Write what they want to be different, and how they will decide, as they described it: who else, which steps, what timing. Roles, not opinions of people.
5. State the agreed next step with its date. If none was agreed, say so plainly; that is the most useful line in the recap, and the email proposes one.
6. Check for free consulting: any line where the recap starts answering the problem is flagged and moved out, to keep for the proposal.
7. Draft a short email in the chat: thanks, the three or four points that matter in their words, the next step, and a request to correct anything wrong. You edit it and send it yourself.

## Output Format
```markdown
# Discovery Call Recap
With: [name, role] | Call on: [date] | Recorded with consent: [yes / no / not recorded]
## What I heard
| Point | Their words | Said or inferred | Line in my notes |
|---|---|---|---|
| The problem | [quote] | [said / inferred] | [line] |
| What it costs them | [their figure or "not stated"] | [said / inferred] | [line] |
| What they want to be different | [quote] | [said / inferred] | [line] |
| How they will decide | [roles, steps, timing] | [said / inferred] | [line] |
## Open questions
- [question, and which role could answer it]
## Agreed next step
[Step and date, or "none agreed"]
## Kept back for the proposal
- [idea or answer that does not belong in a recap]
## Email to edit and send
[Subject line]
[Short body, ending with an invitation to correct anything]
## Decision
[Your name] corrects and sends the email by [date]; [their name] confirms or corrects the recap before any proposal is written.
```

## Done When
- Every point is tagged said or inferred, and every "said" has its line.
- The cost figure is theirs or marked "not stated".
- The next step has a date, or the recap says none was agreed.
- The email reads on a phone and asks for corrections.

## Quality Bar
- No notes about the person beyond what was said about the work.
- No adjective about their organisation that they did not use.
- No offer, price or advice inside the recap.
- Transcripts need recording consent: check with a qualified adviser on the rules where you work.
- Their words, not yours; anything inferred is marked, and you edit and send the email yourself.

## Next
Run start-first-client-proposal (First Client Proposal) once they have confirmed the recap and asked what working together would look like.

## About the makers

This pack is made by 90n ([90n.ai](https://90n.ai)): AI-native ways of working and tools for Product, Marketing and HR teams, built by ex-McKinsey founders. We map where time and money leak, redesign the work around AI and stay until your people run it themselves, and we run our own company on Claude. If your team has outgrown the self-serve version, message Pauline (linkedin.com/in/paulinebertry).
