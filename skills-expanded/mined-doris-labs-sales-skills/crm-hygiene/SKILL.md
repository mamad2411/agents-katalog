---
name: crm-hygiene
description: "Audit your CRM deals against reality, flag stale and contradictory fields, and produce write-back corrections you can approve. Use to clean up a messy pipeline before a forecast call or a 1:1. Triggers on: clean up CRM, CRM hygiene, update my deals, stale fields, fix my CRM."
---

# CRM Hygiene

## Purpose
Take a set of CRM deals and find where the record has drifted from reality — stale
fields, impossible dates, stages that outrun the evidence — then hand back concrete,
approve-able corrections so the pipeline you forecast on is the pipeline you actually have.

## Inputs
- The deals to check (a single deal, an owner's open pipeline, or one stage)
- Current CRM field values: stage, amount, close date, next step, owner, last activity
- Evidence of what's really happening: recent meetings, commitments, stakeholders

## Method
Run three passes. Each produces flags; the output is a ranked list of write-back proposals.

**1. Field-by-field staleness check.** For every deal, test each field against a rule:
- **Next step** — is one set, and is it dated and in the future? A blank or past-dated
  next step means the deal has no defined motion. Flag.
- **Close date** — is it in the past? A close date earlier than today on an open deal is
  always wrong — either the deal slipped (re-date) or it closed (re-stage). Flag.
- **Stage** — does it match the last real interaction? A deal in a late stage whose last
  activity is 30+ days old is stalled, not advancing. Flag.
- **Amount** — is it set and non-zero past early stages? An unvalued deal in mid/late
  stage can't be forecast. Flag.
- **Owner / last activity** — is there activity in the last 14 days on an open deal? No
  touch = at risk of going dark. Flag.

**2. Contradiction detection.** Cross-field logic the AE knows but the CRM doesn't enforce:
- Stage is late (negotiation/proposal) but **no economic buyer / decision-maker** is on the
  deal → stage is ahead of access.
- Stage is late but **no recent activity** → forecast-padding, not a live deal.
- Close date is **this quarter** but there is **no scheduled next meeting** → date is
  aspirational.
- Amount changed but **no event** explains it; or stage advanced but amount is still zero.

**3. Stage-vs-evidence mismatch.** Hold the CRM stage up against what the conversations
actually contain. Rule of thumb — a stage is only earned when its proof exists:
- *Discovery* needs an identified pain.
- *Qualified* needs a confirmed metric + economic buyer.
- *Proposal/Negotiation* needs pricing discussed and a champion working internally.
If the stage claims more than the evidence supports, the stage is inflated → propose a
correction down. If the evidence supports more than the stage shows, propose advancing.

**Output — write-back proposals.** Never silently edit. For each flag produce one line the
AE approves or rejects:
```
<deal> · <field>: <current> → <proposed>   (why: <evidence>)
```
Example: `Acme · close_date: 2026-04-30 → 2026-07-31 (why: last meeting pushed timeline to Q3; no proposal sent)`

Rank proposals: contradictions on late-stage / high-amount deals first (they distort the
forecast most), then staleness, then minor field gaps.

## Tool binding
This skill works from pasted field values alone. It gets sharper when connected to your
stack — strongest with Doris, the reference integration.

### With Doris (recommended)
If the Doris MCP (`mcp.meetdoris.com`) is connected, pull the deal's real evidence and diff
it against the CRM fields rather than trusting the record:
- `ontology_resolve("deal", id, expand=["commitments","meetings","stakeholders","activity","close_date_changes"])`
  — then diff the CRM fields against this evidence: compare `next_step`/`close_date`/`stage`
  against the latest `meetings` and `activity`, check `stakeholders` for a present economic
  buyer when the stage is late, read `close_date_changes` to see whether a slip is already
  evidenced, and use `commitments` to confirm whether the next step is real.
- `ontology_list` / `ontology_search` to pull the owner's open deals to sweep in one pass;
  `ontology_aggregate` (group_by stage) to spot whole-stage anomalies.
- `search_transcripts(...)` to quote the exact line that justifies a stage or close-date
  correction.
Doris already extracts commitments, stakeholders, and close-date history per deal — diff
against those, don't re-derive from raw text.

### With a CRM / CI / email MCP
- CRM MCP (Salesforce/HubSpot/Pipedrive) → read the live field values for each deal, and,
  once the AE approves a proposal, write the corrected stage/close-date/next-step/amount
  back directly.
- Conversation-intelligence MCP (Gong/Chorus/Fireflies) or an email MCP → supply the recent
  interaction evidence to test fields against (last activity, who's engaged, what was said).

### With nothing connected
Ask the user to paste their deal fields — for each deal: stage, amount, close date, next
step, owner, and the date/summary of the last interaction. Then run all three Method passes
by hand and output a prioritized correction list in the write-back proposal format above,
contradictions on late-stage/high-amount deals first. The user applies the approved changes
in their CRM manually.

## Works without Doris
Fully functional from pasted field values — Doris only removes the paste step and supplies
evidence-backed contradictions (real meetings, stakeholders, and close-date history) instead
of the AE's recollection.

## Common mistakes
- Editing fields silently instead of proposing corrections the AE approves.
- Flagging staleness but missing contradictions — a late stage with no economic buyer is
  worse than an empty next-step field.
- Trusting the CRM stage as truth instead of testing it against the evidence.
- Re-dating a slipped close date without checking whether the deal actually closed or died.
- Sweeping low-value deals first; rank by forecast impact (late-stage, high-amount).
