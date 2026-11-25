---
name: micro-niche-authority-validator
description: "Validate micro-niche viability with search volume analysis, competitor saturation metrics, and monetization signals. Use when the user needs market validation, niche research, or go/no-go decisions before launching."
version: 1.0.0
homepage: https://github.com/ncreighton/empire-skills
metadata:
  {
    "openclaw": {
      "requires": {
        "env": ["SEMRUSH_API_KEY", "GOOGLE_TRENDS_API_KEY", "SERPSTACK_API_KEY"],
        "bins": []
      },
      "os": ["macos", "linux", "win32"],
      "files": ["SKILL.md"],
      "emoji": "📊"
    }
  }
---

# Micro-Niche Authority Validator

## Overview

The **Micro-Niche Authority Validator** is a production-grade market research automation skill that evaluates whether a micro-niche opportunity is worth pursuing before you invest time and capital.

This skill analyzes four critical validation pillars:

1. **Search Volume & Trends** — Google Trends historical data + SEMrush keyword metrics to identify growing vs. declining niches
2. **Competitor Saturation** — Domain Authority distribution analysis to assess competitive landscape density
3. **Monetization Signals** — Identification of active affiliate programs, SaaS tools, and commercial intent keywords
4. **Audience Intent Patterns** — Deep-dive into searcher behavior, question density, and buyer readiness

The skill outputs a **Viability Score (1–100)** with specific, actionable go/no-go recommendations backed by data. Perfect for solopreneurs, content creators, SaaS founders, and agency strategists validating niche markets before launch.

### Why This Matters
Choosing the wrong niche costs months of wasted effort. This skill eliminates guesswork by automating the research that typically takes 20+ hours of manual analysis across Google Trends, Ahrefs, SEMrush, and competitor sites.

### Integrations & Data Sources
- **Google Trends API** — Historical search interest and geographic breakdowns
- **SEMrush API** — Exact search volumes, keyword difficulty, and trend direction
- **SerpStack** — Live SERP analysis for competitor domain authority distribution
- **Slack** — Direct report delivery to your team
- **Airtable/Google Sheets** — Automated niche pipeline management
- **WordPress** — Publish validation reports as private blog posts

---

## Quick Start

### Example 1: Validate a Broad Micro-Niche
```
Validate the niche: "Best ergonomic keyboards for programmers"
Include: 3-year search volume trends, top 10 competitors with DA scores, 
affiliate programs in the space, and monetization difficulty
```

**Expected Output Time:** 2-3 minutes | **Report Depth:** Full 40+ metric analysis

### Example 2: Validate a Hyper-Specific Niche
```
Is "sustainable bamboo desk organizers" a viable niche?
Check: Monthly search volume, competitor count with authority distribution,
active Amazon affiliate programs, Etsy seller saturation, and buyer intent signals
```

**Expected Output Time:** 1-2 minutes | **Report Depth:** Saturated niche assessment

### Example 3: Compare Multiple Niches
```
Compare these three niches and rank by viability:
1. "Low-FODMAP meal planning for IBS"
2. "Vintage film camera restoration"
3. "Python web scraping tutorials"

Return viability scores, key differentiators, and which has the strongest monetization signals
```

**Expected Output Time:** 3-4 minutes | **Report Depth:** Competitive analysis matrix

---

## Capabilities

### 1. Search Volume & Trend Analysis
The skill integrates with **Google Trends API** and **SEMrush** to:
- Extract 3–5 year historical search volume data
- Identify seasonal patterns and growth/decline trajectories
- Flag emerging vs. declining niches
- Compare global vs. regional search interest
- Calculate year-over-year growth rates

**Example Output:**
```
Search Volume Analysis:
├─ Current Monthly Volume: 4,200 searches
├─ 3-Year Trend: +23% YoY growth (strong upward trajectory)
├─ Seasonality: 15% variation (stable year-round)
├─ Geographic Hotspots: US (45%), UK (18%), Canada (12%)
└─ Verdict: Growing niche with consistent demand
```

### 2. Competitor Saturation Mapping
Uses **SerpStack** SERP analysis to evaluate:
- Top 10 competitor domain authority distribution
- Average DA of page-1 results
- Newer domains ranking (opportunity indicator)
- Content gap analysis
- Backlink saturation levels

**Example Output:**
```
Competitor Landscape:
├─ Average DA of Top 10: 42 (moderate barrier to entry)
├─ Newest Domain on Page 1: 2.4 years old (fresh competitors possible)
├─ Authority Distribution: [68, 61, 54, 48, 43, 38, 35, 31, 28, 24]
├─ Saturation Level: Medium (7/10)
└─ Entry Difficulty: Moderate — doable for established content creators
```

### 3. Monetization Signal Detection
Automated identification of:
- Active affiliate programs (Amazon Associates, CJ Affiliate, ShareASale)
- SaaS tools targeting the niche (detected via SERP ads)
- Digital product opportunities (courses, templates, tools)
- Service monetization potential (consulting, coaching)
- Advertising CPM estimates (via competitor site analysis)

**Example Output:**
```
Monetization Opportunities:
├─ Affiliate Programs Found: 8 active programs
│  ├─ Amazon Associates (high volume products)
│  ├─ Specialized affiliate networks (2x average commission)
│  └─ Direct sponsor partnerships (5 B2B companies targeting niche)
├─ SaaS Tools Operating Here: 12 tools (recurring revenue model)
├─ Digital Product Demand: High (Q&A sites show course/template requests)
├─ Estimated Monthly CPM: $8-12 (Google Adsense)
└─ Monetization Difficulty: Easy (multiple revenue streams available)
```

### 4. Audience Intent Pattern Analysis
Analyzes:
- Question-type keywords (How-to, Reviews, Comparisons, Problems)
- Buyer intent distribution (Research vs. Purchase keywords)
- Long-tail keyword opportunities
- Pain-point identification from question analysis
- Content format preferences (guides, tools, reviews, videos)

**Example Output:**
```
Audience Intent Breakdown:
├─ Problem-Solving Keywords: 62% (strong pain points present)
├─ Product Review Keywords: 23% (buying signals detected)
├─ How-To/Educational: 15% (tutorial demand)
├─ Pain Points Identified: 
│  ├─ Cost (budget-conscious audience)
│  ├─ Complexity (beginner-friendly solutions wanted)
│  └─ Time investment (quick-win seekers)
└─ Content Strategy: Comparison guides + problem-solving tutorials = high ROI
```

### 5. Viability Score Calculation
Composite score weighing:
- **Search Volume (25%)** — Growth trajectory and absolute search volume
- **Saturation (20%)** — Competitor count and authority distribution
- **Monetization (30%)** — Number of revenue streams and CPM potential
- **Intent (25%)** — Buying signals and pain-point clarity

**Score Interpretation:**
- **80–100:** Go! Green-light niche with strong fundamentals
- **60–79:** Proceed with caution — Viable but requires differentiation
- **40–59:** High-risk — Consider alternatives unless you have unique angle
- **1–39:** No-go — Skip this niche, poor fundamentals across metrics

---

## Configuration

### Required Environment Variables
Set these before using the skill:

```bash
export SEMRUSH_API_KEY="your_semrush_api_key"
export GOOGLE_TRENDS_API_KEY="your_google_trends_api_key"
export SERPSTACK_API_KEY="your_serpstack_api_key"
```

### Optional Configuration
```javascript
{
  "report_format": "json|markdown|html",
  "analysis_depth": "quick|standard|deep",
  "competitor_sample_size": 10,
  "trend_lookback_months": 36,
  "include_geographic_breakdown": true,
  "slack_notification": true,
  "slack_webhook_url": "https://hooks.slack.com/services/YOUR/WEBHOOK/URL"
}
```

### Setup Instructions
1. **Get API Keys:**
   - SEMrush: Create account at semrush.com, generate API key
   - Google Trends: Enable Google Trends API in Google Cloud Console
   - SerpStack: Sign up at serpstack.com for free tier (1,000 requests/month)

2. **Install Dependencies:**
   - Requests library for API calls
   - Pandas for data analysis
   - JSON for parsing

3. **Authenticate:**
   ```bash
   openclaw config set SEMRUSH_API_KEY "your_key_here"
   openclaw config set GOOGLE_TRENDS_API_KEY "your_key_here"
   openclaw config set SERPSTACK_API_KEY "your_key_here"
   ```

4. **Test Connection:**
   ```
   Validate niche: "test keyword"
   ```

---

## Example Outputs

### Sample Full Report: "Mechanical Keyboard Keycaps"

```
╔════════════════════════════════════════════════════════════════════╗
║        MICRO-NICHE AUTHORITY VALIDATION REPORT                    ║
║        Niche: Mechanical Keyboard Keycaps                          ║
║        Analysis Date: 2024-01-15                                  ║
╚════════════════════════════════════════════════════════════════════╝

📊 VIABILITY SCORE: 78/100 [PROCEED WITH CAUTION]

─────────────────────────────────────────────────────────────────────
1️⃣  SEARCH VOLUME & TRENDS (78/100)

Current Monthly Volume: 12,400 searches
3-Year Trend: +18% YoY (steady growth)
Seasonal Pattern: Peak Sept-Dec (+35% during holidays)
Google Trends Slope: Upward ↗

Key Insight: Consistent growth with strong seasonal spike.
Recommendation: Launch content pre-September to capitalize on Q4 demand.

─────────────────────────────────────────────────────────────────────
2️⃣  COMPETITOR SATURATION (72/100)

Top 10 Competitor Domain Authority:
  1. mechanicalkeyboards.com    DA: 68
  2. keychron.com               DA: 65
  3. switchandclick.com         DA: 52
  4. reddit.com/r/...           DA: 92 (forum, not direct competitor)
  5. amazon.com (keycaps)       DA: 98 (not organic competitor)
  6. etsy.com (custom keycaps)  DA: 96 (marketplace, not direct)
  7. projectkeyboard.com        DA: 48
  8. desksetup.org              DA: 42
  9. customkeystyles.com        DA: 38
  10. keycap-guide.blogspot.com DA: 28

Average Relevant DA (organic only): 45
Saturation Level: 6.5/10 (MODERATE)
Newest Competitor Entry: 1.2 years ago
Opportunity Index: MEDIUM (fresh competitors entering, but space not saturated)

Key Insight: Authority barrier is moderate. Page 1 possible within 6-12 months
with strong content and backlinks.

─────────────────────────────────────────────────────────────────────
3️⃣  MONETIZATION SIGNALS (82/100)

Affiliate Programs Available:
  ✓ Amazon Associates (primary keycap products in stock)
  ✓ MechanicalKeyboards.com Affiliate Program (12% commission)
  ✓ Keychron Affiliate Program (10% commission)
  ✓ Drop.com Affiliate Program (5-15% commission)
  ✓ Etsy Affiliate Program (4% commission)

SaaS Tools Targeting This Niche: 4
  - Mechanical Keyboard PCB Design Tools
  - Keycap Design & 3D Printing Services
  - Typing Test Platforms (sponsorship potential)

Direct Monetization Opportunities:
  ✓ Digital Products: Keycap design guides, collection catalogs, reviews
  ✓ Services: Keycap customization, photography services for collectors
  ✓ Sponsorships: Keycap manufacturers (8 identified active sponsors)
  ✓ Advertising CPM: $12-18/1000 impressions (tech enthusiast audience)

Estimated Monthly Revenue (if 10K monthly visitors):
  - Affiliate commissions: $400-800/mo
  - Sponsorships: $500-1,200/mo
  - Digital products: $300-600/mo
  - Display ads: $120-180/mo
  ─────────────────────────
  TOTAL POTENTIAL: $1,320-2,780/mo

Key Insight: Multiple revenue streams available. Niche supports full-time
income potential with audience scale of 20K+ monthly visitors.

─────────────────────────────────────────────────────────────────────
4️⃣  AUDIENCE INTENT ANALYSIS (78/100)

Keyword Intent Distribution:
  • Product Reviews: 35% ("best mechanical keyboard keycaps", "keycap comparison")
  • Problem-Solving: 28% ("how to replace keycaps", "keycap compatibility")
  • Buying Intent: 22% ("where to buy", "cheap keycaps")
  • Entertainment/Community: 15% (aesthetic builds, collections)

Primary Pain Points Identified:
  🔴 Keycap Compatibility Issues
     → Opportunity: Comprehensive compatibility guide with troubleshooting
  🔴 Overwhelmed by Options
     → Opportunity: Curated recommendation guides by use case/budget
  🔴 Quality Assessment Difficulty
     → Opportunity: Detailed review framework and comparison tool
  🔴 Aesthetic Customization
     → Opportunity: Visual guides, color matching, design templates

Content Format Preferences:
  • Long-Form Guides: 40% search intent
  • Video Reviews: 32% (YouTube dominates for visual comparison)
  • Comparison Tools/Lists: 18%
  • Galleries/Inspo: 10%

Audience Demographics:
  • Primary: Tech enthusiasts, 25-45 years old
  • Engagement: High (Reddit, Discord communities very active)
  • Spending Power: High (keycaps range $50-200+)

Key Insight: Review-driven audience with strong buying intent. Video + guide
combo strategy recommended.

─────────────────────────────────────────────────────────────────────
📋 FINAL RECOMMENDATION: PROCEED WITH CAUTION ⚠️

✅ STRENGTHS:
  • Growing niche with +18% YoY trajectory
  • Moderate competitor saturation (room for new entrants)
  • Multiple monetization streams
  • High-intent, engaged audience with spending power
  • Clear content gaps (guides, compatibility tools)

⚠️  CHALLENGES:
  • Requires video content for competitive advantage
  • Established players have significant authority (DA 65+)
  • Seasonal demand may require off-season content strategy
  • Niche appeal limits total addressable market

🎯 RECOMMENDED STRATEGY:
  1. DIFFERENTIATION: Focus on aesthetic/customization angle
     (less competitive than technical reviews)
  2. CONTENT MOAT: Build compatibility tools/guides competitors lack
  3. CHANNEL MIX: YouTube reviews + written guides for SEO
  4. MONETIZATION: Lead with affiliate partnerships, then digital products
  5. TIMELINE: 6-9 month investment to reach $1K/mo revenue

💰 VIABILITY: VIABLE (score: 78/100)
   With focused differentiation strategy, expect ROI within 12 months.
   Not a slam-dunk, but solid opportunity for patient builders.

─────────────────────────────────────────────────────────────────────
Generated: 2024-01-15 | Analysis Version: 1.0.0
```

---

## Tips & Best Practices

### 1. Validate Multiple Niches in Batch
Don't commit to a single