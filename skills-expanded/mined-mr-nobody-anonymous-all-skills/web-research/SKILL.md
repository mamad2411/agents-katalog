---
name: web-research
description: Conduct structured web research — query formulation, source diversification, synthesis, and source tracking.
category: research
aliases:
- research
- internet-research
- search
triggers:
- research this topic
- research this
- look this up
- find information about
- what does the internet say
- search for
keywords:
- research
- search
- web
- lookup
- find
- information
- query
dependencies: []
risk: low
version: 1.0.0
source: custom
enabled: true
author: Mr-Nobody-Anonymous
tags:
- lookup
- research
- search
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

# Web Research

## Purpose

Conduct structured, well-sourced web research. Decompose a question, search diversely,
extract claims, track sources, and synthesize an answer.

## When to Use

- User asks a question that requires current / external information
- User wants a summary of a topic
- User wants citations / sources

## When NOT to Use

- The user wants a primary source they're handing you (route to `summarization` or `document-extraction`)
- The question is well-known and answerable from general knowledge

## Capabilities

- Query decomposition
- Source diversification (official, scholarly, news, community)
- Snippet extraction
- Source tracking
- Synthesis with attribution

## Inputs

- The research question
- Desired depth (quick scan vs. deep dive)
- Required recency

## Workflow

1. **Decompose.** Break the question into 2–5 sub-questions.
2. **Search diversely.** Use multiple queries and source types. Note exact queries run.
3. **Extract claims.** Capture specific claims with their source URL and date.
4. **Triangulate.** Where multiple sources agree, confidence is higher. Where they disagree, surface the disagreement.
5. **Synthesize.** Compose an answer that cites sources inline.
6. **Flag uncertainty.** Be explicit about what's well-established vs. contested vs. unknown.

## Tools

- Web search (via agent's tools)
- Browser tool for primary sources
- Note-taking surface for source tracking

## Safety

- Don't trust single sources for high-stakes claims
- Surface conflicts of interest in sources
- Note when sources are out-of-date

## Source

Custom skill, written for this library.

## Notes

Pairs with:
- `source-verification`
- `fact-checking`
- `summarization` (after research)
- `academic-research` (when scholarly sources needed)

## Examples

Requests that should activate this skill include: "research this"; "look this up"; "find information about".
