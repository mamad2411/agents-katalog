---
name: citlyze-visibility-report
description: Build a window-over-window AI search visibility report from Citlyze data. Use when asked "how visible is my brand in AI search", "what changed this week/month", "build an AI visibility report", or for recurring exec reporting on ChatGPT/Claude/Perplexity/Gemini visibility. Requires the Citlyze MCP server.
license: MIT
metadata:
  author: Citlyze (https://www.citlyze.com)
---

# Citlyze visibility report

Produce an executive-ready report on how a brand shows up in AI search engines, comparing the latest completed measurement window to the previous one.

## Prerequisites

The [Citlyze](https://www.citlyze.com) MCP server must be connected ([setup guide](https://www.citlyze.com/docs/mcp/setup-clients)). All Citlyze tools are read-only. When a tool takes `measurement_window_id` and none is given, it defaults to the latest completed window.

## Workflow

1. **Orient.** Call `get_workspace_overview`. Note the workspace name, target brand, `active_prompts`, `active_engines`, `tracked_competitors`, and `latest_completed_window`.
2. **Pick windows.** Call `list_measurement_windows` with `status: "completed"`. Take the two most recent windows. If only one exists, report a single-window snapshot and say trend data needs a second window.
3. **Pull metrics for both windows.** Call `get_visibility_overview` once per window. Each row in `by_brand_engine` carries: `visibility_score`, `mention_rate`, `citation_rate`, `source_rate`, `avg_prominence`, `share_of_answer`, and `n_runs`.
4. **Competitive standings.** Call `list_competitor_visibility` for the latest window. `by_brand` is sorted by `visibility_score`; note the target brand's rank and the gap to the leader.
5. **Headline movers.** Compute per-engine deltas between the two windows for the target brand. Flag any engine where `visibility_score` moved notably in either direction. Always sanity-check surprising swings against `n_runs`: a big move on very few runs is weak evidence, so say so.
6. **Write the report** in this shape:
   - **TL;DR** - three sentences: overall direction, best engine, biggest risk.
   - **Scoreboard table** - one row per engine: previous score, current score, delta, mention rate, citation rate.
   - **Competitive position** - rank, gap to leader, any competitor overtakes since last window.
   - **Watch items** - low-`n_runs` caveats, engines with falling citation rate, anything needing a decision.

## Interpretation rules

- `visibility_score` is Citlyze's blended per-engine score; compare it across windows for the same brand rather than across different companies.
- A citation (link shown) is not the same as a mention (brand named in the answer) or a source consulted (page the engine read). Report them as separate signals.
- Percentages are rates across runs in the window, not absolute counts.

## Out of scope

This skill reports; it does not change anything in the workspace (the MCP surface is read-only). For acting on findings, chain into `citlyze-action-plan`.

Learn more: [Citlyze dashboard guide](https://www.citlyze.com/docs/using-citlyze/dashboard) - [citlyze.com](https://www.citlyze.com)
