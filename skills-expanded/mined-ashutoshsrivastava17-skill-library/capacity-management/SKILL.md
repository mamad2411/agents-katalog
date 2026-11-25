---
name: capacity-management
description: >
  Plan IT capacity with demand forecasting, resource utilization analysis, scaling triggers,
  performance baselines, and capacity reports for proactive infrastructure management.
  TRIGGER when: user says /capacity-management, "capacity planning", "capacity management", "resource utilization",
  "demand forecasting", "scaling plan", "infrastructure capacity", or "will we run out of capacity".
argument-hint: "[system_name or resource_type]"
user-invocable: true
---

# IT Capacity Management

You are an expert IT capacity management practitioner. When the user asks you to plan or manage IT capacity, follow this structured process to ensure infrastructure meets current and future demand while optimizing cost and performance.

## Step 1: Current Capacity Assessment

Establish a baseline of current resource utilization:

| Resource Type | Metrics to Collect | Source | Collection Method |
|---------------|-------------------|--------|-------------------|
| Compute (CPU) | Utilization %, core count, clock speed | Servers, VMs, containers | Monitoring agent (Prometheus, Datadog, CloudWatch) |
| Memory (RAM) | Utilization %, allocated vs used, swap usage | Servers, VMs, containers | Monitoring agent |
| Storage | Used capacity, IOPS, throughput, latency | SAN, NAS, cloud storage, local disk | Storage management tool, cloud metrics |
| Network | Bandwidth utilization, packet loss, latency | Switches, routers, load balancers | SNMP, NetFlow, cloud VPC metrics |
| Database | Connection count, query throughput, buffer pool hit ratio | Database servers | Database monitoring (pganalyze, RDS metrics) |
| Application | Request rate, response time, error rate, queue depth | Application servers | APM tool (New Relic, Datadog APM) |
| Cloud resources | Instance count, reserved vs on-demand, spot utilization | Cloud provider | Cloud cost management tool (CloudHealth, Spot.io) |

### Utilization Summary Template

| Resource | Current Capacity | Peak Utilization | Average Utilization | Available Headroom | Status |
|----------|-----------------|-----------------|--------------------|--------------------|--------|
| CPU — Prod cluster | 128 cores | 82% | 55% | 18% at peak | Warning |
| RAM — Prod cluster | 512 GB | 71% | 48% | 29% at peak | OK |
| Storage — Primary DB | 2 TB | 78% | 78% (growing) | 22% | Warning |
| Network — WAN link | 1 Gbps | 45% | 22% | 55% at peak | OK |
| DB connections | 200 max | 168 (84%) | 92 (46%) | 16% at peak | Warning |

### Health Status Thresholds

| Status | Utilization Range | Action |
|--------|------------------|--------|
| OK (Green) | 0-60% | Monitor normally |
| Warning (Yellow) | 60-80% | Plan capacity increase, monitor closely |
| Critical (Red) | 80-90% | Immediate scaling needed, alert stakeholders |
| Emergency (Black) | 90-100% | Service impact imminent or occurring, emergency action |

## Step 2: Demand Forecasting

Project future capacity requirements:

### Forecasting Methods

| Method | Data Required | Best For | Accuracy |
|--------|-------------|----------|----------|
| Linear trend | 6-12 months historical utilization | Steady, predictable growth | Medium |
| Seasonal decomposition | 12-24 months historical with seasonal patterns | Business with cyclical demand | High |
| Business driver correlation | Utilization + business metric (users, revenue, transactions) | Growth tied to business KPIs | High |
| Capacity modeling | Application architecture, resource-per-unit ratios | New systems, major changes | Medium |
| Scenario planning | Business plans, product roadmap | Strategic planning, uncertainty | Variable |

### Demand Forecast Template

| Resource | Current | 3-Month Forecast | 6-Month Forecast | 12-Month Forecast | Confidence |
|----------|---------|-----------------|-----------------|-------------------|------------|
| CPU cores | 128 | 140 (+9%) | 155 (+21%) | 180 (+41%) | High |
| RAM (GB) | 512 | 550 (+7%) | 600 (+17%) | 700 (+37%) | High |
| Storage (TB) | 2.0 | 2.3 (+15%) | 2.7 (+35%) | 3.5 (+75%) | Medium |
| DB connections | 200 | 220 (+10%) | 250 (+25%) | 300 (+50%) | Medium |

### Growth Driver Analysis

| Business Driver | Current Value | Growth Rate | Capacity Impact |
|-----------------|--------------|-------------|-----------------|
| Registered users | 500,000 | +8% monthly | +2 cores, +8 GB RAM per 50K users |
| Daily transactions | 1.2M | +5% monthly | +50 IOPS per 100K transactions |
| Data ingestion | 50 GB/day | +10% monthly | +1.5 TB storage per quarter |
| API calls | 10M/day | +15% monthly | +4 cores per 5M daily calls |
| Concurrent users | 25,000 peak | +6% monthly | +500 DB connections per 10K concurrent |

## Step 3: Performance Baselines

Establish and monitor performance baselines:

### Baseline Metrics

| Metric | Baseline Value | Acceptable Range | Alert Threshold | Measurement Period |
|--------|---------------|-----------------|-----------------|-------------------|
| API response time (p50) | 120 ms | 80-160 ms | > 200 ms | Last 30 days |
| API response time (p99) | 450 ms | 300-600 ms | > 800 ms | Last 30 days |
| Database query time (avg) | 25 ms | 15-40 ms | > 60 ms | Last 30 days |
| Page load time | 2.1 s | 1.5-3.0 s | > 4.0 s | Last 30 days |
| Error rate | 0.1% | 0-0.3% | > 0.5% | Last 7 days |
| Throughput (requests/sec) | 1,200 | 800-2,000 | < 600 or > 2,500 | Last 7 days |

### Baseline Deviation Detection

| Deviation Type | Detection Method | Response |
|----------------|-----------------|----------|
| Gradual degradation | Week-over-week trend analysis | Investigate root cause, plan capacity |
| Sudden spike | Real-time alerting on threshold breach | Incident response, auto-scaling |
| Periodic pattern | Seasonal decomposition, day-of-week analysis | Adjust baselines, pre-scale for known peaks |
| Post-change regression | Before/after comparison around change windows | Rollback or optimize, update baseline |

## Step 4: Scaling Triggers and Strategies

Define when and how to scale:

### Scaling Trigger Matrix

| Resource | Scale-Up Trigger | Scale-Down Trigger | Method | Lead Time |
|----------|-----------------|-------------------|--------|-----------|
| CPU | Sustained > 75% for 15 min | Sustained < 30% for 1 hour | Horizontal (add instances) | 5 min (cloud) |
| Memory | Sustained > 80% for 10 min | Sustained < 40% for 1 hour | Vertical (upgrade instance) | 15 min (cloud) |
| Storage | > 75% capacity | N/A (rarely shrink) | Add volume, expand disk | 30 min (cloud) |
| Database | Connections > 80% max | Connections < 30% max | Read replicas, connection pooling | 1-4 hours |
| Network | Bandwidth > 70% for 5 min | Bandwidth < 20% for 1 hour | Upgrade link, add CDN | Hours-days |

### Scaling Strategies

| Strategy | Description | Best For | Considerations |
|----------|-------------|----------|----------------|
| Vertical scaling (scale up) | Increase resource on existing instance | Databases, monoliths | Downtime during resize, upper limits |
| Horizontal scaling (scale out) | Add more instances behind load balancer | Stateless services, web tier | Requires load balancing, session management |
| Auto-scaling | Automated horizontal scaling based on metrics | Cloud-native, variable load | Set min/max limits, avoid thrashing |
| Pre-scaling | Proactively scale before known demand spikes | Events, sales, seasonal peaks | Requires advance knowledge of demand |
| Caching | Reduce load on origin systems | Read-heavy workloads | Cache invalidation complexity |
| Queue-based buffering | Absorb burst traffic, process asynchronously | Write-heavy, batch processing | Adds latency, queue monitoring needed |

### Auto-Scaling Configuration Template

```
Resource: [target group / service]
Metric: [CPU utilization / request count / custom metric]
Scale-out: When [metric] > [threshold] for [duration], add [count] instances
Scale-in: When [metric] < [threshold] for [duration], remove [count] instances
Minimum instances: [floor]
Maximum instances: [ceiling]
Cooldown period: [seconds between scaling actions]
Health check: [endpoint and expected response]
```

## Step 5: Capacity Reports

Produce regular capacity reports for stakeholders:

### Monthly Capacity Report Template

| Section | Content |
|---------|---------|
| Executive summary | Key findings, risk areas, recommended actions |
| Resource utilization summary | Table of all resources with current/peak/average utilization |
| Trend analysis | Utilization trends with forecast overlay |
| Capacity risks | Resources approaching thresholds with timeline to breach |
| Cost analysis | Current spend, projected spend, optimization opportunities |
| Scaling events | Auto-scale and manual scale events in the period |
| Performance baseline status | Any baseline deviations and their causes |
| Recommendations | Prioritized list of capacity actions |

### Capacity Risk Register

| Risk ID | Resource | Current Util. | Projected Breach | Business Impact | Mitigation | Owner | Cost |
|---------|----------|--------------|-----------------|-----------------|-----------|-------|------|
| CR-001 | Primary DB storage | 78% | 6 weeks | Service outage if full | Expand to 4 TB, archive old data | DBA Team | $500/month |
| CR-002 | Prod CPU cluster | 82% peak | 4 weeks | Degraded response times | Add 4 nodes to cluster | Platform Team | $2,400/month |
| CR-003 | WAN bandwidth | 45% peak | 6 months | Slow remote access | Upgrade link to 2 Gbps | Network Team | $1,200/month |

## Step 6: Optimization and Cost Management

Balance capacity with cost efficiency:

### Optimization Opportunities

| Opportunity | Detection Method | Potential Savings |
|-------------|-----------------|-------------------|
| Right-sizing over-provisioned instances | Instance utilization < 30% consistently | 30-60% per instance |
| Reserved instance purchasing | Stable workloads running 24/7 | 30-70% vs on-demand |
| Spot/preemptible instances | Fault-tolerant, interruptible workloads | 60-90% vs on-demand |
| Storage tiering | Infrequently accessed data on cold storage | 50-80% on storage costs |
| Decommission unused resources | Resources with zero utilization for 30+ days | 100% of unused resource cost |
| Scheduling non-production | Dev/test environments off during non-business hours | 40-60% of non-prod costs |
| Application optimization | Code profiling reveals inefficient resource use | Variable — often 20-50% |

### Cost-Capacity Trade-off Analysis

| Option | Capacity Provided | Monthly Cost | Cost per Unit | Lead Time | Flexibility |
|--------|------------------|-------------|---------------|-----------|-------------|
| On-demand cloud | Variable | $$$ | High | Minutes | Maximum |
| Reserved instances | Fixed | $$ | Medium | Committed | Low |
| Spot instances | Variable | $ | Low | Minutes | High risk |
| On-premises | Fixed | $$ (amortized) | Low (at scale) | Weeks-months | Minimal |
| Hybrid | Mixed | $$ | Medium | Variable | Moderate |

## Output Format

Present the capacity management deliverable as:

1. **Capacity Summary** (current state, key risks, headline recommendations)
2. **Resource Utilization Report** (all resources with current/peak/average and status)
3. **Demand Forecast** (3/6/12-month projections with confidence levels)
4. **Performance Baselines** (metrics, acceptable ranges, current deviations)
5. **Scaling Plan** (triggers, strategies, auto-scaling configurations)
6. **Capacity Risk Register** (risks ranked by urgency with mitigations)
7. **Cost Optimization Analysis** (opportunities, savings estimates, trade-offs)
8. **Capacity Roadmap** (quarterly plan for capacity investments and optimizations)

## Quality Checklist

Before delivering the capacity plan, verify:

- [ ] All critical resources are inventoried with current utilization
- [ ] Performance baselines are established with at least 30 days of data
- [ ] Demand forecasts use appropriate methods with stated confidence levels
- [ ] Scaling triggers are defined with specific thresholds and response actions
- [ ] Cost implications are quantified for all capacity recommendations
- [ ] Capacity risks have owners, timelines, and mitigation plans
- [ ] Report cadence and distribution are defined
- [ ] Optimization opportunities are identified and prioritized
- [ ] Plan accounts for known business events (launches, campaigns, seasonal peaks)

## Edge Cases

- **Sudden viral growth**: Pre-define an emergency scaling runbook with pre-approved budget; use auto-scaling with generous maximums; have a CDN and queue-based buffering ready
- **Multi-cloud environments**: Normalize metrics across providers; use a unified monitoring platform; consider cross-cloud burst capacity
- **Legacy on-premises systems**: Plan longer lead times for hardware procurement (8-16 weeks); maintain a buffer of spare capacity; evaluate cloud migration for elastic workloads
- **Shared infrastructure (multi-tenant)**: Implement resource quotas per tenant; monitor noisy-neighbor effects; plan capacity based on aggregate demand, not individual tenants
- **Seasonal businesses (e.g., retail)**: Forecast based on prior year peaks with growth factor; pre-scale 2 weeks before peak; use reserved capacity for baseline + on-demand for burst
- **Data growth outpacing compute growth**: Implement data lifecycle policies (archive, purge, compress); evaluate storage tiering; consider data warehouse vs operational database separation
