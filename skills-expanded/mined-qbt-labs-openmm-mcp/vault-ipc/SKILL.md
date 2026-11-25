# Vault IPC Socket

Unified Unix socket replacing the old two-socket model (x402-signer.sock + openmm-creds.sock).

## Socket
- Path: `/tmp/openmm.sock` (override via `OPENMM_SOCKET` env var)
- Permissions: mode `0600` (owner-only)
- Started by: `openmm serve` after interactive vault unlock

## Message Protocol
JSON messages over the socket, dispatched by `type`:
```json
{ "type": "sign_payment", "payload": {} }
→ { "signature": "0x..." }

{ "type": "get_credentials", "exchange": "mexc" }
→ { "apiKey": "...", "secret": "..." }

{ "type": "ping" }
→ { "status": "ok", "wallet": "0x...", "exchanges": ["mexc", "gateio"] }
```

## signAndWipe Pattern
Private key is decrypted inline, used once, and goes out of scope immediately.
It is NEVER held in a long-lived variable.

## Security Invariants
- Password typed once interactively in terminal — never passed as flag or env var
- Socket file = proof of authentication (exists → vault is unlocked)
- Stale socket cleaned up on startup, deleted on shutdown
- MCP server connects via socket — does NOT hold vault data in its own memory
