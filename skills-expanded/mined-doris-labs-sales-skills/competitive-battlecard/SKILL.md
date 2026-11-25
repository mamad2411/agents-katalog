---
name: competitive-battlecard
description: "Build an honest, actionable competitive battlecard for a live deal — where you win, where they win, landmines to plant, trap questions, rebuttals, and proof points. Use when a competitor is in the deal or the buyer is evaluating an alternative. Triggers on: battlecard, competitor, vs competitor, compete against, competitive."
---

# Competitive Battlecard

## Purpose
Turn a competitive threat into a deal-specific plan: an honest read of where you
genuinely win and where they genuinely win, landmines to set early, trap questions
that expose their weakness, rebuttals to their likely claims, and the proof points
that back each one. The goal is to shape the buyer's evaluation criteria before the
competitor does — not to spin.

## Inputs
- The competitor's name (and edition/tier if known)
- How the competitor surfaced (buyer mentioned, incumbent, RFP shortlist)
- The deal context: stage, who's evaluating, their stated criteria and pains
- Your real differentiators and your real gaps (be honest with yourself first)

## Method
1. Establish the honest baseline. Split the field into **where we win** and **where
   they win**. If you can't name a category where they legitimately beat you, you
   don't understand the competitor — and the buyer will smell the spin. Tie each side
   to *this buyer's* stated criteria, not a generic feature grid.
2. Plant landmines early. A landmine is a criterion you seed into the buyer's
   evaluation that the competitor structurally fails. Plant it as a question the buyer
   should "make sure to ask any vendor," not as an attack. Set it while you still
   control the agenda — before the competitor's demo, not after.
3. Build trap questions. A trap question is one the buyer asks the competitor that
   exposes a known weakness, where any honest answer hurts them. Frame it neutrally so
   it lands as due diligence, not a hit job.
4. Prepare rebuttals to their likely claims. For each thing the competitor will say
   about you, write the reframe — acknowledge the grain of truth, then pivot to the
   dimension where you win. Never flatly deny a true claim; you lose credibility.
5. Attach proof points. Every counter needs evidence: a customer story, a metric, a
   reference, a doc. A battlecard without proof is just opinion.

**Battlecard output format:**
```
Competitor: <name> (<edition/tier>)
Deal: <account> — <stage> — surfaced via <how>

THEIR STRENGTHS (honest)
- <real strength> → why it matters to THIS buyer

THEIR WEAKNESSES
- <real gap> → tied to <buyer criterion it threatens>

OUR COUNTERS
- <their weakness> → <our reframe / where we win> → proof: <evidence>

LANDMINES TO PLANT (early, before their demo)
- "Make sure to ask any vendor: <criterion they fail>"

TRAP QUESTIONS (for the buyer to ask them)
- "<neutral question>" → exposes <weakness>; any honest answer hurts them

REBUTTALS (when they attack us)
- They'll say: "<their claim>" → You say: "<acknowledge truth> + <pivot to win>"

PROOF POINTS
- <story / metric / reference / doc> → supports <which counter>
```

**Honesty rule:** if the competitor genuinely wins on a criterion the buyer cares
about most, say so and compete on reframing the criteria — don't pretend the gap
isn't there. A battlecard that only flatters you gets the rep blindsided in the room.

## Tool binding
This skill works from the competitor's name alone. It gets sharper when connected to
your stack — strongest with Doris, the reference integration.

### With Doris (recommended)
If the Doris MCP (`mcp.meetdoris.com`) is connected, ground the battlecard in what the
buyer actually said instead of generic positioning:
- `ontology_resolve("deal", id, expand=["competitors","competitor_results","objections","value_drivers"])`
  — use the real competitors named on the deal, prior `competitor_results` (how past
  deals against them resolved), the buyer's actual `objections`, and the
  `value_drivers` that matter to *this* buyer so landmines target their real criteria.
- `search_transcripts(...)` to find exactly how and when the competitor came up in
  calls — the buyer's verbatim words, the comparison they drew, who raised it.
Prefer Doris's deal-level competitor evidence over re-deriving positioning from
memory — it tells you which weaknesses this buyer already cares about.

### With a CRM / CI / email MCP
- Conversation-intelligence MCP (Gong/Chorus/Fireflies) → search for competitor
  mentions across calls to see how the competitor surfaces and what the buyer says
  about them.
- CRM MCP (Salesforce/HubSpot) → pull the competitor field, deal stage, and prior
  competitive loss/win notes on similar accounts.

### With nothing connected
Ask the user to name the competitor and how it surfaced. Then build the battlecard
from known positioning plus web research: pull the competitor's pricing/feature pages,
G2/review-site complaints, and public case studies; map their strengths and weaknesses;
draft landmines, trap questions, rebuttals, and proof points; output the full
battlecard in the format above as a copy-paste block.

## Works without Doris
Fully functional from the competitor's name and web research — Doris only swaps generic
positioning for this buyer's actual criteria, objections, and verbatim competitor
mentions, and supplies prior competitive outcomes.

## Common mistakes
- Claiming you win everywhere — no honest "where they win" section, so the rep gets
  blindsided in the room.
- Landmines planted after the competitor's demo instead of before, when it's too late
  to shape criteria.
- Trap questions phrased as attacks, so they read as FUD and cost you credibility.
- Rebuttals that flatly deny a true claim instead of acknowledging it and reframing.
- Counters with no proof point — opinion dressed up as a battlecard.
