---
name: linkedin-engagement-lead-scoring-dm-sequence-trigger
description: "Analyze LinkedIn engagement signals (comments, shares, profile views) and auto-trigger personalized DM sequences based on buying intent scoring. Use when the user needs lead qualification, sales outreach automation, or engagement-to-revenue conversion optimization."
version: 1.0.0
homepage: https://github.com/ncreighton/empire-skills
metadata:
  {
    "openclaw": {
      "requires": {
        "env": [
          "LINKEDIN_API_KEY",
          "LINKEDIN_COMPANY_URN",
          "OPENAI_API_KEY",
          "SLACK_WEBHOOK_URL",
          "GOOGLE_SHEETS_API_KEY"
        ],
        "bins": ["python3", "node"]
      },
      "os": ["macos", "linux", "win32"],
      "files": ["SKILL.md"],
      "emoji": "🎯"
    }
  }
---

## Overview

**LinkedIn Engagement → Lead Scoring & DM Sequence Trigger** transforms raw LinkedIn engagement data into actionable, revenue-ready leads. This skill automatically monitors who engages with your content (comments, shares, reposts, profile views), scores them by buying intent signals (job title changes, seniority level, industry, engagement velocity), and triggers hyper-personalized multi-touch DM sequences.

**Why This Matters:**
- **80% of B2B deals** begin with engagement, not cold outreach
- Most teams lose track of **valuable engagers** after they interact once
- Manual follow-up is inconsistent, missing the 24-48 hour intent window
- Personalization at scale drives **5-7x higher response rates**

**Integrations & Connections:**
- **LinkedIn API** (engagement data, profile intelligence)
- **OpenAI** (intent scoring, message personalization via GPT-4)
- **Google Sheets** (lead pipeline tracking, analytics)
- **Slack** (real-time notifications, HQ alerts)
- **Typeform/HubSpot** (CRM sync, deal stage updates)
- **Zapier/Make** (webhook triggers, workflow orchestration)

---

## Quick Start

Try these prompts immediately:

```
1. "Score all LinkedIn post engagers from last 7 days and show me top 20 by buying intent. Segment by: job title, company size, engagement type."

2. "Generate 3 personalized DM sequences for: (a) C-suite comment engagers, (b) job title change signals, (c) repeat engagers from competitor companies."

3. "Analyze response rates from our last DM campaign. Which sequences converted best? What's the average response time and engagement velocity?"

4. "Set up automated DM trigger: When someone comments on posts with 'pricing' or 'ROI' keywords, send them our Case Study sequence within 2 hours."

5. "Create a LinkedIn engagement dashboard: engagement type breakdown, scoring distribution, DM response funnel, and conversion-to-opportunity rate."
```

---

## Capabilities

### 1. **Engagement Data Collection & Normalization**
- Polls LinkedIn API for real-time engagement on your posts (native content, reposts, shared articles)
- Captures: commenter profile URN, comment text, timestamp, engagement type (comment/share/repost/view)
- Fetches enriched profile data: current role, company, seniority level, industry, location, years at company
- Deduplicates repeat engagers and tracks engagement frequency per person
- **Usage:** Automatically ingest all engagers daily at 6 AM UTC

### 2. **AI-Powered Buying Intent Scoring**
- **Proprietary scoring model** combines 12+ signals:
  - **Primary Signals:** Job title (VP/C-suite = +25pts), company size (500-5K = +20pts), industry match (+15pts)
  - **Behavioral Signals:** Comment sentiment (positive/problem-seeking = +10pts), engagement velocity (3+ interactions in 7 days = +15pts), keyword triggers ("budget," "pain point," "struggling" = +20pts)
  - **Temporal Signals:** Recent job change (< 30 days = +20pts), promotion/role change detection (+15pts), profile activity in last 24hrs (+5pts)
- Outputs **0-100 intent score** + confidence level (high/medium/low)
- Flags **high-intent hot leads** (score 75+) for immediate action
- **Usage:** "Show me all engagers scored 70+ with confidence=HIGH from SaaS companies"

### 3. **Multi-Sequence DM Automation**
- **Pre-built sequences:**
  - **Value-First Sequence** (3 messages, 48-96 hrs apart): Insight share → relevant case study → soft CTA
  - **Problem-Aware Sequence** (4 messages): Empathy → solution overview → customer proof → calendar link
  - **Competitor-to-Customer Sequence** (5 messages): Industry insight → competitive advantage → deeper discovery → demo offer → final follow-up
  - **Thought-Leader Sequence** (3 messages): Personalized compliment → exclusive content → collaboration idea
- **AI Personalization:**
  - Dynamically inserts first name, company, job title, recent activity
  - Adapts tone based on seniority (formal for C-suite, conversational for mid-market)
  - References specific comment or post engagement: "I saw your comment on retention—that's a pain point we solve..."
- **Smart Timing:** Sends based on recipient's typical LinkedIn activity hours
- **Usage:** "Trigger the 'Problem-Aware' sequence for all comment engagers scored 65+ in Tech industry. Personalize with their specific comment text."

### 4. **Conditional Trigger Rules**
- Create if/then rules without code:
  - IF engagement_type = "comment" + intent_score >= 70 + job_title includes "VP" → THEN send Value-First Sequence immediately
  - IF company_size = "1000+" + industry = "SaaS" + engagement_velocity >= 3 → THEN add to "hot leads" Slack channel
  - IF job_change_detected = true + days_at_company < 30 → THEN send Thought-Leader Sequence (higher career fluidity = more openness)
  - IF keyword_trigger = ["budget," "struggling," "improve"] + has_commented_before = true → THEN escalate to sales team
- **Unlimited custom rules** per account
- **Usage:** "Create trigger: anyone from my 'target account list' who engages = auto-send Case Study + calendar link within 1 hour"

### 5. **Response Tracking & Analytics**
- Monitors all sent DM sequences for: opens, replies, time-to-response, reply sentiment
- Segments response metrics by:
  - Sequence type (which DM template performs best?)
  - Intent score band (do high-intent leads reply faster?)
  - Industry, company size, seniority level
  - Engagement type (comment engagers vs. share engagers vs. profile viewers)
- Calculates: reply rate %, avg time-to-first-response, conversation-to-meeting conversion rate
- **Identifies winning sequences** and auto-suggests which to use for future leads
- **Usage:** "Which sequence had highest response rate in last 30 days? What's the correlation between intent score and reply time?"

### 6. **Pipeline Sync & CRM Integration**
- Auto-creates contacts in HubSpot/Salesforce when:
  - DM response received
  - Lead moves to "hot" threshold (intent_score 75+)
  - User manually marks as "sales-ready"
- Syncs to Google Sheets for real-time pipeline tracking
- Updates deal stage based on engagement depth (1st message → 3rd message = progression tracking)
- **Usage:** "Sync all hot leads to HubSpot 'Sales Qualified Lead' stage automatically when they reply to DM"

### 7. **Reporting & Dashboard**
- **Real-time dashboard metrics:**
  - Weekly engagement volume by type
  - Intent score distribution histogram
  - DM sequence performance (response %, conversion %)
  - Top industries/companies/job titles by engagement
  - Time-to-response funnel
  - Revenue-attributed leads (if connected to CRM)
- Scheduled weekly email reports with highlights
- One-click Slack notifications for hot leads
- **Usage:** "Send me a Slack message every time someone with intent_score 80+ engages with our posts"

---

## Configuration

### Required Environment Variables
```bash
LINKEDIN_API_KEY=your_linkedin_api_key_here
LINKEDIN_COMPANY_URN=urn:li:organization:12345678
OPENAI_API_KEY=sk-your-openai-key
SLACK_WEBHOOK_URL=https://hooks.slack.com/services/YOUR/WEBHOOK/URL
GOOGLE_SHEETS_API_KEY=your-google-sheets-api-key
HUBSPOT_API_KEY=your-hubspot-api-key (optional)
TIMEZONE=America/New_York (for scheduling)
```

### Setup Instructions

**Step 1: LinkedIn API Access**
- Go to [LinkedIn Developer Portal](https://www.linkedin.com/developers/)
- Create an app, request **Sign In with LinkedIn** + **Share on LinkedIn** permissions
- Request **Sales Navigator** or **LinkedIn Ads Analytics** API for engagement data
- Copy API key and Company URN to environment

**Step 2: Enable Slack Notifications**
- Create a Slack workspace
- Go to [Slack Apps](https://api.slack.com/apps) → Create New App
- Enable Incoming Webhooks, create one for your #sales channel
- Copy webhook URL to SLACK_WEBHOOK_URL env var

**Step 3: Connect Google Sheets**
- Create a Google Sheet for lead pipeline
- Enable Google Sheets API in Cloud Console
- Generate service account key, paste contents into GOOGLE_SHEETS_API_KEY
- Share sheet with service account email

**Step 4: Sync to CRM (Optional)**
- HubSpot: Generate private app token [here](https://app.hubspot.com/l/settings/apps), add to HUBSPOT_API_KEY
- Salesforce: Generate OAuth token, use standard Salesforce webhooks

**Step 5: Configure Scoring Rules**
```yaml
# Example config.yaml for custom scoring:
scoring_model:
  job_title_weights:
    C-level: 25
    VP: 20
    Director: 15
    Manager: 10
  company_size_weights:
    1000+: 20
    500-999: 18
    100-499: 15
  industry_match:
    - SaaS: +15
    - Financial Services: +15
    - Healthcare: +10
  keyword_triggers:
    - budget: +20
    - struggling: +20
    - pain point: +15
    - ROI: +10
```

---

## Example Outputs

### Example 1: Engagement Report
```json
{
  "period": "2024-01-15 to 2024-01-22",
  "total_engagers": 127,
  "breakdown": {
    "comments": 78,
    "shares": 31,
    "profile_views": 18
  },
  "top_10_leads": [
    {
      "rank": 1,
      "name": "Sarah Chen",
      "company": "Acme Corp",
      "job_title": "VP Sales",
      "intent_score": 92,
      "engagement_type": "comment",
      "engagement_text": "This is exactly the pain point we're solving for. Would love to learn more.",
      "recommended_sequence": "Problem-Aware Sequence",
      "urgency": "HOT - Reply within 24 hours"
    },
    {
      "rank": 2,
      "name": "Marcus Johnson",
      "company": "TechVenture Inc",
      "job_title": "Director of Operations",
      "intent_score": 87,
      "engagement_type": "comment",
      "recent_job_change": true,
      "days_at_company": 8,
      "recommended_sequence": "Thought-Leader Sequence",
      "urgency": "HOT - Career transition = high openness"
    }
  ],
  "intent_distribution": {
    "high_intent_75_plus": 23,
    "medium_intent_50_74": 56,
    "low_intent_below_50": 48
  }
}
```

### Example 2: Personalized DM Sequence (Auto-Generated)
```
Message 1 (Sent immediately):
"Hi Sarah, I saw your comment on our post about retention challenges—sounds like 
something you're actively thinking about at Acme. We've helped 40+ companies 
reduce churn by 30% in 90 days. Would love to share one specific case study 
with your ops team. Free 15-min call this week? [calendar link]"

Message 2 (Sent 48 hours later if no reply):
"No worries if you missed my last message. Thought you'd appreciate this metric: 
companies with your operational scale typically see $X0K annual revenue impact 
from better retention. Here's how → [case study]. Curious to chat?"

Message 3 (Sent 96 hours later if no reply):
"Last chance—I'm heading into a busy week. Would you prefer a brief call 
(15 min) or would a recorded walkthrough be better for your team? Let me know."
```

### Example 3: Weekly Performance Summary
```
WEEKLY DM PERFORMANCE (Jan 8-14, 2024)

📊 Sequences Sent: 64
✅ Replies Received: 19 (29.7% reply rate)
⏱️ Avg Time to First Reply: 4.2 hours
🎯 High-Intent Engagers Contacted: 42
💬 Conversations Moved to 3+ Messages: 8 (12.5%)
🤝 Meetings Booked from DMs: 3 (4.7%)

Top Performing Sequences:
1. Problem-Aware Sequence: 35% reply rate
2. Thought-Leader Sequence: 28% reply rate
3. Value-First Sequence: 25% reply rate

By Intent Score Band:
- 80-100: 38% reply rate (6/16)
- 70-79: 32% reply rate (8/25)
- 60-69: 22% reply rate (4/18)
- Below 60: 8% reply rate (1/12)

→ Insight: Higher intent scores = 4.75x better response rates
```

---

## Tips & Best Practices

### 1. **Master the 24-Hour Window**
- LinkedIn engagement intent peaks in the first 24 hours
- Set up **immediate DM triggers** (within 15-60 minutes) for hot leads
- Follow-up sequences work best at 48, 96, and 168 hours
- **Pro tip:** Send first message during recipient's typical LinkedIn active hours (AI calculates this automatically)

### 2. **Segment Your Sequences**
- Don't use the same DM for everyone
- **By Seniority:** C-suite gets formal, value-driven messaging; mid-market gets problem-focused; ICs get peer-to-peer tone
- **By Intent Score:** 80+ gets immediate calendar link; 65-79 gets soft education; Below 65 gets nurture-focused content
- **By Engagement Type:** Commenters are buyers (engage with your thinking); sharers are amplifiers (can be advocates); profile viewers are curious (early-stage)
- **Test and iterate:** Run 3-4 sequence variants per segment, measure reply rates, double down on winners

### 3. **Personalization = Reply Rate Multiplier**
- Generic messages get 8-12% reply rates
- Personalized to company get 18-22% reply rates
- Personalized to specific comment/engagement get 28-35% reply rates
- Always reference their exact comment or company challenge
- **Template example:** "I saw you mention [SPECIFIC QUOTE] on our post—we help teams solve that exact challenge..."

### 4. **Leverage Job Change Signals**
- People in first 60 days at new company are 7x more likely to evaluate new solutions
- Prioritize job_change_detected = true leads
- Send Thought-Leader sequences (non-salesy) to freshly promoted folks
- Use tone: "Congrats on the new role! Bet you're exploring new solutions for..."

### 5. **Build Intent Score Context**
- Don't rely solely on automated scores—add manual context
- Mark leads as "strategic" if they're from target accounts, regardless of score
- Note if they're in an active buying cycle (multiple engagements in 7 days)
- Track which industries/roles have highest lifetime value; weight their scores higher

###