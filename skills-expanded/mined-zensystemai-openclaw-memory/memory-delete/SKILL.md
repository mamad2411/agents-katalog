---
name: memory-delete
description: Delete memories from long-term storage. Use for GDPR erasure requests (delete all data for a client), or to remove specific outdated/incorrect memories. Requires Steven's explicit approval for bulk deletions.
metadata:
  openclaw:
    requires:
      bins: ["curl", "jq"]
      env: ["QDRANT_API_KEY"]
---

# Memory Delete

Delete memories from the Qdrant vector database.

## Usage
```bash
# Delete all memories for a specific client (GDPR erasure)
bash ~/.openclaw/skills/memory-delete/delete.sh \
  --client_id "client_name" \
  --confirm

# Delete a specific memory by ID
bash ~/.openclaw/skills/memory-delete/delete.sh \
  --point_id 123456789
```

## Parameters

- `--client_id`: Delete ALL memories for this client. Requires --confirm.
- `--point_id`: Delete a single memory by point ID.
- `--confirm`: Required for bulk client deletion (safety gate).

## Security rules
- Bulk deletion (by client_id) ALWAYS requires --confirm flag
- Steven must explicitly approve GDPR erasure requests
- Deletion is permanent — no undo
- Always log what was deleted
