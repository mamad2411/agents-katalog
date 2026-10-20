---
name: fiber-prefork-risks
description: >
  Identify and mitigate security and correctness risks of Go Fiber Prefork mode:
  multi-process listeners, shared state pitfalls, in-memory sessions/caches that do
  not shard, file descriptor and privilege issues, and graceful shutdown. Use when
  enabling Prefork in Fiber apps, debugging sticky bugs under load, or reviewing
  production Fiber deployments on owned services.
---

# Fiber Prefork Risks

## Scope And Authorization

- **In scope:** Fiber applications you own or are authorized to review/operate.
- **Out of scope:** attacking third-party Fiber services or unapproved production experiments.
- Validate Prefork changes in staging with production-like process counts.
- Redact session secrets and connection strings from crash dumps.
- Pair code changes with `code-quality-standards` and `go-style-conventions` if applicable.

## When To Use

- Enabling `Prefork: true` (or CLI prefork) on **gofiber/fiber** for multi-core throughput.
- Incidents where sessions, rate limits, or in-memory feature flags “randomly” fail under Prefork.
- Reviewing whether process model breaks websocket hubs, cron, or singleton jobs.
- Hardening child process privileges and listen sockets.

## Do Not Use As Primary

| Need | Skill instead |
| --- | --- |
| General Go style | `go-style-conventions` |
| Rate-limit bypass testing | `rate-limit-bypass-testing` |
| Redis-backed session security | session/redis skills in catalog |
| Container security baseline | container/K8s skills in catalog |
| Implementation quality baseline | `code-quality-standards` |

## Domain Focus

| Area | Guidance |
| --- | --- |
| Prefork model | Master forks N children; each accepts on shared listener (SO_REUSEPORT patterns) |
| Broken by default | process-local maps, memory sessions, in-process rate limiters, singleton schedulers |
| Security angles | unexpected multiple priv contexts; secret loaded N times; weaker isolation assumptions |
| Ops | metrics per PID; tracing; graceful shutdown of all children |
| Safer state | Redis/Memcached/DB for shared state; sticky external stores |

## Risk table

| Risk | Why Prefork triggers it | Mitigation |
| --- | --- | --- |
| In-memory sessions | User hits different child → session miss / auth glitches | Cookie sessions signed + external store, or disable Prefork |
| In-process rate limit | Limits are N× higher effectively | Distributed limiter (Redis) |
| CSRF/nonce stores in memory | Validation fails across processes | Shared store |
| Background worker started per child | Duplicate jobs, double charge emails | Run workers in separate deployment; gate with `fiber.IsChild()` |
| WebSocket hub in memory | Broadcast incomplete | Redis pub/sub or single-process WS service |
| File-based SQLite | Multi-process write corruption risk | External DB or one writer |
| pprof/debug on all children | Larger attack surface | Bind debug to localhost; disable in prod |
| Env secret duplication | More core dumps contain secrets | Least privilege; mem protection practices |

## Workflow

### 1. Confirm scope and success criteria

1. Record Fiber version, OS, container vs bare metal, `Prefork` setting, GOMAXPROCS, replica count.
2. Success: no process-local security controls; workers not duplicated; load test passes auth/session; shutdown drains cleanly.
3. Decide if horizontal pods already provide multi-core—Prefork may be unnecessary in K8s.

### 2. Inventory Prefork and state

```go
// Typical Fiber config to review
app := fiber.New(fiber.Config{
    Prefork: true, // focus of this skill
    // Immutable, ProxyHeader, etc.
})
```

```bash
grep -R "Prefork\|prefork\|IsChild" --include='*.go' .
grep -R "session\|RateLimiter\|memory\|gocache\|cron\|websocket" --include='*.go' . | head
```

1. List every global `map`, in-memory cache, and `sync.*` assumed process-wide.
2. List init() hooks that start goroutines/workers.

### 3. Baseline without Prefork

1. Run single-process; confirm session and rate-limit behavior.
2. Enable Prefork in staging; retest login, cart, admin CSRF, uploads.
3. Compare metrics: request rate, error rate, RSS × children.

### 4. Apply mitigations

```go
import "github.com/gofiber/fiber/v2"

func main() {
    app := fiber.New(fiber.Config{Prefork: true})

    // Only master should register cluster-wide singleton side effects
    if !fiber.IsChild() {
        // optional: migrate, one-time bootstrap — still prefer external job runners
    }

    // Sessions: use redis storage, not memory
    // rate limit: redis storage
    // WS: separate service or redis fanout

    log.Fatal(app.Listen(":3000"))
}
```

1. **Prefer** multiple container replicas + single process each over Prefork unless you measured benefit.
2. Externalize sessions, rate limits, feature flags, and locks.
3. Guard one-shot tasks with `fiber.IsChild()` or move out of web process entirely.
4. Ensure listen address and TLS termination model still correct under Prefork (usually parent coordinates).
5. Drop privileges carefully—understand which process binds ports.

### 5. Verify with evidence

```bash
# Staging load: multiproc
# Watch process count
ps aux | grep -i '[f]iber\|your-binary'

# Login twice via load generator; ensure sticky session store works without LB stickiness
# Rate limit: N parallel IPs/users should not get N× free budget from multi-process memory limiter
```

1. Chaos: kill one child; ensure master recovers; sessions still valid via Redis.
2. Confirm scheduled email job fires once, not once per child.

### 6. Observe and harden

1. Per-process and aggregate metrics; avoid double-counting if scraping all PIDs wrong.
2. Structured logs include `pid` field.
3. Document Prefork on/off in runbook with state-store dependencies.

### 7. Hand off

1. Table of former in-memory features → external store.
2. Residual risk if Prefork kept with any local state.
3. Apply `code-quality-standards` / Go style skills for patches.

## Good / Bad

| Topic | Good | Bad |
| --- | --- | --- |
| Sessions | Redis/DB store | Memory store + Prefork |
| Workers | Separate Deployment | `go func` email sender in every child |
| K8s | 1 process/pod, scale pods | Prefork inside tiny pods + high replica |
| Rate limit | Distributed | Per-PID counter |
| Verification | Multi-request session test | “Listen works, ship it” |
| Security | Debug off; shared secrets managed | pprof public on all children |

## Output Checklist

- [ ] Fiber version and Prefork setting recorded
- [ ] Process-local state inventory complete
- [ ] Sessions/rate limits/flags externalized or Prefork off
- [ ] Singleton/worker duplication addressed
- [ ] Staging load and auth tests passed
- [ ] Metrics/logging include pid awareness
- [ ] Runbook updated
- [ ] `code-quality-standards` applied

## Rules

- Owned services only.
- Treat Prefork as a process model change, not a free performance flag.
- Security controls that live only in memory are incorrect under Prefork.
- Prefer architecture clarity (split workers) over clever `IsChild` branches when possible.
