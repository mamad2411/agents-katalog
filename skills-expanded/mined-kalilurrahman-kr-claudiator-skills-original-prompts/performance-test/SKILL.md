---
name: performance-test
description: Design performance and load tests with JMeter, k6, Locust. Outputs test scenarios, metrics, bottleneck analysis, and capacity planning.
argument-hint: [expected load, SLA requirements, infrastructure]
allowed-tools: Read, Write, Bash
---

# Performance Testing

Design load, stress, and performance tests for applications. Not ad-hoc testing — systematic scenarios with metrics, bottleneck identification, and capacity planning.

## Process

1. **Define SLAs.** Response time (p95 < 200ms), throughput (1000 rps), error rate (< 0.1%).
2. **Create scenarios.** Normal load, peak load, stress (2x peak), spike, endurance.
3. **Choose tool.** k6 (modern, JS), JMeter (GUI, enterprise), Locust (Python).
4. **Write tests.** User journeys, realistic data, think time.
5. **Run tests.** Ramp-up, sustained load, ramp-down.
6. **Analyze metrics.** Response time (p50/p95/p99), throughput, errors, saturation.
7. **Identify bottlenecks.** CPU, memory, database, network.

## Output Format

### Performance Test: [Application Name]

**Tool:** k6  
**Target SLA:** p95 < 200ms, 1000 rps  
**Test Types:** Load, stress, spike, endurance  
**Result:** Passed (p95 = 180ms @ 1200 rps)  
**Bottleneck:** Database connection pool (fixed)

---

## Test Types

### Load Test (Normal Usage)
```
Users: 1000 concurrent
Duration: 30 minutes
Goal: Verify system handles expected load
SLA: p95 < 200ms, error rate < 0.1%
```

### Stress Test (Beyond Capacity)
```
Users: Ramp from 1000 → 5000
Duration: 60 minutes
Goal: Find breaking point
Expected: Graceful degradation, no crashes
```

### Spike Test (Sudden Traffic)
```
Users: 100 → 2000 (instant)
Duration: 10 minutes
Goal: Test autoscaling, caching
Expected: System recovers within 2 minutes
```

### Endurance Test (Soak)
```
Users: 1000 concurrent
Duration: 24 hours
Goal: Find memory leaks, resource exhaustion
Expected: Stable metrics over time
```

---

## k6 (Recommended)

```javascript
// load-test.js
import http from 'k6/http';
import { check, sleep } from 'k6';
import { Rate } from 'k6/metrics';

// Custom metrics
const errorRate = new Rate('errors');

export const options = {
  stages: [
    { duration: '2m', target: 100 },   // Ramp up to 100 users
    { duration: '5m', target: 100 },   // Stay at 100 users
    { duration: '2m', target: 500 },   // Ramp up to 500
    { duration: '5m', target: 500 },   // Stay at 500
    { duration: '2m', target: 0 },     // Ramp down
  ],
  thresholds: {
    http_req_duration: ['p(95)<200'],  // 95% under 200ms
    http_req_failed: ['rate<0.01'],    // < 1% errors
    errors: ['rate<0.1'],              // < 10% check failures
  },
};

export default function () {
  // Login
  let loginRes = http.post('https://api.example.com/login', JSON.stringify({
    username: 'user@example.com',
    password: 'password123',
  }), {
    headers: { 'Content-Type': 'application/json' },
  });

  check(loginRes, {
    'login successful': (r) => r.status === 200,
    'has auth token': (r) => r.json('token') !== '',
  }) || errorRate.add(1);

  const token = loginRes.json('token');

  sleep(1); // Think time

  // Browse products
  let productsRes = http.get('https://api.example.com/products', {
    headers: { 'Authorization': `Bearer ${token}` },
  });

  check(productsRes, {
    'products loaded': (r) => r.status === 200,
    'has products': (r) => r.json('products').length > 0,
  }) || errorRate.add(1);

  sleep(2);

  // Add to cart
  const productId = productsRes.json('products.0.id');
  let cartRes = http.post('https://api.example.com/cart', JSON.stringify({
    productId: productId,
    quantity: 1,
  }), {
    headers: {
      'Authorization': `Bearer ${token}`,
      'Content-Type': 'application/json',
    },
  });

  check(cartRes, {
    'added to cart': (r) => r.status === 201,
  }) || errorRate.add(1);

  sleep(5);
}

// Run: k6 run load-test.js
```

### k6 Results
```
execution: local
     scenarios: (100.00%) 1 scenario, 500 max VUs, 16m30s max duration
     default: 500 looping VUs for 14m0s

     ✓ login successful
     ✓ has auth token
     ✓ products loaded
     ✓ added to cart

     checks.........................: 100.00% ✓ 48523      ✗ 0
     data_received..................: 122 MB  145 kB/s
     data_sent......................: 18 MB   21 kB/s
     http_req_blocked...............: avg=1.2ms    p(95)=3.5ms
     http_req_duration..............: avg=180ms    p(95)=195ms  p(99)=210ms
     http_req_failed................: 0.00%   ✓ 0          ✗ 48523
     http_reqs......................: 48523   57.5/s
     iteration_duration.............: avg=8.2s     p(95)=8.5s
     iterations.....................: 16174   19.2/s
     vus............................: 100     min=100      max=500
     vus_max........................: 500     min=500      max=500
```

---

## JMeter

### Test Plan Structure
```
Test Plan
├── Thread Group (Users)
│   ├── HTTP Request Defaults
│   ├── HTTP Header Manager
│   └── Requests
│       ├── Login
│       ├── Browse Products
│       └── Add to Cart
├── Listeners
│   ├── View Results Tree
│   ├── Summary Report
│   └── Aggregate Report
└── Assertions
    ├── Response Time < 200ms
    └── Response Code = 200
```

### Thread Group Config
```
Number of Threads: 1000
Ramp-up Period: 60 seconds (16.6 users/sec)
Loop Count: 10
Duration: 600 seconds
```

### CSV Data Set Config
```csv
# users.csv
username,password
user1@example.com,pass1
user2@example.com,pass2
...
```

```
CSV Data Set Config:
- Filename: users.csv
- Variable Names: username,password
- Recycle on EOF: True
- Stop thread on EOF: False
```

### Run JMeter
```bash
# GUI mode (development)
jmeter -t load-test.jmx

# CLI mode (CI/CD)
jmeter -n -t load-test.jmx -l results.jtl -e -o report/

# Distributed testing
jmeter -n -t test.jmx -R server1,server2,server3
```

---

## Locust (Python)

```python
# locustfile.py
from locust import HttpUser, task, between
import random

class EcommerceUser(HttpUser):
    wait_time = between(1, 5)  # Think time: 1-5 seconds
    
    def on_start(self):
        """Login once per user"""
        response = self.client.post("/login", json={
            "username": "user@example.com",
            "password": "password123"
        })
        self.token = response.json()["token"]
        self.client.headers["Authorization"] = f"Bearer {self.token}"
    
    @task(3)  # Weight: 3x more likely than other tasks
    def browse_products(self):
        """Browse product list"""
        self.client.get("/products")
    
    @task(2)
    def view_product(self):
        """View product detail"""
        product_id = random.randint(1, 100)
        self.client.get(f"/products/{product_id}")
    
    @task(1)
    def add_to_cart(self):
        """Add product to cart"""
        self.client.post("/cart", json={
            "productId": random.randint(1, 100),
            "quantity": 1
        })
    
    @task(1)
    def view_cart(self):
        """View cart"""
        self.client.get("/cart")

# Run: locust -f locustfile.py --host=https://api.example.com
# Web UI: http://localhost:8089
```

---

## Metrics to Track

### Response Time
```
p50 (median): 50% of requests faster
p95: 95% of requests faster (SLA target)
p99: 99% of requests faster (tail latency)
max: Slowest request
```

**Example:**
```
p50: 150ms  ← Most users experience
p95: 200ms  ← SLA threshold
p99: 350ms  ← Outliers
max: 2000ms ← Database timeout
```

### Throughput
```
Requests per second (RPS)
Concurrent users (VUs)
```

### Error Rate
```
HTTP 4xx: Client errors
HTTP 5xx: Server errors
Timeouts
Connection errors
```

### Resource Utilization
```
CPU: %
Memory: % used
Disk I/O: IOPS
Network: Mbps
```

---

## Bottleneck Analysis

### Symptoms → Diagnosis

#### High Response Time + Low CPU
```
Symptom: p95 > 500ms, CPU < 50%
Diagnosis: I/O bound (database, external API)
Fix: Optimize queries, add caching, parallel requests
```

#### High CPU + Normal Response Time
```
Symptom: CPU > 80%, p95 = 200ms
Diagnosis: Compute bound
Fix: Optimize algorithms, horizontal scaling
```

#### Increasing Memory Over Time
```
Symptom: Memory grows from 2GB → 8GB over 1 hour
Diagnosis: Memory leak
Fix: Profile with heap dump, fix leak
```

#### Spike in Error Rate at 1000 Users
```
Symptom: Errors jump to 5% at exactly 1000 users
Diagnosis: Connection pool exhausted
Fix: Increase pool size, add queueing
```

---

## Database Bottlenecks

```sql
-- Slow query log
SET global slow_query_log = 'ON';
SET global long_query_time = 0.5;  -- Log queries > 500ms

-- Find slow queries
SELECT query, query_time, rows_examined
FROM mysql.slow_log
ORDER BY query_time DESC
LIMIT 10;

-- Connection pool saturation
SHOW STATUS LIKE 'Threads_connected';
SHOW VARIABLES LIKE 'max_connections';

-- If Threads_connected = max_connections → exhausted
```

**Fixes:**
- Add indexes on frequently queried columns
- Optimize N+1 queries (use joins or DataLoader)
- Increase connection pool size
- Add read replicas
- Implement caching (Redis)

---

## CI/CD Integration

```yaml
# .github/workflows/performance.yml
name: Performance Tests

on:
  pull_request:
    branches: [main]

jobs:
  performance:
    runs-on: ubuntu-latest
    
    steps:
      - uses: actions/checkout@v3
      
      - name: Run k6 test
        uses: grafana/k6-action@v0.3.0
        with:
          filename: tests/load-test.js
          cloud: true
          token: ${{ secrets.K6_CLOUD_TOKEN }}
      
      - name: Check SLA
        run: |
          if [ $(jq '.metrics.http_req_duration.p95' results.json) -gt 200 ]; then
            echo "SLA violated: p95 > 200ms"
            exit 1
          fi
```

---

## Capacity Planning

### Calculate Capacity
```
Current: 1000 RPS @ 50% CPU
Target: Support 5000 RPS

Linear scaling:
5000 RPS = 5x load = 250% CPU = 2.5x servers
Round up: 3x current capacity

Budget for spikes (2x peak):
10,000 RPS = 6x current capacity
```

### Autoscaling Configuration
```yaml
# Kubernetes HPA
apiVersion: autoscaling/v2
kind: HorizontalPodAutoscaler
metadata:
  name: api-hpa
spec:
  scaleTargetRef:
    apiVersion: apps/v1
    kind: Deployment
    name: api
  minReplicas: 3
  maxReplicas: 10
  metrics:
  - type: Resource
    resource:
      name: cpu
      target:
        type: Utilization
        averageUtilization: 70  # Scale at 70% CPU
```

---

## Best Practices

### Realistic Test Data
```python
# Bad: Same user every time
user = "test@example.com"

# Good: Random users from dataset
import random
users = load_users_from_csv()
user = random.choice(users)
```

### Think Time
```javascript
// Bad: Instant requests
http.get('/products');
http.get('/cart');

// Good: Simulate real user behavior
http.get('/products');
sleep(3);  // User browses for 3 seconds
http.get('/cart');
```

### Gradual Ramp-Up
```
Bad:  0 → 1000 users instantly (spikes error rate)
Good: 0 → 1000 over 5 minutes (smooth ramp)
```

---

## Monitoring During Tests

```bash
# Real-time metrics
watch -n 1 'curl -s http://localhost:9090/metrics | grep http_requests'

# Top processes by CPU
top -o %CPU

# Database connections
psql -c "SELECT count(*) FROM pg_stat_activity;"

# Network throughput
iftop -i eth0
```

---

## Report Template

```markdown
## Performance Test Report

**Date:** 2024-03-21  
**Tool:** k6  
**Duration:** 30 minutes  
**Target:** 1000 concurrent users

### SLA Requirements
- p95 response time: < 200ms
- Error rate: < 0.1%
- Throughput: > 1000 RPS

### Results
- **p50:** 145ms ✅
- **p95:** 180ms ✅
- **p99:** 220ms ⚠️
- **Error rate:** 0.05% ✅
- **Throughput:** 1200 RPS ✅

### Bottlenecks Identified
1. Database query on /products endpoint (150ms)
   - Fix: Add index on category_id
2. JWT verification CPU spike at peak
   - Fix: Cache decoded tokens for 5 minutes

### Recommendations
- Current capacity supports 1500 RPS
- For 2000 RPS, scale to 2x instances
- Implement Redis caching for products catalog
```

## Rules

- Define SLAs before testing — p95 response time, error rate, throughput targets.
- Ramp up gradually — instant load causes false failures from connection storms.
- Use realistic data — production-like datasets, not "test@test.com" everywhere.
- Include think time — users don't instantly click, simulate 1-5 second pauses.
- Test at 2x peak load — stress test reveals breaking point and graceful degradation.
- Run in production-like environment — staging with same infra as production.
- Monitor resources during test — CPU, memory, database connections, not just response time.
- Test for 30+ minutes — catches memory leaks and resource exhaustion missed in 5-minute tests.
- Automate tests in CI — run on every release candidate to catch regressions.
- Document bottlenecks and fixes — knowledge base for future optimization.
