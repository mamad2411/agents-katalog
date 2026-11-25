---
name: package
description: Analyze the status, health, completeness, and pipelines of your current skill configuration. Use when the user asks about skill health, package analysis, or to check the status of automation scripts.
---

# Package Analysis Skill (/package)

Analyzes your skill configuration including status monitoring, health assessment, completeness analysis, improvement recommendations, and pipeline optimization insights.

## Quick Start

```bash
python3 _scripts/package_skill.py
```

## What It Analyzes

1. **Status Monitoring** - Scans all skills, tracks last modification
2. **Health Assessment** - 0-100% score based on documentation, structure, recency
3. **Completeness** - Documentation coverage, CLI interface checks
4. **Recommendations** - Actionable improvements with priority levels
5. **Pipelines** - Workflow scripts and optimization opportunities

## Options

- `-d, --days N`: Days of history to analyze (default: 30)
- `-s, --save`: Save analysis report to Sources/
- `-j, --json`: Output JSON instead of Markdown

## Examples

```bash
# Basic analysis
python3 _scripts/package_skill.py

# Save report to Sources
python3 _scripts/package_skill.py --save

# Analyze last 60 days
python3 _scripts/package_skill.py --days 60 --save

# JSON output
python3 _scripts/package_skill.py --json
```

## Output

- Terminal: Markdown report with executive summary, health details, completeness analysis, recommendations, pipeline insights
- Saved report: `Sources/Skill Package Analysis - YYYY-MM-DD.md`
