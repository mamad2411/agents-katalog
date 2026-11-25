---
name: clean
description: Find and remove redundant notes with your permission. Detects exact duplicates, empty/stub notes, and optional near-duplicates. Always asks before removing. Use when you want to clean the vault, remove duplicates, or declutter notes.
---

# Clean Skill (/clean)

Find and remove redundant notes in your Obsidian vault. Always asks for explicit permission before removing any file.

## What It Detects

1. **Exact Duplicates** — Notes with identical content (keeps one copy per group)
2. **Empty / Stub Notes** — Notes with &lt; 50 characters of content
3. **Near-Duplicates** — Notes ≥90% similar (optional, for manual review)

## Quick Start

```bash
# Scan only — find redundancies, no removal
python3 _scripts/clean_redundant.py scan

# Clean — scan, then ask before removing
python3 _scripts/clean_redundant.py clean
```

## Options

- `scan` — Find redundancies only, no removal
- `clean` — Find redundancies and remove with your permission
- `--duplicates` — Include exact duplicates in removal (keeps one per group)
- `--stubs` — Include empty/stub notes in removal
- `--near-duplicates` — Include near-duplicate detection (slower, manual review)
- `--save` — Save scan report to `Sources/Clean Report - YYYY-MM-DD.md`
- `--folder PATH` — Limit scan to a specific folder (e.g., Sources, Atlas)
- `-y, --yes` — Skip confirmation (use with caution)

## Examples

```bash
# Scan and save report
python3 _scripts/clean_redundant.py scan --save

# Clean duplicates and stubs (will prompt for confirmation)
python3 _scripts/clean_redundant.py clean

# Only remove stub notes
python3 _scripts/clean_redundant.py clean --stubs

# Only remove exact duplicates (keeps one per group)
python3 _scripts/clean_redundant.py clean --duplicates

# Scan Sources folder only
python3 _scripts/clean_redundant.py scan --folder Sources

# Clean with near-duplicate detection
python3 _scripts/clean_redundant.py clean --near-duplicates
```

## Output

- **Terminal**: Markdown report with duplicate groups, stub list, and removal summary
- **Saved report**: `Sources/Clean Report - YYYY-MM-DD.md` (when `--save` used)

## Safety

- **No removal without permission** — `clean` mode always prompts before deleting
- **Excluded directories** — `.obsidian`, `.trash`, `_scripts`, `.claude`, etc. are never scanned
- **Duplicate handling** — For exact duplicates, keeps the "first" file (by path) and removes the rest
