---
name: rate-limiter
description: Design a distributed rate limiter at scale, policy model, enforcement layers (edge/gateway/service), algorithms (token bucket, sliding window), hot keys, fail-open vs fail-closed, multi-region, shadow mode. Topic playbook from the System Design series EP (Rate Limit #2). Use when the system is a rate limiter, throttle, quota enforcer, or abuse/cost guard. Sensors and evals gate.
user_invocable: true
---

Design a distributed rate limiter. Topic playbook. The agent loads this reference and adapts it to the
user's real scale, policy, and latency budget, then emits the SDD via the generic template.

Use when the problem is: rate limiting, throttling, quota/budget enforcement, abuse protection, or
cost control in front of an expensive dependency (LLM, search, third-party API).

Ask once if missing: enforcement point (edge / gateway / in-service / layered), the limit key
(user / token / IP / tenant / endpoint), hard vs soft limit, fail-open or fail-closed, single vs
multi-region, accuracy tolerance.

Read:
- guides/design-method.md
- guides/writing-style.md
- guides/templates/system-design.md
- guides/pipeline.md

Generate the SDD using the template, filled with the reference below, adapted to user scale.

Save to .claude/runtime/outputs/architect/design/{feature_id}.md.
Sensors: sensors/design-structure.md, sensors/design-rigor.md. Evals: evals/design-quality.md.

---

## Reference architecture (adapt, do not copy blindly)

One line: rate limiting is not "a counter with TTL in Redis". That solves part of it. The real design
starts from policy, not storage. The organizing question, asked first: **what exactly am I protecting,
and how much imprecision do I accept to protect it without destroying latency and simplicity?** That
one question drives almost every decision.

### Why it exists (five goals at once)

1. Protect finite capacity of a system.
2. Fairness between clients, tenants, users.
3. Reduce blast radius (a client in a loop, a deploy generating anomalous traffic).
4. Sustain commercial models (free / pro / enterprise plans).
5. Control cost (services that call expensive dependencies: LLM, search, third parties).

A good design is a set of **overlapping limits** (global, tenant, user, endpoint, IP security), not a
single counter. Policy first, Redis second.

### Where to enforce (defense in depth)

| Layer | Good for | Limit |
|---|---|---|
| Edge / CDN | absorb volumetric abuse, L7 DDoS, block early | coarse, lacks rich business context |
| API Gateway | most common place; per token/user/tenant/endpoint | generic API limits; if it becomes a bottleneck the whole platform feels it |
| Inside the service | limit depends on domain context the gateway lacks (expensive report, LLM inference) | semantic / cost limits |

Mature architecture is layered: edge for coarse protection, gateway for generic API limits, service
for semantic/cost limits. Each layer catches what the layer above cannot see.

### The limit key

Pick the dimension(s) consciously: user, token, IP, tenant, endpoint, method, region, often a
composite. The key choice sets cardinality (and therefore hot-key risk and store load) and the abuse
surface. Composite keys (tenant+endpoint) localize limits but multiply key count.

### Algorithms

| Algorithm | Behavior | Trade-off |
|---|---|---|
| Fixed window counter | count per fixed bucket, reset at boundary | cheap and simple; **boundary burst** allows ~2x at the window edge |
| Sliding window counter | weight current + previous fixed buckets by elapsed fraction | smooths the boundary; small approximation; one atomic op |
| Sliding log | timestamp per request, exact count in window | exact and fair; memory and cost grow with traffic |
| Leaky bucket | constant drain rate, queue smooths bursts | shapes a steady output rate |
| **Token bucket** | tokens refill at a sustained rate, bucket cap allows burst | **industry default for platforms**: separates allowed burst from sustained rate |

Default recommendation: **token bucket** when you want a sustained rate plus a controlled burst;
**sliding window counter** when you want a simple, near-exact rolling limit with a sub-ms check. Make
the check atomic (a Lua script in Redis) so read-decide-write is one round trip and races vanish.

### State and storage

- Per-key counter/bucket in an in-memory store (Redis), TTL-bounded (e.g. 2 windows) so cold keys
  expire and memory stays bounded.
- Atomic decision: single Lua script does refill/weight + check + decrement in one op.
- Limit config (key -> quota/refill) in a config service with a short local cache, hot-reloadable
  without redeploy. (See [[good-system-design-example]] for the filled rate-limiter SDD shape.)

### Hot keys

One tenant with disproportionate traffic concentrates load on one store shard. Mitigations:
- **Local budgets**: each node is granted a slice of the global budget and decrements locally,
  reducing central-store pressure; reconcile periodically.
- **Composite limits** to spread a tenant across sub-keys.
- Local pre-check / token pre-filter before the central call, so a saturating key is throttled at the
  node before it hits the shared store.
- Sharding the store by key (consistent hashing) so one key's ops stay on one shard.

### Fail-open vs fail-closed

When the rate-limit store fails, decide deliberately. **Fail-open** (allow) protects legit traffic
from your own outage but drops protection. **Fail-closed** (deny) preserves protection but turns a
limiter outage into an availability incident. Most platforms fail open on the generic path and
fail closed only where the limit guards a hard capacity or cost ceiling. State which, and why, per
layer. Pair with a circuit breaker so a slow store does not add latency to every request.

### Multi-region

Strict global accuracy across regions costs a synchronous cross-region hop on every request, which
kills latency. The realistic compromise is **regional budgets with reconciliation**: each region
enforces a local share of the global limit and reconciles asynchronously. Accept bounded over-admit
for low latency. Reserve strict global counting for the few limits that truly need it.

### Shadow mode

Before enforcing a hard limit, run it in **observation mode**: the system computes the block decision
but does not apply it, and emits what it would have blocked. This catches misconfigured policies
before they cause an incident. Promote a limit from shadow to enforce only after the shadow metrics
look right. This is the single highest-leverage operational practice here.

### Hard vs soft

Hard limit rejects (429 + Retry-After). Soft limit warns, degrades, or queues but still serves. Cost
and fairness limits are often soft with escalating friction; security and capacity limits are hard.

### Observability

Essential metrics: requests allowed per policy, requests blocked (429) per policy and dimension,
decision latency (the limiter must add near-zero to the request path), store op latency, fail-open
events, top-throttled keys, shadow-mode would-block counts. At 3am someone must answer: which limit
fired, in which dimension, was the policy wrong, was there a traffic regression. If the design cannot
answer that, it is not operationally governable.

### Failure modes

- Store down -> chosen posture (fail-open default) + local fallback budget + circuit breaker + alert.
- Hot key saturates a shard -> local pre-filter + composite keys + local budgets.
- Bad policy pushed -> shadow mode first; fast rollback of config; per-policy block-rate alert.
- Gateway limiter becomes the bottleneck -> push coarse limits to edge, keep the gateway check O(1).

### Incremental plan

1. Vertical slice: one enforcement layer (gateway), fixed or sliding window, single Redis, one limit
   key, 429 + Retry-After, allow/deny metrics.
2. Correctness/ops: token bucket via atomic Lua, fail-open + circuit breaker, shadow mode, hot-reload
   config, per-policy metrics.
3. Scale: sharded store, hot-key local budgets + pre-filter, layered enforcement (edge/gateway/service).
4. Global: regional budgets with reconciliation, composite policies, cost/LLM semantic limits in-service.

### Trade-offs to state explicitly

accuracy vs latency (exact global count vs local budget); fail-open vs fail-closed; central store vs
local budgets; one limit key vs composite; enforce now vs shadow first; per-layer placement (catch
early at edge vs rich context in service).

<!-- canon: Kleppmann (consistency vs latency, accept bounded imprecision), Nygard (circuit breaker, bulkhead, fail-open as a stability decision), Vogels (design for failure, the store will fail), Helland (local budgets = data on the outside reconciled async) -->
