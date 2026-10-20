---
name: godot-docs
description: Look up Godot 4.x API documentation — classes, methods, properties, signals, enums. Use when implementing any Godot feature, when you need to know how a Godot class works, or before writing any Godot code.
---

Search Godot 4.x class reference docs via `agent-docs-search`. The DB lives in this skill's `dbs/` directory. Always pass `--corpus godot`.

## Typical workflow

```bash
# 1. Search first — usually sufficient. Results include chunk IDs and source files.
agent-docs-search --db <this-skill-dir>/dbs/godot.db search "CharacterBody3D move_and_slide" --corpus godot

# 2. Fetch a specific chunk if you need full content
agent-docs-search --db <this-skill-dir>/dbs/godot.db chunk 1234

# 3. When exploring a whole class — get the outline first, then fetch specific chunks
agent-docs-search --db <this-skill-dir>/dbs/godot.db outline "doc/classes/CharacterBody3D.xml" --corpus godot
agent-docs-search --db <this-skill-dir>/dbs/godot.db chunk 1234

# 4. Find semantically similar chunks (requires embeddings)
agent-docs-search --db <this-skill-dir>/dbs/godot.db related 1234
```

## Setup (one-time human step)

Clone the Godot repo and parse the docs:

```bash
cd <docs-reading-skill-dir>

uv run scripts/parse_godot.py \
  --godot-repo /path/to/godot \
  --db <this-skill-dir>/dbs/godot.db \
  --corpus-name godot \
  --corpus-version 4.6
```

No further configuration needed — no MCP server, no settings changes.
