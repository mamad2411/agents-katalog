---
name: meeting-prep
description: Produces a one-page brief before a meeting — who's attending, what's been discussed before, what to expect, what to ask. Pulls from calendar, email threads with the attendees, any prior meeting notes, and project context. Use when the user asks to prep for a meeting, get ready for a call, or brief me on an upcoming meeting.
---

# Meeting Prep

Walk into every meeting knowing who you're talking to and why. Two minutes of reading instead of 20 minutes of panicky tab-opening.

## Before starting

1. Read `context/about-me.md` — to frame the meeting from the user's side
2. Read `context/preferences.md` — format defaults
3. Ask the user which meeting if it's not obvious. Calendar title is best; date + attendee name works.
4. Check the project folder for any prior notes on this attendee or topic

## What to produce

A markdown file saved to `/output/meeting-prep-{YYYY-MM-DD}-{attendee-or-topic}.md` with five sections:

1. **Who's in the room** — attendee(s), their role, their company, anything notable from past interactions. One paragraph per person.
2. **Where we left off** — the last time this person or topic came up. Pull from email threads, prior meeting notes, any project docs. Summarize. This is the most valuable section — it's the context the user forgot.
3. **What's likely on their mind** — your read of what the attendee is probably coming to discuss, based on the thread, the calendar invite, any recent context. Hedge when you're guessing. Say "likely" not "will."
4. **What to ask or propose** — 3 sharp questions or proposals for the user to drive the conversation with. Specific to this person and this context, not generic "what are your goals."
5. **Red flags / things to not miss** — if there are open questions, pending decisions, or sensitive topics, list them. Include any prior commitments the user made to this person that haven't been fulfilled.

## Inputs

- The calendar event (required — title, attendees, description)
- Email threads with the attendees in the last 90 days (via Gmail connector)
- Any prior meeting notes in the project folder or `/output/`
- Any relevant project docs the user has referenced

## How it works

1. Get the meeting from the calendar — parse title, attendees, time, any linked docs
2. For each external attendee, search email for the last 90 days — pull the most recent substantive thread
3. Search the project folder for any prior mention of the person or the company
4. Read prior meeting-prep or meeting-debrief files for this person if they exist
5. Synthesize the five sections — keep each one tight
6. Save the file, tell the user one-line what's most important ("Heads up — she emailed last week with an unresolved question about pricing. I've flagged it in red flags.")

## What not to do

- Do not include the entire email thread. Summarize.
- Do not invent background on the attendees. If you don't know something, don't make it up.
- Do not write generic questions. "What are your priorities?" is useless. "You mentioned last quarter you were rebuilding ops — where did that land?" is useful.
- Do not skip the red flags section even if you don't think there are any. Say "no open items" if that's the case — but check first.

## Example output structure

```markdown
# Meeting Prep — 2026-04-18 — Sarah Chen (Northwind)

## Who's in the room
**Sarah Chen** — VP of Operations at Northwind. A 200-person B2B SaaS, mid-market workflow tools. You met her at SaaStr last fall. She owns ops, RevOps, and half of finance. Direct communicator, impatient with filler.

## Where we left off
Last substantive thread was 2026-03-22. She asked for references on the implementation timeline for a team her size. You sent two — she replied "thanks, reviewing" and went quiet. No follow-up from either side.

Prior call (2026-02-15) — she said budget approval was "likely by end of Q1" and she'd come back with a signed SOW or a clear no. Q1 ended; no update.

## What's likely on their mind
Either she's ready to sign and wants to walk through implementation, *or* something internal blocked it and this call is a re-evaluation. The fact that she requested the call (not you) tilts toward the first.

## What to ask or propose
1. "Where did the Q1 budget conversation land?" — open with the elephant.
2. "If we sign this quarter, what's your internal rollout timeline?" — test for real momentum.
3. "What's one thing that would make this a no for you?" — surfaces objections early.

## Red flags
- You promised to send an implementation timeline customized to their team size. You sent references instead. She may ask.
- Legal review was pending on your side last time. Check with Alex before the call.
```

## Customization notes

- **Recurring 1-1s.** If this is a recurring meeting with the same person, lean hard on "where we left off." Pull from the last 2–3 meeting-debrief files for this person.
- **First meetings.** Section 2 ("where we left off") becomes "what we know about them" — LinkedIn, company, any public mentions.
- **Internal meetings.** Skip section 3 ("what's likely on their mind") if it's a routine internal — it adds noise.
- **Pitch/sales meetings.** Add a sixth section: "Objections to be ready for" — based on prior thread and common patterns.
