---
name: meeting-debrief
description: Turns raw meeting notes or a rough recap into structured action items, a follow-up email draft, and a saved record for future reference. Use when the user says they just finished a meeting, wants to debrief a call, needs to send a follow-up, or wants to capture notes from a meeting. Pairs with meeting-prep — saves to the same attendee/topic file pattern.
---

# Meeting Debrief

The meeting just ended. The user has rough notes or a memory. Turn that into action items, a follow-up email, and a durable record — in under three minutes.

## Before starting

1. Read `context/about-me.md` and `context/voice.md` — the follow-up email needs to sound like the user
2. Read `context/preferences.md` — how they want action items formatted, sign-off preferences
3. Ask the user to either paste their notes or describe what happened. Don't guess.
4. If there's a corresponding `meeting-prep-*.md` file for this meeting, read it. Compare: what did you predict vs. what happened?

## What to produce

Two outputs:

**1. A debrief file** saved to `/output/meeting-debrief-{YYYY-MM-DD}-{attendee-or-topic}.md` with five sections:
- **What happened** — 3–6 bullets summarizing the conversation. Factual.
- **Decisions made** — list them cleanly. One line each. (Feed these to the decision log over time.)
- **Action items** — for each: owner, what, deadline. Separate items owned by the user from items owned by others.
- **Open questions** — things that didn't get answered or got deferred.
- **What to do next** — the user's next move, specific.

**2. A follow-up email draft** — attached inline at the bottom of the debrief file under the heading `## Draft follow-up email`. Under 150 words unless the situation genuinely requires more. Matches the user's voice. Confirms action items with clear deadlines. Ends with a specific next step.

## Inputs

- The user's raw notes or verbal recap (required)
- The `meeting-prep-*.md` file for this meeting, if it exists
- Any relevant context from the project folder

## How it works

1. Parse the user's notes — separate facts from opinions from decisions
2. If a meeting-prep file exists, reference it: did the attendee bring up what you expected? Were there surprises?
3. Draft the five sections of the debrief
4. Draft the follow-up email in the user's voice (see `voice.md`). Keep it tight.
5. Save everything to the debrief file
6. Tell the user: "Debrief saved. Follow-up email is ready to review at the bottom — say the word and I'll send it." (Do not send without approval. See global instructions.)

## What not to do

- Do not over-write. If the meeting was 20 minutes, the debrief shouldn't read like an epic.
- Do not invent action items that weren't discussed. If the user's notes don't mention an action, don't add one.
- Do not send the follow-up email automatically, even if you've sent similar emails before. Show the draft, wait for approval.
- Do not skip the "open questions" section. What didn't get answered is often more valuable than what did.

## Example output structure

```markdown
# Meeting Debrief — 2026-04-18 — Sarah Chen (Northwind)

## What happened
- Sarah confirmed Q1 budget approval came through two weeks ago
- Walked through implementation timeline — she's targeting a 5/15 kickoff
- Talked about integration requirements — she'll send a list by Monday
- She asked about reference customers in her vertical — you said you'd follow up

## Decisions made
- Kickoff target: 2026-05-15
- SOW scope: standard implementation package + 3 custom integrations
- Legal review: mutual expedite, target close by 2026-04-25

## Action items
**You own:**
- Send SOW with kickoff date by EOD 2026-04-19
- Send two reference customer intros by 2026-04-22
- Loop in Alex on legal expedite — today

**She owns:**
- Send integration requirements doc by Monday 2026-04-21
- Introduce you to their CFO for legal sign-off — this week

## Open questions
- Is there a hard deadline on her side if legal slips past 4/25?
- Does she want the kickoff call with her full team or just her?

## What to do next
1. Draft SOW today, send tomorrow AM
2. Pull the two reference intros — recommend Morgan at Alpine and Priya at Relay

## Draft follow-up email

Subject: Northwind — next steps

Sarah,

Great to talk today. Quick recap to make sure we're aligned:

- **Kickoff:** targeting May 15
- **SOW:** sending by EOD tomorrow
- **References:** two intros headed your way Tuesday (Morgan at Alpine, Priya at Relay — both ran similar implementations)
- **Legal:** I'm looping Alex in today to expedite on our side

On your end: the integration requirements doc by Monday, and an intro to your CFO this week.

Let me know if I'm missing anything.

— [User's name]
```

## Customization notes

- **Internal meetings.** Skip the follow-up email section unless one is warranted. The debrief file is enough.
- **Interview / hiring meetings.** Add a "signal" section — what you learned about the candidate, gut-check rating. Save to a candidate-specific folder.
- **Board / investor meetings.** The debrief file itself becomes the record. Be extra careful with decisions — flag anything that commits the company, so the user can double-check.
- **Recurring 1-1s.** Keep debriefs in a single folder per person. Over time this becomes a relationship history.
