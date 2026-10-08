---
name: cross-client-metrics-overview
description: >
  Pull and compare performance metrics across multiple Planable workspaces (clients or brands)
  in a single view. Use this skill whenever the user wants to compare clients, see how all
  accounts are performing, get an agency-wide metrics overview, or says things like
  "how are all my clients doing", "compare performance across workspaces", "give me a
  cross-client report", "agency overview", "which client is performing best", or
  "metrics across all accounts". Always activate for multi-workspace analytics queries
  in Planable. For single-workspace reports, use the monthly-performance-summary skill instead.
---

# Cross-client metrics overview

Compare social media performance across multiple Planable workspaces in one view.
Built for agency operators and managers who need to see the full picture without opening each workspace individually.

## How this skill works

1. Identify the workspaces and time period to cover
2. Fetch page and post metrics for each workspace
3. Produce a ranked, comparative summary
4. Flag outliers — best performers, problem accounts, accounts needing attention

---

## Step 1: Gather inputs

- **Workspaces to include** — specific clients, or all workspaces (default: all)
- **Date range** — default to previous calendar month if not specified
- **Primary metric to rank by** — engagement rate (default), impressions, posts published, or audience growth

If the user asks for "all clients", proceed — but if there are more than 15 workspaces, confirm before fetching them all.

---

## Step 2: Fetch data for each workspace

For each workspace:

```
list_pages(workspaceId) → get all pageIds

get_page_metrics_summary(
  workspaceId,
  pageIds[],
  startDate,
  endDate
)

get_post_metrics_summary(
  workspaceId,
  pageIds[],
  startDate,
  endDate
)
```

Store results keyed by workspace name. Handle failures gracefully — if a workspace returns no data, note it rather than stopping the whole report.

---

## Step 3: Build the comparison

### At a glance — ranked table

Rank workspaces by the primary metric. Show as a clean list:

```
Agency performance — [Month Year]
Ranked by engagement rate

1. [Client A]       Eng. rate: 4.2%   Impressions: 48K   Posts: 22
2. [Client B]       Eng. rate: 3.8%   Impressions: 31K   Posts: 18
3. [Client C]       Eng. rate: 2.1%   Impressions: 62K   Posts: 30
...
```

Include totals row at the bottom: total impressions, total engagement, total posts across all clients.

### Highlights and flags

After the table, add a short section with 3–5 specific callouts:

**🏆 Top performer** — [Client] led on [metric] with [number]. [One sentence on why if inferable — e.g., "Ran 2 campaigns this month."]

**📈 Most improved** — [Client] grew audience by [X%] vs. prior period (only include if prior-period data is available).

**⚠️ Needs attention** — [Client] published [n] posts but engagement rate dropped to [X%]. Worth reviewing content mix.

**💤 Low activity** — [Client] had fewer than 3 posts scheduled this month. May need a content push.

Keep callouts specific and data-backed. Don't include a callout category if there's no data to support it.

### Per-client detail (optional)

If the user wants per-client breakdowns, add a short block per workspace after the table — same format as the monthly-performance-summary report. Only generate these if explicitly requested, to keep the default output scannable.

---

## Step 4: Tone and formatting

- Write for an operations manager or agency lead reviewing accounts
- Be direct about which clients are underperforming — don't soften it with filler
- Numbers: round to nearest whole number or one decimal. Use K for thousands (48K, not 48,000)
- Don't repeat numbers across sections — show each metric once in the right place
- If data is missing for a workspace, include it in the table with "No data" rather than omitting it

---

## Edge cases

- **Unsupported platforms**: Google My Business and Threads don't return metrics via the connector. Note these per workspace in a "Data not available" footnote.
- **Large workspace count (15+)**: Warn the user that fetching all workspaces may take a moment. Proceed unless they want to narrow scope.
- **Single workspace accidentally**: If only one workspace is found or specified, suggest using the monthly-performance-summary skill instead — it's better suited for single-client reports.
- **Mixed plan types**: Some Planable plans may have limited analytics access. If a workspace returns empty metrics, note that analytics may not be available on that workspace's plan and suggest checking Planable directly.
- **Comparing incomparable periods**: If workspaces have different amounts of data (e.g., one client was just onboarded), flag this in the notes section.
