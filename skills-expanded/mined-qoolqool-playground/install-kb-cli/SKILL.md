---
name: kb
description: Install and use the `kb` CLI to submit, pull, and manage entries in the Central Knowledge Base. For searching, use the `search-kb` skill instead.
---

# kb CLI Skill

Installs and uses the `kb` command-line tool for the Central Knowledge Base. Works standalone — no external package dependencies beyond Python 3.11+ and Python stdlib.

## Responsibility Split

| Skill | Scope | What it does |
|-------|-------|-------------|
| **`kb`** (this skill) | Central KB **write** pipeline | Install, submit, pull, drift, candidates, conflicts |
| **`search-kb`** (unified search) | **Read** from all backends | Detects available backends, searches local + Central KB, agent synthesizes narrative |

For searching, use the `search-kb` skill — it combines local vector DB + Central KB results and synthesizes them.

## When to Use This Skill

- Submitting local `knowledgebase/` YAML entries to the Central KB server
- Pulling entries from the Central KB server
- Checking for concept drift across projects
- Listing promotion candidates or resolving conflicts
- The `kb` command is not found or needs reinstalling

## Prerequisites

| Requirement | Why | Check |
|-------------|-----|-------|
| Python 3.11+ | CLI runtime | `python3 --version` |
| **Embedding source** (one of) | Generating 1024-dim vectors for submit | See Embedding Source below |
| Central KB server running | API target | `curl $CENTRAL_KB_URL/health` |

## Embedding Source

`kb submit` generates embedding vectors client-side before sending entries to the server. Sources are tried in priority order:

| Priority | Source | Speed | How |
|-----------|--------|-------|-----|
| 1 | **embed-server HTTP sidecar** | ~100ms | `host.containers.internal:9001`, auto-detected |
| 2 | **Ollama** (fallback) | ~330ms | `localhost:11434/api/embeddings`, model `bge-large:latest` |

No local embedding model download required if the embed-server sidecar is reachable. On a fresh clone (no model pulled), `kb submit` auto-detects the sidecar and uses it.

## Installation Procedure

1. Run the install script:
   ```bash
   bash ~/.pi/agent/skills/kb/install-kb-cli.sh
   ```
   Or from the project repo:
   ```bash
   bash tooling/skills/install-kb-cli/install-kb-cli.sh
   ```

2. The script tries two strategies in order:
   - **Official CLI**: If `tooling-central` package exists → `pip install -e` (full kb CLI)
   - **Standalone wrapper**: If not → copies `kb-cli.py` to `~/.local/bin/kb` (zero deps, talks HTTP directly)

3. The script automatically:
   - Adds `~/.local/bin` to PATH (persists to `~/.bashrc`)
   - Auto-detects the Central KB server URL (tries `host.containers.internal`, `host.docker.internal`, then default gateway)
   - Auto-detects embed-server HTTP sidecar or pulls Ollama embedding model if needed
   - Verifies the Central KB server is reachable

4. Set environment variables (server URL is auto-detected, only project name must be set):
   ```bash
   export CENTRAL_KB_PROJECT=playground
   # CENTRAL_KB_URL is auto-detected via host.containers.internal
   # Override manually if needed:
   # export CENTRAL_KB_URL=http://192.168.100.183:9000
   ```

5. Verify end-to-end:
   ```bash
   kb health
   ```

## Commands

### Write Pipeline (this skill)

```bash
kb submit --project my-project                    # Push local KB entries
kb pull --project my-project                     # Pull entries from server
kb drift --project my-project                    # Check for concept drift
kb lint --project my-project                     # Run memory lint (rule-based)
kb lint --project my-project --llm               # Full lint with contradiction detection
kb lint --project my-project --stale-days 30     # Custom staleness threshold
kb candidates                                    # List promotion candidates
kb conflicts                                     # List conflicts
kb conflicts 1 --resolve "accept proposed"     # Resolve a conflict
```

### Read Pipeline → use `search-kb` skill

```bash
# These commands work, but the search-kb skill gives a unified search
# across both local and Central KB backends:
kb search "query" --scope my-project              # Semantic + full-text search
kb explain "topic" --scope my-project            # Structured view of how entries relate
kb explain "topic" --scope my-project --llm       # Standalone: local Ollama synthesizes narrative
```

**In an agent session**, use the `search-kb` skill instead of calling `kb search`/`kb explain` directly — it searches all available backends and the agent synthesizes a narrative.

### `kb explain` — Two Modes

**In an agent session (preferred):** `kb explain "topic" --scope proj` returns structured results.
The agent itself synthesizes the narrative — no local LLM needed, and the agent model
(cloud-hosted) is far more capable than any local Ollama model.

**Standalone CLI:** `kb explain "topic" --scope proj --llm` calls a local Ollama chat
model to produce a narrative. Auto-detects available models (qwen2.5:0.5b → gemma3:4b …).
Use `--model` or `KB_LLM_MODEL` to override. Quality is limited by local model size.

## Environment Variables

| Variable | Default | Purpose |
|----------|---------|---------|
| `CENTRAL_KB_URL` | Auto-detected (host.containers.internal:9000) | Server URL |
| `CENTRAL_KB_PROJECT` | (none) | Default project name |
| `KB_EMBED_MODEL` | `bge-large:latest` | Ollama embedding model (1024-dim) |
| `KB_LLM_MODEL` | auto-detected | Ollama chat model for `kb explain --llm` (auto-detects qwen2.5:0.5b, gemma3:4b, etc.) |

## How Submission Works

When you run `kb submit`:

1. Reads all `.yaml`/`.yml` files from `knowledgebase/{decisions,patterns,sessions}/`
2. Generates a 1024-dim embedding vector for each entry (title + first 512 chars)
   - Tries embed-server HTTP sidecar first (~100ms)
   - Falls back to Ollama `bge-large:latest` (~330ms)
   - If neither available, exits with clear error message
3. Submits entries in batches of 5 to the server `/submit` endpoint
4. Reports accepted/duplicate/conflicted/error status for each entry

**Critical**: The server requires `vector` field on every submission. Entries without vectors are silently rejected with `status: "error"`. Never mix embedding dimensions in the same server DB — this corrupts the index and causes 500 errors on all subsequent submissions.

## `kb lint` — Self-healing memory scan

Two-phase diagnostic that checks knowledgebase health:

**Phase 1 (rule-based, no LLM):** Always runs. Detects:
- Orphan references — entries pointing to non-existent superseded parents
- Broken chains — entries claiming to be superseded by missing entries
- Stale entries — no access in N days (default: 90), candidates for forget sweep
- Mixed vector dimensions — entries with embedding dims that don't match the expected 1024

**Phase 2 (LLM-driven, opt-in with `--llm`):** Requires Ollama running locally.
- Contradiction detection — finds semantically similar entry pairs (cosine ≥ 0.75)
  and asks the LLM if they make opposing claims

```bash
kb lint --project my-project                    # Rule-based only
kb lint --project my-project --llm              # Full lint with contradiction detection
kb lint --project my-project --stale-days 30    # Custom staleness threshold
```

## Pitfalls

| Problem | Fix |
|---------|-----|
| Submit returns all `error` statuses | Server requires `vector` field — use this CLI (auto-embeds), don't POST manually without vectors |
| Mixed vector dimensions (768 vs 1024) | **Never mix models**. Default is `bge-large` (1024-dim). Using `nomic-embed-text` (768-dim) against a DB that has 1024-dim entries corrupts the index |
| Ollama embedding times out | Restart: `pkill ollama; ollama serve`. First request loads model into memory (cold start ~30s) |
| No embedding source available | `kb submit` needs embeddings. Start embed-server sidecar OR run: `ollama pull bge-large:latest`. `kb search`/`kb explain` still work (server generates query vectors) |
| `kb` not found | `export PATH="$HOME/.local/bin:$PATH"` or rerun install script |
| Server 500 on submit | Two known causes: (1) vector dimension mismatch in DB, (2) simhash OverflowError — CLI pre-computes signed simhash to prevent this |
| `pip install` fails with PEP 668 | Install script uses `--break-system-packages`. Or use a venv |
| Central KB server not reachable | Auto-detection will find it. If not, set `CENTRAL_KB_URL` manually |

## Files

| File | Purpose |
|------|---------|
| `SKILL.md` | This skill definition |
| `install-kb-cli.sh` | Installation script (tries official CLI, falls back to standalone) |
| `kb-cli.py` | Standalone `kb` CLI — pure Python, no external package deps, auto-embeds via embed-server or Ollama |

## Verification Checklist

After installation, verify each step:

```bash
# 1. CLI is on PATH
command -v kb   # → /home/tool/.local/bin/kb

# 2. Server is reachable (URL auto-detected)
kb health       # → Central KB server: ok v0.1.0

# 3. Submit works (auto-detects embed-server HTTP or Ollama)
kb submit --project playground

# 4. Search works (uses server-side embeddings, no local model needed)
kb search "docker" --scope playground
```