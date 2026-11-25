---
name: Web Research Executor
description: Orchestrates parallel web searches using Tavily + brave-search. Handles rate limiting, deduplication, source extraction. Use for broad market/tech research.
version: 1.0.0
network: true
dependencies: python>=3.8
---

# Web Research Executor

## Overview

This skill provides the operational layer for executing web research at scale. It orchestrates multiple search tools in parallel, handles errors gracefully, deduplicates results, and extracts structured data.

**When to use this skill:**
- When executing the queries defined in `research/plan.json`
- When you need comprehensive coverage across multiple search tools
- When you need reliable, production-grade web research

## Architecture

```
research/plan.json (queries defined)
        ↓
web-exec skill invoked
        ↓
Parallel Execution:
  ├─ Tavily search (advanced depth)
  ├─ Brave web search
  └─ Brave news search (if recent news needed)
        ↓
Merge & Deduplicate
        ↓
Extract & Structure
        ↓
research/sources.json (output)
```

## Parallel Search Orchestration

The `scripts/parallel_search.py` script handles concurrent API calls:

```python
import asyncio
from typing import List, Dict

async def execute_searches(queries: List[str], tools: List[str]) -> List[Dict]:
    """
    Execute multiple queries across multiple tools in parallel.

    Args:
        queries: List of search queries from research/plan.json
        tools: ["tavily", "brave_web", "brave_news"]

    Returns:
        List of search results with metadata
    """
    tasks = []

    for query in queries:
        if "tavily" in tools:
            tasks.append(tavily_search_async(query))
        if "brave_web" in tools:
            tasks.append(brave_web_search_async(query))
        if "brave_news" in tools and is_news_query(query):
            tasks.append(brave_news_search_async(query))

    # Execute all searches in parallel
    results = await asyncio.gather(*tasks, return_exceptions=True)

    # Filter out errors, log them
    successful = [r for r in results if not isinstance(r, Exception)]
    errors = [r for r in results if isinstance(r, Exception)]

    if errors:
        log_errors(errors)

    return successful
```

### Query Routing Logic

Not all queries need all tools. Route intelligently:

| Query Type | Tavily | Brave Web | Brave News |
|------------|--------|-----------|------------|
| Market data | ✅ (advanced) | ✅ | ❌ |
| Technical docs | ✅ (basic) | ✅ | ❌ |
| Recent news | ✅ (freshness: pw) | ❌ | ✅ |
| User sentiment | ❌ | ✅ | ❌ |
| Competitive intel | ✅ (advanced) | ✅ | ✅ |

**Example routing:**
```python
def route_query(query: str) -> List[str]:
    tools = []

    # Always use Tavily for structured research
    tools.append("tavily")

    # Add Brave web for broad coverage
    tools.append("brave_web")

    # Add news search if query suggests recent events
    if any(word in query.lower() for word in ["launch", "announce", "2025", "latest"]):
        tools.append("brave_news")

    return tools
```

## Rate Limiting Strategy

### Tavily
- **Free tier:** 1,000 requests/month
- **Strategy:** Batch queries, use advanced search (returns more per query)
- **Backoff:** Exponential (1s, 2s, 4s, 8s) on 429 errors

### Brave Search
- **Rate limits:** Check plan-specific limits
- **Strategy:** Distribute load, cache aggressively
- **Backoff:** Linear (1s, 2s, 3s) on 429 errors

### Implementation
```python
class RateLimiter:
    def __init__(self, tool: str):
        self.tool = tool
        self.retry_count = 0
        self.max_retries = 3

    async def execute_with_backoff(self, search_fn, *args):
        while self.retry_count < self.max_retries:
            try:
                return await search_fn(*args)
            except RateLimitError:
                wait_time = self.get_backoff_time()
                await asyncio.sleep(wait_time)
                self.retry_count += 1

        raise MaxRetriesExceeded(f"{self.tool} rate limit exceeded")

    def get_backoff_time(self) -> int:
        if self.tool == "tavily":
            return 2 ** self.retry_count  # Exponential
        else:
            return self.retry_count + 1    # Linear
```

## Deduplication Logic

Merge results from multiple tools, removing duplicates:

```python
def deduplicate_sources(sources: List[Dict]) -> List[Dict]:
    """
    Remove duplicate sources based on URL and content similarity.
    """
    seen_urls = set()
    seen_content_hashes = set()
    unique_sources = []

    for source in sources:
        url_normalized = normalize_url(source['url'])
        content_hash = hash_content(source.get('content', ''))

        # Check URL duplication
        if url_normalized in seen_urls:
            continue

        # Check content duplication (catches mirror sites)
        if content_hash in seen_content_hashes:
            continue

        seen_urls.add(url_normalized)
        seen_content_hashes.add(content_hash)
        unique_sources.append(source)

    return unique_sources

def normalize_url(url: str) -> str:
    """Remove tracking params, fragments, normalize protocol."""
    from urllib.parse import urlparse, parse_qs, urlencode

    parsed = urlparse(url)

    # Remove common tracking params
    query_params = parse_qs(parsed.query)
    clean_params = {
        k: v for k, v in query_params.items()
        if k not in ['utm_source', 'utm_medium', 'utm_campaign', 'ref', 'source']
    }

    # Reconstruct clean URL
    clean_url = f"{parsed.scheme}://{parsed.netloc}{parsed.path}"
    if clean_params:
        clean_url += f"?{urlencode(clean_params, doseq=True)}"

    return clean_url.lower()
```

## Source Extraction

Transform raw API responses into structured source objects:

```python
def extract_source_metadata(raw_result: Dict, tool: str) -> Dict:
    """
    Extract standardized metadata from tool-specific response.
    """
    if tool == "tavily":
        return {
            "source_id": generate_id(),
            "url": raw_result['url'],
            "title": raw_result['title'],
            "excerpt": raw_result.get('content', '')[:500],
            "publication_date": extract_date_from_content(raw_result),
            "discovery_method": "tavily",
            "raw_score": raw_result.get('score', 0),
            "relevance_score": normalize_score(raw_result.get('score', 0))
        }

    elif tool == "brave_web":
        return {
            "source_id": generate_id(),
            "url": raw_result['url'],
            "title": raw_result['title'],
            "excerpt": raw_result.get('description', '')[:500],
            "publication_date": raw_result.get('age'),
            "discovery_method": "brave_web",
            "relevance_score": 0.7  # Brave doesn't provide scores
        }

    # Add other tools as needed

def extract_date_from_content(result: Dict) -> str:
    """
    Attempt to extract publication date from content or metadata.
    Returns ISO 8601 string or None.
    """
    # Try explicit published_date field
    if 'published_date' in result:
        return result['published_date']

    # Parse from content using regex
    content = result.get('content', '')
    date_patterns = [
        r'Published:?\s*(\d{4}-\d{2}-\d{2})',
        r'(\d{4}-\d{2}-\d{2})',
        r'(\w+ \d{1,2}, \d{4})'
    ]

    for pattern in date_patterns:
        match = re.search(pattern, content)
        if match:
            return parse_date_string(match.group(1))

    return None
```

## Error Handling

Graceful degradation when tools fail:

```python
async def execute_search_with_fallback(query: str) -> List[Dict]:
    """
    Try primary tool, fall back to secondary on failure.
    """
    try:
        # Primary: Tavily (higher quality)
        return await tavily_search(query, search_depth="advanced")

    except TavilyError as e:
        logger.warning(f"Tavily failed for '{query}': {e}")

        try:
            # Fallback: Brave Web Search
            return await brave_web_search(query)

        except BraveError as e:
            logger.error(f"Both Tavily and Brave failed for '{query}': {e}")

            # Last resort: return empty with error flag
            return [{
                "error": True,
                "query": query,
                "message": "All search tools failed"
            }]
```

## Caching Strategy

Cache results to avoid redundant API calls:

```python
import hashlib
import json
from pathlib import Path

CACHE_DIR = Path("research/.cache")

def get_cached_result(query: str, tool: str, max_age_hours: int = 24) -> Dict | None:
    """Check if cached result exists and is fresh."""
    cache_key = hashlib.md5(f"{tool}:{query}".encode()).hexdigest()
    cache_file = CACHE_DIR / f"{cache_key}.json"

    if not cache_file.exists():
        return None

    with open(cache_file) as f:
        cached = json.load(f)

    # Check age
    cached_time = datetime.fromisoformat(cached['cached_at'])
    age_hours = (datetime.now() - cached_time).total_seconds() / 3600

    if age_hours > max_age_hours:
        return None

    return cached['result']

def save_to_cache(query: str, tool: str, result: Dict):
    """Save search result to cache."""
    CACHE_DIR.mkdir(exist_ok=True)
    cache_key = hashlib.md5(f"{tool}:{query}".encode()).hexdigest()
    cache_file = CACHE_DIR / f"{cache_key}.json"

    with open(cache_file, 'w') as f:
        json.dump({
            'query': query,
            'tool': tool,
            'cached_at': datetime.now().isoformat(),
            'result': result
        }, f)
```

## Performance Metrics

Track execution performance:

```json
{
  "execution_metrics": {
    "total_queries": 12,
    "queries_from_cache": 3,
    "queries_executed": 9,
    "parallel_batches": 3,
    "total_wall_time_seconds": 45.2,
    "avg_query_time_seconds": 5.0,
    "rate_limit_errors": 2,
    "network_errors": 0,
    "results_before_dedup": 87,
    "results_after_dedup": 63,
    "deduplication_rate": 0.28
  }
}
```

## Output Format

`research/sources.json`:

```json
{
  "execution_date": "2025-10-18T15:30:00Z",
  "plan_reference": "research/plan.json",
  "queries_executed": [
    {
      "query": "AI coding agents market size 2025",
      "tools_used": ["tavily", "brave_web"],
      "results_count": 15,
      "cache_hit": false,
      "execution_time_ms": 3420
    }
  ],
  "sources": [
    {
      "source_id": "src_001",
      "url": "https://gartner.com/...",
      "title": "Market Guide for AI-Assisted Developer Tools",
      "author": "Gartner Research",
      "publication_date": "2025-06-15",
      "excerpt": "...",
      "discovery_method": "tavily",
      "relevance_score": 0.95,
      "query_matched": "AI coding agents market size 2025"
    }
  ],
  "execution_metrics": { /* see above */ }
}
```

## Integration

The web-exec skill is invoked by industry-signal-scout:

```
industry-signal-scout loads industry-scout skill
    ↓
Calls scripts/parallel_search.py with queries from plan.json
    ↓
parallel_search.py uses this skill's orchestration logic
    ↓
Outputs research/sources.json
    ↓
Passed to source-evaluator for tier rating
```

## References

See `scripts/parallel_search.py` for implementation
See Python SDK docs for Tavily and Brave Search APIs
