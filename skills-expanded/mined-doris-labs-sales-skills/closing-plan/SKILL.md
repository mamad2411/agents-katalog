---
name: closing-plan
description: "Build a step-by-step path to signature for a live deal — mapping every gate, owner, and date between now and a signed contract. Use when a deal needs a close plan or you're driving toward a signing date. Triggers on: close plan, how do I close, path to close, get this signed, closing steps."
---

# Closing Plan

## Purpose
Turn a "we want to move forward" into a dated, owned, gate-by-gate plan that gets the
contract signed by a real date — surfacing procurement, legal, and security blockers
early instead of in the final week.

## Inputs
- The target close date (the buyer's, not your forecast wish)
- The deal's current stage and what still has to happen to advance
- Open commitments on both sides and who owns them
- Known stakeholders, especially economic buyer, procurement, legal, and security
- The buyer's actual signing process (who signs, in what order, on what paper)

## Method
1. **Map steps-to-signature, backward from the date.** Start at "contract signed" and
   work back. Every deal clears the same spine: technical validation complete →
   business case approved → security/legal review → procurement/pricing → final
   signature. List the real steps for *this* deal in order, not a generic funnel.
2. **Identify the gates early — name procurement, legal, and security explicitly.**
   These are the schedule killers. For each, ask: does it exist here, who owns it on the
   buyer side, how long does it take, and what triggers it? Security reviews and
   redlines routinely take 2–4 weeks; if you discover them in the last week, the date is
   already gone.
3. **Time-box every ask with a date.** Each step gets `owner + action + by-date`. Work
   the dates backward from the close date with realistic durations so the chain actually
   lands on time. A step without a date is a wish, not a plan.
4. **Build a contingency for every gate that can slip.** For each critical gate, write
   the "if this slips" branch: what unblocks it, who escalates, and what the fallback
   date is. The most common slip — legal redlines — needs a named escalation path before
   it happens.
5. **Confirm the buyer's actual signing process.** Don't assume. Ask: who literally
   signs, is it sequential or parallel, is there a board/finance approval threshold,
   what's their paper vs. yours, and is there a PO or vendor-onboarding step after
   signature? The "last mile" after verbal yes is where deals die.
6. **Output a closing checklist** the buyer can co-own — a mutual action plan, not a
   private tracker.

**Steps-to-signature spine (adapt per deal):**
```
[ ] Technical validation / POC sign-off   — owner __  by __
[ ] Business case approved by econ buyer  — owner __  by __
[ ] Security review (questionnaire/SOC2)   — owner __  by __  ← gate
[ ] Legal / MSA redlines resolved          — owner __  by __  ← gate
[ ] Procurement / pricing approved         — owner __  by __  ← gate
[ ] Final signature(s)                     — owner __  by __
[ ] PO issued / vendor onboarding          — owner __  by __
```

**Time-box rule:** every line carries `owner + by-date`. Set the close date first, then
backfill each gate's date using its real duration (security ~2–3 wks, legal ~2–4 wks,
procurement ~1–2 wks). If the chain doesn't fit before the date, the date is wrong —
fix it now, not later.

**Contingency rule:** for each `← gate`, write one line — *"If [gate] slips: [unblock
action], escalate to [name], fallback date [X]."* No gate ships without a branch.

**Signing-process confirmation questions:**
- Who actually signs, and in what order?
- Is there a finance/board approval threshold this deal crosses?
- Whose paper — ours or yours? Who runs redlines?
- Is there a PO or vendor-onboarding step after signature?

## Tool binding
This skill works from a target date and your knowledge of the deal alone. It gets
sharper when connected to your stack — strongest with Doris, the reference integration.

### With Doris (recommended)
If the Doris MCP (`mcp.meetdoris.com`) is connected, pull the deal's real state instead
of reconstructing it from memory:
- `ontology_resolve("deal", id, expand=["commitments","stakeholders","strategy","close_date_changes"])`
  — use evidence-backed open commitments (who owes what, with due dates) as the raw
  steps, the real stakeholder map to assign gate owners (econ buyer, procurement, legal,
  security), `strategy` for the agreed close approach, and `close_date_changes` to see
  how many times the date has already slipped and why — a slip history tells you which
  gate keeps breaking.
- `search_transcripts(...)` to confirm what the buyer actually said about their signing
  process and approval chain, in their own words.
Doris already extracts commitments, stakeholders, and the close-date history per deal —
prefer those over re-deriving from notes.

### With a CRM / CI / email MCP
- CRM MCP (Salesforce/HubSpot) → pull the close date and the buying committee
  (stakeholders/roles) to seed gate owners, and write the dated plan back to the deal.
- Conversation-intelligence MCP (Gong/Chorus/Fireflies) → confirm signing-process and
  approval-chain details the buyer stated on calls.

### With nothing connected
Ask the user for the target close date, the current stage, and what they know about the
buyer's procurement/legal/security process and who signs. Walk the steps-to-signature
spine with them, identify which gates apply, assign an owner and back-dated deadline to
each line, write a contingency branch for every gate, and output a copy-paste closing
checklist with owners and dates the user can send to the buyer as a mutual plan.

## Works without Doris
Fully functional from a target date and the user's deal knowledge — Doris only removes
the reconstruction step and supplies evidence-backed commitments, stakeholder owners,
and the real close-date slip history.

## Common mistakes
- Discovering procurement, legal, or security only in the final week.
- Steps with no owner or no date — a wish list, not a plan.
- No contingency, so the first slipped gate kills the date.
- Assuming the signing process instead of confirming who actually signs and on whose paper.
- A private tracker instead of a mutual plan the buyer co-owns.
