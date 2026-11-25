---
name: braincell-sync
description: |
  Incrementally refresh the CURRENT Project's BrainCell memory: re-embed only
  content-changed notes and pick up new Claude/Codex transcripts with the local
  qwen3-embedding:4b embedder (mtime→SHA + cluster skip, so unchanged content is
  not re-embedded). Assumes /braincell-init already ran (BrainCell connected for
  this Project). Use when: "braincell-sync", "sync braincell", "refresh braincell
  memory", "update BrainCell for this project".
allowed-tools:
  - Bash
  - Read
  - Glob
  - Grep
---

# /braincell-sync — incrementally refresh BrainCell memory for this Project

Keeps this Project's BrainCell memory current after more work. Unlike `/braincell-init`,
this does not reconnect BrainCell and does not rebuild from scratch — it processes only
what changed.

**Engine:** braincell-mcp, **Project-scoped** — syncs memory for the current working
directory (`$PWD`), the same Project memory the MCP serves. **Embedder:** the local
Ollama `qwen3-embedding:4b` (1024-d) default; the sync must use the SAME embedder Project memory was
built with (fingerprint-gated) or it fails loud rather than corrupting the vector space.

## Steps

Resolve the CLI once — it ships with the `braincell-mcp` package as a console script:
```bash
BC="$(command -v braincell || true)"
[ -n "$BC" ] || { echo "ERROR: braincell CLI not found on PATH. Activate the environment where braincell-mcp is installed, then re-run."; exit 1; }
```

1. **Pre-flight.** Confirm this Project already has BrainCell memory and a
   client connection; if not, this is the wrong skill → run `/braincell-init`. Confirm the
   local embedder is ready:
   ```bash
   ollama list 2>/dev/null | grep -q 'qwen3-embedding:4b' || { echo "ERROR: qwen3-embedding:4b not pulled. Run: ollama pull qwen3-embedding:4b"; exit 1; }
   ```

2. **Incremental sync — targets `$PWD` (the served Project memory):**
   ```bash
   "$BC" sync .
   ```
   Re-embeds only content-changed notes and reads new transcript pages for this Project;
   unchanged content is skipped (mtime→SHA / cluster gate). Writes only to the XDG
   store. Cheap on repeat runs.

3. **Verdict.** Report what changed (notes re-embedded / new transcript pages / skipped
   counts from the sync output). No restart needed — the connected MCP serves
   the updated store on its next query.

## Guardrails
- **Same embedder as the build — one embedder per Project memory store.** braincell's store is
  fingerprint-gated (`ollama:qwen3-embedding:4b:1024` by default); syncing with a different
  model/dim fails the dimension guard rather than silently corrupting search. If you
  deliberately changed the embedder, use `braincell build --reembed` (a full rebuild),
  not sync.
- **Project-scoped: syncs `$PWD`**, the memory the MCP serves for this Project. Do not
  target another directory.
- **Read-only over the Project tree** (writes only to BrainCell's data store).
- If this Project has no BrainCell memory yet, `sync` has nothing to refresh → run
  `/braincell-init` first; do not mint identity here.
- Don't run concurrently with an active build on the same project (single-writer
  SQLite). A read-only MCP server querying Project memory is fine — WAL allows concurrent
  readers.
