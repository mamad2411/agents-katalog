---
name: research-methodology
description: >
  Search and research workflow patterns. Research depth levels, source credibility assessment,
  multi-hop reasoning, search query formulation, and citation management. Use when conducting
  research, evaluating sources, or synthesizing findings.
---

# research-methodology

Search and research workflow patterns.

## how to use

- `/research-methodology`
  Apply these research standards to all investigation work in this conversation.

- `/research-methodology <topic>`
  Plan and execute a research workflow for the given topic.

## when to apply

Reference these guidelines when:
- investigating unfamiliar technologies or APIs
- evaluating library or framework options
- conducting competitive or market research
- gathering requirements from multiple sources
- synthesizing findings into recommendations
- verifying claims or troubleshooting with external info

## rule categories by priority

| priority | category | impact |
|----------|----------|--------|
| 1 | research planning | critical |
| 2 | search execution | critical |
| 3 | source assessment | high |
| 4 | synthesis | high |
| 5 | citation management | medium |

## quick reference

### 1. research planning (critical)

**Depth levels** (choose before starting):
| Level | Time | Hops | Use When |
|-------|------|------|----------|
| Quick | 1-2 queries | 1 | Known-answer lookup, single fact |
| Standard | 3-5 queries | 2-3 | Compare options, understand a concept |
| Deep | 5-10 queries | 3-5 | Architecture decisions, technology evaluation |
| Exhaustive | 10+ queries | 5+ | Critical decisions, security analysis, compliance |

**Before searching**:
- state the question precisely
- list what you already know
- identify knowledge gaps
- determine depth level
- set a scope boundary (what's NOT in scope)

### 2. search execution (critical)

**Tool routing**:
| Need | Tool | When |
|------|------|------|
| Library docs | Context7 | API signatures, usage patterns, version-specific info |
| Live web results | WebSearch | Current events, comparisons, community discussions |
| Specific page content | WebFetch | Reading a known URL, documentation page, GitHub README |
| Codebase patterns | Grep/Glob | How something is used in the current project |

**Query formulation**:
- use specific terms over generic ones
- include version numbers when relevant
- add "vs" for comparisons, "best practices" for patterns
- quote exact error messages
- chain queries: broad first, then narrow based on results

**Multi-hop reasoning**:
1. Initial query establishes landscape
2. Follow-up queries drill into promising leads
3. Cross-reference findings across sources
4. Validate with official documentation
5. Verify currency (check dates)

### 3. source assessment (high)

**Credibility hierarchy**:
| Tier | Source Type | Trust Level |
|------|-----------|-------------|
| 1 | Official documentation, RFCs, specifications | High |
| 2 | Peer-reviewed papers, reputable tech blogs (engineering blogs from known companies) | High |
| 3 | Stack Overflow (accepted + high-vote answers), GitHub issues/PRs | Medium-High |
| 4 | Tutorial sites, Medium articles, dev.to posts | Medium |
| 5 | Forum posts, social media, AI-generated content | Low |

**Red flags**:
- no date or very old date (> 2 years for fast-moving tech)
- no author attribution
- contradicts official documentation
- promotes specific product without disclosure
- contains factual errors in verifiable claims

### 4. synthesis (high)

- lead with the answer, then provide evidence
- compare options with a structured table (pros/cons/tradeoffs)
- state confidence level: high (multiple confirming sources), medium (limited sources), low (single/conflicting sources)
- flag conflicting information explicitly
- separate facts from opinions
- provide actionable recommendations, not just summaries
- note what remains unknown

### 5. citation management (medium)

- link to sources inline where referenced
- provide a sources table for deep research:
  | Source | URL | Type | Date | Credibility |
- prefer permalinks over search result links
- note when information may become outdated
- distinguish primary sources from secondary references

## anti-patterns

| anti-pattern | problem | fix |
|-------------|---------|-----|
| searching without a plan | scattered, inefficient research | state question and depth level first |
| trusting first result | may be outdated or wrong | cross-reference with 2+ sources |
| ignoring dates | stale information | check publication date, prefer recent |
| over-researching | diminishing returns | set scope boundary and depth level |
| no source tracking | can't verify or revisit | maintain citation table |
