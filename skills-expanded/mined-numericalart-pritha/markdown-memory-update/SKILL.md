---
id: skill-markdown-memory-update
type: agent-skill
status: reviewed
created: 2026-05-30
updated: 2026-05-30
name: markdown-memory-update
description: Update Markdown-first agent memory while keeping raw input, curated notes, decisions and generated navigation layers separate.
version: 0.1.0
topics:
  - agent-skills
  - markdown-memory
  - indexing
tools:
  - Pritha
  - Markdown
sources:
  - 04_standards/memory-structure.md
  - 07_workflows/memory-indexing.md
  - docs/memory.md
related:
  workflows:
    - 07_workflows/agent-skill-pack-selection.md
source: pritha-memory
source_paths:
  - 04_standards/memory-structure.md
  - 07_workflows/memory-indexing.md
  - docs/memory.md
review_status: reviewed
trust_level: local-reviewed
requires_toolsets:
  - filesystem
  - markdown
risk_level: low
tags:
  - markdown
  - memory
  - indexing
---

# Markdown Memory Update

## When to Use

Use when an agent needs to add or revise durable memory in Markdown files.

## Procedure

1. Keep raw material separate from curated knowledge.
2. Add YAML frontmatter to every new curated Markdown artifact.
3. Link sources, related artifacts, superseded artifacts and replacement artifacts when known.
4. Keep generated navigation or wiki pages out of the authoritative decision path.
5. Rebuild or validate indexes only after Markdown source files are coherent.

## Pitfalls

- Do not store secrets in memory.
- Do not treat SQLite, embeddings or generated wiki as the canonical authored source.
- Do not rewrite unrelated memory files as cleanup during a narrow update.

## Verification

- Frontmatter contains required fields.
- Source paths are stable.
- Related and supersession fields are updated when applicable.
- Index rebuild or validation command is documented if needed.
