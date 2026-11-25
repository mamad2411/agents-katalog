---
name: grovs-manage-links
description: Search, list, and update your existing tracking links — change metadata, tags, redirects, campaign assignment, or custom data on any link without leaving your editor. Use when the user wants to find, list, update, or organize their links.
---

# Grovs: Manage Links

## ID types — this is where LLMs mess up

| What the user gives you | What you need | How to get it |
|------------------------|---------------|---------------|
| Link name or URL | numeric `link_id` | `search_links` → use the `id` field from results |
| Full URL or path slug | link details | `get_link` with `path` (accepts both) |
| Wants to update | numeric `link_id` | from `search_links` or `get_link` response |

**`get_link` accepts a full URL (`https://myapp.grovs.io/summer-sale`) or just the slug (`summer-sale`) — the server extracts the path. `update_link` takes a numeric ID. Never pass a path to `update_link`.**

## Key behaviors

- If you already have the project_id from this conversation, **skip `get_status`**.
- `search_links` returns metrics (views, opens, installs) per link — useful for quick performance checks without the analytics tools.
- `update_link` is a partial update — only send fields the user wants to change.
- To assign a link to a campaign: pass `campaign_id` in `update_link`.

## Archiving links

`archive_link` permanently deactivates a link — it stops redirecting users. **This cannot be undone. Always confirm with the user before calling.**

`archive_link` takes `project_id` + numeric `link_id` (not a path slug). If the user says "delete the summer-sale link," you need to look up the numeric ID first via `search_links` or `get_link`.

## Pagination

`search_links` returns paginated results with `meta.page`, `meta.total_pages`, and `meta.total_entries`. If the user says "show more" or "next page," call `search_links` again with `page: current + 1` using the same filters.

## Example

User: "Change the summer sale link to point to the new promo screen"

```
1. search_links(project_id: "p_m9f", search: "summer sale")
   → finds: {id: 42, name: "Summer Sale", path: "summer-sale", ...}
2. update_link(project_id: "p_m9f", link_id: 42, data: {"screen": "new-promo"})
   → updated
```

## If something fails

- "Link not found" on `get_link` → the path slug might be wrong. Use `search_links` with a search term instead.
- `update_link` with an invalid `link_id` → re-check by searching first.

## All tool responses are pre-formatted

Every Grovs tool returns human-readable formatted text. Don't reformat — just present and add context.
