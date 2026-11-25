---
name: performance-load
description: "Load testing: goals from SLOs, realistic scenarios and data, k6 as the default tool (Locust, Gatling, Artillery, oha and wrk for quick checks), ramp, stress, soak and spike tests, thresholds for latency percentiles and error rates, a production-like environment, watching saturation while the test runs, finding the knee, and reporting. Read before load testing a service or planning capacity."
---

# Load testing

The generated load test: `ab -n 1000 -c 100` against the home page, from a
laptop on Wi-Fi, at a staging database with fifty rows, reporting the
average and "handles 1,000 users". The generator itself is at 100% CPU, the
tool waits for each response before sending the next so the slowdown hides
itself, and nobody watched the database. This skill sets goals from SLOs,
builds scenarios from real traffic, uses k6 by default, runs the right test
types, watches saturation while the test runs, finds the knee and reports
it. The measurement method is in `performance`; fixing what the test finds
is in `performance-backend`.

## 1. Goals first

- **Traffic**: the expected peak in requests per second at the busiest
  minute (from access logs or analytics, not a daily average), expected
  growth, known events (a launch, a campaign). With no data, state the
  assumption and have the owner confirm it.
- **SLOs as pass or fail**: for example p95 under 300ms and p99 under 1s at
  peak, errors under 1%, per endpoint when they differ.
- **The question** the run answers: does it meet the SLO at the expected
  peak (load)? Past it (stress)? Where does it break (breakpoint)? Does it
  hold for hours (soak)? Does it recover from a burst (spike)?
- **Users to requests**: active users x requests per user per second. A
  thousand active users each making a request every 10 seconds is 100
  requests per second, not 1,000.

## 2. Scenarios from real traffic

- The endpoint mix from access logs or APM: the top 5 to 10 endpoints by
  volume and by total time, in their real proportions, reads and writes.
- User journeys where order matters (sign in, list, open, update), with
  think time between steps (1 to 5s, randomised). A single-endpoint test
  only answers a focused question.
- Many distinct test users and records: one account for every virtual user
  tests one row lock and one hot cache key. Create tokens in `setup()` or
  beforehand; do not hammer sign-in unless it is the subject (password
  hashing is slow on purpose).
- Data at production volume and shape, the largest tenants included:
  query plans, hit rates and index sizes change with size. Never copy real
  personal data into a test environment.
- Warm or cold caches: a warm-up stage excluded from the results, or a run
  right after a deploy; test the one that matches the question.
- Writes create data: use a test tenant and clean it up afterwards.

## 3. Tools

| Tool | Use it for |
|---|---|
| k6 | the default: scripts in JavaScript or TypeScript, open and closed models, thresholds that fail the run, CI-friendly; distributed with the k6 Operator or Grafana Cloud k6 |
| Locust | a Python team, or behaviour easiest to write in Python: `locust -f locustfile.py --headless -u 500 -r 50 -t 10m --host <url>` |
| Gatling | JVM teams; high load from one machine; open injection profiles in a Java, Kotlin or Scala DSL |
| Artillery | YAML scenarios, Node plugins, browser load through Playwright |
| oha, wrk, hey, vegeta | a quick look at one endpoint; vegeta, wrk2 (`-R`) and oha with `-q` hold a constant rate |

Not ApacheBench (`ab`): HTTP/1.0, one thread and a closed model; it
measures itself as much as the server.

## 4. A k6 script

```js
import http from "k6/http";
import { check } from "k6";
import { SharedArray } from "k6/data";

// users.json: test accounts generated for this environment, never committed
const users = new SharedArray("users", () => JSON.parse(open("./users.json")));
const BASE = __ENV.BASE_URL;

export const options = {
  scenarios: {
    peak: {
      executor: "constant-arrival-rate", // open model: arrivals ignore response times
      rate: 200, timeUnit: "1s", duration: "15m",
      preAllocatedVUs: 100, maxVUs: 1000,
    },
  },
  thresholds: {
    http_req_failed: ["rate<0.01"],
    "http_req_duration{name:orders_list}": ["p(95)<300", "p(99)<1000"],
    checks: ["rate>0.99"],
  },
};

export default function () {
  const user = users[Math.floor(Math.random() * users.length)];
  const res = http.get(`${BASE}/api/orders?status=open`, {
    headers: { Authorization: `Bearer ${user.token}` },
    tags: { name: "orders_list" },
  });
  check(res, { "status is 200": (r) => r.status === 200 });
}
```

```bash
k6 run -e BASE_URL=https://staging.example.com orders.js
K6_WEB_DASHBOARD=true k6 run --out json=results.json -e BASE_URL=https://staging.example.com orders.js
```

- Give requests with ids in the URL a `name` tag (or use the `http.url`
  template), or every id becomes its own metric series.
- `http_req_duration` is sending, waiting and receiving; `http_req_waiting`
  is time to first byte, and connection setup sits in `http_req_connecting`
  and `http_req_tls_handshaking`.
- Thresholds make the run pass or fail: k6 exits with code 99 when one
  fails, which gates CI. `abortOnFail: true` stops a run already failing.
- `dropped_iterations` counts arrivals k6 could not start for lack of VUs:
  the system or the generator is not keeping up. Raise `maxVUs`, or treat
  it as a failure.
- Tokens and URLs come from the environment (`-e`, `__ENV`), never written
  into the script.

## 5. Test types

| Test | Load shape | Answers | Length |
|---|---|---|---|
| Smoke | 1 to 5 VUs | the script works; a baseline latency | 1 to 2 min |
| Load | ramp to the expected peak, hold | the SLO holds at peak | 5 to 10 min ramp, 15 to 60 min hold |
| Stress | ramp past peak (1.5 to 3x), hold | degrades cleanly or falls over | 20 to 40 min |
| Breakpoint | arrival rate rising until thresholds break | the capacity limit and what gives first | until it breaks |
| Soak | normal load for hours | leaks, pool exhaustion, disks filling, token and certificate expiry, drift | 4 to 12 hours |
| Spike | 5 to 10x within seconds, then back | autoscaling, queueing, recovery time | 10 to 20 min |

Smoke first, then load; stress and breakpoint only where breaking things
is allowed. A breakpoint scenario in k6:

```js
export const options = {
  scenarios: {
    breakpoint: {
      executor: "ramping-arrival-rate",
      startRate: 50, timeUnit: "1s",
      preAllocatedVUs: 200, maxVUs: 3000,
      stages: [{ target: 2000, duration: "30m" }],
    },
  },
  thresholds: {
    http_req_failed: [{ threshold: "rate<0.05", abortOnFail: true }],
    http_req_duration: [{ threshold: "p(95)<1000", abortOnFail: true, delayAbortEval: "1m" }],
  },
};
```

## 6. Open and closed models

- **Closed**: a fixed number of virtual users, each waiting for its
  response before sending the next (k6 `constant-vus` and `ramping-vus`,
  Locust, wrk, hey, ab). When the server slows, the tool sends less: load
  drops exactly when it matters, and latency looks better than users would
  see it.
- **Open**: requests arrive at a set rate whatever the responses do, like
  users on the internet (k6 `constant-arrival-rate` and
  `ramping-arrival-rate`, Gatling's open injection, Artillery's
  `arrivalRate`, vegeta, wrk2). Use it for public services and APIs.
- Closed fits a system with a fixed set of clients: a pool of workers, a
  fleet of devices polling on a schedule.
- **Coordinated omission**: a closed tool measures from when it sent a
  request, not from when it should have, so a 2s stall is recorded once
  instead of as the hundreds of requests that would have queued behind it.
  Percentiles come out far too good. Use an open model, or a tool that
  corrects for it (wrk2, oha with `--latency-correction`, HdrHistogram's
  correction).

## 7. The environment

- Production-like: the same instance sizes and counts (results do not
  scale linearly from a smaller setup), the same database size, indexes
  and settings, production mode and log level, and the same path (load
  balancer, TLS, CDN when it is in the path).
- Not production, unless planned with its owners: an agreed window,
  people watching, a way to stop at once, rate limits and the WAF told,
  and the traffic marked (a header) so analytics, billing and alerts can
  exclude it.
- Third parties stubbed (a mock server answering with realistic latency)
  or agreed with the provider. Never load test a payment, email or SMS
  provider, or anyone's API, without consent: it costs money and breaks
  their terms.
- Rate limits and bot protection raised for the test users, or the test
  measures the limiter.
- The generator must not be the bottleneck: keep its CPU under about 70
  to 80% and watch its network; spread it over machines when needed. Run
  it in the target's region to measure the service, from outside to
  measure the user's path.

## 8. Watch saturation while it runs

The generator's numbers say that it got slow; the system's metrics say
why. For every resource, the USE method: utilisation, saturation, errors.

| Resource | Watch |
|---|---|
| CPU | utilisation per instance, run queue, container throttling (`container_cpu_cfs_throttled_periods_total`) |
| Memory | RSS and GC time; growth across a soak (`performance-memory`) |
| Database | CPU, connections in use against `max_connections`, lock waits, slow queries, replication lag |
| Pools and queues | connections in use and waiting, acquire time; queue depth and age of the oldest item |
| Runtime | event loop delay (Node), thread pool queue (.NET, JVM), goroutine count |
| Network | bandwidth, open connections, `TIME_WAIT` and ephemeral ports on the generator |
| Caches | hit ratio and evictions |

- Per endpoint, rate, errors and duration (the RED method) from the
  service's own metrics, to confirm what the generator saw.
- Traces of the slowest requests during the run show where the time went
  (`performance-backend`).
- Errors by kind: `5xx`, timeouts, connection refused or reset, `429`. A
  run that passes its latency threshold with 2% connection resets has
  failed.

## 9. Find the knee

- Step the arrival rate up (10 to 20% per step, each held 3 to 5 minutes
  to settle) and plot achieved throughput, p95 and p99 against the
  offered rate.
- The knee is where throughput stops following the offered load while p95
  and p99 bend upward; past it, queues grow and timeouts and errors
  follow.
- Capacity is the highest rate that stays inside the SLO. Plan peak
  traffic at 60 to 75% of it, which leaves room for a slow dependency, a
  deploy or a lost instance.
- Name the first resource that saturated at the knee: that is the
  bottleneck and the next fix (`performance-backend`, `database-queries`).
  Fix it and test again; the next bottleneck appears.
- After a stress or spike test, check recovery: latency back to baseline
  within minutes, pools drained, no retry storm. A system that stays
  broken after the load has gone is a finding in itself.

## 10. Report

```text
Question:     <what the run answers>
Scenario:     <endpoints and mix, think time, data volume, open or closed, warm or cold>
Load profile: <rates and stages, durations>
Environment:  <instances and sizes, database size, versions, commit, generator location>
Results:      per stage: offered rate, achieved rate, p50 / p95 / p99, errors by kind
Saturation:   <first resource to saturate, and at what rate>
Capacity:     <knee rate>; within the SLO up to <rate>
Verdict:      <meets the SLO at peak, or not>
Next:         <the fix or capacity change recommended>
Not tested:   <what was stubbed, skipped or could not be run>
```

Attach the k6 summary or JSON output, and the dashboards for the test
window. Only measured numbers; say what could not be run and why.

## 11. Load tests in CI

- A short run (1 to 3 minutes at a modest fixed rate) against a preview or
  staging deployment, with thresholds, on each merge: a guard against gross
  regressions (a new N+1, a missing index), not a capacity test. Shared
  runners and small environments turn fine differences into noise.
- Thresholds loose enough not to flake (for example twice the usual p95),
  and the summary compared with the previous run's.
- In GitHub Actions, `grafana/setup-k6-action` and `grafana/run-k6-action`
  run the scripts; tokens come from the CI's secret store.

## Check it

- The smoke run passed with checks at 100% before the real run.
- The generator stayed inside its own limits: CPU below saturation,
  `dropped_iterations` at zero, no connection errors on its side.
- The model matches the question (open for public traffic), and the
  percentiles cover the full run minus the warm-up.
- The system's own metrics agree with the generator's numbers.
- Results are reported per stage with the environment, and what could not
  be run is said.

## Avoid

`ab` against the home page; a closed model for internet traffic; averages
instead of percentiles; one test user and one record; a seed-sized
database; a generator on a laptop or at 100% CPU; load tests on production
or third-party APIs without agreement; results with no system metrics
beside them; "handles 1,000 users" without a rate, a latency and an error
rate; secrets in the script; a capacity claimed from a run that never
reached the knee.
