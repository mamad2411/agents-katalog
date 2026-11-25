---
name: ad-creative-to-meta
description: When the user wants to take an Appeeky-generated ad creative and create a draft Meta ad — upload image, create creative, ad set, and ad. Use when the user mentions "publish Meta ad", "upload creative to Facebook", "listing to live Meta ad", "end-to-end Meta pipeline", or "create Facebook ad from creative". For generation only see meta-ad-creative. Requires mmp-setup before activation.
metadata:
  version: 1.0.0
---

# Listing → Meta Ad Pipeline

End-to-end pipeline: **App Store listing → Appeeky creative → Meta draft ad (PAUSED)**. User reviews tracking and creative before activation.

Automate the tedious steps. Never auto-activate without explicit user approval and verified MMP events.

## Prerequisites Checklist

| Requirement | Verify via |
|-------------|------------|
| Appeeky MCP connected | API key configured |
| Meta OAuth connected | `meta_ads_credentials_status` → connected |
| Default ad account | `meta_ads_list_ad_accounts` → `meta_ads_set_default_ad_account` |
| Facebook Page linked | `meta_ads_list_pages` |
| App in Events Manager | App ID + store URL |
| MMP live | `mmp-setup` — Purchase/Subscribe events last 7 days |
| Context doc | `app-ads-context.md` — CPA target, geo, budget |

```
meta_ads_credentials_status
```

If not connected:
```
meta_ads_oauth_start
```

## Pipeline Overview

Preferred path — one-shot PAUSED app-install draft:

```
1. generate_app_ad_creative  →  imageUrl + copy
2. meta_ads_upload_ad_image_from_url  →  image_hash
3. meta_ads_list_advertisable_applications + meta_ads_list_pages
4. meta_ads_create_app_install_draft  →  campaign + ad set + creative + ad
5. User review  →  manual activate
```

Manual path (when you need a shared ad set for multiple variants):

```
1. generate_app_ad_creative  →  imageUrl + copy
2. meta_ads_upload_ad_image_from_url  →  image_hash
3. meta_ads_create_campaign  →  campaign_id (if new)
4. meta_ads_create_adset  →  adset_id  (destination_type: APP)
5. meta_ads_create_creative  →  creative_id  (format: app_install, name required)
6. meta_ads_create_ad  →  ad_id
7. User review  →  manual activate
```

All entities created **PAUSED**. Writes cost **2 Appeeky API credits** each.

## Step 1 — Generate Creative

Single creative or batch from prior skills:

```
generate_app_ad_creative
  app_url: "https://apps.apple.com/us/app/id123456789"
  mode: "generate"
  style: "ugc"
  image_preset: "person_holding_phone"
  quality: "medium"
```

Poll:
```
get_app_ad_creative_job
  job_id: "<job-id>"
```

**Save:**
- `result.ad.imageUrl`
- `result.ad.copy.primaryText`
- `result.ad.copy.headline`
- `result.ad.copy.description`
- `result.ad.copy.callToAction`

For batches (`ad-creative-variants`), repeat upload + ad creation per variant.

## Step 2 — Upload Image to Meta

```
meta_ads_upload_ad_image_from_url
  ad_account_id: "act_1234567890"
  image_url: "https://cdn.appeeky.com/..."
```

Returns `image_hash` (or `imageHash`) — use in creative step.

| Error | Fix |
|-------|-----|
| Invalid URL | Ensure Appeeky CDN URL is public |
| Account mismatch | Verify `ad_account_id` |
| Token expired | Re-run OAuth |

## Preferred path by monetization

MCP default for `meta_ads_create_app_install_draft` is `APP_INSTALLS`. That is wrong for subscription/IAP apps — Meta will optimize for cheap installs, not paying users.

| App type | Path |
|----------|------|
| Subscription / IAP | **Manual** campaign → ad set with `OFFSITE_CONVERSIONS` + `custom_event_type` (below). Do not use the one-shot default. |
| Games / ad-supported | One-shot draft is fine. Pass `optimization_goal: "APP_INSTALLS"` explicitly. |

The one-shot tool does not accept `custom_event_type` on `promoted_object`. Use the manual ad set when optimizing to Purchase or Subscribe.

Use the manual campaign → ad set → creative → ad steps when attaching **multiple variants to one shared ad set**.

## Step 3 — Create Campaign (if new)

Skip if adding ads to existing test campaign — use known `campaign_id`.

```
meta_ads_create_campaign
  ad_account_id: "act_1234567890"
  name: "FocusApp - App Installs - US"
  objective: "OUTCOME_APP_PROMOTION"
  status: "PAUSED"
  is_adset_budget_sharing_enabled: false
```

### Campaign Settings Reference

| Setting | Recommended | Notes |
|---------|-------------|-------|
| Objective | `OUTCOME_APP_PROMOTION` | App installs + events |
| Buying type | Auction (default) | |
| CBO | Off for first test | Ad set budget per test |
| Status | `PAUSED` | Always |

List existing:
```
meta_ads_list_campaigns
  ad_account_id: "act_1234567890"
```

## Step 4 — Create Ad Set

```
meta_ads_create_adset
  ad_account_id: "act_1234567890"
  campaign_id: "<campaign-id>"
  name: "US - iOS - Creative Test"
  daily_budget_minor: 5000
  billing_event: "IMPRESSIONS"
  optimization_goal: "OFFSITE_CONVERSIONS"
  destination_type: "APP"
  promoted_object: {
    "application_id": "<meta-app-id>",
    "object_store_url": "https://apps.apple.com/us/app/id123456789",
    "custom_event_type": "PURCHASE"
  }
  targeting: { "geo_locations": { "countries": ["US"] } }
  status: "PAUSED"
```

Use `SUBSCRIBE` if that is the primary MMP event. Meta rejects `OFFSITE_CONVERSIONS` without `custom_event_type`.

### Ad Set Settings Reference

| Setting | Test value | Scale value |
|---------|------------|-------------|
| Daily budget | $30–50 (3000–5000 minor) | +20%/day on winners |
| Optimization | `OFFSITE_CONVERSIONS` + `custom_event_type` Purchase or Subscribe | Not `APP_INSTALLS` or Link Clicks |
| Destination | `APP` (`destination_type`) | Never leave default `WEBSITE` |
| Geo | US first | Expand after 7d stable CPA |
| Placements | Advantage+ ON | |
| Age | 18–65+ or app-specific | |
| Audience | Broad | LAL after 100+ converters |

### iOS 14+ Notes

- AEM + SKAN: expect delayed reporting
- Trust MMP over Meta dashboard for iOS CPA
- Do not pause winners at 24h on iOS alone

### Android Notes

- Google Play URL in `object_store_url`
- Same structure; often faster conversion feedback

## Step 5 — Create Ad Creative

```
meta_ads_create_creative
  ad_account_id: "act_1234567890"
  format: "app_install"
  name: "FocusApp - VarA - Problem"
  page_id: "<facebook-page-id>"
  link_url: "https://apps.apple.com/us/app/id123456789"
  message: "<primaryText from Appeeky>"
  headline: "<headline from Appeeky>"
  description: "<description from Appeeky>"
  image_hash: "<from step 2>"
  call_to_action_type: "INSTALL_MOBILE_APP"
```

`name` is required. Default `format` is `"link"` — set `"app_install"` for store-install ads.

### Creative Field Mapping

| Appeeky field | Meta field |
|---------------|------------|
| `copy.primaryText` | `message` |
| `copy.headline` | `headline` |
| `copy.description` | `description` (optional) |
| `copy.callToAction` | `call_to_action_type` |
| `imageUrl` → hash | `image_hash` |

## Step 6 — Create Ad

```
meta_ads_create_ad
  ad_account_id: "act_1234567890"
  adset_id: "<adset-id>"
  creative_id: "<creative-id>"
  name: "FocusApp - VarA - Problem - 20250629"
  status: "PAUSED"
```

Repeat steps 2, 5, 6 for each variant in a batch (shared campaign + ad set).

## Step 7 — User Review

Present summary. **Do not activate** until checklist complete.

```
meta_ads_list_ads
  ad_account_id: "act_1234567890"
```

## Output Template

```markdown
# Meta Ad Draft Created — [App Name]

**Status:** All entities PAUSED — awaiting your approval

| Entity | Name | ID | Status |
|--------|------|-----|--------|
| Campaign | FocusApp - App Installs - US | [id] | PAUSED |
| Ad Set | US - iOS - Creative Test | [id] | PAUSED |
| Creative | VarA - Problem | [id] | — |
| Ad | FocusApp - VarA - Problem | [id] | PAUSED |

## Copy Used
| Field | Value |
|-------|-------|
| Primary text | ... |
| Headline | ... |
| Description | ... |
| CTA | INSTALL_MOBILE_APP |

## Creative
- **Image preview:** [imageUrl]
- **Image hash:** [hash]

## Budget & Targeting
- **Daily budget:** $50
- **Geo:** US
- **Optimization:** Purchase
- **Placements:** Advantage+

## Before Activating
- [ ] MMP Purchase/Subscribe events in last 7 days (mmp-setup)
- [ ] Meta Events Manager shows app events
- [ ] User reviewed creative + copy
- [ ] iOS SKAN delay expectations set
- [ ] Target CPA documented in app-ads-context.md

## Activate (user confirms)
```
meta_ads_update_ad
  ad_id: "<id>"
  status: "ACTIVE"

meta_ads_update_adset
  adset_id: "<id>"
  status: "ACTIVE"

meta_ads_update_campaign
  campaign_id: "<id>"
  status: "ACTIVE"
```

## 48h Follow-up
→ meta-campaign-audit
```

## Batch Pipeline (5 variants)

| Step | Action |
|------|--------|
| 1 | One `generate` batch (or 5 prior jobs) |
| 2 | 5× `upload_ad_image_from_url` |
| 3 | 1× campaign, 1× ad set |
| 4 | 5× creative + 5× ad |

Total write credits: ~(2 × 12) = ~24 API credits for full batch setup.

## Error Reference

| Error | Cause | Fix |
|-------|-------|-----|
| OAuth not connected | Missing Meta token | `meta_ads_oauth_start` |
| No Page | Page not linked to account | Connect Page in Business Settings |
| Invalid app link | Wrong store URL format | Use full App Store / Play URL |
| `application_id` invalid | App not in Events Manager | Add app in Meta Events Manager |
| Policy rejection | Claims in copy | Soften primary text; review guidelines |
| Budget too low | Below Meta minimum | Raise `daily_budget_minor` |
| Creative rejected | Image text % / content | Edit via `ad-creative-edit` |

## REST API Equivalents

Base: `https://api.appeeky.com/v1/connect/meta-ads/`

MCP tools hit the un-nested paths and pass `ad_account_id`. Nested aliases also exist.

| MCP tool | REST |
|----------|------|
| `meta_ads_create_campaign` | `POST /campaigns` or `POST /ad-accounts/:adAccountId/campaigns` |
| `meta_ads_create_adset` | `POST /adsets` |
| `meta_ads_create_creative` | `POST /creatives` |
| `meta_ads_upload_ad_image_from_url` | `POST /adimages/from-url` |
| `meta_ads_create_app_install_draft` | `POST /app-install-drafts` |

See [appeeky-meta-ads.md](../../tools/integrations/appeeky-meta-ads.md).

## Common Mistakes

| Mistake | Risk | Fix |
|---------|------|-----|
| Auto-activating | Spend without tracking | Always PAUSED first |
| Optimizing for installs only | Low-quality users | Optimize Purchase/Subscribe |
| Separate ad sets per variant (day 1) | Bad comparison | One ad set for test |
| Wrong `object_store_url` | Broken deep link | Match platform to ad set |
| Skipping image re-upload after edit | Stale creative | Re-upload on every edit |
| No ad naming convention | Audit chaos | Use VarA/B/C pattern |

## Pre-Flight Checklist

```
Appeeky:
- [ ] Creative job completed
- [ ] imageUrl + copy extracted

Meta auth:
- [ ] credentials_status connected
- [ ] Default ad account set
- [ ] Page ID confirmed

Tracking:
- [ ] mmp-setup complete
- [ ] promoted_object application_id correct

Pipeline:
- [ ] All entities PAUSED
- [ ] User has summary + preview
- [ ] 48h audit scheduled
```

## Related Skills

- `meta-ad-creative` — step 1 generation
- `ad-creative-variants` — batch before pipeline
- `ad-creative-edit` — fix creative before upload
- `meta-campaign-setup` — manual setup reference
- `mmp-setup` — prerequisite before activation
- `meta-campaign-audit` — 48h performance review
- `meta-budget-optimizer` — post-launch budget rules
