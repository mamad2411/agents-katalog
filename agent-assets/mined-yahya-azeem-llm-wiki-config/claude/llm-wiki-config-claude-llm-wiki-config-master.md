# CLAUDE.md - LLM Wiki & Agentic Workflow

This file provides guidance to Claude Code when maintaining this knowledge base.

## Project Overview: The LLM Wiki
This repository is an **Andrej Karpathy style LLM Wiki**. It is a compounding knowledge base where the AI acts as the primary librarian and maintainer.

### Directory Structure
- `raw/`: **Immutable Capture Layer.** Drop unorganized notes, web clips, and transcripts here.
- `wiki/`: **Structured Knowledge Layer.** AI-compiled articles, interlinked and organized.
- `assets/`: **Media Layer.** Store images and attachments here.
- `.claude/`: **Agent Intelligence.** Contains skills, rules, and configurations.


## The Karpathy Workflow
When files are added to `raw/`, the LLM should:
1.  **Ingest**: Process the raw file and synthesize it into new or existing wiki articles.
2.  **Compile**: Use professional, structured Markdown.
3.  **Interlink**: Automatically create `[[wikilinks]]` to related concepts.
4.  **Index**: Maintain a central `wiki/_index.md` or topic-specific indices.

### Metadata Schema
Every wiki article MUST include YAML frontmatter:
```yaml
---
title: "Article Title"
tags: [tag1, tag2]
sources: [link1, "File Name"]
last_compiled: 2024-04-24
---
```

## Impeccable Design Constraints
Avoid "AI slop" in any generated UI or visualizations:
- **Typography**: Use intentional rhythm and hierarchy. No generic Inter-only layouts.
- **Color**: Use OKLCH palettes. Avoid purple-to-blue gradients or "generic tech purple."
- **Layout**: Use spatial depth and hierarchy. Avoid nesting cards inside cards recursively.
- **Visuals**: No generic icons. Use high-quality, intentional imagery.

## Slash Commands
- `/ingest`: Process all new files in `raw/` and update `wiki/`.
- `/lint`: Check for broken wikilinks or orphaned pages.
- `/query`: Synthesize an answer from the existing knowledge base.
- `/polish`: Refactor a wiki page for better clarity and depth.

## Rules & Standards
- **Wikilinks**: Use `[[Page Name]]` for internal references.
- **Hierarchy**: Use H1 for titles, H2 for main sections.
- **Language**: Academic but accessible; high signal-to-noise ratio.
- **Persistence**: Never delete raw files; move them to an `archive/` folder after processing if desired.
