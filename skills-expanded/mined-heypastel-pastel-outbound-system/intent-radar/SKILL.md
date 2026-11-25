---
name: intent-radar
description: Radar — lists people Pastel caught doing something that suggests they could buy (asking for a tool, reacting to a competitor, discussing the problem, changing role), each with what they did and when. Use for "get me leads", "who's buying right now", "who engaged with this post", or building a warm list.
---

# Intent radar — Radar

House rules: [`../command-center/shared/house-rules.md`](../command-center/shared/house-rules.md) · Pastel tools: [`../command-center/shared/pastel-tools.md`](../command-center/shared/pastel-tools.md)

Every row answers one question: **what did this person just do?** The event and its date are the row.

## Signal strength

| Strength | What they did |
|---|---|
| 🔥 Hot | Asked publicly for a tool or recommendation; complained about the problem we solve |
| 🟠 Warm | Reacted to or commented on a competitor's or a category post; engaged with our own content; commented a keyword ("DEMO", "SALES", "interested") to claim someone else's giveaway |
| 🟡 Early | New role in the last 90 days; team we'd equip is hiring; funding tied to this problem |

## Steps

1. Load the market map or `outbound-brief.md`.
2. **Ask Pastel for the ranked list first:** `pastel_recommend_best_leads` with the segment's filters (`job_titles`, `countries`, `industries`, `icp_definition_id`, and `created_since` when the user gives a time window). Use `pastel_query_leads` to go past the top of the list.
3. **"Who engaged with X":** find the post with `pastel_query_posts`, then `pastel_leads_for_post`.
4. **Read what happened.** Ranked results carry it in `evidence` (`primary_event_type`, `primary_event_at`, `selection_reason`). For the others, or to quote the actual comment, use `pastel_get_details`, five ids at a time.
5. **Label** each row 🔥 / 🟠 / 🟡 from the table. Anything older than 60 days drops a level. Read the comment itself: a one-word keyword under a "comment to get it" post shows interest in a free resource, not a buying decision, so it stays 🟠 even when the post is about exactly what we sell.
6. Default list size: 30. The user can ask for more or fewer.

No results → run the empty-result check from the house rules.

## Output

```
# Radar — [what we looked for] — [date]
Source: Copilot ranking | lead search | post engagers · Rows: N · 🔥 n · 🟠 n · 🟡 n

| | Person | Headline | Company | What they did | When | lead_id |
```

Close with one `pastel_show_leads` call with the same ids in the same order, then hand the lead cards to `fit-check`.
