---
name: performance-tester
description: "Design and run performance tests to identify bottlenecks, validate SLOs, and measure system capacity. Covers load tests, stress tests, and spike tests."
category: testing
tags: [performance, load-testing, k6, jmeter, benchmarking]
complexity: advanced
risk: low
compatibility: [claude-code, antigravity, gemini-cli, cursor, copilot, codex-cli, autohand, kiro]
source: antigravity-official
version: "1.0.0"
date_added: "2026-07-10"
last_updated: "2026-07-10"
---

# Performance Tester

## Purpose
Identify performance bottlenecks and validate that systems meet SLOs under realistic and extreme load conditions.

## Performance Test Types
| Type | Goal | When |
|---|---|---|
| Load test | Validate normal traffic | Before release |
| Stress test | Find breaking point | Capacity planning |
| Spike test | Handle sudden traffic | Event preparation |
| Soak test | Find memory leaks | Long-running validation |
| Smoke test | Basic sanity check | After deploy |

## k6 Test Scripts
```javascript
import http from 'k6/http';
import { check, sleep } from 'k6';
import { Rate, Trend } from 'k6/metrics';

const errorRate = new Rate('errors');
const apiDuration = new Trend('api_duration');

export const options = {
  scenarios: {
    // Ramping load test
    load_test: {
      executor: 'ramping-vus',
      startVUs: 0,
      stages: [
        { duration: '2m', target: 100 },   // Ramp up
        { duration: '5m', target: 100 },   // Sustain
        { duration: '2m', target: 200 },   // Increase
        { duration: '5m', target: 200 },   // Sustain
        { duration: '2m', target: 0 },     // Ramp down
      ],
    },
  },
  thresholds: {
    http_req_duration: ['p(95)<500', 'p(99)<1000'],  // SLO: P95 < 500ms
    errors: ['rate<0.01'],                             // Error rate < 1%
    http_req_failed: ['rate<0.01'],
  },
};

export default function() {
  const res = http.get('https://api.example.com/posts', {
    headers: { Authorization: `Bearer ${__ENV.API_TOKEN}` },
  });

  const success = check(res, {
    'status is 200': (r) => r.status === 200,
    'response time < 500ms': (r) => r.timings.duration < 500,
    'has data': (r) => r.json().data !== undefined,
  });

  errorRate.add(!success);
  apiDuration.add(res.timings.duration);

  sleep(1);
}
```

## Identifying Bottlenecks
```bash
# Profile running Node.js app
node --prof app.js

# Analyze flame graph
npx clinic flame -- node server.js

# Database slow query log
SET GLOBAL slow_query_log = 1;
SET GLOBAL long_query_time = 0.1;

# Profile PostgreSQL queries
EXPLAIN (ANALYZE, BUFFERS, FORMAT JSON) SELECT ...;
```

## Outputs
1. k6 test scripts for all scenarios
2. SLO definition (P95, P99 targets)
3. Performance baseline report
4. Bottleneck analysis
5. Optimization recommendations
6. Continuous performance monitoring setup
