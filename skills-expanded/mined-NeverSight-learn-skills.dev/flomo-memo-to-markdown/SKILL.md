---
name: flomo-memo-to-markdown
description: Convert flomo memos from local desktop auth/API into grouped Markdown files for AI/NotebookLM reading, plus human-readable Markdown tag statistics with tree totals. Use when a user asks to export flomo notes to Markdown, split memos by month/quarter/year, generate NotebookLM-friendly archives, or produce flomo tag counts/aggregation.
---

# Flomo Memo To Markdown

## Overview

Convert flomo memos into Markdown files grouped by time range and generate `tag-stats.md` with both `direct_count` and `total_count` per tag node.

This is a standalone export skill. It is not a CRUD helper and should not be used for interactive "find one memo and edit it" requests.

Default behavior is optimized for fast one-shot processing from the local flomo desktop login state: full date range, monthly split, `{{user}}_{{range}}` filenames, and `asset-mode=placeholder`.

## Preconditions

- `flomo.app` has been logged in on this Mac before
- Local flomo storage exists under `~/Library/Containers/com.flomoapp.m/...`
- Network access to flomo API is available if using the local source

## Quick Start

Set the script path from the current environment instead of hardcoding a user directory:

```bash
SKILL_ROOT="${CODEX_HOME:-$HOME/.codex}/skills/flomo-memo-to-markdown"
SCRIPT="$SKILL_ROOT/scripts/flomo_to_nblm.py"
```

Examples:

```bash
python3 "$SCRIPT"
python3 "$SCRIPT" --preview-only
python3 "$SCRIPT" --split quarter --asset-mode copy
```

## Default Agent Workflow

1. Use the local flomo API source.
2. If any local API read step fails, fail fast and return error immediately.
3. Do not fall back to cached exports.
4. Do not ask for exported HTML unless the user explicitly requests postprocessing an archive.
5. Run with defaults unless the user specifies date range / split / naming / asset handling.
6. Report output directory, generated Markdown file count, per-file memo/char counts, threshold warnings, and the `tag-stats.md` path.

## When To Ask Follow-Up Questions

Ask only when one of these materially changes execution:

- The user wants a custom date range
- The user wants a different split granularity
- The user wants a custom filename template
- The user wants copied attachments or explicitly wants to ignore attachments
- Local desktop auth is missing or broken

## Output Behavior

- Default output is decompressed Markdown files
- Also writes `tag-stats.md` in export mode
- `--preview-only` performs parsing, filtering, grouping, and tag stats only
- `--word-limit` is treated as a character count threshold

## Local Source Semantics

- Default input is the local flomo desktop login state, not exported HTML
- The script reads the local desktop auth token from `~/Library/Containers/com.flomoapp.m/.../leveldb`
- Memo bodies come from flomo API `content` HTML and are rendered to Markdown
- Memo timestamps come from `created_at`
- Attachments come from memo `files`
- Tags are re-derived from rendered Markdown text using `#tag` syntax

## Attachment Modes

- `placeholder` (default): Append attachment path lines to memo Markdown; do not copy files
- `ignore`: Ignore attachments entirely
- `copy`: Download signed attachment URLs into `assets/` under the output directory and rewrite Markdown references

## Tag Statistics Semantics

- Tags are extracted from memo plain text using `#tag` syntax
- Counting is deduped per memo
- `direct_count`: memos tagged with this exact tag
- `total_count`: `direct_count` plus all descendant tags

## Resources

### scripts/

- `scripts/flomo_to_nblm.py`: Main converter CLI for local flomo export to grouped Markdown

### references/

- `references/flomo-export-dom.md`: HTML export DOM assumptions and attachment selectors
