---
name: memory-store
description: Store a memory in the long-term vector database. Use this to save important facts, decisions, client information, or conversation summaries that should persist across sessions. Always include a client_id for client-specific data, or use "global" for general knowledge.
metadata:
  openclaw:
    requires:
      bins: ["curl", "jq"]
      env: ["QDRANT_API_KEY"]
---

# Memory Store

Store a memory in the Qdrant vector database for long-term retrieval.

## Usage
```bash
bash ~/.openclaw/skills/memory-store/store.sh \
  --text "The actual content to remember" \
  --client_id "global" \
  --category "semantic" \
  --importance "high"
```

## Parameters

- `--text` (required): The memory content to store. Be specific and factual.
- `--client_id` (required): Client identifier or "global" for non-client data.
- `--category`: One of: episodic, semantic, procedural. Default: semantic.
- `--importance`: One of: critical, high, medium, low. Default: medium.

## Security rules
- NEVER store API keys, tokens, passwords, or credentials
- NEVER store raw email content (summarize instead)
- Client data is isolated by client_id — always set correctly
- All text is scrubbed for common credential patterns before embedding
