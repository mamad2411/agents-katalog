---
name: ai-niche-newsletter-editorial-calendar-and-subscriber-segment-matcher
description: "Generate optimized editorial calendars and segment-specific content strategies from subscriber engagement data. Use when the user needs newsletter planning, churn prevention, or audience-targeted send time optimization."
version: 1.0.0
homepage: https://github.com/ncreighton/empire-skills
metadata:
  {"openclaw":{"requires":{"env":["MAILCHIMP_API_KEY","CONVERTKIT_API_KEY","GOOGLE_ANALYTICS_API_KEY"],"bins":["python3","jq"]},"os":["macos","linux","win32"],"files":["SKILL.md"],"emoji":"📧"}}
---

## Overview

The **AI Niche Newsletter Editorial Calendar & Subscriber Segment Matcher** is a production-ready content strategy automation tool that transforms raw subscriber engagement data into actionable editorial calendars and segment-specific content recommendations.

This skill analyzes:
- **Engagement metrics** — open rates, click-through rates, time-zone patterns, device preferences
- **Newsletter archives** — historical content performance, topic clustering, subject line effectiveness
- **Subscriber cohorts** — micro-segmentation by behavior, interests, lifecycle stage, churn risk
- **Competitive gaps** — trending topics in your niche vs. your current content mix

The skill then generates:
1. **12-week editorial calendars** with recommended topics, send times, and content angles
2. **Segment-specific send strategies** — optimal times for each timezone/behavior cohort
3. **Subject line templates** — A/B testing recommendations based on historical winners
4. **Churn prevention playbooks** — re-engagement content hooks for at-risk subscribers

**Integrations:** Mailchimp, ConvertKit, Substack, Google Analytics, Slack (for calendar delivery)

---

## Quick Start

### Example 1: Generate a 12-Week Editorial Calendar from Engagement Data

```
Analyze my Mailchimp subscriber list and generate a 12-week editorial calendar.

Include:
- Top 5 content topics that drive opens and clicks for my audience
- Recommended send days and times for each segment
- Subject line A/B test recommendations
- Content angles that match my niche (SaaS product management)

Output format: CSV with columns [Week, Topic, Send_Day, Send_Time, Subject_Line_A, Subject_Line_B]
```

### Example 2: Identify Churn Risk Segments and Create Re-engagement Content

```
Analyze my ConvertKit subscriber engagement for the last 90 days.

Identify:
- Subscribers who haven't opened an email in 30+ days (churn risk)
- Their original signup source and interests
- Topics they engaged with in the first 2 weeks

Recommend 5 re-engagement email hooks specific to each risk cohort.
Output: JSON with subscriber_segment, churn_risk_score, recommended_topics, hook_subject_lines
```

### Example 3: Optimize Send Times by Timezone and Behavior

```
Analyze my subscriber list across time zones and create a send schedule.

For each segment (by timezone + device + engagement level):
- Calculate optimal send time (highest historical open rate)
- Recommend sending 2x per week vs. 1x per week based on engagement
- Suggest content cadence that matches their behavior pattern

Output: Segment-specific send calendar for next 4 weeks
```

---

## Capabilities

### 1. **Subscriber Segmentation Engine**
Automatically clusters subscribers into micro-segments based on:
- Geographic location (timezone, country)
- Engagement behavior (openers, clickers, inactive)
- Content preferences (inferred from click patterns)
- Lifecycle stage (new, active, at-risk, dormant)
- Device type (mobile-first, desktop, app)

**Usage:** `segment my subscribers by engagement level and timezone, then show me the 5 largest cohorts`

### 2. **Editorial Calendar Generator**
Produces 4-week, 12-week, or 26-week content calendars with:
- Topic recommendations ranked by engagement potential
- Optimal send day/time for each segment
- Content format suggestions (long-form, short-form, educational, promotional)
- Seasonal trend analysis
- Competitor gap analysis (what topics your niche discusses but you don't)

**Usage:** `generate a 12-week editorial calendar optimized for my tech newsletter audience, with topic diversity and send time optimization`

### 3. **Subject Line Optimization**
Analyzes historical subject line performance and recommends:
- Power words that drive opens in your niche
- Optimal subject line length (typically 40-50 characters)
- A/B test recommendations with predicted winner
- Emoji usage patterns that improve clicks
- Personalization opportunities (first name, segment-specific)

**Usage:** `analyze my top 50 highest-performing emails and extract subject line patterns, then generate 10 new subject lines for a "productivity tips" email`

### 4. **Churn Risk Detection & Prevention**
Identifies at-risk subscribers using:
- Engagement decline velocity (recent drop in opens/clicks)
- Time-since-last-engagement threshold
- Unsubscribe/complaint rate by segment
- Inactivity patterns (e.g., opens but never clicks)

Recommends re-engagement content hooks tailored to their interests.

**Usage:** `identify my top 100 churn-risk subscribers, show me what they engaged with initially, and recommend 3 re-engagement email hooks for each cohort`

### 5. **Send Time Optimization by Segment**
Calculates statistically significant optimal send times for:
- Each timezone independently
- Mobile vs. desktop audiences
- High-engagement vs. low-engagement subscribers
- Day-of-week preferences

**Usage:** `analyze my send times and open rates by timezone, then recommend a send schedule that maximizes opens for my 3 largest segments`

### 6. **Content Performance Clustering**
Groups your newsletter archive by:
- Topic/keyword
- Content format (educational, promotional, story-driven)
- Performance tier (top 25%, middle 50%, bottom 25%)
- Engagement trajectory (improving, stable, declining)

**Usage:** `cluster my last 50 newsletters by topic and show me which topics consistently outperform`

---

## Configuration

### Required Environment Variables

```bash
# Email platform credentials (choose at least one)
export MAILCHIMP_API_KEY="your_mailchimp_api_key"
export CONVERTKIT_API_KEY="your_convertkit_api_key"
export SUBSTACK_API_KEY="your_substack_api_key"

# Analytics (optional but recommended)
export GOOGLE_ANALYTICS_API_KEY="your_ga_api_key"

# Output delivery (optional)
export SLACK_WEBHOOK_URL="https://hooks.slack.com/services/YOUR/WEBHOOK"
export GOOGLE_DRIVE_FOLDER_ID="your_folder_id"
```

### Setup Instructions

1. **Connect your email platform:**
   - Mailchimp: Generate API key in Account → Extras → API keys
   - ConvertKit: Get API key in Creator Network → Account → API
   - Substack: Use API token from account settings

2. **Authorize analytics (optional):**
   - Google Analytics: Create service account JSON and set `GOOGLE_ANALYTICS_API_KEY`
   - This enables topic trend analysis and competitive benchmarking

3. **Test the connection:**
   ```
   Verify my email platform connection and show me subscriber count by engagement level
   ```

### Advanced Options

```yaml
engagement_threshold:
  inactive_days: 30           # Days without open = inactive
  churn_risk_days: 60         # Days without open = churn risk
  
segmentation:
  min_segment_size: 50        # Don't create segments smaller than N
  timezone_grouping: true     # Auto-group by timezone
  
calendar:
  lookahead_weeks: 12         # Generate calendar for N weeks
  content_diversity: 0.7      # 0-1 scale: how varied should topics be?
  
optimization:
  ab_test_sample_size: 100    # Min subscribers per A/B segment
  statistical_significance: 0.95
```

---

## Example Outputs

### Output 1: Editorial Calendar (CSV)

```
Week,Topic,Send_Day,Send_Time,Segment,Subject_Line_A,Subject_Line_B,Predicted_Winner,Confidence
1,"5 AI Productivity Tools for Product Managers",Tuesday,9:00 AM,High-Engagement,"New AI tools PMs are using 🤖","The AI stack your PM competitors are using",Subject_Line_A,0.78
1,"5 AI Productivity Tools for Product Managers",Wednesday,2:00 PM,Low-Engagement,"This changed how I manage projects","Quick wins for your product roadmap",Subject_Line_B,0.72
2,"How to Build Product Roadmaps with AI",Thursday,10:30 AM,High-Engagement,"Roadmaps 2.0: AI-powered planning","Your roadmap is about to change",Subject_Line_A,0.81
2,"How to Build Product Roadmaps with AI",Friday,3:00 PM,Low-Engagement,"The future of product planning","Simple roadmap framework (AI-powered)",Subject_Line_B,0.68
```

### Output 2: Churn Risk Segments (JSON)

```json
{
  "analysis_date": "2024-01-15",
  "total_subscribers": 5200,
  "churn_risk_segments": [
    {
      "segment_id": "seg_001",
      "segment_name": "Inactive Tech Readers (30-60 days no open)",
      "subscriber_count": 340,
      "churn_risk_score": 0.92,
      "original_interests": ["AI", "Product Strategy", "SaaS Trends"],
      "last_engagement": "2023-11-15",
      "re_engagement_hooks": [
        "The AI tool that changed how 10k+ PMs work",
        "Your competitors are using this (and you should too)",
        "New feature: AI-powered roadmap templates"
      ]
    },
    {
      "segment_id": "seg_002",
      "segment_name": "Mobile-Only Readers (declining engagement)",
      "subscriber_count": 210,
      "churn_risk_score": 0.68,
      "original_interests": ["Quick Tips", "News Roundups"],
      "engagement_trend": "declining 12% per week",
      "re_engagement_hooks": [
        "3-min reads: What PMs missed this week",
        "Mobile-friendly: 5 AI tools for on-the-go learning",
        "Podcast: Latest PM trends (listen while commuting)"
      ]
    }
  ]
}
```

### Output 3: Send Time Optimization (JSON)

```json
{
  "optimization_results": {
    "US_Eastern_High_Engagement": {
      "current_send_time": "Tuesday 9:00 AM",
      "recommended_send_time": "Tuesday 10:30 AM",
      "predicted_open_rate_lift": "+8.3%",
      "sample_size": 480,
      "confidence": 0.94,
      "subscriber_count": 1200
    },
    "US_Pacific_Low_Engagement": {
      "current_send_time": "Tuesday 9:00 AM",
      "recommended_send_time": "Wednesday 2:00 PM",
      "predicted_open_rate_lift": "+12.1%",
      "sample_size": 210,
      "confidence": 0.87,
      "subscriber_count": 520
    },
    "Europe_Mobile_Readers": {
      "current_send_time": "Tuesday 9:00 AM",
      "recommended_send_time": "Thursday 7:00 AM",
      "predicted_open_rate_lift": "+6.7%",
      "sample_size": 180,
      "confidence": 0.91,
      "subscriber_count": 450
    }
  }
}
```

---

## Tips & Best Practices

### 1. **Feed It Real Data for Better Recommendations**
- Provide at least 50+ historical emails for pattern analysis
- Include engagement data from the last 90 days minimum
- Ensure your email platform has accurate timezone/location data

### 2. **Segment by Behavior, Not Just Demographics**
- Don't just segment by timezone; combine with engagement level
- A West Coast subscriber who opens 80% of emails ≠ one who opens 10%
- Use the skill's automatic segmentation; manual segments often miss patterns

### 3. **A/B Test Subject Lines at Scale**
- Use the skill's subject line recommendations to power A/B tests
- Test 2 subject lines per week minimum (larger sample = faster learning)
- Feed results back into the skill monthly for continuous improvement

### 4. **Refresh Your Editorial Calendar Monthly**
- Run the skill every 4 weeks to incorporate new engagement data
- Topics that worked in Q1 may not work in Q2 (seasonal trends)
- Competitor topics shift; update your gap analysis regularly

### 5. **Act on Churn Risk Immediately**
- Re-engagement emails should go out within 48 hours of the skill identifying risk
- Use the recommended hooks; they're tailored to what the subscriber originally liked
- Track re-engagement campaign performance separately (higher bar than normal emails)

### 6. **Respect Subscriber Preferences**
- Segment by engagement level before increasing send frequency
- High-engagement subscribers can tolerate 3x/week; low-engagement need 1x/week
- Always provide easy preference center access for frequency/topic selection

---

## Safety & Guardrails

### What This Skill Will NOT Do

- **Override explicit subscriber preferences** — If a subscriber selected "1x per week," the skill will not recommend 3x/week sends, even if data suggests higher engagement potential
- **Enable spam or aggressive re-engagement** — Churn prevention recommendations assume ethical, value-driven content (not manipulative subject lines or bait-and-switch tactics)
- **Violate data privacy laws** — Does not collect PII beyond what your email platform already stores; complies with GDPR, CAN-SPAM, CASL
- **Predict individual subscriber behavior** — Only analyzes segment-level patterns, not individual subscriber predictions
- **Automatically send emails** — Generates recommendations only; all sends require human approval

### Limitations & Boundaries

- **Requires clean data** — If your email platform has incomplete timezone or engagement data, recommendations will be less accurate
- **Minimum data threshold** — Needs at least 20+ emails and 500+ subscribers for statistically significant recommendations
- **Niche-specific accuracy** — Works best for B2B, SaaS, and professional niches; consumer/entertainment niches may need manual review
- **Subject line suggestions are templates** — Use them as starting points; always customize for your brand voice
- **Seasonal blindness** — Historical data from winter may not apply to summer; the skill notes this but can't predict unprecedented seasonal shifts

### Ethical Guardrails

- Do not use churn risk detection to harass inactive subscribers
- Do not use segmentation to create "dark patterns" (e.g., aggressive re-engagement to inactive users)
- Always maintain a clear unsubscribe link and honor opt-outs immediately
- Respect the "preference center" — let subscribers choose topics and frequency
- Use engagement data to serve subscribers better, not to manipulate them

---

## Troubleshooting

### Q: "I got a low-confidence editorial calendar recommendation. Why?"
**A:** This typically means:
- Your historical email data is too small (< 30 emails) or too recent (< 90 days)
- Your subscriber segments are too small (< 100 per segment)
- Your engagement data has missing fields (timezone, device type)

**Solution:** Provide more historical data, or ask the skill to `generate a lower-confidence calendar with confidence threshold set to 0.70` (vs. the default 0.85).

---

### Q: "The recommended send times don't match what I'm currently doing. Should I change?"
**A:** Not necessarily. The skill recommends based on historical open rates, but:
- Your brand may have built habits (subscribers expect Tuesday 9 AM)
- Changing send times can temporarily hurt engagement as subscribers adjust
- Test incrementally: change one segment's send time, measure for 4 weeks, then decide

**Solution:** Run an A/B test with the skill's recommendation for 20% of a segment, measure for 4 weeks, then roll out if successful.

---

### Q: "My churn risk subscribers aren't re-engaging with the recommended hooks. What's wrong?"
**A:** Possible causes:
- The hooks are too generic; customize them to their specific interests
- Your re-engagement email is too long or comes across as desperate
- You're sending too frequently (re-engagement should be 1x per week max)
- The subscriber has genuinely lost interest; sometimes churn is natural

**Solution:** 
1.