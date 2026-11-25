---
name: mutual-action-plan
description: "Build a mutual action plan (MAP) with the buyer — backward-planned milestones from go-live, owners on both sides, and the decision/procurement/legal/security steps that actually gate close. Use when a deal needs a joint close plan. Triggers on: mutual action plan, MAP, close plan with buyer, joint plan, success plan."
---

# Mutual Action Plan

## Purpose
Turn a target go-live date into a shared, dated plan the buyer co-owns — so the path to
close is explicit, every step has a named owner on both sides, and the hidden gates
(decision, procurement, legal, security) surface before they slip the date.

## Inputs
- The buyer's target go-live / "value by" date (the only date that matters — work back from it)
- Stakeholders on both sides and their roles (champion, EB, procurement, legal, security, IT)
- The deal's current stage and what's already committed
- Known process requirements (security review, MSA/redlines, vendor onboarding, budget approval)

## Method
1. **Anchor on the go-live date, not the close date.** Ask the buyer: "When do you need
   this delivering value?" Close date is derived, not chosen.
2. **Backward-plan the milestones.** From go-live, subtract each step's lead time to place it
   on the calendar. Don't forward-plan from today — that hides the slack you don't have.
   Typical chain (work right-to-left):
   - Go-live / onboarding kickoff
   - Contract signed
   - Procurement / PO issued
   - Legal redlines + MSA executed
   - Security / InfoSec review passed
   - Verbal commit / decision made
   - Business case approved by EB
   - Technical validation / POC complete
3. **Assign an owner on BOTH sides for every milestone.** A milestone with only a seller
   owner is a wish; one with only a buyer owner is a hope. Each row names a seller owner
   *and* a buyer owner. Buyer-only steps (procurement, legal, security) still get a seller
   owner who chases.
4. **Surface the non-sales gates explicitly.** Decision, procurement, legal, and security
   are where deals die silently. Each gets its own row with realistic lead time:
   - **Decision:** who signs off, what they need to see, by when
   - **Procurement:** vendor onboarding, PO process, payment terms, portal setup
   - **Legal:** MSA/DPA, redline rounds (assume ≥2), who in legal owns it
   - **Security:** InfoSec questionnaire, SOC2/pen-test review, SSO/data requirements
5. **Make it a shared document, not a slide.** The MAP lives where the buyer can see and
   edit it (shared doc / deal room). Use the table format below.
6. **Get the buyer to co-own it.** Co-ownership is earned, not asked for:
   - Build the first draft *with* the champion live on a call, not for them in advance.
   - Ask them to fill in the buyer-side owners and dates — their handwriting on it is the commit.
   - Frame it as protecting *their* go-live date: "If we miss security by the 14th, your
     March launch slips — let's make sure that doesn't happen."
   - Send it after every call with the status column updated; it becomes the shared truth.
   - A champion who won't engage with the MAP is telling you the deal isn't real.

**MAP table format (shared document):**
```
Mutual Action Plan — <Account> × <Your Co> | Target go-live: <date>

| # | Milestone                          | Seller owner | Buyer owner   | Target date | Status      |
|---|------------------------------------|--------------|---------------|-------------|-------------|
| 1 | Technical validation complete      | <AE/SE>      | <Tech lead>   | <date>      | Done        |
| 2 | Business case approved by EB       | <AE>         | <Champion>    | <date>      | In progress |
| 3 | Decision / verbal commit           | <AE>         | <EB>          | <date>      | Not started |
| 4 | Security / InfoSec review passed    | <SE>         | <Security>    | <date>      | Not started |
| 5 | Legal — MSA/DPA redlines executed  | <AE>         | <Legal>       | <date>      | Not started |
| 6 | Procurement — PO issued            | <AE>         | <Procurement> | <date>      | Not started |
| 7 | Contract signed                    | <AE>         | <EB>          | <date>      | Not started |
| 8 | Onboarding kickoff / go-live       | <CSM>        | <Champion>    | <date>      | Not started |
```
Status values: `Not started` / `In progress` / `Done` / `At risk` / `Blocked`.

**Lead-time rule:** every step has a realistic duration. Legal ≈ 2–4 weeks (redlines never
go one round), security ≈ 2–6 weeks (their queue, not yours), procurement ≈ 1–3 weeks.
If the backward math lands a step before today, the go-live date is already at risk — say so.

## Tool binding
This skill works from a target date and a list of steps alone. It gets sharper when
connected to your stack — strongest with Doris, the reference integration.

### With Doris (recommended)
If the Doris MCP (`mcp.meetdoris.com`) is connected, pull the real deal state instead of
asking the user to reconstruct it:
- `ontology_resolve("deal", id, expand=["commitments","stakeholders","strategy","close_date_changes"])`
  — `commitments` give the existing both-sided obligations to seed milestones, `stakeholders`
  map owners (champion, EB, procurement, legal, security) to real people, `strategy` gives
  the close path, and `close_date_changes` shows where the date has already slipped so the
  backward plan is honest about historical risk.
Prefer the evidence-backed commitments and stakeholder roles Doris already extracts over
re-deriving them from memory.

### With a CRM / CI / email MCP
- CRM MCP (Salesforce/HubSpot) → pull deal dates (close date, stage) and the contact list
  to populate buyer-side owners, and write the MAP milestones back as tasks/next steps.
- Conversation-intelligence MCP (Gong/Chorus/Fireflies) → confirm who owns what from the
  actual call where the plan was discussed.

### With nothing connected
Ask the user for the buyer's target go-live date and the known steps (decision, security,
legal, procurement, contract). Then:
1. Backward-plan from go-live, subtracting realistic lead times for each step.
2. Assign a seller and buyer owner to every row (ask the user who fills each).
3. Output the completed MAP table for them to paste into a shared doc and review with the buyer.
4. Flag any step whose backward date falls before today as `At risk`.

## Works without Doris
Fully functional from a target date and a step list — Doris only removes the manual
reconstruction step and supplies evidence-backed commitments, stakeholder owners, and the
deal's real close-date history.

## Common mistakes
- Forward-planning from today instead of backward from go-live — hides the lack of slack.
- Milestones with an owner on only one side (a to-do list, not a mutual plan).
- Omitting the silent killers: no row for security, legal redlines, or procurement.
- Building the MAP *for* the buyer and emailing it — co-ownership comes from building it *with* them.
- Single-round legal/security assumptions; real lead times are longer than reps hope.
