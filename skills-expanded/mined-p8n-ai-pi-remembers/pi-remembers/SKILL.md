---
name: pi-remembers
description: >
  Manage persistent agent memory powered by Cloudflare AI Search.
  Use when the user asks to remember something, recall past decisions,
  check what was previously discussed, or when you need context from
  prior sessions. Also use when starting work on a familiar codebase
  to recall architecture decisions and conventions. Triggers on:
  "remember this", "do you remember", "what did we decide",
  "what was the approach", "store this preference", "forget this",
  "what do you know about this project", "list memories".
---

# Pi Remembers Skill

Pi has persistent memory powered by Cloudflare AI Search via the `@p8n.ai/pi-remembers` extension.

## Available Tools

| Tool | Purpose |
|------|---------|
| `memory_recall` | Search memories for past context — decisions, preferences, patterns |
| `memory_remember` | Store a fact, decision, or preference persistently |
| `memory_list` | List all stored memories for this project or globally |
| `memory_search` | Search indexed project files using hybrid vector+keyword search |

## Hooks (automatic behavior)

Hooks are **OFF by default**. The user can toggle them via `/memory-settings` or in config files.

| Hook | Default | What it does |
|------|---------|-------------|
| Smart Context Recall | **OFF** | Auto-recall memories before each LLM turn |
| Compaction Ingest | **OFF** | Auto-store conversations on compaction |
| Footer Status | **ON** | Show 🧠 in footer bar |

Even with hooks OFF, all tools above are always available for manual use.

## When to Use Memory

### Proactive recall — do this automatically
- **Start of a session**: recall project-specific context before diving in
- **Architecture questions**: check if a decision was already made
- **User says "remember" or "we discussed"**: recall immediately

### Proactive remember — store these automatically
- User explicitly states a preference ("I prefer X over Y")
- Important architectural or design decisions
- Coding conventions or project-specific patterns
- Configuration choices ("we're using Tailwind v4", "deploy to Cloudflare")

### Scoping
- Use `scope: "project"` for project-specific memories (default)
- Use `scope: "global"` for cross-project user preferences
- Use `scope: "both"` when recalling to get full context

## Commands

| Command | Purpose |
|---------|---------|
| `/memory-setup` | Configure Cloudflare AI Search connection |
| `/memory-settings` | Toggle hooks on/off interactively |
| `/memory-status` | Show connection status, hook states, and memory counts |
| `/memory-index` | Index project files for searchable knowledge |

## Example Workflows

### User starts a new session on a familiar project
```
1. memory_recall(query: "project architecture and tech stack", scope: "both")
2. Use recalled context to inform responses
```

### User makes a decision
```
User: "Let's use tRPC for the API layer"
1. memory_remember(content: "Project uses tRPC for the API layer", scope: "project")
2. Acknowledge the decision
```

### User asks about past context
```
User: "What auth approach did we pick?"
1. memory_recall(query: "authentication approach decision", scope: "project")
2. Present the recalled context
```
