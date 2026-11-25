---
name: vaultwarden-manage
description: Self-hosted password management with Vaultwarden
version: 1.0.0
tags: [security, passwords, vault, bitwarden]
---

# Vaultwarden – Self-Hosted Password Vault

Vaultwarden is a lightweight, Rust-based Bitwarden-compatible server
for self-hosted password management.

- **GitHub**: github.com/dani-garcia/vaultwarden (45 000+ ⭐)
- **License**: AGPL-3.0
- **Security**: Community-audited Rust codebase. Bitwarden protocol compliant. No malware.

## Environment Variables

| Variable | Description |
|---|---|
| `{{VAULTWARDEN_URL}}` | Base URL of the Vaultwarden instance |
| `{{VAULTWARDEN_ADMIN_TOKEN}}` | Admin panel token |

## Usage Examples

### Check server status

```bash
curl -s "{{VAULTWARDEN_URL}}/api/alive"
```

### Access admin panel

```bash
curl -s "{{VAULTWARDEN_URL}}/admin" \
  -H "Cookie: VW_ADMIN={{VAULTWARDEN_ADMIN_TOKEN}}"
```

## AI Agent Tips

- Use official Bitwarden clients (browser extensions, mobile, CLI) to connect.
- Admin API enables user management, organisation control, and diagnostics.
- Always enable HTTPS and strong admin tokens.
- Supports WebSocket for live sync between clients.
