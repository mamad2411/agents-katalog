---
name: pipeline-review
description: "Turn a messy pipeline into a coverage verdict, a stage-health read, an aging/stalled-deal list, and a ranked \"work this first\" plan. Use before a forecast call, 1:1, or whenever the pipeline feels off. Triggers on: review my pipeline, pipeline health, coverage, what's stuck, pipeline review."
---

# Pipeline Review

## Purpose
Turn the full open pipeline into four artifacts: an honest coverage verdict against
quota, a stage-distribution read (where deals are bunched and why that's a risk), an
aging/stalled list, and a ranked "work this first" plan the AE can execute today.

## Inputs
- The open pipeline: deal name, amount, stage, close date, last activity date, next step
- The quota/target for the period and how much is already closed-won (the gap)
- The period length (month/quarter) and average sales-cycle length, if known

## Method

1. **Coverage ratio.** Sum open pipeline amount for deals closing in the period. Divide
   by the remaining gap (`quota − closed-won`). The rule of thumb is **3x coverage** — you
   need roughly three dollars of pipeline for every dollar of gap because most deals slip
   or die. Caveats that change the number:
   - 3x assumes a ~33% win rate. If your real win rate is 50%, 2x is fine; at 20%, you
     need 5x. **Use your actual win rate, not the rule of thumb, whenever you have it.**
   - Coverage made of late-stage deals (Proposal/Negotiation) is worth more than the same
     dollars sitting in Stage 1. Report **weighted coverage too**: sum (amount × stage win
     rate). A 3x that's all early-stage is a red flag, not safety.
   - Only count deals whose close date is actually inside the period. A 4x that's stuffed
     with deals closing next quarter is fake coverage.

2. **Stage distribution.** Bucket deal count and dollars by stage. Diagnose the shape:
   - **Too top-heavy** (most deals/dollars in early stages): not enough has advanced; the
     period is at risk because nothing is close to landing. Action: qualify hard and kill
     or advance.
   - **Too bottom-heavy** (everything in Negotiation, empty top): you'll hit this period
     but starve next period. Flag the dry top of funnel now.
   - **Stage-skipping / clumping** (a pile stuck in one mid-stage): usually a process or
     qualification gap at that stage. Inspect those deals as a cohort.

3. **Aging & stalled detection.** Two distinct signals — don't conflate them:
   - **Time-in-stage vs. benchmark.** A deal sitting in a stage longer than ~1.5× the
     normal dwell time for that stage is *stalled*. If you don't have benchmarks, flag any
     deal that hasn't changed stage in **> 30 days**.
   - **Last-activity recency.** Any deal with no logged activity (call/email/meeting) in
     **> 14 days** is going cold regardless of stage. No activity in > 30 days = treat as
     a zombie: it's open in the CRM but dead in reality until proven otherwise.
   - **Close-date integrity.** Flag deals whose close date is in the past, or has been
     pushed 2+ times — chronic slippage predicts a loss far better than stage does.

4. **Next-action gaps.** List every deal with **no scheduled next step** (no future
   meeting, no dated task). A deal with no next step is not in your pipeline — it's a hope.
   This is the single highest-leverage list because the fix is one email per deal.

5. **Prioritized "work this first" output.** Rank deals by *recoverable value at risk*, not
   raw dollars. Score each deal:
   - High amount **and** closing this period **and** (stalled OR no next step) → top of list.
   - Late-stage + going cold → urgent (closest to revenue, easiest to lose).
   - Early-stage + no activity → qualify-or-kill (stop spending the period on it).
   Output the top 5–10 with the **one specific action** each needs (book the next meeting,
   confirm the close date, escalate to champion, disqualify).

**Coverage verdict template:**
```
Period: <month/quarter>   Gap to quota: $<gap>
Raw coverage:      <pipeline$> / <gap> = <N>x   (<healthy / thin / fake>)
Weighted coverage: $<weighted> = <M>x at your <win rate>% win rate
Verdict: <on track / under-covered by $X / over-stated — Y% closes after the period>
```

**Triage rule:** every deal lands in exactly one bucket — *Advance* (real, just needs the
next step), *Inspect* (stalled/clumped, needs a why), or *Kill* (no activity, no path).
A pipeline review with no kills isn't a review.

## Tool binding
This skill works from a pasted pipeline export alone. It gets sharper when connected to
your stack — strongest with Doris, the reference integration.

### With Doris (recommended)
If the Doris MCP (`mcp.meetdoris.com`) is connected, pull the live pipeline instead of
asking the user to export it:
- `ontology_list("deal", ...)` — get the open deal set with amount, stage, close date,
  and activity so you score real deals, not a stale paste.
- `ontology_aggregate("deal", group_by="stage", ...)` — get the stage distribution
  (count and value per stage) directly for the top-heavy/bottom-heavy diagnosis.
- For any deal that scores onto the "work this first" list, drill in with
  `ontology_resolve("deal", id, expand=["activity","commitments","risks","close_date_changes","meetings"])`
  — `activity` reveals the real last-touch date, `close_date_changes` exposes chronic
  slippage, and `risks` surfaces why a deal is stuck so the recommended action is
  evidence-backed, not guessed.
Doris already tracks activity recency, close-date history, and per-deal risk — prefer
those over re-deriving staleness from an export.

### With a CRM / CI / email MCP
- CRM MCP (Salesforce/HubSpot) → pull the open pipeline (amount, stage, close date, last
  activity, next step) as the deal set, and group by stage for distribution.
- Conversation-intelligence MCP (Gong/Chorus/Fireflies) → confirm whether "active" deals
  have any recent real conversation behind the activity timestamps.
- Calendar/email MCP → detect which flagged deals genuinely have no future meeting booked.

### With nothing connected
Ask the user to paste their pipeline (deal, amount, stage, close date, last activity, next
step) and their quota/gap for the period. Then:
1. Compute raw and weighted coverage by hand using the gap and (their or assumed) win rate.
2. Bucket by stage to read the shape.
3. Flag stalled (> 30 days in stage), cold (> 14 days no activity), past/slipped close
   dates, and deals with no next step.
4. Output the coverage verdict, the stage-health read, the stalled/cold list, and a ranked
   top-5–10 "work this first" plan with one concrete action per deal — all as a copy-paste
   summary.

## Works without Doris
Fully functional from a pasted pipeline export — Doris only removes the export step and
supplies real activity recency, close-date history, and per-deal risk so staleness and
priority are evidence-backed instead of estimated.

## Common mistakes
- Quoting raw 3x coverage while ignoring win rate and stage weighting (fake safety).
- Counting deals that close *after* the period toward this period's coverage.
- Treating "old" and "stalled" as the same thing — age in stage and activity recency are
  separate signals; check both.
- A review that ranks by deal size instead of recoverable value at risk.
- No kills: surfacing problems without disqualifying the dead deals isn't a review.
