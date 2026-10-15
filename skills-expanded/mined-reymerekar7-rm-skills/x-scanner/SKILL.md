---
name: x-scanner
description: >
  Scan X/Twitter for recent posts from a curated list of AI creators and news accounts
  using xAI's Grok API with the x_search tool. Use this skill whenever the user asks to:
  check what's happening on AI Twitter, scan X for news, pull recent tweets from creators,
  get an AI news digest, find trending AI topics, or generate content ideas from X. Also
  trigger when a scheduled news-scan task runs. This skill requires an xAI API key.
---

# X/Twitter Scanner

## What This Does

Uses xAI's Grok API with the built-in `x_search` tool to scan X/Twitter for recent posts
from AI-focused accounts. Grok has native access to X data, so one API call handles search,
filtering, and summarization. No separate Twitter API credentials needed.

The scan produces a structured digest tagging launches, tools worth trying, learning
material, build ideas, and content angles — with a coverage check so your must-watch
accounts never silently drop out.

## Setup

The script reads the xAI API key from the environment first, then falls back to a `.env`
file (it walks up the directory tree to find one). Either works:

```bash
export XAI_API_KEY=your_xai_api_key_here
# or add to a .env file at your project root:
# XAI_API_KEY=your_xai_api_key_here
```

Get an API key from https://x.ai/api. No external Python packages are needed — the script
uses the standard library only.

## Configuring Who You Track — `watchlist.json`

Accounts live in `watchlist.json` next to the `scripts/` folder. **Edit that file, not the
script**, to track whoever you want. It has two parts:

- **`must_surface_handles`** — accounts the scan always tries to cover. If one is missed on
  the first pass, the scanner automatically re-scans just those handles and merges them in.
  A coverage footer reports how many were surfaced.
- **`groups`** — everyone else, organized into named buckets (AI labs, builders, news, etc.).
  Each group is scanned together, and grouped scans kick in as a fallback if a broad pass
  comes back thin. Handles can be plain strings or `{ "handle": "...", "note": "..." }`
  objects — notes are just for your own reference.

If `watchlist.json` is missing or invalid, the script falls back to a small set of baked-in
default handles so it still runs.

## How It Works

The script calls `https://api.x.ai/v1/responses` with the `x_search` tool enabled. Grok
searches X in real-time and returns a summarized digest. The scanner adds reliability on top:

1. **Broad pass** over all watchlist accounts.
2. If the result is thin or misses required accounts, it **escalates** — scanning curated
   groups separately, then falling back to a must-surface-only scan.
3. It **re-scans** any still-missing required handles and merges them in.
4. It appends a deterministic **coverage check** and exits non-zero if nothing usable came back.

## Digest Structure

Every account scan returns these sections:

- **FLAGGED** — high-signal posts: launches, real revenue/growth numbers, contrarian takes,
  adoption-worthy workflows, or viral engagement.
- **TRY THIS** — concrete tools, models, APIs, or integrations you can go use right now.
  Publicly callable models, free-tier or open-source releases, new API capabilities, or
  replicable "here's exactly how" posts. Not research papers, waitlists, or "coming soon."
- **LEARN NEXT** — educational content worth studying (frameworks, tutorials, becoming-table-stakes skills).
- **BUILD IDEAS** — concrete product/automation/agent ideas inspired by the scan.
- **CONTENT ANGLES** — angles usable across LinkedIn, X, newsletter, or short-form video.
- **TOP FEED** — remaining notable posts, ranked by relevance.
- **COVERAGE CHECK** — how many must-surface handles were surfaced, and which were missed.

## How to Use

### Quick scan (default — last 48 hours)
```bash
python <skill-directory>/scripts/scan_x.py
```

### Custom time window
```bash
python <skill-directory>/scripts/scan_x.py --hours 6
```

### Specific accounts only (skips the fallback machinery — scans exactly what you pass)
```bash
python <skill-directory>/scripts/scan_x.py --handles karpathy sama AnthropicAI
```

### Freeform X search
```bash
python <skill-directory>/scripts/scan_x.py --query "Claude Code update"
```

### Summary only (no JSON wrapper)
```bash
python <skill-directory>/scripts/scan_x.py --summary-only
```

Output is JSON to stdout with a `summary` field containing Grok's digest (or just the digest
text with `--summary-only`). The script exits with code `2` if the scan returned nothing usable.

## Default Workflow

1. Run `scan_x.py` to pull recent posts via the xAI Grok API.
2. If the script fails (key expired, rate limited), fall back to a web search with queries
   like "AI news today", "Claude update", "OpenAI announcement".
3. Present the digest to the user, leading with FLAGGED and TRY THIS.
4. **STOP here.** Don't generate downstream content or push to any external tool unless the
   user explicitly asks.

## Automated Scanning

`scripts/scheduled_scan.sh` writes a timestamped digest to a `digests/` folder next to the
script — wire it into cron for hands-off daily scans:

```bash
# Scan twice a day at 8am and 8pm
0 8,20 * * * /path/to/skills/x-scanner/scripts/scheduled_scan.sh
```
