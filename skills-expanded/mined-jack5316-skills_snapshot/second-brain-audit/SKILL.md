---
name: second-brain-audit
description: Second brain audit — vault health + PARA check. Runs obsidian-vault, obsidian-links, obsidian-tasks, knowledge-graph, and clean. Use when user asks for second brain audit, vault health check, PARA audit, knowledge base audit, or /second-brain-audit.
---

# Second Brain Audit Skill (/second-brain-audit)

Comprehensive audit of your Obsidian vault: health metrics, link structure, tasks, PARA organization (Inbox/Projects/Areas/Resources/Archive), and redundant notes.

## Quick Start

```bash
python3 _scripts/pipeline.py --run second-brain-audit
```

## What It Runs

1. **obsidian-vault** — File stats, tags, links, tasks, health score
2. **obsidian-links** — Orphans, dead-ends, unresolved links, hubs
3. **obsidian-tasks** — Task completion and priorities
4. **knowledge-graph** — PARA structure, content categories, connectivity
5. **clean** — Redundant notes scan (no deletion without permission)

## Options

```bash
# Verbose (stream output)
python3 _scripts/pipeline.py --run second-brain-audit -v

# Continue even if a step fails
python3 _scripts/pipeline.py --run second-brain-audit --no-fail-stop
```

## Output

Reports from each skill; use `--save` on individual skills to persist to vault (e.g. `Sources/Vault Analytics - YYYY-MM-DD.md`).
