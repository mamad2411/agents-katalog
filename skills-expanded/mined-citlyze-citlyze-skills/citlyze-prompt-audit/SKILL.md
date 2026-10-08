---
name: citlyze-prompt-audit
description: Audit tracked prompts in Citlyze to find weak spots and coverage gaps. Use when asked "which prompts are underperforming", "audit my tracked prompts", "where are we invisible", or "what prompts should we track next". Requires the Citlyze MCP server.
license: MIT
metadata:
  author: Citlyze (https://www.citlyze.com)
---

# Citlyze prompt audit

Review the prompt portfolio: find prompts where the brand is invisible, engines or locations that drag performance down, and intent gaps worth tracking next.

## Prerequisites

The [Citlyze](https://www.citlyze.com) MCP server must be connected ([setup guide](https://www.citlyze.com/docs/mcp/setup-clients)). Tools are read-only; adding or editing prompts happens in the app, not over MCP.

## Workflow

1. **Inventory.** Call `list_prompts` with `active: true`. Each prompt has `query_id`, `query_text`, `intent`, `tier`, `topic`, and `prompt_group`. Summarize the portfolio: counts by intent and topic.
2. **Baseline.** Call `get_visibility_overview` for the latest completed window to know the brand's average per-engine performance.
3. **Drill into suspect prompts.** For prompts the user cares about (or a sample of high-`tier` ones), call `get_prompt_visibility` with the `query_id`. Rows in `by_engine_location` break metrics down per engine and location; look for:
   - prompts with near-zero `mention_rate` everywhere (invisible)
   - prompts strong on one engine but absent on another (engine gap)
   - prompts that diverge sharply by location (localization gap)
   Read every conclusion alongside `n_runs`; thin run counts make weak evidence.
4. **Coverage gaps.** Compare the prompt inventory against how buyers actually ask: are commercial-intent prompts ("best X for Y", "X vs Y", "X alternatives") represented for each core topic? Which competitor comparisons are missing? Which customer questions from the user's domain knowledge have no tracked prompt?
5. **Deliver:**
   - **Weak prompt table**: prompt text, worst engine/location, mention rate, n_runs, suspected reason.
   - **Suggested prompts to add** (5-15), each with intent label and the reason it earns a slot. Remind the user to add them in the Citlyze app.

## Interpretation rules

- Treat `intent`, `tier`, `topic`, and `prompt_group` as the workspace's own labels; group by whatever values are present rather than assuming a fixed set.
- Zero visibility on a prompt is not automatically bad tracking; it may be the honest baseline the user needs to see.

Learn more: [Prompt results in Citlyze](https://www.citlyze.com/docs/using-citlyze/prompt-results) - [citlyze.com](https://www.citlyze.com)
