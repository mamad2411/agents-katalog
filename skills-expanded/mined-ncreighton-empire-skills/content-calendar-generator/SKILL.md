---
name: content-calendar-generator
description: "Generate AI-powered monthly content calendars from trending topics, seasonal events, and keyword gaps. Use when the user needs SEO content planning, editorial calendars, or multi-channel publishing schedules."
version: 1.0.0
homepage: https://github.com/ncreighton/empire-skills
metadata:
  {"openclaw":{"requires":{"env":["OPENAI_API_KEY","GOOGLE_SEARCH_API_KEY","SERPAPI_KEY"],"bins":["python3"]},"os":["macos","linux","win32"],"files":["SKILL.md"],"emoji":"📅"}}
---

## Overview

The **Content Calendar Generator** is an AI-powered automation skill that builds comprehensive monthly editorial calendars tailored to your industry, audience, and SEO strategy. This skill eliminates manual research by analyzing trending topics, seasonal events, keyword gaps, and competitor content to produce a structured, publication-ready calendar.

### Why This Matters

Content teams spend 10-15 hours weekly on calendar planning, research, and coordination. This skill automates that entire workflow, delivering:

- **SEO-optimized topics** based on Google Trends, keyword difficulty, and search volume
- **Seasonal relevance** with holiday hooks, industry events, and cultural moments
- **Multi-channel scheduling** for blog, email, social media, and video
- **Competitor gap analysis** to find untapped content opportunities
- **Cross-platform integration** with WordPress, HubSpot, Asana, Slack, and Google Calendar

Perfect for marketing teams, agencies, solopreneurs, and content creators who need data-driven planning without the research overhead.

---

## Quick Start

Try these prompts immediately to see the skill in action:

### Example 1: SaaS Product Launch Calendar
```
Generate a 90-day content calendar for a B2B SaaS product launch (project management tool).
Include:
- 15 blog posts targeting product keywords
- 20 social media posts (LinkedIn, Twitter)
- 4 email nurture sequences
- Seasonal tie-ins for Q1
- Competitor gap analysis vs. Asana, Monday.com, and Jira
Format as CSV with columns: Date, Channel, Topic, Keyword, Search Volume, Difficulty, CTA
```

### Example 2: E-commerce Holiday Planning
```
Create a 6-month content calendar for an eco-friendly fashion e-commerce brand.
Focus on:
- Seasonal events (Earth Day, Black Friday, New Year)
- Trending hashtags and TikTok/Instagram Reels topics
- Product launch announcements (3 new collections)
- User-generated content campaigns
- Email campaigns tied to each season
Include estimated reach and engagement metrics for each piece.
Output as JSON with metadata for WordPress scheduling.
```

### Example 3: Personal Brand / Newsletter
```
Generate a 12-week content calendar for a personal finance newsletter targeting millennials.
Analyze trending topics in:
- Cryptocurrency and Web3
- Side hustles and remote work
- Sustainable investing
- Debt payoff strategies
Include:
- Weekly newsletter themes
- 3 viral content ideas per week
- Guest post opportunities
- Podcast episode topics
- LinkedIn article calendar
Rank by estimated engagement potential.
```

---

## Capabilities

### 1. **Trend & Keyword Analysis**
Analyzes Google Trends, SEMrush, Ahrefs, and SerpAPI data to identify:
- Rising keywords in your niche (30-day, 90-day, 12-month trends)
- Search volume and keyword difficulty scores
- Long-tail keyword opportunities with low competition
- Question-based keywords (People Also Ask)
- Seasonal search patterns

**Usage Example:**
```
Analyze trending topics in "sustainable fashion" for Q1 2024.
Show keywords with:
- Search volume > 500/month
- Difficulty < 40
- Trend trajectory (up/down)
List the top 20 opportunities with estimated traffic potential.
```

### 2. **Seasonal & Event-Based Planning**
Automatically maps:
- National holidays and observances (US, UK, EU, Asia-Pacific)
- Industry-specific events (conferences, award seasons, fiscal calendars)
- Cultural moments and trending conversations
- Product launch windows
- Promotional periods (Black Friday, Cyber Monday, Prime Day, etc.)

**Usage Example:**
```
Map all relevant seasonal events for a fitness brand in 2024.
Include:
- Fitness industry events (IHRSA, fitness expos)
- New Year's resolutions (Jan), summer body (Apr-May), fall training (Sep)
- Holiday gift guides (Nov-Dec)
- Weather-based content (winter workouts, spring training)
```

### 3. **Competitor Gap Analysis**
Crawls competitor content and identifies:
- Topics competitors are covering (and you're not)
- Content formats they're using (blogs, videos, podcasts, infographics)
- Publishing frequency and cadence
- Engagement metrics (estimated shares, comments)
- Backlink opportunities and cited sources

**Usage Example:**
```
Analyze content gaps vs. HubSpot, Mailchimp, and ConvertKit in the email marketing space.
Show:
- Topics they cover that we don't
- Topics we cover that they don't (our advantages)
- Underperforming content we could improve
- Emerging topics none of us cover yet
Prioritize by search volume and engagement potential.
```

### 4. **Multi-Channel Distribution Planning**
Generates channel-specific content for:
- **Blog/Website**: Long-form SEO articles (2,000-5,000 words)
- **Email**: Newsletter themes, nurture sequences, promotional campaigns
- **Social Media**: LinkedIn posts, Twitter threads, TikTok/Instagram Reels scripts
- **Video**: YouTube video outlines, thumbnail ideas, script frameworks
- **Podcast**: Episode topics, guest suggestions, show notes templates

### 5. **Audience Segmentation & Personalization**
Tailors content calendar to:
- Buyer journey stage (awareness, consideration, decision)
- Audience personas (role, industry, company size, pain points)
- Content preferences (visual, textual, interactive, educational)
- Engagement history and past performance data

---

## Configuration

### Required Environment Variables

```bash
# OpenAI API (for content generation and analysis)
export OPENAI_API_KEY="sk-..."

# Google Search API (for trend analysis)
export GOOGLE_SEARCH_API_KEY="your-key-here"

# SerpAPI (for competitor analysis and keyword data)
export SERPAPI_KEY="your-key-here"

# Optional: HubSpot, WordPress, Slack, Asana integrations
export HUBSPOT_API_KEY="your-key-here"
export WORDPRESS_API_KEY="your-key-here"
export SLACK_WEBHOOK_URL="https://hooks.slack.com/..."
export ASANA_API_KEY="your-key-here"
```

### Setup Instructions

1. **API Keys**: Obtain keys from OpenAI, Google Cloud Console, and SerpAPI
2. **Python Dependencies**: Install `openai`, `google-api-python-client`, `serpapi`, `pandas`, `requests`
3. **Data Files**: Provide CSV with competitor URLs, audience personas, or historical performance data (optional)
4. **Integrations**: Connect WordPress, HubSpot, Asana, or Slack for automatic scheduling/notifications

### Configuration Options

```yaml
calendar_config:
  duration: "30"              # days (30, 60, 90, 365)
  channels:
    - blog
    - email
    - social_media
    - video
  
  seo_settings:
    min_search_volume: 100
    max_keyword_difficulty: 50
    include_long_tail: true
    
  competitor_analysis:
    competitors: ["competitor1.com", "competitor2.com"]
    analyze_backlinks: true
    
  seasonal_focus: "all"       # "all", "q1", "q2", "q3", "q4"
  
  output_format: "csv"        # csv, json, markdown, google_sheets
```

---

## Example Outputs

### Output Format 1: CSV Calendar
```
Date,Channel,Topic,Keyword,Search Volume,Difficulty,CTA,Estimated Reach,Format
2024-01-08,Blog,New Year Fitness Goals for Busy Professionals,fitness goals 2024,8900,32,Sign up for 7-day challenge,1200,Article
2024-01-10,Email,New Year Motivation Series Part 1,new year fitness,6500,28,Click to read blog,2400,Newsletter
2024-01-12,Social,5 Quick Workouts Under 15 Minutes,quick workout,12000,25,Link in bio,450,Instagram Carousel
2024-01-15,Blog,The Science Behind HIIT Training,HIIT training benefits,5600,42,Download free guide,800,Long-form Article
2024-01-17,Video,How to Build a Home Gym on a Budget,home gym setup,4200,35,Subscribe for more,350,YouTube Script
```

### Output Format 2: JSON with Metadata
```json
{
  "calendar_metadata": {
    "generated_date": "2024-01-01",
    "duration_days": 30,
    "total_pieces": 24,
    "estimated_reach": 45000,
    "channels": ["blog", "email", "social", "video"]
  },
  "content_pieces": [
    {
      "id": "piece_001",
      "date": "2024-01-08",
      "channel": "blog",
      "topic": "New Year Fitness Goals for Busy Professionals",
      "keyword": "fitness goals 2024",
      "seo_metrics": {
        "search_volume": 8900,
        "difficulty": 32,
        "trend": "up"
      },
      "content_outline": [
        "Why goals matter for fitness success",
        "5 SMART goal examples for 2024",
        "How to track progress without obsessing"
      ],
      "cta": "Sign up for our 7-day challenge",
      "estimated_reach": 1200,
      "format": "2500-word article",
      "internal_links": ["challenge-page", "goal-tracking-tool"]
    }
  ]
}
```

### Output Format 3: Google Sheets Integration
Automatically creates a shared Google Sheet with:
- Sortable/filterable calendar
- Color-coded by channel and priority
- Embedded competitor analysis sidebar
- Collaboration features (comments, assignments)
- Auto-synced with WordPress/HubSpot for scheduling

---

## Tips & Best Practices

### 1. **Align Calendar with Business Goals**
Before generating, define:
- Primary KPI (traffic, leads, revenue, brand awareness)
- Target audience persona(s)
- Seasonal revenue patterns
- Product launch dates or promotions

**Pro Tip**: Include historical performance data (past blog traffic, email open rates) so the skill can prioritize high-performing content types.

### 2. **Leverage Competitor Intelligence**
- Provide 3-5 competitor URLs for gap analysis
- Analyze both direct competitors and adjacent players
- Look for underserved topics with high search volume
- Identify content formats that drive engagement in your space

### 3. **Balance Evergreen & Trending Content**
- **Evergreen (60%)**: Foundational topics, how-tos, ultimate guides (sustained traffic)
- **Trending (30%)**: News hooks, seasonal content, viral opportunities (quick wins)
- **Promotional (10%)**: Product launches, sales, webinars, CTAs (conversion focus)

### 4. **Optimize for Multi-Channel Repurposing**
One piece of core research can become:
- 1 long-form blog post (2,500+ words)
- 1 email sequence (4-5 emails)
- 8-10 social media posts (LinkedIn, Twitter, Instagram)
- 1 video script (YouTube, TikTok)
- 1 podcast episode outline

Use the skill's "repurpose" feature to maximize ROI on research.

### 5. **Plan for Consistency**
- Set a realistic publishing cadence (2x/week blog, 3x/day social, 1x/week email)
- Build in 2-week buffer for editing, design, and approvals
- Schedule content batching sessions (dedicate 1 day/week to creation)
- Use integrations to auto-publish and notify teams

### 6. **Monitor & Iterate**
- Track actual performance vs. estimates (traffic, engagement, conversions)
- Feed performance data back into the skill for next month's calendar
- Identify your top-performing content types and topics
- Adjust keyword targets based on actual search volume and difficulty

---

## Safety & Guardrails

### What This Skill WILL NOT Do

- **Create plagiarized content**: The skill generates topic ideas and outlines; actual content creation requires human authorship
- **Bypass SEO best practices**: Recommends only ethical, white-hat SEO tactics (no keyword stuffing, cloaking, or manipulative linking)
- **Violate competitor IP**: Analyzes publicly available content only; does not scrape proprietary data
- **Generate misinformation**: Recommends fact-checking and expert review for health, legal, financial, and scientific claims
- **Automate publishing without approval**: Generates calendars for human review; integrations require explicit approval before publishing

### Limitations & Boundaries

1. **Data Freshness**: Trend data is 24-48 hours old; real-time trending topics may not be captured
2. **Niche Markets**: Works best for industries with significant search volume; ultra-niche topics may lack data
3. **Personalization**: Calendar reflects provided personas; accuracy depends on persona quality
4. **Competitor Analysis**: Limited to publicly available content; cannot access private/gated content
5. **Forecast Accuracy**: Estimated reach/traffic is based on historical benchmarks; actual results vary by execution quality and audience

### Recommended Guardrails

- **Always fact-check**: Verify claims, especially in health, finance, and legal spaces
- **Attribute sources**: Link to original research and cite competitor content appropriately
- **Respect robots.txt**: Ensure competitor analysis respects website crawling policies
- **Get approval**: Have stakeholders approve calendar before publishing
- **Monitor performance**: Track actual metrics; adjust strategy if targets aren't met

---

## Troubleshooting

### Common Issues & Solutions

**Q: "API key not found" error**
- **A**: Ensure all required env vars are set. Run `echo $OPENAI_API_KEY` to verify. Restart your terminal after setting variables.

**Q: "No trending topics found for my niche"**
- **A**: Niche is too specific. Try broader keywords first (e.g., "sustainable fashion" instead of "eco-friendly hemp activewear"). Add 2-3 competitor URLs for gap analysis.

**Q: "Search volume estimates seem too high/low"**
- **A**: Estimates are based on US search data. Adjust for target geography. Use SerpAPI directly to verify keyword data.

**Q: "Calendar doesn't match my brand voice"**
- **A**: The skill generates topic ideas and outlines, not final copy. Customize content during creation phase. Provide brand guidelines in the prompt for tone/style preferences.

**Q: "How do I integrate with WordPress/HubSpot?"**
- **A**: Use the `output_format: "json"` option and export to Zapier, Make.com, or native integrations (WordPress REST API, HubSpot API). See references/ folder for integration templates.

**Q: "Can I generate a calendar for multiple brands/products?"**
- **A**: Yes. Run the skill separately for each brand, or provide multiple audience personas in a single request. Output will segment by persona.

**Q: "How often should I regenerate the calendar?"**
- **A**: Monthly is standard. Regenerate weekly for fast-moving industries (news, tech, finance). Update mid-month if major trends shift.

**Q: "What if my competitors aren't ranking for the keywords recommended?"**
- **A**: That's a gap opportunity! Low-difficulty keywords with high search volume are ideal targets. Rank for them before competitors do.

**Q: "Can I use this for non-English content?"**
- **A**: Yes. Specify language in the prompt (e.g., "Generate calendar in Spanish for Mexican audience"). Trend data may be less robust for non-English queries.

---

## Next Steps

1. **Set up API keys** (5 minutes)
2. **Define your audience personas** (15 minutes)
3. **List 3-5 competitors** (5 minutes)
4. **Run your first calendar** (2 minutes)
5. **Customize and approve** (30 minutes)
6. **Integrate with WordPress/HubSpot** (optional, 15 minutes)
7. **Start publishing** and track performance

---

**Tags for ClawHub Discovery**: content-calendar, SEO, editorial-planning, content-