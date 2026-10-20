---
name: disaster-recovery-planning
description: >-
  Disaster recovery patterns for Azure workloads. Covers Active-Active,
  Active-Passive, Pilot Light, and Backup & Restore with RTO/RPO tradeoffs,
  implementation checklists, and service-specific replication options.
when-to-use: >-
  Invoke when designing business continuity for Azure workloads, selecting a
  DR pattern, implementing cross-region replication, or planning failover
  and failback procedures.
categories:
  - architecture
  - reliability
  - disaster-recovery
  - azure
---

# Disaster Recovery Planning

DR that isn't tested doesn't work. Define RTO/RPO first, then pick the cheapest pattern that meets both.

## Key Concepts

| Term | Definition |
|---|---|
| **RTO** (Recovery Time Objective) | Maximum acceptable downtime |
| **RPO** (Recovery Point Objective) | Maximum acceptable data loss (time) |
| **Failover** | Switching traffic from primary to secondary region |
| **Failback** | Returning traffic to primary after recovery |

---

## Pattern Comparison

| Pattern | RTO | RPO | Cost | Complexity |
|---|---|---|---|---|
| Active-Active | Near zero | Near zero | High (2x resources) | High |
| Active-Passive (Hot) | Minutes | Minutes | Medium-High | Medium |
| Active-Passive (Cold) | Hours | Minutes-Hours | Medium | Medium |
| Pilot Light | Hours | Minutes | Low-Medium | Low-Medium |
| Backup & Restore | Hours-Days | Hours | Low | Low |

---

## Active-Active

Both regions serve live traffic simultaneously.

**Architecture:**
- Identical compute stacks in two+ regions
- Cosmos DB multi-region writes or Azure SQL active geo-replication
- Azure Front Door for global routing with health probes per region
- Shared-nothing design — each region is fully self-contained

**When to use:** Mission-critical — near-zero RTO/RPO. E-commerce, financial services, global SaaS.

**Gotchas:**
- Data conflicts with multi-region writes
- Session affinity breaks if a region fails
- Costs are ~2x
- Testing failover is complex

---

## Active-Passive (Hot Standby)

Primary serves all traffic. Secondary is deployed and running but idle.

**Architecture:**
- Full compute stack in secondary region, scaled down but running
- Azure SQL geo-replication (async) or Cosmos DB single-write with read replicas
- Front Door or Traffic Manager with failover routing
- DNS TTL set low (~60 seconds) for timely failover

**When to use:** Business-critical with minutes of acceptable downtime. Most production SaaS.

**Gotchas:**
- Secondary may need scale-up during failover
- Async replication means some data loss (RPO > 0)
- Test failover regularly

---

## Pilot Light

Minimal infrastructure in secondary — data replication and core services only.

**Architecture:**
- Database replication to secondary region (always running)
- IaC templates ready to deploy compute (Bicep/Terraform)
- DNS-based failover via Traffic Manager
- Compute provisioned on-demand during failover (10-60 min)

**When to use:** Cost-sensitive with RTO tolerance of 1-4 hours. Internal apps, batch systems.

**Gotchas:**
- Provisioning during an incident adds stress
- Region capacity may be constrained during widespread outages
- Pre-reserve capacity with on-demand capacity reservations if RTO is critical

---

## Backup & Restore

No secondary infrastructure. Recovery relies on restoring from backups.

**When to use:** Dev/test, non-critical tools, RTO tolerance of 8+ hours.

**Implementation:**
- Azure Backup with cross-region restore
- Geo-redundant storage (GRS) for blobs
- Point-in-time restore for databases
- IaC to rebuild infrastructure in target region

---

## Data Replication Options

| Service | Replication Method | RPO |
|---|---|---|
| Azure SQL Database | Active geo-replication (async) | Seconds |
| Azure SQL Database | Failover groups (auto failover) | Seconds |
| Cosmos DB | Multi-region writes | Near zero |
| Cosmos DB | Single-write with read replicas | Seconds |
| Azure Storage | GRS / GZRS (async) | ~15 minutes |
| Azure Storage | Cross-region replication (object) | Minutes |
| Azure Cache for Redis | Geo-replication | Seconds |
| PostgreSQL Flexible | Read replicas (cross-region) | Seconds |

---

## Global Load Balancing

| Service | Best For |
|---|---|
| **Azure Front Door** | HTTP(S) workloads, CDN, WAF, path-based routing |
| **Traffic Manager** | DNS-based routing, non-HTTP protocols |

- Configure health probes for each backend region
- Set appropriate probe intervals and failure thresholds
- Use priority routing for active-passive, weighted for active-active

---

## Implementation Checklist

| Step | Action |
|---|---|
| 1 | Define RTO and RPO for each workload tier |
| 2 | Select DR pattern based on RTO/RPO/budget |
| 3 | Choose paired or non-paired secondary region |
| 4 | Implement data replication (SQL geo-rep, Cosmos multi-region, GRS) |
| 5 | Configure global load balancer (Front Door or Traffic Manager) |
| 6 | Automate failover with IaC — no manual portal steps |
| 7 | Test failover quarterly — untested DR is not DR |
| 8 | Document runbooks for failover and failback procedures |
| 9 | Set up alerts for replication lag and region health |

---

## Failover Testing Cadence

| Frequency | Test Type |
|---|---|
| Monthly | Verify replication lag metrics are within RPO |
| Quarterly | Full failover drill to secondary region |
| Quarterly | Failback drill from secondary to primary |
| Annually | Chaos engineering — simulate region outage |

**After every test:** Update runbooks with lessons learned. Fix any issues before the next test.

## Related Skills

- `observability-baseline` — Monitoring and alerting for replication lag
- `documentation-standards` — Runbook templates for failover procedures
