---
name: citlyze-action-plan
description: Turn Citlyze optimization recommendations into a prioritized, sequenced action plan. Use when asked "what should we do to improve AI visibility", "prioritize the recommendations", "make an AEO/GEO action plan", or after a visibility report surfaces problems. Requires the Citlyze MCP server.
license: MIT
metadata:
  author: Citlyze (https://www.citlyze.com)
---

# Citlyze action plan

Convert the recommendation backlog into a two-week plan a marketing or content team can execute.

## Prerequisites

The [Citlyze](https://www.citlyze.com) MCP server must be connected ([setup guide](https://www.citlyze.com/docs/mcp/setup-clients)). Tools are read-only; marking recommendations planned or done happens in the app.

## Workflow

1. **Pull the backlog.** Call `list_recommendations`. Rows arrive highest `priority_score` first, each with `title`, `summary`, `category`, `status`, `impact`, `confidence`, `effort`, and `target_url`.
2. **Filter.** Drop rows whose `status` shows they are already done or dismissed; keep new and in-progress work. Treat `category` as a free-form label: group by whatever values appear.
3. **Build an impact/effort matrix.** Place each recommendation in one of four quadrants (high impact + low effort first). Where `confidence` is low, say what evidence would raise it before committing serious effort.
4. **Cluster by page.** Group recommendations sharing a `target_url`; one page edit often clears several items at once. Clusters usually beat one-off fixes.
5. **Sequence into a plan:**
   - **Week 1** - quick wins (high impact, low effort) plus anything unblocking other items.
   - **Week 2** - the highest-impact medium-effort cluster.
   - **Backlog** - everything else in priority order, with a one-line reason each.
6. **For each planned item** state: what to change, on which URL, who plausibly owns it (content, dev, PR), and how success will show up in Citlyze afterwards (better mention rate, new citation, improved visibility on a named engine).

## Interpretation rules

- `priority_score` already blends Citlyze's view of value; use it as the default sort but override with the user's business context when they give any.
- Never promise a score outcome; frame expected results as the metric to watch in the next measurement window.
- If two recommendations conflict on one page, surface the conflict instead of silently picking one.

Learn more: [Recommendations in Citlyze](https://www.citlyze.com/docs/using-citlyze/recommendations) - [citlyze.com](https://www.citlyze.com)
