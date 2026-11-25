---
name: obsidian-medical-knowledge
description: Use when organizing clinical research notes, medical concepts, tags, Dataview pages, or knowledge graph workflows in Obsidian.
---

# Obsidian Medical Knowledge

## Goal

Organize medical research notes in a way that remains traceable, reviewable, and safe for non-programmer clinicians.

## Required Behavior

1. Preserve original source notes.
2. Do not rewrite raw source material as if it were verified clinical advice.
3. Keep concepts, claims, and references separated.
4. Use clear tags and frontmatter when the vault already uses them.
5. Avoid bulk reorganizing the vault unless explicitly requested.

## Suggested Note Shape

```md
---
type: literature-note
status: unverified
topic:
source:
reviewed_by_human: false
---

# Title

## Source Facts

## Interpretation

## Links

## Questions for Review
```

## Safety Defaults

- Do not include real patient identifiers.
- Mark unverified notes clearly.
- Keep source links visible.
- Prefer small incremental changes.

