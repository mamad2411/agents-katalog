---
name: load-test
description: Design and execute load tests to validate system performance under expected and peak traffic. Outputs k6/JMeter scripts, performance baselines, SLO validation, and capacity planning reports.
argument-hint: [system under test, expected TPS, SLOs, test types needed]
allowed-tools: Read, Write, Bash
---

# Load Testing

Validate that your system meets performance SLOs before production traffic finds the limit. Load testing is not just about finding the breaking point — it's about confirming behavior at expected load, finding the degradation curve, and capacity planning.

## Process

1. **Define test objectives** — SLOs to validate, peak load assumptions, test types needed.
2. **Model production traffic** — endpoints hit, request mix, user think time.
3. **Set up test environment** — production-like sizing, isolated from real users.
4. **Baseline at low load** — 10% of expected peak, confirm system is healthy.
5. **Ramp to target load** — verify SLOs hold at 100% expected peak.
6. **Stress test** — find the breaking point (120%+ of peak).
7. **Soak test** — run at sustained load for 1-2 hours to find memory leaks.
8. **Analyze results** — P50/P95/P99 latency, error rates, resource utilization.
9. **Report findings** — pass/fail vs. SLOs, bottlenecks, recommendations.

## Output Format

### SLO Definition

| SLO | Target | Test Threshold |
|-----|--------|---------------|
| P50 latency (checkout) | < 200ms | < 180ms |
| P95 latency (checkout) | < 500ms | < 450ms |
| P99 latency (checkout) | < 2000ms | < 1800ms |
| P95 latency (search) | < 300ms | < 270ms |
| Error rate | < 0.1% | < 0.08% |
| Throughput | 500 RPS | 500+ RPS sustained |
| Availability | 99.9% | 99.9% |

### k6 Load Test Script

```javascript
// load-test.js — k6 script
import http from 'k6/http';
import { check, sleep, group } from 'k6';
import { Rate, Trend, Counter } from 'k6/metrics';
import { SharedArray } from 'k6/data';

// Custom metrics
const errorRate = new Rate('error_rate');
const checkoutDuration = new Trend('checkout_duration', true);
const searchDuration = new Trend('search_duration', true);
const ordersCreated = new Counter('orders_created');

// Test data (loaded once, shared across VUs)
const users = new SharedArray('users', function() {
  return JSON.parse(open('./test-data/users.json'));
});
const products = new SharedArray('products', function() {
  return JSON.parse(open('./test-data/products.json'));
});

// Test configuration
export const options = {
  scenarios: {
    // Scenario 1: Steady load — validate SLOs
    steady_load: {
      executor: 'constant-arrival-rate',
      rate: 500,         // 500 RPS
      timeUnit: '1s',
      duration: '5m',
      preAllocatedVUs: 100,
      maxVUs: 200,
      startTime: '2m',   // After ramp-up
    },
    
    // Scenario 2: Ramp-up test
    ramp_up: {
      executor: 'ramping-arrival-rate',
      startRate: 50,
      timeUnit: '1s',
      stages: [
        { duration: '2m', target: 100 },   // Warm up
        { duration: '3m', target: 500 },   // Ramp to target
        { duration: '2m', target: 500 },   // Sustain
        { duration: '1m', target: 0 },     // Cool down
      ],
      preAllocatedVUs: 50,
      maxVUs: 200,
    },
    
    // Scenario 3: Spike test
    spike: {
      executor: 'ramping-arrival-rate',
      startRate: 100,
      timeUnit: '1s',
      stages: [
        { duration: '1m', target: 100 },
        { duration: '30s', target: 1500 }, // Sudden 10x spike
        { duration: '2m', target: 1500 },
        { duration: '1m', target: 100 },   // Recovery
      ],
      preAllocatedVUs: 100,
      maxVUs: 500,
    },
  },
  
  // Thresholds — test fails if violated
  thresholds: {
    'http_req_duration{scenario:steady_load}': [
      'p(50)<200', 'p(95)<500', 'p(99)<2000'
    ],
    'checkout_duration': ['p(95)<500'],
    'search_duration': ['p(95)<300'],
    'error_rate': ['rate<0.001'],   // < 0.1%
    'http_req_failed': ['rate<0.001'],
  },
};

// Auth helper
function getAuthToken(user) {
  const res = http.post(`${__ENV.BASE_URL}/auth/token`, JSON.stringify({
    email: user.email,
    password: user.password,
  }), { headers: { 'Content-Type': 'application/json' } });
  
  if (res.status === 200) {
    return res.json('access_token');
  }
  return null;
}

// Setup: runs once before all VUs
export function setup() {
  // Warm up the service
  http.get(`${__ENV.BASE_URL}/health`);
  return { baseUrl: __ENV.BASE_URL || 'https://staging.api.example.com' };
}

// Main VU function
export default function(data) {
  const user = users[Math.floor(Math.random() * users.length)];
  const token = getAuthToken(user);
  
  if (!token) {
    errorRate.add(1);
    return;
  }
  
  const headers = {
    'Content-Type': 'application/json',
    'Authorization': `Bearer ${token}`,
  };
  
  // Simulate realistic user journey
  group('product_search', function() {
    const startTime = Date.now();
    const query = ['laptop', 'phone', 'headphones'][Math.floor(Math.random() * 3)];
    
    const res = http.get(
      `${data.baseUrl}/products?q=${query}&limit=20`,
      { headers, tags: { name: 'product_search' } }
    );
    
    searchDuration.add(Date.now() - startTime);
    
    const ok = check(res, {
      'search status 200': (r) => r.status === 200,
      'search has results': (r) => r.json('items') && r.json('items').length > 0,
    });
    errorRate.add(!ok);
  });
  
  sleep(Math.random() * 2 + 1);  // Think time: 1-3s
  
  group('add_to_cart', function() {
    const product = products[Math.floor(Math.random() * products.length)];
    
    const res = http.post(
      `${data.baseUrl}/cart/items`,
      JSON.stringify({ product_id: product.id, quantity: 1 }),
      { headers, tags: { name: 'add_to_cart' } }
    );
    
    check(res, {
      'add to cart 201': (r) => r.status === 201,
    });
    errorRate.add(res.status !== 201);
  });
  
  sleep(Math.random() * 3 + 2);  // Think time: 2-5s
  
  group('checkout', function() {
    const startTime = Date.now();
    
    const res = http.post(
      `${data.baseUrl}/orders`,
      JSON.stringify({
        payment_method_id: 'pm_test_1234',
        shipping_address_id: user.default_address_id,
      }),
      { headers, tags: { name: 'checkout' } }
    );
    
    checkoutDuration.add(Date.now() - startTime);
    
    const ok = check(res, {
      'checkout 201': (r) => r.status === 201,
      'checkout has order id': (r) => r.json('order_id') !== undefined,
    });
    
    if (ok) ordersCreated.add(1);
    errorRate.add(!ok);
  });
  
  sleep(Math.random() * 2);
}

// Teardown: runs once after all VUs finish
export function teardown(data) {
  console.log(`Test completed. Base URL: ${data.baseUrl}`);
}
```

### Running Tests

```bash
# Install k6
brew install k6
# or: docker pull grafana/k6

# Generate test data
python scripts/generate_test_data.py --users 1000 --products 500 -o test-data/

# Run against staging
BASE_URL=https://staging.api.example.com \
k6 run \
  --out json=results.json \
  --out influxdb=http://localhost:8086/k6 \
  load-test.js

# Specific scenario only
k6 run --scenario=spike load-test.js

# With dashboard (real-time)
k6 run --out=dashboard load-test.js

# Distributed load (multiple machines)
K6_CLOUD_TOKEN=xxx k6 cloud load-test.js
```

### JMeter Alternative (for Java/enterprise environments)

```xml
<!-- test-plan.jmx excerpt -->
<ThreadGroup guiclass="ThreadGroupGui" testclass="ThreadGroup" testname="Load Test">
  <intProp name="ThreadGroup.num_threads">100</intProp>
  <intProp name="ThreadGroup.ramp_time">60</intProp>
  <longProp name="ThreadGroup.duration">300</longProp>
  
  <HTTPSamplerProxy testname="GET /products">
    <stringProp name="HTTPSampler.path">/products?q=${query}</stringProp>
    <stringProp name="HTTPSampler.method">GET</stringProp>
  </HTTPSamplerProxy>
  
  <ResponseAssertion testname="Status 200">
    <stringProp name="Assertion.test_field">Assertion.response_code</stringProp>
    <collectionProp name="Asserion.test_strings">
      <stringProp>200</stringProp>
    </collectionProp>
  </ResponseAssertion>
</ThreadGroup>
```

### Results Analysis

```python
# analyze_results.py
import json
import statistics
import sys

def analyze_k6_results(json_file: str) -> dict:
    latencies = []
    errors = 0
    total = 0
    
    with open(json_file) as f:
        for line in f:
            entry = json.loads(line)
            if entry["type"] == "Point" and entry["metric"] == "http_req_duration":
                latencies.append(entry["data"]["value"])
                total += 1
            if entry["type"] == "Point" and entry["metric"] == "http_req_failed":
                if entry["data"]["value"] == 1:
                    errors += 1
    
    latencies.sort()
    
    return {
        "total_requests": total,
        "error_rate": errors / total if total > 0 else 0,
        "p50": percentile(latencies, 50),
        "p95": percentile(latencies, 95),
        "p99": percentile(latencies, 99),
        "max": max(latencies) if latencies else 0,
    }

def percentile(sorted_data: list, p: float) -> float:
    if not sorted_data:
        return 0
    k = (len(sorted_data) - 1) * p / 100
    f = int(k)
    c = f + 1
    if c >= len(sorted_data):
        return sorted_data[-1]
    return sorted_data[f] + (sorted_data[c] - sorted_data[f]) * (k - f)

def check_slos(results: dict, slos: dict) -> bool:
    passed = True
    for metric, threshold in slos.items():
        value = results.get(metric, float('inf'))
        status = "✅" if value <= threshold else "❌"
        print(f"{status} {metric}: {value:.1f}ms (threshold: {threshold}ms)")
        if value > threshold:
            passed = False
    return passed

if __name__ == "__main__":
    results = analyze_k6_results(sys.argv[1])
    
    SLOs = {
        "p50": 200,
        "p95": 500,
        "p99": 2000,
    }
    
    print(f"\nTotal requests: {results['total_requests']:,}")
    print(f"Error rate: {results['error_rate']:.3%}")
    print()
    
    passed = check_slos(results, SLOs)
    sys.exit(0 if passed else 1)
```

### CI Integration

```yaml
# .github/workflows/load-test.yml
name: Load Test

on:
  schedule:
    - cron: '0 2 * * *'  # Nightly
  workflow_dispatch:
    inputs:
      target_rps:
        description: 'Target RPS'
        default: '500'

jobs:
  load-test:
    runs-on: ubuntu-latest
    environment: staging
    
    steps:
      - uses: actions/checkout@v4
      
      - name: Setup k6
        uses: grafana/setup-k6-action@v1
      
      - name: Generate test data
        run: python scripts/generate_test_data.py -o test-data/
      
      - name: Run load test
        run: |
          k6 run \
            --out json=results.json \
            --env BASE_URL=${{ secrets.STAGING_URL }} \
            --env TARGET_RPS=${{ inputs.target_rps || 500 }} \
            load-tests/load-test.js
      
      - name: Analyze results
        run: python scripts/analyze_results.py results.json
      
      - name: Upload results
        if: always()
        uses: actions/upload-artifact@v4
        with:
          name: load-test-results-${{ github.run_id }}
          path: results.json
```

## Rules

- **Never run load tests against production** without explicit traffic isolation.
- **Start low** — baseline at 10% of target before ramping up.
- **Use arrival rate, not VU count** — constant arrival rate is more realistic than "N threads".
- **Model real traffic mix** — don't just hammer one endpoint.
- **Add think time** — real users pause between actions (1-5 seconds typical).
- **Test all SLOs explicitly** — set thresholds in the script so tests fail automatically.
- **Monitor the database** — most performance bottlenecks are DB queries, not app code.
- **Soak test weekly** — memory leaks take hours to manifest, not minutes.
- **Store and compare results** — a test that doesn't track trends over time has limited value.
- **Include spike tests** — validate behavior under sudden traffic bursts, not just steady ramp.
