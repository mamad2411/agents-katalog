---
name: wordpress-seo-autopilot
description: "Automate WordPress SEO optimization with meta tags, schema markup, internal linking, and RankMath integration. Use when the user needs to improve search rankings, bulk optimize pages, or set up continuous SEO monitoring."
version: 1.0.0
homepage: https://github.com/ncreighton/empire-skills
metadata:
  {
    "openclaw": {
      "requires": {
        "env": [
          "WORDPRESS_API_KEY",
          "WORDPRESS_SITE_URL",
          "RANKMATH_API_KEY",
          "GOOGLE_SEARCH_CONSOLE_KEY"
        ],
        "bins": []
      },
      "os": ["macos", "linux", "win32"],
      "files": ["SKILL.md"],
      "emoji": "🚀"
    }
  }
---

# WordPress SEO Autopilot

## Overview

WordPress SEO Autopilot is a comprehensive automation skill that transforms your WordPress site into a search-engine-optimized powerhouse. This skill eliminates manual SEO grunt work by automatically generating and applying meta titles, meta descriptions, schema markup, internal linking strategies, and RankMath configurations across your entire site.

**Why this matters:** Most WordPress sites lose 40-60% of potential organic traffic due to poor SEO fundamentals. Manual optimization is time-consuming and error-prone. This skill automates the repetitive work so you can focus on content strategy and user experience.

**Key Integrations:**
- **WordPress REST API** — Direct site access and bulk page updates
- **RankMath API** — Advanced SEO settings, focus keywords, and readability scoring
- **Google Search Console** — Performance data, indexing status, and keyword insights
- **Slack** — Real-time notifications for optimization progress and issues
- **Google Analytics 4** — Traffic correlation with SEO improvements

---

## Quick Start

### Example 1: Bulk Meta Tag Optimization
```
"Analyze my WordPress site at example.com and generate optimized meta titles 
and descriptions for all 47 published posts. Use the RankMath API to set 
focus keywords based on current search volume. Send me a Slack summary when done."
```

### Example 2: Schema Markup Implementation
```
"Add JSON-LD schema markup to all blog posts on my WordPress site. Use 
Article schema with author, publication date, and featured image. Verify 
markup validity with Google's Rich Results Test. Report any errors."
```

### Example 3: Internal Linking Strategy
```
"Scan my WordPress site for orphaned pages and low-authority posts. Create 
an internal linking strategy that connects 5-7 relevant posts to each page. 
Update links using RankMath's internal linking feature. Show me the before/after 
link distribution."
```

### Example 4: SEO Audit & Automated Fixes
```
"Run a complete SEO audit on my WordPress site. Check for missing alt text, 
duplicate meta descriptions, broken internal links, and missing schema. 
Auto-fix what you can and create a prioritized report for manual review."
```

### Example 5: Continuous Monitoring Setup
```
"Set up automated daily SEO monitoring for my WordPress site. Track keyword 
rankings, meta tag compliance, schema validity, and indexing status. Alert me 
via Slack if any pages drop below SEO best practices. Generate weekly reports."
```

---

## Capabilities

### 1. Meta Tag Generation & Optimization
- **Auto-generate meta titles** (50-60 characters) based on page content and target keywords
- **Create meta descriptions** (150-160 characters) with natural keyword inclusion
- **Prevent duplicate meta tags** across your site
- **Dynamic title/description templates** for different post types (blog, product, service)
- **RankMath integration** for SEO score optimization (target: 80+ score)
- **Real-time validation** against Google's latest guidelines

**Usage Example:**
```
"Generate SEO-optimized meta titles for all 23 product pages. Each title 
should be 55-60 characters, include the product name, primary keyword, and 
a benefit statement. Use RankMath to verify focus keyword optimization."
```

### 2. Schema Markup Implementation
- **Article schema** — Blog posts with author, date, word count, featured image
- **Product schema** — E-commerce products with price, rating, availability
- **LocalBusiness schema** — Service-based businesses with address, phone, hours
- **FAQ schema** — Automatically extract Q&A and format for rich snippets
- **BreadcrumbList schema** — Navigation hierarchy for better SERP display
- **Validation reports** — Verify markup with Google Rich Results Test API

**Usage Example:**
```
"Add comprehensive schema markup to all 15 service pages. Include LocalBusiness, 
Service, and AggregateRating schemas. Validate with Google's API and fix any errors."
```

### 3. Internal Linking Automation
- **Orphan page detection** — Identify posts with zero internal links
- **Contextual link suggestions** — Find relevant pages to link based on content similarity
- **Link anchor text optimization** — Use keyword-rich, descriptive anchor text
- **Link distribution analysis** — Ensure authority flows to important pages
- **Broken link detection** — Find and fix 404s before they hurt SEO
- **RankMath internal linking** — Leverage RankMath's built-in linking suggestions

**Usage Example:**
```
"Analyze my 120 blog posts and create an internal linking map. Link each 
post to 5-7 contextually relevant posts. Prioritize linking to pillar pages 
and high-authority content. Use RankMath to verify link quality."
```

### 4. RankMath Integration
- **Focus keyword assignment** — Automatically set primary and secondary keywords
- **Content optimization** — Apply RankMath's readability, keyword density, and structure recommendations
- **Redirect management** — Create 301 redirects for old URLs and consolidated content
- **Bulk SEO settings** — Apply consistent SEO rules across post types
- **Competitor analysis** — Compare your content against top-ranking competitors
- **SEO score tracking** — Monitor improvements over time

**Usage Example:**
```
"Use RankMath to optimize all 50 blog posts for their primary keywords. 
Target a minimum SEO score of 85. Fix readability issues, improve keyword 
placement, and add missing headers. Generate a compliance report."
```

### 5. Content Analysis & Recommendations
- **Keyword gap analysis** — Find keywords your competitors rank for but you don't
- **Content freshness** — Identify outdated posts that need updating
- **Readability scoring** — Ensure content is accessible to your audience
- **Word count analysis** — Compare your posts against top-ranking competitors
- **Topic clustering** — Group related content for better internal linking
- **Content suggestions** — Recommend new topics based on search volume and competition

**Usage Example:**
```
"Analyze my 80 blog posts and identify the top 10 underperforming posts 
by traffic and ranking. Suggest content improvements, keyword additions, 
and internal linking opportunities. Prioritize by potential traffic gain."
```

### 6. Monitoring & Alerting
- **Daily ranking checks** — Track keyword positions for your target keywords
- **Indexing status** — Monitor which pages are indexed in Google Search Console
- **Core Web Vitals** — Track LCP, FID, CLS metrics and alert on degradation
- **Broken link monitoring** — Continuous scanning for 404s and redirects
- **Duplicate content detection** — Find and fix duplicate meta tags and content
- **Slack/Email alerts** — Real-time notifications for critical issues
- **Weekly/monthly reports** — Comprehensive SEO performance dashboards

**Usage Example:**
```
"Set up continuous monitoring for my 60 target keywords. Check rankings daily 
and alert me via Slack if any keyword drops 5+ positions. Generate a weekly 
report showing ranking trends, new keywords ranking, and lost rankings."
```

---

## Configuration

### Required Environment Variables

```bash
# WordPress API Authentication
WORDPRESS_API_KEY=your_wordpress_application_password
WORDPRESS_SITE_URL=https://example.com
WORDPRESS_REST_ENDPOINT=/wp-json/wp/v2

# RankMath Integration
RANKMATH_API_KEY=your_rankmath_api_key
RANKMATH_SITE_ID=your_rankmath_site_id

# Google Integration
GOOGLE_SEARCH_CONSOLE_KEY=your_gsc_api_key
GOOGLE_ANALYTICS_KEY=your_ga4_api_key

# Slack Integration (Optional)
SLACK_WEBHOOK_URL=https://hooks.slack.com/services/YOUR/WEBHOOK/URL

# Configuration Options
SEO_TITLE_LENGTH=55-60
SEO_DESCRIPTION_LENGTH=150-160
SCHEMA_TYPES=article,product,faq,localbusiness
INTERNAL_LINK_TARGET=5-7
MIN_SEO_SCORE=80
```

### Setup Instructions

1. **Generate WordPress Application Password:**
   - Log in to WordPress admin dashboard
   - Navigate to Users → Your Profile
   - Scroll to "Application Passwords"
   - Create new password named "SEO Autopilot"
   - Copy and set as `WORDPRESS_API_KEY`

2. **Get RankMath API Key:**
   - Go to RankMath dashboard → Settings → General
   - Find API Key section
   - Enable API access and copy key

3. **Enable Google Search Console API:**
   - Create Google Cloud Project
   - Enable Search Console API
   - Create service account credentials
   - Share your site with service account email

4. **Configure Slack Webhook (Optional):**
   - Create Slack app at api.slack.com
   - Enable Incoming Webhooks
   - Create webhook for your channel

---

## Example Outputs

### Meta Tag Optimization Report
```
✅ OPTIMIZATION COMPLETE

📊 Results Summary:
- Pages Processed: 47
- Meta Titles Generated: 47
- Meta Descriptions Generated: 47
- Duplicate Meta Tags Fixed: 3
- Average SEO Score Improvement: +12 points

🎯 Top Optimizations:
1. "5 Best WordPress SEO Plugins for 2024 | Expert Comparison"
   - RankMath Score: 88/100
   - Focus Keyword: "WordPress SEO plugins"

2. "Complete WordPress SEO Guide | Step-by-Step Tutorial"
   - RankMath Score: 85/100
   - Focus Keyword: "WordPress SEO guide"

⚠️ Pages Needing Review:
- /blog/old-post-2020 (RankMath Score: 62/100 - Consider updating)
- /about-us (Meta description too long: 185 chars, target: 160)
```

### Internal Linking Strategy
```
🔗 INTERNAL LINKING ANALYSIS

📈 Current State:
- Total Pages: 120
- Orphaned Pages: 8
- Avg Links Per Page: 3.2
- Link Distribution: Uneven (5 pages have 40% of all links)

🎯 Recommended Strategy:
- Add 47 new internal links
- Target: 5-7 links per page
- Focus: Distribute authority to key pillar pages

✨ Top Link Opportunities:
1. Link "WordPress SEO Guide" → 12 related posts
2. Link "RankMath Tutorial" → 8 setup guides
3. Link "Schema Markup" → 6 technical posts

📊 Before/After:
- Before: 287 total links, 8 orphaned pages
- After: 334 total links, 0 orphaned pages
- Authority Distribution: +35% more balanced
```

### SEO Audit Report
```
🔍 COMPLETE SEO AUDIT REPORT

✅ Passed (45 pages):
- Proper schema markup
- Valid meta tags
- Alt text on all images
- Mobile-friendly

⚠️ Issues Found (12 pages):
- Missing alt text: 8 pages (auto-fixed)
- Duplicate meta descriptions: 3 pages (auto-fixed)
- Missing schema: 1 page (needs review)

❌ Critical Issues (2 pages):
- Broken internal links: /blog/old-post (5 broken links)
- Indexing blocked: /admin-test-page (noindex tag present)

📋 Action Items:
1. [AUTO-FIXED] Added alt text to 47 images
2. [AUTO-FIXED] Fixed 3 duplicate meta descriptions
3. [NEEDS REVIEW] Add schema to /services/custom-development
4. [NEEDS REVIEW] Remove noindex from /admin-test-page
```

### Monitoring Dashboard
```
📊 WEEKLY SEO PERFORMANCE REPORT

🎯 Keyword Rankings:
- Keywords Tracked: 35
- Improved: 8 (+2.3 avg positions)
- Declined: 2 (-1.5 avg positions)
- New Rankings (Top 100): 3

📈 Traffic Impact:
- Organic Sessions: +12% (↑287 sessions)
- Avg Position: 18.4 (↓0.6 from last week)
- CTR: 3.2% (↑0.1%)

🔗 Internal Linking:
- New Links Added: 47
- Broken Links Fixed: 3
- Orphaned Pages: 0

✅ Technical Health:
- Core Web Vitals: All Green
- Indexing Status: 120/120 pages indexed
- Crawl Errors: 0

🚀 Top Performers This Week:
1. "WordPress SEO Guide" - Rank #4 for "WordPress SEO" (+3 positions)
2. "RankMath Tutorial" - Rank #7 for "RankMath setup" (+5 positions)
```

---

## Tips & Best Practices

### 1. Keyword Research First
- Use Google Search Console to identify your current keywords
- Run keyword gap analysis before bulk optimization
- Target long-tail keywords (lower competition, higher intent)
- Balance primary and secondary keywords naturally

### 2. Content Quality Over Optimization
- Automation helps, but great content ranks best
- Ensure content is helpful, original, and comprehensive
- Optimize for user intent, not just keywords
- Update evergreen content regularly

### 3. Internal Linking Strategy
- Link from high-authority pages to new/low-authority pages
- Use descriptive anchor text (avoid "click here")
- Keep link density natural (1 link per 100-150 words)
- Prioritize linking to money pages and pillar content

### 4. Schema Markup Best Practices
- Use appropriate schema for your content type
- Validate markup with Google Rich Results Test
- Include all required and recommended properties
- Test on mobile (rich snippets appear differently)

### 5. Monitoring & Iteration
- Track rankings for 30+ days before assessing impact
- Monitor Core Web Vitals weekly
- Review indexing status in Google Search Console
- Adjust strategy based on data, not assumptions

### 6. RankMath Optimization
- Set realistic SEO score targets (80-85 is excellent)
- Don't sacrifice readability for keyword optimization
- Use RankMath's competitor analysis to find gaps
- Leverage internal linking suggestions from RankMath

### 7. Avoid Common Pitfalls
- ❌ Don't keyword stuff (damages readability and rankings)
- ❌ Don't create duplicate content across pages
- ❌ Don't ignore Core Web Vitals (ranking factor since 2021)
- ❌ Don't link to irrelevant pages (hurts user experience)
- ❌ Don't set and forget (SEO is continuous)

---

## Safety & Guardrails

### What This Skill WILL NOT Do

❌ **Violate Google Guidelines**
- This skill follows Google's SEO Starter Guide and E-E-A-T principles
- Does not create cloaking, doorway pages, or deceptive redirects
- Does not implement keyword stuffing or hidden text
- Does not purchase or exchange links

❌ **Damage Your Site**
- All changes are logged and reversible
- Requires explicit confirmation before bulk updates
- Performs validation checks before publishing changes
- Creates automatic backups before major operations

❌ **Violate Terms of Service**
- Respects WordPress, RankMath, and Google ToS
- Does not scrape or violate API rate limits
- Does not access sites without proper authentication
- Does not modify competitor sites

❌ **Guarantee Rankings**
- This skill optimizes technical SEO and on-page factors
- Rankings depend on content quality, backlinks, and competition
- Google's algorithm has 200+ ranking factors
- Results typically take 4-12 weeks to appear

### Limitations & Boundaries

⚠️ **Technical Limitations:**
- Requires WordPress 5.0+ with REST API enabled
- Works with RankMath Free, Pro, or Business plans
- Google Search Console API has