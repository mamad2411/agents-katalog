---
name: jadegate-trust
description: Manage TOFU (Trust On First Use) certificates and Ed25519 cryptographic signatures for MCP server identity verification.
---

# Certificate Trust Manager

Manage TOFU (Trust On First Use) certificates and Ed25519 cryptographic signatures for MCP server identity verification.

## When to Use

- User asks about MCP server identity or trust
- User wants to manage certificates
- User asks about cryptographic verification of skills

## Usage

```bash
jadegate cert list                     # List all trusted certificates
```

## How TOFU Works

1. First encounter with an MCP server creates a certificate fingerprint
2. Subsequent connections verify the fingerprint matches
3. If fingerprint changes, JadeGate alerts the user (possible MITM)
4. Ed25519 signatures verify skill provenance

## Trust Model

Similar to SSH known_hosts or browser certificate pinning — trust is established on first use and verified on every subsequent connection.
