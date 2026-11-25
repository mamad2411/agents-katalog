---
name: competitor-spy-tool
description: "Monitor competitor websites for pricing changes, new content, and keyword movements. Use when the user needs competitive intelligence, market tracking, or SEO benchmarking across multiple domains."
version: 1.0.0
homepage: https://github.com/ncreighton/empire-skills
metadata:
  {
    "openclaw": {
      "requires": {
        "env": ["COMPETITOR_DOMAINS", "SLACK_WEBHOOK_URL", "GOOGLE_SHEETS_API_KEY"],
        "bins": ["curl", "jq", "node"]
      },
      "os": ["macos", "linux", "win32"],
      "files": ["SKILL.md"],
      "emoji": "🕵️"
    }
  }
---

# Competitor Spy Tool

## Overview

The Competitor Spy Tool automates continuous monitoring of competitor websites, tracking critical business signals in real-time. This skill crawls multiple competitor domains on a schedule, detecting:

- **Price changes** across products/services
- **New content publications** (blog posts, landing pages, feature announcements)
- **Keyword ranking shifts** in SERPs (via SEO API integration)
- **Feature launches** and product updates
- **Promotional campaigns** and messaging changes
- **Metadata updates** (titles, descriptions, schema changes)

Perfect for **Product Managers**, **Marketing Teams**, **SEO Specialists**, and **E-commerce Managers** who need to stay ahead of market movements. Integrates with **Slack** for instant alerts, **Google Sheets** for historical tracking, and **WordPress** for automated blog post generation about competitor moves.

---

## Quick Start

Try these prompts immediately to see the tool in action:

### Example 1: Monitor Pricing Changes
```
Monitor my top 3 competitors for price changes on their main product pages.
Track: shopify.com, wix.com, squarespace.com
Alert me if any prices drop below $29/month
Send daily summary to Slack #marketing
```

### Example 2: Track New Content Launches
```
Watch these 5 SaaS competitors for new blog posts and feature announcements:
- competitors: [intercom.com, drift.com, hubspot.com, zendesk.com, freshworks.com]
- Check daily at 9 AM UTC
- Extract: title, publish date, main keywords, estimated word count
- Log to Google Sheet "Competitor Content Calendar"
- Slack alert if post targets our keywords
```

### Example 3: SEO Keyword Tracking
```
Track keyword rankings for my competitors across these terms:
Keywords: "project management software", "team collaboration tool", "agile workflow"
Competitors: asana.com, monday.com, jira.atlassian.com
Baseline: Google top 10 results
Alert threshold: If competitor moves up 5+ positions, notify Slack
Weekly report to Google Sheets with ranking history
```

### Example 4: Monitor Landing Page Changes
```
Watch competitor landing pages for:
- asana.com/pricing
- monday.com/pricing
- jira.atlassian.com/pricing
Changes to track: CTA text, pricing tiers, feature lists, testimonials
Detect: New tiers, removed features, messaging pivots
Email digest every Monday with change summary
```

---

## Capabilities

### 1. **Price Monitoring**
- Scrapes product pages and pricing tables
- Detects price increases/decreases with percentage change
- Tracks bundle pricing, discounts, and seasonal changes
- Compares pricing across tiers (Basic, Pro, Enterprise)
- Alerts when competitors match or undercut your pricing

**Usage Example:**
```
Monitor pricing on competitor product pages
Targets: [shopify.com/pricing, wix.com/pricing]
Fields: product name, tier, price, currency, billing cycle
Store in: Google Sheet "Pricing Intelligence"
Frequency: Daily
Alert if: Price drops > 10% OR new tier added
```

### 2. **Content Discovery & Tracking**
- Crawls blog/resource sections for new articles
- Extracts: title, publish date, URL, meta description, word count
- Identifies target keywords in competitor content
- Detects content gaps (topics they cover, you don't)
- Tracks content update frequency and publishing patterns

**Usage Example:**
```
Track competitor blog content
Sources: hubspot.com/blog, marketo.com/blog, pardot.com/blog
New content alert threshold: Published in last 24 hours
Extract keywords and categorize by topic
Send weekly "Competitor Content Digest" to marketing@company.com
```

### 3. **SEO & Keyword Ranking Monitoring**
- Integrates with SEMrush API, Ahrefs API, or Moz API
- Tracks competitor keyword rankings in Google SERPs
- Identifies new keywords competitors are ranking for
- Monitors position changes (movement tracking)
- Detects keyword opportunities (high-volume, low-competition)

**Usage Example:**
```
Track SEO rankings for competitor keywords
Competitors: [competitor1.com, competitor2.com]
Keywords: ["software pricing comparison", "best project management tools"]
Frequency: Weekly
Alert if: Competitor ranks #1 for keyword we target
Store rankings history in Google Sheets with date stamps
```

### 4. **Feature & Product Announcement Detection**
- Monitors product pages, changelogs, and announcement sections
- Detects new features, integrations, and partnerships
- Extracts feature descriptions and launch dates
- Tracks roadmap changes and deprecations
- Identifies competitive threats and opportunities

**Usage Example:**
```
Monitor competitor product announcements
Watch: [product-site.com/changelog, product-site.com/features]
Extract: Feature name, description, launch date, target user segment
Alert if: New feature directly competes with our offering
Log to "Competitive Feature Tracker" spreadsheet
```

### 5. **Promotional Campaign Tracking**
- Detects new promotions, discounts, and limited-time offers
- Tracks campaign messaging and creative angles
- Monitors email campaigns (if publicly accessible)
- Identifies seasonal promotions and patterns
- Captures promotional copy for competitive analysis

**Usage Example:**
```
Track competitor promotions and campaigns
Monitor: competitor-site.com/promotions, competitor-email-signup
Detect: New discount codes, limited-time offers, seasonal campaigns
Extract: Offer details, expiration dates, target audience
Alert if: Promotion runs during our key sales period
```

---

## Configuration

### Required Environment Variables

```bash
# Domain monitoring
COMPETITOR_DOMAINS="shopify.com,wix.com,squarespace.com"

# Slack notifications (optional but recommended)
SLACK_WEBHOOK_URL="https://hooks.slack.com/services/YOUR/WEBHOOK/URL"
SLACK_CHANNEL="#competitive-intelligence"

# Google Sheets integration for historical tracking
GOOGLE_SHEETS_API_KEY="your-google-api-key"
GOOGLE_SHEET_ID="your-sheet-id"

# SEO API integration (choose one)
SEMRUSH_API_KEY="your-semrush-key"  # OR
AHREFS_API_KEY="your-ahrefs-key"    # OR
MOZ_API_KEY="your-moz-key"

# Email notifications (optional)
SMTP_SERVER="smtp.gmail.com"
SMTP_USER="alerts@company.com"
SMTP_PASSWORD="your-app-password"

# Crawling preferences
CRAWL_FREQUENCY="daily"  # daily, weekly, hourly
CRAWL_TIME_UTC="09:00"
MAX_PAGES_PER_DOMAIN="50"
RESPECT_ROBOTS_TXT="true"
USER_AGENT="Mozilla/5.0 (compatible; CompetitorSpyBot/1.0)"
```

### Setup Instructions

1. **Set environment variables:**
   ```bash
   export COMPETITOR_DOMAINS="competitor1.com,competitor2.com"
   export SLACK_WEBHOOK_URL="https://hooks.slack.com/services/..."
   ```

2. **Configure Google Sheets (optional):**
   - Create a Google Cloud project and enable Sheets API
   - Download service account JSON credentials
   - Set `GOOGLE_SHEETS_API_KEY` to the JSON key path

3. **Choose your SEO API provider:**
   - SEMrush (recommended for price tracking + SEO)
   - Ahrefs (best for keyword research depth)
   - Moz (budget-friendly option)

4. **Test the connection:**
   ```bash
   curl -X GET "https://api.semrush.com/analytics/v3/" \
     -H "Authorization: Bearer $SEMRUSH_API_KEY"
   ```

---

## Example Outputs

### Price Change Alert (Slack)
```
🔴 PRICE DROP DETECTED
Competitor: Shopify
Product: Basic Plan
Previous: $29/month → Current: $24/month
Change: -17.2% (Save $60/year)
Detected: 2024-01-15 09:23 UTC
Action: Review your pricing strategy
```

### New Content Notification (Email)
```
📝 NEW COMPETITOR CONTENT
Source: HubSpot Blog
Title: "The Ultimate Guide to AI-Powered Sales Automation"
Published: 2024-01-15
Word Count: 4,200
Target Keywords: AI sales, automation, CRM, lead scoring
Your Coverage: 2/4 keywords (gap: "AI sales")
Recommendation: Create content for "AI sales" to compete
```

### SEO Ranking Report (Google Sheets)
```
| Keyword | Competitor | Current Rank | Previous Rank | Change | Date |
|---------|------------|--------------|---------------|--------|------|
| "project management" | asana.com | 2 | 3 | ↑ +1 | 2024-01-15 |
| "team collaboration" | monday.com | 1 | 1 | → 0 | 2024-01-15 |
| "agile workflow" | jira.com | 4 | 6 | ↑ +2 | 2024-01-15 |
```

### Feature Launch Alert (Slack)
```
⚡ NEW COMPETITOR FEATURE
Competitor: Intercom
Feature: "AI-Powered Response Suggestions"
Description: Automatically generate customer service responses using GPT-4
Launch Date: 2024-01-15
Status: Generally Available
Competitive Impact: HIGH - Direct threat to our AI feature roadmap
Recommendation: Accelerate similar feature or differentiate
```

---

## Tips & Best Practices

### 1. **Smart Domain Selection**
- Start with your top 3-5 direct competitors
- Add 2-3 indirect competitors (adjacent markets)
- Monitor market leaders even if not direct competitors
- Limit to 10-15 domains for manageable data volume

### 2. **Optimize Crawl Frequency**
- **Pricing pages**: Daily (changes can happen overnight)
- **Blog/content**: 2-3x per week (less frequent updates)
- **SEO rankings**: Weekly (daily is overkill, costs more)
- **Feature pages**: Weekly (launches are less frequent)
- **Off-peak hours**: Schedule crawls at 3-6 AM UTC to avoid rate limits

### 3. **Filter Noise, Capture Signal**
- Set meaningful alert thresholds (don't alert on every change)
- Example: Only alert if price drops >5% or new feature launches
- Use keyword filtering to ignore irrelevant content
- Combine multiple signals (e.g., price drop + new feature = high priority)

### 4. **Integrate with Your Workflow**
- **Slack**: Real-time alerts for critical changes
- **Google Sheets**: Historical tracking and trend analysis
- **WordPress**: Auto-publish blog posts analyzing competitor moves
- **Email**: Weekly digests for non-urgent updates
- **Jira**: Create tickets for product team on feature threats

### 5. **Respect Legal & Ethical Boundaries**
- Always respect robots.txt and rate limits
- Don't scrape private data (paywalled content, user data)
- Use appropriate User-Agent headers
- Avoid overwhelming competitor servers (spread requests)
- Review terms of service before monitoring

### 6. **Data Quality & Accuracy**
- Manually verify major price changes (scraping can error)
- Cross-reference with multiple sources when possible
- Keep historical data for trend analysis (6+ months recommended)
- Document data collection timestamps for context
- Use regex patterns to extract structured data reliably

---

## Safety & Guardrails

### What This Skill Will NOT Do

❌ **Unauthorized Access**: Will not bypass authentication, paywalls, or login walls
❌ **Illegal Scraping**: Will not violate Computer Fraud and Abuse Act or local laws
❌ **Personal Data**: Will not collect or store PII, user data, or private information
❌ **DDoS/Attacks**: Will not overwhelm servers or perform denial-of-service attacks
❌ **Copyright Violation**: Will not reproduce full competitor content without attribution
❌ **Malware/Injection**: Will not inject code, malware, or malicious payloads

### Limitations & Boundaries

- **Rate Limiting**: Respects robots.txt and implements polite crawling (1-2 req/sec per domain)
- **JavaScript-Heavy Sites**: May miss dynamic content (consider Puppeteer integration for JS rendering)
- **Paywalled Content**: Cannot access subscriber-only or authenticated content
- **Real-Time Accuracy**: Pricing/content may be cached (5-30 min delay typical)
- **Legal Responsibility**: User is responsible for compliance with local laws and competitor ToS
- **Data Retention**: Historical data older than 90 days may be archived or deleted per config

### Compliance Checklist

- ✅ Review competitor ToS before monitoring
- ✅ Implement appropriate rate limiting and delays
- ✅ Use descriptive User-Agent headers
- ✅ Respect robots.txt directives
- ✅ Don't scrape personal/private data
- ✅ Don't violate CFAA or local computer fraud laws
- ✅ Don't republish full competitor content without attribution
- ✅ Document your monitoring for audit purposes

---

## Troubleshooting

### Common Issues & Solutions

**Q: Slack alerts not sending**
- Verify `SLACK_WEBHOOK_URL` is correct and active
- Check Slack workspace permissions (bot must have message access)
- Test webhook: `curl -X POST -H 'Content-type: application/json' --data '{"text":"Test"}' $SLACK_WEBHOOK_URL`
- Ensure channel exists and bot is invited to channel

**Q: Price detection missing changes**
- Competitor may have changed page structure (HTML/CSS updated)
- Increase `MAX_PAGES_PER_DOMAIN` to crawl more pages
- Manually inspect competitor site for pricing location
- Consider using Puppeteer for JavaScript-rendered content
- Add custom CSS selectors for that competitor's pricing table

**Q: Google Sheets integration failing**
- Verify API key has Sheets API enabled (not just Drive API)
- Check sheet ID is correct (from URL: `docs.google.com/spreadsheets/d/{SHEET_ID}`)
- Ensure service account email is added as editor to the sheet
- Test API: `curl -H "Authorization: Bearer $GOOGLE_SHEETS_API_KEY" https://sheets.googleapis.com/v4/spreadsheets/$GOOGLE_SHEET_ID`

**Q: SEO ranking data looks stale**
- Check API key validity and rate limits (SEMrush limits 100 req/month on free tier)
- Verify keywords are in correct format (URL-encoded if spaces)
- Note: Ranking data refreshes 1-2x per month on most APIs (not real-time)
- Consider weekly crawls instead of daily to manage API quota

**Q: Crawling too slow or timing out**
- Reduce `MAX_PAGES_PER_DOMAIN` (start with 10-20)
- Increase timeout threshold (default 30s per page)
- Reduce number of concurrent domains (process 2-3 at a time)
- Schedule during off-peak hours to avoid network congestion

**Q: Getting blocked by competitor (403/429 errors)**
- Add random delays between requests (2-5 seconds)
- Rotate User-Agent headers
- Reduce crawl frequency or spread across more time
- Consider using proxy service if blocking persists
- Check robots.txt for disallowed paths and respect them

**Q: False positives in change detection**
- Competitor site may have dynamic content (ads, widgets changing)
- Implement "noise filtering" to ignore layout/ad changes
- Use text-diff instead of HTML-diff to focus on content
- Increase change threshold (only alert if >20% of page changed)
- Manually review alerts before acting on them

**Q: Cost concerns with API usage**
- SEMrush free tier: 100 requests/month
- Switch to Moz