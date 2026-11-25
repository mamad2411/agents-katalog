---
name: gatus-health
description: Automated health monitoring with Gatus
version: 1.0.0
tags: [monitoring, health-check, uptime, alerting]
---

# Gatus – Health Dashboard

Gatus monitors endpoints and displays results on a dashboard
with alerting support for Slack, Discord, PagerDuty, and more.

- **GitHub**: github.com/TwiN/gatus (7 000+ ⭐)
- **License**: Apache-2.0
- **Security**: Lightweight Go binary. No malware.

## Environment Variables

| Variable | Description |
|---|---|
| `{{GATUS_URL}}` | Base URL of Gatus |

## Usage Examples

### Get endpoint statuses

```bash
curl -s "{{GATUS_URL}}/api/v1/endpoints/statuses"
```

## AI Agent Tips

- Configure endpoints in YAML with conditions (status code, response time, body).
- Supports HTTP, TCP, DNS, ICMP, and SSH checks.
- Alerts via Slack, Discord, Teams, PagerDuty, email, and webhooks.
- Lightweight — single Go binary with embedded UI.
