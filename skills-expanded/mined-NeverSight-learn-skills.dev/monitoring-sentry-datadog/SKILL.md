---
name: monitoring-sentry-datadog
description: Use when adding error tracking, monitoring, or observability to a Gemini or AI application, setting up Sentry for error tracking or Datadog for metrics and APM
---

# Monitoring with Sentry & Datadog

## Overview

Add production monitoring to Gemini API applications. Sentry for error tracking and crash reporting; Datadog for metrics, APM, and dashboards. Can use one or both.

## When to Use

- User says "監視入れて", "add monitoring", "add error tracking"
- App is deployed and needs observability
- User is experiencing errors in production and has no visibility

**When NOT to use:** For local development debugging.

## Platform Decision

| Need | Sentry | Datadog |
|------|--------|---------|
| Error tracking | Excellent | Good |
| APM / Traces | Good | Excellent |
| Custom metrics | Limited | Excellent |
| Free tier | 5K errors/mo | 14-day trial |
| Setup effort | 5 min | 15 min |
| Best for | "Just tell me when it breaks" | "I need dashboards and deep metrics" |

**Recommendation:** Start with Sentry (fast setup, free tier). Add Datadog when you need metrics/dashboards.

## Sentry Quick Setup (Python)

```python
# pip install sentry-sdk
import sentry_sdk

sentry_sdk.init(
    dsn=os.environ["SENTRY_DSN"],
    traces_sample_rate=0.1,
    environment=os.environ.get("ENVIRONMENT", "production"),
)
```

## Sentry Quick Setup (Node.js)

```javascript
// npm install @sentry/node
const Sentry = require("@sentry/node");

Sentry.init({
  dsn: process.env.SENTRY_DSN,
  tracesSampleRate: 0.1,
  environment: process.env.ENVIRONMENT || "production",
});
```

## Key Metrics to Track for Gemini Apps

| Metric | Why |
|--------|-----|
| Gemini API latency | Detect slowdowns |
| Token usage per request | Cost monitoring |
| Error rate by endpoint | Identify failing routes |
| Rate limit hits (429s) | Capacity planning |
| Response quality scores | If using evals |

## Implementation Steps

1. **Create Sentry project** at sentry.io (or self-hosted)
2. **Install SDK** and initialize in app entry point
3. **Add DSN to environment** — Secret Manager or platform env vars
4. **Tag requests** — Add user context, request IDs
5. **Set up alerts** — Error spike, latency threshold
6. **(Optional) Add Datadog** — Install agent, configure APM

## Common Mistakes

- **`traces_sample_rate=1.0` in production** — Sample at 0.1 or lower to control costs
- **Missing environment tag** — Always set `environment` to distinguish staging/production
- **No source maps (Node.js)** — Upload source maps for readable stack traces
- **Ignoring Gemini API errors** — Catch and report `google.api_core.exceptions` explicitly
