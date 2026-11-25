---
name: load-testing
description: >
  Plan load testing — workload modeling, user journey scripts, ramp-up profiles,
  SLA thresholds, bottleneck identification, and capacity recommendations.
  TRIGGER when: user says /load-testing, needs to plan performance testing,
  or asks about stress testing and capacity validation.
argument-hint: "[system or endpoint to load test]"
user-invocable: true
---
# Load Testing Plan
## Process
### Step 1: Define Test Objectives
| Test Type | Purpose | When to Use |
|-----------|---------|------------|
| Load test | Validate under expected load | Pre-release |
| Stress test | Find breaking point | Capacity planning |
| Soak test | Find memory leaks, degradation | Pre-release |
| Spike test | Handle sudden traffic surges | Event planning |
### Step 2: Model Workload
| Scenario | Requests/sec | User Pattern | % of Traffic |
|----------|-------------|-------------|-------------|
| Browse catalog | X rps | Read-heavy | X% |
| Search | X rps | CPU-intensive | X% |
| Checkout | X rps | Write + external calls | X% |
| API integration | X rps | Burst pattern | X% |
### Step 3: Design Ramp-Up Profile
| Phase | Duration | Load | Purpose |
|-------|----------|------|---------|
| Warmup | 5 min | 10% target | Cache warmup |
| Ramp | 10 min | 10% → 100% | Gradual increase |
| Steady state | 30 min | 100% target | Sustained load |
| Peak | 10 min | 150% target | Headroom validation |
| Cool down | 5 min | Decrease to 0 | Graceful degradation |
### Step 4: Set SLA Thresholds
| Metric | Target | Failure Threshold |
|--------|--------|------------------|
| p50 latency | < 200ms | > 500ms |
| p95 latency | < 500ms | > 2000ms |
| p99 latency | < 1000ms | > 5000ms |
| Error rate | < 0.1% | > 1% |
| Throughput | X rps | < 80% target |
### Step 5: Execute and Monitor
| Monitor | What to Watch |
|---------|-------------|
| Application | Latency, error rate, throughput |
| Infrastructure | CPU, memory, disk I/O, network |
| Database | Query time, connections, locks |
| External deps | API latency, timeout rate |
### Step 6: Analyze and Recommend
| Bottleneck | Evidence | Recommendation |
|-----------|----------|---------------|
| [component] | [metric at failure] | [scaling/optimization] |
## Output Format
```markdown
## Load Test Report: [System]
### Test Config: [Type, duration, peak load]
### Results Summary
| Metric | Target | Actual | Status |
|--------|--------|--------|--------|
### Bottlenecks: [Identified with evidence]
### Capacity: [Max sustainable load]
### Recommendations: [Scaling/optimization actions]
```
## Quality Checklist
- [ ] Workload model reflects production patterns
- [ ] Test environment matches production (or scaled proportionally)
- [ ] SLA thresholds defined before testing
- [ ] All system layers monitored during test
- [ ] Results analyzed for bottlenecks
- [ ] Recommendations are specific and actionable
## Edge Cases
- For serverless, test cold start impact under load
- For distributed systems, test cross-region latency
- If test env differs from prod, document scaling assumptions
