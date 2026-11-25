---
name: load-test-design
description: Design realistic load tests with open-model arrival rates, request mix, think time, ramp, thresholds, and observability. Use to verify SLOs at expected load before launch and after material changes.
source: self
date_added: 2026-05-01
---

# Load Test Design

Load testing answers: *"Does the system meet SLOs at expected load?"* — distinct from stress (find the knee), spike (sudden surges), and soak (long-term drift). This skill keeps your load tests realistic, repeatable, and CI-friendly.

## Stack Baseline (2026)

| Concern | Default |
| --- | --- |
| Tool | **k6 0.55** (preferred), Gatling 3.13, Locust 3, JMeter 5.6 |
| Model | Open model (`constant-arrival-rate`) — not closed VUs |
| Load shape | Ramp → steady → ramp-down; 30–60 min steady at target RPS |
| Mix | Real production traffic mix (read/write ratio, endpoint weights) |
| Data | Per-VU users; randomized IDs; idempotency keys; rotated tokens |
| Thresholds | per-endpoint p95/p99, error rate, throughput, dropped requests |
| Cloud runners | k6 Cloud (Grafana Cloud), Gatling Enterprise, BlazeMeter |
| CI | GitHub Actions / GitLab job; artifacts published to Grafana |

## When to Use

- Pre-launch sign-off against SLOs.
- Post-deploy nightly to detect regression.
- After material changes (framework upgrade, schema migration, new dependency).
- Black-Friday / sale-event readiness.
- Continuous trickle: "tiny load test on every PR" (smoke).

## Inputs You Need First

1. **Forecast peak RPS** per endpoint (from analytics or capacity plan).
2. **SLOs**: p95/p99 latency, error rate, availability per endpoint.
3. **Request mix** (e.g., 70% read, 25% browse, 5% checkout) with realistic payload sizes.
4. **User shape**: think time distribution (often log-normal), session length.
5. **Auth flow**: how to obtain a token without coupling tests to login.
6. **Environment**: staging sized like prod, real downstreams or realistic latency mocks.
7. **Data set**: enough breadth so cache hit-rate matches prod (small sets bias high).

## Load Shape Anatomy

```
RPS
 ^
 |          ┌───────────── steady (45 min @ 800 RPS) ─────────────┐
 |         /                                                       \
 |        /                                                         \
 |       / ramp (5 min)                                              \ ramp-down (5 min)
 +------/--------------------------------------------------------------\---> time
       t0                                                              t60
```

Why ramp: bypasses cold caches, JIT warmup, autoscaling delay. Don't measure during ramp.

## Open vs. Closed Model

- **Open** (`constant-arrival-rate`): generator submits N requests/sec regardless of response time. Reveals saturation truthfully.
- **Closed** (fixed VUs running back-to-back): under stress, slow responses *reduce* offered load → masks saturation. Use only when modeling fixed-user workloads (e.g., call-center).

## k6 Reference Test

```js
import http from 'k6/http';
import { sleep } from 'k6';
import { Trend } from 'k6/metrics';

const checkoutLatency = new Trend('checkout_latency', true);

export const options = {
  scenarios: {
    main: {
      executor: 'ramping-arrival-rate',
      startRate: 0,
      timeUnit: '1s',
      preAllocatedVUs: 400,
      maxVUs: 1500,
      stages: [
        { target: 800, duration: '5m'  },  // ramp
        { target: 800, duration: '45m' },  // steady
        { target: 0,   duration: '5m'  },  // ramp down
      ],
    },
  },
  thresholds: {
    'http_req_failed': ['rate<0.005'],
    'http_req_duration{name:GET /products}':       ['p(95)<200', 'p(99)<400'],
    'http_req_duration{name:GET /products/:id}':   ['p(95)<250', 'p(99)<500'],
    'http_req_duration{name:POST /cart}':          ['p(95)<300', 'p(99)<700'],
    'checkout_latency':                            ['p(99)<800'],
  },
};

const BASE = __ENV.BASE;
const TOKEN = __ENV.TOKEN;
const headers = (extra = {}) => ({ Authorization: `Bearer ${TOKEN}`, ...extra });

export default function () {
  // mix
  const r = Math.random();
  if (r < 0.70) {
    http.get(`${BASE}/products`, { headers: headers(), tags: { name: 'GET /products' } });
  } else if (r < 0.95) {
    const id = `sku-${Math.floor(Math.random() * 5000)}`;
    http.get(`${BASE}/products/${id}`, { headers: headers(), tags: { name: 'GET /products/:id' } });
  } else {
    const idem = crypto.randomUUID();
    const t0 = Date.now();
    http.post(`${BASE}/checkout`, JSON.stringify({ sku: 'A' }),
      { headers: headers({ 'Idempotency-Key': idem, 'Content-Type': 'application/json' }), tags: { name: 'POST /checkout' } });
    checkoutLatency.add(Date.now() - t0);
  }
  sleep(Math.max(0.05, randomLogNormal(0.3, 0.5)));
}
```

## Trace Correlation

Always emit `traceparent` so failed/long requests link to backend traces:

```js
import { uuidv4 } from 'https://jslib.k6.io/k6-utils/1.4.0/index.js';
const traceId  = uuidv4().replace(/-/g, '').slice(0, 32);
const spanId   = uuidv4().replace(/-/g, '').slice(0, 16);
const traceparent = `00-${traceId}-${spanId}-01`;
```

## Common Pitfalls

| Pitfall | Fix |
| --- | --- |
| Closed-model VUs at scale | Use open model (`*-arrival-rate`) for true saturation behavior |
| Cache hit too high (small dataset) | Use realistic ID cardinality |
| All requests hit `/health` | Mix real endpoints with real payloads |
| Single test user | Per-VU users; respect rate-limits via auth rotation |
| Ramp included in measurement | Window your assertions to steady-state only |
| No threshold per endpoint | Set per-endpoint p95/p99 — averages hide tails |
| No trace correlation | Emit `traceparent` for backend drill-down |
| Run on dev laptop ad-hoc | Run from CI in a stable region; pin runner spec |
| Authoring tests in staging only | Smoke against PR previews keeps regressions out |

## Output Format

```
Load Test: orders-api  shape=ramp(5)+steady(45)+rampdown(5)  target=800 RPS
Pass:    ✅
Latency (steady window only):
  GET /products            p95 138ms  p99 286ms  (SLO 200/400)  ✅
  GET /products/:id        p95 196ms  p99 410ms  (SLO 250/500)  ✅
  POST /checkout           p95 248ms  p99 612ms  (SLO 300/800)  ✅
Errors: 0.18%               (SLO ≤0.5%)                          ✅
Throughput delivered:      797.4 RPS (target 800)
Top latency drivers:       OrderService.assemble (38%), tax-svc call (22%)
Notes:                     2 transient 502s during deploy at 22:43 — re-run baseline w/o deploy window
```

## References

- k6 Test Types: <https://grafana.com/docs/k6/latest/testing-guides/test-types/load-testing/>
- N. Gunther — *Open vs. Closed Workloads*
- Google SRE Book — Eliminating toil; SLOs
- Brendan Gregg — Latency heat maps
- Gatling docs: <https://docs.gatling.io/>
