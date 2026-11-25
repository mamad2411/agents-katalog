---
name: ai-niche-keyword-gap-and-content-opportunity-mapper
description: "Analyze competitor content gaps and identify high-intent keyword clusters your competitors missed. Use when the user needs SEO content strategy, niche keyword research, or competitive content opportunities."
version: 1.0.0
homepage: https://github.com/ncreighton/empire-skills
metadata:
  {
    "openclaw": {
      "requires": {
        "env": ["SEMRUSH_API_KEY", "AHREFS_API_KEY", "GOOGLE_SEARCH_CONSOLE_KEY"],
        "bins": []
      },
      "os": ["macos", "linux", "win32"],
      "files": ["SKILL.md"],
      "emoji": "🎯"
    }
  }
---

## Overview

The **AI Niche Keyword Gap and Content Opportunity Mapper** is a production-ready SEO automation skill that identifies untapped content opportunities in your niche by analyzing competitor keyword rankings and content strategies. This skill compares your site against the top 20 competitors, discovers high-intent keywords with low competition, and generates 50+ ranked content ideas with actionable metrics.

### Why This Matters

Most SEO strategies rely on generic keyword tools. This skill goes deeper—it finds the *gaps* where competitors haven't published content for valuable search queries. By analyzing search volume, cost-per-click (CPC), keyword difficulty, and backlink opportunities, you can prioritize content that drives both traffic and revenue.

### Key Integrations

- **Google Search Console** — pulls your current keyword rankings and impressions
- **Semrush API** — competitor keyword analysis, backlink data, content gaps
- **Ahrefs API** — domain authority scoring, URL-level authority metrics
- **WordPress** — direct content planning integration with editorial calendar
- **Slack** — automated daily/weekly opportunity reports to your team
- **Google Sheets** — exports ranked keyword opportunities for collaboration

---

## Quick Start

Try these prompts immediately to see the skill in action:

### Example 1: Basic Niche Analysis
```
Analyze keyword gaps for my SaaS project management niche.
My domain: projectflow.io
Top competitors: asana.com, monday.com, notion.so, jira.atlassian.com, clickup.com
Focus on: "project management for remote teams", "agile software", "task management"
```

### Example 2: E-Commerce Competitive Analysis
```
Find content opportunities in the "sustainable fashion" niche.
My site: ecothread.shop
Competitors: patagonia.com, everlane.com, reformation.com, allbirds.com, veja.com
Include: backlink opportunities, content gap analysis, CPC estimates
Output format: ranked by search volume and commercial intent
```

### Example 3: Local Service Business
```
Map keyword gaps for a digital marketing agency in Austin, Texas.
My domain: austindigitalco.com
Competitors: wistia.com, hubspot.com, mailchimp.com (national), plus 5 local agencies
Focus on: local intent keywords, service-based content, case study opportunities
Prioritize: keywords with 100-500 monthly searches and low difficulty
```

---

## Capabilities

### 1. Competitor Keyword Analysis
- **Scrapes top 20 competitors** across your niche using Semrush and Ahrefs
- **Extracts 2,000+ ranked keywords** per competitor with monthly search volume, difficulty, and CPC
- **Identifies overlapping keywords** where you rank but competitors don't, and vice versa
- **Maps keyword clusters** (e.g., "project management" cluster includes "task tracking," "team collaboration," "sprint planning")

### 2. Content Gap Discovery
- **Finds high-intent keywords** (commercial, transactional, informational) with <40 difficulty score that competitors haven't targeted
- **Analyzes competitor content** for each keyword (article length, publish date, engagement metrics)
- **Scores feasibility** — can you realistically rank for this keyword given your domain authority?
- **Prioritizes by ROI potential** — search volume × CPC × ranking difficulty

### 3. Content Opportunity Generation
- **Generates 50+ specific content ideas** ranked by search volume, CPC, and feasibility
- **Suggests content types** — blog posts, pillar pages, comparison guides, case studies, tutorials
- **Recommends target URLs** — where to publish on your site for optimal internal linking
- **Includes semantic keywords** — LSI keywords and related search terms to naturally incorporate

### 4. Competitive URL Analysis
- **Identifies which competitor URLs rank** for each opportunity keyword
- **Extracts on-page SEO metrics** — title tags, meta descriptions, H1/H2 structure, word count, backlink count
- **Scores content quality** — readability, multimedia usage, freshness, authority signals
- **Reveals backlink sources** — where competitors get links from for ranking authority

### 5. Backlink Opportunity Scoring
- **Maps backlink profiles** for top-ranking URLs in your niche
- **Identifies link sources** — industry publications, resource pages, directories, guest posting opportunities
- **Scores link quality** — domain authority, relevance, traffic potential
- **Suggests outreach targets** — where to pitch your content for maximum link velocity

---

## Configuration

### Required Environment Variables

```bash
# Semrush API credentials (for competitor keyword & content analysis)
SEMRUSH_API_KEY=your_semrush_api_key_here

# Ahrefs API credentials (for backlink and domain authority data)
AHREFS_API_KEY=your_ahrefs_api_key_here

# Google Search Console API (for your site's current rankings)
GOOGLE_SEARCH_CONSOLE_KEY=your_gsc_json_key_here
GOOGLE_PROPERTY_URL=https://yoursite.com

# Optional: Slack webhook for automated reports
SLACK_WEBHOOK_URL=https://hooks.slack.com/services/YOUR/WEBHOOK/URL

# Optional: WordPress integration for content calendar
WORDPRESS_API_URL=https://yoursite.com/wp-json
WORDPRESS_API_TOKEN=your_bearer_token
```

### Configuration Options

```yaml
analysis_depth: "comprehensive"  # Options: quick, standard, comprehensive
competitor_count: 20             # Number of competitors to analyze (5-50)
keyword_volume_min: 50           # Minimum monthly searches to include
keyword_difficulty_max: 50       # Maximum difficulty score (0-100)
content_idea_count: 50           # Number of opportunities to generate
include_backlink_analysis: true  # Enable backlink opportunity scoring
output_format: "json"            # Options: json, csv, markdown, google_sheets
auto_slack_report: false         # Send weekly summary to Slack
```

---

## Example Outputs

### Content Opportunity Report (Top 10 Ideas)

```json
{
  "niche": "Project Management for Remote Teams",
  "analysis_date": "2024-01-15",
  "total_opportunities": 52,
  "top_opportunities": [
    {
      "rank": 1,
      "keyword": "best project management tools for remote teams",
      "search_volume": 2400,
      "search_trend": "rising",
      "keyword_difficulty": 28,
      "cpc": "$3.20",
      "commercial_intent": "high",
      "content_type": "comparison guide",
      "target_url": "/blog/best-pm-tools-remote-teams",
      "estimated_monthly_traffic": 180,
      "ranking_feasibility": "high",
      "competitor_content": {
        "top_ranking_url": "asana.com/templates/remote-team-management",
        "current_rank": 2,
        "content_length": 2400,
        "publish_date": "2023-06-15",
        "backlinks": 145
      },
      "backlink_opportunities": [
        {
          "source": "techcrunch.com",
          "domain_authority": 92,
          "traffic_potential": "high",
          "relevance_score": 0.92
        }
      ],
      "semantic_keywords": [
        "remote work collaboration tools",
        "asynchronous project management",
        "distributed team software"
      ]
    },
    {
      "rank": 2,
      "keyword": "asynchronous communication tools for remote teams",
      "search_volume": 890,
      "keyword_difficulty": 22,
      "cpc": "$2.15",
      "commercial_intent": "medium",
      "content_type": "pillar page + 3 cluster articles",
      "estimated_monthly_traffic": 95,
      "ranking_feasibility": "very_high"
    }
  ],
  "gap_analysis": {
    "keywords_you_rank_for": 342,
    "keywords_competitors_rank_for": 1850,
    "unique_competitor_keywords": 1508,
    "exploitable_gaps": 47,
    "low_competition_high_volume": 12
  }
}
```

### Competitor Content Gap Matrix

| Keyword | Vol | Diff | CPC | You | Asana | Monday | Notion | Jira | Opportunity |
|---------|-----|------|-----|-----|-------|--------|--------|------|-------------|
| project management remote teams | 2400 | 28 | $3.20 | — | #2 | #5 | #8 | — | **HIGH** |
| free project management tools | 1800 | 35 | $2.50 | #12 | #1 | #3 | — | #2 | MEDIUM |
| project tracking software | 1200 | 22 | $4.10 | — | #4 | #6 | #9 | #1 | **HIGH** |
| task management for teams | 950 | 18 | $2.80 | #15 | #2 | #1 | #4 | — | LOW |

---

## Tips & Best Practices

### 1. Niche Selection is Critical
- **Be specific**: "Project management" is too broad. "Project management for remote SaaS teams" is ideal.
- **Use long-tail keywords**: Focus on 3-5 word phrases where you can realistically rank.
- **Validate market demand**: Ensure your chosen keywords have 100+ monthly searches and actual commercial intent.

### 2. Prioritize by Feasibility Score
- **Quick wins**: Keywords with difficulty <25 and your domain authority within 5 points of top-ranking competitors
- **Medium-term goals**: Keywords 25-40 difficulty; requires 4-8 weeks of content + link building
- **Long-term plays**: Keywords >40 difficulty; invest only if search volume justifies 6+ month effort

### 3. Content Cluster Strategy
- **Create pillar pages** for broad keywords (e.g., "Project Management Tools")
- **Add cluster content** for specific long-tail variations (e.g., "Best PM Tools for Startups," "PM Tools for Nonprofits")
- **Internal link strategically**: Pillar → Cluster → Pillar creates topical authority

### 4. Backlink Leverage
- **Prioritize content** where you've identified 5+ high-quality backlink sources
- **Reach out proactively**: Use the identified backlink opportunities to pitch your superior content
- **Create link-worthy assets**: Original research, data visualizations, and case studies earn links naturally

### 5. Timing & Trend Analysis
- **Watch search trends**: Keywords marked "rising" often indicate emerging opportunities
- **Publish strategically**: Publish when competitors' content is >6 months old (signals freshness to Google)
- **Update competitor content**: Improve on existing ranking content with newer data, better structure, multimedia

### 6. Validation Before Publishing
- **Verify search intent**: Read top 10 ranking results to ensure your content angle matches user expectations
- **Check SERP features**: Are there featured snippets, People Also Ask, or video results? Optimize for these
- **Analyze backlink profiles**: Ensure you can realistically build links for this keyword

---

## Safety & Guardrails

### What This Skill Will NOT Do

- **Does not guarantee rankings**: Keyword research is one component of SEO success. Content quality, link building, and technical SEO are equally critical.
- **Does not automatically publish content**: All recommendations require human review, editing, and strategic approval before publication.
- **Does not scrape competitor sites directly**: Uses only legitimate APIs (Semrush, Ahrefs, Google Search Console). Respects robots.txt and terms of service.
- **Does not create content**: Generates outlines, keyword clusters, and opportunity lists. You must create original, valuable content.
- **Does not perform black-hat SEO**: Will not recommend keyword stuffing, cloaking, private link networks, or other Google-violating tactics.

### Limitations & Boundaries

- **API rate limits**: Semrush and Ahrefs have monthly query limits. Comprehensive analysis of 20+ competitors may require higher-tier API plans.
- **Data freshness**: Competitor keyword data updates weekly (not real-time). Recent ranking changes may not be reflected immediately.
- **Local SEO limitations**: Works best for national/international niches. Local SEO requires additional Google Maps and local citation analysis.
- **Niche maturity**: Works best in established niches with 50+ competitors. Emerging niches have limited comparative data.
- **Language support**: Currently optimized for English. Other languages require manual configuration.

### Ethical Considerations

- **Respect competitor intellectual property**: Use competitive insights to inform strategy, not to copy content.
- **Create original value**: Every piece of content should provide unique insights, data, or perspectives beyond what competitors offer.
- **Transparent sourcing**: Cite competitor data and research appropriately; don't plagiarize.

---

## Troubleshooting

### Common Issues & Solutions

#### Issue: "API Key Invalid" or "Authentication Failed"
**Solution:**
- Verify API keys are correctly set in your environment variables
- Check that API keys have appropriate permissions/scopes enabled
- For Google Search Console, ensure the service account has "Read" access to your property
- Test API connectivity: `curl -H "Authorization: Bearer YOUR_KEY" https://api.semrush.com/v3/`

#### Issue: "No Data Returned" for Competitors
**Solution:**
- Ensure competitor domains are valid and indexed by Semrush/Ahrefs
- Check that competitors are in the same niche (e.g., don't mix SaaS with e-commerce)
- Verify domains don't have robots.txt restrictions blocking data collection
- Try with top-ranking competitors first (Asana, Monday.com) to validate setup

#### Issue: Keyword Difficulty Scores Seem Inaccurate
**Solution:**
- Keyword difficulty varies by tool (Semrush vs. Ahrefs). Use the same source for consistent comparison.
- Consider your domain authority: a DA 40 site ranks easier for "difficulty 35" keywords than a DA 20 site
- Check SERP features: keywords with featured snippets or local packs may be harder than difficulty scores suggest

#### Issue: Too Many Opportunities Generated (Analysis Paralysis)
**Solution:**
- Filter by commercial intent: "high" intent keywords convert better than informational
- Sort by feasibility score: focus on keywords where your DA is within 5 points of top competitors
- Start with top 10-15 opportunities, not all 50
- Batch content creation: plan 3-5 pieces per month rather than rushing 20

#### Issue: Backlink Opportunities Show Competitors' Links Only
**Solution:**
- This is expected. Use "Backlink Opportunities" as research only—reach out to these sites with *better* content
- Look for "Broken Link" and "Resource Page" opportunities where you can suggest your content as a replacement
- Check competitor link sources for relevance to your niche before outreach

### FAQ

**Q: How often should I run this analysis?**
A: Monthly for competitive niches, quarterly for stable niches. Run ad-hoc when entering new sub-niches or after major competitor content launches.

**Q: Can I use this for local SEO?**
A: Partially. This skill works for service-based local businesses (e.g., "digital marketing agency Austin"). For pure local SEO, supplement with Google Maps and local citation analysis.

**Q: What's the minimum domain authority to rank for these opportunities?**
A: Generally, your DA should be within 5-10 points of current top-ranking competitors. DA 20 can rank for keywords where competitors' DA is 25-35.

**Q: How long does analysis take?**
A: Quick analysis (5 competitors): 2-3 minutes. Comprehensive (20 competitors): 5-10 minutes. Time depends on API response rates.

**Q: Can I export results to WordPress or Google Sheets?**
A: Yes. Set `output_format: "google_sheets"` or `"wordpress"` in configuration. Results integrate directly with your editorial calendar.

**Q