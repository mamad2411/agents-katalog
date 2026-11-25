---
name: launch-window-optimizer-time-zone-traffic-pattern-analyzer
description: "Analyze historical traffic patterns, time zone distribution, and competitor timing to recommend optimal launch windows for products, courses, or campaigns. Use when the user needs data-driven launch timing, maximum visibility strategy, or campaign momentum planning."
version: 1.0.0
homepage: https://github.com/ncreighton/empire-skills
metadata:
  {"openclaw":{"requires":{"env":["GOOGLE_ANALYTICS_API_KEY","GOOGLE_SHEETS_API_KEY","SLACK_WEBHOOK_URL"],"bins":["python3","curl"]},"os":["macos","linux","win32"],"files":["SKILL.md"],"emoji":"🚀"}}
---

# Launch Window Optimizer: Time Zone × Traffic Pattern Analyzer

## Overview

**Launch Window Optimizer** is a sophisticated growth strategy tool that transforms raw traffic data into actionable launch recommendations. Rather than guessing when to go live, this skill analyzes:

- **Historical traffic patterns** from Google Analytics (hourly, daily, weekly trends)
- **Audience geographic distribution** (time zones, regions, countries)
- **Competitor launch timing** (social signals, press release patterns, market gaps)
- **Seasonal & cultural factors** (holidays, industry events, shopping patterns)

The skill outputs **hour-by-hour recommendations** for maximum initial momentum, visibility across all time zones, and competitive advantage. Perfect for SaaS launches, course releases, product drops, campaign rollouts, and community announcements.

**Integrations:** Google Analytics 4, Google Sheets, Slack, WordPress, Zapier, HubSpot, ConvertKit, Substack, Twitter/X API, Product Hunt API.

---

## Quick Start

Try these prompts immediately:

```
Analyze my Google Analytics traffic for Q4 2024 and recommend the best 
launch window for my new SaaS product targeting US and EU audiences. 
Include competitor timing insights from similar product launches.
```

```
I'm launching an online course on [topic] next month. My audience is 
40% US Eastern, 35% UTC+1 (Europe), 25% UTC+8 (Asia). What's the optimal 
launch day and time? Include timezone-specific prep activities.
```

```
Schedule a 48-hour product campaign with staggered notifications across 
time zones. Show me the hour-by-hour breakdown that maximizes reach for 
each regional audience segment. Format as a Google Calendar import file.
```

```
My historical data shows peak traffic Wednesdays 10am-2pm EST. Analyze 
seasonal patterns in my WordPress analytics and recommend 3 alternative 
launch windows if Wednesday isn't available.
```

---

## Capabilities

### 1. **Traffic Pattern Analysis**
Ingests Google Analytics 4 data to identify:
- Peak traffic hours across 7-day, 30-day, and 90-day windows
- Day-of-week performance (which days generate highest engagement?)
- Bounce rate analysis by time slot (quality vs. quantity)
- Page load performance correlation (faster pages = better launch timing)
- Mobile vs. desktop traffic distribution across hours

**Usage Example:**
```
Input: GA4 property ID + date range
Output: {
  "peak_hours": ["10:00-11:00", "14:00-15:00", "19:00-20:00"],
  "best_day": "Wednesday",
  "confidence_score": 0.92,
  "audience_online_distribution": [...]
}
```

### 2. **Time Zone Optimization**
Maps audience location data to determine:
- Simultaneous coverage across regions (e.g., "9am EST = 2pm GMT = 11pm JST")
- Staggered launch windows for sequential regional reach
- Overlap analysis (when can you reach multiple zones simultaneously?)
- Recommendation: Single launch time vs. multi-phased rollout

**Usage Example:**
```
Audience breakdown: 45% EST, 30% PST, 20% GMT, 5% IST
Recommendation: Launch Tuesday 1:00 PM EST to catch morning GMT, 
afternoon PST, evening IST within 8-hour window.
```

### 3. **Competitor Launch Intelligence**
Analyzes market positioning via:
- Twitter/X API: Track competitor announcement timestamps
- Product Hunt API: Analyze trending launch times
- Press release database queries: Industry launch patterns
- Reddit/HN activity timing: Community discussion peaks
- Industry event calendars: Avoid launch collision windows

### 4. **Momentum Forecasting**
Predictive models for:
- Expected traffic surge magnitude (based on historical similar campaigns)
- Viral coefficient estimation
- Sustained engagement curves (first 24h, 7d, 30d)
- Conversion lift predictions by launch window
- ROI projection by launch timing ($X investment → $Y revenue)

### 5. **Multi-Channel Campaign Orchestration**
Generates integrated launch schedules:
- Email send times (ConvertKit, Substack APIs)
- Social media posting cadence (Twitter, LinkedIn, Instagram optimal times)
- Slack/Discord announcement timing
- WordPress publication scheduling
- SMS/push notification windows
- Zapier workflow automation rules

### 6. **Risk & Conflict Detection**
Alerts you to:
- Major competitor launches within ±72 hours
- Trending cultural events (viral topics = lower visibility)
- Platform downtime windows (avoid launching when services are degraded)
- Regional holidays/blackout periods
- Industry event calendars (conference weekends, earnings dates)

---

## Configuration

### Required Environment Variables

```bash
# Google Analytics 4
export GOOGLE_ANALYTICS_API_KEY="your-ga4-api-key"
export GA4_PROPERTY_ID="123456789"

# Google Sheets (for historical data storage & reporting)
export GOOGLE_SHEETS_API_KEY="your-sheets-api-key"
export SHEETS_TEMPLATE_ID="your-template-spreadsheet-id"

# Slack notifications (optional but recommended)
export SLACK_WEBHOOK_URL="https://hooks.slack.com/services/YOUR/WEBHOOK"

# Social/Competitor Intelligence (optional)
export TWITTER_API_KEY="your-twitter-bearer-token"
export PRODUCTHUNT_API_KEY="your-producthunt-api-key"
```

### Setup Instructions

1. **Connect Google Analytics:**
   - Go to Google Cloud Console → Create new project
   - Enable Google Analytics Data API
   - Create service account → Download JSON credentials
   - Share GA4 property with service account email

2. **Authorize Google Sheets:**
   - Create copy of template: [Link to template]
   - Share with same service account
   - Copy Spreadsheet ID into environment

3. **Optional: Configure Social APIs**
   - Twitter: Developer Portal → Create app → Get bearer token
   - Product Hunt: Settings → API → Generate token

---

## Example Outputs

### Output 1: Hour-by-Hour Recommendation Grid

```
LAUNCH WINDOW ANALYSIS: Q1 2025 New Course Release
Generated: 2024-12-15 | Confidence: 94%

RECOMMENDED LAUNCH: Tuesday, January 14 @ 10:00 AM EST

┌─────────────────────────────────────────────────────────┐
│ TIME ZONE COVERAGE SNAPSHOT                             │
├─────────────────────────────────────────────────────────┤
│ 10:00 AM EST  → Morning (engagement +23%)              │
│  7:00 AM PST  → Early morning (engagement +15%)        │
│  3:00 PM GMT  → Afternoon (engagement +28%)            │
│  8:30 PM IST  → Evening (engagement +12%)              │
└─────────────────────────────────────────────────────────┘

EXPECTED REACH:
• Hour 1: 2,400 concurrent visitors
• Hour 6: 8,900 concurrent visitors (peak)
• Hour 24: 34,200 unique visitors
• 72-hour total: 126,300 unique visitors

HISTORICAL COMPARISON:
Your typical Tuesday 10am launch: 89 avg visitors/hour
Recommended window: 312 avg visitors/hour (+250%)

COMPETITOR ANALYSIS:
• Nearest competitor launch: Friday 2pm EST (3 days later)
• Market saturation risk: LOW (only 1 competitor posting that week)
• Press coverage likelihood: HIGH (media picks Tuesday product news)
```

### Output 2: Google Calendar Import Format

```ics
BEGIN:VCALENDAR
VERSION:2.0
PRODID:-//Launch Optimizer//ClawHub//EN
CALSCALE:GREGORIAN
METHOD:PUBLISH

BEGIN:VEVENT
DTSTART:20250114T150000Z
DTEND:20250114T160000Z
SUMMARY:🚀 MAIN LAUNCH: Email announcement + Website go-live
DESCRIPTION:Send ConvertKit email to 45K subscribers
LOCATION:Your website
UID:launch-main-20250114@clawhub
END:VEVENT

BEGIN:VEVENT
DTSTART:20250114T170000Z
DTEND:20250114T180000Z
SUMMARY:Social Wave 1: Twitter/LinkedIn posts
DESCRIPTION:Post across all major social platforms
UID:launch-social1-20250114@clawhub
END:VEVENT

BEGIN:VEVENT
DTSTART:20250114T220000Z
DTEND:20250114T230000Z
SUMMARY:Asia-optimized push: Staggered message
DESCRIPTION:LinkedIn/Twitter posts in UTC+8 language
UID:launch-asia-20250114@clawhub
END:VEVENT

END:VCALENDAR
```

### Output 3: Detailed Recommendation Report (Google Sheet)

```
Sheet Name: "Launch_Recommendation_Jan2025"

Column A: Time Slot
Column B: EST Coverage
Column C: GMT Coverage
Column D: JST Coverage
Column E: Expected Traffic
Column F: Social Sentiment Signal
Column G: Competitor Activity
Column H: Recommended Action

Row 1: Headers
Row 2: 09:00 | ✓ High | ✓ Medium | ✗ Minimal | 2,100 | Positive | None | PREPARE
Row 3: 10:00 | ✓ Peak | ✓ High | ✗ Minimal | 3,800 | Trending | Low | GO LIVE ⭐
Row 4: 11:00 | ✓ High | ✓ High | ✗ Minimal | 3,200 | Positive | None | POST SOCIAL
...
```

---

## Tips & Best Practices

### 1. **Pre-Launch Data Collection (2-4 weeks prior)**
- Ensure Google Analytics is capturing complete data
- Run analysis on at least 30 days of historical traffic
- Cross-reference with email open rates, social engagement peaks
- Account for upcoming holidays/events in your calendar

### 2. **Multi-Phase Launches > Single Bang**
- If audience spans 3+ time zones, consider staggered launch
- First wave (8am local) → Second wave (12pm local) → Third wave (6pm local)
- Each phase gets fresh email/social pushes → multiplies reach

### 3. **Pre-Heat Strategy (24-48 hours before)**
- Announce "coming soon" Tuesday to warm up audience
- Build anticipation with countdown posts
- Email segmentation by timezone for preview access
- This creates FOMO + increases Day 1 momentum

### 4. **Competitor Blindspot Analysis**
- If 3+ competitors launching same week, shift ±3 days
- Position as "complementary alternative" vs. direct competitor
- Capitalize on competitor launch fatigue (users overwhelmed)

### 5. **Content Maturation Curve**
- Day 1: Initial surge (you + media mentions)
- Days 2-3: Secondary surge (word-of-mouth from early buyers)
- Days 4-7: Sustained interest (organic traffic + social shares)
- Day 8+: New equilibrium
- Schedule content/updates to ride each wave

### 6. **A/B Test Launch Windows**
- If possible, launch soft version (limited access) on recommended time
- Monitor first 2-hour conversion rate
- If underperforming, pivot to backup window immediately
- Use learnings for Phase 2 rollout

### 7. **Regional Customization**
- Translate launch messaging for non-English markets
- Adjust send times to "native peak hours" (not just timezone conversion)
- Example: Japan doesn't peak at same conversion rate as US even at equivalent hour

---

## Safety & Guardrails

**What This Skill Will NOT Do:**

❌ **Guarantee sales or traffic increases** — recommends optimal timing; actual performance depends on product quality, marketing execution, pricing

❌ **Predict viral moments** — provides data-driven recommendations, not trend forecasting; virality is unpredictable

❌ **Bypass algorithm changes** — based on historical patterns; social platform algorithm updates can shift recommendations

❌ **Manipulate competitor data** — uses only public information (Twitter, Product Hunt, press releases); never scrapes private analytics

❌ **Generate content** — only recommends timing; you must create actual email copy, social posts, landing pages

❌ **Guarantee competitor data accuracy** — relies on public APIs which may be incomplete or delayed

**Limitations:**

- **Data freshness**: Requires GA4 data from past 30+ days for accuracy
- **Regional accuracy**: Works best for English-speaking markets; cultural factors in Asia/MENA may require manual adjustment
- **API rate limits**: Google Analytics API has daily quotas; large-scale analysis may batch over multiple days
- **Time zone edge cases**: Daylight saving time transitions require manual verification
- **Platform dependency**: Social API changes (Twitter, Product Hunt) may affect competitor analysis

**Privacy & Compliance:**

- All analysis is **read-only** from your own GA4 property
- No personal user data is stored or transmitted externally
- GDPR/CCPA compliant (respects privacy settings in GA4)
- Recommend: Review any Slack webhook logs for sensitive info

---

## Troubleshooting

### "No data found in Google Analytics"
**Solution:** 
- Verify GA4 property ID matches your website
- Confirm service account email has "Viewer" role on property
- Check that GA4 has been collecting data for 30+ days
- Run test query: `openai_execute("python3 test_ga_connection.py")`

### "Time zone recommendations seem off for my audience"
**Solution:**
- Manually input audience breakdown if auto-detection is inaccurate
- Cross-reference with email platform's open rate data
- Use Slack channel activity times if internal team
- Consider that audience behavior may vary by season

### "Competitor data missing from analysis"
**Solution:**
- Twitter API requires authentication; verify bearer token
- Product Hunt API has rate limits; retry after 1 hour
- Manually add known competitor launches to Google Sheet
- Focus on your own traffic patterns if external data unavailable

### "Expected traffic numbers seem too high/low"
**Solution:**
- Compare against previous campaign conversion rates
- Adjust confidence interval (conservative vs. optimistic projection)
- Account for new vs. returning audience composition
- Test recommendation on small segment first (email list subset)

### "Slack notifications not arriving"
**Solution:**
- Verify webhook URL is current (webhooks expire after 30 days of inactivity)
- Check Slack workspace settings → Installed Apps → Permissions
- Test webhook manually: `curl -X POST -H 'Content-type: application/json' --data '{"text":"Test"}' YOUR_WEBHOOK_URL`
- Enable notifications in your Slack preferences

### "Google Sheets API returning 403 errors"
**Solution:**
- Spreadsheet must be shared with service account email
- Verify API is enabled in Google Cloud Console
- Check quota limits haven't been exceeded (100 requests/100 seconds default)
- Try creating new spreadsheet from template vs. using existing

### "How do I know which timezone to launch in if I serve global audience?"
**Solution:**
- Launch in timezone with 35-45% of your audience (sweet spot)
- If evenly distributed, choose largest time zone (covers most hours simultaneously)
- Use "staggered" approach: 3 separate launches ±8 hours apart
- Review email open rates by timezone to find actual peak times

### "Can I schedule this to run automatically every month?"
**Solution:**
- Yes! Create Zapier workflow: "First of month" → Run this skill
- Store results in Google Sheet for historical trending
- Set Slack reminder 72 hours before recommended window
- Export calendar events to team calendars automatically

---

## Getting Help

- **Skill Documentation:** Full Python code in `/references/analyzer.py`
- **ClawHub Community:** Post questions in #growth-strategy channel
- **API Issues:** Check rate limit status at `google.com/cloud/console`
- **Feature Requests:** GitHub issues at homepage link above

**Last Updated:** December 2024 | **Status:** Production Ready