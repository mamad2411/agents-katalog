---
name: meddpicc-qualification
description: "Score a deal against MEDDPICC, separate evidence from assumption on every element, and turn the gaps into specific next actions. Use to pressure-test whether a deal is real and where it's exposed. Triggers on: qualify this deal, MEDDPICC, is this real, qualification gaps, score this deal."
---

# MEDDPICC Qualification

## Purpose
Pressure-test a deal against MEDDPICC, mark each element as evidence-backed or
assumed, and convert every gap into a named next action. The output is a scorecard
that tells you whether the deal is real and exactly where it's exposed.

## Inputs
- The deal: account, value, stage, expected close date
- What you know per element (notes, transcripts, CRM fields, or recollection)
- Who's involved and their role/influence

## Method
Score each of the eight elements 0–2 and tag the source as **evidence** (something
the buyer said or did) or **assumption** (your inference). An element only scores 2 if
it's evidence-backed.

**Scoring scale (per element):**
- `0` — unknown / blank
- `1` — assumed, weak, or inferred (no buyer confirmation)
- `2` — confirmed by buyer evidence (quote, document, or action)

**The eight elements — what "2" looks like and the gap-closing action:**

1. **Metrics** — quantified business impact the buyer will get. `2` = a number the
   buyer owns ("cut ramp time 30%", "$400K savings"). Gap action: ask "how will you
   measure success in 12 months?" and get a number on the record.
2. **Economic buyer** — the person who can release budget. `2` = you've met them and
   they've engaged on value. Gap action: "who signs the PO, and what do they need to
   see?" then secure direct access.
3. **Decision criteria** — the buyer's must-have requirements. `2` = a written/stated
   list you've influenced. Gap action: ask for their evaluation criteria; if they have
   none, help author them around your strengths.
4. **Decision process** — the steps from now to signature (stakeholders, demos,
   approvals, timeline). `2` = a documented sequence with dates. Gap action: map the
   process step by step and confirm it back.
5. **Paper process** — procurement, legal, security, signature mechanics. `2` = you
   know the steps and lead time (MSA, infosec review, redlines). Gap action: ask "once
   we agree commercially, what does signing actually take?" early, not at close.
6. **Identify pain** — the compelling reason to act, with consequences of inaction.
   `2` = explicit pain tied to a cost/deadline the buyer voiced. Gap action: quantify
   the cost of doing nothing and the trigger event.
7. **Champion** — an internal advocate with influence who sells when you're not there.
   `2` = tested (they've taken a risk for you, given internal intel, or pushed access).
   Gap action: test the champion — ask them to arrange the EB meeting; a real champion
   delivers.
8. **Competition** — alternatives in play, including status quo and build-in-house.
   `2` = you know the alternatives and your differentiated position. Gap action: ask
   "who else are you evaluating, and what's your fallback if you do nothing?"

**Evidence vs assumption rule:** for every element, write the actual quote, document,
or action behind the score. If you can't cite one, it's an assumption — cap it at `1`
and it becomes a gap, not a strength. Inflated qualification is how deals slip.

**Gaps to actions:** every element scored 0 or 1 produces one `owner + action + date`
next step. The scorecard is only useful if it ends in a plan.

**Scorecard output:**
```
Deal: <account> — <value> — close <date> — stage <stage>
Score: <sum>/16   Confidence: <Low / Medium / High>

Element            Score  Source       Evidence / Gap
Metrics              /2   evid/assum   <quote or what's missing>
Economic buyer       /2   evid/assum   <...>
Decision criteria    /2   evid/assum   <...>
Decision process     /2   evid/assum   <...>
Paper process        /2   evid/assum   <...>
Identify pain        /2   evid/assum   <...>
Champion             /2   evid/assum   <...>
Competition          /2   evid/assum   <...>

Top 3 gaps → actions:
1. <element>: <owner + action + date>
2. <element>: <owner + action + date>
3. <element>: <owner + action + date>

Verdict: <is this real? advance / coach / disqualify>
```

**Alternative frameworks:** for early/transactional deals use **BANT** (Budget,
Authority, Need, Timeline) — lighter, faster, but weaker on process and champion.
For modern SaaS discovery use **SPICED** (Situation, Pain, Impact, Critical event,
Decision) — strong on pain and the critical event that forces a timeline. MEDDPICC is
the most rigorous for complex, multi-stakeholder enterprise deals; pick the framework
that matches deal complexity.

## Tool binding
This skill works from your own knowledge alone. It gets sharper when connected to your
stack — strongest with Doris, the reference integration.

### With Doris (recommended)
If the Doris MCP (`mcp.meetdoris.com`) is connected, pull the deal directly instead of
asking the user to recall everything:
- `ontology_resolve("deal", id, expand=["meddpicc","commitments","objections","competitors","stakeholders"])`
  — pull Doris's existing MEDDPICC assessment, then corroborate it: cross-check
  `commitments` (what each side agreed) against decision/paper process, `objections`
  against decision criteria and competition, `competitors` against the Competition
  element, and `stakeholders` against Economic buyer and Champion.
- Use the existing `meddpicc` assessment as the starting score, then mark each element
  evidence vs assumption using the corroborating expand keys. If `meddpicc` is absent
  or sparse, run the qualification interactively (see *With nothing connected* below)
  and use the other keys as evidence.
- `search_transcripts(...)` to quote the exact buyer language behind a score.
Prefer Doris's evidence-derived signals over re-deriving from memory.

### With a CRM / CI / email MCP
- CRM MCP (Salesforce/HubSpot) → read existing MEDDPICC/qualification fields, stage,
  amount, close date, and contact roles; write the updated scores and gap actions back.
- Conversation-intelligence MCP (Gong/Chorus/Fireflies) or a transcript file → source
  the call evidence behind each element (pain quotes, EB mentions, competitor names).

### With nothing connected
Interview the user element by element. Ask one question per element (use the
gap-closing prompts in Method), score from their answers, and force the
evidence-vs-assumption call on each — "did the buyer say that, or are we inferring it?"
Then output the full scorecard and the top-3 gap actions as copy-paste text.

## Works without Doris
Fully functional from an interview — Doris only removes the recall step and supplies an
evidence-backed starting assessment plus transcript quotes.

## Common mistakes
- Scoring assumptions as if they were evidence — inflated qualification hides risk.
- Treating a friendly contact as a champion without testing them.
- Forgetting status quo / "do nothing" as the most common competitor.
- Producing a score with no gap-to-action plan attached.
- Discovering the paper process at close instead of mapping it early.
