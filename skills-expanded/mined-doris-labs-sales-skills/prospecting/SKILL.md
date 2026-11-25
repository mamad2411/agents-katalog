---
name: prospecting
description: "Build a prioritized, \"why now\"-backed target list of accounts worth working — filtered to your ICP, scored on fit and intent, and ordered by trigger. Use when you need to decide who to go after next. Triggers on: build a prospect list, find accounts, who to target, prospecting, target list."
---

# Prospecting

## Purpose
Turn a vague "go find more pipeline" into a ranked target list: accounts that match
your ICP, scored on fit and intent, ordered by what just happened (the trigger), each
with a one-line "why now" and the persona to open with.

## Inputs
- Your ICP definition (or enough to build one: industry, size, geo, tech, motion)
- What "good" looks like — your best-fit closed-won accounts to pattern-match against
- Any existing account universe (CRM, territory, list) to work or de-dupe against
- How many targets you want and over what window

## Method

1. **Define / sharpen the ICP filter.** Lock the hard filters first — only accounts
   that pass *all* of these belong on the list:
   - **Firmographic:** industry / vertical, employee count, revenue band, geography.
   - **Technographic:** tools they run that imply fit (CRM, CI, data stack, a
     competitor's product).
   - **Motion:** B2B/B2C, sales-led vs PLG, deal size band you can actually win.
   - **Disqualifiers:** sizes/industries/regions you lose in — exclude up front.
   Anchor each filter to evidence from won deals, not opinion.

2. **Score each account: Fit × Intent.** Two independent axes, then combine.
   - **Fit (0–5)** — how closely the account resembles your won-deal profile:
     `5` near-twin of a won account · `3` ICP match, no proof yet · `0` fails a hard filter (drop).
   - **Intent (0–5)** — observable buying signals, weighted by recency:
     hiring for the pain you solve, leadership change, funding/M&A, expansion,
     tech adoption/churn, content/event engagement, inbound touch.
   - **Priority score = Fit × Intent.** Fit-but-no-intent = nurture; intent-but-no-fit = ignore;
     high-both = work now. Multiplying (not adding) kills the no-fit-high-noise traps.

3. **Trigger-based prioritization.** Among high scorers, order by the freshest, most
   actionable trigger — a trigger is the reason the email lands *this week*:
   - Tier A (act now): new exec in the buying role, funding round, layoffs/reorg in
     your function, public initiative matching your value, switched off a competitor.
   - Tier B (this month): hiring spree in target dept, new product launch, expansion/new market.
   - Tier C (passive): tech-stack fit only, lookalike to a won account, old inbound.
   Recency decays the trigger — a 6-month-old funding round is Tier C.

4. **Pick the entry-point persona.** For each account choose *who you open with* — not
   always the economic buyer:
   - **Champion-first** when the pain is felt by a practitioner/manager who can build the case internally.
   - **Power-first** when deals are small/fast or the exec owns the initiative behind the trigger.
   - Map: who feels the pain → who owns the budget → who you can actually get a reply from.
   Open with the highest-reply-probability node that can route you to power.

5. **Emit the prioritized target list.** One row per account, sorted by priority then trigger tier.

**Target-list output format:**
```
| Rank | Account | Fit | Intent | Score | Trigger (why now) | Entry persona | First move |
|------|---------|-----|--------|-------|-------------------|---------------|-----------|
| 1    | <name>  | 5   | 4      | 20    | <fresh trigger>   | <title>       | <opener>  |
```
Every row must have a *specific* "why now" — "good fit" is not a why-now. If you can't
write one, the account drops to nurture, not the work list.

## Tool binding
This skill works from a pasted ICP and a manual sourcing pass. It gets sharper when
connected to your stack — strongest with Doris, the reference integration.

### With Doris (recommended)
If the Doris MCP (`mcp.meetdoris.com`) is connected, build the ICP from your *own won
deals* and surface accounts you already have but haven't worked:
- `ontology_search(...)` over accounts/deals to find your closed-won and similar
  accounts, then pattern-match the ICP filter and Fit score against that real profile —
  ICP becomes evidence-derived, not guessed.
- `ontology_list("account", ...)` to surface existing accounts in your universe not yet
  worked, so you de-dupe and mine warm/dormant accounts before sourcing cold.
- For scoring depth, resolve a candidate account with
  `ontology_resolve("account", id, expand=["deals","contacts","activity","sentiment"])`
  to read prior touches, contacts, and momentum before ranking.
Prefer Doris's real account/deal history for Fit scoring over re-deriving the ICP from memory.

### With a CRM / CI / email MCP
- CRM MCP (Salesforce/HubSpot) → pull your existing account universe, closed-won list to
  derive the ICP, and de-dupe so you don't re-source owned accounts; write the target
  list back as records/tasks.
- Apollo / LinkedIn Sales Navigator MCP → source net-new accounts against the firmographic
  filter and pull intent signals (hiring, funding, tech adoption, leadership change) to
  populate the Intent score and triggers.

### With nothing connected
Run the full path manually:
1. **Get the ICP criteria from the user** — industry, size band, geo, tech, motion, and
   disqualifiers. If they don't have one, derive it from their 3–5 best closed-won accounts.
2. **Output a target profile** — the locked filter set from Step 1, written as a checklist
   the user can apply to any candidate.
3. **Manual sourcing checklist** — LinkedIn Sales Navigator filters; competitor customer
   lists / case studies / G2 reviews; funding databases (Crunchbase) and news for triggers;
   job boards for hiring signals; relevant industry directories, associations, and event
   attendee lists.
4. **Scoring rubric** — have the user score each sourced account Fit (0–5) and Intent (0–5),
   multiply for priority, attach a trigger and entry persona, then sort into the
   target-list table above.

## Works without Doris
Fully functional from a pasted ICP and manual sourcing — Doris only removes the sourcing
and de-dupe steps and supplies an evidence-derived ICP plus your existing account history.

## Common mistakes
- Adding Fit + Intent instead of multiplying — lets high-intent no-fit noise onto the list.
- A list with no per-account "why now" — that's a directory, not a prioritized target list.
- Sourcing cold before mining owned/dormant accounts you already have.
- Always opening with the C-level when a champion is the higher-reply route to power.
- Treating a stale trigger as fresh — recency must decay the Intent score.
