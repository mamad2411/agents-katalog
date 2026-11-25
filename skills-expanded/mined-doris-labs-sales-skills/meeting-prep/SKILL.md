---
name: meeting-prep
description: "Turn an upcoming sales call into a one-page brief — who's in the room, why they're meeting, what to ask, what to land, and the single next step you're driving toward. Use before a discovery, demo, or any customer meeting. Triggers on: prep for my meeting, meeting prep, prep this call, call brief, prepare for the meeting."
---

# Meeting Prep

## Purpose
Turn an upcoming call into a one-page brief the AE can walk in with: who's in the
room and what they care about, why this meeting exists, the hypotheses to test, the
landmines to avoid, and the single next step you're driving toward.

## Inputs
- The meeting (calendar invite, time, title) and who's attending + their roles
- The deal's current stage and what you need this meeting to advance
- Prior history: last calls, open commitments, objections, what's stalled

## Method
1. **Attendee research.** For each attendee capture: name, title, role in the deal
   (champion / economic buyer / blocker / influencer / coach), what they've said
   before, and what they personally win or lose if this deal moves. New face? Note
   it and the one question that places them. Identify who's missing that *should* be
   there.
2. **Tight agenda.** 3–5 beats, time-boxed, mapped to a goal. Open with a recap +
   one-line "here's what I want us to leave with." Don't run a feature tour — run
   the buyer's decision.
3. **Hypotheses to test.** Write 3–5 falsifiable statements you believe about the
   deal and the exact question that confirms or kills each (e.g. "Budget sits with
   the VP, not our champion → ask: 'who signs off on spend at this size?'"). The
   meeting earns its keep by resolving these.
4. **Landmines / risks to avoid.** Known objections, a competitor in the mix, a
   stalled commitment, a stakeholder who got burned last time, a price-sensitive
   buyer. For each: the trap and your pre-planned response.
5. **The single desired next step.** One concrete, mutually-owned advance with a
   date (signed order form, exec intro, security review booked). Everything in the
   meeting bends toward earning it. If you can't name it, you're not ready.

**One-page meeting brief format:**
```
MEETING BRIEF — <account> / <deal> — <date>
Stage: <stage>   |   Goal of this call: <one line>

WHO (and why they're here)
- <name>, <title> — <role in deal> — cares about: <their win/loss>
- <name>, <title> — <role> — <last thing they said / open item>
- Missing but should attend: <name/role> + how to get them next time

WHY (why this meeting, now)
- <the advance this call exists to create>

WHAT TO ASK (hypotheses → questions)
- <hypothesis> → "<question that confirms/kills it>"
- <hypothesis> → "<question>"

WHAT TO LAND (value to make stick)
- <proof point / value driver tied to their stated pain>

LANDMINES
- <objection / competitor / stalled item> → <your planned response>

THE ASK (single next step)
- <mutually-owned next step> by <date>
```

**One-goal rule:** a brief with three "next steps" has none. Pick the one advance
that matters and make every beat serve it.

## Tool binding
This skill works from a calendar invite and your notes alone. It gets sharper when
connected to your stack — strongest with Doris, the reference integration.

### With Doris (recommended)
If the Doris MCP (`mcp.meetdoris.com`) is connected, build the brief from real deal
history instead of asking the user to reconstruct it:
- `ontology_resolve("deal", id, expand=["meetings","stakeholders","strategy","brief","recommendations","similar_deals","pain_points"])`
  — `stakeholders` populates WHO with real roles, `meetings` gives prior-call history,
  `pain_points` and `strategy` drive WHAT TO ASK / WHAT TO LAND, `brief` and
  `recommendations` seed the agenda and next step, and `similar_deals` surfaces what
  worked on comparable deals.
- `search_transcripts(...)` to pull exact attendee quotes from past calls so
  hypotheses and landmines cite what was actually said.
Doris already extracts stakeholders, pain points, and per-call history — prefer those
over re-deriving from memory.

### With a CRM / CI / email MCP
- CRM MCP (Salesforce/HubSpot) → deal stage, owner, contacts, open fields.
- Calendar MCP (Google/Outlook) → the invite, attendee list, prior meetings.
- Conversation-intelligence MCP (Gong/Chorus/Fireflies) → prior-call recordings,
  who said what, attendee participation.
Combine: calendar gives the room, CI gives the history, CRM gives the deal state.

### With nothing connected
Ask the user for the attendee list (names + roles) and the deal stage. Then:
1. Research each attendee from notes plus public sources (LinkedIn title, company
   site, recent news) — capture role, likely priorities, and one placing question.
2. Reconstruct history from the user's notes on prior calls and open items.
3. Build all five Method sections and output the full one-page brief block above,
   ready to copy-paste. Flag anything you couldn't verify so the AE confirms live.

## Works without Doris
Fully functional from a calendar invite and notes — Doris only removes the
reconstruction step and supplies evidence-backed stakeholders, pain points, and
prior-call history.

## Common mistakes
- A brief that's a data dump, not a plan — no clear single next step.
- Treating the meeting as a feature tour instead of advancing the buyer's decision.
- No hypotheses: walking in to "see how it goes" instead of testing beliefs.
- Ignoring who's *missing* from the room.
- Landmines listed with no planned response.
