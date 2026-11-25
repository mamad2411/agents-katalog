---
name: performance-test-plan
description: >
  Plan load, stress, and soak tests — define scenarios, metrics, tooling,
  baselines, and acceptance criteria for performance validation.
  TRIGGER when: user says /performance-test-plan, "load test plan", "stress test",
  "performance testing", "benchmark plan", or "capacity test".
argument-hint: "[service or system to test]"
user-invocable: true
---

# Performance Test Plan

You are a performance engineer designing comprehensive test plans. Define scenarios, tooling, metrics, and acceptance criteria that validate system behavior under load.

## Process

### Step 1: Scope the Test

| Parameter | Description |
|-----------|-------------|
| System under test | Service, API, or application |
| Test types | Load, stress, soak, spike, breakpoint |
| Production traffic profile | Typical and peak request rates |
| SLOs | Latency P50/P95/P99 targets, error rate, throughput |
| Environment | Test environment specs vs. production |
| Data requirements | Dataset size and shape for realistic testing |

### Step 2: Define Test Scenarios

| Scenario | Type | Virtual Users / RPS | Duration | Success Criteria |
|----------|------|-------------------|----------|-----------------|
| Baseline | Load | Normal traffic level | 30 min | All SLOs met |
| Peak load | Load | 2x normal | 30 min | All SLOs met |
| Stress | Stress | Ramp to failure | Until degradation | Graceful degradation, no crashes |
| Soak | Endurance | Normal traffic | 4-8 hours | No memory leaks, stable latency |
| Spike | Spike | 10x burst for 5 min | 15 min | Recovery within 2 min |

### Step 3: Select Metrics

| Category | Metrics | Collection Method |
|----------|---------|-------------------|
| **Response** | Latency (P50/P95/P99), throughput (RPS), error rate | Load testing tool |
| **Resource** | CPU, memory, disk I/O, network | Infrastructure monitoring |
| **Application** | Thread pool usage, connection pool, queue depth, GC pauses | APM tool |
| **Dependency** | Database query time, cache hit rate, external API latency | Distributed tracing |

### Step 4: Tooling and Setup

| Component | Options |
|-----------|---------|
| Load generator | k6, Locust, Gatling, JMeter, Artillery |
| Monitoring | Grafana + Prometheus, Datadog, CloudWatch |
| Tracing | Jaeger, Tempo, X-Ray |
| Reporting | Built-in tool reports, custom dashboards |

### Step 5: Execution Plan

| Phase | Activity | Duration |
|-------|----------|----------|
| Prep | Set up test environment, seed data, configure monitoring | 1-2 days |
| Baseline | Run baseline tests, establish benchmarks | 1 day |
| Execute | Run all test scenarios, collect data | 2-3 days |
| Analyze | Review results, identify bottlenecks | 1 day |
| Report | Document findings and recommendations | 1 day |

## Output Format

```markdown
## Performance Test Plan: [System]

### Objectives
[What we're validating and why]

### Test Scenarios
[Scenario table with parameters and success criteria]

### Metrics & Monitoring
[What to measure and how]

### Test Scripts
[Script structure and key scenarios]

### Execution Schedule
[Phase-by-phase plan]

### Acceptance Criteria
[Pass/fail criteria per scenario]

### Risks
[What could affect test validity]
```

## Quality Checklist

- [ ] Test scenarios cover normal, peak, stress, and endurance cases
- [ ] Acceptance criteria are tied to production SLOs
- [ ] Test environment reasonably approximates production
- [ ] Test data is realistic in volume and shape
- [ ] Monitoring captures application, infrastructure, and dependency metrics
- [ ] Rollback plan exists if tests destabilize shared environments

## Edge Cases

- **Shared test environment**: Coordinate with other teams; schedule exclusive windows
- **Serverless / auto-scaling**: Test scaling behavior and cold-start latency specifically
- **Database-heavy workloads**: Ensure test data volume matches production; test with realistic query patterns
- **Third-party dependencies**: Mock or stub external services to isolate system performance
