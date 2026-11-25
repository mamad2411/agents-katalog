---
name: expired-domain-finder
description: Find and evaluate expired domains for niche SEO projects using scraping and SEO metrics enrichment.
---

# Expired Domain Finder for PBN Building

Find high-quality expired domains for Private Blog Networks (PBNs) using automated scraping and SEO metrics enrichment.

## Trigger Phrases

- "find expired domains"
- "expired domain finder"
- "pbn domains"
- "find domains for [niche]"
- "search expired domains [niche]"

## Overview

This skill automates the discovery and evaluation of expired domains suitable for PBN building. It combines domain discovery via Apify scrapers with detailed SEO metrics from DataForSEO to identify high-quality expired domains with clean backlink profiles.

## Input Requirements

### Required Input
- **Niche/Industry**: The target niche or industry for domain relevance (e.g., "heating", "plumbing", "electrical")

### Optional Inputs (defaults provided)
- **TLD Filter**: Default `.co.uk` (can be modified to `.com`, `.org`, etc.)
- **Minimum DR**: Default `5`
- **Minimum Referring Domains**: Default `5`
- **Max Results**: Default `100` domains to check

## Workflow Steps

### Step 1: Input Collection

If the user hasn't provided a niche in their trigger phrase:

```
Ask: "What niche or industry are you targeting? (e.g., heating, plumbing, electrical, roofing)"
```

Optional follow-up:
```
"Would you like to customize the filters? Current defaults:
- TLD: .co.uk
- Minimum DR: 5
- Minimum Referring Domains: 5
- Max Results: 100

Reply with 'yes' to customize or 'continue' to use defaults."
```

### Step 2: Keyword Preparation

Load keyword variations from `references/niche-keywords.md` for the specified niche. If the niche isn't in the reference file, use the user's input directly and generate variations:

- Primary keyword
- [keyword] + service
- [keyword] + repair
- [keyword] + contractor
- [keyword] + installation

### Step 3: Domain Discovery (Apify MCP)

Use Apify to find expired domains:

**Tool Sequence:**

1. **Search for the scraper**:
```
Tool: mcp__apify__search-actors
Query: "expireddomains.net scraper" or "expired domains"
```

2. **Call the actor**:
```
Tool: mcp__apify__call-actor
Actor ID: [from search results]
Input: {
  "keyword": "[niche keyword from step 2]",
  "tld": "co.uk",
  "minBacklinks": 5,
  "maxResults": 100,
  "includeDeleted": true,
  "includePending": true
}
```

3. **Retrieve results**:
```
Tool: mcp__apify__get-actor-output
Run ID: [from previous call]
```

**Fallback Strategy** (if no results):
1. Retry with broader keyword (remove qualifiers)
2. Expand TLD filter to include `.com`
3. Lower `minBacklinks` to `1`
4. Try alternative keywords from niche list
5. If still no results, inform user and suggest manual search on expireddomains.net

### Step 4: Domain Enrichment (DataForSEO MCP)

For each domain discovered, fetch detailed metrics:

**Primary Tool:**
```
Tool: mcp__dataforseo__api_request
Request: {
  "method": "POST",
  "path": "/v3/backlinks/summary/live",
  "data": [{
    "target": "[domain]",
    "include_subdomains": false
  }],
  "noAiMode": true
}
```

**Extract these metrics:**
- Domain Rating (DR) / Domain Authority (DA)
- Total referring domains
- Total backlinks
- Domain age (first seen date)
- Follow vs. nofollow ratio

**Additional enrichment (if needed):**
```
Tool: mcp__dataforseo__api_request
Request: {
  "method": "POST",
  "path": "/v3/backlinks/anchors/live",
  "data": [{
    "target": "[domain]",
    "limit": 100
  }],
  "noAiMode": true
}
```

**Extract:**
- Top anchor texts
- Anchor text distribution
- Spam anchor detection

**Rate Limiting:**
- Process domains in batches of 20
- Add 1-second delay between batches to respect API limits

**Fallback Handling:**
- If DataForSEO fails for a domain: Mark as "metrics unavailable" in output
- If rate limited: Pause for 5 seconds and retry
- Still include domain in results with available data

### Step 5: Domain Scoring

Apply scoring criteria from `references/domain-scoring.md` to each domain:

**Scoring Process:**

1. Start with base score: **50 points**

2. **Add points for positive factors:**
   - Domain age evaluation
   - DR/DA evaluation  
   - Referring domains count
   - Anchor text quality
   - Niche relevance
   - TLD bonus

3. **Subtract points for red flags:**
   - Spammy anchors (check against red flag keywords)
   - PBN footprint indicators
   - Suspicious backlink patterns
   - Foreign language spam
   - Thin backlink profile

4. **Flag critical issues:**
   - Check anchors against red flag keyword list
   - Note any domains with score < 40 as "Poor - Not recommended"

5. **Calculate final score** (0-100 scale)

**Red Flag Detection:**

Scan anchor texts for these patterns:
- Casino/gambling keywords
- Pharmaceutical keywords
- Adult content keywords
- Payday loan keywords
- Foreign spam patterns

### Step 6: Output Generation

Create two outputs:

#### A. CSV File Export

Generate CSV with these columns:

| Column | Description |
|--------|-------------|
| domain | Domain name |
| score | Calculated quality score (0-100) |
| rating | Excellent/Good/Fair/Poor |
| dr | Domain Rating |
| referring_domains | Count of unique referring domains |
| total_backlinks | Total backlink count |
| domain_age_years | Approximate age in years |
| top_anchors | Top 5 anchor texts (comma-separated) |
| red_flags | List of detected issues |
| niche_relevant | Yes/No based on keyword match |
| namecheap_link | Direct registration link |

**Namecheap Link Format:**
```
https://www.namecheap.com/domains/registration/results/?domain={domain}
```

**File Location:**
Save to: `/Users/georgelane/.Codex/scratchpad/expired-domains-[niche]-[timestamp].csv`

#### B. Console Summary

Display summary for user:

```
Found [X] expired domains for [niche]

Top 10 Recommendations:
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

1. example-domain.co.uk (Score: 87 - Excellent)
   DR: 25 | RDs: 45 | Age: 12 years
   Top Anchors: brand name, naked URL, click here
   ✓ Clean backlink profile
   Register: https://namecheap.com/...

2. another-domain.co.uk (Score: 78 - Good)
   DR: 18 | RDs: 32 | Age: 8 years
   Top Anchors: service name, website, visit
   ⚠ Minor: 15% foreign anchors
   Register: https://namecheap.com/...

[... continue for top 10]

Full results saved to: /Users/georgelane/.Codex/scratchpad/expired-domains-[niche]-[timestamp].csv

Summary Statistics:
- Total domains checked: [X]
- Excellent (80+): [X]
- Good (60-79): [X]
- Fair (40-59): [X]
- Poor (<40): [X]
```

### Step 7: User Follow-up

After presenting results:

```
Would you like me to:
1. Check availability for top domains?
2. Get more detailed backlink analysis for specific domains?
3. Search for additional domains with different filters?
4. Export to a different format?
```

## Error Handling & Fallbacks

### Apify Actor Not Found
```
Manual fallback instructions:
1. Visit expireddomains.net manually
2. Use filters: TLD=.co.uk, Min Backlinks=5
3. Search for niche keywords
4. Export results
5. Share the list and I'll run DataForSEO enrichment
```

### DataForSEO API Errors
- **Rate Limited**: Pause processing, wait 10 seconds, resume
- **Domain Not Found**: Mark as "new domain - no history" (score penalty)
- **Invalid Response**: Skip domain, log error, continue with next
- **API Down**: Offer to save domain list for later enrichment

### No Qualifying Domains Found
```
No domains met the minimum criteria (score ≥ 40).

Suggestions:
1. Broaden keyword search (try related terms)
2. Lower minimum DR requirement
3. Expand TLD filter to include .com
4. Consider domains with scores 30-39 (review manually)

Would you like me to try again with relaxed criteria?
```

### Low Result Count (< 5 domains)
```
Only found [X] qualifying domains. This might indicate:
- Very competitive niche
- Strict filtering criteria
- Limited expired domain availability

Recommendations:
1. Check again in 1-2 weeks (new domains expire daily)
2. Expand search to related niches
3. Consider alternative TLDs

Would you like to see the available domains anyway?
```

## Example MCP Tool Calls

### Finding Apify Scraper

```typescript
// Step 1: Search for the actor
mcp__apify__search-actors({
  query: "expireddomains.net scraper"
})

// Response example:
// [
//   {
//     id: "username/expireddomains-scraper",
//     name: "Expired Domains Scraper",
//     description: "Scrapes expireddomains.net for expired domains"
//   }
// ]
```

### Running the Scraper

```typescript
// Step 2: Call the actor
mcp__apify__call-actor({
  actorId: "username/expireddomains-scraper",
  input: {
    keyword: "plumber OR plumbing OR drainage",
    tld: "co.uk",
    minBacklinks: 5,
    maxResults: 100,
    includeDeleted: true,
    includePending: true
  },
  waitForFinish: 120 // wait up to 2 minutes
})

// Response: { runId: "abc123..." }
```

### Getting Domain Metrics

```typescript
// Step 3: Enrich with DataForSEO
mcp__dataforseo__api_request({
  method: "POST",
  path: "/v3/backlinks/summary/live",
  data: [{
    target: "example-plumbing.co.uk",
    include_subdomains: false
  }],
  noAiMode: true
})

// Response example:
// {
//   rank: 25,
//   backlinks: 1234,
//   referring_domains: 45,
//   first_seen: "2012-03-15",
//   ...
// }
```

### Getting Anchor Text Analysis

```typescript
mcp__dataforseo__api_request({
  method: "POST",
  path: "/v3/backlinks/anchors/live",
  data: [{
    target: "example-plumbing.co.uk",
    limit: 100,
    order_by: ["backlinks_count,desc"]
  }],
  noAiMode: true
})

// Response example:
// {
//   anchors: [
//     { anchor: "Example Plumbing", backlinks: 450 },
//     { anchor: "example-plumbing.co.uk", backlinks: 320 },
//     { anchor: "click here", backlinks: 89 },
//     ...
//   ]
// }
```

## Reference Files

This skill relies on these reference files:

1. **references/domain-scoring.md**: Detailed scoring criteria and red flag keywords
2. **references/niche-keywords.md**: Pre-defined keyword lists for common niches
3. **references/apify-setup.md**: Apify actor configuration details and troubleshooting

Consult these files during execution for specific scoring rules and keyword variations.

## Best Practices

1. **Always ask for niche confirmation** - Even if provided, confirm understanding
2. **Show progress updates** - Let user know which step you're on (discovery, enrichment, scoring)
3. **Be transparent about API limits** - If hitting rate limits, explain delays
4. **Prioritize quality over quantity** - Better to return 5 excellent domains than 50 poor ones
5. **Include actionable next steps** - Always end with clear options for user
6. **Save all data** - Even low-scoring domains might be useful for future reference

## Success Criteria

A successful run should produce:
- ✓ At least 3 domains with score ≥ 60
- ✓ Complete CSV export with all metrics
- ✓ Clear summary with top recommendations
- ✓ No unhandled errors (fallbacks engaged when needed)
- ✓ Actionable next steps provided to user

## Notes for Future Improvements

- Consider integrating Wayback Machine checks for historical content
- Add bulk domain availability checking via Namecheap API
- Implement domain age verification via WHOIS
- Create scoring model variations for different PBN strategies
- Add competitive analysis (compare to existing PBN domains)
