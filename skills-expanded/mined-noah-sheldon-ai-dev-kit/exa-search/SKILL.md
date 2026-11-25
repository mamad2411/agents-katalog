---
name: exa-search
description: Exa search — MCP server usage, semantic search queries, query optimization, result filtering, relevance scoring, research workflows, comparing results across queries, combining Exa with Context7 docs lookup, search result validation.
origin: AI Dev Kit
---

# Exa Search

Use Exa's neural search engine for deep web research, code reference lookup,
and technical investigation. Covers MCP server integration, query strategies,
result filtering, and combining Exa with documentation lookups.

## When to Use

- Researching technologies, libraries, or frameworks not in local context.
- Finding recent blog posts, tutorials, or announcements about a topic.
- Looking for migration guides, breaking changes, or version comparisons.
- Investigating error messages, bugs, or community-reported issues.
- Gathering evidence for architecture decisions or technology evaluations.
- Complementing local code search with external knowledge from the web.

## Core Concepts

### 1. MCP Server Usage

Exa is accessed via MCP (Model Context Protocol) server configuration:

```json
{
  "mcpServers": {
    "exa": {
      "command": "npx",
      "args": ["-y", "exa-mcp-server"],
      "env": {
        "EXA_API_KEY": "your-api-key"
      }
    }
  }
}
```

**Available tools:**
- `exa_search` — Neural search with highlighted excerpts
- `exa_get_contents` — Fetch full page content from URLs
- `exa_find_similar` — Find pages similar to a given URL

### 2. Semantic Search Queries

Exa uses neural embeddings, so query formulation matters:

```
# Good queries (specific, contextual)
"FastAPI 0.115 breaking changes dependency injection"
"Pydantic v2 field_validator migration from v1 validator"
"React Server Components vs Client Components when to use each 2025"

# Bad queries (too vague or keyword-stuffed)
"FastAPI changes"
"Pydantic validator migration v1 v2 difference how to update code"
```

**Query optimization patterns:**

```python
def optimize_query(original: str) -> list[str]:
    """Generate multiple query variations for better coverage."""

    variations = [
        original,  # Original query
        original + " 2025 2026",  # Recency boost
        original + " breaking changes migration",  # Migration focus
        original + " tutorial example code",  # Code examples
    ]

    # Remove duplicates while preserving order
    seen = set()
    unique = []
    for q in variations:
        normalized = q.lower().strip()
        if normalized not in seen:
            seen.add(normalized)
            unique.append(q)

    return unique[:4]
```

### 3. Search Execution and Result Filtering

```python
async def exa_search(
    query: str,
    num_results: int = 5,
    include_highlights: bool = True,
    start_date: str = None,
    end_date: str = None,
    domains: list[str] = None,
) -> list[dict]:
    """Execute an Exa search with filters."""

    search_params = {
        "query": query,
        "num_results": num_results,
        "type": "neural",
        "use_autoprompt": True,
    }

    if include_highlights:
        search_params["highlights"] = {
            "num_sentences": 3,
            "query": query,
        }

    if start_date:
        search_params["start_published_date"] = start_date
    if end_date:
        search_params["end_published_date"] = end_date
    if domains:
        search_params["include_domains"] = domains

    results = await exa_client.search(**search_params)

    return [
        {
            "url": r.url,
            "title": r.title,
            "text": r.text,
            "highlights": r.highlights,
            "score": r.score,
            "published_date": r.published_date,
            "author": r.author,
        }
        for r in results.results
    ]
```

### 4. Relevance Scoring

```python
def score_exa_result(result: dict, query: str) -> float:
    """Composite relevance score for an Exa result."""

    # Exa's own neural score
    neural_score = result.get("score", 0.5)

    # Query term overlap
    query_terms = set(query.lower().split())
    title_terms = set(result.get("title", "").lower().split())
    title_overlap = len(query_terms & title_terms) / max(len(query_terms), 1)

    # Recency bonus
    pub_date = result.get("published_date")
    recency_bonus = 0.0
    if pub_date:
        try:
            from datetime import datetime
            pub = datetime.fromisoformat(pub_date.replace("Z", "+00:00"))
            days_old = (datetime.now(pub.tzinfo) - pub).days
            if days_old < 30:
                recency_bonus = 0.15
            elif days_old < 90:
                recency_bonus = 0.10
            elif days_old < 365:
                recency_bonus = 0.05
        except (ValueError, TypeError):
            pass

    # Content length (longer = more substantial, up to a point)
    text_len = len(result.get("text", ""))
    length_bonus = min(text_len / 5000, 1.0) * 0.1

    composite = (neural_score * 0.6) + (title_overlap * 0.2) + recency_bonus + length_bonus
    return min(composite, 1.0)
```

### 5. Research Workflows

**Single-topic deep dive:**

```python
async def deep_dive_research(topic: str) -> dict:
    """Comprehensive research on a single topic."""

    # Phase 1: Broad search
    queries = optimize_query(topic)
    all_results = []
    for q in queries:
        results = await exa_search(q, num_results=5, start_date="2025-01-01")
        all_results.extend(results)

    # Phase 2: Deduplicate by URL
    seen_urls = set()
    unique_results = []
    for r in all_results:
        if r["url"] not in seen_urls:
            seen_urls.add(r["url"])
            unique_results.append(r)

    # Phase 3: Score and rank
    for r in unique_results:
        r["relevance"] = score_exa_result(r, topic)

    unique_results.sort(key=lambda x: x["relevance"], reverse=True)

    # Phase 4: Fetch full content for top results
    top_urls = [r["url"] for r in unique_results[:3]]
    contents = await exa_client.get_contents(top_urls)

    return {
        "topic": topic,
        "sources": unique_results[:10],
        "top_contents": contents,
        "total_sources": len(unique_results),
    }
```

**Comparison research:**

```python
async def compare_technologies(tech_a: str, tech_b: str, context: str) -> dict:
    """Research two technologies for comparison."""

    queries = [
        f"{tech_a} vs {tech_b} {context}",
        f"{tech_a} advantages disadvantages {context}",
        f"{tech_b} advantages disadvantages {context}",
        f"migrate from {tech_a} to {tech_b}",
    ]

    results_by_tech = {"a": [], "b": [], "comparison": []}

    for q in queries:
        results = await exa_search(q, num_results=5)
        for r in results:
            if "vs" in q.lower() or "compare" in q.lower():
                results_by_tech["comparison"].append(r)
            elif tech_a.lower() in q.lower():
                results_by_tech["a"].append(r)
            else:
                results_by_tech["b"].append(r)

    return results_by_tech
```

### 6. Combining Exa with Context7 Docs Lookup

```python
async def research_with_docs_and_web(
    topic: str,
    product_name: str,
) -> dict:
    """Combine Exa web search with Context7 documentation lookup."""

    # Parallel: search the web AND check official docs
    import asyncio

    web_task = exa_search(f"{product_name} {topic}", num_results=5)
    docs_task = context7_lookup(f"{product_name} {topic}")

    web_results, docs_results = await asyncio.gather(
        web_task, docs_task, return_exceptions=True,
    )

    # Combine and deduplicate
    combined = []

    if not isinstance(web_results, Exception):
        for r in web_results:
            r["source_type"] = "web"
            combined.append(r)

    if not isinstance(docs_results, Exception):
        for d in docs_results:
            d["source_type"] = "official_docs"
            d["relevance"] = 0.95  # Official docs get high base relevance
            combined.append(d)

    combined.sort(key=lambda x: x.get("relevance", 0.5), reverse=True)

    return {
        "topic": topic,
        "product": product_name,
        "results": combined[:15],
        "has_official_docs": any(r["source_type"] == "official_docs" for r in combined),
    }
```

### 7. Comparing Results Across Queries

```python
def compare_query_results(
    query_results: dict[str, list[dict]],
) -> dict:
    """Analyze overlap and uniqueness across multiple query results."""

    all_urls = {}
    for query, results in query_results.items():
        for r in results:
            if r["url"] not in all_urls:
                all_urls[r["url"]] = {
                    "url": r["url"],
                    "title": r["title"],
                    "found_in_queries": [],
                    "best_score": 0,
                }
            all_urls[r["url"]]["found_in_queries"].append(query)
            all_urls[r["url"]]["best_score"] = max(
                all_urls[r["url"]]["best_score"],
                r.get("score", 0),
            )

    # Analysis
    unique_to_query = {}
    shared = []
    for url, info in all_urls.items():
        if len(info["found_in_queries"]) == 1:
            q = info["found_in_queries"][0]
            unique_to_query.setdefault(q, []).append(info)
        else:
            shared.append(info)

    return {
        "total_unique_urls": len(all_urls),
        "unique_by_query": {q: len(v) for q, v in unique_to_query.items()},
        "shared_across_queries": len(shared),
        "top_shared_sources": sorted(shared, key=lambda x: x["best_score"], reverse=True)[:5],
    }
```

### 8. Search Result Validation

```python
def validate_search_results(
    results: list[dict],
    min_relevance: float = 0.3,
    min_content_length: int = 100,
    blocked_domains: list[str] = None,
) -> list[dict]:
    """Filter out low-quality or irrelevant results."""

    valid = []
    for r in results:
        # Relevance threshold
        if r.get("score", 0) < min_relevance:
            continue

        # Content quality
        if len(r.get("text", "")) < min_content_length:
            continue

        # Domain filtering
        if blocked_domains:
            from urllib.parse import urlparse
            domain = urlparse(r["url"]).netloc
            if any(bd in domain for bd in blocked_domains):
                continue

        # Title quality
        if not r.get("title") or len(r["title"]) < 5:
            continue

        valid.append(r)

    return valid
```

## Anti-Patterns

- **Single-query searches** — one query misses important angles; use multiple variations
- **Ignoring date filters** — stale results for fast-moving technologies are misleading
- **Not fetching full content** — highlights alone may miss critical details; get_contents for top results
- **No deduplication** — the same page appears across multiple query results
- **Trusting Exa scores blindly** — always apply your own relevance scoring on top
- **Searching without context** — vague queries return vague results; be specific

## Best Practices

1. **Generate 3-4 query variations** — broad, specific, migration-focused, and code-focused.
2. **Always filter by date** — limit to the last 12 months for fast-moving projects.
3. **Score results with composite metrics** — combine Exa score, title overlap, recency, and content length.
4. **Deduplicate across queries** — the same URL from different queries should appear once.
5. **Fetch full content for top 3 results** — highlights are summaries; full text reveals nuance.
6. **Combine Exa with Context7** — web search + official docs gives the most complete picture.
7. **Compare query results** — analyze which queries surface unique vs shared sources.
8. **Validate before using** — filter by relevance, content length, and blocked domains.
9. **Use autoprompt** — let Exa reformulate your query for better neural matching.
10. **Include domain restrictions** when relevant — `include_domains: ["github.com", "docs.python.org"]`.

## Related Skills

- `deep-research` — Full research methodology that uses Exa as a primary source
- `search-first` — Search-before-coding discipline
- `documentation-lookup` — Context7 docs lookup to complement Exa
- `iterative-retrieval` — Progressive context loading from search results
- `prompt-optimizer` — Crafting search queries that return high-quality results
