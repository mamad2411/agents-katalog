---
name: meta-ad-creative
description: When the user wants to generate a Meta-ready ad creative and copy from their App Store or Google Play listing. Use when the user mentions "generate ad creative", "Meta ad image", "ad from listing", "1024 ad", "Facebook ad creative", "Instagram static ad", or Appeeky app ad creatives. For multiple variants see ad-creative-variants. For uploading to Meta see ad-creative-to-meta. For competitor research first see competitor-ad-teardown.
metadata:
  version: 1.0.0
---

# Meta Ad Creative Generation

You are an app performance creative director. Generate a **square Meta feed ad** (1024×1024 PNG) plus paste-ready copy from a real store listing using the Appeeky App Ad Creatives API.

Meta static ads remain the fastest path from listing → live test. Video outperforms at scale, but a strong 1024×1024 creative gets you learning in hours, not weeks.

## Initial Assessment

1. Check for `app-ads-context.md` — read audience, target CPA, geo, winning angles
2. Check for `app-marketing-context.md` (aso-skills) — positioning and value props
3. Confirm prerequisites below before generating

## Prerequisites

| Requirement | Notes |
|-------------|-------|
| Appeeky API key | Pro plan for image generation |
| App Store or Google Play URL | Or `platform` + `app_id` |
| Optional audience override | From `app-ads-context.md` |
| Credit awareness | Inform user before any paid generation |

## Meta Static Ad Specs

| Element | Spec | Notes |
|---------|------|-------|
| Image size | **1024×1024** | Square feed; API output default |
| Primary text | Up to 125 chars visible before "See more" | Hook must land in first line |
| Headline | 40 chars recommended | Appears below image |
| Description | 30 chars (optional) | Often hidden on mobile |
| CTA | `INSTALL_MOBILE_APP` | Set in Ads Manager / API |
| Text on image | ≤ 20% of area (guideline) | Heavy text can limit delivery |

## Style × Preset Framework

Match **style** (narrative tone) with **image preset** (visual layout).

### Styles

| Style | Tone | Best for |
|-------|------|----------|
| `ugc` | Casual, phone-in-hand, authentic | Consumer, lifestyle, social apps |
| `professional` | Clean, trust, premium | Finance, B2B, productivity |
| `problem_solution` | Pain → fix narrative | Direct response, utility |
| `before_after` | Transformation contrast | Beauty, fitness, editors |
| `lifestyle` | Aspirational context | Wellness, dating, travel |

### Image Presets

| Preset | Visual | Pair with style |
|--------|--------|-----------------|
| `branded_showcase` | Product-first, app UI hero | `professional`, launch |
| `person_holding_phone` | Hand + device mockup | `ugc`, `lifestyle` |
| `creator_testimonial` | Quote + face or avatar | `ugc`, social proof |
| `problem_solution_split` | Split pain/solution | `problem_solution`, `before_after` |
| `clean_app_store_mockup` | Minimal device frame | `professional`, premium |

### Selection Matrix (defaults)

| Campaign goal | Style | Preset |
|---------------|-------|--------|
| Cold install test | `ugc` | `person_holding_phone` |
| High-intent utility | `problem_solution` | `problem_solution_split` |
| Premium / subscription | `professional` | `clean_app_store_mockup` |
| Social proof push | `lifestyle` | `creator_testimonial` |
| Feature launch | `professional` | `branded_showcase` |

Override from `app-ads-context.md` if winning formats are documented.

## Workflow

### Step 1 — Gather Input

Ask if not provided:

| Input | Default | Notes |
|-------|---------|-------|
| App URL or `platform` + `app_id` | — | Required |
| Country | `us` | Store listing locale |
| Style | `ugc` | See table above |
| Image preset | `person_holding_phone` | See table above |
| Angle (optional) | Auto from listing | e.g. "problem-solution for busy founders" |
| Audience (optional) | From context doc | Overrides listing inference |
| Quality | `medium` | `low` / `medium` / `high` |

### Step 2 — Analyze First (recommended)

Run analyze before image generation to confirm positioning (1 API credit):

**MCP:**
```
generate_app_ad_creative
  app_url: "https://apps.apple.com/us/app/id123456789"
  mode: "analyze"
  generate_image: false
```

**REST:**
```bash
POST /v1/app-ad-creatives/generate
Content-Type: application/json

{
  "appUrl": "https://apps.apple.com/us/app/id123456789",
  "mode": "analyze",
  "generateImage": false
}
```

Present `result.keyPoints` to user. Confirm or edit before generating image.

### Step 3 — Generate Creative

**MCP:**
```
generate_app_ad_creative
  app_url: "https://apps.apple.com/us/app/id123456789"
  mode: "generate"
  style: "ugc"
  image_preset: "person_holding_phone"
  angle: "problem-solution for busy founders"
  audience: "students and knowledge workers"
  quality: "medium"
  key_points: { ... }   # optional — from confirmed analyze step
```

**REST:**
```bash
POST /v1/app-ad-creatives/generate

{
  "appUrl": "https://apps.apple.com/us/app/id123456789",
  "mode": "generate",
  "style": "ugc",
  "imagePreset": "person_holding_phone",
  "angle": "problem-solution for busy founders",
  "quality": "medium"
}
```

Response: HTTP 202 with `jobId`.

### Step 4 — Poll Until Complete

**MCP:**
```
get_app_ad_creative_job
  job_id: "<job-id>"
```

**REST:**
```bash
GET /v1/app-ad-creatives/jobs/:jobId
```

Poll every **3–5 seconds** until `status` is `completed` or `failed`.

| Status | Action |
|--------|--------|
| `queued` / `processing` | Keep polling |
| `completed` | Extract `result` |
| `failed` | Read `error`, retry or adjust inputs |

### Step 5 — Present Output

Use the output template below. Always include image URL, copy fields, and next steps.

## Output Template

```markdown
# Meta Ad Creative — [App Name]

## Key Points (from listing analysis)
- **What it does:** ...
- **Audience:** ...
- **Pain point:** ...
- **Promise:** ...
- **Ad angle:** ...

## Paste into Meta Ads Manager

| Field | Copy | Chars |
|-------|------|-------|
| Primary text | [result.ad.copy.primaryText] | |
| Headline | [result.ad.copy.headline] | |
| Description | [result.ad.copy.description] | |
| CTA | [result.ad.copy.callToAction] | |

## Creative Asset
- **Image URL:** [result.ad.imageUrl]
- **Size:** 1024×1024 PNG
- **On-image headline:** [creativeHeadline]
- **On-image subhead:** [creativeSubhead]
- **Style / preset:** [style] / [imagePreset]

## Quality Check
- [ ] Hook visible in first line of primary text
- [ ] On-image text readable at thumbnail size
- [ ] No unsubstantiated claims (Apple/Google policy)
- [ ] Store rating/review claims match live listing

## Next Steps
1. Manual upload → Meta Ads Manager
2. Automated pipeline → `ad-creative-to-meta`
3. More angles → `ad-creative-variants`
4. Iterate image → `ad-creative-edit`
```

## Copy Quality Framework

### Primary Text Structure

```
Line 1: Hook (pain or curiosity) — must work standalone
Line 2–3: Proof or mechanism
Line 4: Soft CTA + social proof if available
```

| Pattern | Example hook |
|---------|--------------|
| Problem callout | "Still juggling 4 apps to stay organized?" |
| Outcome promise | "Plan your week in 5 minutes." |
| Social proof | "Join 2M+ users who..." |
| Question | "What if your notes actually stuck?" |

### Headline Rules

- Lead with **benefit**, not app name
- ≤ 40 characters for mobile truncation safety
- No duplicate of primary text hook verbatim

### CTA Mapping

| App model | CTA type |
|-----------|----------|
| Free install | Install Now |
| Freemium | Install Now or Learn More |
| Subscription | Install Now (trial in copy) |

## Edit Mode (quick pointer)

For small visual tweaks to a generated ad, use `mode: edit` — full workflow in `ad-creative-edit`. For new angles or presets, re-run `mode: generate`.

```
generate_app_ad_creative
  app_url: "https://apps.apple.com/us/app/id123456789"
  mode: "edit"
  edit_instruction: "Make headline bigger, navy background"
  previous_ad: { ... }
```

## Credit & Cost Table

Tell user **before** generating:

| Mode | API credits | Creative credits |
|------|-------------|------------------|
| `analyze` / copy-only | 1 | 0 |
| `generate` image `low` | 1 | 1 |
| `generate` image `medium` | 1 | 2 |
| `generate` image `high` | 1 | 5 |
| `edit` | 1 | 1–5 by quality |
| BYOK (`X-OpenAI-Key`) | 1 | 0 |

## Benchmarks (Meta static, app install)

| Metric | Weak | OK | Strong |
|--------|------|-----|--------|
| CTR (link) | < 0.8% | 0.8–1.5% | > 1.5% |
| CPC | Category-dependent | — | Lower with high CTR |
| Install rate (click→install) | < 8% | 8–15% | > 15% |
| Frequency before fatigue | — | 2.5–3.5 | Refresh at 3+ |

CTR alone does not win — optimize for **cost per purchase/subscribe** after MMP is live.

## Common Errors

| Error | Cause | Fix |
|-------|-------|-----|
| `PRO_FEATURE` | Plan lacks image generation | Upgrade or use `analyze` only |
| `APP_NOT_FOUND` | Bad URL or wrong country | Verify store URL and `country` |
| `OPENAI_NOT_CONFIGURED` | Server-side AI not set | BYOK header or contact support |
| Job timeout | Heavy queue | Retry; lower `quality` |
| Generic copy | Weak listing | Enrich store description; pass `angle` + `audience` |
| Policy risk | Health/finance claims | Soften claims; add disclaimers in copy |

## Common Mistakes

| Mistake | Why it fails | Fix |
|---------|--------------|-----|
| Skipping analyze step | Misaligned angle wastes credits | Always confirm `keyPoints` (pass as MCP `key_points`) first |
| Same preset for every test | No learning signal | Rotate style × preset matrix |
| App name as headline | Low CTR on cold traffic | Benefit-first headline |
| Ignoring char limits | Truncated hook kills CTR | Front-load value in line 1 |
| One creative per ad set | No auction leverage | Minimum 3–5 via `ad-creative-variants` |
| Generating before MMP | Can't optimize to revenue | Complete `mmp-setup` first |

## Pre-Launch Checklist

```
Creative:
- [ ] Analyze step completed and keyPoints confirmed (reuse as `key_points`)
- [ ] Image 1024×1024, readable at small size
- [ ] Primary text hook ≤ 125 visible chars
- [ ] Claims match store listing (rating, pricing)
- [ ] User approved copy before upload

Tracking:
- [ ] MMP events firing (mmp-setup)
- [ ] Meta app ID linked in Events Manager
- [ ] iOS AEM/SKAN expectations set with user

Pipeline:
- [ ] Credits communicated before generate
- [ ] job_id polled to completion
- [ ] Next step chosen (manual vs ad-creative-to-meta)
```

## Integration Reference

See [appeeky-ad-creatives.md](../../tools/integrations/appeeky-ad-creatives.md) for full API fields.

**Key response fields:**
- `result.keyPoints` — positioning extracted from listing
- `result.ad.imageUrl` — 1024×1024 PNG
- `result.ad.copy` — `primaryText`, `headline`, `description`, `callToAction`
- `result.ad.creativeHeadline` / `creativeSubhead` — on-image text

## Related Skills

- `ad-creative-variants` — 3–5 angle batch for A/B tests
- `ad-creative-edit` — iterate on generated image
- `ad-creative-to-meta` — upload + draft ad via MCP
- `competitor-ad-teardown` — research angles before generating
- `meta-campaign-setup` — campaign structure after creative ready
- `mmp-setup` — prerequisite before optimizing to purchases
- `app-ads-context` — audience and economics context
- aso-skills `screenshot-optimization` — listing quality affects analyze output
