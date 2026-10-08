---
name: lat-md-knowledge-graph
description: >
  Design or audit a repo-local markdown knowledge graph with wiki links,
  source-code backlinks, drift checks, and searchable sections. Use when
  AGENTS.md/CLAUDE.md is too flat for a large codebase or when a custom
  harness needs durable structured project memory.
---

# lat.md Knowledge Graph

## Purpose

Turn durable project knowledge into linked markdown files that agents can
search, cite, and keep synchronized with code.

## When to Use

- One root instruction file is too large or hides domain decisions.
- Agents repeatedly rediscover the same architecture or business rules.
- Test intent needs explicit specs linked to test code.
- A custom harness needs persistent memory outside conversation history.

## Design Pattern

1. Create a repo-local knowledge directory such as `lat.md/` or `docs/knowledge/`.
2. Split pages by durable concepts: architecture, domain rules, workflows,
   interfaces, test specs, and operational constraints.
3. Link concepts with `[[wiki links]]`.
4. Link knowledge pages to source symbols or files.
5. Add code backlinks such as comments or metadata where the code implements a
   documented rule.
6. Add a check that fails on broken links, missing backlinks, stale indexes, or
   test specs without code mentions.

## ctx Fit

Use this alongside ctx's LLM-wiki when a project needs its own local memory
graph. ctx recommends skills/MCPs/agents from its catalog; the repo-local graph
stores project-specific facts that should not live in the global catalog.

## Quality Bar

- Page titles and section anchors are stable.
- Links resolve both ways where needed.
- Code backlinks are narrow and reviewable.
- Checks run in CI before merge.
- Sensitive facts stay out unless the repo already allows them.
- The graph explains current behavior, not a speculative roadmap.
