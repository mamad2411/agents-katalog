---
name: meta-campaign
description: "End-to-end Meta (Facebook/Instagram) ad campaign builder. From a single URL, generates upload-ready ad campaigns through 9 stages: competitor & Facebook Ads Library research, landing page analysis, deep interview, customer roleplay, market research (Reddit/forum mining), competitive synthesis, campaign strategy with angle scoring, creative generation (AI images via Gemini + ad copy), and final delivery with testing plan. Starts with deep competitor ad research using the Meta Ad Library to identify winning patterns, hooks, and angles before building the campaign. Use when the user says 'meta campaign', '/meta-campaign', 'create Meta ads', 'Facebook ad campaign', 'Instagram ad campaign', 'build ads from URL', 'ad campaign from landing page', or wants to create a full paid social campaign. Supports multi-language ad copy."
---

# Meta Campaign Builder

Build complete, upload-ready Meta ad campaigns from a single URL through 9 sequential stages.

```
00 Competitor & Ad Library Research
→  01 Brief & LP Analysis  →  02 Deep Interview  →  03 Customer Roleplay
→  04 Market Research  →  05 Competitive Analysis
→  06 Campaign Strategy [APPROVAL]  →  07 Creative Generation [APPROVAL]
→  08 Final Delivery [APPROVAL]
```

**[APPROVAL]** = Pause and present work to user for approval before continuing.

---

## Stage 00: Competitor & Ad Library Research

**This stage runs FIRST, before anything else.** The goal is to understand the competitive landscape and identify winning ad patterns in the niche before analyzing the user's own page.

### Step 1: Identify Competitors

Ask the user (or infer from the URL/niche):
- Direct competitors (same product/service)
- Indirect competitors (same audience, different solution)
- Aspirational brands (larger players in the space to learn from)

If the user doesn't know competitors, use WebSearch:
- `"[product category]" site:facebook.com/ads/library`
- `"[niche keyword]" facebook ads`
- `"[problem the product solves]" online course OR formation OR training`
- `best [product category] 2025 2026`

### Step 2: Facebook Ads Library Research

For each competitor (3-5 minimum), search the Meta Ad Library:

**Using agent-browser (preferred):**
```bash
npx agent-browser open "https://www.facebook.com/ads/library/?active_status=active&ad_type=all&country=ALL&q=[competitor name or keyword]"
npx agent-browser wait --load networkidle
npx agent-browser screenshot competitor_ads_1.png
npx agent-browser scroll down 800
npx agent-browser screenshot competitor_ads_2.png
# Repeat scrolling to capture all active ads
```

**Using WebSearch (fallback):**
- `site:facebook.com/ads/library "[competitor name]"`
- `"[competitor]" facebook ads examples [year]`
- `"[niche keyword]" meta ad library active ads`

### Step 3: Analyze Competitor Ads

For each competitor, extract and document:

**Volume & Activity:**
- Number of active ads (high volume = sophisticated advertiser)
- Ad longevity (long-running ads = proven performers, prioritize these)
- Launch frequency (how often they refresh creatives)

**Creative Patterns:**
- **Hooks** — First line of ad copy. Classify by type: question, statistic, bold claim, story opener, fear/urgency, social proof, curiosity gap
- **Angles** — Pain, aspiration, social proof, urgency, curiosity, comparison, transformation
- **Formats** — Static image, carousel, video, UGC-style, before/after, screenshot
- **Image patterns** — Bold text overlay, founder face, VS comparison, testimonial card, product demo, meme-style, data/chart
- **Video patterns** — Hook in first 3s, talking head, screen recording, B-roll + voiceover, green screen
- **Ad copy length** — Short (1-2 lines), medium (3-5 lines), long (paragraph+)
- **CTAs** — Button type, urgency language, offer framing
- **Offers** — Discounts, free trials, guarantees, bonuses, scarcity

**Winning Signals (prioritize these ads):**
- Ads running for 30+ days = likely profitable
- Ads with multiple variations of same hook = proven angle
- High engagement (visible likes/comments if accessible)

### Step 4: Output — Competitive Ad Intelligence Report

Produce a structured report:

```markdown
## Competitive Ad Intelligence Report

### Market Overview
- Niche maturity: [low/medium/high] advertiser sophistication
- Dominant formats: [list]
- Dominant angles: [list]
- Average creative volume per advertiser: [number]

### Competitor Breakdown
#### [Competitor 1]
- Active ads: [number]
- Longest-running ad: [description + duration]
- Top hooks: [list with classification]
- Top angles: [list]
- Creative formats: [breakdown]
- Key offers: [list]

[Repeat for each competitor]

### Pattern Analysis
- Most common hooks in the niche: [ranked list]
- Most common angles: [ranked list]
- Underused angles (opportunity gaps): [list]
- Creative formats missing from competitors: [list]

### Implications for Our Campaign
- Proven angles to test: [list with evidence]
- Differentiation opportunities: [what competitors DON'T do]
- Hook inspiration: [top 5 hooks adapted for our product]
- Format recommendations: [based on competitor performance signals]
```

This report feeds directly into Stage 05 (Competitive Analysis) and Stage 06 (Campaign Strategy) to ensure our angles and creatives are informed by real market data.

---

## Stage 01: Brief & LP Analysis

Use WebFetch to scrape the user's landing page URL. Extract:

- **Brand**: Name, colors, tone of voice
- **Value proposition**: Headline, core promise
- **Features/Benefits**: All features with benefit framing
- **Social proof**: Testimonials, stats, trust badges
- **CTAs**: All calls-to-action
- **Pricing**: Plans, offers, discounts
- **Audience signals**: Pain points addressed, aspirational framing

Output a structured **Brand Brief**. Note gaps to fill in Stage 02.

## Stage 02: Deep Interview

3-5 rounds of strategic questioning. See [references/interview-framework.md](references/interview-framework.md) for the full question bank.

1. **Business fundamentals** — Goals, budget, timeline, past performance
2. **Customer deep-dive** — Who buys, why, alternatives considered
3. **Differentiators** — Unique advantages, proof points
4. **Constraints** — Compliance, brand guidelines, seasonal factors
5. **Creative direction** — Preferred styles, references, what to avoid

Ask 3-5 focused questions per round. Skip rounds if info is clear. Produce a **Campaign Brief** = Brand Brief + interview insights.

## Stage 03: Customer Roleplay

Use Opus-level depth. Based on the Campaign Brief:

1. Define 2-3 buyer personas (name, demographics, psychographics)
2. For each persona, roleplay the buying journey:
   - Trigger event, current feelings, objections, what makes them click vs scroll
   - Language they use to describe the problem
3. Extract per persona:
   - Top 5 emotional triggers
   - Top 5 objections
   - Key voice-of-customer phrases
   - The "aha moment" that converts

Output a **Persona & Motivation Map**.

## Stage 04: Market Research

Use Opus-level depth. Mine real customer language via WebSearch.

**Search queries:**
- `"[product category] reddit"` + pain point keywords
- `"[competitor] review" "switched from"` / `"better than"`
- `"[problem] forum"` + solution-seeking language
- `site:reddit.com "[relevant subreddit]"` + topic keywords

**Extract and categorize:**
- Pain points (in customer's words)
- Desires (what they wish existed)
- Objections (why they hesitate)
- Language patterns (exact phrases, emotional words)
- Competitor sentiment (love/hate about alternatives)

Use WebFetch on the most relevant threads. Output a **Voice of Customer (VoC) Report** with direct quotes and source links.

## Stage 05: Competitive Analysis

**Build on the Stage 00 Competitive Ad Intelligence Report.** Do NOT redo the Ad Library research — use the data already collected.

At this stage, synthesize the competitive research with insights from Stages 01-04:

1. **Cross-reference competitor angles with our persona pain points** (from Stage 03)
   - Which competitor angles match our personas' top triggers?
   - Which competitor angles are irrelevant to our audience?

2. **Identify positioning gaps** using VoC data (from Stage 04)
   - Pain points customers mention that NO competitor addresses in their ads
   - Language/framing competitors miss that customers actually use

3. **Score competitor creative effectiveness:**
   - Hooks — classify using hook taxonomy (see [references/creative-patterns.md](references/creative-patterns.md))
   - Rank angles by evidence strength (longevity, variations, engagement)
   - Identify the "table stakes" messaging (what everyone says) vs differentiators

4. **Define our competitive advantage in ads:**
   - What can we say that competitors can't? (unique proof, unique angle, unique format)
   - What format/style is underrepresented in the niche?
   - What hook types are overused vs untapped?

Output an updated **Competitive Ad Landscape** that merges Stage 00 data with persona/VoC insights, highlighting the top 3-5 opportunity gaps to exploit in Stage 06.

## Stage 06: Campaign Strategy [APPROVAL]

See [references/campaign-architecture.md](references/campaign-architecture.md) for structure templates.

1. **Score angles** (1-10) based on research evidence:
   - Pain-agitate-solve
   - Aspirational transformation
   - Social proof / authority
   - Comparison / switchover
   - Urgency / scarcity
   - Curiosity / pattern interrupt

2. **Design campaign architecture:**
   - Campaign objective (conversions, traffic, leads)
   - Ad sets by angle or audience
   - 5-10+ ad variations per ad set (use hook taxonomy for diversity — see [references/creative-patterns.md](references/creative-patterns.md))
   - Targeting strategy per ad set
   - Budget allocation recommendation
   - Creative volume target (see [references/campaign-architecture.md](references/campaign-architecture.md) for volume strategy)

3. **Per ad set define:** Primary angle, target persona, hook direction, visual concept

**PAUSE: Present strategy for user approval. Iterate before proceeding.**

## Stage 07: Creative Generation [APPROVAL]

See [references/ad-copy-frameworks.md](references/ad-copy-frameworks.md) for copywriting formulas and hook bank.
See [references/creative-patterns.md](references/creative-patterns.md) for hook taxonomy, image patterns, UGC/video guidance, and volume testing strategy.

### Ad Copy (per ad)
- **Hook**: First 125 characters — use the hook taxonomy (7 types). Test at least 1 ad per hook type.
- **Primary text**: 3 variants — short (1-2 lines), medium (3-5 lines), long (paragraph)
- **Headline**: Under 40 characters
- **Description**: Under 30 characters
- **CTA button**: Learn More, Shop Now, Sign Up, etc.

Write in the target market's language. If audience is bilingual, create variants in both languages.

### Image Generation (per ad)
Generate images using **Gemini 3 Pro** (`gemini-3-pro-image-preview` with `response_modalities=["IMAGE", "TEXT"]`):
- Use proven image patterns from [creative-patterns.md](references/creative-patterns.md): bold text on dark, founder face, VS comparison, before/after, screenshot style
- Match brand colors and style
- Aspect ratios: 1080x1080 (feed), 1080x1920 (stories)
- Image must be readable in 1 second on mobile — max 2-3 lines of bold text
- Generate and present alongside copy

### Video/UGC Recommendations (per winning hook)
If applicable, recommend UGC/talking head scripts for top hooks:
- First 3 seconds = hook (same hook taxonomy)
- Under 60 seconds for feed, 15 seconds for Reels
- Subtitles always on (85% watch without sound)
- Intentionally imperfect production signals authenticity

**PAUSE: Present all creatives for approval. Offer to regenerate or revise specific ads.**

## Stage 08: Final Delivery [APPROVAL]

See [references/delivery-templates.md](references/delivery-templates.md) for output structure.

Organize into markdown files:

```
campaign-name/
├── 00-campaign-brief.md
├── 01-research-report.md
├── 02-campaign-strategy.md
├── 03-ad-sets/
│   ├── ad-set-1-[angle].md
│   ├── ad-set-2-[angle].md
│   └── ...
├── 04-testing-plan.md
└── 05-launch-checklist.md
```

**Testing plan:**
- Phase 1 (Wk 1-2): Test angles — 1 ad per angle, equal budget
- Phase 2 (Wk 3-4): Scale winners, test copy/image variants
- Phase 3 (Wk 5+): Kill losers, scale winners, test new hooks
- KPIs: CTR, CPC, CPM, ROAS with decision thresholds

**PAUSE: Present complete package for final approval.**

## Multi-Language Support

If target market is not English:
- Ask for target language in Stage 02
- Write all ad copy in that language
- Keep strategy docs in user's preferred language
- Adapt cultural references and idioms
