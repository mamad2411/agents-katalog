---
name: high-availability
description: Design high-availability systems with redundancy, failover, and disaster recovery. Outputs architecture diagrams, SLA targets, and failure modes.
argument-hint: [SLA requirements, budget, geographic distribution]
allowed-tools: Read, Write, Bash
---

# High Availability Design

Design systems that stay operational during failures. Not single points of failure — redundancy, failover, health checks, and disaster recovery.

## Process

1. **Define SLA.** Uptime target (99.9%, 99.99%), acceptable downtime.
2. **Eliminate SPOFs.** Redundant servers, databases, load balancers.
3. **Add health checks.** Liveness probes, circuit breakers.
4. **Implement failover.** Automatic switchover to backup systems.
5. **Geographic distribution.** Multi-region for disaster recovery.
6. **Plan degradation.** Graceful failures, read-only mode.
7. **Test failure scenarios.** Chaos engineering, disaster drills.

## Output Format

### HA Architecture: [System Name]

**SLA:** 99.95% uptime (4.38 hours downtime/year)  
**Architecture:** Multi-AZ, active-active  
**Redundancy:** 3x app servers, 2x databases (primary/replica)  
**Failover:** Automatic (< 30 seconds)  
**DR:** Multi-region backup, 4-hour RPO

---

## Availability Calculations

### SLA Targets
```
90%     (1 nine)  → 36.5 days downtime/year
99%     (2 nines) → 3.65 days downtime/year
99.9%   (3 nines) → 8.76 hours downtime/year
99.99%  (4 nines) → 52.56 minutes downtime/year
99.999% (5 nines) → 5.26 minutes downtime/year
```

### Series Components
```
Component A: 99.9% available
Component B: 99.9% available
Component C: 99.9% available

System (A AND B AND C):
99.9% × 99.9% × 99.9% = 99.7% available
```

### Parallel Components
```
Component A: 90% available
Component B: 90% available (failover)

System (A OR B):
1 - (0.1 × 0.1) = 99% available
```

---

## Single Points of Failure (SPOF)

### ❌ Single Server
```
[Client] → [Single Server] → [Database]

Problem: Server fails → entire system down
```

### ✅ Load Balanced Servers
```
               ┌─[Server 1]─┐
[Client] → [LB]┼─[Server 2]─┼→ [Database]
               └─[Server 3]─┘

Solution: Any server fails, LB routes to others
```

### ❌ Single Database
```
[App Servers] → [Single Database]

Problem: DB fails → system down
```

### ✅ Primary-Replica Database
```
               ┌─[Primary DB] (write)
[App Servers]──┤
               └─[Replica DB] (read, failover)

Solution: Primary fails → promote replica
```

---

## Load Balancing

### Round Robin
```
Request 1 → Server A
Request 2 → Server B
Request 3 → Server C
Request 4 → Server A (repeat)

Simple, but ignores server load
```

### Least Connections
```
Server A: 10 connections
Server B: 5 connections  ← Route here
Server C: 8 connections

Better for long-running requests
```

### Weighted
```
Server A: weight=3 (3x capacity) → 60% traffic
Server B: weight=1 (1x capacity) → 20% traffic
Server C: weight=1 (1x capacity) → 20% traffic

Use for heterogeneous servers
```

---

## Health Checks

### Liveness Probe
```bash
# Kubernetes
livenessProbe:
  httpGet:
    path: /health
    port: 8080
  initialDelaySeconds: 10
  periodSeconds: 5
  timeoutSeconds: 3
  failureThreshold: 3

# If fails 3 times → restart container
```

### Readiness Probe
```bash
# Check if ready to serve traffic
readinessProbe:
  httpGet:
    path: /ready
    port: 8080
  initialDelaySeconds: 5
  periodSeconds: 3

# If fails → remove from load balancer
```

### Health Endpoint
```python
@app.route('/health')
def health():
    checks = {
        'database': check_db_connection(),
        'cache': check_redis_connection(),
        'disk': check_disk_space()
    }
    
    if all(checks.values()):
        return {'status': 'healthy'}, 200
    else:
        return {'status': 'unhealthy', 'checks': checks}, 503
```

---

## Database High Availability

### Primary-Replica Replication
```
[Primary DB] --async replication--> [Replica DB]

Writes: Primary only
Reads: Primary + Replica (load balance)

Failover:
1. Detect primary failure
2. Promote replica to primary
3. Point app to new primary
```

### Synchronous Replication
```
[Primary] --sync--> [Replica]

Write completes only after replica confirms
No data loss, but higher latency
```

### Multi-Master
```
[Master A] <--bidirectional--> [Master B]

Both accept writes
Conflict resolution needed
```

---

## Automatic Failover

### AWS RDS Multi-AZ
```
Primary DB (AZ-A) --sync--> Standby (AZ-B)

Failure detection: 60 seconds
Automatic failover: Yes
DNS update to standby
Application reconnects automatically
```

### PostgreSQL with Patroni
```python
# Patroni handles failover
- Detects primary failure (via Consul/etcd)
- Elects new primary from replicas
- Updates HAProxy to point to new primary
- Typically < 30 seconds
```

---

## Geographic Distribution

### Active-Passive (DR)
```
Primary Region (Active)
  ↓ async replication
Backup Region (Passive)

Normal: All traffic to primary
Disaster: Manual failover to backup
RPO: Minutes to hours (async lag)
RTO: Hours (manual process)
```

### Active-Active (Multi-Region)
```
Region A (Active) <--sync--> Region B (Active)

Traffic routed to nearest region
Both regions serve requests
If region fails, traffic reroutes
RPO: 0 (sync replication)
RTO: Seconds (automatic)
```

---

## Graceful Degradation

### Read-Only Mode
```python
if database.is_primary_down():
    # Serve from read replica
    # Disable writes
    return "Service in read-only mode", 503

# Allow critical reads
user = get_user_from_replica(user_id)
```

### Feature Toggles
```python
if external_api.is_down():
    # Disable non-critical features
    disable_feature('recommendations')
    disable_feature('analytics')
    
    # Keep core features working
    allow_feature('checkout')
    allow_feature('login')
```

---

## Disaster Recovery

### Backup Strategy
```
Full backup: Weekly (Sunday)
Incremental: Daily
Transaction logs: Every 5 minutes

Retention:
- Daily: 7 days
- Weekly: 4 weeks
- Monthly: 12 months
```

### Recovery Point Objective (RPO)
```
RPO = Maximum acceptable data loss

RPO 1 hour: Can lose up to 1 hour of data
RPO 0: No data loss (sync replication)
```

### Recovery Time Objective (RTO)
```
RTO = Maximum acceptable downtime

RTO 4 hours: System must recover within 4 hours
RTO 1 minute: Near-instant failover required
```

---

## Chaos Engineering

### Failure Scenarios to Test
```
1. Single server failure
2. Database primary failure
3. Availability zone failure
4. Region failure
5. Network partition
6. Slow external API
7. Disk full
8. Memory leak
```

### Chaos Monkey
```bash
# Randomly terminate instances
chaosmonkey.sh --target=production --probability=0.1

# Simulates real failures
# Forces systems to be resilient
```

---

## Monitoring & Alerting

### Key Metrics
```
Uptime: % of time system is operational
Error rate: % of requests failing
Latency: Response time (p50, p95, p99)
Saturation: Resource usage (CPU, memory, disk)
```

### Alerts
```yaml
# Critical: Page on-call
- alert: HighErrorRate
  expr: error_rate > 0.05
  for: 5m
  severity: critical

# Warning: Ticket
- alert: DiskSpaceLow
  expr: disk_free < 0.1
  for: 10m
  severity: warning
```

---

## Cost vs Availability

```
99.9% (3 nines):
- Single region
- Active-passive
- Manual failover
- Cost: $X/month

99.99% (4 nines):
- Multi-AZ
- Active-active
- Auto failover
- Cost: $2-3X/month

99.999% (5 nines):
- Multi-region
- Geo-distributed
- Zero-downtime deploys
- Cost: $10X/month
```

## Rules

- Define SLA before architecture — 99.9% vs 99.99% drastically different designs.
- Eliminate all single points of failure — every component needs redundancy.
- Automate failover, don't rely on manual — humans too slow for RTO < 1 hour.
- Health checks on all components — detect failures before users notice.
- Test failure scenarios regularly — chaos engineering, not just hope it works.
- Geographic distribution for DR — region failure should not mean total outage.
- Graceful degradation over hard failures — read-only mode better than down.
- Monitor uptime, not just metrics — track actual availability vs SLA.
- RPO and RTO drive backup strategy — how much data loss and downtime acceptable.
- Cost scales with nines — each additional nine roughly doubles cost.
