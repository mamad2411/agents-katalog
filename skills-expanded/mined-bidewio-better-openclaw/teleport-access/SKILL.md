---
name: teleport-access
description: Zero-trust infrastructure access with Teleport
version: 1.0.0
tags: [security, access, ssh, kubernetes, zero-trust]
---

# Teleport – Zero-Trust Infrastructure Access

Teleport provides identity-based access to servers, databases,
Kubernetes clusters, and web apps with audit logging.

- **GitHub**: github.com/gravitational/teleport (18 000+ ⭐)
- **License**: Apache-2.0 (Community Edition)
- **Security**: SOC 2 / FedRAMP compliant. No malware.

## Environment Variables

| Variable | Description |
|---|---|
| `{{TELEPORT_URL}}` | Teleport proxy address |
| `{{TELEPORT_TOKEN}}` | Join token or API credentials |

## Usage Examples

### List nodes via tctl

```bash
tctl --auth-server={{TELEPORT_URL}} nodes ls
```

### SSH to a node via tsh

```bash
tsh --proxy={{TELEPORT_URL}} ssh user@node-name
```

## AI Agent Tips

- Certificate-based, passwordless access to infrastructure.
- Session recording and audit trail for compliance.
- Access requests and approval workflows built-in.
- Supports SSH, Kubernetes, databases, Windows RDP, and web apps.
