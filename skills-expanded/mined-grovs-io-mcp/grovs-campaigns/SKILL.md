---
name: grovs-campaigns
description: Group deep links into campaigns to track marketing efforts as a whole — create campaigns, list them with aggregated metrics (views, opens, installs, revenue), and archive old ones. Use when the user wants to organize links by campaign, see campaign-level performance, or clean up old campaigns.
---

# Grovs: Manage Campaigns

## What a campaign is

A grouping of links — nothing more. No config, no settings. You create it, attach links via `campaign_id`, then `list_campaigns` shows aggregated metrics (views, opens, installs, revenue) across all links in that campaign.

## Hard limitations

- **No rename.** Name is permanent.
- **No unarchive.** `archive_campaign` deactivates all links permanently. **Always confirm with the user.**
- **No "get single campaign."** Use `list_campaigns` with `term: "name"` to find one.
- **No delete without archive.** Archive is the only way to remove.

## Typical workflow

```
create_campaign(project_id: "p_m9f", name: "Summer Sale 2026")     → campaign_id: 42
create_link(project_id: "p_m9f", name: "Banner Ad", campaign_id: 42)
create_link(project_id: "p_m9f", name: "Email CTA", campaign_id: 42)
...later...
list_campaigns(project_id: "p_m9f", sort_by: "revenue")            → see all campaigns ranked
```

## Pagination

`list_campaigns` paginates — returns `meta.page`, `meta.total_pages`. If user says "show more," call again with `page: current + 1` using the same filters.

## When to suggest campaigns proactively

- User is about to create 2+ related links → "Want to group these in a campaign so you can track them together?"
- User asks "which campaign is doing best" → `list_campaigns` with `sort_by: "revenue"` or `sort_by: "installs"`
- User wants a link-level breakdown within a campaign → use `search_links` (shows per-link metrics) — there's no campaign-scoped link search, so search by tag or name pattern

## If something fails

- "Campaign not found" on archive → campaign_id is a **number**, not a string. Check you're passing the numeric ID from `list_campaigns`.

## All tool responses are pre-formatted

Every Grovs tool returns human-readable formatted text. Don't reformat — just present and add context.
