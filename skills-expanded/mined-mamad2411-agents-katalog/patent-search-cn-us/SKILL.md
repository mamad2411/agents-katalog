---
name: patent-search-cn-us
version: 1.0.0
license: MIT
description: Patent prior-art search and novelty check guidance focused on China and the United States (CNIPA, USPTO, Google Patents, WIPO). Use when asked to plan or run CN/US patent searches, draft search strategies, or produce a preliminary novelty search report.
---

# Patent Search CN/US

## Overview

Plan and execute a preliminary patent search for CN/US, then summarize novelty risks and gaps with a traceable search log.

## Workflow

### 1) Scope the invention
- Extract the core technical problem, steps, and outputs.
- List essential features vs. optional features.
- Capture synonyms in EN + CN (translate key terms both ways).
- Define the jurisdiction scope (CN, US, and optionally WIPO/EPO) and time range.

### 2) Build search queries
- Start with 3-5 keyword clusters (problem, method, system, output, domain).
- Add technical terms, abbreviations, and synonyms; include Chinese equivalents when searching CN.
- If available, map to IPC/CPC classes and include them as filters.
- Add assignee/inventor filters only when narrowing is needed.

### 3) Run searches in public databases
- Use at least one CN database and one US database.
- Include Google Patents as a cross-jurisdiction sweep.
- Optionally use WIPO PATENTSCOPE or Espacenet for broader coverage.
- Reference site list: `references/patent-search-sites.md`.

### 4) Triage and record results
- Scan titles/abstracts; keep candidates that overlap with the essential features.
- Open claims for the top hits; record claim elements that match or differ.
- Keep a log with: database, query, filters, date, and top hits.

### 5) Assess novelty risk
- For each candidate, mark: full match / partial match / non-match.
- Identify distinguishing features (potential novelty points).
- Call out risky overlaps and missing evidence (gaps).

### 6) Produce a preliminary novelty search report
- Include: scope, queries, databases, key hits, and novelty assessment.
- State limitations (public sources only, no paid databases, time constraints).

## Output checklist
- Search scope and assumptions
- Keyword clusters (EN/CN)
- Databases used and date
- Query strings and filters
- Top results summary (title, year, link)
- Novelty assessment and risk notes

## Resources

- `references/patent-search-sites.md`
- `references/open-paper-sites.md`
