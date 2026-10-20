---
name: Source Quality Policy
description: Evaluates source credibility using tier system (Tier-1 to Tier-4) with independence and recency checks. Use when rating sources.
version: 1.0.0
dependencies: none
---

# Source Quality Policy

## Overview

This skill provides the framework for evaluating source credibility and authority. It uses a four-tier system to classify sources, ensuring research is grounded in the best-of-best evidence.

**When to use this skill:**
- After web research has gathered candidate sources
- When evaluating the credibility of a claim's supporting evidence
- Before creating the source review JSON

## The Four-Tier System

### Tier-1: Primary & Authoritative Sources (Highest Quality)
**Characteristics:**
- Original research or primary data
- Published by authoritative institutions
- Peer-reviewed or extensively validated
- Cited by other reputable sources

**Examples:**
- Government statistical agencies (Census Bureau, BLS, SEC filings)
- Peer-reviewed academic journals
- Official technical documentation (AWS docs, language specs)
- Primary research reports from top-tier firms (Gartner, McKinsey, BCG)
- Direct statements from company executives (earnings calls, official blog posts)

**Use for:** Market sizing, technical specifications, regulatory requirements, financial data

### Tier-2: Reputable Secondary Sources
**Characteristics:**
- Established editorial standards
- Professional journalism or analysis
- Fact-checked content
- Named authors with credentials

**Examples:**
- Major business/tech publications (WSJ, NYT, Bloomberg, TechCrunch, The Verge)
- Industry analyst reports (Forrester, IDC)
- Well-researched blog posts from domain experts
- Technical books from recognized publishers

**Use for:** Competitive analysis, trend identification, qualitative insights

### Tier-3: Community & Practitioner Sources
**Characteristics:**
- User-generated content
- Practitioner perspectives
- Anecdotal but valuable insights
- Less rigorous fact-checking

**Examples:**
- Reddit threads from relevant communities
- Hacker News discussions
- Stack Overflow insights
- Indie blog posts
- Product review sites
- Twitter/X threads from practitioners

**Use for:** Customer pain points, unmet needs, product complaints, real-world usage patterns

### Tier-4: Unverified or Promotional
**Characteristics:**
- No editorial oversight
- Potential conflicts of interest
- Marketing or promotional content
- Unverifiable claims

**Examples:**
- Marketing materials and sales decks
- Press releases without corroboration
- AI-generated content farms
- Anonymous sources
- Unattributed statistics

**Use with extreme caution:** Only as directional signals; require Tier-1 or Tier-2 corroboration

## Independence Check

Sources supporting the same claim must be **independent** to avoid circular reporting.

**Not Independent:**
- Article A cites Article B as its source → Only Article B counts
- Both articles cite the same primary source → Only 1 independent source
- Owned by same parent company → Not independent

**Independent:**
- Different methodologies for reaching same conclusion
- Different original data sources
- No citation relationship between sources

## Recency Check

Evaluate whether the source's **publication date** matches the **claim's timeframe**.

**Date Types:**
1. **Publication date**: When the article/report was published
2. **Event date**: When the data/event occurred
3. **Claim date**: The timeframe the claim refers to

**Red Flags:**
- **Stale**: Claim about "2025 market size" citing 2020 data
- **Mismatch**: Claim about "current trends" citing 3-year-old article

**Acceptable:**
- Historical claims citing historical sources
- Evergreen content (architectural patterns, principles)
- Data with clear "as of" dates

## Source Rating JSON Schema

```json
{
  "source_id": "src_001",
  "url": "https://www.census.gov/data/...",
  "title": "U.S. Business Statistics 2025",
  "author": "U.S. Census Bureau",
  "publication_date": "2025-06-15",
  "tier": 1,
  "tier_justification": "Government statistical agency; primary data source",
  "independence": "independent",
  "independence_notes": "Original data collection; not derived from other sources",
  "authority": "high",
  "authority_justification": "Official U.S. government agency",
  "method": "survey",
  "method_notes": "Annual Business Survey with 1M+ sample",
  "recency": "current",
  "recency_notes": "Published June 2025, data from Q1 2025",
  "signal_strength": "strong",
  "signal_notes": "Direct answer to TAM question",
  "verdict": "approved",
  "concerns": []
}
```

### Field Definitions

| Field | Values | Description |
|-------|--------|-------------|
| `tier` | 1-4 | Source tier classification |
| `independence` | "independent", "derived", "circular" | Source independence status |
| `authority` | "high", "medium", "low" | Institutional/author authority |
| `method` | "survey", "experiment", "analysis", "interview", "opinion" | Research methodology |
| `recency` | "current", "acceptable", "stale", "mismatch" | Date alignment check |
| `signal_strength` | "strong", "moderate", "weak" | How directly it answers the question |
| `verdict` | "approved", "supplemental", "rejected" | Final rating |

## Rating Decision Tree

```
1. Is it from a Tier-1 source?
   YES → tier: 1, proceed to independence check
   NO → Continue to step 2

2. Is it from a Tier-2 source?
   YES → tier: 2, proceed to independence check
   NO → Continue to step 3

3. Is it from a Tier-3 source?
   YES → tier: 3, flag as "supplemental only"
   NO → tier: 4, flag as "rejected"

4. Independence Check
   - Does it cite another source as its basis?
     YES → Mark "derived", identify original source
     NO → Mark "independent"

5. Recency Check
   - Publication date within acceptable range for claim?
     YES → "current" or "acceptable"
     NO → "stale" or "mismatch"

6. Signal Strength
   - Does it directly answer the research question?
     YES → "strong"
     PARTIALLY → "moderate"
     NO → "weak"

7. Final Verdict
   - Tier-1/2 + independent + current + strong → "approved"
   - Tier-3 or has concerns → "supplemental"
   - Tier-4 or major concerns → "rejected"
```

## Quality Gates

For high-stakes research, enforce:
- **Minimum 2 Tier-1 sources** for load-bearing claims (e.g., market size, pricing decisions)
- **Or 1 Tier-1 + 1 Tier-2** if Tier-1 coverage is limited
- **All sources must be independent**
- **Publication date within 180 days** for current market/trend claims

For exploratory research, allow:
- **Minimum 2 Tier-2 sources**
- Tier-3 sources acceptable if they represent customer voice

## Common Pitfalls

❌ **Citation Chaining**: Counting 5 articles that all cite the same Gartner report as 5 sources
✅ **Independent Validation**: Finding the original Gartner report + an IDC report with different methodology

❌ **Recency Blindness**: Using 2020 market size data for "current market size" claim in 2025
✅ **Date-Aware**: Flagging as "stale" and seeking 2024-2025 data

❌ **Authority Halo**: Assuming all content from a Tier-1 institution is Tier-1 quality
✅ **Content Evaluation**: A blog post on a .gov site may only be Tier-2 or Tier-3

❌ **Tier Inflation**: Calling a Medium article "Tier-1" because the author is an expert
✅ **Objective Classification**: Medium = Tier-3 (community platform), regardless of author

## Output Format

Create `research/source_review.json`:

```json
{
  "review_date": "2025-10-18T14:30:00Z",
  "reviewer": "source-evaluator",
  "total_sources_evaluated": 15,
  "sources": [
    { /* source rating object */ },
    { /* source rating object */ }
  ],
  "summary": {
    "tier1_count": 3,
    "tier2_count": 7,
    "tier3_count": 4,
    "tier4_count": 1,
    "independent_count": 12,
    "approved_count": 10,
    "supplemental_count": 4,
    "rejected_count": 1
  },
  "quality_assessment": "High: 10 approved sources, 3 Tier-1, sufficient for claims validation"
}
```

## References

See `resources/tier-rubric.md` for detailed tier classification examples
See `resources/independence-check.md` for independence evaluation methodology
