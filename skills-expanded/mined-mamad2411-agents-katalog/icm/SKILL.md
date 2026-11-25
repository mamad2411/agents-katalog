---
name: icm
description: Provides the ICM (Infinite Context Memory) persistent-memory rule for Codex. Use when persistent memory should be consulted or maintained for a task, when the user asks to use ICM generally, or when durable context such as user preferences, resolved errors, architecture decisions, or significant project progress should persist across Codex sessions.
---

# ICM

Use ICM as Codex persistent memory when durable context is likely to matter.

## Recall First

At task start, search relevant past context. Prefer the ICM MCP recall tool. If
MCP is unavailable, use the local ICM CLI through `rtk run`:

```bash
rtk run 'icm recall "query"'
```

## Store

Before replying, store privacy-safe durable facts:

- Resolved error: topic `errors-resolved`, importance `high`.
- Architecture decision: topic `decisions-{project}`, importance `high`.
- User preference: topic `preferences`, importance `critical`.
- Significant progress or completion: topic `context-{project}`, importance `high`.
- Long run without a store: save a concise progress summary.

Prefer ICM MCP store when available. If MCP is unavailable, use the local ICM
CLI through `rtk run`:

```bash
rtk run 'icm store -t "topic" -c "summary" -i high'
```

Never store secrets, tokens, passwords, recovery codes, private personal data, or raw session exports. Keep ICM Codex-facing unless the user says otherwise; do not add other harness setup or touch install directories for ICM cleanup.
