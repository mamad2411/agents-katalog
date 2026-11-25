---
name: micro-influencer-audience-authenticity-auditor
description: "Analyze micro-influencer audiences (1K-100K followers) for authenticity using engagement velocity, sentiment analysis, and bot detection. Use when the user needs influencer vetting, audience validation, or ROI negotiation data."
version: 1.0.0
homepage: https://github.com/ncreighton/empire-skills
metadata:
  {"openclaw":{"requires":{"env":["INSTAGRAM_GRAPH_API_KEY","TWITTER_API_KEY","TIKTOK_API_KEY","HUME_API_KEY","RAPIDAPI_KEY"],"bins":["python3","curl"]},"os":["macos","linux","win32"],"files":["SKILL.md"],"emoji":"🔍"}}
---

# Micro-Influencer Audience Authenticity Auditor

## Overview

The **Micro-Influencer Audience Authenticity Auditor** is a comprehensive vetting tool designed for marketing teams, agencies, and brand managers who need to validate creator authenticity before investing in partnerships. This skill analyzes follower profiles across Instagram, TikTok, and Twitter (1K-100K follower range) using machine learning-powered engagement pattern detection, comment sentiment analysis, and demographic coherence scoring.

Instead of relying on surface-level metrics (follower count, engagement rate), this skill identifies:

- **Bot follower percentages** using behavioral clustering algorithms
- **Engagement velocity anomalies** (sudden spikes suggesting purchased engagement)
- **Audience demographic misalignment** (followers don't match creator's niche)
- **Comment authenticity scores** using NLP sentiment and linguistic patterns
- **Industry benchmark comparisons** (e.g., "Fashion micro-influencers average 5.2% bot followers; this creator has 23%")

The output includes an **Authenticity Score (0-100)**, specific **Risk Flags**, and **ROI Negotiation Leverage** data—actionable intelligence for contract negotiation and campaign forecasting.

**Perfect for:** Marketing agencies vetting creators for brand partnerships, influencer marketplaces (like AspireIQ, Upfluence), in-house brand teams, and content networks (YouTube Networks, TikTok collectives).

---

## Quick Start

Try these prompts immediately to see the auditor in action:

### Prompt 1: Basic Authenticity Audit
```
Audit the audience authenticity for Instagram creator @sarah_lifestyle 
who has 47,000 followers in the fashion/beauty niche. 
Provide authenticity score, bot detection analysis, and engagement velocity patterns.
```

### Prompt 2: Comparative Benchmarking
```
Analyze TikTok creator @alex_fitness (52K followers, fitness vertical) 
and compare their audience metrics against industry benchmarks 
for fitness micro-influencers. Flag any anomalies.
```

### Prompt 3: ROI Negotiation Brief
```
I'm considering a $15,000 partnership with Twitter creator @tech_insights (38K followers, tech niche).
Generate an authenticity report with specific bot percentage, risk flags, 
and ROI adjustment recommendations for contract negotiation.
```

### Prompt 4: Batch Vetting Multiple Creators
```
Audit these 5 Instagram creators for a beauty brand campaign:
- @creator_a (25K followers)
- @creator_b (64K followers)
- @creator_c (18K followers)
- @creator_d (89K followers)
- @creator_e (41K followers)

Rank them by authenticity score and flag any high-risk profiles.
```

---

## Capabilities

### 1. **Bot & Fake Follower Detection**
Analyzes follower account characteristics using HumingFace ML models:
- Account age distribution (new accounts = higher bot risk)
- Bio completeness and coherence
- Profile picture quality (generic stock images flagged)
- Behavioral clustering (identifies accounts with identical follow/like patterns)
- Growth spike detection (flags sudden 10K+ follower spikes)

**Usage Example:**
```
Show me the bot follower breakdown for @sarah_lifestyle's audience.
What percentage are likely fake/bot accounts?
```

**Output includes:**
- Bot follower percentage (0-100%)
- Confidence level (low/medium/high)
- Top bot indicators found

### 2. **Engagement Velocity Analysis**
Detects purchased or artificial engagement using time-series analysis:
- Post engagement rate consistency (flagged if varies 300%+ month-to-month)
- Like-to-comment ratio (natural: 15:1 to 25:1; suspicious: >50:1)
- Engagement velocity curve (natural engagement decays exponentially; artificial plateaus)
- Timing pattern analysis (real followers engage 24/7; bots show timezone clustering)

**Usage Example:**
```
Analyze engagement velocity for @alex_fitness TikTok account over the last 6 months.
Are there signs of purchased engagement or bot activity?
```

### 3. **Comment Sentiment & Authenticity Scoring**
Uses NLP to analyze comment authenticity:
- Sentiment polarity (negative/neutral/positive distribution)
- Linguistic pattern matching (spam, generic praise, copy-paste comments)
- Comment-to-engagement ratio coherence
- Language diversity (real audiences have 40+ languages in comments; bot comment farms have 1-3)
- Conversation depth (real followers reply to each other; bots only reply to creator)

**Usage Example:**
```
Score the authenticity of comments on @tech_insights recent posts.
Are followers having real conversations or just leaving generic praise?
```

### 4. **Audience Demographic Coherence**
Validates audience alignment with creator's niche:
- Gender distribution coherence (e.g., 89% female followers for fashion creator = expected)
- Age range alignment (18-24 year old followers for Gen-Z creator niche)
- Geographic clustering (follower countries vs. creator's claimed markets)
- Interest graph validation (follower interests vs. creator's content pillars)
- Language distribution alignment

**Usage Example:**
```
Validate that @sarah_lifestyle's 47K followers are demographically aligned 
with the fashion/beauty niche. Flag any misaligned audience segments.
```

### 5. **Industry Benchmark Comparison**
Compares creator metrics against 50K+ micro-influencer database:
- Average bot percentage by vertical (Fashion: 4.2%, Tech: 6.8%, Fitness: 5.1%)
- Expected engagement rates by follower count
- Comment authenticity percentiles
- Growth velocity benchmarks
- Risk flag prevalence in niche

**Usage Example:**
```
Show me how @alex_fitness compares to other fitness micro-influencers 
in the 50K-60K follower range. What's the benchmark for bot followers?
```

### 6. **ROI Negotiation Intelligence**
Calculates expected campaign ROI adjustments based on authenticity:
- Authentic follower count (total followers × authenticity %)
- Estimated reach reduction (bot follower percentage)
- Expected conversion rate adjustments
- Recommended budget discount/premium
- Risk-adjusted CPM projection

**Usage Example:**
```
For a $15,000 brand partnership deal, what ROI adjustments should I factor in 
based on @sarah_lifestyle's audience authenticity? What's my negotiation leverage?
```

---

## Configuration

### Required Environment Variables

Set these before using the skill:

```bash
# Instagram API Access
export INSTAGRAM_GRAPH_API_KEY="your-meta-graph-api-key"

# Twitter/X API Access
export TWITTER_API_KEY="your-twitter-api-v2-key"
export TWITTER_API_SECRET="your-twitter-secret"

# TikTok API Access
export TIKTOK_API_KEY="your-tiktok-api-key"

# ML/NLP Services
export HUME_API_KEY="your-humeai-key"  # For comment sentiment analysis
export RAPIDAPI_KEY="your-rapidapi-key"  # For supplementary data

# Optional: Webhook for batch results
export WEBHOOK_URL="https://your-domain.com/influencer-audits"
```

### Optional Configuration Parameters

```yaml
# analysis_depth: "quick" | "standard" | "deep"
# - quick: 100 posts, 1K comments (2-3 minutes)
# - standard: 500 posts, 5K comments (5-8 minutes)
# - deep: 1000 posts, 15K comments (15-20 minutes)
analysis_depth: "standard"

# include_competitors: true/false
# Compare against similar creators in same niche
include_competitors: true

# benchmark_database: "micro_influencers_1k_100k" (default, curated)
# Industry-specific benchmarks available
benchmark_database: "micro_influencers_1k_100k"

# platforms: ["instagram", "tiktok", "twitter", "youtube"]
# Which platforms to audit (multi-platform coming soon)
platforms: ["instagram"]

# risk_sensitivity: "conservative" | "balanced" | "aggressive"
# - conservative: flag at 10% bot followers
# - balanced: flag at 15% bot followers
# - aggressive: flag at 20% bot followers
risk_sensitivity: "balanced"
```

---

## Example Outputs

### Example 1: Individual Creator Authenticity Report

```
═══════════════════════════════════════════════════════════════
AUTHENTICITY AUDIT REPORT
Creator: @sarah_lifestyle
Platform: Instagram
Follower Count: 47,230
Niche: Fashion & Beauty
Analysis Date: 2024-01-15
═══════════════════════════════════════════════════════════════

📊 AUTHENTICITY SCORE: 78/100
Status: MODERATE RISK (Negotiate 20-25% budget discount)

───────────────────────────────────────────────────────────────
🤖 BOT FOLLOWER ANALYSIS
───────────────────────────────────────────────────────────────
Total Followers: 47,230
Estimated Bot Followers: 10,852 (23%)
Authentic Followers: 36,378 (77%)
Confidence Level: HIGH (92%)

Bot Follower Breakdown:
  • Inactive bots (0 engagement): 8.2%
  • Comment-spam bots: 9.1%
  • Engagement-pod bots: 5.7%
  • Likely authentic: 77%

Top Bot Indicators:
  ✓ 312 accounts created within 48 hours of creator follow
  ✓ Generic placeholder bios (32% of flagged accounts)
  ✓ Stock profile pictures (186 accounts)
  ✓ Zero-follower accounts following (214 accounts)

───────────────────────────────────────────────────────────────
📈 ENGAGEMENT VELOCITY ANALYSIS
───────────────────────────────────────────────────────────────
Average Engagement Rate: 4.2%
Benchmark (Fashion, 45K): 5.8%
Status: ⚠️ 27% BELOW BENCHMARK

Engagement Consistency Score: 62/100
  • Month 1 (Nov): 4.8% avg engagement
  • Month 2 (Dec): 3.1% avg engagement (-35% decline)
  • Month 3 (Jan): 4.7% avg engagement (+52% spike)

⚠️ ANOMALY DETECTED: Dec engagement drop suggests audience fatigue 
or disengagement. Jan spike consistent with New Year engagement pods.

Like-to-Comment Ratio: 28:1
Benchmark: 18:1
Status: ⚠️ ELEVATED (Suggests some purchased likes)

Post Engagement Decay Curve: 87% match to natural pattern
Status: ✓ AUTHENTIC (Low bot amplification)

───────────────────────────────────────────────────────────────
💬 COMMENT AUTHENTICITY ANALYSIS
───────────────────────────────────────────────────────────────
Comments Analyzed: 4,247
Authentic Comments: 3,401 (80%)
Spam/Generic Comments: 689 (16%)
Bot-Identified Comments: 157 (4%)

Comment Sentiment Distribution:
  • Positive: 72%
  • Neutral: 19%
  • Negative: 9%
Authenticity: HIGH (Natural negativity present)

Generic Comment Phrases Detected:
  • "Beautiful!" - 312 instances (7.3% of comments)
  • "Amazing content" - 187 instances (4.4% of comments)
  • "👍🔥💕" - emoji-only - 156 instances (3.7% of comments)

Language Diversity: 34 languages detected (Authentic)
Benchmark: 25-45 languages for 45K followers

Conversation Depth Score: 71/100
Status: ✓ GOOD (Followers engaging with each other)

───────────────────────────────────────────────────────────────
👥 AUDIENCE DEMOGRAPHIC COHERENCE
───────────────────────────────────────────────────────────────
Gender Distribution:
  • Female: 84% | Benchmark: 82% | Status: ✓ ALIGNED
  • Male: 14% | Benchmark: 16% | Status: ✓ ALIGNED
  • Other: 2% | Benchmark: 2% | Status: ✓ ALIGNED

Age Distribution:
  • 18-24: 38% | Benchmark: 35% | Status: ✓ ALIGNED
  • 25-34: 41% | Benchmark: 44% | Status: ~ SLIGHT OFFSET
  • 35-44: 15% | Benchmark: 16% | Status: ✓ ALIGNED
  • 45+: 6% | Benchmark: 5% | Status: ✓ ALIGNED

Geographic Distribution (Top 10):
  • United States: 52% | Benchmark: 48% | Status: ✓ ALIGNED
  • United Kingdom: 8% | Benchmark: 7% | Status: ✓ ALIGNED
  • Canada: 6% | Benchmark: 5% | Status: ✓ ALIGNED
  • Australia: 5% | Benchmark: 6% | Status: ~ SLIGHT OFFSET
  • [+6 more countries]

Interest Alignment Score: 85/100
Status: ✓ STRONG (Followers interested in fashion, beauty, lifestyle)

───────────────────────────────────────────────────────────────
📋 INDUSTRY BENCHMARK COMPARISON
───────────────────────────────────────────────────────────────
Vertical: Fashion & Beauty
Follower Tier: 40K-50K
Database Size: 8,472 creators

Metric                          | Creator  | Benchmark | Percentile
Bot Follower %                  | 23%      | 4.2%      | 8th
Engagement Rate                 | 4.2%     | 5.8%      | 32nd
Comment Authenticity            | 80%      | 84%       | 38th
Audience Coherence Score        | 85/100   | 88/100    | 42nd
Growth Velocity (30-day)        | 2.1%     | 1.8%      | 72nd

⚠️ RISK ASSESSMENT: Creator is in the BOTTOM QUARTILE for bot followers 
and comment authenticity in the fashion vertical. Recommend 20-25% budget 
reduction or enhanced performance guarantees.

───────────────────────────────────────────────────────────────
🚨 RISK FLAGS
───────────────────────────────────────────────────────────────
[YELLOW] 23% bot followers (Threshold: 15%)
[YELLOW] 27% below benchmark engagement rate
[YELLOW] Elevated like-to-comment ratio (28:1 vs 18:1 benchmark)
[YELLOW] Engagement inconsistency in Dec (-35% dip)
[YELLOW] 4% spam/bot-identified comments
[GREEN] Audience demographics well-aligned
[GREEN] Natural engagement decay pattern
[GREEN] Strong conversion of followers to commenters

───────────────────────────────────────────────────────────────
💰 ROI NEGOTIATION LEVERAGE
───────────────────────────────────────────────────────────────
Original Offer: $15,000 partnership
Authentic Follower Reach: 36,378 followers (vs claimed 47,230)
Authentic Reach Loss: -23%

Recommended Adjustments:
  • Budget Reduction: -20% to -25% ($12,000 - $12,750)
  • OR Performance Guarantee: Minimum 3% engagement rate on content
  • OR Extended Campaign: Add 2 weeks content production for same fee

Risk-Adjusted CPM: $0.38 per follower
(Standard micro-influencer