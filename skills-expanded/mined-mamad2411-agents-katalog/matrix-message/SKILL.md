---
name: matrix-message
description: "Send messages and manage rooms using Matrix Synapse at {{MATRIX_HOST}}:{{MATRIX_PORT}}."
metadata:
  openclaw:
    emoji: "🟢"
---

# Matrix Messaging

Matrix Synapse is available at `http://{{MATRIX_HOST}}:{{MATRIX_PORT}}` within the Docker network.

## Send a Message

```bash
curl -X PUT "http://{{MATRIX_HOST}}:{{MATRIX_PORT}}/_matrix/client/v3/rooms/{room_id}/send/m.room.message/{txn_id}" \
  -H "Content-Type: application/json" \
  -H "Authorization: Bearer $MATRIX_ACCESS_TOKEN" \
  -d '{"msgtype": "m.text", "body": "Hello from OpenClaw!"}'
```

## Tips for AI Agents

- Matrix is a decentralized protocol — rooms can span multiple servers.
- Use end-to-end encryption for sensitive communications.
- Supports file uploads, reactions, and threaded conversations.
