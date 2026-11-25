---
name: morning-brief
description: Assemble the user's daily brief from Graphory by querying graph stats, recent activity, stale entities, the prebuilt weekly digest, warm-intro candidates, and the pending review queue, then render the result as a clean structured brief. Trigger on phrasings like "morning brief", "brief me", "what's on for today", "catch me up", "Monday rollup", or whenever a scheduled job invokes this skill at the start of the user's day.
---

# morning-brief

This skill assembles a daily situational-awareness brief for the user from their Graphory graph. It's read-only and runs entirely on your own AI - Graphory provides the structured data, the agent (you) does the synthesis and rendering, at zero added inference cost.

The brief should feel like a chief-of-staff handing the user a one-page rundown over coffee: what's new, what's slipping, what to look at, what to act on. Not a data dump.

## When to trigger

Run this skill when the user says:

- "Morning brief" / "brief me" / "what's on for today"
- "Catch me up" / "what did I miss"
- "Monday rollup" / "weekly digest"
- "What should I look at first today"

Or when a scheduled hook fires the skill at a fixed time (e.g. 7am cron / Shortcuts automation / launchd job pointing your AI at this skill).

## Required tools (Graphory MCP)

Call these in roughly this order. Most can run in parallel - fire them concurrently when your runtime supports it:

| Tool                                            | Purpose                                                |
|-------------------------------------------------|--------------------------------------------------------|
| `graph_stats()`                                 | Headline numbers (item count, sources connected)       |
| `get_weekly_digest()`                           | Prebuilt digest of the last 7 days                     |
| `timeline(days=1)`                              | Yesterday + today's activity feed                      |
| `get_stale_entities(days=14)`                   | Contacts with no activity in 14+ days                  |
| `get_latent_connections(entity_id=<top entity>, limit=5)` | Same-community pairs not directly connected (warm intros) for the day's most active entity |
| `get_suggestions(status="pending", limit=10)`   | Top of the review queue                                |
| `connection_health()` *(only if user asks "any issues")* | Surface broken sources                          |

Don't invoke any of these unless your output template needs them. If the user has < 100 items in their graph (brand new), skip the digest and stale checks - they'll be empty/noise.

Note on warm intros: `get_latent_connections` requires a concrete `entity_id` - there is no global form. Derive the day's single most active entity from the `timeline(days=1)` results (the entity appearing most often in the activity feed), then call `get_latent_connections(entity_id=<that entity id>, limit=5)` for it. If no entity is clearly active, skip the warm-intros section entirely. (`dossier(entity=<that>, include_latent=True)` also returns latent connections and is an equally valid path, as long as it's pointed at a concrete entity.)

## The brief

Render the brief from `templates/brief.md` (in this folder). Fill in each section from the corresponding tool result, in plain business language - no internal vocabulary (no "node", "edge", "Activity", "Contact", etc.). The full vocabulary translation rules live at https://docs.graphory.io/mcp.

Section order (matches the template):

1. **Headline** - one sentence. "Quiet day - 3 new items overnight." or "Busy week kicking off - 47 new items, 2 connection issues."
2. **Yesterday in 3 bullets** - from `timeline(days=1)`. Pick the 3 most signal-rich items, not all of them.
3. **Worth your attention** - from `get_weekly_digest()` + `get_stale_entities()`. Things drifting. People you haven't followed up with. Commitments past due.
4. **Warm intros available** - from `get_latent_connections(entity_id=<day's most active entity>, limit=5)`. Surface 1-3, not all 5. Skip this section if no entity was clearly active in `timeline(days=1)`.
5. **Review queue** - from `get_suggestions(status="pending")`. If > 5 pending, say "5 of N pending" and offer to walk them via the cleanup-stale skill.
6. **Suggested first move** - one sentence. The highest-leverage thing to do right now based on what you saw.

## Length budget

- Total brief: 200-400 words.
- Each bullet: one line, two max.
- No tables unless the data is genuinely tabular.
- No "executive summary" / "introduction" / "conclusion" headers - the sections above ARE the structure.

If you can't fit something in 400 words, cut the lowest-signal section, don't shrink the font.

## Example output

```
Headline: Active week ahead - 28 new items overnight, mostly Slack and Gmail.

Yesterday in 3 bullets
- Stripe payment from Northwind cleared ($12k)
- Sarah Chen sent a follow-up on the Q2 contract - still unanswered
- 4 new commits landed on the billing-refactor branch

Worth your attention
- You haven't talked to Geolo Capital in 17 days; their last email asked
  about Q3 timing
- The Acme RFP deadline is Friday - no draft yet
- Two invoices from last month still unpaid

Warm intros available
- Marcus Lee (your Cloze) and David Park (your Gmail) are both at Helix
  Ventures and you haven't directly connected them

Review queue
- 3 pending merge suggestions, 2 unresolved name mentions. Want me to walk
  the queue?

Suggested first move
- Reply to Sarah Chen on the Q2 contract - that's the unblocked path to
  closing this month.
```

## Safety rails

- **Read-only.** This skill never writes to the graph. If the user wants to act on something in the brief, that's a separate tool call (save_message, write_to_graph, etc.).
- **Don't fabricate.** If a section comes back empty, omit it - don't invent "you have a busy day ahead" filler.
- **Never expose internals.** Graph IDs, node labels, edge types, confidence scores - none of these belong in the brief. Translate to plain business language.
- **One brief per day.** If the user runs `morning-brief` twice in one day, lead with "Already briefed you at 7:14am - here's what's changed since:" and only show the delta.
- **Skip if the graph is empty.** If `graph_stats` shows zero items, the brief is "Your graph is empty. Connect a data source and I'll have something for you tomorrow." Stop there.
