---
name: micro-niche-market-validator
description: "Validate micro-niche viability by analyzing search trends, Reddit/Twitter sentiment, competitor saturation, and buyer intent across 8 data sources. Use when the user needs TAM estimates, pricing benchmarks, and GO/NO-GO recommendations with hidden gem detection."
version: 1.0.0
homepage: https://github.com/ncreighton/empire-skills
metadata:
  {"openclaw":{"requires":{"env":["SEMRUSH_API_KEY","AHREFS_API_KEY","TWITTER_BEARER_TOKEN","REDDIT_CLIENT_ID","REDDIT_CLIENT_SECRET","GOOGLE_TRENDS_KEY"],"bins":["curl","python3"]},"os":["macos","linux","win32"],"files":["SKILL.md"],"emoji":"📊"}}
---

# Micro-Niche Market Validator

## Overview

The **Micro-Niche Market Validator** is a comprehensive market research automation tool that eliminates guesswork from niche selection. Instead of relying on gut feeling or outdated market reports, this skill aggregates real-time data from 8 authoritative sources to produce a defensible, data-driven viability score (1-100) with actionable GO/NO-GO recommendations.

### Why This Matters

Entrepreneurs and product developers waste months building in non-viable niches because they lack access to:
- **Real search demand** (not just keyword volume)
- **Authentic customer sentiment** from communities (Reddit, Twitter)
- **Competitive saturation metrics** (pricing power, market concentration)
- **Buyer intent signals** (search behavior, purchase readiness)
- **Hidden gem sub-niches** that competitors miss

This skill synthesizes all eight data sources into a single confidence score, eliminating analysis paralysis and accelerating market entry decisions.

### Integration Ecosystem

- **Google Trends API** — historical search volume and seasonality
- **Semrush API** — competitor keyword difficulty, traffic estimates, CPC
- **Ahrefs API** — backlink profiles, domain authority, competitive gaps
- **Twitter API v2** — real-time sentiment, influencer discussions, trend velocity
- **Reddit API** — community size, engagement depth, pain points
- **Google Search Console** — actual search behavior (if linked)
- **Shopify Product API** — e-commerce pricing benchmarks
- **Slack Integration** — automated reports delivered to channels

---

## Quick Start

### Example 1: Validate a B2B SaaS Niche

```
Analyze the viability of "AI-powered legal contract review for small law firms"

Use these parameters:
- Primary niche: legal tech
- Sub-niche: contract review automation
- Target market: small law firms (1-10 attorneys)
- Geographic focus: USA
- Budget ceiling: $50/month (per firm)

Output format: Detailed viability scorecard with TAM, pricing analysis, and competitor map.
```

**What You'll Get:**
- Viability Score: 72/100 (CONDITIONAL GO)
- Estimated TAM: $2.1B → SAM: $340M
- Monthly search volume: 8,200 (exact match)
- Competitor count: 23 direct, 156 indirect
- Sentiment: 76% positive (Reddit legal communities)
- Pricing benchmarks: $29-$199/month range
- Hidden gem: "Contract review for freelance lawyers" (lower saturation, higher intent)

---

### Example 2: Discover Hidden Gem Sub-Niches

```
Find underserved sub-niches within "sustainable fashion ecommerce"

Search criteria:
- Must have 500+ monthly searches
- Competitor saturation < 30
- Reddit engagement > 50 posts/week
- Price point: $100-$500
- Geographic markets: English-speaking

Return: Top 5 hidden gems ranked by opportunity score.
```

**What You'll Get:**
- Sub-niche #1: "Sustainable activewear for petite women" (Opportunity: 87/100)
- Sub-niche #2: "Eco-friendly business casual for remote workers" (81/100)
- Market size estimates for each
- Competitor analysis (gaps identified)
- Community sentiment quotes from niche communities

---

### Example 3: Competitive Pricing Intelligence

```
Analyze pricing strategy for "project management tools for agencies"

Include:
- Current market pricing (Semrush, Ahrefs data)
- Price sensitivity (Twitter/Reddit discussions)
- Willingness-to-pay signals (search behavior analysis)
- Revenue potential at different price points
- Competitor positioning (feature-to-price mapping)

Format: Executive summary + detailed pricing matrix.
```

**What You'll Get:**
- Market price range: $19-$299/month
- Optimal price point: $79/month (highest demand elasticity)
- Estimated first-year revenue potential
- Customer acquisition cost benchmarks
- Positioning recommendation vs. competitors

---

## Capabilities

### 1. Multi-Source Data Aggregation
Pulls from 8 authoritative sources simultaneously:
- **Search Volume Analysis**: Google Trends (historical), Semrush (current), keyword intent classification
- **Competitive Landscape**: Ahrefs domain authority, Semrush difficulty score, competitor count
- **Community Sentiment**: Reddit (r/entrepreneur, industry-specific subs), Twitter (hashtags, influencers), sentiment polarity scoring
- **Buyer Intent Signals**: Search query analysis (problem + solution keywords), CPC data, landing page trends
- **E-commerce Benchmarks**: Shopify store data, Stripe transaction patterns, industry pricing standards
- **Seasonality & Trends**: Google Trends velocity, Twitter spike detection, Reddit discussion volume trends

### 2. Viability Scoring Engine
Produces a defensible 1-100 score based on weighted factors:
```
Score Components:
- Search Demand (25%): Volume + intent quality + trend direction
- Competitive Saturation (20%): Competitor count + market concentration
- Sentiment Quality (15%): Positive/negative ratio + community size
- Buyer Intent (15%): CPC, click-through rates, landing page quality
- TAM Viability (15%): Market size * addressable percentage
- Pricing Power (10%): Willingness-to-pay signals + price elasticity

GO Threshold: 70+
CONDITIONAL GO: 50-69 (requires validation)
NO-GO: <50
```

### 3. TAM/SAM Estimation
- **Total Addressable Market (TAM)**: Industry-wide opportunity
- **Serviceable Addressable Market (SAM)**: Your target segment size
- **Serviceable Obtainable Market (SOM)**: Realistic 5-year capture
- Includes geographic breakdown and pricing-based revenue models

### 4. Hidden Gem Detection Algorithm
Identifies underserved sub-niches using proprietary scoring:
```
Opportunity Score = (Search Volume × Sentiment Strength) / Competitor Saturation × (1 + Trend Velocity)
```
Filters for:
- Sufficient search demand (500+ monthly searches minimum)
- Low competitive saturation (<50 direct competitors)
- High community engagement (Reddit/Twitter velocity)
- Emerging trends (growth trajectory >15% YoY)

### 5. Competitive Positioning Map
Visual/textual mapping of:
- Feature matrix (you vs. top 5 competitors)
- Pricing positioning
- Target customer overlap
- White-space opportunities

### 6. Sentiment Analysis at Scale
- Pull 1,000+ Reddit/Twitter mentions (with context)
- Classify as problem statement, solution discussion, or pricing objection
- Extract exact pain points and feature requests
- Identify influencers and brand advocates

---

## Configuration

### Required Environment Variables

```bash
# Semrush API
export SEMRUSH_API_KEY="your_semrush_api_key"

# Ahrefs API
export AHREFS_API_KEY="your_ahrefs_api_key"

# Twitter API v2 (for sentiment analysis)
export TWITTER_BEARER_TOKEN="your_twitter_bearer_token"

# Reddit API
export REDDIT_CLIENT_ID="your_reddit_client_id"
export REDDIT_CLIENT_SECRET="your_reddit_client_secret"

# Google Trends (public API, no key required, but supports authenticated requests)
export GOOGLE_TRENDS_KEY="your_google_api_key"

# Optional: Slack integration
export SLACK_WEBHOOK_URL="https://hooks.slack.com/services/YOUR/WEBHOOK/URL"
```

### Setup Instructions

1. **Obtain API Keys:**
   - Semrush: Sign up at semrush.com, API section → generate key
   - Ahrefs: ahrefs.com/api → create application
   - Twitter: developer.twitter.com → create project → generate Bearer Token
   - Reddit: reddit.com/prefs/apps → create app → copy credentials

2. **Install Dependencies:**
   ```bash
   pip install requests pandas numpy tweepy praw beautifulsoup4 aiohttp
   ```

3. **Add Environment Variables to Your System:**
   ```bash
   # macOS/Linux
   echo 'export SEMRUSH_API_KEY="key_here"' >> ~/.zshrc
   source ~/.zshrc
   
   # Windows (PowerShell)
   [Environment]::SetEnvironmentVariable("SEMRUSH_API_KEY", "key_here", "User")
   ```

4. **Test Connectivity:**
   ```
   Run a simple validation query: "Test API connection for sustainable fashion niche"
   ```

### Optional Configuration Parameters

```yaml
analysis_depth: "comprehensive"  # Options: quick (2 sources), standard (5 sources), comprehensive (all 8)
report_format: "json"            # Options: json, markdown, html, pdf
include_visuals: true            # Generate charts (requires matplotlib)
slack_notify: true               # Send results to Slack channel
sample_size: 1000                # Reddit/Twitter mentions to analyze
date_range: "12m"                # Historical data window (1m, 3m, 6m, 12m)
```

---

## Example Outputs

### Output 1: Complete Viability Report (JSON Format)

```json
{
  "niche": "AI-powered meal planning for keto dieters",
  "analysis_date": "2024-01-15",
  "viability_score": 78,
  "recommendation": "GO",
  "confidence": 0.92,
  "summary": {
    "tam": {
      "total": "$4.2B",
      "sam": "$1.1B",
      "som_5yr": "$47M"
    },
    "search_demand": {
      "monthly_volume": 22400,
      "trend_direction": "up_15_percent_yoy",
      "intent_quality": "high",
      "cpc": "$2.14"
    },
    "competition": {
      "direct_competitors": 34,
      "saturation_score": 42,
      "leader_market_share": "12%"
    },
    "sentiment": {
      "positive_ratio": 0.82,
      "reddit_communities": [
        {"name": "r/keto", "subscribers": 2100000, "posts_weekly": 8900},
        {"name": "r/EatCheapAndHealthy", "subscribers": 1900000, "posts_weekly": 4200}
      ],
      "sample_pain_points": [
        "Macro tracking is tedious and error-prone",
        "Meal prep planning takes 3+ hours weekly",
        "Hard to find keto recipes without carb fillers"
      ]
    },
    "pricing": {
      "market_range": "$9.99-$49.99/month",
      "optimal_point": "$19.99/month",
      "revenue_potential_yr1": "$340K",
      "estimated_customer_acq_cost": "$18-$32"
    },
    "hidden_gems": [
      {
        "name": "Keto meal planning for shift workers",
        "opportunity_score": 84,
        "monthly_searches": 3200,
        "competitors": 8
      },
      {
        "name": "Macro-optimized meal plans for competitive athletes",
        "opportunity_score": 79,
        "monthly_searches": 5100,
        "competitors": 12
      }
    ]
  }
}
```

### Output 2: Competitive Positioning Summary

```markdown
## Competitive Landscape Analysis

| Competitor | Monthly Searches | Price | Rating | Market Position |
|-----------|------------------|-------|--------|-----------------|
| MyFitnessPal | 2.1M | Free → $10/mo | 4.2★ | Market Leader |
| Cronometer | 340K | Free → $40/yr | 4.6★ | Niche Leader (nutrition) |
| Carb Manager | 280K | $4.99/mo | 4.1★ | Direct Competitor |
| **Your Opportunity** | **22.4K** | **$19.99/mo** | **TBD** | **Underserved Segment** |

### White-Space Findings:
- **Gap 1**: No meal planning tools optimize for shift workers specifically
- **Gap 2**: Athletes seeking macro optimization lack real-time feedback
- **Gap 3**: Keto community (r/keto: 2.1M members) underserved by major players

### Recommendation:
Position as "Keto-first, athlete-focused alternative with 10-minute meal planning"
```

### Output 3: Sentiment Deep-Dive (Text Format)

```
REDDIT SENTIMENT ANALYSIS (r/keto, 1,000 posts sampled)

Top Problems Mentioned:
1. "Meal planning takes too long" — 247 mentions (24.7%)
2. "Macro tracking is complicated" — 156 mentions (15.6%)
3. "Can't find good keto recipes easily" — 134 mentions (13.4%)
4. "Expensive to eat keto without planning" — 98 mentions (9.8%)

Feature Requests (Explicit):
- One-click meal plan generation
- Automatic macro adjustment based on activity
- Integration with fitness trackers
- Grocery list auto-generation with prices

TWITTER SENTIMENT ANALYSIS (hashtag: #ketomealprep, 500 tweets sampled)

Sentiment Distribution:
- Positive: 342 (68.4%)
- Neutral: 128 (25.6%)
- Negative: 30 (6.0%)

Influencers & Brand Advocates:
- @KetoConnect (145K followers) — discusses meal planning pain weekly
- @TheDietDoctor (230K followers) — 15 keto tool reviews/year
- @CaseyJones_Keto (87K followers) — micro-influencer, high engagement
```

---

## Tips & Best Practices

### 1. **Validate the Score with Manual Research**
While the algorithm is comprehensive, use the score as a starting point, not gospel:
- Interview 10 people in your target niche (Reddit DM, Twitter, LinkedIn)
- Check if top competitors are hiring (sign of growth) or quiet (sign of decline)
- Analyze customer reviews on Trustpilot/G2 to identify pain points the algorithm may miss

### 2. **Focus on Hidden Gems First**
Instead of attacking crowded niches with 100+ competitors, prioritize sub-niches with:
- Viability score 70+
- Competitor count <50
- Trend velocity >12% growth
- These have 3-5x faster time-to-profitability

### 3. **Use TAM Estimates for Fundraising**
Structure your pitch with skill outputs:
```
Total Addressable Market: $4.2B
Serviceable Addressable Market: $1.1B (niche focus)
Year 1 Revenue Target: $340K (5% conversion of TAM)
Year 3 Projection: $8.2M (market penetration: 0.74%)
```

### 4. **Monitor Trends Over Time**
Run this skill quarterly on shortlisted niches to track:
- Search volume velocity (is demand growing or declining?)
- Sentiment shifts (are pain points being solved?)
- New competitor entries (is the space heating up?)

### 5. **Cross-Reference Sentiment with Willingness-to-Pay**
High community sentiment + high CPC = strong willingness-to-pay:
```
Example: Keto meal planning has 82% positive sentiment + $2.14 CPC
→ Indicates strong pain-to-solution mapping + financial resources
→ Viable for SaaS pricing ($19.99+ monthly)
```

### 6. **Use Competitor Pricing as a Floor, Not a Ceiling**
If all competitors charge $9.99/month but sentiment indicates premium demand:
- Test $