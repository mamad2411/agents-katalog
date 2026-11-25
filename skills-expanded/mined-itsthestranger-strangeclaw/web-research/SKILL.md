---
name: web-research
description: Research a topic by formulating searches, evaluating results, and synthesizing well-sourced findings.
version: 1.0.0
tags: [research, web]
---

# Web Research

## When To Use
Use this skill when the task asks for current facts, market or product research, comparisons, background investigation, source-backed summaries, or claims that should be verified against web sources.

Do not use this skill for tasks that can be answered from local repository context alone. If the task concerns a stable concept and the user does not need sources, use normal reasoning unless web verification would materially improve accuracy.

## Research Workflow
1. Clarify the research objective in one sentence before searching.
2. Break broad topics into 2-4 focused search questions.
3. Use `web_search` with specific queries rather than one vague query.
4. Inspect result titles, URLs, and snippets before choosing sources to fetch.
5. Use `web_fetch` on promising primary or high-quality secondary sources.
6. Compare evidence across multiple sources before drawing conclusions.
7. Iterate with narrower searches when sources disagree or gaps remain.
8. Synthesize the answer with clear caveats and source attribution.

## Search Strategy
Prefer queries that include concrete entities, dates, technical terms, or standards names. For recent topics, include the current year or a date constraint in the query when useful. For comparisons, search each side independently before searching for comparison articles.

Start broad enough to discover the vocabulary of the topic, then narrow. If search results are low quality, reformulate the query using terms found in better snippets or fetched pages.

## Source Evaluation
Prefer sources in this order:

- Primary sources: official documentation, standards bodies, government publications, company announcements, source repositories, original research papers, datasets.
- Specialist secondary sources: reputable technical blogs, industry publications, academic reviews, respected news outlets.
- General summaries: useful for orientation, but verify important claims elsewhere.

Treat SEO pages, anonymous reposts, generated-looking content, and unsupported claims as weak evidence. Do not rely on a single weak source for important conclusions.

## Fetching And Reading Sources
Use `web_fetch` for sources that appear directly relevant from search snippets. After fetching, extract the claims, dates, numbers, and named entities that answer the research question. If fetched content is thin, paywalled, unrelated, or mostly boilerplate, discard it and fetch a better source.

When a source mentions another primary source, search for or fetch the primary source before relying on the claim.

## Handling Conflicts And Gaps
If sources disagree, report the disagreement instead of hiding it. Prefer the more primary, more recent, and more specific source when there is a clear quality difference. If the evidence remains insufficient, say what is missing and what conclusion is still uncertain.

## Synthesis Format
For most research tasks, structure the final answer as:

- Direct answer or executive summary.
- Key findings with source-backed evidence.
- Important caveats, uncertainty, or disagreements.
- Source list or inline source attribution, depending on the user's requested format.

Keep the synthesis proportional to the task. Do not dump raw search results. Explain what the evidence supports and what it does not support.
