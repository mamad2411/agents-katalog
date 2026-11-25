---
name: ad-creative-variants
description: When the user wants multiple ad creative variants with different angles, styles, or image presets for A/B testing. Use when the user mentions "ad variants", "A/B creatives", "3 ad angles", "test different hooks", "creative batch for Meta", or "5 ad concepts". Uses Appeeky generate_app_ad_creative multiple times. For single creative see meta-ad-creative. For publishing see ad-creative-to-meta.
metadata:
  version: 1.0.0
---

# Ad Creative Variants (A/B Batch)

Generate **3–5 distinct Meta static creatives** from one store listing for structured creative testing. Each variant isolates a different **angle** (message) and/or **visual format** (style + preset).

One creative teaches you nothing. A disciplined batch tells you which hook and layout wins before you scale spend.

## Initial Assessment

1. Read `app-ads-context.md` — target CPA, geo, documented winning/losing formats
2. Check `competitor-ad-teardown` output if available — borrow hook patterns, not copy
3. Confirm monthly budget tier (determines batch size)

## Batch Size by Budget

| Monthly Meta budget | Variants | Min daily budget | Test duration |
|--------------------|----------|------------------|---------------|
| < $1.5K | 3 | $30–50/day | 5–7 days |
| $1.5K–10K | 5 | $50–100/day | 4–5 days |
| $10K+ | 5–8 | $100+/day | 3–4 days |

**Rule:** Each ad needs enough spend to reach decision threshold (~2× target CPA before kill). Smaller budgets → fewer variants.

## Variant Matrix (default 5)

| # | Label | Style | Preset | Angle | Hypothesis |
|---|-------|-------|--------|-------|------------|
| A | Problem | `problem_solution` | `problem_solution_split` | Pain → fix | Direct response converts cold traffic |
| B | UGC | `ugc` | `person_holding_phone` | Relatable user moment | Native feel lifts CTR |
| C | Premium | `professional` | `clean_app_store_mockup` | Trust + quality | Higher CVR on paid subs |
| D | Transform | `before_after` | `problem_solution_split` | Before/after outcome | Visual contrast stops scroll |
| E | Social proof | `lifestyle` | `creator_testimonial` | Quote + outcome | Reduces skepticism |

Customize angles from `app-ads-context.md` value proposition and competitor teardown gaps.

### 3-Variant Minimal Batch

When credits or budget are tight:

| # | Style | Preset | Angle |
|---|-------|--------|-------|
| A | `ugc` | `person_holding_phone` | Core pain point |
| B | `problem_solution` | `problem_solution_split` | Mechanism / how it works |
| C | `professional` | `branded_showcase` | Premium / feature-led |

## Angle Library (fill per app)

| Angle type | Prompt stem | Example |
|------------|-------------|---------|
| Pain agitation | "For [persona] tired of [pain]…" | "For founders tired of inbox chaos…" |
| Outcome | "Get [result] in [timeframe]" | "Plan your week in 5 minutes" |
| Mechanism | "The [category] app that [unique how]" | "The journal that writes back" |
| Social proof | "[N] users / [rating] stars" | Only if true on listing |
| Contrarian | "Stop [common bad habit]" | "Stop using 4 apps for one job" |
| Seasonal | "[Event] is coming — [benefit]" | Tie to `seasonal-aso` campaigns |

## Workflow

### Step 1 — Confirm Inputs

| Input | Required |
|-------|----------|
| App URL or `platform` + `app_id` | Yes |
| Country | Default `us` |
| Batch size (3 / 5) | Default 5 |
| Quality tier | Default `medium` |
| Custom angles | Optional per slot |

### Step 2 — Analyze Once (1 API credit)

```
generate_app_ad_creative
  app_url: "https://apps.apple.com/us/app/id123456789"
  mode: "analyze"
  generate_image: false
```

Present `result.keyPoints`. User approves or edits. **Reuse confirmed `keyPoints` as MCP `key_points` on all variant jobs** for consistent positioning.

### Step 3 — Launch Parallel Jobs

One job per variant. Run in parallel when MCP supports concurrent calls.

```
# Variant A — Problem
generate_app_ad_creative
  app_url: "https://apps.apple.com/us/app/id123456789"
  mode: "generate"
  style: "problem_solution"
  image_preset: "problem_solution_split"
  angle: "For busy professionals drowning in tasks — one app to plan your day"
  key_points: { ...confirmed }
  quality: "medium"

# Variant B — UGC
generate_app_ad_creative
  app_url: "https://apps.apple.com/us/app/id123456789"
  mode: "generate"
  style: "ugc"
  image_preset: "person_holding_phone"
  angle: "POV: you finally found an app that actually sticks"
  key_points: { ...confirmed }
  quality: "medium"

# ... repeat for C, D, E
```

**REST equivalent:** `POST /v1/app-ad-creatives/generate` per variant → collect `jobId`s.

### Step 4 — Poll All Jobs

```
get_app_ad_creative_job
  job_id: "<variant-a-job-id>"
```

Poll every 3–5 seconds per job. Track status in a table while waiting.

| Variant | job_id | Status |
|---------|--------|--------|
| A | | queued / completed / failed |
| B | | |
| C | | |

If one job fails, retry that variant only — do not restart the full batch.

### Step 5 — Present Comparison

Use output template. Highlight differentiated hooks, not just images.

## Meta Test Structure

Run all variants in **one ad set** for fair auction comparison:

```
Campaign: App Promotion (PAUSED)
└── Ad Set: US - iOS - Creative Test
    ├── Ad: Variant A - Problem
    ├── Ad: Variant B - UGC
    ├── Ad: Variant C - Premium
    ├── Ad: Variant D - Transform
    └── Ad: Variant E - Social proof
```

| Setting | Value | Why |
|---------|-------|-----|
| Budget | Ad set level, equal delivery | CBO optional after winner found |
| Optimization | Purchase or Subscribe | Not installs alone at scale |
| Placements | Advantage+ ON | Let Meta find feed vs stories |
| Audience | Broad | Creative is the variable |

**Do not** split variants across ad sets in the first test — you lose comparative signal.

## Decision Rules (during test)

| Condition | Action |
|-----------|--------|
| Spend > 2× target CPA, 0 conversions | Pause that ad |
| CPA < target after 15+ conversions | Mark winner candidate |
| CTR < 0.5% after 5K impressions | Likely hook failure — note for teardown |
| One ad takes > 70% spend | Meta favors it — still wait for CPA data |
| Frequency > 3 on winner | Prepare `ad-creative-edit` variations |

Full audit framework: `meta-campaign-audit`.

## Credit Estimate

Inform user **before** running:

| Batch | Analyze | Generate (medium) | Total creative credits |
|-------|---------|-------------------|------------------------|
| 3 variants | 1 API | 3 × 2 = 6 | 6 creative |
| 5 variants | 1 API | 5 × 2 = 10 | 10 creative |
| 5 variants (high) | 1 API | 5 × 5 = 25 | 25 creative |

BYOK (`X-OpenAI-Key`): 1 API credit per job, 0 creative credits.

## Output Template

```markdown
# Ad Creative A/B Batch — [App Name]

**Batch date:** [date]  |  **Country:** [us]  |  **Quality:** medium

## Positioning (shared keyPoints)
- Pain: ...
- Promise: ...
- Audience: ...

## Variant Comparison

| Label | Angle | Style / Preset | Image | Headline | Primary (excerpt) | Chars |
|-------|-------|----------------|-------|----------|-------------------|-------|
| A | Problem | problem_solution / split | [url] | | | |
| B | UGC | ugc / phone | [url] | | | |
| C | Premium | professional / mockup | [url] | | | |
| D | Transform | before_after / split | [url] | | | |
| E | Social proof | lifestyle / testimonial | [url] | | | |

## Differentiation Check
- [ ] No two variants share the same hook line
- [ ] At least 2 different presets used
- [ ] Primary text lengths within Meta limits

## Meta Test Plan
- **Ad set:** 1 ad set, all variants, $[X]/day
- **Kill rule:** Pause at 2× CPA, 0 conversions
- **Scale rule:** +20%/day on winner when CPA < target
- **Review:** 48h → meta-campaign-audit

## Next Steps
1. Publish → ad-creative-to-meta (all variants)
2. Winner iteration → ad-creative-edit (hook tweaks on winner preset)
3. Loser post-mortem → note angles to retire
```

## Variant Naming Convention

Use consistent ad names in Meta for clean audits:

```
[App] - [Geo] - Var[A-E] - [AngleSlug] - [YYYYMMDD]
```

Example: `FocusApp - US - VarB - UGC - 20250629`

## Benchmarks (batch-level)

| Signal | Weak batch | Healthy batch |
|--------|------------|---------------|
| Best ad CTR | All < 0.8% | Winner > 1.2% |
| CPA spread | All within 10% | Clear winner 20%+ better |
| Spend distribution | One ad 90%+ | Top ad 40–60% |
| Time to decision | > 7 days | 4–5 days at $50/day |

If entire batch fails, diagnose with failure matrix in `meta-campaign-audit` — may be store/onboarding, not creative.

## Common Mistakes

| Mistake | Consequence | Fix |
|---------|-------------|-----|
| Same angle, different colors | False A/B | Change hook and visual format |
| Different ad sets per variant | Uneven delivery | One ad set for test phase |
| Stopping test at 24h | Premature kills | Wait 48h unless 2× CPA rule hits |
| 8+ variants on $30/day | No statistical power | Reduce variants or raise budget |
| Skipping shared keyPoints | Inconsistent positioning | One analyze, shared `key_points` |
| Scaling whole batch | Dilutes budget on losers | Scale winner only |

## Pre-Batch Checklist

```
Planning:
- [ ] app-ads-context.md has target CPA
- [ ] Competitor teardown reviewed (optional)
- [ ] Batch size matches budget tier
- [ ] User approved credit estimate

Generation:
- [ ] Analyze completed, keyPoints confirmed (pass as `key_points`)
- [ ] Each variant has unique angle string
- [ ] All jobs polled to completed
- [ ] Failed variants retried or documented

Meta setup:
- [ ] mmp-setup complete
- [ ] Single ad set test structure
- [ ] Ad names follow convention
- [ ] Campaign starts PAUSED
```

## Related Skills

- `meta-ad-creative` — single creative generation
- `ad-creative-edit` — winner iterations (A′, B′)
- `ad-creative-to-meta` — publish batch to Meta
- `competitor-ad-teardown` — angle research input
- `meta-campaign-setup` — ad set settings
- `meta-campaign-audit` — pick winner after 48h
- `meta-budget-optimizer` — scale winner
- `tiktok-creative-strategy` — parallel video batch for TikTok
