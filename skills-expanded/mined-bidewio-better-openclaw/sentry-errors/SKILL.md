---
name: sentry-errors
description: Application error tracking with Sentry
version: 1.0.0
tags: [monitoring, errors, debugging, apm]
---

# Sentry – Error Tracking & Performance

Sentry is an application monitoring platform for error tracking,
performance monitoring, and release health with real-time alerts.

- **GitHub**: github.com/getsentry/sentry (42 000+ ⭐)
- **License**: FSL (Functional Source License → Apache-2.0 after 2 years)
- **Security**: Self-hostable. 100K+ organisations use Sentry. No malware.

## Environment Variables

| Variable | Description |
|---|---|
| `{{SENTRY_URL}}` | Self-hosted Sentry URL |
| `{{SENTRY_AUTH_TOKEN}}` | Authentication token |
| `{{SENTRY_DSN}}` | Data Source Name for SDK initialisation |

## Usage Examples

### List projects

```bash
curl -s "{{SENTRY_URL}}/api/0/projects/" \
  -H "Authorization: Bearer {{SENTRY_AUTH_TOKEN}}"
```

### List recent issues

```bash
curl -s "{{SENTRY_URL}}/api/0/projects/<org>/<project>/issues/" \
  -H "Authorization: Bearer {{SENTRY_AUTH_TOKEN}}"
```

## AI Agent Tips

- SDKs for 100+ platforms (JavaScript, Python, Go, Java, etc.).
- Stack traces, breadcrumbs, and context for fast debugging.
- Performance monitoring shows slow transactions and bottlenecks.
- Self-hosted version via Docker Compose for full data control.
