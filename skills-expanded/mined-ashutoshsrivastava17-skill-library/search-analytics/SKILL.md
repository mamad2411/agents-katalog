---
name: search-analytics
description: >
  Analyze enterprise search behavior including query analysis, zero-result
  queries, click-through rates, search refinement patterns, and relevance
  tuning recommendations to continuously improve search quality.
  TRIGGER when: user says /search-analytics, "analyze search logs",
  "search performance", "zero result queries", "search relevance",
  "why can't people find things", or "improve search quality".
argument-hint: "[search system or dataset to analyze]"
user-invocable: true
---

# Search Analytics

You are a search analyst helping organizations understand how users search and where search fails. Analyze search behavior data to produce actionable recommendations that improve findability and relevance.

## Process

### Step 1: Gather Search Data

Identify the data sources and ensure sufficient coverage:

| Data Source | What It Contains | Minimum Period |
|---|---|---|
| Query logs | Raw search terms entered by users | 30 days (90 preferred) |
| Click logs | Which results users clicked after searching | 30 days |
| Session logs | Sequence of searches, clicks, and refinements in a session | 30 days |
| Zero-result logs | Queries that returned no results | 30 days |
| Autocomplete logs | Suggested terms shown and which were selected | 30 days |
| Facet usage logs | Which filters users applied and in what order | 30 days |

**Data quality checklist before analysis:**

| Check | Action |
|---|---|
| Bot traffic excluded | Filter out crawlers, monitoring scripts, API calls |
| Internal test queries removed | Exclude QA and admin searches |
| Personally identifiable information (PII) scrubbed | Anonymize or pseudonymize user IDs |
| Sufficient volume | At least 1,000 queries in the analysis period; fewer requires qualitative analysis instead |
| Timestamps present | Every query and click has a timestamp for session reconstruction |

### Step 2: Analyze Query Patterns

Examine what users search for and how they express their needs:

**Query volume analysis:**

| Metric | How to Calculate | What It Reveals |
|---|---|---|
| Total queries | Count all queries in the period | Overall search demand |
| Unique queries | Count distinct query strings | Vocabulary diversity |
| Queries per session | Total queries / total sessions | How much users refine |
| Top 100 queries | Rank by frequency | What users need most |
| Long-tail distribution | % of queries searched only once | Content coverage challenges |
| Query length distribution | Average and median word count | Search sophistication |

**Query classification framework:**

| Query Type | Definition | Example | Typical % |
|---|---|---|---|
| Known-item | User knows exactly what they want | "Q3 expense report form" | 30-40% |
| Topical | User exploring a subject area | "remote work policy" | 30-40% |
| Navigational | User trying to reach a specific page | "HR portal", "benefits" | 15-20% |
| Re-finding | User searching for something they found before | Same query by same user within 7 days | 10-15% |

**Temporal patterns to examine:**

| Pattern | What to Look For |
|---|---|
| Day of week | Monday spikes (people catching up), Friday dips |
| Time of day | Peaks during work hours; off-hours searches suggest urgent needs |
| Seasonal trends | Open enrollment, fiscal year end, performance review cycles |
| Event-driven spikes | Policy changes, reorgs, tool launches |

### Step 3: Analyze Zero-Result Queries

Zero-result queries are the highest-value signal for search improvement:

| Analysis Step | Action |
|---|---|
| Volume | What percentage of all queries return zero results? (Target: under 5%) |
| Top zero-result queries | Rank by frequency; these are your top priorities |
| Root cause classification | Categorize each using the table below |
| Remediation mapping | Assign a fix action to each root cause |

**Zero-result root cause classification:**

| Root Cause | Description | Fix |
|---|---|---|
| Content gap | The content does not exist | Create the content; add to content roadmap |
| Vocabulary mismatch | Content exists but uses different terms | Add synonyms to the search engine |
| Typo / misspelling | User misspelled the query | Enable spell correction and fuzzy matching |
| Acronym | User searched an acronym not indexed | Add acronym expansion to the search config |
| Format mismatch | Content is in a non-indexed format (PDF, image, video) | Expand indexing to cover the format |
| Access restriction | Content exists but is not in the search index | Verify index coverage; consider showing "restricted" results |
| Stale index | Content was recently added but not yet indexed | Check indexing latency; reduce crawl interval |

### Step 4: Analyze Click-Through and Engagement

Measure whether search results satisfy user intent:

| Metric | Formula | Healthy Range |
|---|---|---|
| Click-through rate (CTR) | Sessions with at least 1 click / total search sessions | 60-80% |
| Mean reciprocal rank (MRR) | Average of (1 / rank of first clicked result) | 0.5-0.8 |
| Clicks at position 1 | Clicks on the first result / total clicks | 40-60% |
| Abandonment rate | Sessions with 0 clicks and no refinement / total sessions | Under 20% |
| Refinement rate | Sessions where user modified their query / total sessions | 15-30% (higher = relevance problem) |
| Short-click rate | Clicks where user returned to results in under 10 seconds / total clicks | Under 15% |
| Long-click rate | Clicks where user stayed on result for 30+ seconds / total clicks | Above 50% |

**Position-based CTR benchmarks:**

| Result Position | Expected CTR |
|---|---|
| 1 | 35-50% |
| 2 | 15-25% |
| 3 | 8-15% |
| 4-5 | 4-8% |
| 6-10 | 1-4% |
| Below 10 | Under 1% |

**Warning signs:**
- Position 1 CTR below 30%: top result is consistently wrong
- High refinement rate (above 40%): initial results are poor
- High abandonment rate (above 30%): users give up on search
- Short-click rate above 25%: results look relevant but are not

### Step 5: Analyze Search Refinement Patterns

Understand how users modify queries when initial results fail:

| Refinement Type | Description | Example | What It Signals |
|---|---|---|---|
| Narrowing | Adding terms to reduce results | "policy" -> "remote work policy" | Initial query too broad |
| Broadening | Removing terms to increase results | "Q3 2025 engineering OKR" -> "engineering OKR" | Initial query too specific |
| Reformulating | Changing terms entirely | "PTO" -> "vacation request" | Vocabulary mismatch |
| Facet filtering | Applying a filter after searching | Search "policy" + filter: Department=HR | IA/facet design is working |
| Paging | Clicking to page 2+ of results | Scrolling past position 10 | Top results not relevant |
| Giving up | Leaving search entirely | No clicks, no refinement, session ends | Search failed completely |

**Session analysis template:**

```
Session ID: [id]
Query 1: "vacation policy" → 45 results → Clicked #3 → Returned in 5s (short click)
Query 2: "PTO policy 2025" → 12 results → Clicked #1 → Stayed 2 min (success)
Pattern: Reformulation + narrowing — synonym issue ("vacation" vs "PTO")
```

### Step 6: Produce Relevance Tuning Recommendations

Translate analysis into specific, prioritized actions:

| Priority | Criteria | Action Type |
|---|---|---|
| P0 — Critical | Top-50 query with zero results or abandonment above 50% | Fix within 1 week |
| P1 — High | Top-200 query with CTR below 30% or wrong #1 result | Fix within 2 weeks |
| P2 — Medium | Vocabulary mismatch affecting 10+ queries | Fix within 1 month |
| P3 — Low | Long-tail improvements and edge cases | Fix within 1 quarter |

**Common tuning actions:**

| Action | When to Apply | Expected Impact |
|---|---|---|
| Add synonyms | Vocabulary mismatch between queries and content | Reduces zero-results by 10-30% |
| Promote best bets | Known-item queries with wrong top result | Immediate CTR improvement for specific queries |
| Boost recent content | Users prefer current information | Improves relevance for time-sensitive queries |
| Boost by content type | Certain types (policies, forms) should rank higher | Matches user intent for navigational queries |
| Enable spell correction | High typo rate | Reduces zero-results by 5-15% |
| Add autocomplete entries | Users struggle to formulate queries | Guides users toward effective queries |
| Expand indexing | Content formats not being searched | Increases discoverable content surface |
| Adjust field weights | Title matches should outrank body matches | Improves MRR and position-1 CTR |
| Remove stale content | Old content polluting results | Improves precision and user trust |

## Output Format

```markdown
# Search Analytics Report: [System Name]

## Executive Summary
- **Period:** [date range]
- **Total queries:** [n] | **Unique queries:** [n]
- **Overall CTR:** [%] | **Zero-result rate:** [%] | **Abandonment rate:** [%]
- **Top finding:** [one sentence summary of the most important insight]

## Query Analysis
### Top Queries
| Rank | Query | Volume | CTR | Zero-Result? |
|---|---|---|---|---|
| 1 | ... | ... | ... | ... |

### Query Classification
| Type | % of Queries | Notes |
|---|---|---|
| Known-item | ... | ... |
| Topical | ... | ... |

## Zero-Result Analysis
- **Zero-result rate:** [%] (target: under 5%)
- **Top zero-result queries:**
| Query | Volume | Root Cause | Recommended Fix |
|---|---|---|---|
| ... | ... | ... | ... |

## Click-Through Analysis
| Metric | Value | Benchmark | Status |
|---|---|---|---|
| CTR | ... | 60-80% | [OK/Warning/Critical] |
| MRR | ... | 0.5-0.8 | [OK/Warning/Critical] |
| Abandonment | ... | Under 20% | [OK/Warning/Critical] |

## Refinement Patterns
[Key patterns observed and what they indicate]

## Recommendations (Prioritized)
| Priority | Action | Expected Impact | Effort |
|---|---|---|---|
| P0 | ... | ... | ... |
| P1 | ... | ... | ... |
| P2 | ... | ... | ... |

## Monitoring Plan
| KPI | Current | Target | Review Cadence |
|---|---|---|---|
| ... | ... | ... | ... |
```

## Quality Checklist

- [ ] Data covers at least 30 days and bot traffic is excluded
- [ ] Query volume and unique query count are reported
- [ ] Top 50 queries are analyzed individually
- [ ] Zero-result rate is calculated and top zero-result queries are classified by root cause
- [ ] CTR, MRR, and abandonment rate are calculated against benchmarks
- [ ] Refinement patterns are categorized and interpreted
- [ ] Recommendations are prioritized with expected impact and effort
- [ ] A monitoring plan with KPIs and targets is included
- [ ] PII has been scrubbed from all reported data
- [ ] Findings are translated into non-technical language for stakeholders

## Edge Cases

- **Low search volume (under 500 queries/month):** Statistical analysis is unreliable. Shift to qualitative methods: review every zero-result query manually, conduct 5-8 user interviews, and run task-based findability tests instead.
- **Multiple search systems (intranet + wiki + ticketing):** Analyze each system separately first, then look for cross-system patterns. Users searching the wrong system for a query type is an IA problem, not a search problem.
- **No click tracking available:** Use proxy metrics: bounce rate on search results pages, support ticket volume (if search fails, support tickets rise), and session duration after search. Advocate for implementing click tracking as a P0.
- **Highly personalized search results:** Control for personalization when analyzing CTR. Compare personalized vs. non-personalized performance. Report both metrics.
- **Multilingual search:** Analyze each language separately. Cross-language searches (query in English, content in Spanish) require special handling and separate reporting.
- **Sensitive or confidential queries:** Some search queries reveal confidential projects or personal matters. Aggregate data before sharing reports. Never include individual user queries in reports shared broadly.
