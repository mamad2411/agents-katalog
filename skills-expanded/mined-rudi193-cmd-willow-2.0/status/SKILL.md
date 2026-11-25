---
name: status
description: System status — atoms, edges, ratio, boot health, unpushed work, open threads
---

@markdownai v1.0

# /status — System Status

Quick read of where things stand. No writes, no changes — just source ring.

## TOOL PRE-LOAD (first action after invocation)

```
ToolSearch query: "select:mcp__willow__fleet_status,mcp__willow__soil_search,mcp__willow__soil_stats,mcp__willow__agent_task_list"
```

## Report

1. **Boot health** — Postgres, Ollama, manifests (from `fleet_status`)
2. **Agent schema** — atom count, edge count, edges/atoms ratio (from `soil_stats`)
3. **Fleet** — models available, manifest pass/fail
4. **Open work** — `soil_list(<agent>/flags)` top 5 by severity, status=open
5. **Unpushed** — uncommitted/unpushed code changes (`git status`, `git log @{u}..`)
6. **Session delta** — atoms written this session, edges created

## Rules
- Read only. No writes.
- Keep it concise. Plain language, not tables (USER's preference).
- Compare numbers against targets — don't report raw numbers without the frame.
