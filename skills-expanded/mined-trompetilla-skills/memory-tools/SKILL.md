---
name: memory-tools
description: Agent-controlled memory plugin for OpenClaw with confidence scoring, decay, and semantic search. The agent decides WHEN to store/retrieve memories — no auto-capture noise.
homepage: https://github.com/Purple-Horizons/openclaw-memory-tools
metadata:
  openclaw:
    emoji: 🧠
    kind: plugin
    requires:
      env:
        - OPENAI_API_KEY
---

# Memory Tools

Agent-controlled persistent memory for OpenClaw.

## Why Memory-as-Tools?

Traditional memory systems auto-capture everything, flooding context with irrelevant information. Memory Tools follows the [AgeMem](https://arxiv.org/abs/2409.02634) approach: **the agent decides** when to store and retrieve memories.

## Features

- **6 Memory Tools**: `memory_store`, `memory_update`, `memory_forget`, `memory_search`, `memory_summarize`, `memory_list`
- **Confidence Scoring**: Track how certain you are (1.0 = explicit, 0.5 = inferred)
- **Importance Scoring**: Prioritize critical instructions over nice-to-know facts
- **Decay/Expiration**: Temporal memories automatically become stale
- **Semantic Search**: Vector-based similarity via LanceDB
- **Hybrid Storage**: SQLite (debuggable) + LanceDB (fast vectors)
- **Conflict Resolution**: New info auto-supersedes old (no contradictions)

## Installation

### Step 1: Install from ClawHub

```bash
clawhub install memory-tools
```

### Step 2: Build the plugin

```bash
cd skills/memory-tools
npm install
npm run build
```

### Step 3: Activate the plugin

```bash
openclaw plugins install --link .
openclaw plugins enable memory-tools
```

### Step 4: Restart the gateway

**Standard (systemd):**
```bash
openclaw gateway restart
```

**Docker (no systemd):**
```bash
# Kill existing gateway
pkill -f openclaw-gateway

# Start in background
nohup openclaw gateway --port 18789 --verbose > /tmp/openclaw-gateway.log 2>&1 &
```

### Requirements

- `OPENAI_API_KEY` environment variable (for embeddings)

## Memory Categories

| Category | Use For | Example |
|----------|---------|---------|
| fact | Static information | "User's dog is named Rex" |
| preference | Likes/dislikes | "User prefers dark mode" |
| event | Temporal things | "Dentist Tuesday 3pm" |
| relationship | People connections | "Sarah is user's wife" |
| instruction | Standing orders | "Always respond in Spanish" |
| decision | Choices made | "We decided to use PostgreSQL" |
| context | Situational info | "User is job hunting" |
| entity | Named things | "Project Apollo is their startup" |

## Tool Reference

### memory_store
```
memory_store({
  content: "User prefers bullet points",
  category: "preference",
  confidence: 0.9,
  importance: 0.7,
  tags: ["formatting", "communication"]
})
```

### memory_search
```
memory_search({
  query: "formatting preferences",
  category: "preference",
  limit: 10
})
```

### memory_update
```
memory_update({
  id: "abc123",
  content: "User now prefers numbered lists",
  confidence: 1.0
})
```

### memory_forget
```
memory_forget({
  query: "bullet points",
  reason: "User corrected preference"
})
```

### memory_summarize
```
memory_summarize({
  topic: "user's work projects",
  maxMemories: 20
})
```

### memory_list
```
memory_list({
  category: "instruction",
  sortBy: "importance",
  limit: 20
})
```

## Debugging

Inspect what your agent knows:
```bash
sqlite3 ~/.openclaw/memory/tools/memory.db "SELECT id, category, content FROM memories"
```

Export all memories:
```bash
openclaw memory-tools export > memories.json
```

## Troubleshooting

**"Database connection not open" error:**
- Hard restart the gateway: `pkill -f openclaw-gateway`
- Check permissions: `chown -R $(whoami) ~/.openclaw/memory/tools`

**Plugin not loading:**
- Verify build: `ls skills/memory-tools/dist/index.js`
- Check doctor: `openclaw doctor --non-interactive`

## License

MIT — [Purple Horizons](https://github.com/Purple-Horizons)
