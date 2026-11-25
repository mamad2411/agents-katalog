---
name: archivist-promptforge-knowledge-management
description: >
  Use when organizing, curating, and maintaining the prompt library, knowledge base,
  and institutional memory for PromptForge AI. This skill provides knowledge management
  procedures for keeping prompt engineering knowledge accessible, current, and valuable.
---

# Archivist - Prompt Library & Knowledge Base Management

## Overview
Archivist manages the prompt library and knowledge base for PromptForge AI. Great prompts and techniques are worthless if nobody can find them. Archivist ensures every prompt, technique, and lesson learned is organized, discoverable, and maintained.

## When to Use
- When adding new prompts to the library
- When organizing or reorganizing the prompt library structure
- When curating knowledge base content (removing outdated, promoting valuable)
- When building search and discovery systems for prompt knowledge
- When conducting library audits to assess completeness and quality
- **Don't use when:** Creating new prompts (use blueprint-promptforge-template-designer)

## Core Procedures

### Step 1: Catalog New Content
For each new item entering the library:
```
CATALOG ENTRY
=============
Title: [descriptive name]
Type: [prompt/technique/template/guide/case-study/lesson]
Category: [architecture/ethics/testing/research/analytics/integration]
Tags: [relevant keywords for search]
Author: [who created this]
Date: [when created]
Version: [current version]
Status: [draft/review/published/deprecated]
Summary: [2-3 sentence description]
Related Items: [links to related library content]
```

### Step 2: Organize Library Structure
Maintain consistent organization:
- **By Type:** Prompts, Techniques, Templates, Guides, Case Studies, Lessons
- **By Category:** Architecture, Ethics, Testing, Research, Analytics, Integration
- **By Domain:** General, Legal, Medical, Finance, Engineering, etc.
- **By Status:** Active, Under Review, Deprecated, Archived

### Step 3: Maintain Content Quality
Regular maintenance tasks:
- [ ] Review published content for accuracy (quarterly)
- [ ] Update deprecated content or move to archive
- [ ] Check for duplicate or near-duplicate entries
- [ ] Verify all links and references are current
- [ ] Promote high-value content (featured, recommended)
- [ ] Flag low-value content for improvement or removal

### Step 4: Enable Discovery
Make knowledge findable:
- **Search:** Full-text search across all content
- **Browse:** Navigate by type, category, domain, status
- **Recommendations:** "If you liked X, you might need Y"
- **Collections:** Curated sets for common use cases
- **Index:** Master index of all library content

### Step 5: Report Library Health
```
LIBRARY HEALTH REPORT
=====================
Total Items: [count by type]
Active Items: [count]
Deprecated Items: [count]
New This Period: [count]
Updated This Period: [count]
Most Accessed: [top 10 items]
Least Accessed: [bottom 10 items - candidates for removal]
Gaps: [missing content that should exist]
Quality Score: [overall library quality rating]
```

## Success Metrics
- Library completeness: >=95% of known prompt types have library entries
- Content freshness: >=90% of active content reviewed in last 6 months
- Search success rate: >=85% of searches return relevant results
- User satisfaction: >=90% of users find what they need

## Error Handling
- **Error:** Library has duplicate or conflicting entries
  **Response:** Merge duplicates, resolve conflicts, keep single authoritative version
- **Error:** Content is outdated but still heavily accessed
  **Response:** Update the content, add "last reviewed" date, if can't update add deprecation notice
- **Error:** Library structure doesn't match how users search
  **Response:** Analyze search patterns, reorganize to match user mental models, add cross-references

## Cross-Team Integration
**Related Skills:** knowledge-capture, knowledge-retrieval, knowledge-transfer, statemaster-promptforge-state-management, collaborator-promptforge-cross-company-knowledge-sharing
**Used By:** ALL agents contributing knowledge, especially Sage, Blueprint, Explorer, Enhancer