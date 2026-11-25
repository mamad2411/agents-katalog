---
name: assembled-campaign-read
description: Write the six-beat campaign read for the client dashboard. Trigger on "campaign read", "write the read", or the dashboard Regenerate action. Ground every number in a tool. Never invent a cause.
metadata:
  version: 1.3.0
---

# Campaign read

A campaign read is six short beats for the client, in a fixed order. It is not commentary, not a PCA, and not a performance report. Each beat is 1-3 sentences. Each number is copied from a tool result. If a beat has no evidence, write exactly `Nothing to report yet.` for that beat.

## Procedure

1. Load this skill's `references/voice.md` and follow it as the voice contract (Luke approves that file before ship).
2. Call these tools for the MBA on the page (or supplied in the request):
   - **get_campaign_context**
   - **get_delivery_snapshot**
   - **get_campaign_insights** (live rows only — context, never a numeric source)
   - Campaign KPI review rows (the `buildKpiReview` / campaign_kpi payload supplied with the generate job). There is no separate KPI tool — do not invent one.
   - Do **not** call **get_pacing_snapshot**. Campaign pace is spend-to-date vs expected-to-date on the delivery snapshot totals (same figures as the dashboard strip).
3. Write the six beats in this order. Do not reorder. Do not add a seventh.

| Key | Heading | What it answers |
|---|---|---|
| `planned` | What was planned | Mix, flight, and **one** budget: `liveLineBudgetTotal` (the sum of live line budgets). State it as the live-line sum. Do not use the MBA booked total from context. |
| `happened` | What has happened | Delivered spend and deliverables from **reportedTotals** (reported + `spend_only` spend — same figures as the Where we are strip), plus `daysElapsed` / `daysInCampaign`. |
| `vsPlan` | Against the plan | Copy `expectedSpendToDate` and `behindBy` from the snapshot (the strip's figures). Do not recompute as budget × elapsed. Name the **reported** channel and platform that drives the gap. |
| `best` | Best thing going on | The strongest **reported** result, or a KPI row with `eligibleForBestWorst: true`. |
| `worst` | Worst thing | The weakest **reported** result or eligible KPI, stated plainly. Never a `no_source` / `no_rows_yet` line when a reported line is behind. Never a KPI with `eligibleForBestWorst: false`. |
| `upcoming` | Coming up | What needs to happen next (booked flights, catch-up, a material date). Describe the need. Never promise we are following up or contacting someone. |

4. Rules while writing:
   - Copy numbers as the tool gave them. Money to the nearest dollar or $K.
   - Never invent a cause. If the cause is not in a tool or a live insight, omit it.
   - Prior insights are context. Do not restate them as this period's finding unless you say what was believed before and what changed.
   - Delivery $ / KPI figures come from **get_delivery_snapshot** / the KPI review payload — never from insight bodies.
   - Happened copies **reportedTotals.spendToDate**. Against the plan copies **expectedSpendToDate** and **behindBy** (strip resolver — never budget × elapsed). `no_source` / `no_rows_yet` have null metrics and a `deliveryNote`.
   - Each snapshot line has `delivery_state`: `reported`, `no_rows_yet`, `no_source`, or `spend_only`.
     - `no_source`: the line **has no delivery reporting connected yet**.
     - `no_rows_yet`: the line **has not reported yet**.
     - `spend_only`: **spend is fixed-cost accrual; no delivery reporting connected**. Count its spend. Do not narrate zero impressions or clicks.
     - Never treat `no_source` / `no_rows_yet` as zero impressions, zero clicks, or "spent $X with no delivery".
     - They are never the worst thing when a `reported` line is behind.
   - KPI review rows come from `buildKpiReview`. Best/worst may only use a row with `eligibleForBestWorst: true` (tracked, with a delivered value). Never narrate "Not tracked for this source" as zero, as worst, or as "no conversions have landed".
   - Name the channel and the platform (Channel Factory, Meta, Seven). Do not say "digital".
   - Talk to the client as "you". The agency is "we".
   - Never promise a follow-up action. Never name a person or partner as being contacted. Coming up says what needs to happen, not who we will call.
5. Return **JSON only** (no markdown fence unless you must). Shape:

```
{
  "beats": {
    "planned": "...",
    "happened": "...",
    "vsPlan": "...",
    "best": "...",
    "worst": "...",
    "upcoming": "..."
  },
  "sources": ["get_delivery_snapshot", "get_campaign_context"]
}
```

`sources` lists the tool names you actually used. Omit a source you did not call.

## Failure modes

Reject the draft if any beat invents a number, invents a cause, uses a banned word from `voice.md`, hides a miss on a **reported** line, treats `no_source` / `no_rows_yet` as zero delivery, narrates a not-tracked KPI as zero / worst / no conversions, or promises a follow-up / names someone as being contacted.
