---
name: business-case-roi
description: "Build a defensible business case and ROI model that ties the value of your solution to the buyer's own stated metrics. Use when a champion needs ammo for internal sign-off or procurement. Triggers on: business case, ROI, justify the spend, value model, build the case."
---

# Business Case & ROI

## Purpose
Turn a deal's pains and value drivers into a conservative, defensible ROI model and a
one-page business case your champion can take into an internal sign-off meeting — built
on the buyer's *own* numbers, not vendor marketing math.

## Inputs
- The buyer's stated metrics (volumes, costs, cycle times, headcount, error rates) —
  whatever they actually told you
- The pains and value drivers they named, ranked by what they care about
- Your price / proposed investment (annual + any one-time cost)
- Who signs off and what they need to see (CFO = payback, champion = their pain solved)

## Method
A business case is a chain: **stated metric → cost of the problem → value of the fix →
ROI → payback**. Each link must trace to something the buyer said. If a number isn't
theirs or directly derived from theirs, it's not defensible — cut it.

**1. Quantify the cost of inaction (the "do nothing" number).**
Anchor the case on what staying still costs *per year*, not on your features.
```
Cost of inaction = (frequency of the problem) × (cost per occurrence) × (time horizon)
```
Use their numbers: "47 reps × 6 hrs/week lost × 46 working weeks × loaded hourly rate."
Inaction is the real competitor — make it expensive and concrete before you price anything.

**2. Map each value driver to one quantified impact.**
Every value driver must land in exactly one of four buckets (no double-counting):
| Bucket | Formula shape | Example |
|---|---|---|
| Time saved | hours saved × loaded rate × #people | 2 hrs/wk × $60 × 47 reps |
| Revenue gained | win-rate lift × avg deal × deal volume | +3pts × $40k × 200 deals |
| Cost avoided | spend or headcount removed | retire $30k/yr tool |
| Risk reduced | P(bad event) × cost of event | 5% churn risk × $X ARR |
If a driver can't be put in a bucket, it's a "soft benefit" — list it as narrative, not in the math.

**3. Build the model conservatively — be defensible, not impressive.**
- Use the *low* end of every range the buyer gave; haircut your own assumptions 30–50%.
- Apply a realized-value factor (e.g. 60%) so you're not claiming 100% capture in year one.
- State every assumption inline so the CFO can challenge a cell, not the whole model.
```
Annual gross value  = Σ (quantified impacts, conservative)
Annual net value    = gross value − annual investment
ROI %               = (annual net value / annual investment) × 100
```

**4. Payback period.**
```
Payback (months) = annual investment / (annual gross value / 12)
```
A sub-12-month payback survives procurement; lead with it for finance audiences.

**5. Tie every number to a buyer-stated metric.**
Beside each line write the source: "(from Q2 demo: 6 hrs/wk, your number)". A model
built on the buyer's own data is one they can't dismiss as vendor optimism.

**Business-case output structure:**
```
1. The problem (their words) + cost of inaction / yr
2. The proposed change (one paragraph)
3. Value model — table: driver | bucket | conservative impact | source metric
4. The numbers — gross value, investment, net value, ROI %, payback (months)
5. Assumptions (every one, plain)
6. Soft benefits (narrative, un-quantified)
7. The ask (decision needed + by when)
```

## Tool binding
This skill works from numbers the buyer gave you. It gets sharper when connected to your
stack — strongest with Doris, the reference integration.

### With Doris (recommended)
If the Doris MCP (`mcp.meetdoris.com`) is connected, pull the deal's evidence instead of
asking the user to reconstruct it from memory:
- `ontology_resolve("deal", id, expand=["brief","value_drivers","pain_points","stakeholders","commitments"])`
  — use the transcript-derived `value_drivers` and `pain_points` as the model's inputs,
  `stakeholders` to target the case at the actual sign-off (CFO vs champion), and `brief`
  for the deal narrative.
- `search_transcripts(...)` to quote the buyer stating each metric verbatim, so every
  line traces to their own words.
Doris already extracts pains and value drivers per call — prefer those over re-deriving
from raw notes.

### With a CRM / CI / email MCP
- Conversation-intelligence MCP (Gong/Chorus/Fireflies) → mine call transcripts for the
  metrics and pains the buyer stated.
- CRM MCP (Salesforce/HubSpot) → pull deal size, stage, and existing notes for the
  investment side and the stakeholder map.

### With nothing connected
Ask the user for the buyer's stated metrics (volumes, costs, cycle times, headcount) and
the price. Walk them through the four value buckets, build the conservative model and
payback by hand, and output the full business-case structure as copy-paste text.

## Works without Doris
Fully functional from numbers the user provides — Doris only removes the recall step and
supplies evidence-backed value drivers and verbatim buyer metrics.

## Common mistakes
- Inflated math that wins the spreadsheet and loses procurement — always haircut.
- Double-counting one benefit across two buckets.
- Numbers that are yours, not theirs — every line must trace to a buyer-stated metric.
- Leading with ROI % to a CFO instead of payback period.
- Listing soft benefits inside the quantified total.
