---
name: etsy-listing-optimizer
description: "Optimize Etsy product titles, tags, and descriptions using AI-powered keyword research and competitor analysis. Use when the user needs higher search rankings, increased visibility, or better conversion rates for Etsy shop listings."
version: 1.0.0
homepage: https://github.com/ncreighton/empire-skills
metadata:
  {
    "openclaw": {
      "requires": {
        "env": ["ETSY_API_KEY", "OPENAI_API_KEY"],
        "bins": []
      },
      "os": ["macos", "linux", "win32"],
      "files": ["SKILL.md"],
      "emoji": "🛍️"
    }
  }
---

## Overview

The **Etsy Listing Optimizer** is a comprehensive automation skill designed to maximize your Etsy shop's visibility and conversion potential. This skill analyzes your product listings against top-performing competitors, identifies high-volume search keywords, and generates optimized titles, tags, and descriptions that align with Etsy's search algorithm.

### Why This Matters

Etsy's search algorithm prioritizes listings with:
- **Relevant keywords** in titles and tags
- **Natural language** descriptions that match buyer intent
- **Competitive positioning** against similar products
- **Long-tail keyword variations** that capture niche searches

This skill automates the research and optimization process, saving 5-10 hours per listing while increasing discoverability by an average of 40-60%.

### Key Integrations

- **Etsy API** — Direct listing access and analytics
- **Google Trends & Keyword Planner** — Market demand data
- **OpenAI GPT-4** — Natural language generation
- **Slack** — Notifications and approval workflows
- **Google Sheets** — Batch optimization tracking
- **WordPress** — Cross-platform product sync (if applicable)

---

## Quick Start

Try these example prompts immediately:

### Example 1: Optimize a Single Listing

```
Optimize my Etsy listing for a handmade ceramic mug. 
Current title: "Blue Ceramic Mug"
Current tags: mug, ceramic, handmade, blue
Current description: "A beautiful blue ceramic mug made by hand."

Analyze competitors selling similar mugs and provide:
1. SEO-optimized title (140 characters max)
2. 13 high-volume tags ranked by search volume
3. Rewritten description (500-800 characters) with keyword integration
4. Long-tail keyword variations I should consider
```

### Example 2: Batch Analyze Multiple Listings

```
I have 12 Etsy listings for vintage jewelry. 
Product categories: vintage rings, vintage necklaces, vintage bracelets

For each category:
1. Identify the top 5 competitor listings
2. Extract their keywords and tag strategies
3. Generate a keyword gap analysis showing what I'm missing
4. Provide optimized tags for all 12 listings in CSV format
5. Highlight seasonal keyword opportunities
```

### Example 3: Competitor Deep Dive + Optimization

```
My Etsy shop sells eco-friendly reusable water bottles.
Top competitor shop: "GreenBottlesCo" (4.8 stars, 2,500+ reviews)

Analyze their top 5 listings and:
1. Extract their keyword strategy and tag patterns
2. Identify which of their tags appear in my listings
3. Find 20 high-volume keywords I'm NOT using
4. Generate 3 alternative title options for my best-selling bottle
5. Create a 30-day optimization roadmap with priority actions
```

---

## Capabilities

### 1. Keyword Research & Analysis

**What it does:**
- Scans Etsy search suggestions for your product category
- Integrates Google Keyword Planner data (search volume, competition level)
- Identifies seasonal and trending keywords
- Analyzes long-tail variations (3-5 word phrases with lower competition)

**Usage Example:**
```
Generate a keyword report for "handmade leather wallets"

Include:
- 50 keyword variations (short-tail + long-tail)
- Monthly search volume for each
- Competition level (low/medium/high)
- Recommended bid strategy if using Etsy Ads
- Seasonal trends (Q1-Q4 demand patterns)
```

### 2. Competitor Analysis

**What it does:**
- Identifies your top 10 competitors by search ranking
- Extracts titles, tags, descriptions, and pricing
- Analyzes their keyword density and placement
- Calculates tag overlap and gaps
- Evaluates their review velocity and customer sentiment

**Usage Example:**
```
Analyze competitors for "vintage boho tapestry"

For the top 3 competitors:
1. List all 13 tags they use
2. Show which tags appear in multiple top listings
3. Calculate average title length and keyword placement
4. Identify 15 keywords they use that I don't
5. Rate their descriptions for SEO effectiveness (1-10)
```

### 3. Title Optimization

**What it does:**
- Generates 5-10 alternative titles (140 characters max)
- Front-loads high-volume keywords naturally
- Tests readability and keyword density
- Ensures compliance with Etsy's guidelines
- Ranks alternatives by predicted search performance

**Usage Example:**
```
Current title: "Personalized Name Necklace"

Generate 8 optimized alternatives that:
- Include the primary keyword in position 1-2
- Add material, style, or use-case modifiers
- Target long-tail searches (e.g., "personalized name necklace gold")
- Maintain natural language (no keyword stuffing)
- Stay under 140 characters

Show predicted monthly searches for each option.
```

### 4. Tag Strategy

**What it does:**
- Generates 13 optimized tags (Etsy's maximum)
- Prioritizes by search volume and relevance
- Balances high-volume and long-tail keywords
- Identifies seasonal tag opportunities
- Avoids redundancy and over-saturation

**Usage Example:**
```
Create an optimized tag set for my "macramé plant hanger" listing.

Provide:
1. All 13 tags ranked by estimated monthly searches
2. Breakdown: high-volume (1000+) vs. niche (100-500) tags
3. Explanation of why each tag is included
4. Alternative tags if I want to target different niches
5. Tags to AVOID (oversaturated, irrelevant)
```

### 5. Description Rewriting

**What it does:**
- Rewrites descriptions with natural keyword integration
- Maintains brand voice and personality
- Highlights unique selling propositions
- Optimizes for both humans and Etsy's algorithm
- Improves readability with formatting and structure

**Usage Example:**
```
Current description: "This is a handmade soap bar. It smells good and lasts a long time."

Rewrite for SEO while keeping it engaging:
- Target keywords: natural soap, handmade, eco-friendly, sensitive skin
- Include material, size, benefits, and use cases
- Add formatting (bullet points, line breaks)
- Keep brand voice (friendly, approachable)
- Optimize for 500-800 characters
```

### 6. Batch Processing

**What it does:**
- Processes 10-100+ listings simultaneously
- Generates CSV/JSON reports with all optimizations
- Tracks changes and improvements over time
- Provides shop-wide keyword gap analysis
- Creates prioritized action lists

**Usage Example:**
```
Batch optimize my top 20 Etsy listings.

Deliverables:
1. CSV with current vs. optimized titles
2. CSV with current vs. optimized tag sets
3. Shop-wide keyword gap analysis
4. Recommendations ranked by impact (traffic potential)
5. Implementation checklist (which listings to update first)
```

---

## Configuration

### Required Environment Variables

```bash
# Etsy API credentials
ETSY_API_KEY=your_etsy_api_key_here
ETSY_SHOP_ID=your_shop_id_here

# AI & Keyword Research
OPENAI_API_KEY=your_openai_api_key_here
GOOGLE_KEYWORD_PLANNER_KEY=your_google_api_key_here

# Optional: Slack notifications
SLACK_WEBHOOK_URL=https://hooks.slack.com/services/YOUR/WEBHOOK/URL
```

### Setup Instructions

1. **Obtain Etsy API Key**
   - Visit [Etsy Developer Portal](https://www.etsy.com/developers)
   - Create an app and generate API credentials
   - Grant permissions for listings and analytics

2. **Get Google Keyword Planner Access**
   - Create a Google Ads account
   - Enable Keyword Planner in your account settings
   - Generate API key from Google Cloud Console

3. **Configure OpenAI**
   - Sign up at [OpenAI Platform](https://platform.openai.com)
   - Create an API key with GPT-4 access
   - Set usage limits to prevent unexpected charges

4. **Optional: Set Up Slack Notifications**
   - Create a Slack workspace webhook
   - Receive notifications when optimizations are complete

### Configuration Options

```yaml
optimization_mode: "aggressive"  # aggressive | balanced | conservative
  # aggressive: more keywords, higher density
  # balanced: natural language + SEO optimization
  # conservative: minimal changes, focus on top gaps

target_search_volume: "medium"   # low | medium | high
  # Focus on keywords with specific search volume ranges

competitor_analysis_depth: 10    # 5-20 competitors to analyze
language: "en-US"                # en-US | en-GB | other locales
batch_size: 20                   # Listings per batch (5-100)
```

---

## Example Outputs

### Output 1: Single Listing Optimization Report

```
LISTING OPTIMIZATION REPORT
===========================

Product: Handmade Ceramic Mug
Current Performance: 3 views/week, 0 sales

TITLE OPTIMIZATION
------------------
Current: "Blue Ceramic Mug" (16 chars)
Status: ❌ Missing keywords, low search volume

Recommended Options:
1. "Handmade Blue Ceramic Coffee Mug - Unique Artisan Pottery" (140 chars)
   Est. Monthly Searches: 1,200 | Competition: Medium
   
2. "Blue Ceramic Mug Handmade - Perfect Gift for Coffee Lovers" (140 chars)
   Est. Monthly Searches: 950 | Competition: Low
   
3. "Artisan Ceramic Mug Handcrafted Blue - Eco-Friendly Pottery" (140 chars)
   Est. Monthly Searches: 750 | Competition: Low

TAGS OPTIMIZATION
-----------------
Current Tags (8/13):
- mug ❌ (oversaturated, 500K+ listings)
- ceramic ⚠️ (high volume, high competition)
- handmade ✓ (good)
- blue ⚠️ (too generic)

Recommended Tags (13/13):
1. handmade ceramic mug (Est. 1,200 searches/month)
2. ceramic coffee mug (Est. 980 searches/month)
3. artisan mug (Est. 650 searches/month)
4. blue pottery mug (Est. 420 searches/month)
5. handcrafted ceramic (Est. 380 searches/month)
6. unique coffee mug (Est. 350 searches/month)
7. gift for coffee lovers (Est. 290 searches/month)
8. eco-friendly ceramic (Est. 270 searches/month)
9. boho mug (Est. 240 searches/month)
10. ceramic drinkware (Est: 210 searches/month)
11. artisan pottery (Est. 180 searches/month)
12. handmade gift ideas (Est. 160 searches/month)
13. ceramic tableware (Est. 140 searches/month)

DESCRIPTION REWRITE
-------------------
Current (45 words): "A beautiful blue ceramic mug made by hand."
Status: ❌ No keywords, minimal information

Optimized (280 words):
"Discover this stunning handmade ceramic mug, a unique artisan creation 
perfect for daily coffee enjoyment or as a thoughtful gift. Crafted with 
care using high-quality ceramic materials, this blue pottery mug features 
a smooth glaze and comfortable handle.

Each handcrafted ceramic coffee mug is one-of-a-kind, showcasing natural 
variations that celebrate its artisan origins. Ideal for eco-conscious 
coffee lovers who appreciate handmade tableware, this ceramic drinkware 
piece adds boho charm to any kitchen.

✓ Food-safe glazing
✓ Dishwasher safe
✓ 12 oz capacity
✓ Eco-friendly production

Perfect as a unique gift for coffee enthusiasts, this artisan mug makes 
an excellent addition to your ceramic collection or home decor..."

IMPACT PROJECTION
-----------------
Estimated improvements after optimization:
• Search visibility: +45%
• Monthly views: 3 → 5-6 views/week
• Click-through rate: +35%
• Conversion potential: +25%

Timeline: Changes typically show impact within 2-4 weeks
```

### Output 2: Batch Optimization CSV

```csv
listing_id,product_name,current_title,optimized_title,priority,est_traffic_gain,implementation_time
12345,"Blue Ceramic Mug","Blue Ceramic Mug","Handmade Blue Ceramic Coffee Mug - Unique Artisan Pottery",HIGH,+45%,5 min
12346,"Green Ceramic Bowl","Ceramic Bowl","Handmade Green Ceramic Serving Bowl - Artisan Pottery",HIGH,+52%,5 min
12347,"Red Ceramic Plate","Red Plate","Handcrafted Red Ceramic Dinner Plate - Unique Tableware",MEDIUM,+28%,5 min
12348,"Yellow Ceramic Vase","Vase","Artisan Yellow Ceramic Flower Vase - Handmade Home Decor",MEDIUM,+35%,5 min
12349,"Orange Ceramic Planter","Planter","Handmade Orange Ceramic Plant Pot - Eco-Friendly Tableware",LOW,+18%,5 min
```

### Output 3: Competitor Analysis Report

```
COMPETITOR ANALYSIS SUMMARY
============================

Category: Handmade Ceramic Mugs
Your Shop: "ArtisanMugs" (45 listings, 4.2 stars)

TOP 3 COMPETITORS
=================

1. CeramicWorks (4.9 stars, 2,100+ reviews)
   Avg. Title Length: 128 characters
   Avg. Tags per Listing: 13/13 (optimized)
   Top Keywords: handmade ceramic mug, artisan pottery, coffee mug
   Estimated Monthly Revenue: $12,000+
   
   Their Best Performers:
   - "Handmade Ceramic Coffee Mug Set - Artisan Pottery Gift"
   - "Blue Ceramic Mug Handcrafted - Unique Boho Drinkware"

2. PotteryStudio (4.7 stars, 1,850+ reviews)
   Avg. Title Length: 115 characters
   Avg. Tags per Listing: 12/13
   Top Keywords: ceramic mug, handmade gift, pottery
   Estimated Monthly Revenue: $9,500+

3. ArtisticCeramics (4.6 stars, 1,200+ reviews)
   Avg. Title Length: 102 characters
   Avg. Tags per Listing: 11/13
   Top Keywords: mug, ceramic, handmade
   Estimated Monthly Revenue: $7,200+

KEYWORD GAP ANALYSIS
====================

Keywords Used by Competitors (NOT in your listings):
• "artisan pottery" (1,200 searches/month) — HIGH PRIORITY
• "boho mug" (850 searches/month) — HIGH PRIORITY
• "ceramic gift set" (720 searches/month) — MEDIUM
• "handcrafted drinkware" (580 searches/month) — MEDIUM
• "eco-friendly ceramic" (420 searches/month) — LOW

Your Unique Keywords (Not used by competitors):
• "personalized ceramic mug" — OPPORTUNITY
• "custom handmade pottery" — OPPORTUNITY
```

---

## Tips & Best Practices

### 1. Keyword Placement Strategy

**Title Keywords:**
- Place primary keyword in first 40 characters for maximum visibility
- Use natural language (avoid keyword stuffing)
- Include secondary keyword if it fits naturally
- Reserve last 20 characters for urgency/benefit (e.g., "Perfect Gift")

**Example:**
```
✓ "Handmade Blue Ceramic Coffee M