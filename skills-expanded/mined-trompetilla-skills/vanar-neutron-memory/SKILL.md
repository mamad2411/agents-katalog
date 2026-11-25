---
name: vanar-neutron-memory
description: Store and retrieve agent memory using Vanar Neutron API. Use for saving information with semantic search, and persisting agent context between sessions.
user-invocable: true
metadata: {"openclaw": {"emoji": "🧠", "requires": {"env": ["NEUTRON_API_KEY", "NEUTRON_AGENT_ID"]}, "primaryEnv": "NEUTRON_API_KEY"}}
---

# Vanar Neutron Memory

Persistent memory storage with semantic search for AI agents. Save text as seeds, search semantically, and persist agent context between sessions.

## Features

- **Auto-Recall**: Automatically queries relevant memories before each AI turn and injects as context
- **Auto-Capture**: Automatically saves conversations after each AI turn
- **Semantic Search**: Find memories by meaning using Jina Embeddings v4 (1024 dimensions)
- **Memory Types**: Episodic, semantic, procedural, and working memory
- **Blockchain Attestation**: Tamper-evident memory storage with transaction hashes

## Prerequisites

Get your API keys at: **https://openclaw.vanarchain.com/**

API credentials via environment variables:
```bash
export NEUTRON_API_KEY=your_key
export NEUTRON_AGENT_ID=your_agent_id
export YOUR_AGENT_IDENTIFIER=your_agent_name_or_id  # agent_id name or defaults to 1
```

Or stored in `~/.config/neutron/credentials.json`:
```json
{
  "api_key": "your_key_here",
  "agent_id": "your_agent_id_here",
  "your_agent_identifier": "your_agent_name_or_id"
}
```

## Testing

Verify your setup:
```bash
./scripts/neutron-memory.sh test  # Test API connection
```

## Hooks (Auto-Capture & Auto-Recall)

The skill includes OpenClaw hooks for automatic memory management:

- `hooks/pre-tool-use.sh` - **Auto-Recall**: Queries memories before AI turn, injects relevant context
- `hooks/post-tool-use.sh` - **Auto-Capture**: Saves conversation after AI turn

### Configuration

Both features are **enabled by default**. To disable:

```bash
export VANAR_AUTO_RECALL=false   # Disable auto-recall
export VANAR_AUTO_CAPTURE=false  # Disable auto-capture
```

Or add to your credentials file:
```json
{
  "api_key": "your_key_here",
  "agent_id": "your_agent_id_here",
  "your_agent_identifier": "your_agent_name_or_id",
  "auto_recall": true,
  "auto_capture": true
}
```

## Scripts

Use the provided bash script in the `scripts/` directory:
- `neutron-memory.sh` - Main CLI tool

## Common Operations

### Save Text as a Seed
```bash
./scripts/neutron-memory.sh save "Content to remember" "Title of this memory"
```

### Semantic Search
```bash
./scripts/neutron-memory.sh search "what do I know about blockchain" 10 0.5
```

### Create Agent Context
```bash
./scripts/neutron-memory.sh context-create "my-agent" "episodic" '{"key":"value"}'
```

### List Agent Contexts
```bash
./scripts/neutron-memory.sh context-list "my-agent"
```

### Get Specific Context
```bash
./scripts/neutron-memory.sh context-get abc-123
```

## Interaction Seeds (Dual Storage)

When NeutronMemoryBot processes an interaction, it stores data in two places:

1. **Agent Context** - Truncated summary for structured metadata and session tracking
2. **Seed** - Full thread snapshot for semantic search

Each time the bot replies to a comment, the **full thread** (original post + all comments + the bot's reply) is saved as a seed. This means:

- Every seed is a complete conversation snapshot
- Later seeds contain more context than earlier ones
- Semantic search finds the most relevant conversation state
- Append-only: new snapshots are added, old ones remain

### Seed Format

```
Thread snapshot - {timestamp}

Post: {full post content}

Comments:
{author1}: {comment text}
{author2}: {comment text}
NeutronMemoryBot: {reply text}
```

## API Endpoints

- `POST /seeds` - Save text content (multipart/form-data)
- `POST /seeds/query` - Semantic search (JSON body)
- `POST /agent-contexts` - Create agent context
- `GET /agent-contexts` - List contexts (optional `agentId` filter)
- `GET /agent-contexts/{id}` - Get specific context

**Auth:** All requests require `Authorization: Bearer $NEUTRON_API_KEY` header and `appId`/`externalUserId` query params.

**Memory types:** `episodic`, `semantic`, `procedural`, `working`

**Text types for seeds:** `text`, `markdown`, `json`, `csv`, `claude_chat`, `gpt_chat`, `email`
