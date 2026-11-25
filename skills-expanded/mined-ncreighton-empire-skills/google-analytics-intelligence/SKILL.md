---
name: google-analytics-intelligence
description: "Extract GA4 metrics, detect traffic anomalies, and auto-generate growth recommendations. Use when the user needs analytics reports, conversion tracking, or traffic diagnosis across websites."
version: 1.0.0
homepage: https://github.com/ncreighton/empire-skills
metadata:
  {
    "openclaw": {
      "requires": {
        "env": ["GOOGLE_ANALYTICS_PROPERTY_ID", "GOOGLE_SERVICE_ACCOUNT_JSON"],
        "bins": []
      },
      "os": ["macos", "linux", "win32"],
      "files": ["SKILL.md"],
      "emoji": "📊"
    }
  }
---

## Overview

**Google Analytics Intelligence** automates the extraction, analysis, and interpretation of Google Analytics 4 (GA4) data to deliver actionable insights without manual dashboard navigation. This skill eliminates the friction of jumping between GA4, spreadsheets, and reporting tools by delivering:

- **Automated data extraction** from GA4 via the Google Analytics Reporting API v4
- **Anomaly detection** that identifies unusual traffic patterns, conversion dips, and user behavior changes
- **Intelligent report generation** with visualizations, trends, and comparisons
- **Growth recommendations** powered by pattern analysis (what channels, pages, or campaigns are driving results)
- **Slack/email integration** for scheduled reports and alerts
- **WordPress integration** for tracking conversions on landing pages and content performance

This skill is valuable for:
- **Marketing teams** tracking campaign ROI and channel attribution
- **E-commerce businesses** monitoring conversion funnels and revenue per session
- **SaaS companies** analyzing onboarding flows and user engagement trends
- **Content creators** measuring page performance and audience behavior
- **Agencies** generating client reports automatically and detecting issues before clients do

---

## Quick Start

Try these prompts immediately to see the skill in action:

```
1. "Pull my GA4 data for the last 30 days and identify any traffic anomalies. 
   Focus on users by source/medium and conversion rate changes."
```

```
2. "Generate a weekly traffic report comparing this week vs. last week. 
   Include top pages, traffic sources, and conversion funnel metrics. 
   Format for Slack posting."
```

```
3. "Analyze my GA4 data for the past 90 days. What pages have the highest 
   bounce rates? What traffic sources drive the most revenue? 
   Suggest 3 actions to improve conversion rate."
```

```
4. "Set up an automated anomaly detector. Alert me if daily users drop 
   more than 25%, or if conversion rate falls below my 30-day average. 
   Send alerts to Slack #analytics channel."
```

```
5. "Compare traffic from organic search vs. paid ads for my top 10 landing pages. 
   Show cost-per-acquisition, sessions, and revenue impact. 
   Identify which pages have the best ROI."
```

---

## Capabilities

### 1. **Automated GA4 Data Extraction**
Connects directly to your GA4 property using OAuth 2.0 service account authentication. Pulls:
- Sessions, users, and pageviews
- Conversion events (custom events, purchases, sign-ups, etc.)
- Traffic source data (organic, paid, direct, referral, social)
- Device and audience demographics
- User engagement metrics (session duration, scroll depth, video views)
- E-commerce data (revenue, items sold, average order value)

**Usage Example:**
```
"Pull all conversion events from my GA4 property for the past 7 days. 
Group by user_source_medium and show count, conversion rate, and 
average event value. Export as CSV."
```

### 2. **Intelligent Anomaly Detection**
Uses statistical baselines (moving averages, standard deviation) to identify:
- Sudden traffic spikes or drops
- Conversion rate deviations (>15% change)
- Unusual user behavior (increased bounce rate, session duration changes)
- Revenue anomalies (cost-per-acquisition spiking)
- Device/channel performance shifts

**Usage Example:**
```
"Scan my last 30 days of GA4 data for anomalies. If any metric deviates 
more than 20% from its 30-day average, flag it and suggest a root cause 
(e.g., 'Traffic from Facebook Ads dropped 35% on March 15 - possible 
campaign pause or budget cut')."
```

### 3. **Dynamic Report Generation**
Creates professional reports with:
- Period-over-period comparisons (week/week, month/month, year/year)
- Visual summaries (tables, trend lines, distribution charts)
- Narrative insights (highlighting winners and problem areas)
- Custom metrics and KPI dashboards
- PDF export with branding options
- Slack message formatting with embedded data

**Usage Example:**
```
"Generate a monthly performance report for March. Include: total revenue, 
top 10 landing pages by conversions, traffic sources ranked by ROI, 
funnel drop-off analysis, and 5 key insights. Format for client email."
```

### 4. **Growth Action Recommendations**
Analyzes patterns to suggest:
- High-performing channels to increase budget allocation
- Low-performing pages to optimize or sunset
- Underutilized traffic sources to expand
- Funnel improvements (where users drop off)
- A/B test opportunities based on traffic volume and variance
- Audience segments to retarget (users with high intent, high cart abandonment)

**Usage Example:**
```
"Based on 90 days of GA4 data, tell me: Which 3 channels should I 
invest more in? Which 3 pages need optimization? What traffic source 
has the lowest CAC? Suggest 5 specific actions to increase revenue 
by 20%."
```

### 5. **Scheduled Anomaly Alerts**
Sets up continuous monitoring with:
- Daily/weekly digest emails or Slack messages
- Real-time alerts for critical deviations
- Customizable thresholds (e.g., "alert if daily revenue drops 30%")
- Auto-generated explanations (traffic drop? conversion issue? seasonality?)
- Comparison to historical baselines

**Usage Example:**
```
"Create a daily anomaly alert. If sessions drop >20%, OR conversion rate 
falls >15% below 30-day average, OR revenue per session falls >10%, 
send me a Slack DM with the anomaly and suggested next steps."
```

### 6. **Integration with Marketing Tools**
Connects GA4 insights to:
- **Slack** — automated reports, alerts, daily digests
- **Google Sheets** — export data for team collaboration
- **WordPress** — track post performance, landing page conversions
- **Zapier/Make** — trigger workflows based on anomalies
- **HubSpot** — sync GA4 revenue data to contact records
- **Email** — scheduled PDF reports to stakeholders

---

## Configuration

### Environment Variables (Required)
```
GOOGLE_ANALYTICS_PROPERTY_ID=123456789
# Your GA4 Property ID (found in Admin > Property Settings > Property ID)

GOOGLE_SERVICE_ACCOUNT_JSON={"type": "service_account", "project_id": "...", ...}
# Service account JSON key with Analytics API access
# Create at: Google Cloud Console > APIs & Services > Credentials > Service Account

SLACK_WEBHOOK_URL=https://hooks.slack.com/services/YOUR/WEBHOOK/URL
# Optional: for automated Slack reporting

WORDPRESS_SITE_URL=https://yoursite.com
# Optional: for WordPress integration
```

### Setup Instructions

1. **Enable Google Analytics API**
   - Go to Google Cloud Console
   - Create a project or use existing
   - Enable "Google Analytics Reporting API"
   - Create a Service Account key (JSON format)
   - Download and paste into `GOOGLE_SERVICE_ACCOUNT_JSON`

2. **Grant Service Account Access to GA4**
   - In GA4 Admin > Account Access > Account > Manage all properties
   - Add your service account email as an Editor
   - Wait 5-10 minutes for permissions to propagate

3. **Optional: Connect Slack**
   - Create a Slack Incoming Webhook in your workspace
   - Paste URL into `SLACK_WEBHOOK_URL`
   - Test: `"Send a test Slack message"`

4. **Optional: Connect WordPress**
   - Install a GA4 WordPress plugin (e.g., MonsterInsights, ExactMetrics)
   - Authenticate with GA4 property
   - Skill will auto-detect and pull post-level performance data

---

## Example Outputs

### Output 1: Weekly Traffic Report
```
📊 WEEKLY ANALYTICS REPORT (Mar 10-16)
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

🎯 KEY METRICS
Users: 4,250 (+12% vs last week)
Sessions: 6,100 (+8%)
Conversions: 340 (+18%)
Revenue: $4,850 (+15%)

📍 TOP TRAFFIC SOURCES
1. Organic Search: 2,100 users (49%) - $2,310 revenue
2. Google Ads: 1,200 users (28%) - $1,890 revenue  
3. Direct: 620 users (15%) - $450 revenue
4. Referral: 330 users (8%) - $200 revenue

🏆 TOP PAGES (by revenue)
1. /pricing — 45 conversions, $2,250 revenue (50% conversion rate)
2. /features — 38 conversions, $1,890 revenue (22% conversion rate)
3. /blog/seo-tips — 12 conversions, $450 revenue (8% conversion rate)

⚠️ ANOMALIES DETECTED
• Organic traffic up 18% (trending positive)
• Mobile conversion rate down 12% (investigate mobile UX)
• Direct traffic spike on Mar 12 (+45%) — possible press mention?

💡 RECOMMENDATIONS
→ Increase Google Ads budget (ROI: 3.2x)
→ A/B test mobile checkout flow
→ Analyze Mar 12 spike — may indicate new backlinks
```

### Output 2: Anomaly Alert
```
🚨 TRAFFIC ANOMALY DETECTED
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

ISSUE: Conversion rate dropped 28%
Baseline (30-day avg): 4.2%
Current (today): 3.0%
Time: March 17, 2:30 PM

POSSIBLE CAUSES (ranked by likelihood):
1. Checkout form broken — validation errors increased 340%
2. Email campaign sent to cold list (high bounce rate)
3. Traffic quality decreased (organic CTR down, ad fraud suspected)
4. Competitor promotion — paid ads CTR down 15%

RECOMMENDED ACTIONS:
✓ Check Google Search Console for indexing issues
✓ Test checkout flow on mobile/desktop
✓ Review Ads campaign settings for recent changes
✓ Monitor next 2 hours — anomaly may be temporary
```

### Output 3: Growth Recommendations Report
```
📈 90-DAY GROWTH ACTION PLAN
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

OPPORTUNITY #1: Scale High-ROI Channels
Current: Google Ads spend $2,000/mo → Revenue $6,400 (3.2x ROAS)
Recommendation: Increase to $4,000/mo
Projected Impact: +$6,400 revenue/month
Confidence: 95%
Action: Request 100% budget increase for top 5 keywords

OPPORTUNITY #2: Fix Mobile Conversion Funnel
Current: Mobile conversion rate 1.8% vs Desktop 5.2%
Issue: 68% of mobile users abandon at payment step
Recommendation: Simplify mobile checkout (1-click payment, guest checkout)
Projected Impact: +2.5% mobile conversion rate = +$1,200/month
Confidence: 88%
Timeline: 2 weeks to implement

OPPORTUNITY #3: Expand Organic Search
Current: Organic traffic 2,100 users/week, opportunity: 4,000 users/week
Low-hanging fruit: 15 blog posts with high impressions, low CTR
Recommendation: Optimize title tags, meta descriptions, featured snippets
Projected Impact: +35% organic traffic = +$2,100/month
Confidence: 82%
Timeline: 30 days

OPPORTUNITY #4: Reduce Ad Spend Waste
Current: Display Ads ROI 0.8x (losing money)
Recommendation: Pause underperforming placements, retarget website visitors
Projected Impact: Save $400/month on Display, invest in Search
Confidence: 92%
Timeline: Immediate

TOTAL PROJECTED GROWTH: +$9,700/month (+45% revenue increase)
Effort Level: Medium (2-3 weeks implementation)
```

---

## Tips & Best Practices

### 1. **Set Up Conversion Events Properly**
GA4 relies on event tracking. Ensure these are configured:
- Purchase/payment completion
- Sign-up/account creation
- Add to cart
- Contact form submission
- Book demo/consultation
- Video plays (if relevant)

Use the skill to audit: `"What conversion events are being tracked in my GA4 property? Which ones have <100 events/month and might be misconfigured?"`

### 2. **Use Segment Comparisons for Deeper Insights**
Don't just look at aggregate data. Break down by:
- Device type (mobile vs. desktop conversion rates often differ drastically)
- Traffic source (organic vs. paid have different user quality)
- Geographic region (international traffic may need localization)
- User behavior (new vs. returning users)

```
"Compare conversion rates for new vs. returning users. 
Which segment spends more per transaction? 
Should I focus retention budget on high-value returners?"
```

### 3. **Create Custom Dashboards for Different Roles**
- **Marketing**: Traffic sources, campaign performance, CPA
- **Sales**: Lead quality, conversion funnel, contact form submissions
- **C-suite**: Revenue trend, customer acquisition cost, growth rate
- **Product**: Feature usage, user engagement, onboarding completion

Use the skill to generate role-specific reports:
```
"Generate a 'CMO Dashboard' showing monthly revenue, top 5 channels by ROI, 
CAC trend, and YoY growth rate. Make it one-page, suitable for board presentation."
```

### 4. **Establish Anomaly Baselines**
The skill learns your normal patterns over time. After 30 days:
- Set baseline thresholds based on your actual variance
- High-variance businesses (seasonal, event-driven) need wider thresholds
- Low-variance businesses can use tighter thresholds for early detection

```
"Analyze my last 90 days of traffic. What's my typical daily variance? 
What should my anomaly threshold be to avoid false alarms but catch real issues?"
```

### 5. **Combine GA4 with Other Data Sources**
GA4 tells you *what* happened, but not always *why*. Cross-reference with:
- **Google Search Console** — search query rankings and CTR
- **Social media analytics** — content performance and engagement
- **Email platform** (Mailchimp, ConvertKit) — campaign effectiveness
- **Help desk tickets** — customer pain points
- **Server logs** — technical issues affecting traffic

### 6. **Review Anomalies Weekly, Not Just When Alerted**
Anomaly detection catches sudden changes, but trends develop gradually. Spend 10 minutes weekly reviewing:
- Weekly growth rate (is it accelerating or decelerating?)
- Seasonal patterns (are holidays/events affecting data?)
- Cohort analysis (are newer users engaging better than old ones?)

---

## Safety & Guardrails

### What This Skill Will NOT Do

❌ **Will NOT overwrite or delete GA4 data** — read-only access, safe for production
❌ **Will NOT make changes to your GA4 configuration** — analysis only, no modifications to properties, events, or filters
❌ **Will NOT access personal user data** — respects GA4 privacy controls and aggregates data appropriately
❌ **Will NOT predict the future** — growth recommendations are based on historical patterns, not guaranteed forecasts
❌ **Will NOT integrate with third-party tools without explicit approval** — requires explicit setup (Slack webhook, WordPress, etc.)
❌ **Will NOT bypass GA4 API rate limits** — respects Google's 100K requests/day quota per property
❌ **Will NOT share data with external services** — all processing happens locally or on approved platforms only

### Limitations & Boundaries

⚠️ **Data