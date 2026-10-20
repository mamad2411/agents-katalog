# Persistent Memory Skill

**Description:** Three-layer persistent memory system (Markdown + ChromaDB vectors + NetworkX knowledge graph) for long-term agent recall across sessions.

## When to Use This Skill

Activate when the agent needs to:
- Remember decisions, facts, context, or institutional knowledge between sessions
- Search across past conversations and memories
- Prevent directive ignorance by ensuring workspace rules are indexed
- Maintain continuity across sessions

## Architecture

| Layer | Technology | Purpose |
|-------|-----------|---------|
| L1: Markdown | MEMORY.md + memory/*.md + reference/ | Human-readable curated knowledge |
| L2: Vector | ChromaDB + all-MiniLM-L6-v2 | Semantic search across all memories |
| L3: Graph | NetworkX | Relationship traversal between concepts |

## Setup Instructions

### First Time Setup

```bash
# Step 1: Create the 3-layer memory system
bash ~/.openclaw/workspace/skills/persistent-memory/scripts/setup.sh

# Step 2: Configure OpenClaw integration (CRITICAL)
python ~/.openclaw/workspace/skills/persistent-memory/scripts/configure_openclaw.py
```

### Daily Usage

**Write Memories:**
- MEMORY.md — Curated long-term knowledge
- memory/YYYY-MM-DD.md — Daily logs
- reference/*.md — Institutional facts

**Index After Editing:**
```bash
~/.openclaw/workspace/vector_memory/venv/bin/python ~/.openclaw/workspace/vector_memory/indexer.py
```

**Search Memories:**
```bash
~/.openclaw/workspace/vector_memory/venv/bin/python ~/.openclaw/workspace/vector_memory/search.py "your query"
```

**Check Sync Status:**
```bash
~/.openclaw/workspace/vector_memory/venv/bin/python ~/.openclaw/workspace/vector_memory/auto_retrieve.py --status
```

## Agent Behavior Rules

### Pre-Response (Mandatory)
Before answering questions about prior work, decisions, dates, people, or preferences:
1. Use OpenClaw's `memory_search` tool first
2. If results insufficient, run vector search
3. Never say "I don't remember" without checking

### Pre-Action (Mandatory)
Before using external identifiers (URLs, emails, repo names):
1. Query reference/ files for exact value
2. If not found, query vector memory
3. If still not found, ask the user
4. **Never fabricate identifiers**

### Post-Edit (Mandatory)
After editing MEMORY.md, memory/*.md, or reference/*.md:
```bash
~/.openclaw/workspace/vector_memory/venv/bin/python ~/.openclaw/workspace/vector_memory/indexer.py
```

## Reference Directory (Optional)

Create `reference/` for institutional knowledge:
- people.md — Contacts, roles, communication details
- repos.md — GitHub repositories, URLs, status
- infrastructure.md — Hosts, IPs, ports, services
- business.md — Company info, strategies, rules
- properties.md — Domain-specific entities

## Troubleshooting

- **"No module named chromadb"** — Run setup.sh again
- **OUT_OF_SYNC status** — Run the indexer
- **Empty search results** — Check MEMORY.md content
- **Agent ignoring directives** — Run configure_openclaw.py
