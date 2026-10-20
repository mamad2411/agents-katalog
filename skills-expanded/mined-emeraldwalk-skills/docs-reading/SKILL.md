---
name: docs-reading
description: Parses technical documentation corpora (Markdown or Godot XML) into a local SQLite database with full-text and semantic search, then queries them via a CLI tool. Use when an agent needs to read, search, or reference documentation for a library, framework, or engine — especially large docs that would exceed context limits.
---

## Overview

docs-reading is a two-phase pipeline:

1. **Parse** — A human runs a parser script once to ingest documentation into a local SQLite database with FTS5 full-text search and optional sentence-embedding vectors. Multiple corpora and versions can coexist in a single DB.
2. **Query** — Claude calls `agent-docs-search` (a self-contained binary on `$PATH`) to search, browse, and retrieve documentation without loading the raw files into context.

## Parsing (human setup step)

### Generic Markdown

```bash
uv run scripts/parse_docs.py \
  --input /path/to/docs \
  --db ./docs.db \
  --corpus-name mylib \
  --corpus-version 1.0
```

Options: `--glob "**/*.md"` (default), `--max-tokens 512`, `--min-tokens 50`, `--no-embeddings`, `--force`

### Godot XML

```bash
uv run scripts/parse_godot.py \
  --godot-repo ./godot \
  --db ./godot.db \
  --corpus-name godot \
  --corpus-version 4.6
```

Parses the engine's native XML class reference (one chunk per method/property/signal/enum). Version is auto-detected from `version.py` if `--corpus-version` is omitted.

### Multi-corpus workflow

Multiple corpora can share one DB — just run parsers targeting the same `--db`:

```bash
uv run scripts/parse_docs.py --input ./react-docs --db ./project.db --corpus-name react --corpus-version 18
uv run scripts/parse_docs.py --input ./typescript-docs --db ./project.db --corpus-name typescript --corpus-version 5.4
```

### Embeddings (optional but recommended)

```bash
uv run scripts/add_embeddings.py --db ./docs.db
# Limit to one corpus:
uv run scripts/add_embeddings.py --db ./project.db --corpus-name react --corpus-version 18
```

The first run downloads the `all-MiniLM-L6-v2` model (~80 MB, cached locally).

## DB convention

Each skill that uses docs-reading stores its DB in its own `dbs/` directory, relative to that skill's install location:

```
$THAT_SKILL_DIR/dbs/<name>.db
```

Where `THAT_SKILL_DIR` is the directory containing the consuming skill's `SKILL.md`. Always pass `--db` explicitly — there is no auto-detection.

## Querying (agent usage)

Use `agent-docs-search` — available on `$PATH`. Output format is controlled by `--format`:

| Format | Description |
|--------|-------------|
| `json` | Compact JSON (default) |
| `json-pretty` | Indented JSON |
| `text` | Plain text — agent-friendly, no parsing needed |
| `markdown` | Structured markdown with headers |

`--db` is required. Always pass `--corpus` too (and `--version` if multiple versions exist).

For agent use, prefer `--format text` or `--format markdown` to avoid inline parsing of JSON.

```bash
# Search (hybrid FTS5 + semantic, or FTS-only if no embeddings)
agent-docs-search --db /path/to/skill/dbs/name.db --format text search "move_and_slide physics" --corpus godot --version 4.6

# Fetch a chunk by ID
agent-docs-search --db /path/to/skill/dbs/name.db --format text chunk 4821

# Heading outline for a file (browse before fetching full content)
agent-docs-search --db /path/to/skill/dbs/name.db --format text outline "CharacterBody2D.xml" --corpus godot

# List all corpora in the DB
agent-docs-search --db /path/to/skill/dbs/name.db --format text corpuses

# List all parsed files
agent-docs-search --db /path/to/skill/dbs/name.db --format text files --corpus godot

# Semantically similar chunks (requires embeddings)
agent-docs-search --db /path/to/skill/dbs/name.db --format text related 4821 --limit 5
```

## Typical agent workflow

```bash
# 1. Search — always pass --corpus (and --version if multiple versions exist)
#    Without a filter, results from different versions mix and may conflict.
agent-docs-search --db /path/to/skill/dbs/name.db search "your query" --corpus mylib --version 1.0

# 2. Browse a file's structure before loading full content
agent-docs-search --db /path/to/skill/dbs/name.db outline "path/to/file.md" --corpus mylib

# 3. Fetch a specific chunk by ID from search results
agent-docs-search --db /path/to/skill/dbs/name.db chunk 4821
```

## Dependencies

**Querying:** `agent-docs-search` is a self-contained binary on `$PATH` — no runtime dependencies.

**Parsing scripts** use `uv run` with inline dependency blocks — no install step needed. Just run with `uv run scripts/<script>.py ...` and uv handles the environment automatically.

Requires `uv` to be installed: https://docs.astral.sh/uv/getting-started/installation/

**Python version note:** `parse_docs.py` and `parse_godot.py` work on any Python version when run with `--no-embeddings` (no heavy dependencies). Generating embeddings requires a Python version supported by `torch` (a `sentence-transformers` dependency). If embedding generation fails due to a Python version incompatibility, parse with `--no-embeddings` first, then run `add_embeddings.py` in a compatible environment.
