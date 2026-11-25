---
name: dead-link-recovery-authority-redirector
description: "Audit broken links across your website, identify high-traffic ones, find authoritative replacements, and generate SEO-optimized redirect maps. Use when the user needs link recovery, traffic preservation, or site authority improvement."
version: 1.0.0
homepage: https://github.com/ncreighton/empire-skills
metadata:
  {
    "openclaw": {
      "requires": {
        "env": ["SEMRUSH_API_KEY", "AHREFS_API_KEY", "GOOGLE_SEARCH_CONSOLE_TOKEN"],
        "bins": ["curl", "jq"]
      },
      "os": ["macos", "linux", "win32"],
      "files": ["SKILL.md"],
      "emoji": "🔗"
    }
  }
---

# Dead Link Recovery & Authority Redirector

## Overview

This skill automatically scans your entire website for broken internal and external links, prioritizes them by traffic impact and backlink authority, discovers high-authority replacement URLs on the same topic, and generates production-ready redirect mappings with SEO-optimized anchor text suggestions.

**Why This Matters:** Broken links cause user friction, destroy domain authority signals, and waste the SEO value of your existing backlinks. A single high-traffic broken link can cost thousands in organic traffic. This skill recovers that value systematically.

**Integrations:** Works with WordPress (via REST API), Drupal, static site generators, Google Search Console (traffic data), Semrush (backlink analysis), Ahrefs (authority scoring), Google Analytics (user behavior), and Slack (reporting).

### The Problem
- Your website has 50-500+ broken links you don't know about
- Those links receive legitimate traffic and backlinks
- Every broken link signals poor maintenance to Google
- Manual recovery takes 40+ hours per site
- Wrong redirects destroy SEO value permanently

### The Solution
Automated end-to-end recovery: find → prioritize → replace → redirect → monitor

---

## Quick Start

### Example 1: Full Site Audit with Traffic Prioritization
```
Audit my website at example.com for all broken links. 
Cross-reference with Google Search Console to find which 
broken links have traffic, then identify the top 5 by backlink 
authority using Ahrefs. Generate redirect mappings with anchor 
text suggestions for WordPress native redirects plugin.
```

### Example 2: External Link Recovery (Category-Specific)
```
Scan my blog for broken external links in the "AI Tools" 
category only. For each broken link, find the current best 
authority resource (same topic, newer), and generate a CSV 
mapping with 301 redirect instructions. Include domain authority 
score and traffic potential for each replacement.
```

### Example 3: Authority Boost + Anchor Text Optimization
```
Find all broken links pointing to outdated "Best Practices" 
guides on my site. Identify which ones have high domain authority 
backlinks using Semrush. Create new internal link targets on my 
updated guide and generate anchor text suggestions that preserve 
SEO value while improving readability.
```

### Example 4: Crisis Recovery (Post-Migration)
```
My website moved domains last month. Crawl both old and new 
domain structures, identify 404 errors on the new domain, and 
auto-generate a .htaccess redirect map for Apache servers. 
Include traffic estimates for each broken URL from Search Console.
```

---

## Capabilities

### 1. Comprehensive Link Auditing
- **Full-site crawling:** Discovers internal and external links automatically
- **Protocol support:** HTTP/HTTPS, checks SSL validity
- **JavaScript rendering:** Handles JS-rendered links (via Playwright/Puppeteer)
- **Sitemap parsing:** Extracts links from XML sitemaps, RSS feeds
- **Navigation mapping:** Builds internal link graph to understand URL relationships
- **Status code capture:** 404, 410, 500, timeouts, redirects, and soft 404s

**Usage Example:**
```
Start a deep crawl of mydomain.com starting from sitemap.xml, 
including all subdomains. Flag pages that return 404, timeout 
after 5 seconds, or show 500 errors. Export results as JSON.
```

### 2. Traffic & Authority Prioritization
- **Google Search Console integration:** Maps broken links to user queries, clicks, impressions
- **Backlink analysis:** Semrush/Ahrefs pulls domain authority, referring domains, link velocity
- **User behavior correlation:** Combines GA4 data (bounce rate, conversions) with link metrics
- **Impact scoring:** Calculates business cost (lost conversions, organic traffic value)
- **Tiered recommendations:** "Critical" (high traffic + high authority), "Important" (one metric high), "Nice to fix"

**Usage Example:**
```
Prioritize the 100 broken links I found by this formula: 
(Search Console traffic × 2) + (Backlink authority score × 1.5). 
Show me the top 20 that are costing me the most SEO value.
```

### 3. Intelligent Replacement Discovery
- **Topic-based matching:** Analyzes broken page content, extracts topics/entities
- **Google Search:** Finds current best resources for the same query
- **Competitor analysis:** Checks where competing sites link instead
- **Authority filtering:** Only recommends sites with DA > 40 (customizable)
- **Content freshness check:** Prioritizes recent articles (< 1 year old)
- **Domain whitelisting:** Option to redirect only to owned properties or vetted sources

**Usage Example:**
```
For my broken link about "AWS Lambda cost optimization," find 
the 3 best current replacement articles from AWS, TechCrunch, 
or my own site. Score by freshness and authority. Return top match.
```

### 4. Redirect Mapping Generation
- **Multiple format exports:** .htaccess, Nginx conf, meta-refresh, 301 JSON, CSV
- **Platform-specific:** WordPress (Redirection plugin JSON), Drupal (URL aliases), Vercel (vercel.json)
- **Bulk import ready:** Direct upload to Redirection plugin, Yoast, RankMath
- **Validation:** Tests redirects before deployment (detects chain redirects, loops)
- **Rollback support:** Generates before/after snapshots for safe deployment

**Usage Example:**
```
Generate a Redirection plugin import file for all 47 broken 
internal links I found. Test each 301 redirect chain to ensure 
it doesn't loop. Include a CSV backup I can import to 
Google Sheets.
```

### 5. SEO-Optimized Anchor Text Suggestions
- **Context preservation:** Analyzes original anchor text, page context
- **Keyword alignment:** Suggests anchors using target keywords from your redirect target
- **Readability:** Generates 3-5 anchor text options (branded, keyword-rich, natural)
- **Internal linking:** Calculates silos and recommends related internal redirects
- **On-page implementation:** Suggests where to add internal links to redirect targets

**Usage Example:**
```
Show me the original anchor text for each broken link, then 
suggest 3 new anchor text options for the replacement page. 
Include keyword difficulty score for each option.
```

---

## Configuration

### Environment Variables (Required)
```bash
# Google Search Console API (OAuth 2.0 token)
export GOOGLE_SEARCH_CONSOLE_TOKEN="ya29.a0..."

# Ahrefs API (for backlink authority)
export AHREFS_API_KEY="your-ahrefs-key"

# Semrush API (for domain authority, alternative to Ahrefs)
export SEMRUSH_API_KEY="your-semrush-key"

# Optional: Slack webhook for notifications
export SLACK_WEBHOOK_URL="https://hooks.slack.com/services/..."

# Optional: WordPress REST API credentials
export WORDPRESS_API_USER="api-user"
export WORDPRESS_API_PASSWORD="application-password"
```

### Configuration Options
```yaml
crawl:
  start_url: "https://example.com"
  follow_sitemap: true
  include_subdomains: false
  exclude_patterns:
    - "/admin/*"
    - "/private/*"
  javascript_render: true
  timeout_seconds: 10
  max_pages: 5000

prioritization:
  authority_weight: 1.5
  traffic_weight: 2.0
  backlink_weight: 1.2
  min_authority_score: 40

replacement:
  search_domains:
    - "owned"  # your own domains
    - "competitors"  # top 5 competitors
    - "google_results"  # top 10 Google results
  min_content_freshness_days: 365
  max_results_per_link: 3

export:
  format: "json"  # json, csv, htaccess, nginx, wordpress-json
  include_anchor_suggestions: true
  include_traffic_data: true
  test_redirects_before_export: true
```

---

## Example Outputs

### Output 1: Prioritized Broken Links Report (JSON)
```json
{
  "audit_summary": {
    "total_links_scanned": 2847,
    "broken_links_found": 127,
    "critical_priority": 8,
    "important_priority": 31,
    "nice_to_fix": 88,
    "estimated_lost_traffic_monthly": 4320,
    "estimated_traffic_value_usd": 12960
  },
  "critical_links": [
    {
      "id": "broken_001",
      "url": "https://example.com/old-guide",
      "status_code": 404,
      "pages_linking_to_it": 12,
      "anchor_texts": ["best practices", "complete guide"],
      "monthly_searches_from_gsc": 220,
      "total_backlinks": 47,
      "referring_domain_authority": 67,
      "priority_score": 94.2,
      "traffic_value_usd": 660,
      "recommended_replacement": {
        "url": "https://example.com/updated-guide-2024",
        "domain_authority": 72,
        "content_freshness": "2024-01-15",
        "relevance_match": "98%",
        "suggested_anchor_texts": [
          "updated best practices guide",
          "2024 best practices",
          "complete guide"
        ]
      },
      "redirect_instruction": {
        "source": "/old-guide",
        "destination": "/updated-guide-2024",
        "status_code": 301,
        "test_result": "PASS"
      }
    }
  ]
}
```

### Output 2: WordPress Redirection Plugin Import (JSON)
```json
{
  "version": "1.0",
  "redirects": [
    {
      "source": "/old-guide",
      "target": "/updated-guide-2024",
      "status": 301,
      "title": "Broken link recovery: Best Practices Guide",
      "priority": "critical"
    },
    {
      "source": "/products/discontinued-item",
      "target": "/products/alternative-item",
      "status": 301,
      "priority": "important"
    }
  ],
  "import_instructions": "Copy this JSON, go to Tools > Redirection, click 'Bulk Import', paste content."
}
```

### Output 3: Anchor Text Optimization Suggestions (CSV)
```csv
broken_url,original_anchor_text,new_target_url,suggested_anchor_1,suggested_anchor_2,suggested_anchor_3,keyword_difficulty
/old-guide,best practices,/updated-guide-2024,2024 best practices guide,complete best practices,best practices for beginners,23
/products/old,click here,/products/new,shop new item,view alternatives,new product,45
```

---

## Tips & Best Practices

### 1. Audit Frequency
- Run full audits **monthly** on content-heavy sites (50+ pages/week)
- Run **quarterly** on stable sites (< 10 changes/week)
- Run **immediately** after major migrations or redesigns
- Monitor critical links **weekly** using alerts

### 2. Redirect Chain Prevention
- Always test generated redirects before bulk deployment
- Use the validation tool to catch A→B→C chains (should be A→C directly)
- Avoid 302 (temporary) redirects for permanent changes; always use 301
- Check old domain still exists before migrating off-platform redirects

### 3. Authority Matching
- **Internal redirects:** Prefer redirecting to your own high-authority pages when possible
- **External redirects:** Match authority level (DA 50+ to DA 50+) to preserve Google's authority transfer
- **Competitor links:** Review competitor replacements before committing—they may not be permanent either
- **Orphaned content:** Create new pages for high-traffic broken links if no good replacements exist

### 4. Anchor Text Optimization
- Use **keyword-rich anchors** for traffic-generating links (SEO value)
- Use **branded anchors** for user experience (avoid keyword stuffing)
- Match anchor to page context (don't suggest "AI tools" anchor for general reference)
- Review historical anchor text patterns to maintain consistency with backlinks

### 5. Slack Notifications
Configure real-time alerts:
```
For every broken link with traffic > 100/month OR backlinks > 20,
send a Slack notification to #seo-team with:
- URL, current status, traffic impact, priority score
- Recommended replacement with authority score
- 1-click button to "Approve Redirect"
```

### 6. Integration with WordPress SEO Plugins
- **Yoast SEO:** Exports compatibility with Yoast redirect manager
- **RankMath:** Direct import into RankMath Console
- **All in One SEO:** Standard WordPress redirection APIs
- **Redirection Plugin:** JSON format automatically formatted for bulk import

### 7. Monitoring Post-Redirect
- Track 404 rates for 30 days after redirect deployment (should drop 95%+)
- Monitor ranking changes for affected keywords (should stabilize within 2 weeks)
- Check Google Search Console for "Not Found (404)" errors post-recovery
- Set monthly alerts on critical redirect targets to catch future breakage

---

## Safety & Guardrails

### What This Skill Will NOT Do

1. **Blindly redirect without validation**
   - ❌ Will NOT create redirects to spam/malware sites
   - ✅ Only recommends sites with domain authority > 40 (configurable) and passing safety checks
   - ✅ Validates SSL certificates and content match before suggesting

2. **Modify your site without approval**
   - ❌ Will NOT deploy redirects directly to your server
   - ✅ Generates export files ONLY—requires manual import or explicit API permission
   - ✅ All redirects are staged and tested before delivery

3. **Redirect to competitor sites automatically**
   - ❌ Will NOT prioritize external redirects over internal options
   - ✅ Suggests internal replacements first, external only if no internal match exists
   - ✅ Requires explicit whitelist approval for external domains

4. **Preserve broken affiliate/referral links**
   - ❌ Will flag (but ask before modifying) affiliate URLs in detected broken links
   - ✅ Requires confirmation if replacement removes commission/tracking parameters
   - ✅ Preserves UTM parameters and tracking IDs in redirects when possible

5. **Break API contracts or webhook URLs**
   - ❌ Will NOT redirect API endpoints or webhook URLs detected in code
   - ✅ Excludes /api/*, /webhook/*, /callback/* from redirect suggestions
   - ✅ Flags these separately as "technical broken links" requiring developer review

6. **Handle auth-required or user-specific content**
   - ❌ Will NOT crawl password-protected or login-required areas
   - ✅ Requires manual whitelist of authenticated URLs
   - ✅ Skips personalized/dynamic content that varies by user

### Limitations

- **Large sites (>50k pages):** Consider breaking crawl into sections; full crawl may take 6-12 hours
- **JavaScript-heavy sites:** Rendering adds 30-50% to crawl time; consider disabling for initial pass
- **Third-party CDN links:** May show false positives if CDN enforces referrer policies
- **Rate limiting:** Respects robots.txt; crawl speed set to 1 request/second to avoid server strain
- **API quotas:** Google Search Console free tier limited to 3 queries/sec; upgrade for faster audits

---

## Troubleshooting

### Issue: "API key not found" error
**Solution:**