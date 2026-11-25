---
name: ai-micro-saas-product-market-fit-validator
description: "Validate SaaS product-market fit by researching TAM, identifying 5-7 high-conversion micro-niches, and scoring demand signals from Reddit/Twitter/G2. Use when the user needs go-to-market strategy, niche validation, or founder research for new products."
version: 1.0.0
homepage: https://github.com/ncreighton/empire-skills
metadata:
  {
    "openclaw": {
      "requires": {
        "env": ["OPENAI_API_KEY", "SERPER_API_KEY", "REDDIT_CLIENT_ID", "REDDIT_CLIENT_SECRET", "TWITTER_BEARER_TOKEN"],
        "bins": []
      },
      "os": ["macos", "linux", "win32"],
      "files": ["SKILL.md"],
      "emoji": "🎯"
    }
  }
---

## Overview

The **AI Micro-SaaS Product-Market Fit Validator** is an autonomous research engine designed for indie hackers, bootstrapped founders, and product teams validating new SaaS ideas. Instead of spending weeks manually researching market demand, this skill:

- **Analyzes your product** against Total Addressable Market (TAM) frameworks
- **Identifies 5-7 micro-niches** ranked by conversion potential and willingness-to-pay
- **Validates demand signals** by scraping Reddit threads, Twitter conversations, and G2 reviews for pain point mentions
- **Scores each niche** on market readiness, competition intensity, and buyer sophistication
- **Generates a prioritized go-to-market roadmap** with specific messaging angles, customer acquisition channels, and pricing signals for each segment

This skill integrates with **Slack** (for async team notifications), **Notion** (for storing research artifacts), and **Google Sheets** (for collaborative scoring matrices). It's built on OpenAI's GPT-4 for synthesis, Serper API for web search, Reddit API for community validation, and Twitter API for trend analysis.

**Why this matters:** 90% of SaaS failures are due to targeting the wrong niche or misunderstanding buyer willingness-to-pay. This skill compresses months of founder research into 15 minutes of autonomous validation.

---

## Quick Start

### Example 1: Validate a Project Management Tool for Freelancers

```
I've built a lightweight project management tool focused on freelancers. 
It has time tracking, invoice generation, and client collaboration features. 
Help me identify the best micro-niches to target first and validate if there's 
real demand for this solution.

Product description:
- Name: TimeFlow
- Core features: Time tracking, invoice automation, client portals
- Target: Freelancers and small agencies
- Price point: $29-99/month
- Differentiation: Simpler than Monday.com, cheaper than Asana, built for solopreneurs
```

**What you'll get:** A ranked list of 6 niches (e.g., "UX designers managing multiple clients," "Virtual assistants tracking billable hours," "Freelance accountants needing compliance tracking"), demand validation scores, and messaging frameworks for each.

---

### Example 2: Validate a Content Creator Analytics Platform

```
I'm launching a content analytics tool specifically for creators on YouTube, TikTok, 
and Instagram. It provides AI-powered content recommendations, audience sentiment 
analysis, and competitor benchmarking. Can you validate if this solves real problems 
and which creator verticals would pay the most?

Product spec:
- Name: CreatorIQ
- Features: Multi-platform analytics, AI recommendations, sentiment tracking
- Target: Content creators (YouTubers, TikTokers, Instagrammers)
- Pricing: $49-199/month (tiered by follower count)
- MVP launch: 60 days
```

**What you'll get:** Niche rankings (e.g., "Finance educators," "Fitness coaches," "Beauty/lifestyle creators"), willingness-to-pay signals from YouTube comments and Twitter threads, and a 90-day GTM roadmap with specific acquisition channels per niche.

---

### Example 3: Validate a B2B HR Compliance Tool

```
We've built an AI-powered HR compliance assistant that helps small businesses 
(10-100 employees) stay compliant with labor laws, generate compliant offer letters, 
and automate leave tracking. The market is dominated by big players (Workday, 
BambooHR). Where should we focus first?

Product details:
- Name: ComplianceBot
- Features: AI offer letter generation, leave tracking, compliance alerts
- Target: SMBs, 10-100 employees
- Price point: $199-499/month
- Competitive advantage: 10x cheaper than incumbents, AI-native
```

**What you'll get:** High-potential niches (e.g., "Tech startups in Series A-B," "Healthcare clinics," "Professional services firms"), demand validation from HR subreddits and Twitter HR community, and messaging that resonates with each segment.

---

## Capabilities

### 1. **TAM & Market Sizing Analysis**
The skill estimates Total Addressable Market for your product category using:
- Industry reports (via Serper API)
- LinkedIn employment data for target roles
- SaaS benchmarking databases (Capterra, G2, Stackshare)
- Historical funding data for comparable products

**Usage:** Provides realistic TAM estimates to help you understand market ceiling and identify underserved segments.

---

### 2. **Micro-Niche Identification Engine**
Autonomously generates 5-7 hyper-specific customer segments using:
- **Firmographic analysis** (company size, industry, geography)
- **Psychographic profiling** (pain points, buying behavior, tech adoption)
- **Behavioral signals** (search volume, community mentions, content consumption)
- **Competitive mapping** (existing solutions, willingness to switch)

**Example output:**
```
NICHE #1: UX/UI Designers at Design Agencies (50-200 people)
- Willingness to Pay Score: 8.2/10
- Market Readiness: High (early adopters)
- Estimated TAM: $245M
- Primary Pain: Time tracking across multiple client projects
- Messaging Angle: "Billable hours that don't require spreadsheets"

NICHE #2: Freelance Accountants (Solo + Small Teams)
- Willingness to Pay Score: 7.9/10
- Market Readiness: Medium (pragmatists)
- Estimated TAM: $187M
- Primary Pain: Invoice reconciliation and tax tracking
- Messaging Angle: "Compliance-first invoicing for tax season"
```

---

### 3. **Demand Validation via Reddit/Twitter/G2**
Scrapes and analyzes community discussions to find:
- **Reddit:** Pain point mentions in relevant subreddits (r/freelance, r/smallbusiness, industry-specific communities)
- **Twitter:** Sentiment analysis and influencer conversations about the problem space
- **G2 Reviews:** Competitor reviews highlighting unmet needs and feature gaps
- **Search Trends:** Google Trends data showing growing/declining interest in the problem

**Output includes:**
- Exact quotes from users mentioning the pain point
- Sentiment score (positive/negative/neutral)
- Influencer mentions and follower reach
- Competitor review gaps (features users are asking for)

---

### 4. **Willingness-to-Pay Scoring**
For each niche, the skill analyzes:
- **Current spending patterns** (via G2 pricing data, Capterra reviews)
- **Budget allocation** (what % of revenue do companies spend on this category?)
- **Switching costs** (how hard is it to move from competitors?)
- **Price sensitivity** (based on company size, industry margins)
- **Urgency signals** (how painful is the problem?)

**Scoring formula:**
```
WTP Score = (0.25 × Budget Allocation) + (0.25 × Switching Costs) 
          + (0.25 × Urgency Signals) + (0.15 × Competitive Intensity) 
          + (0.10 × Tech Adoption Rate)
```

---

### 5. **Prioritized Go-to-Market Roadmap**
Generates a 90-day GTM plan with:
- **Phase 1 (Weeks 1-4):** Target niche #1, messaging, and acquisition channels
- **Phase 2 (Weeks 5-8):** Launch to niche #2, refine positioning
- **Phase 3 (Weeks 9-12):** Expand to niche #3, scale winning channels

For each phase:
- **Customer acquisition channels** (specific subreddits, Twitter communities, LinkedIn groups, Slack communities)
- **Messaging templates** (subject lines, positioning statements, value props)
- **Success metrics** (conversion targets, CAC targets, retention benchmarks)
- **Competitive positioning** (how to differentiate from incumbents)

---

### 6. **Integration Outputs**
The skill exports findings to:
- **Slack:** Async notifications with niche rankings and top quotes
- **Google Sheets:** Collaborative scoring matrix for team discussion
- **Notion:** Full research report with all demand signals
- **GitHub:** JSON export for version control and CI/CD pipelines

---

## Configuration

### Required Environment Variables

```bash
# OpenAI API (for GPT-4 synthesis)
export OPENAI_API_KEY="sk-..."

# Serper API (for web search and industry reports)
export SERPER_API_KEY="..."

# Reddit API (for community validation)
export REDDIT_CLIENT_ID="..."
export REDDIT_CLIENT_SECRET="..."

# Twitter API v2 (for trend analysis)
export TWITTER_BEARER_TOKEN="..."

# Optional: For Slack notifications
export SLACK_WEBHOOK_URL="https://hooks.slack.com/services/..."

# Optional: For Google Sheets export
export GOOGLE_SHEETS_API_KEY="..."
```

### Setup Instructions

1. **Get OpenAI API key** → https://platform.openai.com/api-keys
2. **Get Serper API key** → https://serper.dev (free tier: 100 searches/month)
3. **Create Reddit app** → https://www.reddit.com/prefs/apps (read-only)
4. **Create Twitter app** → https://developer.twitter.com/en/dashboard (API v2 access)
5. **Optional Slack integration** → Create incoming webhook in your workspace
6. **Optional Google Sheets** → Enable Sheets API and create service account

### Configuration Options

```yaml
research_depth: "comprehensive"  # or "quick" (15 min vs 45 min)
niche_count: 7                   # number of micro-niches to identify
min_demand_threshold: 0.6        # only include niches with >60% confidence
include_competitor_analysis: true
export_format: ["slack", "sheets", "notion", "json"]
```

---

## Example Outputs

### Sample Research Report: TimeFlow (Project Management for Freelancers)

```
EXECUTIVE SUMMARY
Product: TimeFlow (Time tracking + invoicing for freelancers)
Research Date: 2024-01-15
Confidence Score: 8.7/10
Recommendation: Launch to Niche #1 (UX/UI Designers) in Week 1

---

NICHE RANKINGS

🥇 NICHE #1: UX/UI Designers at Agencies (50-200 employees)
├─ Willingness to Pay: 8.2/10
├─ Market Size: $245M TAM
├─ Competition: Medium (Monday.com, Asana, Harvest)
├─ Demand Signals: 347 Reddit mentions, 89 Twitter conversations, 23 G2 feature requests
├─ Key Quote: "I spend 3 hours/week manually tracking billable hours across 5 clients" 
│  (r/Design, 156 upvotes)
├─ Messaging Angle: "Billable hours that don't require spreadsheets"
└─ GTM Channel: Designer-focused Slack communities, Design Twitter, ADPList mentors

🥈 NICHE #2: Freelance Accountants (Solo + Small Teams)
├─ Willingness to Pay: 7.9/10
├─ Market Size: $187M TAM
├─ Competition: High (QuickBooks, FreshBooks, Wave)
├─ Demand Signals: 412 Reddit mentions, 67 Twitter conversations, 45 G2 feature requests
├─ Key Quote: "Tax season is a nightmare because I can't reconcile invoices with tax codes"
│  (r/Accounting, 203 upvotes)
├─ Messaging Angle: "Invoice tracking built for tax compliance"
└─ GTM Channel: Accounting subreddits, CPA Twitter, LinkedIn accountant groups

🥉 NICHE #3: Virtual Assistants (Solo + Small Teams)
├─ Willingness to Pay: 7.1/10
├─ Market Size: $156M TAM
├─ Competition: High (Toggl, Clockify, Everhour)
├─ Demand Signals: 289 Reddit mentions, 54 Twitter conversations, 34 G2 feature requests
├─ Key Quote: "Managing time across 10+ clients is impossible without a system"
│  (r/VirtualAssistant, 128 upvotes)
├─ Messaging Angle: "Multi-client time tracking for VAs"
└─ GTM Channel: VA Facebook groups, Upwork forums, LinkedIn VA community

NICHE #4: Freelance Developers
├─ Willingness to Pay: 7.8/10
├─ Market Size: $312M TAM (largest)
├─ Competition: VERY HIGH (Toggl, Clockify, Harvest, Everhour all dominate)
├─ Demand Signals: 1,247 Reddit mentions, 234 Twitter conversations
├─ Recommendation: DEPRIORITIZE (too much competition, lower switching costs)

NICHE #5: Copywriters & Content Creators
├─ Willingness to Pay: 6.9/10
├─ Market Size: $98M TAM
├─ Competition: Low (underserved)
├─ Demand Signals: 156 Reddit mentions, 31 Twitter conversations
├─ Key Quote: "I need to track billable hours but most tools are bloated"
│  (r/Copywriting, 87 upvotes)
├─ Messaging Angle: "Simple time tracking for creative freelancers"
└─ GTM Channel: Copywriter Twitter, r/Copywriting, writing newsletters

NICHE #6: Freelance Consultants (Business/Strategy)
├─ Willingness to Pay: 8.4/10 (HIGHEST)
├─ Market Size: $201M TAM
├─ Competition: Medium (Harvest, Toggl, FreshBooks)
├─ Demand Signals: 198 Reddit mentions, 112 Twitter conversations
├─ Key Quote: "We bill by the hour and need bulletproof time tracking for client invoicing"
│  (r/Consulting, 167 upvotes)
├─ Messaging Angle: "Time tracking for consultants who bill by the hour"
└─ GTM Channel: Consulting Slack communities, LinkedIn consultants, industry associations

NICHE #7: Freelance Designers (Non-Agency)
├─ Willingness to Pay: 7.3/10
├─ Market Size: $134M TAM
├─ Competition: High
├─ Demand Signals: 267 Reddit mentions, 78 Twitter conversations
└─ Recommendation: SECONDARY (similar to Niche #1 but less concentrated)

---

90-DAY GO-TO-MARKET ROADMAP

PHASE 1 (Weeks 1-4): Launch to UX/UI Designers
├─ Primary Channel: Designer Slack communities (ADPList, Designer Hangout, UXPA)
├─ Secondary Channels: Design Twitter (design_systems, UX_UI_Designers hashtags)
├─ Messaging: "Billable hours that don't require spreadsheets"
├─ Offer: Free tier for first 100 users + lifetime discount for early adopters
├─ Success Metrics:
│  ├─ 50 signups (target CAC: $50)
│  ├─ 20% activation rate (10 paying customers)
│  └─ $290/MRR (at $29/month)
└─ Competitive Positioning: "Asana for time tracking, not project management"

PHASE 2 (Weeks 5-8): Expand to Freelance Accountants
├─ Primary Channel: r/Accounting, r/Freelance, Accounting subredd