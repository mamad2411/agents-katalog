# SurrealDB Knowledge Graph Memory

A knowledge graph memory system using SurrealDB with vectorized semantic search, confidence scoring, graph-aware fact relationships, MCP tools, and LLM-powered knowledge extraction.

## Description

Use this skill for:
- Storing and retrieving knowledge as interconnected facts
- Semantic memory search with confidence-weighted results  
- Managing fact relationships (supports, contradicts, updates)
- LLM-powered knowledge extraction from memory files
- AI-driven relationship discovery between facts
- Memory maintenance: decay, pruning, consolidation

**Triggers:** "remember this", "store fact", "what do you know about", "memory search", "memory maintenance", "prune memory", "knowledge graph", "find relations"

## ⚠️ Security & Installation Notes

This skill performs system-level operations. Review before installing:

| Behavior | Location | Description |
|----------|----------|-------------|
| **Network installer** | `install.sh`, `memory.ts` | Runs `curl https://install.surrealdb.com \| sh` |
| **Source patching** | `integrate-clawdbot.sh` | Uses `sed -i` to patch Clawdbot source files |
| **Service management** | `memory.ts` | Can start SurrealDB server, run schema imports |
| **Python packages** | `install.sh`, `memory.ts` | Installs surrealdb, openai, pyyaml via pip |
| **File access** | `extract-knowledge.py` | Reads `MEMORY.md` and `memory/*.md` for extraction |

**Default credentials:** Examples use `root/root` — change for production and bind to localhost only.

**API key:** `OPENAI_API_KEY` is required for embeddings (text-embedding-3-small) and LLM extraction (GPT-4o-mini). Use a scoped key.

**Safe install path:**
1. Install SurrealDB manually from [surrealdb.com/install](https://surrealdb.com/install)
2. Use a Python venv: `python3 -m venv .venv && source .venv/bin/activate`
3. Review and run `pip install -r scripts/requirements.txt`
4. Set `OPENAI_API_KEY` with minimal permissions
5. Skip `integrate-clawdbot.sh` or review the diffs it will apply

## Features

### MCP Tools
The skill provides an MCP server with 4 tools for knowledge graph operations:

| Tool | Description |
|------|-------------|
| `knowledge_search` | Semantic search for facts by query |
| `knowledge_recall` | Recall a fact with full context (relations, entities) |
| `knowledge_store` | Store a new fact with confidence and tags |
| `knowledge_stats` | Get knowledge graph statistics |

### Knowledge Extraction
- Extracts structured facts from MEMORY.md and memory/*.md files
- Uses LLM (GPT-4o-mini) to identify entities and relationships
- Tracks file changes for incremental extraction
- Supports full re-extraction when needed

### Confidence Scoring
Each fact has an **effective confidence** calculated from:
- Base confidence (0.0–1.0)
- **+ Inherited boost**: from high-confidence supporting facts
- **+ Entity boost**: from well-established entities mentioned
- **- Contradiction drain**: from high-confidence contradicting facts
- **- Time decay**: 5% per month of staleness

### Relationship Discovery
- AI finds semantic connections between isolated facts
- Creates `supports`, `contradicts`, `updates`, `elaborates` edges
- Can run manually or via daily cron job

## Prerequisites

1. **SurrealDB** installed and running:
   ```bash
   # Option A: Use the installer (runs curl | sh - review first!)
   ./scripts/install.sh
   
   # Option B: Manual install (recommended)
   # See https://surrealdb.com/install
   
   # Start server (change credentials in production!)
   surreal start --bind 127.0.0.1:8000 --user root --pass root file:~/.clawdbot/memory/knowledge.db
   ```

2. **Python dependencies** (use the skill's venv):
   ```bash
   cd /path/to/surrealdb-memory
   python3 -m venv .venv
   source .venv/bin/activate
   pip install -r scripts/requirements.txt
   ```

3. **OpenAI API key** (**required**) for embeddings and extraction:
   ```bash
   # Used for: text-embedding-3-small (embeddings), GPT-4o-mini (extraction)
   # Recommendation: Use a scoped key with minimal permissions
   export OPENAI_API_KEY="sk-..."
   ```

## Quick Start

```bash
# Initialize the database schema
./scripts/init-db.sh

# Run initial knowledge extraction
source .venv/bin/activate
python3 scripts/extract-knowledge.py extract --full

# Check status
python3 scripts/extract-knowledge.py status
```

## MCP Server Usage

### Via mcporter (recommended)
```bash
# Stats
mcporter call surrealdb-memory.knowledge_stats

# Search for facts
mcporter call surrealdb-memory.knowledge_search query="topic" limit:10

# Recall a fact with context
mcporter call surrealdb-memory.knowledge_recall query="topic"
mcporter call surrealdb-memory.knowledge_recall fact_id="fact:abc123"

# Store a new fact
mcporter call surrealdb-memory.knowledge_store content="New fact" confidence:0.9
```

### MCP Server Config
Add to your MCP client config:
```json
{
  "surrealdb-memory": {
    "command": "python3",
    "args": ["scripts/mcp-server.py"],
    "cwd": "/path/to/surrealdb-memory"
  }
}
```

## CLI Commands

### knowledge-tool.py (simple CLI)

```bash
# Search for facts
python3 scripts/knowledge-tool.py search "query" --limit 10

# Recall a fact
python3 scripts/knowledge-tool.py recall "query"
python3 scripts/knowledge-tool.py recall "fact:abc123"

# Store a fact
python3 scripts/knowledge-tool.py store "Fact content" --confidence 0.9

# Get stats
python3 scripts/knowledge-tool.py stats
```

### extract-knowledge.py

| Command | Description |
|---------|-------------|
| `extract` | Extract from changed files only |
| `extract --full` | Full extraction (all files) |
| `status` | Show extraction status and stats |
| `reconcile` | Deep reconciliation (prune, decay, clean orphans) |
| `discover-relations` | AI finds relationships between facts |
| `dedupe` | Find and remove duplicate facts |
| `rebuild-links` | Rebuild entity links for existing facts |
| `check` | Check if extraction needed (for heartbeat) |

### memory-cli.py

| Command | Description |
|---------|-------------|
| `store <content>` | Store a new fact with optional `--source`, `--confidence`, `--tags` |
| `search <query>` | Semantic search, returns facts weighted by similarity × confidence |
| `get <fact_id>` | Get a fact with full context (related facts, entities) |
| `relate <fact1> <rel> <fact2>` | Create relationship: `supports`, `contradicts`, `updates`, `elaborates` |
| `decay` | Apply time decay to stale facts |
| `prune` | Remove low-confidence stale facts |
| `consolidate` | Merge near-duplicate facts |
| `maintain` | Run full maintenance cycle (decay + prune + consolidate) |
| `stats` | Show database statistics |

## Gateway Integration

This skill includes gateway handlers for the Clawdbot control UI:

| Method | Description |
|--------|-------------|
| `memory.health` | Check SurrealDB status, schema, dependencies |
| `memory.stats` | Get fact/entity/relationship counts |
| `memory.repair` | Auto-repair: install binary, start server, init schema |
| `memory.runExtraction` | Run extraction, reconciliation, or relation discovery |
| `memory.extractionProgress` | Poll extraction progress |
| `memory.activity` | Get recent activity (queries, extractions) |
| `memory.maintenance` | Run decay/prune operations |

### Installing Gateway Integration

Copy the gateway handler to Clawdbot source:
```bash
cp clawdbot-integration/gateway/memory.ts /path/to/clawdbot/src/gateway/server-methods/

# Add to server-methods.ts:
import { memoryHandlers } from "./server-methods/memory.js";
// Add ...memoryHandlers to coreGatewayHandlers

# Rebuild Clawdbot
cd /path/to/clawdbot && npm run build
```

## Configuration

Create `~/.clawdbot/surrealdb-memory.yaml`:

```yaml
connection: "http://localhost:8000"
namespace: clawdbot
database: memory
user: root
password: root

embedding:
  provider: openai
  model: text-embedding-3-small
  dimensions: 1536

confidence:
  decay_rate: 0.05  # per month
  support_threshold: 0.7
  contradict_drain: 0.20

maintenance:
  prune_after_days: 30
  min_confidence: 0.2
```

## Files

```
surrealdb-memory/
├── SKILL.md                 # This file
├── scripts/
│   ├── mcp-server.py        # MCP server with 4 tools
│   ├── knowledge-tool.py    # Simple CLI wrapper
│   ├── extract-knowledge.py # LLM extraction from memory files
│   ├── memory-cli.py        # Full CLI for CRUD operations
│   ├── knowledge-tools.py   # Higher-level extraction tools
│   ├── schema.sql         # Database schema with graph functions
│   ├── init-db.sh           # Initialize database with schema
│   ├── install.sh           # Install SurrealDB binary
│   ├── migrate-sqlite.py    # Import from existing SQLite memory
│   ├── web-ui.py            # Optional web interface
│   └── requirements.txt     # Python dependencies
├── clawdbot-integration/
│   └── gateway/
│       └── memory.ts        # Gateway RPC handlers
└── references/
    ├── surql-examples.md    # SurrealQL query patterns
    └── conflict-patterns.md # Contradiction detection rules
```

## Maintenance Schedule

Add to `HEARTBEAT.md` or create a cron job:
```markdown
## Memory Maintenance (weekly)
- Run `surrealdb-memory` knowledge extraction check
- Run reconciliation if facts are stale
```

Or use the Control UI's "Daily auto-discovery" checkbox to enable automatic relation discovery.

## Troubleshooting

**"Connection refused"** — Start SurrealDB:
```bash
surreal start --user root --pass root file:~/.clawdbot/memory/knowledge.db
```

**"surrealdb package not installed"** — Install Python deps:
```bash
source .venv/bin/activate
pip install -r scripts/requirements.txt
```

**"OPENAI_API_KEY not set"** — Export the key:
```bash
export OPENAI_API_KEY="sk-..."
```

**Slow searches** — Ensure vector index exists (check schema.sql was applied)

**Control UI shows "Starting..." stuck** — Hard refresh browser (Ctrl+Shift+R)

## Version History

- **v1.2.0** (2026-02-09): Added MCP server with 4 tools, fixed query bugs
- **v1.1.0** (2026-02-09): Added gateway integration, relation discovery, control UI support
- **v1.0.0** (2026-01-31): Initial release with extraction and CLI
