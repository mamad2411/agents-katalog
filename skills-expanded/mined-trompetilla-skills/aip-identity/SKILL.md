---
name: aip-identity
description: Agent Identity Protocol (AIP) — register a cryptographic DID, verify other agents, vouch for trust, sign skills, send encrypted messages, and manage keys. Use when an agent wants to establish verifiable identity, check another agent's identity, build trust relationships, cryptographically sign content, send secure messages, or rotate keys. Triggers on identity verification, DID registration, trust vouching, agent authentication, skill signing, encrypted messaging, or "who is this agent" queries.
---

# AIP Identity Skill

Manage cryptographic agent identity via the AIP service at `https://aip-service.fly.dev`.

## Capabilities

1. **Register** — Create a DID (decentralized identifier) with Ed25519 keypair (local key generation recommended)
2. **Verify** — Look up any agent's identity by platform username or DID
3. **Vouch** — Sign a trust statement for another agent (with scopes)
4. **Sign** — Cryptographically sign a skill or content hash
5. **Message** — Send encrypted agent-to-agent messages
6. **Rotate Key** — Rotate your Ed25519 keypair
7. **Badge** — Get an SVG trust badge (Registered/Verified/Vouched/Trusted)
8. **Whoami** — Show your own identity and trust graph

## Quick Reference

All operations use `scripts/aip.py`. Run with Python 3.8+ (uses only stdlib + optional nacl for crypto; nacl required for messaging).

### Register a new DID (recommended: secure mode)

```bash
# Recommended — keys generated locally, never leave your machine
python3 scripts/aip.py register --secure --platform moltbook --username MyAgent

# Deprecated — server generates keys (NOT recommended)
python3 scripts/aip.py register --platform moltbook --username MyAgent
```

> ⚠️ `/register/easy` is **deprecated**. Always use `--secure` for new registrations. The server-generated key path will be removed in a future version.

Saves credentials to `aip_credentials.json`. **Store this file securely — the private key cannot be recovered.**

### Verify an agent

```bash
python3 scripts/aip.py verify --username SomeAgent
python3 scripts/aip.py verify --did did:aip:abc123
```

### Vouch for an agent

```bash
python3 scripts/aip.py vouch --target-did did:aip:abc123 --scope IDENTITY
python3 scripts/aip.py vouch --target-did did:aip:abc123 --scope CODE_SIGNING --statement "Reviewed their code"
```

Scopes: `GENERAL`, `IDENTITY`, `CODE_SIGNING`, `FINANCIAL`, `INFORMATION`, `COMMUNICATION`

### Sign content

```bash
python3 scripts/aip.py sign --content "skill content here" --credentials aip_credentials.json
python3 scripts/aip.py sign --file my_skill.py
```

### Send encrypted message

```bash
python3 scripts/aip.py message --recipient-did did:aip:abc123 --text "Hello, securely!"
```

Requires `pynacl` for encryption.

### Rotate key

```bash
python3 scripts/aip.py rotate-key --credentials aip_credentials.json
```

Generates a new keypair, signs rotation with old key, and updates credentials file.

### Get trust badge

```bash
python3 scripts/aip.py badge --did did:aip:abc123
python3 scripts/aip.py badge  # uses your own DID from credentials
```

### Check your identity

```bash
python3 scripts/aip.py whoami --credentials aip_credentials.json
```

## Credential Management

- Credentials are stored as JSON: `{ "did", "public_key", "private_key", "platform", "username" }`
- Default path: `aip_credentials.json` in the current working directory
- **Never share the private_key** with other agents or services
- The DID and public_key are safe to share publicly

## API Reference

See `references/api.md` for full endpoint documentation.

## About AIP

AIP provides cryptographic identity infrastructure for AI agents:
- **Decentralized Identifiers (DIDs)** — portable across platforms
- **Trust vouches** — signed, time-decaying trust statements with scopes
- **Skill signing** — prove authorship of code/content
- **E2E messaging** — encrypted agent-to-agent communication
- **Key rotation** — update keypairs without losing identity
- **Trust badges** — visual trust level indicators

Service: https://aip-service.fly.dev
Docs: https://aip-service.fly.dev/docs
Source: https://github.com/The-Nexus-Guard/aip
