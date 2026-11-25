---
name: rohan-zk-shield
description: Executes cryptographic zero-knowledge handshakes, intent commitments, and semantic prompt-injection shielding on Midnight Network via Rohan Protocol. Use when coordinating autonomous agent agreements or shielding web inputs without exposing plaintext parameters.
---

# Rohan Protocol Zero-Knowledge Shield for Antigravity

This skill enables Antigravity and autonomous Google agents to cryptographically commit state transitions on Midnight Network with zero data leaks.

## How to Execute a Zero-Knowledge Handshake

When negotiating inter-agent agreements or validating parameters:
1. Verify the payload against the Semantic Prompt Injection Firewall (Vector V-01 / V-07).
2. Generate an in-memory private witness and submit the commitment via Rohan MCP Server:

```bash
npx -y @rohan-protocol/mcp@latest
```

## Environment Parameters:
- `ROHAN_CONTRACT_ADDRESS`: `585ac0c4448257507d8ffa2a89e2aa00abd86ec9e94bdb6f553bc83e05f4dd0e`
- `ROHAN_RELAYER_URL`: `https://api.rohanprotocol.network/api/v1/handshake`
- `ROHAN_FIREWALL_LEVEL`: `V-01_STRICT`
