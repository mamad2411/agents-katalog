---
name: seo-research
description: Research keyword competitors, analyse on-page factors, and create optimization plans. Use when user asks to "research SEO competitors", "analyse keyword competition", "reverse engineer rankings", "SEO competitor analysis", or mentions "competitor analysis for [keyword]". Also triggers for requests to understand why competitors rank, on-page SEO audits, or creating content optimization plans.
user-invocable: true
---

# SEO Research Skill

Automated competitor research and on-page analysis for SEO optimization. Analyses what's ranking, reverse-engineers their success factors, and creates actionable optimization plans with word count targets.

## Key Features

- **Multi-keyword support** - Process multiple keywords in one run
- **Automated competitor filtering** - Removes directories/nationals for local SEO
- **Comprehensive on-page analysis** - Title, meta, headings, schema, content, performance
- **Word count guidance** - Total and per-section recommendations
- **Sub-agent architecture** - Preserves context window during heavy processing

## Input Requirements

Extract from user request or ask if not provided:

| Parameter | Required | Default | Description |
|-----------|----------|---------|-------------|
| keywords | Yes | - | Array of target keywords |
| business_type | Yes | local | `local`, `national`, or `any` |
| location | No | United Kingdom | Location for SERP data |
| client_url | No | - | URL being optimised (for gap analysis) |

**Example inputs:**
```
Keywords: ["boiler repair dartford", "emergency plumber dartford"]
Business type: local
Location: United Kingdom
```

## Orchestration Architecture

Use the Task tool with `subagent_type="general-purpose"` to delegate data-heavy operations. This keeps raw API responses out of the main context.

```
Main Orchestrator
     │
     ├─→ SERP Agents (parallel per keyword)
     │        └─→ Returns: Structured SERP data
     │
     ├─→ Classification Agent (sequential)
     │        └─→ Returns: Filtered competitor list
     │
     ├─→ Analysis Agents (3 parallel batches)
     │        └─→ Returns: Structured on-page data
     │
     └─→ Report Agent (sequential)
              └─→ Returns: Final markdown report
```

## Phase 1: SERP Data Collection

Launch SERP agents in parallel (up to 5 keywords simultaneously).

### SERP Agent Prompt Template

```
You are a SERP data collection agent. Your task is to collect search results for a keyword and return ONLY structured data.

**Keyword:** [KEYWORD]
**Location:** [LOCATION]
**Language:** en

**Instructions:**
1. Use `mcp__dataforseo__api_request` with:
   - method: "POST"
   - path: "/v3/serp/google/organic/live/advanced"
   - data: [{ keyword: "[KEYWORD]", location_name: "[LOCATION]", language_code: "en", device: "desktop", depth: 10, people_also_ask_click_depth: 2 }]
   - noAiMode: true

2. Extract and return ONLY this JSON structure (no other text):

```json
{
  "keyword": "[KEYWORD]",
  "location": "[LOCATION]",
  "results": [
    {
      "position": 1,
      "url": "https://example.com/page",
      "domain": "example.com",
      "title": "Page Title as shown in SERP",
      "description": "Meta description as shown in SERP"
    }
  ],
  "paa_questions": [
    "Question 1 from People Also Ask",
    "Question 2 from People Also Ask"
  ],
  "serp_features": {
    "featured_snippet": true/false,
    "local_pack": true/false,
    "knowledge_panel": true/false
  },
  "related_searches": ["related term 1", "related term 2"]
}
```

Do NOT include raw API responses. Extract only the structured data above.
```

### Launching SERP Agents

For each keyword, launch a Task agent in parallel:

```
Task tool parameters:
- subagent_type: "general-purpose"
- description: "SERP collection: [keyword]"
- prompt: [SERP Agent Prompt with keyword/location substituted]
```

Collect all results before proceeding to Phase 2.

## Phase 2: Competitor Classification

After collecting all SERP data, run classification to filter results.

### Classification Agent Prompt Template

```
You are a competitor classification agent. Your task is to filter SERP results to identify direct competitors.

**Business Type:** [BUSINESS_TYPE]
**SERP Data:** [JSON from Phase 1]

**Classification Rules:**

When business_type = "local":

INCLUDE (Direct Competitors):
- Local/regional businesses in the same trade
- Independent practitioners and tradespeople
- Small to medium businesses serving the target area
- Signals: Local phone numbers, single location, "Serving [Area]" language

EXCLUDE:
1. **Directories & Aggregators:**
   - checkatrade.com, ratedpeople.com, mybuilder.com, bark.com
   - yell.com, yelp.co.uk, thomsonlocal.com, freeindex.co.uk
   - trustpilot.com (business listing pages)
   - URL patterns: /find-a-trader/, /business-directory/, /local-services/
   - Title patterns: "10 Best...", "Top Rated...", "Find a..."

2. **National Chains:**
   - British Gas, HomeServe, Dyno-Rod, Pimlico Plumbers (national scale)
   - Signals: 0800/0333 numbers, "Find your local branch", franchise structure

3. **Lead Generation Sites:**
   - Sites primarily collecting quotes/leads
   - "Get 3 Free Quotes" prominence

4. **Informational Content:**
   - Wikipedia, Reddit, Mumsnet, DIYnot forums
   - News articles, how-to guides from publications
   - Government/council websites

5. **E-commerce:**
   - Amazon, eBay listings
   - Large retailer category pages

When business_type = "national" or "any":
- Include all commercial competitors
- Still exclude pure directories and informational content

**Return ONLY this JSON structure:**

```json
{
  "included_competitors": [
    {
      "position": 1,
      "url": "https://example.com",
      "domain": "example.com",
      "title": "Title",
      "classification": "local_business",
      "reason": "Single-location plumber serving Dartford area"
    }
  ],
  "excluded_results": [
    {
      "position": 2,
      "url": "https://checkatrade.com/...",
      "domain": "checkatrade.com",
      "classification": "directory",
      "reason": "Trade directory - auto-excluded"
    }
  ],
  "competitor_count": 6,
  "excluded_count": 4
}
```
```

### Launching Classification Agent

```
Task tool parameters:
- subagent_type: "general-purpose"
- description: "Classify competitors"
- prompt: [Classification Agent Prompt with business_type and SERP data]
```

## Phase 3: On-Page Analysis

Analyse each competitor in parallel batches of 3.

### Analysis Agent Prompt Template

```
You are an on-page SEO analysis agent. Your task is to analyse a competitor page and return structured data.

**URL to Analyse:** [URL]
**Target Keyword:** [KEYWORD]

**Instructions:**

1. Use `mcp__dataforseo__api_request` with:
   - method: "POST"
   - path: "/v3/on_page/task_post"
   - data: [{ target: "[URL]", max_crawl_pages: 1, enable_content_parsing: true }]
   - noAiMode: true

   After the crawl completes, capture its task id and use the same tool with path
   `/v3/on_page/content_parsing` and data `[{ id: "[TASK_ID]", url: "[URL]" }]`.

2. Use the same tool with:
   - method: "POST"
   - path: "/v3/on_page/lighthouse/live/json"
   - data: [{ url: "[URL]" }]
   - noAiMode: true

3. If content parsing fails, fallback to `mcp__apify__apify-slash-rag-web-browser` with:
   - query: "[URL]"
   - maxResults: 1
   - outputFormats: ["markdown"]

**Extract and calculate:**

- Title tag: exact text, character count, keyword presence
- Meta description: exact text, character count
- H1: exact text (should be only 1)
- H2s: list all H2 headings
- H3 count
- Total word count (visible text)
- Section word counts: words between each H2 heading
- Schema types found (LocalBusiness, FAQ, Review, etc.)
- Internal link count
- Image count and alt text coverage
- Performance score from Lighthouse
- Core Web Vitals (LCP, CLS)
- Trust signals: phone visible, address visible, testimonials present, accreditations

**Return ONLY this JSON structure:**

```json
{
  "url": "[URL]",
  "domain": "[DOMAIN]",
  "title": {
    "text": "Exact title tag text",
    "length": 55,
    "keyword_present": true,
    "keyword_position": "start"
  },
  "meta": {
    "text": "Exact meta description",
    "length": 150,
    "keyword_present": true
  },
  "headings": {
    "h1": ["Main H1 Text"],
    "h2": ["H2 Section 1", "H2 Section 2", "H2 Section 3"],
    "h3_count": 8
  },
  "content": {
    "total_word_count": 1850,
    "section_word_counts": {
      "H2 Section 1": 350,
      "H2 Section 2": 420,
      "H2 Section 3": 380
    },
    "paragraph_count": 24,
    "has_lists": true,
    "has_tables": false
  },
  "schema": {
    "types_found": ["LocalBusiness", "FAQ"],
    "local_business_complete": true,
    "has_reviews": true,
    "review_count": 47,
    "average_rating": 4.8
  },
  "links": {
    "internal_count": 12,
    "external_count": 3,
    "has_contact_link": true
  },
  "images": {
    "count": 8,
    "with_alt_text": 6,
    "alt_coverage_percent": 75
  },
  "performance": {
    "score": 85,
    "lcp_seconds": 2.1,
    "cls": 0.05,
    "fcp_seconds": 1.2,
    "mobile_friendly": true
  },
  "trust_signals": {
    "phone_visible": true,
    "phone_clickable": true,
    "address_visible": true,
    "testimonials_present": true,
    "testimonial_count": 5,
    "accreditations": ["Gas Safe", "Which? Trusted Trader"],
    "years_in_business_mentioned": true
  },
  "key_strengths": [
    "Strong local schema markup",
    "High review count (47) with 4.8 rating",
    "Comprehensive service descriptions"
  ],
  "gaps": [
    "Missing FAQ schema",
    "Only 75% alt text coverage",
    "No breadcrumb navigation"
  ]
}
```

If any tool fails, note it in the response and continue with available data.
```

### Launching Analysis Agents

Launch 3 agents in parallel, wait for completion, then launch next batch:

```
Task tool parameters:
- subagent_type: "general-purpose"
- description: "Analyse: [domain]"
- prompt: [Analysis Agent Prompt with URL and keyword]
```

## Phase 4: Report Generation

After all analysis is complete, generate the final report.

### Report Agent Prompt Template

```
You are a report generation agent. Create a comprehensive SEO competitor analysis report with actionable recommendations.

**Input Data:**
- Keywords analysed: [KEYWORDS]
- Business type: [BUSINESS_TYPE]
- Location: [LOCATION]
- Client URL (if provided): [CLIENT_URL]
- SERP data: [SERP_JSON]
- Classification results: [CLASSIFICATION_JSON]
- Competitor analyses: [ANALYSES_JSON]

**Generate two outputs:**

## OUTPUT 1: Full Markdown Report

Use the template from `references/report-templates.md`:
- Executive summary (2-3 sentences)
- SERP overview with rankings table
- Per-competitor detailed analysis
- Aggregate insights (averages, patterns)
- Recommendations prioritised by impact

## OUTPUT 2: Content Plan with Word Counts

Calculate target word counts:
- Total target = Competitor average + 15% (rounded to nearest 50)
- Per-section targets based on competitor section analysis
- Identify sections competitors commonly use

Format as:

```markdown
## Content Plan for "[KEYWORD]"

**Total Target Word Count:** [X] words
(Based on competitor average of [Y] + 15%)

### Suggested Structure:

| Section | H Level | Target Words | Topics to Cover |
|---------|---------|--------------|-----------------|
| [Section Name] | H2 | 300-400 | [Topics from analysis] |
| [Subsection] | H3 | 150-200 | [Specific points] |

### Must-Answer Questions (from PAA):
1. [Question 1]
2. [Question 2]
3. [Question 3]

### Schema Requirements:
- LocalBusiness (all fields)
- FAQ (for questions section)
- [Other based on competitor usage]

### Technical Targets:
- Performance score: [competitor avg]+
- LCP: <2.5s
- CLS: <0.1
```

## OUTPUT 3: Actionable Checklist

Create implementation checklist with specific targets derived from competitor analysis.

Return the complete report as markdown. Do not truncate.
```

### Launching Report Agent

```
Task tool parameters:
- subagent_type: "general-purpose"
- description: "Generate SEO report"
- prompt: [Report Agent Prompt with all collected data]
```

## Error Handling

All errors are handled silently to maintain automation:

| Error | Recovery Action |
|-------|-----------------|
| SERP returns no results | Note in report, suggest keyword variations |
| Page parsing fails | Fallback to Apify, then skip with note |
| Lighthouse times out | Skip technical metrics, note in report |
| Agent fails | Log error, continue with remaining data |

**Note:** Ask for required inputs (keywords) BEFORE starting execution. Once the workflow begins, never prompt the user - log issues and continue.

## Integration with Other Skills

After generating the report, suggest:

- **seo-copywriting skill** - To write optimised content based on the analysis
- **generate-image skill** - To create supporting images

## Reference Files

For detailed criteria and templates, see:

- `references/competitor-classification.md` - Full classification rules and domain lists
- `references/analysis-factors.md` - Complete on-page factor checklist
- `references/report-templates.md` - Report and checklist templates
- `references/tool-reference.md` - DataForSEO/Apify tool parameters

## Quick Start

When `/seo-research` is invoked:

1. **Check for required keywords in the user's message**
   - If user provided keywords (e.g., "/seo-research for boiler repair dartford"), extract them
   - If NO keywords provided, **ASK the user** using AskUserQuestion tool:
     - "What keyword(s) do you want to research?"
     - "What type of business is this for?" (local/national/any)
     - "Any specific location?" (default: United Kingdom)

2. Apply defaults ONLY for optional parameters:
   - business_type → "local" if not specified
   - location → "United Kingdom" if not specified
   - **keywords have NO default - must be provided by user**

3. Once keywords confirmed, run automated workflow:
   - Launch SERP agents in parallel
   - Run classification on collected data
   - Launch analysis agents in batches of 3
   - Generate final report with word count recommendations

4. Present report to user
5. Suggest next steps (seo-copywriting skill)

**Important:** Never assume or invent keywords. Always confirm with user if not explicitly provided.
