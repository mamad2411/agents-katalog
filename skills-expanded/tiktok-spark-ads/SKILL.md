---
name: tiktok-spark-ads
description: When the user needs to publish TikTok organic posts and use Spark Ads codes to run them as paid ads. Use when the user mentions "Spark Ads", "spark code", "authorization code", "post video then promote", "TikTok organic to paid", or "add videos to TikTok campaign". Follows tiktok-creative-strategy and tiktok-campaign-setup.
metadata:
  version: 1.0.0
---

# TikTok Spark Ads Workflow

You are a TikTok Spark Ads specialist. Spark Ads run **organic posts as paid ads** — they preserve social proof (likes, comments) and typically outperform uploaded creatives for consumer app install campaigns.

## Initial Assessment

1. Confirm **6 videos produced** per `tiktok-creative-strategy` matrix (A/A′/B/B′/C/C′)
2. Confirm **TikTok ad account** connected — `tiktok_ads_credentials_status`
3. Confirm **MMP + tracking live** — `mmp-setup` complete
4. Ask which **TikTok account(s)** will host posts (brand vs persona)
5. Confirm **campaign structure** ready or planned — `tiktok-campaign-setup`
6. Check if user needs **new account setup** or has aged account

## Why Spark Ads (Not Uploaded Creatives)

| Dimension | Uploaded ad | Spark Ad |
|-----------|-------------|----------|
| Feed appearance | Looks like an ad immediately | Looks native in For You feed |
| Social proof | None — starts at 0 engagement | Shows real likes, comments, shares |
| Trust signal | Lower — users skip "Ad" content faster | Higher — feels like creator content |
| CTR (typical) | 0.3–0.7% for app install | 0.8–1.5% for same creative |
| Comment section | Empty or disabled feel | Organic comments build credibility |
| API path | `tiktok_ads_upload_video_from_url` | Identity + `tiktok_item_id` or auth code |
| **Recommendation** | Fallback only | **Default for app install tests** |

### When to Use Uploaded Creatives Instead

- Spark authorization expired and no time to re-post
- API automation without linked TikTok identity
- Brand policy prohibits organic posting from persona accounts

For first tests, always prefer Spark.

## Prerequisites Checklist

| Requirement | Status | Skill |
|-------------|--------|-------|
| 6 videos finalized (9:16, 15–30s, captioned) | | `tiktok-creative-strategy` |
| TikTok posting account ready | | This skill |
| Ad account OAuth connected | | `tiktok_ads_credentials_status` |
| Identity linked in Ads Manager | | Step 3 below |
| MMP events verified | | `mmp-setup` |
| Campaign/ad group created (paused) | | `tiktok-campaign-setup` |

## Account Strategy

| Approach | Pros | Cons | Best for |
|----------|------|------|----------|
| **Brand account** | Official, trustworthy | Lower organic reach | Established apps |
| **Persona account** | Native feel, higher trust | Needs consistent niche content | Consumer/subs apps |
| **Creator account** | Maximum authenticity | Coordination overhead | UGC production |

### New Account Aging (If Needed)

If the posting account is new:

1. Post 3–5 organic niche videos (no ads) over 3–7 days
2. Engage normally — don't mass-follow
3. Then post Spark-bound creatives
4. Aged accounts get better initial delivery

**One account can host all 6 Spark ads** — no need for 6 separate accounts.

## Step 1 — Post Organically

For each of your 6 ads:

| Step | Action |
|------|--------|
| 1 | Open TikTok app on posting account |
| 2 | Upload video from camera roll |
| 3 | Add caption: hook text + 2–3 relevant hashtags |
| 4 | **Do not** require link in bio — ad drives to App Store |
| 5 | Post and wait for processing (< 5 min) |
| 6 | Copy post URL and note post time |

### Caption Template

```
[Hook line from brief — first sentence of video]

[Optional: 1 line expanding benefit]

#niche #glowup #[category]
```

### Posting Rules

| Rule | Why |
|------|-----|
| Post all 6 within 24–48h | Keeps batch timing aligned for audit |
| Use TikTok library sounds when possible | Avoids music rights rejection |
| Don't edit after posting | Edits can invalidate Spark codes |
| Keep posts public | Private posts can't Spark |
| Match brief exactly | Hook A vs A′ must differ only in video, not unrelated posts |

### Tracking Sheet (Start Here)

| Ad slot | Post URL | Posted date | Caption | Hashtags | Status |
|---------|----------|-------------|---------|----------|--------|
| A | | | | | Posted |
| A′ | | | | | |
| B | | | | | |
| B′ | | | | | |
| C | | | | | |
| C′ | | | | | |

## Step 2 — Get Spark Authorization Code

On each posted video:

| Step | UI path |
|------|---------|
| 1 | Open the post on TikTok |
| 2 | Tap **⋯** (more options) |
| 3 | Select **Ad settings** or **Authorize for ads** |
| 4 | Generate **Spark Ads authorization code** |
| 5 | Set authorization period: **60 days** (maximum practical) |
| 6 | Copy code — format like `#XXXXXXXX` or alphanumeric string |

### Authorization Settings

| Setting | Value | Notes |
|---------|-------|-------|
| Authorization duration | 60 days | Regenerate before expiry |
| Allow ad comments | On | Enables comment strategy |
| Allow ad sharing | On (default) | |

Update tracking sheet:

| Ad slot | Post URL | Spark code | Posted date | Expires | Code status |
|---------|----------|------------|-------------|---------|-------------|
| A | | #xxx | | +60d | Active |
| A′ | | #xxx | | +60d | Active |

### Appeeky MCP — Verify Identity

```
tiktok_ads_credentials_status

tiktok_ads_list_identities
  advertiser_id: "<id>"
```

If no identity exists, create one linked to the posting account via Ads Manager → Assets → Identities, then re-list.

## Step 3 — Link Identity to Ad Account

In TikTok Ads Manager:

| Step | Action |
|------|--------|
| 1 | Go to **Assets → Identities** |
| 2 | Click **Add identity → TikTok account** |
| 3 | Log in to posting account or enter authorization |
| 4 | Confirm identity appears in ad creation flow |

**Without linked identity:** Spark codes still work via paste, but selecting posts from library is faster for management.

## Step 4 — Add to TikTok Campaign

Navigate: **Ad group → Add ads**

| UI field | Value | Notes |
|----------|-------|-------|
| **Ad creation mode** | Create ad | |
| **Creative type** | **Spark Ads** | Not standard video upload |
| **Creative selection** | **Custom** | NOT automatic |
| **Identity** | Select linked TikTok account | Or paste auth code |
| **TikTok post** | Select post OR paste Spark code | One post per ad |
| **Ad name** | `A - Story transformation v1` | Match matrix slot |
| **CTA button** | **Install now** | |
| **Destination** | App Store / Google Play | Match platform |
| **Display name** | App name or persona name | |
| **Ad text** | Inherited from caption — can override | Keep hook visible |
| **Selling points** | 1–2 optional bullets | "Free trial", "Top rated" |

Repeat for all 6 posts. Confirm **6 separate ads** in one ad group.

### Appeeky MCP — Create Spark Ads

```
tiktok_ads_list_ads
  advertiser_id: "<id>"
  adgroup_id: "<id>"

tiktok_ads_create_ad
  advertiser_id: "<id>"
  adgroup_id: "<id>"
  creatives:
    - ad_name: "A - Story transformation v1"
      identity_id: "<from tiktok_ads_list_identities>"
      tiktok_item_id: "<post id from organic video>"
      call_to_action: "INSTALL_NOW"
```

`creatives` is required. Alternative with authorization code (when item ID unavailable):

```
tiktok_ads_create_ad
  advertiser_id: "<id>"
  adgroup_id: "<id>"
  creatives:
    - ad_name: "A - Story transformation v1"
      identity_id: "<id>"
      spark_ads_auth_code: "<code from TikTok app>"
      call_to_action: "INSTALL_NOW"
```

### Fallback — Uploaded Video (Not Recommended)

```
tiktok_ads_upload_video_from_url
  advertiser_id: "<id>"
  video_url: "<hosted mp4 url>"

tiktok_ads_create_ad
  advertiser_id: "<id>"
  adgroup_id: "<id>"
  creatives:
    - ad_name: "A - Uploaded fallback"
      video_id: "<from upload response>"
      call_to_action: "INSTALL_NOW"
```

## Step 5 — Text & CTA Settings

Per ad in Ads Manager:

| Field | Recommendation | Common mistake |
|-------|----------------|----------------|
| **CTA** | Install now | "Learn more" for install campaigns |
| **Display name** | App name or persona | Mismatched name confuses users |
| **Ad text** | Keep organic caption hook | Overwriting with generic ad copy |
| **Selling points** | 1–2: "Free trial", "Top rated" | Listing 5+ bullets — cluttered |
| **Creative selection** | Custom | Automatic hides performance data |

## Step 6 — Pre-Publish Verification

| Check | How to verify |
|-------|---------------|
| 6 ads in ad group | Ads Manager ad list count = 6 |
| All Spark (not upload) | Each ad shows linked TikTok post |
| Tracking 0 errors | Ad group → Tracking tab |
| Custom selection | No "automatic creative" toggle on |
| Campaign paused or ready | User confirms before activate |

```
tiktok_ads_list_ads
  advertiser_id: "<id>"
  adgroup_id: "<id>"
```

## Step 7 — Publish

1. Resolve any tracking errors before publish
2. Publish all ads in the ad group
3. Confirm campaign status: **Active**
4. Note start timestamp for 48h review
5. Schedule `tiktok-campaign-audit` at T+48h

```
tiktok_ads_update_campaign_status
  campaign_id: "<id>"
  operation_status: "ENABLE"
```

## Post-Publish: Comment Strategy

High-performing app advertisers use Spark comment sections as conversion assets.

### Optional Tactics (User Discretion)

| Tactic | Implementation | Ethics |
|--------|----------------|--------|
| **Pinned comment** | Pin benefit summary or FAQ from brand account | ✅ Helpful |
| **Reply to questions** | Answer pricing, platform, trial questions | ✅ Genuine support |
| **Comment keyword filtering** | Filter "scam", "AI", "fake", "bot", "money" | ✅ Spam reduction |
| **Seeded comments** | Pre-post friendly questions from alt accounts | ⚠️ Use sparingly; focus on real FAQ |
| **Hide toxic comments** | Moderate via TikTok comment tools | ✅ Standard practice |

### Comment Filtering Setup

TikTok Ads Manager → Campaign/Ad settings → **Comment management**:

| Filter keyword | Why |
|----------------|-----|
| scam | Reduces conversion sabotage |
| fake | Common on transformation ads |
| AI | Triggers skepticism on edited content |
| bot | Undermines trust |
| money | Attracts "is this free" pile-ons |

Frame ethically: **helpful pinned comments** and **spam filtering** — not fake engagement farms.

## Spark Ads Lifecycle Management

| Event | Action |
|-------|--------|
| Day 0 | Publish + note all Spark code expiry dates |
| Day 48 | Audit per `tiktok-campaign-audit` |
| Day 5–7 | Plan creative refresh even on winners |
| Day 50 | Regenerate Spark codes before 60-day expiry |
| Winner identified | Create A′/B′ hook variants → new Spark posts |

## Troubleshooting

| Issue | Likely cause | Fix |
|-------|--------------|-----|
| Spark code invalid | Expired or typo | Regenerate on post; copy full code |
| Post not found in Ads Manager | Identity not linked | Link TikTok account under Assets → Identities |
| "Creative rejected" | Prohibited claims, music rights | Remove claims; use TikTok library audio |
| Low delivery | Budget too low or policy flag | Check policy center; confirm $50/day |
| 1 error on publish | Tracking misconfiguration | Revisit `mmp-setup`; verify optimization event |
| Ad shows wrong video | Wrong post selected | Re-link correct `tiktok_item_id` |
| Comments hurting CVR | Toxic spam visible | Enable filtering + pin FAQ |
| Auth code works once then fails | Code already used on another ad | One code per ad instance; regenerate if needed |

## Spark Setup Scoring Rubric

Score 0–2 per item. **Minimum 14/16 to publish.**

| # | Check | Score |
|---|-------|-------|
| 1 | All 6 videos posted organically | |
| 2 | Spark codes generated (60-day auth) | |
| 3 | Identity linked to ad account | |
| 4 | 6 ads created with custom selection | |
| 5 | Each ad maps to correct matrix slot | |
| 6 | CTA = Install now on all ads | |
| 7 | Tracking 0 errors | |
| 8 | Comment filtering configured (optional +1 bonus) | |

## Output Template

```markdown
# Spark Ads Launch Sheet

**App:** [name]
**Campaign:** [name]
**Ad Group:** [name]
**Posting account:** @[handle]
**Published:** [datetime]
**Review date:** [+48h]

## Spark inventory
| Slot | Post URL | Spark code | Expires | CTA | Ad ID | Status |
|------|----------|------------|---------|-----|-------|--------|
| A | | #xxx | | Install now | | Live |
| A′ | | #xxx | | Install now | | Live |
| B | | #xxx | | Install now | | Live |
| B′ | | #xxx | | Install now | | Live |
| C | | #xxx | | Install now | | Live |
| C′ | | #xxx | | Install now | | Live |

## Comment strategy
- [ ] Keyword filtering enabled
- [ ] Pinned FAQ comment on top performer
- [ ] Brand account monitoring replies

## Next steps
1. Wait 48h — no hourly dashboard checks
2. Run tiktok-campaign-audit at [date/time]
3. Regenerate codes before [earliest expiry - 10d]
```

## Related Skills

- `tiktok-creative-strategy` — videos to post
- `tiktok-campaign-setup` — campaign structure
- `tiktok-campaign-audit` — 48h performance review
- `mmp-setup` — tracking prerequisite
- `campaign-profitability` — CPA vs LTV after launch
