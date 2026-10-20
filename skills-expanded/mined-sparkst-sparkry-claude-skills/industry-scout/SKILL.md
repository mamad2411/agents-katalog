---
name: Industry Signal Scout
description: Searches for best-of-best sources using Tavily + Web. Filters out noise, SEO spam, AI-generated content. Use for finding canonical, primary, independent evidence.
version: 1.0.0
network: true
dependencies: none
---

# Industry Signal Scout

## Overview

This skill orchestrates intelligent web research to find the highest-quality sources while filtering out the vast sea of noise, SEO spam, and AI-generated content farms that pollute search results.

**When to use this skill:**
- At the beginning of web research phase (after plan is created)
- When searching for canonical documentation or primary sources
- When existing sources need independent corroboration

## The Signal vs Noise Problem

The internet is **90% noise**:
- SEO-optimized content farms
- AI-generated "articles" with no original research
- Duplicate content (same info repackaged)
- Outdated information presented as current
- Marketing disguised as objective analysis

**This skill's purpose:** Cut through the noise to find the **10% signal** - original, authoritative, independently valuable sources.

## Search Strategy

### 1. Query Construction

Transform research sub-questions into targeted queries using these patterns:

**For Market Data:**
- `"market size" "TAM" [industry] [year] site:gartner.com OR site:idc.com`
- `"analyst report" [technology] [year]`
- `sec filing [company] "revenue" "segment"`

**For Technical Information:**
- `site:github.com [project] "official documentation"`
- `site:docs.[vendor].com [feature] specification`
- `"RFC" [protocol] site:ietf.org`

**For Competitive Intelligence:**
- `[competitor] "pricing" OR "plans" -inurl:review`
- `[product] vs [product] comparison -inurl:affiliate`
- `site:reddit.com [tool] "switching from" OR "migrating from"`

**For Customer Insights:**
- `site:reddit.com/r/[community] [tool] "frustration" OR "pain point"`
- `site:news.ycombinator.com [topic] "wish" OR "if only"`
- `"user survey" [industry] [year]`

### 2. Canonical Source Mapping

For each domain, prefer canonical sources:

| Domain | Tier-1 Sources | Tier-2 Sources |
|--------|----------------|----------------|
| **Cloud/AWS** | aws.amazon.com/docs, AWS blog | acloudguru.com, AWS re:Invent talks |
| **AI/ML** | arxiv.org, openai.com/research, anthropic.com/research | HuggingFace blog, Papers with Code |
| **Market Data** | gartner.com, idc.com, census.gov | Statista, CB Insights, PitchBook |
| **Developer Tools** | Official docs, GitHub repos | Stack Overflow, dev.to (with scrutiny) |
| **Business** | sec.gov (EDGAR), company investor relations | WSJ, Bloomberg, FT |
| **Technical Specs** | W3C, IETF RFCs, ISO standards | MDN, caniuse.com |

**Resource:** See `resources/canonical-sources-by-domain.md` for comprehensive mapping

### 3. Noise Filtering

**Auto-exclude patterns:**
- AI content farms: `site:medium.com -author:"verified"` (most Medium is noise)
- Affiliate/review spam: `-inurl:review -inurl:best -inurl:top10`
- Outdated: `after:2024-01-01` for current market queries
- Low-authority: `-site:quora.com -site:answers.yahoo.com`

**Red flags in results:**
- Generic domain names (bestaitools.com, topdevelopertools.net)
- "Powered by AI" disclaimers
- No author attribution
- Duplicate content (same text across multiple sites)
- Publish date missing or suspicious (backdated)

### 4. Quality Signals

**Look for:**
- Named authors with verifiable credentials
- Publication date clearly stated
- Primary data or methodology described
- Citations to other reputable sources
- Domain authority (check domain age, backlink profile)
- Editorial standards (corrections policy, fact-checking process)

## Tool Usage: Tavily vs Brave Search

### Use Tavily (`mcp__tavily__tavily-search`) for:
- **Deep research** (search_depth: "advanced")
- **Recent information** (freshness: "pw" = past week, "pm" = past month)
- **Specific domains** (include_domains: ["gartner.com", "idc.com"])
- **Summary needs** (returns clean, structured data)

**Example:**
```python
tavily_search(
    query="AI coding agents market size 2025",
    search_depth="advanced",
    max_results=10,
    include_domains=["gartner.com", "idc.com", "forrester.com"],
    include_raw_content=True
)
```

### Use Brave Search (`mcp__brave-search__brave_web_search`) for:
- **Broad discovery** (when you don't know which domains to target)
- **News** (use brave_news_search for recent announcements)
- **Parallel to Tavily** (cross-check results, find different sources)

**Example:**
```python
brave_web_search(
    query='"Claude Code" vs Cursor comparison',
    count=20,
    freshness="pm"
)
```

### Parallel Execution Pattern

For maximum signal discovery, run both tools in parallel:

```python
# Parallel execution (pseudo-code)
results_tavily = tavily_search(query, depth="advanced")
results_brave = brave_web_search(query, count=20)

# Merge and deduplicate
all_sources = merge_and_dedupe([results_tavily, results_brave])

# Filter noise
high_quality = filter_by_tier_criteria(all_sources)
```

The `scripts/parallel_search.py` script handles this orchestration.

## Source Extraction Workflow

1. **Execute searches** (parallel Tavily + Brave)
2. **Deduplicate** (same URL, same content hash)
3. **Initial filter** (exclude known noise patterns)
4. **Extract metadata** (title, author, date, excerpt)
5. **Tier classification** (preliminary, based on domain)
6. **Save to sources.json**

Output: `research/sources.json`

```json
{
  "search_date": "2025-10-18T15:00:00Z",
  "queries": [
    {
      "query": "AI coding agents market size 2025",
      "tool": "tavily",
      "results_returned": 10,
      "results_kept": 7
    }
  ],
  "sources": [
    {
      "source_id": "src_001",
      "url": "https://gartner.com/...",
      "title": "Market Guide for AI-Assisted Developer Tools",
      "author": "Gartner Research",
      "publication_date": "2025-06-15",
      "excerpt": "We forecast the market for AI coding agents at $5.2B in 2025...",
      "preliminary_tier": 1,
      "discovery_method": "tavily_advanced",
      "relevance_score": 0.95
    }
  ],
  "summary": {
    "total_results": 45,
    "after_deduplication": 32,
    "after_noise_filter": 18,
    "preliminary_tier1": 4,
    "preliminary_tier2": 9,
    "preliminary_tier3": 5
  }
}
```

## Rate Limiting & Error Handling

**Tavily limits:**
- Free tier: 1,000 requests/month
- Implement exponential backoff for 429 errors

**Brave limits:**
- Check plan-specific limits
- Cache results for repeated queries

**Error handling:**
```python
try:
    results = tavily_search(query)
except RateLimitError:
    # Wait and retry with exponential backoff
    time.sleep(2 ** retry_count)
except NetworkError:
    # Fall back to Brave if Tavily fails
    results = brave_web_search(query)
```

## Quality Metrics

Track search effectiveness:

```json
{
  "search_quality": {
    "queries_executed": 12,
    "avg_tier1_per_query": 0.67,
    "avg_tier2_per_query": 1.5,
    "noise_filtered_percent": 62.3,
    "avg_relevance_score": 0.78
  }
}
```

Goal: **≥50% noise filtered**, **≥0.7 average relevance**

## Anti-Patterns

❌ **Generic queries**: "AI tools" → Returns content farms
✅ **Specific queries**: '"Claude Code" features site:docs.claude.com'

❌ **Accepting first page**: Often SEO-gamed
✅ **Deep search**: Use Tavily advanced, check pages 2-3 of Brave results

❌ **Ignoring dates**: Using 2020 data for 2025 claims
✅ **Freshness filters**: `freshness: "pm"` for current market data

❌ **Single tool**: Missing diverse sources
✅ **Parallel tools**: Tavily + Brave for comprehensive coverage

## Output

After execution, the industry-signal-scout agent creates:
1. `research/sources.json` - All discovered sources with metadata
2. Hands off to source-evaluator for formal tier rating

## References

See `resources/canonical-sources-by-domain.md` for domain-specific Tier-1 sources
See `scripts/parallel_search.py` for parallel execution implementation
