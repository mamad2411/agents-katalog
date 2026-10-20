---
name: signoz-observe
description: Full-stack observability with SigNoz
version: 1.0.0
tags: [monitoring, observability, apm, tracing]
---

# SigNoz – Open-Source Observability

SigNoz is an open-source APM providing metrics, traces, and logs
in a single platform — an alternative to Datadog/New Relic.

- **GitHub**: github.com/SigNoz/signoz (20 000+ ⭐)
- **License**: MIT (frontend) / AGPL-3.0 (backend)
- **Security**: OpenTelemetry-native. No malware.

## Environment Variables

| Variable | Description |
|---|---|
| `{{SIGNOZ_URL}}` | Base URL of the SigNoz instance |

## Usage Examples

### Check health

```bash
curl -s "{{SIGNOZ_URL}}/api/v1/health"
```

## AI Agent Tips

- OpenTelemetry-native — instrument once, observe everywhere.
- Unified view of metrics, traces, and logs.
- ClickHouse-powered for fast analytical queries.
- Self-hosted alternative to Datadog with no per-host pricing.
