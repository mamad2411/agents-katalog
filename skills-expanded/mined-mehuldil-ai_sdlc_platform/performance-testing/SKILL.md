# /project:performance-testing

**Interactive Performance Testing & NFR Validation**

Works in: Cursor IDE chat + Claude Code + CLI

## Usage

```
/project:performance-testing AB#123
/project:performance-testing AB#123 --nfr=latency,throughput,memory
/project:performance-testing AB#123 --run-load-test
```

## What This Does

1. **Loads story NFRs** (latency, throughput, availability targets)
2. **Designs perf test** (load profile, scenarios, monitoring)
3. **Runs load tests** (using k6, JMeter, or similar)
4. **Analyzes results** (P50, P95, P99 latency, error rate)
5. **Compares vs targets** (pass/fail on NFRs)
6. **Creates performance report** with recommendations

## Interactive Flow

```
User: /project:performance-testing AB#123

Claude: ⚡ Performance Testing

✅ STORY LOADED:
  Story: Phone verification & OTP (AB#123)
  NFRs:
    • P95 Latency: <200ms
    • Availability: 99.9%
    • Throughput: >1000 RPS
    • Error rate: <0.1%

🎯 LOAD TEST DESIGN:

Scenarios:
  [1] Baseline (50 concurrent users)
  [2] Standard Load (500 concurrent)
  [3] Peak Load (1000 concurrent)
  [4] Stress Test (2000 concurrent)
  [5] All of above

User: [5]

Designing load test profile...

TEST PROFILE:
  Phase 1: Ramp-up (50→1000 users over 5 min)
  Phase 2: Steady state (1000 users for 10 min)
  Phase 3: Stress (1000→2000 over 5 min, identify breaking point)

ENDPOINTS TESTED:
  • POST /api/v1/signup/initiate (40% of traffic)
  • POST /api/v1/signup/verify-otp (40% of traffic)
  • GET /api/v1/languages (20% of traffic)

MONITORING:
  • Metrics: Latency (p50, p95, p99), throughput, error rate
  • Logs: CloudWatch + ELK
  • Alerts: Trigger if P95 >200ms

RUN LOAD TEST NOW?
  [1] Yes, start test (estimated 20 min)
  [2] Preview test config first
  [3] Schedule for later
  [4] Cancel

User: [1]

Running load test on staging environment...
[████████████████░░░░░░░░░░░░] 50%

[Simulating 1000 concurrent users...]

✅ LOAD TEST RESULTS:

Phase 1 (Ramp-up):
  • Max latency: 450ms (acceptable)
  • P95: 145ms ✓
  • Throughput: 950 RPS (starting)
  • Errors: 0 (0%)

Phase 2 (Steady state):
  • P50: 65ms ✓
  • P95: 178ms ✓
  • P99: 280ms ⚠️ (above target)
  • Throughput: 1050 RPS ✓
  • Errors: 0.05% ✓

Phase 3 (Stress - 2000 users):
  • P95: 312ms ✗ (exceeds 200ms target)
  • Throughput: 1890 RPS (plateaus at 1950)
  • Errors: 2.1% ✗ (exceeds 0.1% target)
  • Breaking point: ~1900 RPS

📊 ANALYSIS:

✓ PASS: P95 <200ms at 1000 RPS (production target)
⚠️ CAUTION: P99 slightly elevated (280ms vs 200ms target)
✗ FAIL: Stress test shows degradation >1900 RPS

BOTTLENECK IDENTIFIED:
  • Database connection pool (max 100 connections)
  • Twilio API rate limiting (1000 calls/sec)
  • Recommendation: Increase pool to 150, add queue

RECOMMENDATION:
  [1] Optimize connection pool before deploy
  [2] Proceed to production (meets 1000 RPS target)
  [3] Conduct stress test on database separately
  [4] Adjust NFR targets downward

User: [1]

Add your notes for this optimization (type in chat):

User: "Pool size increase — DBA to approve, target before next load test."

✓ Posted optimization recommendation + user notes as comment on AB#123
  Detail: Increase database connection pool size
  Impact: Expected P99 reduction to <200ms
  
GENERATE PERFORMANCE REPORT?
  [1] Yes, create detailed report
  [2] Just save results locally
  [3] Cancel

User: [1]

✓ Generated performance report (PDF + HTML)
✓ Saved results to .sdlc/memory/performance-testing-AB#123.json
✓ Posted report link to ADO story

PERFORMANCE TESTING COMPLETE
```

## CLI Mode

```bash
$ sdlc skill performance-testing AB#123 --nfr=latency,throughput
$ sdlc skill performance-testing AB#123 --run-load-test --duration=20min
$ sdlc skill performance-testing --sprint=12 --batch
```

## Outputs

- **Load Test Results**: P50, P95, P99 latency data
- **Performance Report**: PDF with analysis + recommendations
- **Optimization Comments**: Posted as ADO comments on work item (user provides notes in chat)
- **Monitoring Setup**: Configured for production

## G9 Gate Clear Conditions

Gate G9 is CLEAR when:
- All NFRs validated via load test
- P95 latency passes target at >1000 RPS
- Error rate <0.1% under sustained load
- No critical bottlenecks identified
- Performance baseline established for comparison

## Next Commands

- `/project:staging-validation AB#123` - SIT/UAT testing
- `/project:release-prep AB#123` - Release readiness check
- `/project:deployment AB#123` - Production deployment

---

## Model & Token Budget
- **Model Tier:** Sonnet (test analysis + recommendations)
- Input: ~1K tokens (story + NFRs)
- Output: ~2K tokens (test plan + results analysis)

