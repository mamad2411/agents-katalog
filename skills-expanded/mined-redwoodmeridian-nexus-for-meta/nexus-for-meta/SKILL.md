---
name: nexus-for-meta
description: >-
  Query and manage a firm's own Meta marketing assets — Facebook Ads, Pages,
  Instagram, and Lead forms — through the Graph API. Use whenever the user asks
  about ad performance, spend, leads, audiences, creatives, best/worst ads, page
  or Instagram stats, or wants to create/edit/pause campaigns. Talks to
  graph.facebook.com directly with curl + their access token (no MCP, no SDK).
---

# Nexus for Meta — Recipes

All calls go through `./scripts/meta <path> "<query>"`. The token is loaded from
`.env` automatically. Base API version is `v25.0`.

If `META_AD_ACCOUNT` is set in `.env`, use it as the default ad account; otherwise
discover accounts with the first recipe and ask the user which one.

---

## Discover what you can reach

```bash
./scripts/meta me "fields=id,name"
./scripts/meta me/adaccounts "fields=account_id,name,account_status"
./scripts/meta me/accounts "fields=id,name"        # Facebook Pages
```

---

## Ads — performance

Account overview (last 30 days). Note `actions` is an array; pull `lead`,
`link_click`, etc. from it.

```bash
./scripts/meta act_ACCOUNT/insights \
  "date_preset=last_30d&fields=spend,impressions,reach,clicks,cpc,cpm,ctr,actions,cost_per_action_type"
```

Lifetime (use this if last_30d is empty — the account may have no recent spend):

```bash
./scripts/meta act_ACCOUNT/insights "date_preset=maximum&fields=spend,impressions,clicks,actions"
```

Per campaign / ad set / ad — change `level`:

```bash
./scripts/meta act_ACCOUNT/insights \
  "date_preset=last_30d&level=campaign&fields=campaign_name,spend,clicks,ctr,actions&limit=100"
./scripts/meta act_ACCOUNT/insights \
  "date_preset=last_30d&level=ad&fields=ad_id,ad_name,adset_name,spend,clicks,ctr,actions&limit=200"
```

**Cost per lead** = `spend` ÷ the `lead` value inside `actions`. Compute it
yourself per row; Meta doesn't return it directly.

Structure (names, status, budgets):

```bash
./scripts/meta act_ACCOUNT/campaigns "fields=name,status,effective_status&limit=100"
./scripts/meta act_ACCOUNT/adsets "fields=name,status,daily_budget&limit=100"
./scripts/meta act_ACCOUNT/ads "fields=name,status,adset_id&limit=200"
```

---

## Best ad → viewable link (Instagram preferred)

1. Rank ads by spend + leads from the `level=ad` insights call above.
2. For the winner, pull its creative's links:

```bash
./scripts/meta AD_ID "fields=name,creative{id,instagram_permalink_url,effective_object_story_id,object_type,title}"
```

3. Give the user `instagram_permalink_url` (opens on Instagram). If it's absent,
   build the Facebook post URL from `effective_object_story_id`
   (`{page-id}_{post-id}` → `https://www.facebook.com/{post-id}`), or generate a
   preview:

```bash
./scripts/meta AD_ID/previews "ad_format=INSTAGRAM_STANDARD"
```

---

## Leads (needs a PAGE token — use `--page`)

Page-level endpoints reject the user token with error 190. Pass `--page PAGE_ID`
and the script fetches that Page's own token for you:

```bash
# 1. find the page
./scripts/meta me/accounts "fields=id,name"
# 2. list lead forms + counts
./scripts/meta --page PAGE_ID PAGE_ID/leadgen_forms "fields=name,status,leads_count&limit=50"
# 3. pull actual leads from a form
./scripts/meta --page PAGE_ID FORM_ID/leads "fields=created_time,field_data&limit=100"
```

---

## Pages & Instagram

```bash
# Page basics
./scripts/meta PAGE_ID "fields=name,fan_count,followers_count,category"
# Page posts (PAGE token — use --page)
./scripts/meta --page PAGE_ID PAGE_ID/posts "fields=message,created_time,permalink_url&limit=10"
# Instagram account linked to the page
./scripts/meta PAGE_ID "fields=instagram_business_account{id,username,followers_count,media_count}"
# Instagram media
./scripts/meta IG_ID/media "fields=caption,like_count,comments_count,permalink,timestamp&limit=20"
```

Page insights metric names change between API versions — if a metric errors,
ask for the current name rather than guessing. The token itself is fine.

---

## Audiences & creatives

```bash
./scripts/meta act_ACCOUNT/customaudiences "fields=name,approximate_count,subtype&limit=50"
./scripts/meta act_ACCOUNT/adcreatives "fields=name,object_type,thumbnail_url&limit=50"
```

---

## Writes — campaigns, ad sets, ads (CONFIRM FIRST)

These spend money or change live delivery. Follow the safety rule in CLAUDE.md:
describe the exact action and dollar amounts, get an explicit yes, then run it.

Writes go through the same script with `--post`. Values are form-encoded, so
spaces, commas and braces are safe:

```bash
# Example: create a PAUSED campaign (does NOT spend until activated)
./scripts/meta --post act_ACCOUNT/campaigns \
  "name=My Campaign&objective=OUTCOME_LEADS&status=PAUSED&special_ad_categories=[]"
```

Always create as `status=PAUSED` first so nothing goes live by accident. Pausing
an existing object:

```bash
./scripts/meta --post CAMPAIGN_ID "status=PAUSED"
```

Deleting:

```bash
./scripts/meta --delete ADSET_ID
```
