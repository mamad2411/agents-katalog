---
name: deep-research
description: Deep research methodology — multi-source investigation, web search with Exa, documentation traversal, cross-referencing sources, synthesizing findings, research report structure, evidence grading, conflicting source resolution, citation format.
origin: AI Dev Kit
---

# Deep Research

Systematic methodology for investigating technical questions across multiple sources,
synthesizing findings with evidence grading, and producing structured research reports.

## When to Use

- Answering complex technical questions that require investigating multiple sources.
- Evaluating technology choices with evidence-backed comparisons.
- Investigating bugs, regressions, or behavioral changes across versions.
- Compiling knowledge about unfamiliar domains, frameworks, or APIs.
- Producing research reports that inform architectural or strategic decisions.
- Cross-referencing documentation, code, and community knowledge for accuracy.

## Core Concepts

### 1. Multi-Source Investigation

```
Research Question: "Should we migrate from FastAPI 0.109 to FastAPI 0.115?"

Sources to investigate:
├── Official docs (fastapi.tiangolo.com/changelog)
├── GitHub releases (github.com/tiangolo/fastapi/releases)
├── GitHub issues (breaking changes, deprecation warnings)
├── Community discussions (Reddit, Twitter, Discord)
├── Blog posts about the migration
├── Our own codebase (current version usage, affected patterns)
└── Benchmark comparisons (performance impact)
```

**Investigation workflow:**

```python
from dataclasses import dataclass
from enum import Enum


class SourceType(Enum):
    OFFICIAL_DOCS = "official_docs"
    GITHUB_ISSUES = "github_issues"
    GITHUB_RELEASES = "github_releases"
    BLOG_POST = "blog_post"
    COMMUNITY = "community"
    BENCHMARK = "benchmark"
    CODEBASE = "codebase"


@dataclass
class ResearchSource:
    url: str
    title: str
    source_type: SourceType
    content: str
    date: str
    relevance: float  # 0.0-1.0


@dataclass
class ResearchFinding:
    claim: str
    evidence: str
    sources: list[str]  # URLs
    confidence: float   # 0.0-1.0
    category: str       # "breaking_change", "feature", "performance", etc.


async def investigate(
    question: str,
    max_sources: int = 15,
) -> list[ResearchSource]:
    """Multi-source investigation."""
    sources = []

    # Step 1: Web search (Exa)
    web_results = await exa_search(question, num_results=5)
    sources.extend(web_results)

    # Step 2: Documentation lookup (Context7 / direct)
    docs = await fetch_official_docs(question)
    sources.extend(docs)

    # Step 3: GitHub investigation
    issues = await search_github_issues(question)
    releases = await fetch_github_releases(question)
    sources.extend(issues + releases)

    # Step 4: Community signal
    community = await search_community(question)
    sources.extend(community)

    # Deduplicate and rank
    return rank_and_deduplicate(sources)[:max_sources]
```

### 2. Web Search with Exa

```python
async def exa_research_search(
    query: str,
    num_results: int = 5,
    use_highlights: bool = True,
) -> list[dict]:
    """Search with Exa for research purposes."""
    results = await exa_client.search(
        query,
        num_results=num_results,
        type="neural",
        use_autoprompt=True,
        start_published_date="2024-01-01",  # Recent results only
    )

    sources = []
    for result in results.results:
        source = {
            "url": result.url,
            "title": result.title,
            "content": result.text or "",
            "highlights": result.highlights if use_highlights else [],
            "score": result.score,
            "published_date": result.published_date,
        }
        sources.append(source)

    return sources
```

### 3. Documentation Traversal

```python
async def fetch_official_docs(question: str) -> list[ResearchSource]:
    """Fetch relevant official documentation."""

    # Extract product name and version from question
    # "FastAPI 0.109 to 0.115" → product=fastapi, versions=[0.109, 0.115]
    entities = extract_entities(question)

    sources = []
    for entity in entities:
        # Fetch changelog
        changelog_url = f"{entity['docs_base']}/changelog"
        changelog = await fetch_page(changelog_url)
        if changelog:
            sources.append(ResearchSource(
                url=changelog_url,
                title=f"{entity['name']} Changelog",
                source_type=SourceType.OFFICIAL_DOCS,
                content=extract_relevant_sections(changelog, entity["versions"]),
                date="",
                relevance=0.95,
            ))

        # Fetch migration guide if exists
        migration_url = f"{entity['docs_base']}/migration"
        migration = await fetch_page(migration_url)
        if migration:
            sources.append(ResearchSource(
                url=migration_url,
                title=f"{entity['name']} Migration Guide",
                source_type=SourceType.OFFICIAL_DOCS,
                content=migration,
                date="",
                relevance=0.9,
            ))

    return sources
```

### 4. Cross-Referencing Sources

```python
def cross_reference(findings: list[ResearchFinding]) -> list[ResearchFinding]:
    """Cross-reference findings across sources to boost confidence."""

    # Group findings by claim
    claim_groups: dict[str, list[ResearchFinding]] = {}
    for f in findings:
        key = normalize_claim(f.claim)
        claim_groups.setdefault(key, []).append(f)

    cross_referenced = []
    for claim, group in claim_groups.items():
        # Count corroborating vs conflicting sources
        corroborating = [f for f in group if f.confidence > 0.5]
        conflicting = [f for f in group if f.confidence < 0.3]

        merged = ResearchFinding(
            claim=claim,
            evidence="\n".join(f.evidence for f in corroborating),
            sources=list(set(s for f in corroborating for s in f.sources)),
            confidence=min(0.95, sum(f.confidence for f in corroborating) / len(corroborating)),
            category=corroborating[0].category,
        )

        if conflicting:
            merged.evidence += f"\n\nCONFLICTING: {conflicting[0].evidence}"
            merged.confidence *= 0.5  # Reduce confidence for conflicts

        cross_referenced.append(merged)

    return sorted(cross_referenced, key=lambda x: x.confidence, reverse=True)
```

### 5. Synthesizing Findings

```python
def synthesize_findings(
    sources: list[ResearchSource],
    findings: list[ResearchFinding],
    question: str,
) -> str:
    """Synthesize findings into a coherent narrative."""

    # Group by category
    by_category: dict[str, list[ResearchFinding]] = {}
    for f in findings:
        by_category.setdefault(f.category, []).append(f)

    report = f"# Research Report: {question}\n\n"
    report += f"**Sources analyzed:** {len(sources)}\n"
    report += f"**Date:** {datetime.now().strftime('%Y-%m-%d')}\n\n"

    # Executive summary
    report += "## Executive Summary\n\n"
    key_findings = sorted(findings, key=lambda x: x.confidence, reverse=True)[:5]
    for i, f in enumerate(key_findings, 1):
        report += f"{i}. **{f.claim}** (confidence: {f.confidence:.2f})\n"
    report += "\n"

    # Detailed findings by category
    for category, cat_findings in by_category.items():
        report += f"## {category.replace('_', ' ').title()}\n\n"
        for f in sorted(cat_findings, key=lambda x: x.confidence, reverse=True):
            report += f"### {f.claim}\n\n"
            report += f"{f.evidence}\n\n"
            report += f"**Sources:** {', '.join(f'[{s}]({s})' for s in f.sources[:3])}\n"
            report += f"**Confidence:** {f.confidence:.2f}\n\n"

    return report
```

### 6. Research Report Structure

```markdown
# Research Report: [Question]

## Executive Summary
- 3-5 key findings with confidence scores
- Overall recommendation (if applicable)

## Methodology
- Sources searched (Exa, GitHub, docs, community)
- Search queries used
- Date range covered

## Findings

### [Category 1: Breaking Changes]
- Finding 1 [confidence: 0.95] — evidence + sources
- Finding 2 [confidence: 0.80] — evidence + sources

### [Category 2: New Features]
- ...

### [Category 3: Performance Impact]
- ...

### [Category 4: Community Consensus]
- ...

## Conflicting Evidence
- What sources disagree and why
- How conflicts were resolved

## Recommendation
- Actionable conclusion based on evidence
- Risks and caveats

## References
- Full list of sources with URLs and access dates
```

### 7. Evidence Grading

```python
def grade_evidence(source: ResearchSource) -> float:
    """Assign a confidence score to a source based on type and quality."""

    base_scores = {
        SourceType.OFFICIAL_DOCS: 0.95,
        SourceType.GITHUB_RELEASES: 0.90,
        SourceType.GITHUB_ISSUES: 0.80,
        SourceType.BENCHMARK: 0.75,
        SourceType.BLOG_POST: 0.65,
        SourceType.COMMUNITY: 0.50,
        SourceType.CODEBASE: 0.85,
    }

    score = base_scores.get(source.source_type, 0.5)

    # Adjustments
    if source.date and is_recent(source.date, days=90):
        score += 0.05  # Recent bonus
    if source.relevance < 0.5:
        score -= 0.2   # Low relevance penalty
    if len(source.content) < 200:
        score -= 0.1   # Too short to be reliable

    return max(0.0, min(1.0, score))
```

### 8. Conflicting Source Resolution

```python
def resolve_conflicts(
    findings: list[ResearchFinding],
) -> list[ResearchFinding]:
    """When sources disagree, apply resolution rules."""

    resolved = []
    for f in findings:
        # Check for conflicts within this finding's evidence
        if "CONFLICT" in f.evidence.upper() or "DISAGREE" in f.evidence.upper():
            # Resolution priority: official docs > releases > issues > blogs > community
            source_priority = {
                SourceType.OFFICIAL_DOCS: 5,
                SourceType.GITHUB_RELEASES: 4,
                SourceType.CODEBASE: 3,
                SourceType.GITHUB_ISSUES: 2,
                SourceType.BLOG_POST: 1,
                SourceType.COMMUNITY: 0,
            }

            # Keep the highest-priority source's claim
            best_source = max(f.sources, key=lambda s: source_priority.get(get_source_type(s), 0))
            f.confidence *= 0.7  # Penalty for conflict
            f.evidence += f"\n\nResolved in favor of: {best_source}"

        resolved.append(f)

    return resolved
```

### 9. Research Citation Format

```markdown
[1] Author/Source. "Title." URL. Accessed YYYY-MM-DD.
    Type: official_docs | blog_post | github_issues | etc.
    Confidence: 0.XX

Example:
[1] FastAPI. "Release Notes — FastAPI 0.115.0." https://fastapi.tiangolo.com/release-notes/#01150. Accessed 2026-04-13.
    Type: official_docs
    Confidence: 0.95

[2] Sebastián Ramírez. "Fix regression in dependency injection #12345." https://github.com/tiangolo/fastapi/issues/12345. Accessed 2026-04-13.
    Type: github_issues
    Confidence: 0.80
```

## Anti-Patterns

- **Single-source research** — relying on one blog post or one Stack Overflow answer
- **No evidence grading** — treating a Reddit comment the same as official documentation
- **Ignoring conflicts** — not surfacing when sources disagree
- **Outdated sources** — citing 3-year-old blog posts for fast-moving projects
- **No methodology section** — readers can't assess research quality without knowing what was searched
- **Copy-paste without synthesis** — raw quotes without analysis are not research
- **Missing confidence scores** — every claim needs a confidence indicator

## Best Practices

1. **Use at least 3 independent sources** per major claim — official docs + community + code.
2. **Grade evidence by source type** — official documentation > GitHub > blogs > forums.
3. **Cross-reference before concluding** — if two sources agree, confidence increases; if they disagree, flag it.
4. **Structure reports consistently** — executive summary, methodology, findings, conflicts, recommendation.
5. **Always include confidence scores** — 0.0-1.0 for every finding.
6. **Resolve conflicts explicitly** — state which source wins and why.
7. **Cite with URLs and access dates** — so readers can verify.
8. **Limit to recent sources** — prefer results from the last 12 months for fast-moving projects.
9. **Synthesize, don't aggregate** — analyze patterns, don't just list sources.
10. **Include a recommendation section** — research should inform decisions, not just inform.

## Related Skills

- `exa-search` — Web search execution with Exa
- `search-first` — Search-before-coding discipline
- `documentation-lookup` — Documentation traversal patterns
- `prompt-optimizer` — Crafting prompts for research synthesis
- `iterative-retrieval` — Progressive context loading during research
