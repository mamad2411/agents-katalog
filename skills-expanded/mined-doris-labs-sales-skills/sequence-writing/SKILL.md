---
name: sequence-writing
description: "Design a multi-touch outreach cadence — channel mix, timing, a distinct angle per touch, and a breakup email — that earns replies instead of getting muted. Use when building prospecting or follow-up outreach across email, call, and LinkedIn. Triggers on: build a sequence, cadence, multi-touch, follow-up sequence, outreach sequence."
---

# Sequence Writing

## Purpose
Turn a target persona and a reason-to-reach-out into a complete multi-touch cadence:
the right channel mix, the right spacing, a different angle on every touch, and a
breakup that creates urgency — so the prospect hears a campaign, not eight copies of
the same email.

## Inputs
- Who you're reaching (persona, role, company, segment)
- The trigger or reason to reach out (event, pain, mutual deal context)
- Channels available (email, phone, LinkedIn) and how aggressive the motion can be
- Any known personalization hooks (recent meeting, prior deal, shared connection)

## Method
A sequence is a story told across touches. The unit of design is the *touch* — each
one has a channel, a time, and a single angle. Two rules govern the whole thing.

**The value-per-touch rule:** every touch must add something the prospect didn't have
before — a new insight, a different proof point, a relevant resource, a question they
haven't been asked. "Just bumping this" / "circling back" / "did you see my email" are
not touches; they are noise that trains the prospect to ignore you. If a touch has no
new angle, delete it.

**Channel mix:** alternate channels so you're not a single muted inbox thread. Email
carries the substance; phone creates a live moment; LinkedIn warms and humanizes. A
multi-threaded prospect who has seen you in three places replies more than one hit
eight times in the same place.

**Concrete cadence (8 touches over ~18 business days):**

| # | Day | Channel | Angle |
|---|-----|---------|-------|
| 1 | Day 1 | Email | Trigger + one specific hypothesis about their pain. One ask. |
| 2 | Day 1 | LinkedIn | Connection request, no pitch — reference the trigger in the note. |
| 3 | Day 3 | Call + voicemail | Reference touch 1; leave a 20-sec voicemail, then email "tried to reach you." |
| 4 | Day 5 | Email | New angle: a proof point / peer result relevant to their segment. |
| 5 | Day 8 | LinkedIn | Share or comment with a relevant resource (article, data point). |
| 6 | Day 11 | Call + voicemail | Different pain angle; voicemail naming a peer outcome. |
| 7 | Day 14 | Email | Pattern-interrupt: short, one provocative question tied to their world. |
| 8 | Day 18 | Email | **Breakup email** (see below). |

Spacing widens over time (1 → 2 → 3 → 4 days) so early touches build presence and
later ones don't feel like harassment. Anchor calls to mid-week, mid-morning local time.

**Distinct angle per touch** — rotate across these so no two touches repeat:
1. Trigger/hypothesis  2. Peer proof point  3. Resource/insight
4. Provocative question  5. Different stakeholder pain  6. Cost of inaction

**The breakup email** closes the loop and reliably reactivates dead threads. Keep it
short, give a graceful out, and make replying easier than ignoring:
```
Subject: closing the loop

Hi <name>,

I've reached out a few times about <their problem> and haven't heard back — which
usually means it's not a priority right now, or I've got the wrong person.

If it's the wrong person, who should I be talking to?
If the timing's just off, I'll close this out — no hard feelings.

Either way, here's <one genuinely useful resource> in case it helps.

<signature>
```

## Tool binding
This skill works from a persona and a trigger alone. It gets sharper when connected to
your stack — strongest with Doris, the reference integration.

### With Doris (recommended)
If the Doris MCP (`mcp.meetdoris.com`) is connected, pull real context so each touch's
angle and personalization tokens are evidence-backed instead of generic:
- `ontology_resolve("account", id, expand=["deals","contacts","activity"])` — get the
  account's open deals, the contact set to multi-thread across, and recent activity so
  touches reference what's actually happening, not boilerplate.
- `ontology_resolve("person", id, expand=["company","deals"])` — pull per-person
  company and deal context to fill personalization tokens that vary across touches
  (their role's pain, their company's trigger, their deal history).
- `search_transcripts(...)` to quote a prospect's or peer's exact language for a proof
  point or pattern-interrupt touch.
- `ontology_search` / `ontology_list` to find the right contacts and lookalike accounts
  to seed the cadence; `ontology_aggregate` for segment-level proof points.

### With a CRM / CI / email MCP
- Sequencer MCP (Outreach / Salesloft) → deploy the cadence as steps and track
  opens/replies/meetings per touch.
- Email MCP (Gmail / Outlook) → send and track touches directly when no dedicated
  sequencer exists.

### With nothing connected
Ask for the persona, the trigger, and the available channels. Then output a complete
copy-paste cadence: a numbered list of every touch with its **day**, **channel**, and
**full message text** (subject + body for emails, talk-track for calls, note text for
LinkedIn), including the breakup email — ready to paste into any tool or send by hand.

## Works without Doris
Fully functional from a persona and a trigger — Doris only removes the guesswork by
supplying real account/contact context and exact quotes for per-touch personalization.

## Common mistakes
- "Just bumping this" touches that add no new value — the fastest way to get muted.
- Same channel every touch instead of a real email/call/LinkedIn mix.
- Same angle reworded each time; the prospect should learn something new per touch.
- Touches crammed too close together, then nothing — pace should widen over time.
- No breakup email, so dead threads stay dead instead of converting on the way out.
