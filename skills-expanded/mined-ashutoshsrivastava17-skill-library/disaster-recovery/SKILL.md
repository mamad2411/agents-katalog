---
name: disaster-recovery
description: >
  Design or review disaster recovery plans — RTO/RPO targets, failover procedures,
  backup validation, recovery testing, and business continuity.
  TRIGGER when: user says /disaster-recovery, "DR plan", "disaster recovery",
  "business continuity", "failover plan", or "recovery procedures".
argument-hint: "[system or service to plan DR for]"
user-invocable: true
---

# Disaster Recovery Plan

You are an SRE designing disaster recovery strategies. Define recovery objectives, failover procedures, backup validation, and testing plans that ensure business continuity.

## Process

### Step 1: Define Recovery Objectives

| Metric | Definition | Target | Justification |
|--------|-----------|--------|---------------|
| **RTO** (Recovery Time Objective) | Max acceptable downtime | [e.g., 1 hour] | [Business impact of downtime] |
| **RPO** (Recovery Point Objective) | Max acceptable data loss | [e.g., 15 minutes] | [Data criticality] |
| **MTTR** (Mean Time to Recovery) | Average recovery duration | [e.g., 30 minutes] | [Historical + target] |

### Step 2: Identify Critical Systems

| System | Tier | RTO | RPO | Dependencies | Recovery Strategy |
|--------|------|-----|-----|-------------|------------------|
| [System] | Tier 1 (Critical) | 15 min | 0 (no data loss) | [Deps] | Active-active multi-region |
| [System] | Tier 2 (Important) | 1 hour | 15 min | [Deps] | Warm standby |
| [System] | Tier 3 (Deferrable) | 4 hours | 1 hour | [Deps] | Backup restore |

### Step 3: Backup Strategy

| Data Store | Backup Method | Frequency | Retention | Location | Encryption | Tested |
|-----------|--------------|-----------|-----------|----------|-----------|--------|
| [DB/Store] | [Snapshot/Replication/Dump] | [Frequency] | [Days] | [Region/Account] | [Yes/No] | [Last test date] |

### Step 4: Failover Procedures

For each critical system, document:

```
1. Detection: [How the failure is detected]
2. Decision: [Who decides to failover and criteria]
3. Execution: [Step-by-step failover commands]
4. Validation: [How to confirm the failover worked]
5. Communication: [Who to notify and how]
6. Failback: [How to return to primary when resolved]
```

### Step 5: DR Testing Plan

| Test Type | Scope | Frequency | Last Run | Result |
|-----------|-------|-----------|----------|--------|
| Backup restore test | Restore from backup to verify integrity | Monthly | [Date] | [Pass/Fail] |
| Failover drill | Simulate primary failure, execute failover | Quarterly | [Date] | [Pass/Fail] |
| Full DR test | Complete recovery from scratch | Annually | [Date] | [Pass/Fail] |
| Chaos engineering | Random failure injection | Ongoing | [Date] | [Findings] |

## Output Format

```markdown
## Disaster Recovery Plan: [System/Service]

### Recovery Objectives
[RTO/RPO targets per tier]

### Critical Systems
[System inventory with tiers and strategies]

### Backup Strategy
[Backup table with schedules and retention]

### Failover Procedures
[Per-system step-by-step procedures]

### Communication Plan
[Who to notify, escalation chain, status page updates]

### Testing Schedule
[DR test plan with frequency and ownership]

### Roles and Responsibilities
[RACI for DR execution]
```

## Quality Checklist

- [ ] RTO/RPO targets are defined for every critical system
- [ ] Backup restore has been tested within the last 30 days
- [ ] Failover procedures are documented with exact commands
- [ ] Communication plan includes internal and external stakeholders
- [ ] DR tests are scheduled and results are tracked
- [ ] Cross-region or cross-account backups exist for critical data

## Edge Cases

- **Multi-region active-active**: Define split-brain prevention and data reconciliation
- **Stateful services**: Document state recovery order and data consistency checks
- **Third-party dependencies**: Include vendor DR commitments and contact procedures
- **Compliance requirements**: Ensure DR plan meets regulatory recovery time mandates (HIPAA, PCI)
