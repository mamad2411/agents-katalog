---
name: crowdsec-protect
description: Collaborative security engine with CrowdSec
version: 1.0.0
tags: [security, firewall, intrusion-detection, self-hosted]
---

# CrowdSec – Collaborative Security Engine

CrowdSec detects and blocks threats using behaviour analysis
and a crowd-sourced IP reputation database.

- **GitHub**: github.com/crowdsecurity/crowdsec (10 000+ ⭐)
- **License**: MIT
- **Security**: Designed for security. Community-curated blocklists. No malware.

## Environment Variables

| Variable | Description |
|---|---|
| `{{CROWDSEC_URL}}` | Local CrowdSec API URL |
| `{{CROWDSEC_API_KEY}}` | Bouncer API key |

## Usage Examples

### List alerts

```bash
curl -s "{{CROWDSEC_URL}}/v1/alerts" \
  -H "Authorization: Bearer {{CROWDSEC_API_KEY}}"
```

### List decisions (bans)

```bash
curl -s "{{CROWDSEC_URL}}/v1/decisions" \
  -H "Authorization: Bearer {{CROWDSEC_API_KEY}}"
```

## AI Agent Tips

- Analyses logs to detect attacks (brute force, scanning, etc.).
- Bouncers enforce decisions at the firewall/proxy level.
- Community threat intelligence shared across 100K+ users.
- Integrates with Traefik, Nginx, iptables, and more.
