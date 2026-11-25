---
name: grovs-analytics
description: See how your tracking links are performing — views, installs, app opens, and revenue. Get an overview, find your top links, or drill into a specific link's stats by date range and platform. Use when the user asks about link performance, traffic, metrics, or analytics.
---

# Grovs: View Analytics

## Three tools, three levels

| Tool | What it answers | Returns |
|------|----------------|---------|
| `get_analytics_overview` | "How's the project doing?" | Current vs previous period totals (views, opens, installs, revenue, users) |
| `get_top_links` | "What's performing best?" | Ranked list by views (no other sort) |
| `get_link_analytics` | "How's this specific link doing?" | Daily breakdowns — **you must sum for totals** |

Start with `get_analytics_overview`. Only call others if the user asks to drill down.

## Non-obvious behavior

- **Overview auto-compares periods.** If you request Apr 1–8, it also returns Mar 24–31. Mention the comparison — that's the point.
- **Link analytics are daily rows**, not totals. Response looks like `"2026-04-01": {view: 100, ...}`. Sum them yourself if the user asks for "total views."
- **Top links sorts by views only.** If user asks "top by installs" — get top links then sort the results yourself, or use `search_links` with `sort_by: "installs"`.
- **Campaign metrics aren't here.** "How's my Summer Sale campaign?" → use `list_campaigns` with `term: "Summer Sale"`, not analytics tools.

## Date ranges

- No range specified → tools default to last 30 days (don't pass dates)
- "This week" → Monday through today
- "This month" → 1st of current month through today
- "Last month" → 1st to last day of previous month

## Example

User: "How are my links doing this month?"

```
get_analytics_overview(project_id: "p_m9f", start_date: "2026-04-01", end_date: "2026-04-08")
→ Current: 1,200 views, 400 opens, 80 installs
→ Previous (auto): 900 views, 300 opens, 60 installs
→ "Views are up 33% compared to the previous period."
```

User: "Which link is getting the most traffic?"
```
get_top_links(project_id: "p_m9f", start_date: "2026-04-01", end_date: "2026-04-08")
→ 1. Summer Sale — 600 views, 200 opens
```

User: "Show me the daily breakdown for that one"
```
get_link_analytics(project_id: "p_m9f", path: "https://foodies.grovs.io/summer-sale", start_date: "2026-04-01", end_date: "2026-04-08")
→ Daily rows. Sum if user wants totals.
```

The `path` parameter accepts a full link URL or just the slug — the server extracts the path automatically.

## Good follow-ups

- High views but low installs → suggest checking redirect config or app store listing
- Offer platform breakdown (`platform: "ios"`) if totals look skewed
- After overview → offer top links or link drill-down

## All tool responses are pre-formatted

Every Grovs tool returns human-readable formatted text. Don't reformat — just present and add context.
