---
name: bluebox-overview
description: Teaches a coding agent what Bluebox is, when to invoke it, and how to phrase requests so the agent picks the right Bluebox skill — investigation, instrumentation, or monitoring.
compatibility: Installed into coding agents by `bluebox setup`; compatible with Claude Code, Cursor, Windsurf, GitHub Copilot, Kiro, OpenCode, and Codex.
metadata:
  version: '1.2'
---

# Bluebox Overview

Bluebox is an autonomous SRE agent platform that connects your codebase, CI/CD pipeline, and Dynatrace observability data. It runs AI-driven agents that investigate production incidents, instrument services, and verify deployments — without requiring manual context switching between your IDE, dashboards, and runbooks.

## When to use Bluebox

Reach for Bluebox when you need to:

- **Investigate a production incident** — Bluebox gathers Dynatrace problems, logs, traces, and metrics, correlates them with recent code changes, and delivers a structured root-cause diagnosis.
- **Instrument a service** — Bluebox detects your language and deployment model, then sets up repo-local OpenTelemetry for server-side traces. Metrics and logs are optional follow-up scope; RUM, AppSec, infrastructure monitoring, synthetics, SLOs, dashboards, and alerts require separate setup paths.
- **Monitor and verify a deploy** — Bluebox compares service health against a pre-deploy baseline and routes to remediation if regressions are detected.

## Example prompts

### Investigation
- "investigate the latest production error"
- "check why the checkout service is slow"
- "analyze the most recent deployment"
- "why did the payment service start throwing 5xx errors after today's release?"

### Instrumentation
- "add OpenTelemetry to this service"
- "instrument the API endpoints"
- "set up distributed tracing for the orders service"

### Monitoring
- "set up an SLO for the search service"
- "configure an alert when error rate exceeds 1%"
- "verify the deploy didn't degrade P99 latency"

## Learning more about Bluebox

The prompts above ask Bluebox to act **on the user's own services**. When the user instead asks a conceptual or how-to question **about Bluebox itself** — what it does, how to set it up, how its concepts work, or how it handles their data — answer it by running `bluebox ask` yourself and relaying what it returns:

```bash
bluebox ask "<question>"
```

For example:

- `bluebox ask "what is Bluebox and how does it work?"`
- `bluebox ask "how does Bluebox handle my data and privacy?"`
- `bluebox ask "what's the difference between Chat and Investigations?"`

Rule of thumb: run `bluebox ask` yourself for **questions about Bluebox**, and use the investigation, instrumentation, and monitoring prompts above for **Bluebox acting on the user's infrastructure**.

## Setup

If initial setup is needed, run `bluebox setup` and follow its instructions.
