
---
name: knowledge-graph
description: Comprehensive knowledge graph overview of your Obsidian vault. Visualize directory structure, file categories, knowledge hubs, thematic tags, and overall vault architecture. Use when you want a holistic picture of your knowledge graph, vault structure, or to understand how your knowledge is organized.
---

# Knowledge Graph Skill (/knowledge-graph)

Comprehensive visual and structural overview of your Obsidian vault providing a holistic picture of your knowledge graph.

## Quick Start

```bash
python3 _scripts/knowledge_graph.py
```

## Features

1. **Vault Architecture** - High-level metrics at a glance (total files, folders, connectivity)
2. **Directory Structure** - Complete folder organization with file counts
3. **Content Categories** - Files grouped by purpose (Sources, Atlas, Maps, Projects, etc.)
4. **Knowledge Hubs** - Top 25 most connected files (hubs with most backlinks + outgoing)
5. **Thematic Tags** - Tag analysis with grouping by prefix
6. **Connectivity Health** - Orphan and dead-end file statistics

## Options

- `--save`: Save report to vault

## Examples

```bash
# Generate knowledge graph report
python3 _scripts/knowledge_graph.py

# Save report to vault
python3 _scripts/knowledge_graph.py --save
```

## Output

- **Terminal**: Markdown report with architecture overview, directory structure, content categories, knowledge hubs, thematic tags, and connectivity health
- **Saved report**: `Sources/Knowledge Graph - YYYY-MM-DD.md`

## What It Shows You

| Section | Purpose |
|---------|---------|
| **Vault Architecture** | Quick stats showing the scale of your knowledge graph |
| **Directory Structure** | How your files are organized across folders |
| **Content Categories** | Distribution of files by type (Sources, Atlas, Maps, etc.) |
| **Knowledge Hubs** | The most important files that anchor your knowledge graph |
| **Thematic Tags** | The main topics and themes in your vault |
| **Connectivity Health** | How well your knowledge is interconnected |

## Use Cases

- Get a quick overview of your entire vault structure
- Identify the most important hub files in your knowledge graph
- Understand how your knowledge is thematically organized
- Assess the overall connectivity of your knowledge graph
- See the distribution of content across different categories
