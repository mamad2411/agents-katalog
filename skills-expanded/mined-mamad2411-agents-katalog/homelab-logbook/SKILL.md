---
name: homelab-logbook
description: Records all homelab changes, incidents, and maintenance events to a structured, searchable log.
---

# homelab-logbook

Provides a structured record of every homelab change, incident, and maintenance event. Acts as the primary audit trail for all infrastructure operations. Feeds into `obsidian-homelab-logbook` for vault-based knowledge storage.

## Invocation

**OpenCode / Codex:** `Invoke homelab-logbook`
**Freebuff:** `/skill homelab-logbook`

## Log Entry Format

```
Date: YYYY-MM-DD HH:MM
Type: change | incident | maintenance | observation
Host: <hostname or service>
Severity: low | medium | high
Summary: <one-line summary>
Details: <what happened, what was done>
Result: success | partial | failed | ongoing
Rollback: N/A | <rollback steps if needed>
```

## Workflow Steps

1. **Classify:** Determine entry type (change, incident, maintenance, observation).
2. **Capture:** Record the event details using the log entry format above.
3. **Store:** Append to the running log file and to `obsidian-homelab-logbook`.
4. **Tag:** Apply host and severity tags.
5. **Index:** Update the homelab log index if a new host or service appears.

## Companion Skills

- `obsidian-homelab-logbook` — vault storage layer
- `homelab-change-planner` — call before changes; log after
- `homelab-monitoring-analyst` — log monitoring findings
