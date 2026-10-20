---
name: homelab-sre-agent
description: Applies Site Reliability Engineering practices to homelab operations including SLOs, toil reduction, and incident management.
---

# homelab-sre-agent

Brings SRE discipline to homelab operations. Defines service level objectives, identifies and reduces toil, manages incident lifecycles, and drives continuous improvement through post-incident reviews.

## Invocation

**OpenCode / Codex:** `Invoke homelab-sre-agent`
**Freebuff:** `/skill homelab-sre-agent`

## Core Responsibilities

### SLO Management
- Define availability and latency targets per service.
- Track SLO burn rate and alert budget consumption.
- Recommend interventions when error budget is low.

### Toil Reduction
- Identify repetitive manual operations.
- Propose automation to eliminate toil (scripts, cron jobs, Ansible tasks).
- Track toil-hours saved.

### Incident Management
1. **Detect:** Alert fires or user reports issue.
2. **Triage:** Assess severity and impact.
3. **Mitigate:** Apply fastest path to restore service.
4. **Root cause:** Investigate underlying failure.
5. **Post-mortem:** Write blameless post-incident review.
6. **Action items:** Define follow-up improvements.

### Reliability Reviews
- Periodically review change frequency, MTTR, and incident count.
- Identify fragile components and propose hardening.

## Companion Skills

- `homelab-monitoring-analyst` — detect and diagnose
- `homelab-change-planner` — implement fixes safely
- `homelab-logbook` — record all incidents
- `homelab-safe-ops` — safety gate

## References

- Google SRE Book: https://sre.google/sre-book/table-of-contents/
