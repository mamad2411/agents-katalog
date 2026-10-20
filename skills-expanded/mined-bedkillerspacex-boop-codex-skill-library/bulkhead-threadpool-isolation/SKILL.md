---
name: bulkhead-threadpool-isolation
description: >
  Thread-pool bulkheads for owned JVM/.NET/similar services: dedicated executors per
  dependency or workload, queue bounds, rejection policies, context propagation, and
  sizing. Use when separate thread pools, executor isolation, Tomcat vs async pools,
  or preventing blocking IO from starving request threads — companion to `bulkhead-isolation`.
---

# Bulkhead Threadpool Isolation

## Scope And Authorization

- **In scope:** Application runtimes you operate (Java, Kotlin, .NET, etc.) where thread pools are explicit.
- **Out of scope:** Exhausting shared CI or third-party systems with unbounded fan-out tests without approval.
- Tune with production-like core counts; bad sizing causes latent deadlocks.
- Pair with general `bulkhead-isolation`, timeouts, and `code-quality-standards`.

## When To Use

- Servlet/request threads block on slow IO and need offload **with** isolation.
- Multiple blocking dependencies share one `ExecutorService` / `TaskScheduler`.
- You see thread pool exhaustion (`RejectedExecutionException`, ASP.NET thread starvation).
- Mixing CPU-bound and blocking IO on the same pool.

## Do Not Use As Primary

| Need | Skill instead |
| --- | --- |
| Conceptual bulkhead / dependency partitioning | `bulkhead-isolation` |
| Pure async event-loop apps (Node) without threads | backend async patterns / Node skills |
| K8s CPU limits only | kubernetes resource skills |
| Retry storms | `retry-backoff-patterns` |
| Implementation quality baseline | `code-quality-standards` |

## Domain Focus

| Concept | Guidance |
| --- | --- |
| Dedicated pool | One pool per dependency or workload class |
| Bound queue | `ArrayBlockingQueue` / limited channel — not unbounded `LinkedBlockingQueue` for bulkheads |
| Rejection policy | `Abort`/`CallerRuns` chosen deliberately; measure |
| Sizing | threads ≈ target concurrency; not `Integer.MAX_VALUE` |
| Context | Propagate MDC/trace/auth carefully to worker threads |
| Naming | Pool names in dumps/metrics (`payments-pool`) |

## Workflow

### 1. Confirm scope and success criteria

1. Runtime (JVM version / .NET), framework (Spring WebMVC vs WebFlux, etc.).
2. Success: slow dependency saturates only its pool; request threads remain available; rejections visible in metrics.
3. Decide which work stays on request threads vs offloaded.

### 2. Inventory pools

```bash
# JVM example: thread dump
jcmd $PID Thread.print | rg -n "pool-|http-nio|reactor|ForkJoin"
# Micrometer / Actuator threadpool metrics if exposed
curl -s localhost:8080/actuator/metrics | rg -i executor || true
```

1. List framework pools: Tomcat/Jetty, reactor, `@Async` default, scheduler.
2. Find shared `@Bean Executor` used by many features.
3. Note blocking calls inside reactive pipelines (anti-pattern).

### 3. Baseline starvation

1. Load test with forced latency on one dependency.
2. Watch: active threads, queue depth, request p99, error rate on unrelated endpoints.
3. Capture one thread dump under stress for evidence.

### 4. Create dedicated executors

**Java sketch:**

```java
@Bean(name = "paymentsExecutor")
public ExecutorService paymentsExecutor() {
  int n = 32;
  return new ThreadPoolExecutor(
      n, n,
      0L, TimeUnit.MILLISECONDS,
      new ArrayBlockingQueue<>(64),
      new ThreadFactoryBuilder().setNameFormat("payments-%d").build(),
      new ThreadPoolExecutor.AbortPolicy()
  );
}

@Bean(name = "recsExecutor")
public ExecutorService recsExecutor() {
  int n = 16;
  return new ThreadPoolExecutor(
      n, n,
      0L, TimeUnit.MILLISECONDS,
      new ArrayBlockingQueue<>(32),
      new ThreadFactoryBuilder().setNameFormat("recs-%d").build(),
      new ThreadPoolExecutor.AbortPolicy()
  );
}
```

**Spring `@Async` isolation:**

```java
@Async("paymentsExecutor")
public CompletableFuture<PaymentResult> charge(...) { ... }
```

**.NET sketch:**

```csharp
// Separate Channel + workers or dedicated System.Threading.ThreadPool is global —
// prefer bounded channels / TPL Dataflow / custom worker groups per dependency
var paymentsWorkers = new SemaphoreSlim(32);
```

**Sizing heuristic:**

1. Measure service time `S` and desired QPS `λ` → concurrency `≈ λ * S` (Little’s law), plus headroom.
2. Queue length: small buffer for bursts; not minutes of work.
3. Sum of pool sizes + server threads must fit memory (stack) and CPU.

### 5. Rejection, timeouts, context

1. On `AbortPolicy` / rejected execution → map to 503 + metric; do not silently drop.
2. `CallerRunsPolicy` can cause latency coupling — use sparingly on noncritical only.
3. Wrap tasks with timeout (`Future.get` timeout, `CompletableFuture.orTimeout`).
4. Propagate trace/MDC:

```java
// Wrap runnable to copy MDC/context
Runnable wrapped = ContextSnapshot.captureAll().wrap(task);
executor.execute(wrapped);
```

5. Never block request thread waiting on the same pool (deadlock risk).

### 6. Verify

```bash
# Load + dump
jcmd $PID Thread.print > /tmp/dump.txt
rg "payments-|recs-|http-nio" /tmp/dump.txt
# Metrics: executor.pool.size, executor.queued, executor.rejected
```

1. Saturate `recs` pool → checkout still healthy.
2. Confirm rejected tasks increment and user-visible fallback works.
3. Heap/CPU under full pools acceptable.

### 7. Hand off

1. Document pool matrix: name, size, queue, rejection, owner.
2. Dashboard row per pool.
3. Code review gate: new blocking dependency needs its own pool bean.
4. Apply `code-quality-standards`; shut down executors on app stop.

## Good / Bad

| Topic | Good | Bad |
| --- | --- | --- |
| Sharing | Pool per dependency | Single applicationTaskExecutor for all |
| Queue | Bounded | Unbounded queue hides incidents |
| Naming | Meaningful thread names | `pool-1-thread-1` only |
| Deadlock | No same-pool reentrant wait | Request thread blocks on same pool task |
| Policy | Abort + metric + fallback | Swallow RejectedExecution |
| Reactive | `publishOn` dedicated scheduler for blocking | `block()` on event loop |

## Output Checklist

- [ ] Runtime/pools inventoried with dumps/metrics
- [ ] Starvation baseline captured
- [ ] Dedicated executors sized and bounded
- [ ] Rejection → user-safe behavior
- [ ] Timeouts and context propagation in place
- [ ] Isolation proven under staging load
- [ ] Pool matrix documented + dashboards
- [ ] Graceful shutdown of executors
- [ ] `code-quality-standards` applied

## Rules

- Bounded queues and explicit rejection are part of the bulkhead.
- Do not size pools by cargo-cult `2 * CPU` alone for blocking IO.
- Avoid deadlocks: document which threads wait on which pools.
- Use `bulkhead-isolation` for non-thread resources (connections, tenants).
- Authorized load tests only.
