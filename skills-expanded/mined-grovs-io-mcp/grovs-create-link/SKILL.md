---
name: grovs-create-link
description: Create a tracking deep link for any campaign, product, or screen in your app. Add social previews, tags, and custom data to measure exactly where your traffic and installs come from. Use when the user wants to create a deep link, share link, or campaign link.
---

# Grovs: Create a Deep Link

## Key behaviors

- Default to the **production** project unless the user says "test."
- If you already have the project_id from earlier in this conversation, **don't re-call `get_status`**.
- `path` auto-generates from `name` — don't ask for it unless the user cares about the URL slug.
- `data` is the JSON payload the **app receives on open**. If the user says "link to the product page," ask what data their app needs to navigate there (e.g., `{"screen": "product", "id": "123"}`).
- `campaign_id` assigns the link to a campaign. If the user mentions a campaign by name, look up its numeric ID with `list_campaigns` first.
- The response includes the full shareable URL — present it prominently.

## Examples

User: "Create a link for our Summer Sale, it should go to the promo screen"

```
create_link(
  project_id: "p_m9f",
  name: "Summer Sale",
  data: {"screen": "promo", "sale_id": "summer-2026"},
  tags: ["marketing", "summer-2026"]
)
→ URL: https://foodies.grovs.io/summer-sale
```

User: "Create a link for the Summer Sale campaign"

```
1. list_campaigns(project_id: "p_m9f", term: "Summer Sale")  → finds campaign_id: 42
2. create_link(
     project_id: "p_m9f",
     name: "Summer Sale Banner",
     campaign_id: 42,
     data: {"screen": "promo"}
   )
→ URL: https://foodies.grovs.io/summer-sale-banner (assigned to campaign 42)
```

If the campaign doesn't exist yet and they're creating several related links, create it first:
```
create_campaign(project_id: "p_m9f", name: "Summer Sale 2026")  → campaign_id: 42
create_link(..., campaign_id: 42)  → first link
create_link(..., campaign_id: 42)  → second link
```

## If something fails

- Path already taken → the `path` slug must be unique per project. Suggest a different slug or let it auto-generate by omitting `path`.
- Invalid `image_url` → must be a valid URL (schema uses `z.url()`).

## After creation

Suggest anything the user skipped that would help:
- No tags → useful for filtering in analytics
- No title/image → improves social sharing (Open Graph)
- No data → app won't know which screen to open
- No campaign → suggest if they'll create more related links

## All tool responses are pre-formatted

Every Grovs tool returns human-readable formatted text. Don't reformat — just present and add context.
