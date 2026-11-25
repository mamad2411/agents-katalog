---
name: data-infographic-generator
description: Generate data-rich comparison infographics (9:16 mobile or 16:9 landscape) with verified research data. Used for AI model comparisons, product specs, pricing tables, and any structured data presentation.
tags: [infographics, data-visualization, nano-banana, gemini, education, community]
---

# Data Infographic Generator

Generates polished, card-based infographics from verified research data. Always uses Gemini 3.1 Flash Image Preview (nano-banana). Used for AI model comparisons, product specs, pricing breakdowns — anything that presents comparative data visually.

## What This Skill Does

This skill Generate data-rich comparison infographics (9:16 mobile or 16:9 landscape) with verified research data. Used for AI model comparisons, product specs, pricing tables, and any structured data presentation.

## When to Use

- User asks for an infographic comparing models, tools, products, or services
- User wants to share data with their community (Skool, social media)
- User wants to recreate an existing infographic with updated data
- Any structured comparison data that needs to look professional and be mobile-readable

## Workflow

### Step 1: Research First (MANDATORY)

**NEVER use stale data or assumptions.** Research every data point from authoritative live sources:

- **Pricing data:** OpenRouter.ai models page, official provider pricing pages
- **Model specs:** Context windows, parameters, capabilities — from official documentation
- **Performance metrics:** Benchmark scores from official sources or leaderboards
- **Current market data:** Always research the actual source, do not guess

```bash
# Use browser tools to research live pricing/data
browser_navigate("https://openrouter.ai/models?q=query")
# Or web_search/web_extract if browser credits are available
```

**If web search credits are exhausted**, use browser tools to navigate directly to source pages.

### Step 2: Compile Verified Data

Before generating, compile a data table with verified values:

```
Model Name | Cost | Context | Performance | Key Notes | Accent Color
```

Verify each data point against what you found in research. Do not include any data you haven't personally verified from a live source.

### Step 3: Generate With Nano Banana

Use the exact workflow below. Always generate with `gemini-3.1-flash-image-preview`.

#### 9:16 Mobile Format (Instagram/TikTok/Stories)

```python
prompt = """
Generate a vertical infographic at 9:16 aspect ratio (1080x1920 pixels) for mobile viewing. Card-based layout, NOT a table. Modern dark SaaS aesthetic.

TITLE: "[exact title]"
Subtitle: "[exact subtitle]"

[For each card:]
CARD N - MODEL NAME (Provider):
- [color] accent stripe on left
- Model: "[exact name]"
- Cost: [verified data] - marked [HIGH/MEDIUM/LOW/VERY LOW] in [color]
- Context: [verified number] tokens
- Performance: [X] out of 5 yellow stars ([descriptor])
- Notes: [exact text]

Design:
- Dark charcoal background, rounded corner cards with colored accent stripes
- Visual cost bars on right side
- Yellow star ratings shown visually
- The recommended card should be visually dominant with glowing green border and "BEST VALUE" badge
- Footer: "[source citation]"

Technical:
- ALL TEXT EXACTLY AS SPECIFIED, NO BACKWARDS TEXT
"""
```

#### 16:9 Landscape Format (Desktop/YouTube/Presentations)

```python
prompt = """
Generate a horizontal infographic at 16:9 aspect ratio (1280x720 pixels). 
Cards arranged in a 2x2 grid. Each card has colored accent stripe on top.
[Same card content structure as above, adapted for horizontal layout]
"""
```

### Step 4: Verify Text (MANDATORY)

After generation, ALWAYS verify with vision_analyze:

1. Ask: "List every word of text. Is everything spelled correctly? Any backwards text? Are all data points accurate?"
2. If text is backwards or incorrect, regenerate with a fresh prompt
3. If a specific data point is wrong, note which card needs fixing
4. Only deliver to user AFTER text verification passes

### Step 5: Deliver

Send the verified infographic to the user. Include a brief summary of what's on it and confirm the source/date of the data.

## Key Design Patterns

### "Highlight the Winner" Pattern

When one option is clearly recommended (lowest cost, best value):
- **Glowing green border** around the entire card
- **Slightly larger** than other cards
- **"BEST VALUE" badge** with fire emoji 🔥
- **Green "VERY LOW" or "LOW" cost** text
- **5/5 stars** to reinforce the recommendation
- Other cards use muted ratings (3-4 stars) to create contrast

### Cost Hierarchy Colors

- **HIGH** → Red text
- **MEDIUM** → Orange text
- **LOW** → Green text
- **VERY LOW** → Bright green text

This creates instant visual hierarchy for cost comparison.

### Card Style Consistency

- Dark fill cards with rounded corners
- Color-matched accent stripe on left (9:16) or top (16:9)
- Brand-appropriate mini icon for each card
- Consistent spacing between cards
- Star ratings shown as filled yellow stars (not text "★★★★")
- Brief notes section on each card (1-2 sentences max)

## Pitfalls

- **Stale data costs credibility.** Always research live data before generating. If the user wants updated numbers, re-research — do not reuse old specs.
- **Web search credits deplete fast.** Switch to browser_navigate when firecrawl credits are exhausted.
- **Text is almost always clean for infographics** (unlike thumbnails). Still verify, but infographics use less stylized text and Gemini handles them well.
- **9:16 vs 16:9 matters.** 9:16 = vertical cards stacked top-to-bottom with side stripes. 16:9 = 2x2 grid with top stripes on each card.
- **Never use PIL compositing for infographics** — Gemini renders clean text and icons directly. No background + text compositing needed.
- **Source citation in footer** is important for credibility. Include "Source: [source]. [Date]."

## Output Paths

- All infographics: `/root/thumbnails/`
- Naming: `topic_format.png` (e.g., `models_9x16.png`, `pricing_16x9.png`)
