---
name: context-continuity
description: Use to create or maintain project maps, session logs, state files, known-issues notes, or durable agent handoff context.
---

# Context Continuity

Use durable context when it will save future rediscovery. Do not create memory files for tiny throwaway tasks.

## Files

- `project-map.md`: stable repo structure and source-of-truth paths.
- `session-log.md`: decisions, rejected paths, and why.
- `state.md`: current plan, progress, blockers, resume point.
- `known-issues.md`: recurring error -> fix mappings.

## Rules

- Current user instructions and repo evidence outrank memory.
- Do not store secrets, credentials, raw private data, or sensitive personal content.
- Keep entries short, dated, and source-linked.
- Update maps surgically rather than rewriting them.
- Mark stale or uncertain entries.

## When To Use

- Long-running implementation.
- Multi-session repo work.
- Repeated debugging.
- Complex architectural decisions.
- Handoffs to another thread or agent.

## Minimal Entry

```md
## YYYY-MM-DD
- Decision:
- Evidence:
- Rejected:
- Next:
```

