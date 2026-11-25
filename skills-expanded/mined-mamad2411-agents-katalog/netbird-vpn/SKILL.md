---
name: netbird-vpn
description: Zero-trust mesh networking with NetBird
version: 1.0.0
tags: [networking, vpn, zero-trust, mesh]
---

# NetBird – Zero-Trust Mesh VPN

NetBird creates encrypted peer-to-peer WireGuard tunnels between
your machines with zero-trust access controls.

- **GitHub**: github.com/netbirdio/netbird (12 000+ ⭐)
- **License**: BSD-3-Clause
- **Security**: WireGuard-based encryption. No malware.

## Environment Variables

| Variable | Description |
|---|---|
| `{{NETBIRD_URL}}` | Management API URL |
| `{{NETBIRD_API_TOKEN}}` | API token |

## Usage Examples

### List peers

```bash
curl -s "{{NETBIRD_URL}}/api/peers" \
  -H "Authorization: Token {{NETBIRD_API_TOKEN}}"
```

### List groups

```bash
curl -s "{{NETBIRD_URL}}/api/groups" \
  -H "Authorization: Token {{NETBIRD_API_TOKEN}}"
```

## AI Agent Tips

- Peer-to-peer WireGuard tunnels — no central relay needed.
- Access control policies define who can reach what.
- Self-hosted management server for full control.
- Integrates with Authentik, Keycloak, and other IdPs for SSO.
