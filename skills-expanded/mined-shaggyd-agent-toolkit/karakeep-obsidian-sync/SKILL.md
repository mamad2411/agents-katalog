---
name: karakeep-obsidian-sync
description: Full CRUD CLI for Karakeep — standalone bookmarking tool with optional Obsidian vault sync
version: 0.5.1
author: Dustin Chadwick
metadata:
  hermes:
    tags: [karakeep, obsidian, bookmarking, sync, cli, crud]
---

# Karakeep ↔ Obsidian Sync

A CLI tool for [Karakeep](https://github.com/karakeep-app/karakeep) (self-hosted bookmarking). All CRUD commands work standalone — Obsidian vault sync is an optional add-on.

**Author:** Dustin "Dusty" Chadwick ([@ShaggyD](https://github.com/ShaggyD))

## CLI Tool: `kk`

Single-file Python script — zero external dependencies.

### Commands

| Command | Description |
|---------|-------------|
| `kk login <url> <key>` | Connect to a Karakeep instance |
| `kk logout` | Wipe saved config and state |
| `kk list [--limit N]` | List recent bookmarks |
| `kk get <id>` | View bookmark as JSON |
| `kk add <url>` | Save a URL bookmark |
| `kk text <content>` | Save a plain text bookmark |
| `kk note <id> [text]` | View/update a bookmark's note |
| `kk edit <id> --title= --note=` | Update title, note, archived, favourited |
| `kk tag <id> <tag>...` | Attach tags |
| `kk untag <id> <tag>...` | Detach tags |
| `kk delete <id>` | Delete a bookmark |
| `kk sync [--enrich]` | Pull new bookmarks → vault; --enrich fetches transcripts/content |
| `kk push` | Push vault note changes → Karakeep (if configured) |
| `kk enrich <id>` | Fetch YouTube transcript or article content for a single bookmark |
| `kk enrich --next` | Enrich the next un-enriched YouTube bookmark (newest first) |
| `kk enrich --list` | Show YouTube enrichment queue and progress |
| `kk config [--set key=val]` | Show or update configuration |

None of the CRUD commands (`list`, `get`, `add`, `text`, `note`, `edit`, `tag`, `untag`, `delete`) require a vault. Sync and push only work if `vault_path` is configured.

## Quick Start (standalone — no vault needed)

```bash
# Install
cp kk ~/.local/bin/ && chmod +x ~/.local/bin/kk

# Connect
kk login https://hoarder.example.com ak2_your_api_key_here

# Use
kk list
kk add https://example.com/article
kk note <id> "My thoughts on this"
```

## Optional: Obsidian Vault Sync

After login (or later), configure vault sync:

```bash
kk config --set vault_path=~/my-vault/003_Resources/Bookmarks
kk config --set daily_path=~/my-vault/002_Journal/daily   # optional
kk sync   # initial pull
```

The `login` command also offers an interactive vault setup prompt.

### What sync does

- Creates a `_Index.md` in your bookmark directory with Dataview-powered Recently Added and By Tag tables
- Each bookmark becomes a `.md` file with frontmatter (source, URL, tags, author)
- Backlinks point to `[[_Index|Bookmarks]]` (relative — works from any folder)
- Optional: appends a cross-reference to today's daily note if `daily_path` is configured

### What push does

Scans your vault for edited `## Notes` sections and pushes changes back to the bookmark's note field in Karakeep.

### Enrichment

Bookmarks can be enriched with additional content before saving to the vault:

| Type | Enrichment | How |
|------|-----------|-----|
| YouTube links | Full transcript (25K+ chars) | `youtube-transcript-api` via `uv run --with` |
| Article links | Readable text extraction | `curl` + Python's built-in `html.parser` |

**Commands:**
- `kk enrich <id>` — enrich a single bookmark and preview the result
- `kk enrich --next` — auto-find the next un-enriched YouTube bookmark (newest first) and add transcript to the vault note
- `kk enrich --list` — show progress: total YouTube bookmarks, how many enriched, how many remaining
- `kk sync --enrich` — sync new bookmarks and auto-enrich each one

**Pacing pattern:** For existing bookmarks, use `kk enrich --next` in a daily cron to process one per day. This avoids hammering the API and gives you a daily artifact to review. Typical pace: 26 bookmarks → ~1 month to catch up.

Enrichment is best-effort. If fetching fails (no uv, no curl, network timeout), the note is still saved with Karakeep's existing content. The cron default is `kk sync` without `--enrich` because enrichment adds latency (transcript fetching, page downloads).

### Vault path inference

When `daily_path` is not explicitly set, the tool infers it from `vault_path` using a PARA-structure heuristic. See `references/vault-path-inference.md`.

### Automation (cron)

```cron
# Daily sync + enrichment (both run at midnight, enrich 10 min later)
0 0 * * * /home/user/.local/bin/kk sync
10 0 * * * /home/user/.local/bin/kk enrich --next
```

Push has no cron by default — editing notes in your vault should be intentional.

## Note Format

```yaml
---
created: 2026-04-30 05:49
source: karakeep
karakeep_id: <full-bookmark-id>
source_url: <original-url>
author: <author>
publisher: <publisher>
tags: [tag1, tag2]
---
```

No personal tags or conventions are baked in. Notes link back to `[[_Index|Bookmarks]]` which works from any vault folder structure.

## Design Principles for General Distribution

This skill was refactored from a personal tool to a distributable one. Key lessons embedded in the design:

- **CLI-first, features second.** The core CRUD commands must work without any vault configuration. Sync and push are opt-in.
- **No default paths.** Never write files to a location the user didn't explicitly configure.
- **Interactive onboarding, but skippable.** `kk login` asks about vault setup, but you can hit enter to skip and configure later.
- **Relative backlinks.** `[[_Index|Bookmarks]]` works from any vault folder — no hardcoded paths.
- **No personal conventions.** Status tags, PARA structure assumptions, and author-specific frontmatter fields are excluded from generated content.
- **YouTube Shorts support.** `_extract_youtube_id` must handle `/shorts/` URLs — these URLs don't match `/watch`, `/embed/`, or `/v/` patterns. Without it, Shorts fall through to article enrichment and never get a `## Transcript` section, creating an infinite loop in `--next`.
- **Graceful degradation.** If uv or curl are missing, enrichment silently skips rather than crashing. The note still gets created.
- **Best-effort enrichment.** YouTube transcripts via uv (tool installed on-the-fly, no permanent dependency — see `references/uv-adhoc-deps.md`). Article text via curl + stdlib HTML parsing. Failures don't block the sync.

## Known Pitfalls

- **API key in plaintext** — stored at `~/.config/kk/config.json`. Recommended: `chmod 600 ~/.config/kk/config.json`
- **User-Agent block** — Karakeep blocks Python's default `urllib` UA. The tool sets `User-Agent: kk-cli/0.5`
- **Full IDs required** — use full bookmark IDs from `kk list`. Truncated IDs return 404
- **Tag format** — the API expects `{"tagName": "..."}` objects, not strings. Handled internally
- **Clearing a note:** `kk note <id> ""` clears a bookmark's note field
- **Filename collisions** — bookmarks without a title/content map to `unknown-untitled.md`
- **Python 3.7+ required** (for `pathlib` and `datetime.fromisoformat`)
- **Empty DELETE responses** — API returns 204 No Content. Tool handles empty body gracefully
- **`--next` vs `--list` discrepancy with orphan bookmarks** — `kk enrich --next` only processes vault files that have a non-empty `karakeep_id` in frontmatter. Bookmarks created manually in the vault (no Karakeep record) are invisible to `--next`, so it may report "All enriched" while `--list` still shows remaining. Meanwhile, `--list` only checks for the `## Transcript` header string — it does not filter by `karakeep_id`. If you see a mismatch between the two commands, check missing karakeep_ids and custom header names (e.g., `## Raw Transcript` won't match `## Transcript`). Reconcile by either adding a Karakeep entry or tweaking the transcript header in the vault file.
- **Transcript header matching is strict** — enrichment detection checks for the literal string `## Transcript`. Variants like `## Raw Transcript`, `## Full Transcript`, or `## YouTube Transcript` are not recognized as enriched. If a vault file has a transcript under a different heading, `--list` will show it as un-enriched and `--next` may loop over it. Keep the header exactly `## Transcript`.
