---
name: seer-shared
version: 0.3.0
description: Seer CLI shared concepts, response format, config, and common rules
metadata: {"requires":{"bins":["seer-q"]}}
---

# Seer Shared

Foundational knowledge for all Seer skills. Read this before using any domain skill.

## What Seer Is

Seer is the intelligence engine behind **Midaz — the Interactive Cognitive Trading Map**. It tracks:

- **Claims** — atomic evidence statements extracted from sources (the raw events/facts)
- **Threads** — tradable angles / sub-theses built from clusters of claims
- **Topics** — narrative domains that group related threads (e.g., "AI Infrastructure", "Energy Transition")
- **Global snapshot** — overall market regime derived from top drivers across all topics

All queries use the `seer-q` CLI.

## The Web UI

Every `view_url` opens the Midaz web app — a 3D interactive map that's much easier to explore than reading JSON:

- **Topic sphere** — click any topic node to zoom into its threads, then drill down to individual claims
- **Driver graph** — causal links between market drivers as a force-directed network you can rotate and explore
- **Verdict rail** — real-time regime summary with conviction level and key uncertainties

The links are deep-linkable: each `view_url` opens the map focused on exactly the right entity. Text summaries are useful, but the map shows relationships and context that's hard to convey in words — so always include the link and let the user know what they'll find there.

## Response Format

All commands return JSON:
- **Success** (stdout): `{ "ok": true, "data": <payload>, "meta": { "view_url": "...", "count": N } }`
- **Errors** (stderr): `{ "ok": false, "error": { "code": "...", "message": "..." } }`

Access the payload via `.data`. The page-level `view_url` is always in `.meta.view_url` — read it from `.meta`, not `.data`. Per-entity URLs (e.g., each topic or thread) appear as `view_url` fields on objects inside `.data`.
For raw API output (no envelope), use `--raw`.

### Global Flags

| Flag | Default | Description |
|------|---------|-------------|
| `--format` | `json` | Output format: `json` or `pretty` |
| `--raw` | false | Raw API response (no envelope) |
| `--api-url` | from config | Override API base URL |

## Setup

Install skills to agent directories (no npm required):

```bash
seer-q setup auto --yes            # Install to detected agent directories
seer-q setup claude --yes          # Install to Claude Code
seer-q setup codex --yes           # Install to Codex
seer-q setup all --yes             # Install to all known targets
seer-q setup auto --dry-run        # Preview without writing
```

## Config & Diagnostics

```bash
seer-q version                  # CLI version, Go version, OS/arch
seer-q doctor                   # Verify API connectivity and config
seer-q config get <key>         # Get config value
seer-q config set <key> <value> # Set config value
seer-q config list              # Show active configuration
seer-q config path              # Show config file path
seer-q schema                   # List all command contracts
seer-q schema <command>         # Describe a command's input/output contract
seer-q health                   # API health check
```

## Common Rules

1. Use `seer-q search` first whenever the user mentions a specific entity, asset, or theme
2. **Always include `view_url` as clickable markdown links.** The page-level URL is in `.meta.view_url`. Per-entity URLs (topics, threads) are on each object inside `.data`. Format as `[descriptive text](url)` — never paste raw URLs. Example: `[Explore this topic on the interactive map](https://www.midaz.xyz/market?topic=abc123)`.
3. Synthesize data into natural language — don't dump raw JSON
4. For multi-entity questions, make multiple calls to build a complete picture
5. When claims are asked about, note their `claim_mode`, `thread_role` (support/contradiction), and `event_date`
