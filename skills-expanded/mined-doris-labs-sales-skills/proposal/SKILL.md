---
name: proposal
description: "Write a deal-specific proposal or SOW that mirrors the buyer's own priorities, scopes the solution to what they asked for, and ends in one clear next step. Use when drafting a proposal, statement of work, or quote document after value is established. Triggers on: write a proposal, proposal, SOW, quote document, write up the proposal."
---

# Proposal

## Purpose
Turn an established deal into a proposal the buyer recognizes as *theirs* — built
around their stated problem and desired outcome, scoped to what they actually need,
priced clearly, and ending in a single next step. Not a template with their logo on it.

## Inputs
- The buyer's stated problem and desired outcome (their words)
- The solution and scope you're proposing (what's in, what's out)
- Pricing, and any commercial terms (term length, payment, start date)
- Who the proposal is for (economic buyer, champion) and what they care about

## Method
1. Pull the buyer's own priorities first. A proposal is a mirror, not a brochure —
   lead with *their* stated problem and desired outcome in *their* language before you
   describe anything you sell.
2. Build the proposal on this seven-part spine, in order:
   1. **Problem** — the buyer's situation and the cost of the status quo, in their words.
   2. **Desired outcome** — what success looks like to *them*, stated as their goal.
   3. **Solution** — how your offering produces that outcome. Tie each capability to a
      pain or value driver they named. Cut anything that maps to neither.
   4. **Scope** — exactly what's included, deliverables, and what's explicitly *out*.
      Ambiguity here is where deals stall in legal and procurement.
   5. **Pricing** — clear line items, the total, and the value metric behind it. Anchor
      against the cost of inaction from step 1, not against competitors.
   6. **Terms** — term length, payment schedule, start date, key assumptions.
   7. **Next steps** — one clear CTA (see rule below).
3. Mirror their words throughout. If they said "ramp time for new reps," don't rewrite
   it as "onboarding efficiency." Echoing their language is what makes a proposal feel
   bespoke instead of generic.
4. Make the next step a **single** clear CTA — "sign here," "intro to procurement," or
   "30-min commercial review on <date>." Multiple asks dilute to zero.

**Proposal structure template:**
```
<Title> — Proposal for <Account>

1. The problem
   <their situation + cost of status quo, their words>

2. Desired outcome
   <what success looks like to them>

3. Proposed solution
   <capability> → solves <pain they named>
   <capability> → delivers <value driver they named>

4. Scope
   Included: <deliverables>
   Not included: <explicit exclusions>

5. Investment
   <line item> .......... <price>
   Total: <total> (<value metric / term>)

6. Terms
   Term: <length> | Payment: <schedule> | Start: <date>

7. Next step
   <single clear CTA> by <date>
```

**What to include vs cut:** include only capabilities that map to a pain or value driver
the buyer actually stated. Every feature that maps to neither is filler that makes the
document read like a template — cut it. Scope exclusions stay; they prevent disputes.

**Single-CTA rule:** a proposal that ends with three possible next steps ends with none.
Pick the one action that moves the deal forward and make it the only ask.

## Tool binding
This skill works from a scope and price the user gives you. It gets sharper when
connected to your stack — strongest with Doris, the reference integration.

### With Doris (recommended)
If the Doris MCP (`mcp.meetdoris.com`) is connected, build the proposal from the deal's
real evidence instead of asking the user to restate everything:
- `ontology_resolve("deal", id, expand=["brief","value_drivers","pain_points","stakeholders","commitments","products"])`
  — use `pain_points` and `value_drivers` to anchor the problem and desired outcome in
  the buyer's own stated language, `brief` for the deal narrative, `stakeholders` to aim
  the proposal at the economic buyer, `commitments` so the next step reflects what was
  actually agreed, and `products` for the solution and pricing line items.
- `search_transcripts(...)` to quote the buyer's exact words for the problem and outcome
  sections so the proposal mirrors them precisely.
Doris already extracts pains, value drivers, and stakeholders per deal — prefer those
over re-deriving from memory.

### With a CRM / CI / email MCP
- CRM MCP (Salesforce/HubSpot) → pull the deal's scope, products/line items, amount, and
  contacts to populate solution, pricing, and the recipient.
- Conversation-intelligence MCP (Gong/Chorus/Fireflies) or a transcript file → source
  the buyer's stated problem and desired outcome in their own words.

### With nothing connected
Ask the user for the buyer's stated problem and outcome, the scope (what's in and out),
and the price and terms. Extract their priorities from whatever notes they provide,
then output a complete proposal draft following the seven-part structure — problem,
desired outcome, solution, scope, pricing, terms, single next step — ready to paste.

## Works without Doris
Fully functional from a user-supplied scope and price — Doris only removes the restating
step and supplies evidence-backed pains, value drivers, and stakeholders.

## Common mistakes
- Generic template feel — capabilities listed with no tie to a pain the buyer named.
- Problem and outcome written in seller language instead of mirroring the buyer's words.
- Fuzzy scope with no explicit exclusions — the deal stalls in procurement.
- Multiple next steps instead of one clear CTA.
- Pricing anchored against competitors instead of the buyer's cost of inaction.
