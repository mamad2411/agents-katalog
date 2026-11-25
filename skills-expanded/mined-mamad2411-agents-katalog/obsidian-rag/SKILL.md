---
name: "obsidian-rag"
description: "Expert skill for managing Obsidian vaults, indexing notes for RAG, and performing semantic searches. Provides tools for reading, writing, and searching notes with automated vector indexing."
---

# obsidian-rag — Obsidian Vault Management & RAG Skill

**Category:** knowledge-management / note-taking / semantic-search
**Language:** Python 3.9–3.12
**Runtime:** uv (dependencies locked via `pyproject.toml`)
**License:** MIT

**Acknowledgment:** This project is inspired by [gemini-obsidian](https://github.com/thoreinstein/gemini-obsidian).

## What It Does

Provides 16 tools for Obsidian vault management (read, write, search, link analysis, frontmatter) plus a full RAG pipeline (LanceDB + FastEmbed embeddings) for semantic search over your notes.

## Setup

When using this skill for the first time, ensure `uv` is installed. Run from the skill directory:

```bash
cd skills/obsidian-rag
uv sync        # installs all dependencies into .venv/
```

On first run, uv will download and cache all packages. Subsequent calls are instant.

## Tools

### Vault Navigation & Read

| Tool | Description |
|------|-------------|
| `list_notes` | List markdown files in vault (optional subfolder filter) |
| `read_note` | Read full content of a note |
| `search_notes` | Full-text search across all notes (filename + content) |

### Note Writing

| Tool | Description |
|------|-------------|
| `create_note` | Create a new note with content |
| `append_note` | Append text to end of existing note |
| `get_daily_note` | Get or auto-create today's daily note |
| `append_daily_log` | Append timestamped entry under a heading in daily note |
| `move_note` | Move or rename a note |

### Wikilink Analysis

| Tool | Description |
|------|-------------|
| `get_backlinks` | Find all notes linking to a target note |
| `get_links` | Extract all outgoing wikilinks from a note |
| `get_broken_links` | Find wikilinks pointing to non-existent notes |

### Content Editing

| Tool | Description |
|------|-------------|
| `update_frontmatter` | Update YAML frontmatter (single key or batch JSON) |
| `replace_section` | Replace body under a heading (preserves heading line) |
| `replace_in_note` | Replace first occurrence of text in a note |

### RAG (Semantic Search)

| Tool | Description |
|------|-------------|
| `rag_index` | Index vault for semantic search (incremental by default) |
| `rag_query` | Semantic search on indexed vault |

## Usage

```bash
# Via uv directly (from skill directory)
cd skills/obsidian-rag
uv run python -m obsidian_rag list_notes
uv run python -m obsidian_rag get_backlinks "Project Alpha"
uv run python -m obsidian_rag append_daily_log "Work Log" "Finished the API integration"

# Reindex vault (using reindex script)
python skills/obsidian-rag/scripts/reindex.py /path/to/vault
```

## Technical Details

### RAG Pipeline
- **Embedding model:** `BAAI/bge-small-zh-v1.5` (512-dim, FastEmbed)
- **Vector store:** LanceDB (local, zero-config)
- **Chinese chunking:** Splits on `。！？；：.!?:;,`, merges up to target size

### Defaults
- Chunk size: 40–1800 chars, target 700 chars
- Embed batch size: 8 (memory-efficient)
- Incremental indexing via MD5 file hashes

### Config Files & Storage
Paths are OS-dependent (managed via `platformdirs`):
- **macOS:** `~/Library/Application Support/obsidian-rag/`
- **Linux:** `~/.config/obsidian-rag/` (config) and `~/.local/share/obsidian-rag/` (data)
- **Windows:** `%LOCALAPPDATA%\openclaw\obsidian-rag\`

Stored files include:
- `config.json` — Vault path configuration.
- `lancedb/` — Vector database directory.
- `file_hashes.json` — Incremental index hashes.

## Requirements (locked versions)

```
fastembed==0.7.4
lancedb==0.25.3
onnxruntime==1.19.2
python-frontmatter>=1.1.0
click>=8.1.7
platformdirs>=2.5.0
```

## Environment Variables

| Variable | Description |
|----------|-------------|
| `OBSIDIAN_VAULT_PATH` | Default vault path (overridden by `--vault-path`) |

## OpenClaw / AI Agent Integration

Each tool maps to a CLI subcommand. The agent invokes:

```bash
cd skills/obsidian-rag && uv run python -m obsidian_rag <tool> [options]
```
