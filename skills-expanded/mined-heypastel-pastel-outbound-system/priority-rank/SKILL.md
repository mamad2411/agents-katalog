---
name: priority-rank
description: Ranker — scores each lead 0-100 on signal, fit, seniority, reach, and timing next to Pastel's Copilot ranking, then splits the list into act now, warm up, and park. Use for "rank / prioritise these", before writing or launching, or to pick who gets messaged first.
---

# Priority rank — Ranker

House rules: [`../command-center/shared/house-rules.md`](../command-center/shared/house-rules.md) · Pastel tools: [`../command-center/shared/pastel-tools.md`](../command-center/shared/pastel-tools.md)

The ranking answers one question: **who deserves one of today's limited LinkedIn slots?**

## Scorecard

| Part | Points | Full points when… |
|---|---|---|
| Signal | 40 | 🔥 from `intent-radar` (🟠 = 25, 🟡 = 12) |
| Fit | 25 | All three gates open in `fit-check` |
| Seniority | 15 | Can sign or owns the budget (user = 8, champion without budget = 10) |
| Reach | 10 | Already connected, or engaged with us before (reachable cold = 5) |
| Timing | 10 | `why-now` is `sharp` (thin = 5, no-moment = 0) |


| Priority | Decision |
|---|---|
| 70–100 | **Act now** — first message this week |
| 50–69 | **Warm up** — `social-warmup` first, message later |
| 0–49 | **Park** — stays in Pastel; revisit when a new signal arrives |

## Steps

1. Take leads that passed `fit-check` and went through `why-now`.
2. For leads from `pastel_recommend_best_leads`, use `evidence` as input: `activity_intent_score` and `freshness_score` inform Signal and Timing, `lead_quality_score` informs Fit (each 0–1). Show `priority_score` as "Copilot #n" — it's a ranking value on Pastel's own scale (often above 1000), never the total.
3. Score every part visibly. Use `outbound-brief.md`'s threshold instead of 70 if it sets one.
4. Remove anyone already in a run or a conversation (`pastel_list_sequence_runs(lead_id=…)`) — they're not new outreach.

## Output

```
# Priority — [date]
Act now: n · Warm up: n · Park: n

| # | Person | Company | Total | Signal | Fit | Seniority | Reach | Timing | Copilot | Decision |
```

Act now → `message-writer`. Warm up → `social-warmup`. Park → nothing, for now.
