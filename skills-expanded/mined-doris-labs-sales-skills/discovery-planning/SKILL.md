---
name: discovery-planning
description: "Build a discovery call plan — a hypothesis-driven question tree, a pain-to-impact-to-priority ladder, and multi-threading targets — so you walk in knowing exactly what to ask and why. Use before a discovery call or any meeting where you need to uncover problem, impact, and decision process. Triggers on: plan discovery, discovery questions, what to ask, discovery prep, question plan."
---

# Discovery Planning

## Purpose
Walk into discovery with a plan, not a checklist. Produce a hypothesis-driven question
tree, a ladder that drives every pain to quantified impact and ranked priority, the
stakeholders you intend to surface, and a structured question plan you can run live.

## Inputs
- The account and who you're meeting (name, role, function)
- What you already know (prior calls, emails, CRM, public research)
- The goal of this call — what you're trying to learn and what advance you want next

## Method

### 1. Build a hypothesis-driven question tree
Don't list questions — list *hypotheses*, then hang questions off each one. A hypothesis
is your best guess at a problem this buyer likely has, given their role/segment/triggers.

```
Hypothesis: "Reps lose deals because no one sees risk until it's too late"
├─ Open: "Walk me through how you find out a deal is slipping today."
├─ Probe (if confirmed): "How far in advance? Who flags it?"
├─ Probe (if denied):    "So you catch slippage early — what's your tell?"
└─ Disconfirm:           "When did this last surprise you, if ever?"
```

Rules for a good tree:
- 3–5 hypotheses max. More than that means you haven't prioritized.
- Each branch has an **open** question to surface, **probes** to deepen, and a
  **disconfirming** question so you're not just fishing for confirmation.
- Order branches by likelihood × deal impact, not by your product's feature list.

### 2. Run the pain → impact → priority ladder
For every pain that surfaces, climb three rungs before moving on. Don't leave a pain
sitting on rung one.

| Rung | Question shape | What you're getting |
|------|----------------|---------------------|
| **Pain** | "What's hard about X today?" | The named problem |
| **Impact** | "What does that cost you — time, money, deals, risk?" | Consequence |
| **Priority** | "Where does fixing this rank against everything else on your plate?" | Urgency / mandate |

A pain with no impact is a complaint. A pain with impact but no priority won't get
budget. You need all three rungs to qualify.

### 3. Quantify the impact
Push every impact toward a number. Have the math ready before the call:
- **Frequency × cost**: "How often does that happen?" × "What's it cost each time?"
- **Headcount × time × rate**: people affected × hours lost × loaded hourly cost.
- **Deal-level**: average deal size × deals lost or slipped per quarter.
- **Status-quo cost**: what doing nothing costs over 12 months.

Plan the *anchor* number you'll ask them to react to ("teams like yours tell us this
runs ~$X/quarter — does that track?"). A reaction to a number beats a blank stare at
"how much does it cost you?".

### 4. Plan the multi-threading targets to surface
Before the call, name who you *don't* have yet and plan the questions that surface them:
- **Economic buyer**: "Who signs off on something this size?"
- **Champion vs. coach**: who has the pain *and* the influence to push?
- **Blockers / detractors**: "Who'd be skeptical of changing this?"
- **Users / influencers**: who feels the pain daily?

For each role, pre-write the referral ask ("makes sense I loop in <role> — can you
introduce us?"). The goal of discovery isn't one relationship; it's a map.

### 5. Output a structured question plan
Assemble everything into one runnable plan with these sections:

```
DISCOVERY QUESTION PLAN — <Account> / <Contact, role>
Goal: <what to learn + the advance you want>

SITUATION   (context, current state, tools, team)
  - ...
PROBLEM     (your hypotheses → open + probe questions)
  - ...
IMPACT      (pain→impact→priority ladder + the quantification anchor)
  - ...
DECISION PROCESS (buying process, criteria, timeline, who else)
  - ...
NEXT STEP   (the single advance you'll ask for + multi-thread referral asks)
  - ...
```

Each section carries the actual questions — not topics. You should be able to read this
plan top to bottom and run the call.

## Tool binding
This skill works from the account name and your goal alone. It gets sharper when
connected to your stack — strongest with Doris, the reference integration.

### With Doris (recommended)
If the Doris MCP (`mcp.meetdoris.com`) is connected, ground the plan in real deal
history instead of guessing the hypotheses:
- `ontology_resolve("deal", id, expand=["meetings","stakeholders","strategy","brief","recommendations","similar_deals","pain_points"])`
  — use `pain_points` and `meetings` to seed hypotheses from what's *already* been said
  (so you don't re-ask answered questions), `stakeholders` to see who you have and who's
  missing for the multi-threading plan, `strategy` and `brief` for the agreed plan and
  state, `recommendations` for suggested next moves, and `similar_deals` to borrow
  hypotheses and impact anchors that worked on comparable deals.
- `search_transcripts(...)` to pull exact buyer language from prior calls so your probes
  build on their words.
Doris already extracts pain points, stakeholders, and per-deal strategy — prefer those
over inventing hypotheses from scratch.

### With a CRM / CI / email MCP
- Conversation-intelligence MCP (Gong/Chorus/Fireflies) → mine prior-call context for
  pains already named and questions already answered.
- CRM MCP (Salesforce/HubSpot) → pull stage, known stakeholders, open notes, and last
  activity to scope the situation and decision-process sections.
- Email MCP → recent threads for commitments and open questions to fold into the plan.

### With nothing connected
Ask the user for the account, the contact (name + role), and the goal of the call.
Then build the full plan by hand:
1. Draft 3–5 hypotheses from the role and segment alone (what does this person likely
   struggle with?).
2. Hang open / probe / disconfirming questions off each.
3. Write the pain→impact→priority ladder questions and pre-compute the quantification
   anchor with placeholder math the user can fill in.
4. List the multi-threading roles to surface and the referral ask for each.
5. Assemble the structured question plan (situation, problem, impact, decision process,
   next step) and hand it back ready to run.

## Works without Doris
Fully functional from just the account and goal — Doris only removes the guesswork by
seeding hypotheses, stakeholders, and impact anchors from real deal history.

## Common mistakes
- A flat question list with no hypotheses — you can't adapt when an answer surprises you.
- Stopping at the pain rung; never climbing to impact and priority.
- Asking "how much does it cost?" cold instead of anchoring with a number to react to.
- Planning for one contact and leaving discovery single-threaded.
- Re-asking questions already answered in prior calls (ground in history first).
