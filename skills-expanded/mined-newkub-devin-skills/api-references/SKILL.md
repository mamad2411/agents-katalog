---
name: deep-research-api-references
description: Find API references from many sources — official docs, examples, type surface — with citations
argument-hint: "[api-or-library]"
related:
  - deep-research
  - follow-best-practice
  - learn
  - check-reference
  - check-types-definition
  - ask-me
---

## Goal

Find trustworthy API references for a given API, library, or tool — summarized as a cited list (merged `/research-api-references`)

## Scope

Use when you need references for a new API/library/tool or want to verify an existing one — searched from multiple sources under the deep-research pipeline

## Execute

### 1. Parse Query

> Goal: understand what to search for

1. Read the API/library/tool name from the argument
2. Define the scope: version, language, framework, platform + data type (official docs, examples, tutorials, benchmarks)
3. If the query is unclear → use `/ask-me` first

### 2. Plan Research

> Goal: set the search strategy

1. Pick primary sources: official docs, GitHub repo, NPM registry, DeepWiki, Context7
2. Define sub-queries for cross-referencing — order: official → code repo → community

### 3. Gather References

> Goal: collect references from multiple sources

1. Run the general `/deep-research` pipeline with the main query
2. Use `/learn-from-web` to read specific official docs when a URL exists
3. Type surface (options, defaults, signatures) → `/check-types-definition` on the real type defs
4. Use `/follow-best-practice` if looking up best practices for that API
5. Record the source, URL, version, and credibility of each reference

### 4. Synthesize References

> Goal: summarize the search results

1. Filter duplicate references — group by category (official, examples, tutorials, comparisons)
2. Rank by credibility/relevance — summarize 2-5 key takeaways

### 5. Format Output

> Goal: present it in a readable form

1. Markdown table or numbered list — include URL, short description, source, year/version
2. Use the same language as the query — show results inline in the chat

## Rules

- Official docs are always the primary source; GitHub repos for source/examples; registries for package info; community sources only as a fallback
- Always go through the research pipeline — no single superficial search; if no data is found, report the gaps
- Credibility: check year/version, maintenance status (last commit, release), flag uncertain information
- No execution — do not modify project files, do not install dependencies
- Use `/check-reference` when needed

## Expected Outcome

- A complete, de-duplicated list of API references — official as primary, with URL/version/takeaways — handoff to `/follow-best-practice` or `/learn-from-web` possible
