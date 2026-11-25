---
name: context-guru-insights
description: Analyze measured context, token, prompt-cache, idle-time, and tool costs. Use when asked what wastes tokens or money, what to optimize, or for context-guru recommendations.
---

# Analyze Codex context cost

Run `python3 ../../scripts/insights.py all`. Report its ranked findings in order and preserve every
measurement label and fix command exactly. The script—not the model—does the arithmetic and sorting.
Stop on `not_installed` or `proxy_unavailable`. On a subscription plan, describe dollar values as
estimated usage-limit value rather than a lower bill.

Codex command sandboxes may block the local `127.0.0.1` dashboard. On `proxy_unavailable`, retry
the same read-only command with `sandbox_permissions="require_escalated"`, explaining that
loopback access is needed. If that retry cannot run, report the measurements as unverified rather
than claiming that the proxy is unavailable.
