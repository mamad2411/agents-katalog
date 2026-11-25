---
name: competitor-ad-teardown
description: When the user wants to analyze competitor Meta ads, find what creatives competitors run, or research ad angles before creating their own. Use when the user mentions "competitor ads", "Meta Ad Library", "what ads is X running", "Facebook ads spy", "ad intelligence", or "swipe file". For generating your own creatives see meta-ad-creative or ad-creative-variants.
metadata:
  version: 1.0.0
---

# Competitor Ad Teardown (Meta Ad Library)

Analyze competitor paid social creatives via Appeeky Meta Ad Library integration. Produce a **swipe file of patterns and hooks** — not a copy-paste kit.

Research before you generate. The best first batch mirrors proven formats with your unique positioning.

## Initial Assessment

1. Read `app-ads-context.md` — your app, category, geo
2. Identify 1–3 competitors (direct + aspirational)
3. Confirm read-only Ad Library access (Appeeky API key; optional `X-Meta-Ad-Library-Token`)

## What You Can Learn (and Cannot)

| Can learn | Cannot learn |
|-----------|--------------|
| Active creative formats | Exact spend / ROAS |
| Hook patterns and angles | Which ad "wins" internally |
| Long-running ads (proxy for profit) | Full funnel CVR |
| Platform mix (FB, IG, etc.) | Audience targeting details (limited) |
| CTA and copy structure | Proprietary assets to steal |

**Long-running active ads** (30+ days) are the strongest signal — competitors rarely keep losers live.

## Data Sources (Appeeky MCP)

| Tool | Use when |
|------|----------|
| `meta_app_ad_intelligence` | You have competitor App Store / Play ID |
| `meta_ads_search` | Keyword or brand name search |
| `meta_ads_page_ads` | You know Facebook Page ID |

See [appeeky-meta-ads.md](../../tools/integrations/appeeky-meta-ads.md).

## Workflow

### Step 1 — Identify Target

| Input | Example |
|-------|---------|
| Competitor app name | "Calm" |
| Apple App ID | `571800810` |
| Google package | `com.competitor.app` |
| Facebook Page ID | If known from prior search |

Pull organic context from aso-skills `competitor-analysis` if available — aligns ASO vs paid positioning.

### Step 2 — Fetch Ad Intelligence (by app)

Best starting point — resolves app → brand → Ad Library:

```
meta_app_ad_intelligence
  app_id: "571800810"
  platform: "apple"
  country: "us"
  status: "ACTIVE"
  media_type: "ALL"
  limit: 25
```

**Google Play:**
```
meta_app_ad_intelligence
  app_id: "com.competitor.app"
  platform: "google"
  country: "us"
  lang: "en"
  limit: 25
```

**Override search terms** if brand name differs from app title:
```
meta_app_ad_intelligence
  app_id: "571800810"
  platform: "apple"
  query: "Calm meditation sleep"
```

### Step 3 — Search by Keyword or Page

**Keyword search:**
```
meta_ads_search
  query: "Calm meditation"
  countries: "US"
  status: "ACTIVE"
  media_type: "ALL"
  limit: 25
```

**Page-specific:**
```
meta_ads_page_ads
  page_id: "<facebook-page-id>"
  countries: "US"
  status: "ACTIVE"
  limit: 25
```

Paginate with `after` cursor if `limit` exhausted.

### Step 4 — Analyze Each Ad

For top **10–15 ads** (prioritize long-running + diverse formats):

| Dimension | What to extract |
|-----------|-----------------|
| **Hook** | First line of primary text / video opening |
| **Format** | Video / static / carousel / meme |
| **Angle** | Problem, social proof, offer, fear, aspiration |
| **Visual** | UGC, studio, screenshot, before/after |
| **CTA** | Install, Learn more, Sign up |
| **Runtime** | `ad_delivery_start_time` → today |
| **Platforms** | Facebook, Instagram, Messenger, Audience Network |
| **Seasonality** | Holiday, back-to-school, New Year |

### Step 5 — Pattern Summary

Cluster ads into 3–5 patterns. Count frequency.

### Step 6 — Translate to Your Variants

Map gaps to `ad-creative-variants` matrix — angles competitors **don't** use are opportunities.

## Analysis Framework

### Hook Taxonomy

| Type | Signal words | Example |
|------|--------------|---------|
| Problem | "Tired of", "Still", "Can't" | "Still can't focus?" |
| Outcome | "Get", "Finally", "In X days" | "Sleep better in 7 nights" |
| Social proof | "Join", "million", "#1" | "Join 10M+ users" |
| Curiosity | "This", "Why", "Secret" | "This app fixed my mornings" |
| Identity | "For [persona]" | "For busy moms" |
| Offer | "Free", "Trial", "% off" | "7-day free trial" |

### Format Taxonomy

| Format | Scroll-stop mechanism | Your Appeeky preset mapping |
|--------|----------------------|----------------------------|
| UGC phone | Authenticity | `person_holding_phone` + `ugc` |
| Split problem/solution | Contrast | `problem_solution_split` |
| Testimonial quote | Trust | `creator_testimonial` |
| Clean product shot | Premium | `clean_app_store_mockup` |
| Video demo | Motion proof | `tiktok-creative-strategy` (not static API) |

### Longevity Scoring

| Days active | Interpretation |
|-------------|----------------|
| < 7 | Testing — weak signal |
| 7–30 | Promising — watch |
| 30–90 | Likely working |
| 90+ | Core evergreen creative |

## REST API Equivalents

```bash
# App intelligence
GET /v1/apps/:id/ad-intelligence?platform=apple&country=us

# Search
GET /v1/ads/meta/search?query=Calm&countries=US&status=ACTIVE

# Page ads
GET /v1/ads/meta/pages/:pageId/ads?countries=US
```

Headers: `Authorization: Bearer <appeeky-key>`; optional `X-Meta-Ad-Library-Token`.

## Output Template

```markdown
# Competitor Ad Teardown — [Competitor Name]

**App ID:** [id]  |  **Platform:** apple  |  **Ads analyzed:** N active
**Date:** [date]  |  **Geo filter:** US

## Executive Summary
[2–3 sentences: what they lean on, what's missing, your opportunity]

## Top Patterns

### 1. [Pattern Name] — X of N ads
- **Format:** Video / static / carousel
- **Angle:** Problem / proof / offer
- **Typical hook:** "..."
- **Why it works:** [hypothesis]
- **Example library ID:** [id]

### 2. [Pattern Name] — X of N ads
...

## Hook Swipe File

| Hook (paraphrased) | Type | Format | Days live | Platforms |
|--------------------|------|--------|-----------|-----------|
| | Problem | Video | 90+ | IG, FB |
| | Social proof | Static | 45 | FB |

## Visual Patterns
- Dominant: [UGC / studio / screenshot]
- On-image text: [heavy / minimal]
- Brand colors: [notes]

## Platform Mix
| Platform | % of ads |
|----------|----------|
| Instagram | |
| Facebook | |
| Audience Network | |

## Gaps & Opportunities
- **Angles they avoid:** [list]
- **Formats underused:** [e.g. before/after]
- **Weak CTAs to beat:** [generic "Learn more"]
- **Geo gaps:** [EU vs US creative differences]

## Recommended Variants for Us
→ Run `ad-creative-variants` with:

| Variant | Angle (inspired by, not copied) | Style / Preset |
|---------|--------------------------------|----------------|
| A | [your problem hook] | problem_solution / split |
| B | [your UGC angle] | ugc / person_holding_phone |
| C | [gap they miss] | professional / mockup |

## Ethical Use Reminder
- Inspire format and structure — never copy exact copy/visuals
- Do not present competitor ads as your own
```

## Multi-Competitor Comparison

When analyzing 2–3 competitors:

| Pattern | Comp A | Comp B | Comp C | You |
|---------|--------|--------|--------|-----|
| UGC video | ✅ Heavy | ⚠️ Some | ❌ None | ? |
| Before/after | ❌ | ✅ Heavy | ❌ | Opportunity |
| Free trial CTA | ✅ | ✅ | ⚠️ | Match |

## TikTok Competitor Research (manual)

No TikTok Ad Library API in Appeeky yet:

1. TikTok Creative Center → Top Ads by industry
2. Search `#[competitor]` and `"[competitor] ad"` on TikTok
3. Document in same teardown template under **TikTok appendix**
4. Feed hooks into `tiktok-creative-strategy`

## Benchmarks (category signals)

| Signal | Saturated market | Open opportunity |
|--------|------------------|-------------------|
| Same hook in 80%+ ads | Parity required + differentiation | |
| Video dominance | Need video channel (TikTok/Meta video) | Static may still work if others ignore |
| No static ads | | Static 1024 via `meta-ad-creative` |
| Heavy offer ads | Trial/price in your copy | Brand/outcome angle unused |

## Common Mistakes

| Mistake | Fix |
|---------|-----|
| Copying hooks verbatim | Paraphrase; adapt to your listing |
| Analyzing inactive ads only | Filter `status: ACTIVE` |
| One competitor only | Compare 2–3 for pattern confidence |
| Ignoring ad age | Weight long-running ads higher |
| Research without action | Always output variant recommendations |
| Skipping your own listing | Generate only after teardown → variants plan |

## Ethical & Legal Use

- **Inspire, don't infringe** — formats and categories are fair game; assets and exact copy are not
- Paraphrase all hooks in swipe file
- Use competitor ads for internal strategy only
- When showing user examples, label clearly as **competitor ad** with source

## Pre-Teardown Checklist

```
- [ ] Competitor app IDs confirmed
- [ ] Geo filter matches your launch market
- [ ] meta_app_ad_intelligence or search returned results
- [ ] 10+ ads analyzed (or documented if fewer exist)
- [ ] Patterns counted and ranked
- [ ] Variant recommendations mapped to ad-creative-variants
- [ ] Ethical use note included in output
```

## Related Skills

- `ad-creative-variants` — build counter-creatives from teardown
- `meta-ad-creative` — single creative from your listing
- `tiktok-creative-strategy` — video format selection
- `meta-campaign-setup` — deploy after creatives ready
- aso-skills `competitor-analysis` — organic/ASO side
- aso-skills `competitor-tracking` — ongoing monitoring
- `app-ads-context` — your positioning vs findings
