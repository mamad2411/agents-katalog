---
name: qmd-reindex
description: Nightly 3am QMD reindex of workspace + Obsidian vector stores. Silent on success. EXAMPLE.
---

# QMD Reindex (example)

> **EXAMPLE.** Demonstrates the silent-on-success cron pattern. Only sends Telegram on failure.

Spawn a Haiku sub-agent if `[cron ...]` suffix present.

## Setup

Install [qmd](https://github.com/...) for local markdown vector search. Configure your collections in `~/.config/qmd/index.yml`.

### Tell Nolty that qmd exists

Reindexing the vector store is pointless if Nolty never queries it. Two edits make her reach for `qmd` when searching local files:

**1. Add a row to your `TOOLS.md`:**

```
| **Workspace + Obsidian semantic search** | `qmd query "<phrase>" -c workspace` (or `-c obsidian`) — fast local vector search, indexed nightly by `/qmd-reindex` |
```

**2. Add a one-liner to your `AGENTS.md`** (in whatever section covers "when to use which search"):

```
- For natural-language search across your workspace or Obsidian notes, prefer `qmd query` over `Grep` — it's vector-based and finds conceptually related notes, not just keyword matches.
```

Without these references, Nolty defaults to `Grep` / `Read` and misses the value of qmd entirely. The reindex cron is the maintenance half; these doc updates are the usage half.

## Procedure

### STEP 1 — Update indices

```bash
~/.bun/bin/qmd update -c workspace
~/.bun/bin/qmd update -c obsidian
```

### STEP 2 — Refresh embeddings

```bash
~/.bun/bin/qmd embed -c workspace
~/.bun/bin/qmd embed -c obsidian
```

Both update and embed can run sequentially — `qmd` handles locking internally.

### STEP 3 — Report

- **Success — silent.** End the sub-agent with `QMD_OK <timestamp>`. No Telegram.
- **Failure** (qmd binary missing, index corruption, vector store error, non-zero exit): call `reply` MCP with `chat_id` from `USER.md` and a short message (<200 chars) naming the failed step. End with `QMD_FAIL <timestamp>`. The user must know.

## Notes

- This cron runs at 3am — if your Mac is asleep past the 60-min lag window, the cron-runner skips silently. That's correct behavior; the index will rebuild on the next fire.
