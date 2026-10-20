---
name: api-gateway-rate-limiting-and-quota-management
description: >
  Designs rate-limiting and quota strategy that applies across gateway
  tools — token bucket vs. sliding/fixed window algorithm choice,
  per-client vs. global vs. tiered limit scoping, burst allowance
  design, and distributed counter consistency — as the vendor-neutral
  layer underneath tool-specific plugins like Kong's `rate-limiting` or
  Apigee's `Quota`/`SpikeArrest`. Use when a user asks to "design a
  rate-limiting strategy," "choose between token bucket and sliding
  window," "set per-client vs. global API limits," "size a burst
  allowance," "why is my distributed rate limit inconsistent across
  nodes," or "protect a backend from one noisy client without punishing
  everyone else."
license: Apache-2.0
compatibility: "Claude Code, GitHub Copilot, OpenAI Codex, Cursor, Gemini CLI"
metadata:
  domain: service-mesh-and-api-gateway
  maturity: stable
---

# API Gateway Rate-Limiting and Quota Management

## Purpose

Every gateway tool exposes a rate-limiting plugin, but the plugin
configuration is downstream of decisions that are the same regardless
of which tool implements them: which algorithm actually matches the
traffic pattern being protected against, whether the limit should be
scoped per-client, per-API-key-tier, or globally, how large a burst
allowance is safe versus how much it just delays the same overload, and
how (or whether) the counter is kept consistent across multiple gateway
nodes. Getting these wrong produces two opposite failures that are
equally bad: a limit so tight it throttles legitimate traffic and gets
"temporarily" raised during an incident until it's effectively
meaningless, or a limit so loose (or inconsistently enforced across
nodes) that it fails to protect the backend it was meant to protect at
all. This skill covers that vendor-neutral strategy layer — the
tool-specific plugin mechanics for applying it live in
[kong-api-gateway-configuration](../kong-api-gateway-configuration/SKILL.md)
and
[apigee-api-management-and-governance](../apigee-api-management-and-governance/SKILL.md).

## When to use

- Designing a new rate-limiting or quota policy for an API, before
  picking a specific gateway plugin's configuration fields.
- Choosing between token bucket, leaky bucket, fixed-window, and
  sliding-window algorithms for a specific traffic pattern (bursty vs.
  steady, per-second protection vs. monthly allowance).
- Deciding whether a limit should be enforced per-client (API key,
  consumer, IP), per-tier (free/paid/partner), or globally across all
  callers to protect a shared backend.
- Sizing a burst allowance so short, legitimate spikes aren't rejected
  while sustained abuse still is.
- Diagnosing why a configured limit is inconsistently enforced across a
  multi-node gateway deployment (some requests over the limit succeed
  when they shouldn't).
- Distinguishing rate-limiting (protecting against short-term burst/
  abuse) from quota management (a longer-window total allowance, often
  tied to billing/tiering) when a single policy is being asked to do
  both jobs.

## Prerequisites & environment

- Clarity on what's actually being protected: a shared, resource-
  limited backend (rate-limiting's job — bound request rate to what the
  backend can handle) versus a business/contractual allowance (quota's
  job — bound total consumption over a longer period, often tied to a
  pricing tier). Conflating the two produces a policy that's tuned
  wrong for at least one of them.
- A real traffic profile (request-rate percentiles, burst frequency,
  per-client distribution) for the API being protected — sizing a limit
  from a guess rather than observed traffic is the most common cause of
  a limit that's wrong in either direction.
- A shared, low-latency counter store (Redis or equivalent) reachable
  from every gateway node, if the gateway is deployed with more than
  one node — an in-memory/per-node counter cannot enforce a
  cluster-wide limit correctly, regardless of which gateway tool is
  used.
- Visibility into 429/`RESOURCE_EXHAUSTED` response rates per client/
  tier after a policy ships, so an overly tight or overly loose limit
  is discoverable from data rather than only from a support escalation.

## Step-by-step guidance

1. **Decide whether you're rate-limiting or quota-managing — or both,
   as separate policies** — before picking an algorithm:
   - **Rate-limiting** bounds request *rate* over a short window
     (per-second/per-minute) to protect a backend's real-time capacity.
   - **Quota management** bounds total *consumption* over a long window
     (per-day/per-month), typically tied to a pricing tier or fair-use
     policy, independent of how bursty the traffic was within that
     window.
   A backend can be protected from a burst (rate-limiting) while a
   consumer is still well within their monthly allowance (quota) —
   these are not substitutes for each other, and a single policy
   covering only one leaves the other failure mode unprotected. This is
   exactly why Apigee ships `SpikeArrest` and `Quota` as separate
   policies (see
   [apigee-api-management-and-governance](../apigee-api-management-and-governance/SKILL.md))
   rather than one combined mechanism.

2. **Choose an algorithm based on the traffic pattern, not habit:**
   - **Token bucket**: tokens refill continuously at a fixed rate up to
     a capped bucket size; allows a burst up to the bucket size, then
     throttles to the refill rate. Good default for APIs with naturally
     bursty legitimate traffic (a client fetching a page of results
     then going idle) where you want to permit the burst but cap
     sustained rate.
   - **Leaky bucket**: requests are processed at a strictly constant
     output rate regardless of arrival burstiness (excess queues or is
     dropped). Better when the backend needs a smooth, constant
     request rate and bursty forwarding would itself cause problems
     (e.g. a downstream system with no burst tolerance of its own).
   - **Fixed window** (e.g. "100 requests per calendar minute"): simplest
     to implement and reason about, but allows up to 2x the intended
     rate at a window boundary (100 requests in the last second of one
     window plus 100 in the first second of the next).
   - **Sliding window** (or sliding-window-log/counter): approximates a
     true rolling rate limit, avoiding the boundary-doubling problem of
     fixed windows at the cost of slightly more implementation/storage
     complexity.
   For most externally-facing APIs, a token-bucket or sliding-window
   approach is worth the modest extra complexity over fixed-window,
   specifically because fixed-window's boundary behavior is exploitable
   by anyone who notices the pattern.

3. **Scope the limit at the right level deliberately:**
   - **Per-client** (API key, authenticated consumer, or IP as a
     fallback for unauthenticated traffic): the default choice for
     protecting against one noisy/abusive caller from affecting others.
   - **Per-tier** (free/paid/partner): different limits for different
     consumer classes of the same API, usually layered on top of (not
     instead of) a per-client limit.
   - **Global** (across all callers combined): protects the backend's
     absolute capacity regardless of how many distinct clients there
     are — necessary in addition to per-client limits when enough
     well-behaved clients calling near their individual limits could
     still collectively overwhelm the backend.
   A per-client-only limit with no global ceiling can still let the
   backend be overwhelmed by simple client-count growth; a global-only
   limit lets one abusive client consume the entire shared allowance and
   starve every other legitimate caller. Most production APIs need
   both, not one or the other.

4. **Size the burst allowance from observed traffic, not intuition.**
   Pull real percentile data (p50/p95/p99 request rate per client over
   short windows) and set the bucket/burst size to comfortably cover
   legitimate p99 burst behavior, with the sustained/refill rate set to
   the backend's real sustained capacity:
   ```
   Observed: typical client bursts to ~40 req/s for 2-3s during a page
   load, then idles; sustained backend capacity: 500 req/s total.

   Token bucket per client: bucket size 50 (covers the p99 burst),
   refill rate 10 req/s (bounds sustained abuse without punishing the
   normal burst-then-idle pattern).
   ```
   A burst allowance sized purely as "whatever number stops complaints"
   without reference to real traffic data tends to ratchet upward over
   time as each complaint is resolved by raising it, until it no longer
   protects anything.

5. **Use a shared, distributed counter for any multi-node gateway
   deployment** — this is the single most common way a "correctly
   designed" limit fails in practice:
   ```
   3 gateway nodes, each with an in-memory (local) counter,
   configured limit: 100 req/min per client
   → actual enforced limit: up to 300 req/min per client
     (100 independently on each node a client's requests happen to hit)
   ```
   Back the counter with Redis (or the gateway's cluster-aware counting
   mode) so all nodes enforce against the same count. See
   [kong-configuration-validation](../kong-configuration-validation/SKILL.md)
   and
   [kong-api-gateway-configuration](../kong-api-gateway-configuration/SKILL.md)
   for the concrete `policy: redis` configuration this maps to in one
   specific tool.

6. **Return a response that lets well-behaved clients self-correct**,
   not just a bare rejection:
   ```
   HTTP/1.1 429 Too Many Requests
   Retry-After: 12
   X-RateLimit-Limit: 100
   X-RateLimit-Remaining: 0
   X-RateLimit-Reset: 1795891200
   ```
   A `Retry-After` header (or the gRPC-equivalent status detail) lets a
   well-implemented client back off correctly instead of immediately
   retrying and compounding the overload — and its absence is a common,
   easily-fixed reason a rate limit doesn't actually reduce load the
   way intended.

7. **Monitor 429/`RESOURCE_EXHAUSTED` rate per client/tier after
   shipping**, treating a sustained high rejection rate for a specific
   client as a signal to investigate (is this abuse, or a legitimate
   traffic pattern the limit was sized wrong for?) rather than either
   ignoring it or reflexively raising the limit:
   ```bash
   # example query against a metrics/logging backend
   sum(rate(gateway_requests_total{status="429"}[5m])) by (consumer)
   ```
   A single client consistently hitting 429 might be legitimately
   under-provisioned for their tier (a business conversation, possibly
   a tier upgrade) or might be misbehaving (a retry loop with no
   backoff) — the fix differs, so don't default to "just raise the
   limit" without checking which case it is.

8. **Re-validate limits after any significant backend capacity
   change**, since a rate limit sized to protect a specific backend
   capacity becomes wrong (too tight or, more dangerously, too loose)
   the moment that capacity changes and nobody revisits the limit.

## Best practices

- Always separate rate-limiting (short-window, protects real-time
  capacity) from quota management (long-window, protects a
  business/fair-use allowance) as distinct policies, even when one
  gateway plugin technically could enforce both — conflating them
  tends to leave one dimension unprotected.
- Default to token bucket or sliding window over fixed window for
  anything externally-facing — fixed window's boundary-doubling
  behavior is a known, exploitable gap.
- Layer per-client and global limits together rather than choosing one;
  each protects against a failure mode the other doesn't.
- Size burst allowances from observed traffic percentiles, and treat
  any later "just raise it" request as a signal to re-examine the
  underlying traffic pattern, not a routine config tweak to rubber-stamp.
- Always back a rate limiter with a distributed counter (Redis or
  equivalent) on any multi-node gateway — a per-node counter silently
  multiplies the effective limit by node count, defeating the whole
  point of setting one.
- Return `Retry-After` and remaining-quota headers on every throttled
  response so well-behaved clients can back off correctly instead of
  hammering the gateway harder.
- Monitor rejection rate per client/tier continuously, and investigate
  before adjusting — a limit raised reactively during every incident
  eventually protects nothing.

## Common pitfalls

- **Symptom:** A configured "100 requests/minute per client" limit
  clearly allows more than 100/minute in production, confirmed by
  request logs.
  **Fix:** The gateway is very likely running multiple nodes with a
  per-node (local/in-memory) counter instead of a shared one — the true
  enforced limit is close to `100 * node_count`. Switch to a
  Redis-backed (or equivalent cluster-aware) counting policy so every
  node enforces against the same count.

- **Symptom:** A rate limit sized from "round numbers that seemed
  reasonable" either constantly throttles normal usage (frequent
  support complaints) or never triggers at all even during a known
  abuse incident.
  **Fix:** The limit wasn't sized from real observed traffic. Pull
  actual p95/p99 per-client request-rate data and re-derive the
  burst/refill (or window) size from it, rather than guessing and then
  reactively adjusting after each complaint.

- **Symptom:** A fixed-window rate limit is bypassed by a client
  sending a burst right at the window boundary — twice the intended
  rate gets through in a one-second span spanning two windows.
  **Fix:** This is fixed window's known structural weakness, not a
  configuration bug. Move to a sliding-window or token-bucket
  implementation, which doesn't have a hard reset boundary an informed
  client can time against.

- **Symptom:** During a traffic spike, an on-call engineer doubles or
  removes the rate limit for the affected client "to stop the 429s,"
  the incident resolves, and the change is never reverted.
  **Fix:** This is a real, standing risk once left in place — the limit
  no longer protects the backend from that client (or anyone using the
  same raised ceiling) going forward. Treat any incident-time limit
  change as temporary and explicitly tracked for revert, and once the
  incident is over, investigate whether the real fix is a legitimate
  tier increase (a deliberate, reviewed change) or addressing an actual
  misbehaving client (a retry loop, a missing cache) rather than leaving
  the emergency value in place by default.

- **Symptom:** A quota (long-window, e.g. monthly) is correctly
  enforced and a client is well within it, but the same client's
  traffic still occasionally degrades the shared backend.
  **Fix:** Quota and rate-limiting solve different problems — a client
  can be far under a monthly quota while still sending a short burst
  the backend can't absorb in real time. Add a separate short-window
  rate-limit (or burst-aware token-bucket policy) alongside the
  existing quota rather than assuming the quota alone provides burst
  protection.

## Worked example

**Scenario:** `payments-api` is called by many partner clients through
a 3-node gateway cluster. Observed traffic: typical client bursts to
~15 req/s for a few seconds during checkout completion, then idles;
overall backend sustained capacity is 300 req/s across all clients
combined. Partner contracts also specify a 500,000-request monthly
allowance per partner.

Design:
- **Rate-limiting (per-client, short window):** token bucket, bucket
  size 20 (covers observed p99 burst with margin), refill rate 5 req/s
  per client — bounds any single client's sustained rate without
  rejecting the normal checkout-completion burst.
- **Rate-limiting (global):** a second, backend-wide token bucket
  capped at 300 req/s total, refill rate matching real sustained
  backend capacity — protects against the case where enough clients
  near their individual limits collectively exceed backend capacity.
- **Quota (per-client, long window):** 500,000 requests/month, enforced
  independently of the rate-limit buckets, tied to the partner's
  contractual tier.
- **Distributed counters:** both rate-limit buckets and the quota
  counter backed by a shared Redis instance reachable from all 3
  gateway nodes — not per-node in-memory counters.
- **Client-facing behavior:** every throttled response
  (rate-limit or quota) returns `429`/`Retry-After` plus
  `X-RateLimit-Remaining`/quota-remaining headers so partner clients can
  observe how close they are to either limit and back off accordingly.

Monitoring: a dashboard tracking 429 rate per partner and per limit type
(rate-limit vs. quota) separately, so a partner hitting their monthly
quota (a contract conversation) is distinguishable at a glance from a
partner triggering the per-second rate-limit (likely a retry loop or a
genuine burst that needs investigating), rather than both showing up as
an undifferentiated "429 spike."

The concrete plugin configuration implementing this design in Kong is
covered in
[kong-api-gateway-configuration](../kong-api-gateway-configuration/SKILL.md);
the equivalent `Quota`/`SpikeArrest` policy pairing in Apigee is covered
in
[apigee-api-management-and-governance](../apigee-api-management-and-governance/SKILL.md).

## Cross-references

- [kong-api-gateway-configuration](../kong-api-gateway-configuration/SKILL.md) — the concrete `rate-limiting` plugin configuration (including the `redis`/`cluster` counter policy) implementing this strategy in Kong.
- [apigee-api-management-and-governance](../apigee-api-management-and-governance/SKILL.md) — the `Quota`/`SpikeArrest` policy pairing implementing rate-limiting vs. quota management separately in Apigee, plus how quota ties into monetization tiers.
- [service-mesh-istio](../../../kubernetes-platform/skills/service-mesh-istio/SKILL.md) — mesh-level local/global rate limiting (Envoy rate-limit filters via `EnvoyFilter`) as an alternative enforcement point for east-west traffic, versus enforcing at the north-south gateway edge covered here.
