---
name: social-intake-orchestrator
description: Automated social bookmark ingestion pipeline. Fetches Twitter/X bookmarks (bird-cli) and Instagram saved posts (gram-cli), deduplicates, enriches with AI analysis, and routes into PARA vault as Obsidian markdown. Use when asked to ingest bookmarks, sync social saves, or run the social intake pipeline.
cluster: social-media
version: 1.0.0
---

# Social Intake Orchestrator

## Overview

Pulls saved/bookmarked content from Twitter/X and Instagram, enriches it with AI-generated summaries, topic tags, and Enneagram resonance analysis, then routes each item into the correct PARA vault folder as a fully-formed Obsidian markdown note.

## Pipeline Stages

1. **FETCH** — Pull new bookmarks from bird-cli and gram-cli
2. **NORMALIZE** — Convert platform-specific JSON to unified SocialItem schema
3. **DEDUPE** — SHA-256 hash check against registry to skip already-ingested items
4. **ENRICH** — AI analysis: summary, topic tags, Enneagram type, PARA folder recommendation
5. **ROUTE** — Map to correct PARA vault folder with fallback to Social-Inbox
6. **WRITE** — Create Obsidian .md file with frontmatter, insert MOC backlinks
7. **STATUS** — Write pipeline.json for status/monitoring

## Trigger

Invoke this skill when:
- User asks to "ingest bookmarks", "sync social saves", "pull bookmarks"
- Scheduled task fires on your chosen daily cadence
- User clicks "Hunt" in the monitoring applet

## Execution

Run the orchestrator:

```bash
bun <skills-dir>/social-intake-orchestrator/lib/orchestrator.ts
```

The orchestrator chains all pipeline stages sequentially, writes status updates at each stage, and reports results.

## Configuration

- **Vault path:** `<VAULT>/` (set to your vault root)
- **Hash registry:** `{vault}/.social-intake-hashes.json` (gitignored)
- **Cursor store:** `<STATE_DIR>/cursors.json`
- **Pipeline status:** `<STATE_DIR>/pipeline.json`
- **Auth:** bird uses Firefox profile extraction, gram uses `~/.config/gram/config.json5`

## Auth Prerequisites

Before running, verify both CLIs are authenticated:

```bash
bird check    # Should show ✅ auth_token and ✅ ct0
gram check    # Should show "OK Credentials valid"
```

## Manual Invocation

To run a single ingestion cycle manually:

```bash
# Full pipeline
bun <skills-dir>/social-intake-orchestrator/lib/orchestrator.ts

# With fetch limit
FETCH_LIMIT=10 bun <skills-dir>/social-intake-orchestrator/lib/orchestrator.ts
```
