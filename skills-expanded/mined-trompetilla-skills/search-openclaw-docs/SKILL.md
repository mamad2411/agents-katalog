---
name: search-openclaw-docs
description: OpenClaw agent skill for semantic search across OpenClaw documentation. Use when users ask about OpenClaw setup, configuration, troubleshooting, or features. Returns relevant file paths to read.
metadata:
  openclaw:
    emoji: "📚"
    homepage: https://github.com/karmanverma/search-openclaw-docs
    requires:
      bins: ["node"]
    install:
      - id: "deps"
        kind: "npm"
        package: "better-sqlite3"
        label: "Install better-sqlite3 (SQLite bindings)"
    postInstall: "node scripts/docs-index.js rebuild"
---

# OpenClaw Documentation Search

Fast file-centric search for OpenClaw docs using FTS5 keyword matching.

**Fully offline** - no network calls, no external dependencies.

## Quick Start

```bash
# Search
node ~/.openclaw/skills/search-openclaw-docs/scripts/docs-search.js "discord requireMention"

# Check index health
node ~/.openclaw/skills/search-openclaw-docs/scripts/docs-status.js

# Rebuild (after OpenClaw update)
node ~/.openclaw/skills/search-openclaw-docs/scripts/docs-index.js rebuild
```

## When to Use

| User asks... | Action |
|--------------|--------|
| "How do I configure X?" | Search → read file → answer |
| "Why isn't X working?" | Search → read file → diagnose |
| "What does Y do?" | Search → read file → explain |

**Don't use for**: Personal memories, preferences → use `memory_search` instead.

## Usage Examples

```bash
# Config question
node scripts/docs-search.js "discord requireMention"

# Troubleshooting  
node scripts/docs-search.js "webhook not working"

# More results
node scripts/docs-search.js "providers" --top=5

# JSON output
node scripts/docs-search.js "heartbeat" --json
```

## Output Format

```
🔍 Query: discord only respond when mentioned

🎯 Best match:
   channels/discord.md
   "Discord (Bot API)"
   Keywords: discord, requiremention
   Score: 0.70

📄 Also relevant:
   concepts/groups.md (0.66)

💡 Read with:
   cat /usr/lib/node_modules/openclaw/docs/channels/discord.md
```

## How It Works

- FTS5 keyword matching on titles, headers, config keys
- Handles camelCase terms like `requireMention`
- Porter stemming for flexible matching
- No network calls - fully offline

## Index Location

- **Index**: `~/.openclaw/docs-index/openclaw-docs.sqlite`
- **Docs**: `/usr/lib/node_modules/openclaw/docs/`

Index is built locally from your OpenClaw version.

## Troubleshooting

### No results / wrong results

```bash
# 1. Check index exists
node scripts/docs-status.js

# 2. Rebuild if stale
node scripts/docs-index.js rebuild

# 3. Try exact config terms (camelCase matters)
node scripts/docs-search.js "requireMention"

# 4. Try broader terms
node scripts/docs-search.js "discord"
```

## Integration

```javascript
const { search } = require('./lib/search');
const INDEX = process.env.HOME + '/.openclaw/docs-index/openclaw-docs.sqlite';

const results = await search(INDEX, "discord webhook");
// results[0].path → full path to read
```
