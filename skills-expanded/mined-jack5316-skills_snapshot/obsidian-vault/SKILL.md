---
name: obsidian-vault
description: Comprehensive vault analytics and health monitoring. Analyze file statistics, tags, links, tasks, and overall vault health. Use when asked about vault statistics, health, analytics, or to check the state of the Obsidian vault.
---

# Obsidian Vault Analytics Skill (/obsidian-vault)

Comprehensive analysis of your Obsidian vault including file statistics, tag usage, link health, task completion, and overall vault health score.

## Quick Start

```bash
python3 _scripts/obsidian_vault_analytics.py
```

## What It Analyzes

1. **File Statistics** - Total files, markdown ratio, folder structure, file types
2. **Tag Analysis** - Tag usage, distribution, and top tags
3. **Link Health** - Orphan files, dead-ends, unresolved links
4. **Task Statistics** - Completion rates, todo/done counts
5. **Properties & Metadata** - Property usage across files
6. **Health Score** - Overall vault health (0-100) with category breakdown

## Options

- `--json`: Output report in JSON format
- `--save`: Save report to Sources/Vault Analytics - YYYY-MM-DD.md

## Examples

```bash
# Basic analytics report
python3 _scripts/obsidian_vault_analytics.py

# Save report to vault
python3 _scripts/obsidian_vault_analytics.py --save

# JSON output
python3 _scripts/obsidian_vault_analytics.py --json
```

## Output

- **Terminal**: Markdown report with health score, file stats, tag analysis, link health, task stats, and recommendations
- **Saved report**: `Sources/Vault Analytics - YYYY-MM-DD.md`

## Health Score Categories

| Category | Weight | Description |
|----------|--------|-------------|
| File Health | 30% | Markdown ratio and organization |
| Link Health | 30% | Graph connectivity |
| Task Health | 25% | Completion rates |
| Activity Health | 15% | Usage patterns |
