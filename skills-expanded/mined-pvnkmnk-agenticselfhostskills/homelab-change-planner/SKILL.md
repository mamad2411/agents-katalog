---
name: homelab-change-planner
description: Plans homelab infrastructure changes with pre-flight checks, rollback strategies, and impact analysis before any execution.
---

# homelab-change-planner

Produces a structured change plan before any homelab infrastructure modification. Ensures every change has a defined scope, risk level, rollback path, and approval gate before execution begins.

## Invocation

**OpenCode / Codex:** `Invoke homelab-change-planner`
**Freebuff:** `/skill homelab-change-planner`

## Workflow Steps

1. **State snapshot:** Run `homelab-topology-mapper` to capture current state of affected hosts/services.
2. **Define change:** Describe the intended change, target host/container/service, and expected outcome.
3. **Impact analysis:** Identify downstream dependencies, services affected, and data at risk.
4. **Risk rating:** Assign LOW / MEDIUM / HIGH based on reversibility and blast radius.
5. **Rollback plan:** Write the exact steps to undo the change if it fails.
6. **Approval gate:** Present the plan. Do not proceed without explicit user confirmation.
7. **Execute:** Carry out the change step by step, confirming each step before proceeding.
8. **Post-check:** Verify services are healthy after the change.
9. **Log:** Record the change in `homelab-logbook` and `obsidian-homelab-logbook`.

## Change Plan Template

```
Change: <one-line description>
Target: <host / container / service>
Risk: LOW | MEDIUM | HIGH
Reason: <why this change is needed>
Steps:
  1. <step>
  2. <step>
Rollback:
  1. <undo step>
  2. <undo step>
Dependencies affected: <list>
Backup confirmed: YES | NO
```

## Companion Skills

- `homelab-safe-ops` — safety gate
- `homelab-topology-mapper` — state snapshot
- `homelab-logbook` — post-change logging
- `homelab-monitoring-analyst` — post-change health check

## References

- Proxmox VE docs: https://pve.proxmox.com/wiki/Main_Page
