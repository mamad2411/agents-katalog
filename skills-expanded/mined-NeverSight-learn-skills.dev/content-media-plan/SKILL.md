---
name: content-media-plan
description: "Content marketing calendar and media plan generator. Creates a complete content calendar (1, 2, or 4 weeks) with a post-by-post schedule, format examples with AI-generated sample images, and a brand strategy summary. Stores results in Notion and/or exports a local HTML file. Use this skill when the user wants to plan their social media content, create a content calendar, build a posting schedule, develop a content strategy, get a media plan for their brand, or says things like 'create a content plan', 'help me plan my social media', 'I need a posting schedule', 'build me a content calendar', 'what should I post this month', 'content strategy for my brand', 'plan my content for Instagram', 'create a media plan', or 'help me plan content for the next month'."
---

# Content Media Plan Generator

A research-first skill that builds comprehensive content media plans by understanding the brand deeply — through reference accounts, website research, and industry trends — then generating a structured calendar, format examples with AI images, and a visual deliverable ready to share with clients or teams.

This is NOT a generic template filler. It's a brand-driven approach: understand who you're talking to, study what works in the space, then build a plan that's authentic and actionable.

## Workflow Overview

```
Input (doc or guided questions)
  → Research (reference accounts + website + industry trends)
    → Strategy (content pillars + platform mix + frequency)
      → Calendar (1/2/4-week day-by-day grid)
        → Format Examples (copy + AI-generated sample images)
          → Visual HTML Output (calendar + gallery, opens in browser)
            → Storage (Notion and/or local export for Google Drive)
```

---

## Step 0: Document Check

**Always ask this first, before anything else:**

> "Do you have a brief, strategy doc, or brand guide I should start from? Share the file path or paste the content directly — otherwise I'll walk you through it step by step."

**If YES (file path provided):**
- Read the file using the Read tool
- Extract: brand name, industry/niche, target audience, goals, active platforms, brand voice, any reference accounts or competitors mentioned, and existing visual identity
- Present a brief summary: *"Here's what I found in your document: [summary table]. Is there anything to add or correct before I start?"*
- Skip Step 1 entirely. Jump to Step 2.

**If YES (pasted text):**
- Process the pasted content exactly as above
- Skip Step 1. Jump to Step 2.

**If NO:**
- Proceed through Step 1 question rounds.

**Implicit detection:** If the user's opening message already contains a long block of text that reads like a brief or brand strategy, treat it as the document without asking Step 0 — parse it directly and confirm what was extracted.

---

## Step 1: Guided Brand Intake

Only run this step if no document was provided in Step 0. Use a maximum of 3 rounds of questions — batch related questions together, never ask one at a time.

### Round 1 — Core Identity

Ask all of these in a single message:
- Brand / business name
- Industry or niche (e.g., wellness coaching, coffee shop, SaaS tool, fashion brand, real estate)
- Target audience (who follows you or who you want to reach — demographics, interests)
- Primary goal for this content plan (choose one: brand awareness / lead generation / community building / direct sales)

### Round 2 — Operational Realities

Ask all of these in a single message:
- Which platforms will this plan cover? (Instagram, X/Twitter, Facebook, Blog, Newsletter — or any combination)
- Realistic posting capacity: how many posts per week total across all platforms? (1-2 / 3-5 / 5-7 / daily)
- Team size for content production: solo / 2-3 people / full team with designer/videographer
- Brand voice — describe in 2-3 words, or pick from: professional, playful, authoritative, warm, bold, minimal, educational, inspirational

### Round 3 — References and Visual Identity

Ask all of these in a single message:
- Website URL (optional — used to scrape existing copy and tone)
- 1-3 social media accounts you admire or consider competitors (any platform — used as research reference)
- Existing brand colors or visual style? (hex codes, "our brand is dark green and gold", or "no defined palette yet")

After Round 3, confirm before proceeding:
> "Here's what I have: [brief summary of brand, platforms, goals, references]. I'll now research the reference accounts to extract content patterns. Ready?"

---

## Step 2: Research Phase

Only run this step if reference accounts or a website URL were provided (either from the document or Round 3). Run all research in parallel.

### 2A: Reference Account Analysis

Fetch all provided accounts using Social Toolkit MCP:

```
FetchInstagramProfileTool → Instagram handles (bio, followers, posts, captions, engagement, hashtags)
FetchTiktokProfileTool → TikTok handles (bio, videos, engagement patterns)
FacebookBusinessPageInfoTool → Facebook pages (about, posts, likes)
FetchYoutubeChannelTool → YouTube channels (description, subscribers)
FetchYoutubeChannelVideosTool → YouTube channels (recent video titles, views, topics)
```

From each profile, extract:
- Posting frequency and cadence (how often, what days/times)
- Most-used content formats (Reels vs. Feed Posts vs. Carousels vs. Stories)
- Top-performing content themes (recurring topics that get the most engagement)
- Hook patterns for video content (how they open their Reels/Shorts)
- Caption style: long/short, formal/casual, emoji-heavy/none
- Hashtag strategy (branded, niche, broad)
- Visual style: dark/light, colorful/muted, text-heavy/image-led

### 2B: Website Scrape (if URL provided)

```
FirecrawlScrapeTool → homepage URL
FirecrawlScrapeTool → /about page (if exists)
```

Extract: existing taglines and copy patterns, service/product descriptions, tone of voice, color cues from design, and any existing content strategy signals.

### 2C: Industry Trend Research

```
PerplexitySonarSearchTool → "[industry] content marketing strategy [current year]"
GoogleNewsSearchTool → "[industry] social media trends"
GoogleForumsSearchTool → "[industry] content creators what works"
```

**Present research summary before proceeding.** Write a brief analysis (3-5 bullet points) of what was found: what content patterns the reference accounts use, what formats perform best in this industry, and any emerging trends worth noting. Let the user correct or add context before moving to strategy.

---

## Step 3: Strategy Definition

Based on all gathered context, propose an opinionated content strategy. Don't present blank options — propose concrete defaults and let the user override.

### 3A: Content Pillars

Propose 3-5 named content themes grounded in the brand's goals, industry, and audience. Present as a table:

| # | Pillar Name | Description | % of Content | Example Topics |
|---|-------------|-------------|--------------|----------------|
| 1 | [Name] | [1-line description] | [%] | [2-3 specific post ideas] |
| 2 | ... | ... | ... | ... |

**Pillar naming conventions:** Be specific, not generic. Not "Educational Content" but "Behind the Craft" or "The Science of [Topic]". Each pillar should feel like a distinct content series.

### 3B: Platform Mix and Format Matrix

Propose a platform and format breakdown based on the active platforms, capacity, and research:

| Platform | Format | Weekly Frequency | Pillars Served |
|----------|--------|-----------------|----------------|
| Instagram | Feed Post | 3x/week | Pillar 1, 3 |
| Instagram | Carousel | 1x/week | Pillar 2 |
| Instagram | Reels | 2x/week | Pillar 4 |
| Instagram | Stories | Daily | All |
| X/Twitter | Tweet | 4x/week | Pillar 2, 5 |
| Facebook | Post | 3x/week | Pillar 1, 3 |
| Blog | Article | 1x/month | Pillar 2 |
| Newsletter | Email | 2x/month | Pillar 2, 3 |

**Capacity guardrails:**
- Solo + 1-2x/week → max 2 platforms, no Reels/video in the mix unless they already produce video
- Small team + 3-5x/week → 2-3 platforms, simple formats + 1-2 Reels per week
- Full team + 5-7x/week → all platforms enabled, full format variety

### 3C: Posting Time Recommendations

Brief per-platform timing table based on industry best practices and research:

| Platform | Best Days | Best Times | Rationale |
|----------|-----------|------------|-----------|
| Instagram | Tue, Thu, Sat | 7-9pm local | ... |
| X/Twitter | Mon-Fri | 8am, 12pm | ... |
| ... | ... | ... | ... |

**Present the full strategy and ask for confirmation before building the calendar.** Be specific: "Here's the strategy I'm proposing for [Brand Name]. Confirm or let me know what to change."

---

## Step 4: Calendar Duration + Generation

### 4A: Ask calendar duration

Before building, ask:
> "How many weeks should this calendar cover? 1 week / 2 weeks / 4 weeks (default: 4 weeks)"

Adjust the calendar depth based on selection:
- **1 week:** Go deep — include full copy hooks and specific post topics for every single slot
- **2 weeks:** Include specific topics and hooks for Week 1, general themes for Week 2
- **4 weeks:** Specific topics for Week 1, planned themes with example hooks for Weeks 2-4

### 4B: Build the Calendar

Generate the calendar day-by-day. Show as a markdown table first for review.

**Table format:**

| Week | Day | Platform | Format | Pillar | Topic / Hook |
|------|-----|----------|--------|--------|--------------|
| 1 | Mon | Instagram | Feed Post | Pillar 2 | "How we [do X] — the part no one talks about" |
| 1 | Mon | X/Twitter | Tweet | Pillar 5 | "The [industry] myth that needs to die: [hook]" |
| 1 | Tue | Instagram | Stories | All | Behind-the-scenes: [day-in-the-life angle] |
| ... | ... | ... | ... | ... | ... |

**Calendar generation rules:**
- No more than 2 consecutive posts from the same pillar
- Vary formats across days — don't stack all Reels in one week
- Leave days empty if capacity is low (under-commit beats burnout)
- Seasonal/cultural moments: note holidays or events relevant to the brand/audience
- For 4-week plans: build momentum — Week 1 is introductory/awareness, Week 2-3 deepens, Week 4 drives conversion or community action

**After showing the markdown table, ask:**
> "Here's the [N]-week calendar. Want to swap any days, adjust topics, or change the pillar balance before I generate the visual and format examples?"

---

## Step 5: Format Examples + Sample Images

For each unique format type included in the calendar, produce a complete example. Only cover formats actually used in the plan — don't generate unused examples.

### Formats to Cover

**Instagram Feed Post**
- Full caption (100-150 words) with hook, body, and CTA
- 3-5 hashtags + 1 branded hashtag
- Copywriting notes: what makes this hook work
- Sample image: 1:1 (square) aspect ratio

**Instagram Carousel**
- Slide-by-slide outline (3-5 slides): Slide 1 = hook, Slides 2-4 = content, Slide 5 = CTA/save prompt
- Caption for the post
- Sample image: Slide 1 cover, 1:1 aspect ratio

**Instagram Reels**
- Hook script (first 3 seconds — text + action)
- Full caption with CTA and hashtags
- Sample image: vertical thumbnail/cover frame, 9:16 aspect ratio

**Instagram Stories**
- Interactive element type (poll / question sticker / countdown / quiz)
- Story copy (very short — 1-2 lines max)
- Background visual concept
- Sample image: 9:16 vertical background

**X / Twitter**
- 3-tweet thread example (Hook tweet → Content tweet → CTA tweet)
- No image needed for standard tweets; include if it's a visual tweet

**Facebook Post**
- Full post copy (150-250 words — Facebook allows longer copy)
- Link preview description
- Sample image: 16:9 landscape aspect ratio

**Blog Post**
- Title (SEO-optimized)
- Meta description (155 chars)
- Article outline (H2 sections + 1-line description each)
- Intro paragraph (fully written, ~100 words)
- Sample image: 16:9 featured/OG image

**Newsletter**
- Subject line (A/B variant: curiosity-driven + value-driven)
- Preview text (50 chars)
- Full intro section (~150 words)
- Sample image: 16:9 header banner

### Image Generation

Check for `infsh` CLI availability first:

```bash
which infsh
```

**If available**, generate images using FLUX model:

```bash
infsh app run falai/flux-dev-lora --input '{
  "prompt": "[brand-aesthetic-matched prompt]"
}'
```

**If not available**, use Social Toolkit MCP `HiggsfieldImageTool`.

**If both fail**, create a visible placeholder in the HTML output: a dashed-border box at the correct aspect ratio showing the full image prompt text, with the instruction "Replace with generated image."

**Prompt construction pattern:**

```
"[brand visual style and aesthetic] content marketing visual,
[specific format context — e.g., 'Instagram feed post'],
[pillar topic context — e.g., 'behind the scenes coffee roasting process'],
[color palette — e.g., 'warm earth tones, terracotta and cream'],
professional [photography type] style,
[aspect ratio orientation] composition,
no text overlay, no logos, clean and brand-authentic"
```

Example (artisan coffee brand, "Behind the Craft" pillar, Feed Post):
```
"Warm artisan coffee brand aesthetic, Instagram feed post, behind the scenes
coffee roasting process, terracotta and cream color palette with warm amber
light, professional lifestyle photography style, square composition, moody
natural lighting, burlap and wood textures, no text overlay, no logos,
clean and brand-authentic"
```

**Download all generated images** to a local `images/` directory alongside the HTML file:
- `images/example-feed-post.jpg`
- `images/example-carousel-cover.jpg`
- `images/example-reels-cover.jpg`
- `images/example-stories-bg.jpg`
- `images/example-facebook-post.jpg`
- `images/example-blog-featured.jpg`
- `images/example-newsletter-banner.jpg`

Generate images in parallel where the tool allows it. Tell the user: *"Generating format example images — this may take a moment..."*

---

## Step 6: Visual HTML Output

Generate a self-contained `content-media-plan.html` file. All CSS must be inline in `<style>` tags. Images are referenced as relative paths (`images/example-*.jpg`). Google Fonts loaded via `<link>` tag. No other external dependencies.

### Page Sections

**1. Header**
- Brand name (large display type)
- Plan period (e.g., "April 2025 — 4-Week Content Calendar")
- Strategy tagline (one line summarizing the plan's focus)
- Brand color band

**2. Strategy Summary Panel**
- Content pillars as color-coded chips/badges
- Platform icons row
- Goals statement
- Brand voice descriptor

**3. Platform Mix Overview**
- One row per platform: platform icon + name + active formats as tags + weekly frequency badge

**4. Content Calendar Grid**

CSS Grid layout: 8 columns (week label + Mon–Sun) × N rows (one per week).

```css
.calendar-grid {
  display: grid;
  grid-template-columns: 80px repeat(7, 1fr);
  gap: 1px;
  background-color: var(--border);
}

.week-label {
  background: var(--surface-alt);
  padding: 12px 8px;
  font-weight: bold;
  writing-mode: vertical-rl;
  text-align: center;
}

.day-cell {
  background: white;
  min-height: 130px;
  padding: 8px;
  display: flex;
  flex-direction: column;
  gap: 4px;
}

.day-number {
  font-size: 11px;
  color: var(--text-muted);
  font-weight: 600;
  margin-bottom: 4px;
}

.post-card {
  border-left: 3px solid var(--platform-color);
  background: var(--pillar-bg);
  border-radius: 4px;
  padding: 4px 6px;
  font-size: 11px;
  line-height: 1.3;
}

.platform-dot {
  display: inline-block;
  width: 6px;
  height: 6px;
  border-radius: 50%;
  background: var(--platform-color);
  margin-right: 4px;
}
```

**Platform color coding:**
- Instagram: `#E1306C` (pink-magenta)
- X/Twitter: `#000000`
- Facebook: `#1877F2`
- Blog: `#16a34a` (green)
- Newsletter: `#d97706` (amber)

Each pillar gets a soft background tint color for the post-cards (derived from the brand's palette or a default 5-color system).

**5. Format Examples Gallery**

2-column card grid. Each card:
```
┌─────────────────────────────────────┐
│ [Platform badge]  [Format type]     │
│ ┌────────────┐ Caption/copy text    │
│ │  Sample    │ shown here...        │
│ │  Image     │                      │
│ └────────────┘ Copy notes (subtle)  │
└─────────────────────────────────────┘
```

**6. Posting Schedule Table**

Simple table: Platform | Best Days | Best Times | Notes

**7. Footer**

Plan generated date, brand name, note about the skill.

### Typography

Select 2 Google Fonts based on the brand's aesthetic direction. Never use Inter, Roboto, Arial, or system-ui as the primary display font. Derive from brand voice:
- Playful/warm → Rounded display + readable body (e.g., Nunito + Lora)
- Bold/editorial → Heavy condensed + clean body (e.g., Barlow Condensed + Inter)
- Luxury/premium → Serif display + light body (e.g., Playfair Display + Raleway)
- Minimal/professional → Geometric display + text (e.g., Outfit + Source Serif 4)
- Creative/artisan → Expressive + humanist (e.g., Fraunces + DM Sans)

### CSS Variables Setup

```css
:root {
  /* Brand colors — replace with actual brand values */
  --brand-primary: #[hex];
  --brand-secondary: #[hex];
  --brand-accent: #[hex];

  /* Platform colors (fixed) */
  --platform-instagram: #E1306C;
  --platform-twitter: #000000;
  --platform-facebook: #1877F2;
  --platform-blog: #16a34a;
  --platform-newsletter: #d97706;

  /* Pillar colors (up to 5) */
  --pillar-1-bg: #[soft tint];
  --pillar-2-bg: #[soft tint];
  --pillar-3-bg: #[soft tint];
  --pillar-4-bg: #[soft tint];
  --pillar-5-bg: #[soft tint];

  /* UI */
  --surface: #ffffff;
  --surface-alt: #f8f7f5;
  --border: #e5e5e5;
  --text: #1a1a1a;
  --text-muted: #6b7280;

  /* Typography */
  --font-display: '[Display Font]', serif;
  --font-body: '[Body Font]', sans-serif;
}
```

### Opening in Browser

After generating the HTML file and saving all images, use Claude Preview MCP to open it:

```
preview_start → serve the content-media-plan directory
preview_screenshot → capture a screenshot to confirm it rendered correctly
```

Tell the user the full local file path. If Preview MCP is not available, instruct them to open the file manually: `open content-media-plan.html`

### Deployment

Include a `wrangler.jsonc` in the project directory so the presentation can be deployed instantly:

```jsonc
{
  "name": "<brand-name>-content-plan",
  "compatibility_date": "2025-04-01",
  "assets": {
    "directory": "./"
  }
}
```

Deploy with:
```bash
cd content-media-plan && wrangler deploy
```

This deploys the HTML + images as a static site to Cloudflare, giving the user a shareable URL for client presentations or team reviews.

---

## Step 7: Storage

Ask the user where to save the plan. They can pick one or both options. Do NOT assume — always ask before saving anywhere.

> "Where should I save this plan?"
> - **Notion** — create a structured Notion page (requires Notion MCP connected)
> - **Google Drive** — I'll organize the files for easy upload
> - **Local only** — the HTML file is already saved, no additional storage needed

### Notion Storage (if selected)

First check for existing plans:
```
notion-search → "[brand name] content plan" (query_type: "internal", page_size: 5)
```

If a matching page is found, ask: *"I found an existing content plan for [Brand] in Notion. Should I update it or create a new page?"*

Create the page with `notion-create-pages`:

**Page title:** `Content Media Plan: [Brand Name] — [Month YYYY]`
**Page icon:** 📅

**Page structure:**

```
# Strategy Overview
[Brand summary, goals, audience, voice]

## Content Pillars
[Table: # | Pillar | Description | % Content | Example Topics]

## Platform Mix
[Table: Platform | Active Formats | Weekly Frequency]

## Posting Schedule
[Table: Platform | Best Days | Best Times]

---

# Content Calendar

## Week 1 — [Date Range]
[Table: Day | Platform | Format | Pillar | Topic / Hook]

## Week 2 — [Date Range]
[Table: Day | Platform | Format | Pillar | Topic / Hook]

[Repeat for all weeks]

---

# Format Examples

## Instagram Feed Post
[Full example caption]
[Copywriting notes as callout block]
[Image generation prompt as code block]

## Instagram Carousel
[Slide outline]
[Caption]
[Image generation prompt as code block]

[One section per format used]

---

# Implementation Notes

## Hashtag Strategy
[Branded hashtags | Niche hashtags | Broad hashtags — organized by pillar]

## Brand Voice Guide
[Extracted or defined voice attributes, do's and don'ts]

## Generated Assets
[Table: File Name | Format | Pillar | Notes]
```

Use separate `table` blocks for each week (not one giant table) — this keeps Notion readable and the API calls manageable.

Include image generation prompts as `code` blocks so they're easy to copy for manual generation.

### Google Drive Export (if selected)

No Google Drive MCP is available for direct upload. Instead, organize the files and provide clear instructions:

**File organization:**
```
content-media-plan/
├── content-media-plan.html       ← open in browser to view
├── wrangler.jsonc                ← deploy with: wrangler deploy
├── images/
│   ├── example-feed-post.jpg
│   ├── example-carousel-cover.jpg
│   ├── example-reels-cover.jpg
│   ├── example-stories-bg.jpg
│   ├── example-facebook-post.jpg
│   ├── example-blog-featured.jpg
│   └── example-newsletter-banner.jpg
└── content-media-plan-summary.md ← text-only summary for quick reference
```

**Generate a `content-media-plan-summary.md`** — a compact text-only version of the plan (strategy + calendar table + format copy, no images) for easy sharing in any context.

**Upload instructions to show the user:**
1. Open Google Drive → New → Folder Upload → select the `content-media-plan/` folder
2. Once uploaded, right-click the folder → Share → "Anyone with the link" → Viewer
3. To share just the HTML visual: right-click `content-media-plan.html` → Open with Google Docs (Drive renders HTML) → Share that link

<!-- TODO: Future feature — integrate Google Drive MCP when available to upload files directly from this skill -->

---

## Step 8: Present Deliverables

Wrap up with a clean summary:

**What was created:**
- [N]-week content calendar with [X] total posts across [platforms]
- [N] format examples with AI-generated sample images
- Visual HTML output: `[local file path]` (open in browser)
- [Notion page URL — if saved to Notion]
- [Google Drive instructions — if Drive was selected]

**Suggested next steps:**
- Import the calendar to Notion Calendar view (if using Notion) by linking dates in the database
- Use the format examples as creative briefs for your designer or video editor
- Schedule posts using Buffer, Later, or Hootsuite — the calendar table can be exported as CSV for bulk import
- Come back next month: `/content-media-plan` to generate the next cycle, building on this one's learnings

<!-- TODO: Future features to implement in later versions of this skill:

  1. EMAIL DELIVERY
     Send the completed media plan via email (Gmail MCP: gmail_create_draft) as a formatted
     message with the HTML output and generated images attached as a PDF.
     Trigger: user says "send this to my client" or "email me the plan".
     Flow: generate PDF from the HTML output → attach to Gmail draft → user reviews and sends.

  2. CALENDAR EXPORT
     Save all scheduled posts directly to Google Calendar (gcal MCP: gcal_create_event) or
     generate a standard .ics file the user can import into any calendar app (Google Calendar,
     Apple Calendar, Outlook, etc.).
     Each post becomes a calendar event with:
       - Title: "[Platform] [Format]: [Topic]"
       - Description: example copy/caption + image generation prompt
       - Start time: derived from posting time recommendations (Step 3C)
       - Reminder: 1 day before (for content preparation)
     Trigger: user says "add to my calendar" or "export calendar file".
     Flow: ask which calendar option (gcal MCP vs .ics file) → create all events in one batch
     call → confirm with summary of events created.
-->

---

## Behavior Notes

- **Research first, plan second.** The quality of the calendar depends on understanding the brand and the competitive landscape. Don't rush to generate the calendar before the strategy is solid.
- **Be opinionated.** Propose specific pillar names, specific topics, specific hooks. Not "you could post about your product" but "Reveal the Process: a 3-Reel series showing how [product] is made, hook: 'This takes 6 hours and most people never see it'".
- **Write in the brand's voice.** Every example caption should sound like it came from someone who deeply understands the brand — not like a generic template.
- **Ground research in real data.** If a reference account posts Reels 4x/week and gets high engagement, reflect that in the strategy. Don't propose what's theoretically ideal — propose what works in this specific context.
- **Respect capacity constraints.** A solo creator with 2 posts/week needs a very different plan than a team of 5. Never over-engineer the plan beyond what's realistic to execute.
- **Use real examples, not placeholders.** Every format example should be fully written — not "[Insert hook here]" but an actual hook. Users should be able to copy-paste these directly.
- **Show research before strategy, strategy before calendar.** Each phase builds on the previous. Let the user validate each step before moving forward. Momentum is built through small confirmations, not one massive reveal at the end.
