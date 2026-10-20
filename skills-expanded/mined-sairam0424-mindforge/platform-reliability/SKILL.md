---
name: platform-reliability
version: 1.0.0
min_mindforge_version: 10.7.0
status: stable
triggers: platform reliability engineering, SLO management platform, error budget policy, platform availability design, capacity management platform, platform SLA, reliability target, platform health metric, platform uptime, error budget spending, toil reduction platform, platform incident prevention
compose: incident-management
---

# Skill — Platform Reliability

## When this skill activates

This skill activates when the user is designing or implementing platform reliability capabilities. This includes SLO management systems, error budget policies, platform availability design, capacity management, platform health metrics, reliability targets, uptime monitoring, error budget tracking, toil reduction initiatives, and platform incident prevention strategies.

## Mandatory actions when this skill is active

### Before writing any code

1. Inventory all platform services and their current reliability posture (uptime, error rates, latency, throughput).
2. Define SLOs for each platform capability (e.g., 99.9% for APIs, 99.5% for batch jobs, 99.99% for critical path services).
3. Establish error budget policy: what happens when budget is exhausted (freeze launches, prioritize reliability work).
4. Identify toil sources (manual escalations, runbook execution, repetitive debugging) and quantify hours spent per week.
5. Map platform dependencies and identify single points of failure that require redundancy.

### During implementation

- **SLO Management:** Define SLOs as percentiles over rolling windows (e.g., 99th percentile latency < 200ms over 28 days). Avoid averages (they hide outliers). Each SLO should have: objective, measurement window, error budget calculation, and owner.
- **Error Budget Policy:** If error budget is exhausted, automatically freeze non-critical deployments and redirect engineering time to reliability improvements. Budget resets monthly or quarterly. Include exemptions for security patches.
- **Platform Availability Design:** Use multi-region active-active for critical path services. Implement circuit breakers, rate limiting, and graceful degradation. Platform should survive single availability zone failure with zero downtime.
- **Capacity Management:** Track resource utilization (CPU, memory, disk, network) and predict exhaustion 30-90 days in advance. Automate horizontal scaling for stateless services. Capacity alerts should fire before user-visible impact.
- **Platform Health Metrics:** Track: request rate, error rate, latency (p50, p95, p99), saturation, and throughput. Use RED (Rate, Errors, Duration) for services and USE (Utilization, Saturation, Errors) for infrastructure. Dashboards should load in under 3 seconds.
- **Toil Reduction:** Automate repetitive tasks that consume more than 2 hours per week. Toil reduction should free up 30-50% of on-call time within 6 months. Track toil hours saved as a platform metric.
- **Incident Prevention:** Use chaos engineering to validate failure modes (kill instances, partition networks, inject latency). Run game days quarterly. Each incident should produce at least one actionable prevention task.

### After implementation

- Verify each platform service has defined SLOs, error budgets, and dashboards tracking compliance.
- Confirm error budget policy is enforced automatically (deployment freezes when budget exhausted).
- Validate multi-region failover works via chaos engineering tests (kill a region, verify zero downtime).
- Ensure capacity management predicts exhaustion 30-90 days in advance with alerts.
- Check that toil reduction initiatives have freed up measurable on-call time (tracked weekly).

## Self-check before task completion

- [ ] Each platform service has SLOs defined as percentiles over rolling windows.
- [ ] Error budget policy automatically freezes non-critical deployments when budget exhausted.
- [ ] Platform survives single availability zone failure with zero user-visible downtime.
- [ ] Capacity management predicts resource exhaustion 30-90 days in advance.
- [ ] Platform health metrics use RED for services and USE for infrastructure.
- [ ] Toil reduction initiatives free up 30-50% of on-call time within 6 months.
- [ ] Chaos engineering validates failure modes quarterly via game days.
