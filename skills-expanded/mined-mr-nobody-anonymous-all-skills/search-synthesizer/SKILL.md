---
name: search-synthesizer
description: Search the web, compare credible sources, and synthesize a cited answer with uncertainty.
category: research
aliases:
- web-search
- synthesize
triggers:
- Search for this
- Synthesize research on a topic
- What does the web say about
- Find information on
- Compare sources on
keywords:
- search
- research
- web
- synthesize
- sources
- compare
- facts
dependencies:
- optional:web-search
risk: low
version: 1.0.0
source: custom
enabled: true
capabilities:
- search-synthesizer
- research
inputs:
- task
- context
outputs:
- result
- report
lifecycle: enabled
author: Mr-Nobody-Anonymous
tags:
- research
- search
- synthesize
- synthesizer
- web
compatibility:
  claude-code: '>=1.0'
  skillhub: '*'
  cursor: '>=0.40'
  codex: '*'
network_access: false
filesystem_access: read
credential_access: false
destructive_operations: false
---

# Search Synthesizer

## Purpose
Search the web for information, evaluate source credibility, compare findings, and
produce a synthesized answer with proper citations and uncertainty acknowledgment.
The skill helps users research topics without hallucination by grounding responses
in verifiable sources.

## When to Use
- The user asks a factual question requiring current web information
- Research requires comparing multiple sources
- The user wants citations for a claim
- Fact-checking a statement

## When NOT to Use
- The question is purely opinion-based
- The topic requires specialized domain expertise beyond web research
- Real-time information (stock prices, live sports) is needed

## Capabilities
- Multi-query web search with source diversity
- Credibility scoring based on domain authority and recency
- Conflict detection when sources disagree
- Structured output with citations
- Uncertainty quantification for low-confidence answers
- Follow-up search suggestion

## Inputs
- `query` (required) — search query or research question
- `num_results` (optional, default: 10) — number of sources to fetch
- `diversity` (optional, default: true) — seek different perspectives
- `format` (optional) — one of: brief, detailed, bullet-points, essay

## Workflow
1. **Decompose** — Break complex questions into search queries
2. **Search** — Execute searches with diverse sources
3. **Extract** — Pull key facts from top results
4. **Evaluate** — Score credibility and recency
5. **Synthesize** — Combine findings into coherent answer
6. **Cite** — Include source URLs with inline references
7. **Qualify** — Mark uncertainty where appropriate

## Tools
- Web search API
- HTTP client for fetching source content
- Text summarization for long pages

## Examples
**User:** "What's the latest on AI regulation in the EU?"
**Response:**
> The EU AI Act passed in March 2024 and entered force in August 2024. Key provisions include:
> - Risk-based classification of AI systems
> - High-risk applications require conformity assessments
> - Prohibited practices (e.g., social scoring)
>
> Sources: [EU AI Act Official](https://digital-strategy.ec.europa.eu...), [Reuters](https://www.reuters.com/...), [TechCrunch](https://techcrunch.com/...)

## Safety
- Distinguish between facts and opinions
- Flag when sources conflict
- Never present speculation as fact
- Include recency dates for all claims
- Acknowledge limitations of web research

## Source
Auto-generated from openclawskills.net description.

## Notes
Maintained as part of canonical research category.
