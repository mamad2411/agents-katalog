---
name: obsidian-links
description: Knowledge graph and link structure analysis. Detect orphan files, dead-ends, unresolved links, find central hubs, and assess overall link health. Use when asked about links, graph connectivity, orphans, or knowledge graph health.
---

# Obsidian Link Analyzer Skill (/obsidian-links)

Comprehensive analysis of your knowledge graph including orphan detection, dead-end identification, unresolved links, central hub discovery, and connectivity health scoring.

## Quick Start

```bash
python3 _scripts/obsidian_link_analyzer.py
```

## Features

1. **Orphan Detection** - Files with no incoming links
2. **Dead-end Identification** - Files with no outgoing links
3. **Unresolved Links** - Broken links to non-existent files
4. **Central Hubs** - Most connected files (MOCs)
5. **Connectivity Score** - Overall graph health (0-100)
6. **Recommendations** - Actionable improvements

## Options

- `--orphans`: Show only orphan files
- `--deadends`: Show only dead-end files
- `--hubs`: Show central hub files
- `--file PATH`: Analyze links for a specific file
- `--save`: Save report to Sources/Link Analyzer Report - YYYY-MM-DD.md

## Examples

```bash
# Full link health report
python3 _scripts/obsidian_link_analyzer.py

# Show only orphan files
python3 _scripts/obsidian_link_analyzer.py --orphans

# Show only dead-end files
python3 _scripts/obsidian_link_analyzer.py --deadends

# Show central hub files
python3 _scripts/obsidian_link_analyzer.py --hubs

# Analyze specific file
python3 _scripts/obsidian_link_analyzer.py --file "Note.md"

# Save report
python3 _scripts/obsidian_link_analyzer.py --save
```

## Health Score Calculation

The link health score (0-100) is calculated as:

- **Base Score**: 100 points
- **Orphan Penalty**: -0.5 points per percentage of orphan files
- **Dead-end Penalty**: -0.3 points per percentage of dead-end files
- **Unresolved Penalty**: -2 points per unresolved link (max 20 points)

## What It Identifies

| Type | Description | Why It Matters |
|------|-------------|-----------------|
| **Orphans** | Files with no incoming links | Isolated from knowledge |
| **Dead-ends** | Files with no outgoing links | Terminal nodes |
| **Unresolved** | Links to non-existent files | Broken connections |
| **Hubs** | Files with most backlinks | Knowledge centers |

## Output

- **Terminal**: Markdown report with health score, link graph overview, central hubs, orphan files, dead-end files, unresolved links, and recommendations
- **Saved report**: `Sources/Link Analyzer Report - YYYY-MM-DD.md
