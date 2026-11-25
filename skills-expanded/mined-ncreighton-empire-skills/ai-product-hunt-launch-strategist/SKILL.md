---
name: ai-product-hunt-launch-strategist
description: "Optimize Product Hunt launches with AI-powered tagline generation, competitor analysis, and engagement playbooks. Use when the user needs launch strategy, copy optimization, or hunter outreach for maximum upvotes and visibility."
version: 1.0.0
homepage: https://github.com/ncreighton/empire-skills
metadata:
  {"openclaw":{"requires":{"env":["OPENAI_API_KEY","PRODUCT_HUNT_API_KEY"],"bins":["curl","jq"]},"os":["macos","linux","win32"],"files":["SKILL.md"],"emoji":"🚀"}}
---

# AI Product Hunt Launch Strategist & Copy Optimizer

## Overview

The **AI Product Hunt Launch Strategist** automates the entire launch preparation process for Product Hunt submissions. This skill analyzes trending launches, competitor positioning, and historical performance data to generate data-driven strategies that maximize upvotes, visibility, and hunter interest.

### Why This Matters

Product Hunt launches are time-sensitive events where the first 24 hours determine success. Manual research and copy iteration consume weeks. This skill compresses that timeline into hours by:

- **Analyzing top-performing launches** in your category (last 30/60/90 days)
- **Generating 5-10 optimized taglines** with A/B testing recommendations
- **Creating hunter outreach templates** personalized for influential hunters
- **Building engagement playbooks** with post-launch timing strategies
- **Identifying optimal launch windows** based on category saturation
- **Suggesting category positioning** for maximum discoverability

### Integrations & Tools

- **Product Hunt API** — Real-time launch data, hunter profiles, upvote trends
- **OpenAI GPT-4** — Copy generation, competitor analysis, strategy synthesis
- **Google Trends API** — Category momentum and seasonal patterns
- **Slack** — Launch reminders, milestone notifications, team collaboration
- **Airtable** — Store competitive intelligence, tagline variants, hunter databases
- **Notion** — Organize launch playbooks and team workflows

---

## Quick Start

### Example 1: Analyze a Competitor Launch & Generate Taglines

```
I'm launching a new AI writing assistant for technical documentation. 
Analyze the top 5 Product Hunt launches in the "Writing Tools" category 
from the last 60 days. Generate 8 tagline variations optimized for 
upvotes, and tell me which category positioning would work best.
```

**What the skill does:**
- Fetches top launches via Product Hunt API
- Extracts taglines, descriptions, and engagement metrics
- Uses GPT-4 to identify patterns in high-performing copy
- Generates original taglines following those patterns
- Recommends category (e.g., "Writing Tools" vs "Developer Tools")

---

### Example 2: Create a Hunter Outreach Strategy

```
I'm launching tomorrow. Create personalized outreach templates for 
the top 15 hunters who support writing tools and AI products. Include 
their past launches, why they'd care about my product, and the best 
time to reach them based on their activity patterns.
```

**What the skill does:**
- Identifies top hunters by upvote influence and category relevance
- Analyzes their past supported launches for tone/style matching
- Generates 3-5 personalized outreach message variants
- Suggests optimal send times (timezone-aware)
- Provides Slack integration for team notifications

---

### Example 3: Build a Launch Day Engagement Playbook

```
Create a detailed launch day playbook for my product. Include: 
(1) optimal post timing for comments, (2) response templates for 
common questions, (3) milestone celebration triggers (100 upvotes, 
top 5 in category, etc.), and (4) contingency tactics if we're 
underperforming at 12 hours.
```

**What the skill does:**
- Analyzes successful launch timelines from Product Hunt data
- Generates templated responses for common questions/objections
- Creates milestone-based action triggers
- Provides contingency strategies (e.g., hunter escalation, media outreach)
- Exports as Notion/Airtable for team coordination

---

## Capabilities

### 1. Competitive Intelligence & Trend Analysis

**Analyze Top Launches in Your Category**
- Fetch top 10-20 launches from the last 30/60/90 days
- Extract: tagline, description, category, upvotes, maker engagement rate
- Identify common themes, keywords, and positioning patterns
- Calculate average upvotes by category and day-of-week
- Provide trend analysis: emerging categories, declining interest

**Example Output:**
```
CATEGORY: Writing Tools (Last 60 Days)
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
Top Tagline Patterns:
  • "X for Y" (40% of top 10) → "Grammarly for code documentation"
  • Problem-first (35%) → "Stop writing boring API docs"
  • Speed/efficiency (25%) → "Write docs 5x faster"

Avg Upvotes by Launch Day:
  Mon-Wed: 2,100 | Thu-Fri: 2,850 | Sat-Sun: 1,200

Emerging Trends:
  ✓ AI-powered personalization (9/10 top launches)
  ✓ Multi-language support (7/10)
  ✗ Generic "productivity" framing (declining engagement)
```

### 2. Tagline & Copy Generation

**AI-Powered Tagline Variants**
- Generate 8-12 tagline options across multiple positioning angles
- Each tagline optimized for: clarity, memorability, SEO keywords, emotional resonance
- Provide A/B testing recommendations (which to test first, sample sizes)
- Include variant explanations (why this positioning works)

**Example Output:**
```
TAGLINE VARIANTS (Ranked by Predicted Performance)
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

1. 🥇 "ChatGPT for your codebase — instant docs, zero effort"
   └─ Positioning: Speed + AI comparison (high-intent keywords)
   └─ A/B Test vs #2 (recommend 500 impressions minimum)

2. 🥈 "Write API documentation 10x faster with AI"
   └─ Positioning: Quantified benefit (CTR optimization)
   └─ Best for: Technical audience segments

3. 🥉 "Stop drowning in documentation — AI writes it for you"
   └─ Positioning: Pain-first (emotional hook)
   └─ Best for: Overworked engineering teams
```

### 3. Hunter Outreach & Relationship Mapping

**Identify & Personalize Hunter Outreach**
- Rank hunters by: influence (followers), category relevance, past support patterns
- Analyze their recent activity, timezone, preferred communication style
- Generate personalized outreach templates (3-5 variants)
- Suggest optimal send times and follow-up sequences
- Track outreach status via Airtable integration

**Example Output:**
```
TOP HUNTER: Sarah Chen (@sarahchen)
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
Influence Score: 9.2/10 (4,200 followers)
Relevance: 8.8/10 (supported 12 writing tools, 8 AI products)
Timezone: PST (UTC-8)
Activity Pattern: Most active 8-10 AM PST, 6-8 PM PST

Recent Supported Launches:
  • Notion AI (featured in comments)
  • Copysmith (early supporter)
  • Jasper (multiple upvotes)

PERSONALIZED OUTREACH TEMPLATE A:
─────────────────────────────────────
Hi Sarah,

I noticed you've been championing AI writing tools (loved your 
support for Copysmith). We just built [Product] — it does for 
technical docs what Jasper did for marketing copy.

Would love your early feedback. Happy to give you a beta key.

Best,
[Your Name]

SEND TIME RECOMMENDATION: Tomorrow 8:30 AM PST
```

### 4. Launch Window Optimization

**Identify Ideal Launch Timing**
- Analyze category saturation by day-of-week and time-of-day
- Compare your product strength against competing launches
- Recommend optimal launch window (day + time)
- Provide contingency windows if primary slot is unavailable
- Factor in global timezone distribution of your target audience

**Example Output:**
```
LAUNCH WINDOW ANALYSIS
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
RECOMMENDED: Wednesday, 12:01 AM PT
  └─ Reasoning: Low competition (avg 1,200 concurrent launches)
  └─ Category strength: Writing Tools peaks Wed-Thu
  └─ Audience overlap: 85% of target hunters active by 8 AM PT

ALTERNATIVE: Tuesday, 12:01 AM PT
  └─ Competitive: 1,400 launches (moderate)
  └─ Advantage: Earlier feedback loop (full 24h in peak hours)

AVOID: Saturday, Sunday (avg 800 launches, 40% lower engagement)
```

### 5. Launch Day Engagement Playbook

**Automated Playbook Generation**
- Hour-by-hour timeline for first 24 hours
- Templated responses for common questions/objections
- Milestone-based action triggers (hit 100 upvotes? → escalate to hunters)
- Contingency tactics for underperformance
- Celebration/momentum-building strategies

**Example Output:**
```
LAUNCH DAY PLAYBOOK
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

HOUR 1-4: MOMENTUM BUILDING
├─ 12:15 AM: Post launch announcement in Slack/Discord
├─ 1:00 AM: First response wave (thank early supporters)
├─ 2:00 AM: Engage with comments (answer technical questions)
└─ 4:00 AM: Reach out to 5 "warm" hunters (pre-briefed)

HOUR 5-12: ENGAGEMENT MAINTENANCE
├─ 8:00 AM: Morning check-in (respond to overnight comments)
├─ 10:00 AM: [TRIGGER] If < 50 upvotes: escalate to 10 hunters
├─ 12:00 PM: Lunch momentum post (behind-the-scenes content)
└─ 3:00 PM: Respond to "comparison" questions (vs competitors)

HOUR 13-24: SUSTAINED ENGAGEMENT
├─ 6:00 PM: Evening engagement push (respond to all comments)
├─ 8:00 PM: [TRIGGER] If top 10 in category: media outreach
├─ 10:00 PM: Final push with user testimonials/social proof
└─ 11:00 PM: Thank all hunters + request final upvotes

RESPONSE TEMPLATES (Auto-generated):
─────────────────────────────────────
Q: "How is this different from [Competitor]?"
A: "[Competitor] is great for X. We focused on Y because our 
users told us that was their biggest pain point. Here's a 
detailed comparison: [link]"

Q: "What's your pricing?"
A: "We're offering early access at 50% off ($X/month). Full 
pricing details: [link]. Happy to answer specific questions!"
```

---

## Configuration

### Required Environment Variables

```bash
# Product Hunt API (get at producthunt.com/api)
export PRODUCT_HUNT_API_KEY="your_api_key_here"

# OpenAI GPT-4 for copy generation
export OPENAI_API_KEY="sk-..."

# Optional: Google Trends for category momentum
export GOOGLE_TRENDS_API_KEY="your_key_here"

# Optional: Airtable for competitive database storage
export AIRTABLE_API_KEY="your_key_here"
export AIRTABLE_BASE_ID="appXXXXXX"
```

### Setup Instructions

**1. Authenticate Product Hunt API**
```bash
curl -H "Authorization: Bearer $PRODUCT_HUNT_API_KEY" \
  https://api.producthunt.com/v2/me
```

**2. Create Airtable Base (Optional)**
- Create a table: `Launches` (columns: tagline, description, category, upvotes, date)
- Create a table: `Hunters` (columns: name, followers, category_focus, activity_pattern)
- Create a table: `Outreach` (columns: hunter_name, status, send_time, response)

**3. Enable Slack Integration (Optional)**
- Create Slack webhook: https://api.slack.com/messaging/webhooks
- Export webhook URL as `SLACK_WEBHOOK_URL`

---

## Example Outputs

### Output 1: Competitive Analysis Report

```
PRODUCT HUNT COMPETITIVE ANALYSIS
Generated: 2024-01-15 | Category: Writing Tools | Timeframe: Last 60 Days

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

TOP 5 LAUNCHES (by upvotes):
1. Notion AI (2,847 upvotes) - "AI-powered notes and docs"
2. Copysmith Pro (2,156 upvotes) - "AI copywriting for marketing teams"
3. Grammarly Premium (1,923 upvotes) - "Write with confidence"
4. Jasper Everywhere (1,834 upvotes) - "Your AI marketing copilot"
5. Copy.ai Teams (1,712 upvotes) - "AI writing for your whole team"

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

KEY INSIGHTS:
✓ "AI-powered" appears in 9/10 top taglines (high SEO value)
✓ Team/collaboration features in 7/10 (strong differentiator)
✓ Average comment count: 287 (high engagement category)
✓ Best day to launch: Wednesday (avg 2,400 upvotes vs 1,800 weekend)
✓ Maker response rate correlates with final rank (r=0.82)

POSITIONING GAPS IDENTIFIED:
⚠ No launches focused on "technical documentation" (underserved niche)
⚠ Limited "industry-specific" positioning (generic "writing" framing)
⚠ Opportunity: "AI for [specific use case]" positioning

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
```

### Output 2: Hunter Outreach Campaign

```
HUNTER OUTREACH CAMPAIGN
Product: TechDocs AI | Target: 20 Hunters | Estimated Reach: 47,000 followers

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

TIER 1: MEGA-INFLUENCERS (>5K followers)
─────────────────────────────────────────
1. Ryan Hoover (@rrhoover) - Product Hunt Founder
   Influence: 9.9/10 | Relevance: 8.2/10
   Best Time: Thu 10 AM PT
   Message: [Personalized, emphasizes innovation angle]

2. Sarah Chen (@sarahchen) - AI Tools Expert
   Influence: 9.2/10 | Relevance: 9.7/10
   Best Time: Wed 8 AM PT
   Message: