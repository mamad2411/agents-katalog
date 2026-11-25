---
name: cloud-cost
last_reviewed: 2026-09-06
group: Ship and run
description: >-
  Cut cloud spend with unit economics, rightsizing, showback and commitment planning. Use when
  optimizing AWS/GCP bills, right-sizing, or FinOps practices.
---

# Cloud Cost

Applies FinOps discipline to cloud infrastructure, optimizing cost efficiency through visibility, allocation, and continuous rightsizing.

## Phased Workflow

### Phase 1: Cost Visibility & Allocation
1. Implement consistent resource tagging strategy (team, service, environment, cost-center).
2. Build cost dashboards breaking down spend by service, team, environment, and resource type.
3. Establish unit economics: cost per transaction, cost per user, cost per API call.

### Phase 2: Optimization & Rightsizing
1. Identify idle and underutilized resources (CPU < 10%, memory < 20% for 7+ days).
2. Rightsize instances based on actual utilization patterns (downgrade oversized, upgrade throttled).
3. Optimize commitment coverage: Reserved Instances, Savings Plans, spot instances for fault-tolerant workloads.
4. Review storage tiers: move infrequently accessed data to cold/archive storage classes.

### Phase 3: Governance & Continuous Improvement
1. Implement budget alerts and anomaly detection for unexpected spend spikes.
2. Establish monthly FinOps review cadence with engineering and finance stakeholders.
3. Define showback (visibility) or chargeback (billing) model per team/service.

## Verification & Quality Checklist
- [ ] 100% of cloud resources tagged with mandatory cost allocation tags.
- [ ] Idle resources flagged and action plan created within 7 days.
- [ ] RI/Savings Plan coverage targets defined and tracked (target: 60-80% of steady-state).
- [ ] Unit economics calculated for top 5 revenue-generating services.

## Anti-Patterns & Constraints
- NEVER optimize costs at the expense of reliability or availability below SLO thresholds.
- NEVER purchase long-term reservations without 3+ months of stable utilization data.
- NEVER implement chargeback without first building trust through accurate showback reporting.
