---
name: resilience-timeouts-retries
description: Makes calls to flaky dependencies (DBs, HTTP/RPC APIs, queues) survive failure without amplifying it — bounded timeouts on connect/read/total/per-attempt, deadline propagation across the call chain, exponential backoff with FULL jitter, retry budgets/caps, circuit breakers (closed/open/half-open), bulkheads, backpressure + load-shedding (429/503 + Retry-After), and hedged requests for tail latency. Retries only idempotent ops; never retries 4xx except 408/429; library-specific for resilience4j, Polly, tenacity, failsafe-go/gobreaker, JS AbortSignal+p-retry, gRPC deadlines, and Envoy/Istio outlier-detection.
when_to_use: User is calling a network dependency that can be slow/down (HTTP API, DB, RPC, queue) and needs it to fail fast, retry safely, or stop hammering a sick service — or is debugging retry storms, thundering-herd, hung pools, cascading timeouts. Distinct from rate-limiting (limits inbound traffic *you* receive; this protects *your* outbound calls) and async-concurrency-correctness (in-process task/lock/cancellation correctness, not network failure policy). For making the retried write itself safe, pair with idempotency-keys.
---

## When to Use

Reach for this skill when your code crosses a network boundary to something that can be slow, flaky, or down:

- "This call to the payments API / DB sometimes hangs forever and pins all our threads"
- "Add retries to this HTTP/RPC client" (and you need them to not make an outage worse)
- "One slow downstream is taking down the whole service" (cascading failure)
- "We had a retry storm / thundering herd after the dependency recovered"
- "Tail latency (p99) is terrible even though p50 is fine"
- "Should we retry this 500? this timeout? this POST?"

NOT this skill:
- Limiting inbound traffic *you serve* (per-user/IP quotas, token bucket) → rate-limiting. This skill governs the *outbound* calls you make and shedding load when *you* are overwhelmed.
- In-process deadlocks, leaked tasks, locks across `await`, channel backpressure → async-concurrency-correctness. That's correctness of concurrency; this is policy for network failure.
- Making the operation you retry safe to run twice (dedup key, exactly-once effect) → idempotency-keys. Retry without idempotency = duplicate charges.
- Delivering *your* outbound webhooks with retry/backoff/DLQ → deliver-webhooks (this skill is the primitive it builds on).

First principle: **every retry adds load to a system that is already failing.** Default to *fewer* retries with jitter and a budget, never *more*.

## Steps

1. **Put a bound on every wait — no unbounded blocking, ever.** A missing timeout is the root cause of most "the whole service hung" incidents: one stuck call holds a connection/thread until the pool is empty. Set all four:

   | Timeout | What it caps | Typical |
   |---|---|---|
   | connect | TCP/TLS handshake | 1–3s |
   | read/socket | gap between bytes | 2–10s |
   | per-attempt total | one try end-to-end | derived from p99 + margin |
   | overall/deadline | whole op incl. retries | < the caller's own deadline |

   Per-language: JS `fetch(url, { signal: AbortSignal.timeout(ms) })` (default fetch has NO timeout); Python `httpx.Timeout(connect=, read=, write=, pool=)` or `requests` `timeout=(connect, read)` (a bare `timeout=5` is read-only — connect can still hang); Go `http.Client{Timeout}` + a per-request `context.WithTimeout`; Java set both `connectTimeout` and `requestTimeout`. Never leave a driver/client on its infinite default.

2. **Propagate a deadline (time budget), don't restart the clock per layer.** A 5s timeout at three nested layers = up to 15s of real wait. Compute an absolute deadline once at the edge and pass it down; each hop spends from the *remaining* budget. Go: pass `ctx` (carries `WithDeadline`) into every call — `ctx, _ := context.WithTimeout(parent, remaining)`. gRPC: set a **deadline** on the client call (`grpc.WithTimeout`/`context` deadline), and servers must check `ctx.Err()` / `context.Deadline()` and stop work when it's blown. Reserve a slice of the budget for retries — don't let a single attempt consume all of it.

3. **Retry ONLY idempotent/safe operations.** GET/PUT/DELETE are safe; a raw POST is not — a retried "create order" can double-charge. Either restrict retries to safe verbs, or make the write idempotent with an **idempotency key** the server dedupes on (→ idempotency-keys) and only then retry it. Treat "I don't know if it ran" (timeout after send) as **possibly executed** — never blind-retry a non-idempotent write on timeout.

4. **Retry the right errors, fail fast on the rest.**

   | Outcome | Retry? |
   |---|---|
   | connection refused / reset / DNS / connect timeout | yes |
   | read timeout (idempotent op only) | yes |
   | 502, 503, 504 | yes |
   | 429, 408 | yes — and honor `Retry-After` |
   | 500 | usually no (often a deterministic bug — same input, same failure) |
   | 400, 401, 403, 404, 409, 422 | **no** — retrying a client error just burns budget |

   gRPC: retry `UNAVAILABLE`/`DEADLINE_EXCEEDED`/`RESOURCE_EXHAUSTED`; not `INVALID_ARGUMENT`/`NOT_FOUND`/`PERMISSION_DENIED`. When `Retry-After` is present, obey it instead of your backoff.

5. **Back off exponentially with FULL jitter.** Fixed delays (or exponential with *no* jitter) make every client that failed at T retry in lockstep — a synchronized retry storm that re-knocks-over the recovering dependency (thundering herd). Use full jitter: `sleep = random_uniform(0, min(cap, base * 2**attempt))`.

   ```python
   delay = random.uniform(0, min(cap, base * (2 ** attempt)))  # base=0.1s, cap=10s
   ```
   "Equal jitter" (`half + rand(half)`) is acceptable; "no jitter" is the bug. Add `Retry-After` override when the server sent one.

6. **Cap retries and add a retry budget — keep nesting from multiplying load.** Limit attempts (typically **2–3 total**, not 5+) AND a max elapsed (the overall deadline from step 2). Crucial at scale: a per-client **retry budget** (e.g. retries ≤ 10–20% of total requests). Retrying at *every* layer multiplies: 3 layers × 3 retries = 27× load on the bottom service. **Retry at exactly one layer** (usually the lowest, closest to the dependency) and have outer layers fail fast.

7. **Add a circuit breaker so a dead dependency fails instantly.** Stop sending into a hole; give it room to recover. States: **closed** (pass through, count failures) → **open** (fail fast immediately, no call) → **half-open** (after a cooldown, allow a few probes; success → closed, failure → open). Trip on **error-rate over a rolling window** (e.g. >50% of ≥20 calls) rather than raw consecutive failures (less noisy under low traffic). Per-dependency breaker — never one global breaker for all downstreams.

8. **Bulkhead: isolate pools so one sick dependency can't drown the rest.** Give each downstream its *own* connection pool / thread pool / semaphore with a bounded max. Without it, slow calls to dep A consume every worker and requests to healthy dep B also fail. resilience4j `Bulkhead`/`ThreadPoolBulkhead`; a per-dependency `Semaphore(N)`; separate HTTP clients with separate `maxConnsPerHost`. Bound the pool *and* the wait-for-a-slot timeout.

9. **Backpressure & load-shed when *you're* the one overwhelmed.** Bounded queues only — an unbounded queue just hides the overload until OOM and inflates latency past every deadline. When the queue/pool is full, **reject early**: return `503` (or `429`) with `Retry-After` and shed load *before* doing expensive work. Fast rejection beats slow timeout. (Inbound *policy* limits → rate-limiting; this is shedding under acute overload.)

10. **Choose fail-fast vs fail-open/degrade per call deliberately.** On exhausted retries / open breaker: **fail-fast** (propagate the error) for must-be-correct calls (payment authorize); **fail-open / degrade** for optional ones — return a cached/stale value, a default, or a partial response so one non-critical dep can't take down the page. Decide and document it; never default to "throw 500".

11. **Hedge requests for tail latency (read-only/idempotent only).** If p99 ≫ p50, send a second (parallel) request after a delay (e.g. at the p95 latency mark), take whichever returns first, cancel the loser. Cuts tail latency at the cost of extra load — gate it (e.g. ≤5% hedged) so it doesn't amplify during an incident. gRPC supports hedging policy natively. Never hedge non-idempotent writes.

12. **Use the battle-tested library, not a hand-rolled `for` loop.**

    | Stack | Use | Notes |
    |---|---|---|
    | Java/Kotlin | **resilience4j** | `Retry` + `CircuitBreaker` + `Bulkhead` + `TimeLimiter`, composed; order matters (TimeLimiter inside Retry) |
    | .NET | **Polly** | `ResiliencePipeline`: `AddRetry` (with jitter) + `AddCircuitBreaker` + `AddTimeout` |
    | Python | **tenacity** or **backoff** | `@retry(wait=wait_random_exponential(max=10), stop=stop_after_attempt(3), retry=retry_if_exception_type(...))` |
    | Go | **failsafe-go** / **sony/gobreaker** | gobreaker for the breaker; failsafe-go for retry+backoff+circuit composed |
    | JS/TS | **p-retry** + `AbortSignal.timeout` | p-retry for backoff; `opossum` for the circuit breaker |
    | gRPC | service-config `retryPolicy` + `hedgingPolicy` | declarative; set deadlines on the client |
    | Mesh | **Envoy / Istio** | `retryPolicy` (`retry_on: 5xx,connect-failure,retriable-4xx`) + `numRetries` + **outlier detection** (the mesh's circuit breaker — ejects bad hosts) |

    Push retry/breaker policy to the mesh (Envoy/Istio) when you can — it's per-route, consistent across languages, and observable. Keep app-level resilience for finer control (idempotency-aware retries, fallbacks).

13. **Make all of it observable.** Emit metrics per dependency: attempt count, retry count, breaker state transitions, timeout count, shed/rejected count, p99 latency. A breaker that's silently open looks identical to a healthy-but-idle dependency — you must be able to see it. Alert on breaker-open and on retry-budget exhaustion.

## Anti-Patterns

| Anti-pattern | Why it bites | Fix |
|---|---|---|
| Retrying a non-idempotent POST | Double charge / duplicate record | Idempotency key (→ idempotency-keys) or don't retry |
| Backoff with no jitter | Synchronized retry storm hammers the recovering dep | Full jitter |
| Unbounded retries (`while`/no cap) | Burns budget, melts the dependency | Cap 2–3 + overall deadline |
| Retries nested at every layer | 3×3×3 = 27× load multiplication | Retry at ONE layer only |
| Retrying inside a retry (library + manual) | Hidden multiplication, double the attempts | Pick one place to own retries |
| No timeout / infinite default | One hung call drains the whole pool → service down | Bound connect+read+total |
| Retrying 4xx (400/401/404) | Same input, same failure — pure waste | Only retry 5xx/408/429/connect errors |
| One global circuit breaker | One bad dep opens the breaker for all deps | Per-dependency breaker + bulkhead |
| Unbounded queue for backpressure | Latency blows past deadlines, then OOM | Bounded queue + reject early (503/Retry-After) |
| Same timeout at every layer | Inner timeout ≥ outer → outer fires first, inner work wasted | Propagate a shrinking deadline |
