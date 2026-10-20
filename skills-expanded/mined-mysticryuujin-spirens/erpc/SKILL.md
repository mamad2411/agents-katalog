---
name: erpc
description: eRPC — finality-aware JSON-RPC caching, hedging, failover, per-chain config tiers, and the "why cache JSON-RPC at all" story. Use when designing an RPC proxy, tuning eRPC, or deciding between self-hosted nodes + vendor fallback.
---

# eRPC (JSON-RPC proxy)

## What You Probably Got Wrong

**You cache `latest` block responses.** Don't. The latest block is
reorg-prone — cache a `latest` response, serve it to a client, and the
chain reorgs; you just served stale state. eRPC's cache policies are
**finality-aware**: only blocks past the finality threshold are cached
indefinitely; recent blocks get short TTLs or no caching at all.

**You assume JSON-RPC is uncacheable because every call is "live."**
Wrong. `eth_chainId` is constant. `eth_getTransactionByHash` for a
finalized tx is constant. `eth_getBlockByNumber(N)` for finalized N is
constant. `eth_call` at a specific block is pure. A huge fraction of
RPC traffic is reading immutable history — which is exactly the
cacheable case.

**You run one vendor and no fallback.** Vendors have outages. If your
app hard-fails when Alchemy is degraded, you didn't design for
reliability. Even a 95% Alchemy / 5% public-endpoint-fallback split
catches every Alchemy outage during the ~hour they take to recover.

**You don't distinguish retry-safe from retry-unsafe methods.** A retry
on `eth_sendRawTransaction` can submit the same tx twice if the first
actually went through but the response was dropped. eRPC knows which
methods are idempotent and which aren't — don't override that logic.

## What eRPC does

Clients hit one URL. eRPC:

1. Routes by chain ID and project to the right upstream(s).
2. Checks cache for the exact method + params + block tag. Returns hit.
3. On miss, picks a healthy upstream based on selection policy.
4. Retries on transient errors (backoff, only on retry-safe methods).
5. Optionally hedges — dispatches a second request after N ms if the
   first is slow — to the best backup.
6. Trips a circuit breaker when an upstream fails repeatedly.
7. Applies rate limit budgets so one chain/project can't starve
   another.
8. Caches the response if finality rules allow.
9. Exports metrics.

## The URL shape

```text
https://rpc.example.com/<projectId>/evm/<chainId>
# e.g.
https://rpc.example.com/main/evm/1        → Ethereum mainnet
https://rpc.example.com/main/evm/8453     → Base
https://rpc.example.com/main/evm/42161    → Arbitrum One
https://rpc.example.com/main/evm/10       → OP Mainnet
```

Projects are a scoping concept: a project has its own upstreams, its
own budgets, its own cache namespace. Use one project per logical
environment (e.g. `main`, `staging`, `internal`).

## The tiers of config, from MVP to production

| Tier      | What you add                                   | Payoff                                  |
| :-------- | :--------------------------------------------- | :-------------------------------------- |
| MVP       | Public endpoints repository                    | Boots out of the box; good for dev      |
| Node      | Your own geth/reth + lighthouse                | Low latency, no rate limits on hot data |
| Vendor    | Alchemy / QuickNode / Ankr / Infura keys       | SLA for data you can't serve locally    |
| Cache     | Redis / Postgres database for persistent cache | Survives restarts; cross-instance share |
| Hedging   | `hedge.delay: 200ms`                           | Tail-latency wins; costs 2× bandwidth   |
| Selection | `prefer-local`, score-based                    | Routing smarter than round-robin        |
| Per-chain | Finality policies for L2s (flashblocks etc.)   | Correct caching for fast-finality L2s   |
| Budgets   | Per-chain, per-upstream                        | One hot chain can't exhaust another     |

SPIRENS ships tier 1 (MVP + repository provider) with hooks for tiers
2-3 commented in `config/erpc/erpc.yaml`. Tiers 4-7 link to upstream
docs.

## Finality-aware caching — the core idea

Different block states have different cache policies:

| Block state | Default policy               | Why                                                |
| :---------- | :--------------------------- | :------------------------------------------------- |
| Finalized   | Cache forever                | Can't change per Casper FFG                        |
| Safe        | Cache with long TTL          | Very unlikely to reorg, but theoretically possible |
| Latest      | Don't cache / very short TTL | Subject to reorg                                   |
| Pending     | Never cache                  | Mempool state, changes every block                 |

For L2s with fast finality (Base preconfirmations, Optimism flashblocks,
Arbitrum sequencer), eRPC has per-chain finality policies that match
the chain's real finality model, not Ethereum's.

Configure with `caching` block in `erpc.yaml` — see
[upstream caching docs](https://docs.erpc.cloud/config/caching#cache-policies).

## Failover and retry — what gets retried

```yaml
failsafe:
  - matchMethod: "*"
    retry:
      maxAttempts: 2
      delay: 500ms
      backoffMaxDelay: 2s
    circuitBreaker:
      failureThresholdCount: 20
      failureThresholdCapacity: 100
      halfOpenAfter: 30s
```

Retry rules:

- eRPC automatically excludes non-idempotent methods
  (`eth_sendRawTransaction`, `eth_sendTransaction`) from retries.
- Backoff starts at `delay`, doubles, caps at `backoffMaxDelay`.
- Retries happen before considering the upstream failed for circuit
  breaker purposes.

Circuit breaker trips when `failureThresholdCount` out of last
`failureThresholdCapacity` requests fail. Upstream is marked unhealthy
for `halfOpenAfter` before a single probe request is allowed.

## Hedging — tail latency weapon

```yaml
failsafe:
  - matchMethod: "*"
    hedge:
      delay: 200ms
      maxCount: 1
```

If the first request hasn't returned in 200ms, dispatch a second
request to the next-best upstream. Take whichever returns first. Cancel
the loser. Costs 2× bandwidth on slow requests, but kills the P99 tail.

Only enable on read methods. Writes (`eth_sendRawTransaction`) bypass
hedging automatically.

## Rate-limit budgets

```yaml
rateLimiters:
  budgets:
    - id: vendor-strict
      rules:
        - method: "*"
          maxCount: 5
          period: 1s
    - id: vendor-generous
      rules:
        - method: "*"
          maxCount: 25
          period: 1s
```

Each upstream references a budget: `rateLimitBudget: vendor-strict`.
When the budget is exhausted, eRPC fails over to the next upstream.
Prevents a client burst from draining your Alchemy quota.

## Selection policy

With N healthy upstreams, which does eRPC pick?

- **Default: round-robin with health weighting.** Simple.
- **`prefer-local`:** local node first, fall back to vendors.
- **Score-based:** each upstream gets a rolling score based on latency
  and error rate; best score wins. Good for heterogeneous upstreams.

SPIRENS uses default selection; production stacks with real SLA needs
usually graduate to score-based.

## Observability

Prometheus metrics on `:4001/metrics` — not exposed publicly by
default. Critical metrics:

- `erpc_request_duration_seconds` — per-method latency histogram.
- `erpc_upstream_health` — per-upstream health score.
- `erpc_cache_hit_ratio` — cache effectiveness.
- `erpc_circuit_breaker_state` — per-upstream CB state.

Scrape with Prometheus, graph in Grafana. The [eRPC dashboards
repo](https://github.com/erpc/erpc) has starting points.

## The "my eRPC is slow" checklist

1. **Cache hit ratio.** If it's near-zero on methods that should cache
   (`eth_chainId`, finalized `eth_getBlockByNumber`), something's
   wrong with the cache config.
2. **Which upstream is serving?** Check per-upstream latency metrics.
   If the "slow" one wins selection, fix the policy.
3. **Is the local node healthy?** `eth_syncing` on the local upstream.
   If it's syncing, eRPC should be failing over to vendors.
4. **Budget exhausted?** Rate-limit metrics show rejections. Raise
   budget or add another vendor.
5. **Circuit breaker tripped?** CB state metric. If an upstream is
   stuck open, investigate why it keeps failing.

## Worked example: SPIRENS

Config is at [`config/erpc/erpc.yaml`](../config/erpc/erpc.yaml) —
intentionally ~150 lines (MVP). Key choices:

- One project: `main`.
- Default upstream: eRPC's `repository` provider (2,000+ chains via
  public endpoints). Zero keys required.
- Commented-in slots for a local node (`ETH_LOCAL_URL`), Alchemy,
  Ankr, Infura.
- Three budget tiers: `default`, `vendor-generous`, `vendor-strict`.
- Retry + circuit breaker applied globally.
- No Redis cache in MVP — add one from `optional/compose.redis.yml`
  and wire the eRPC `database` block to graduate.

See [`docs/07-erpc.md`](../docs/07-erpc.md) for the walk-through and
the "going further" pointers to upstream docs for tiers 4-7.

## Why eRPC over a naive "put nginx in front"

An nginx reverse proxy in front of a node gives you TLS and basic LB.
It does not give you:

- JSON-RPC awareness (can't cache by method + params).
- Finality-aware caching.
- Method-aware retry (can't skip retries on `sendRawTransaction`).
- Per-chain routing.
- Circuit breakers specific to upstream health signals.

For dev, nginx-in-front is fine. For anything serving multiple clients
or multiple chains, eRPC earns its keep.

## Upstream references

- [eRPC docs](https://docs.erpc.cloud/)
- [eRPC caching policies](https://docs.erpc.cloud/config/caching)
- [eRPC selection policies](https://docs.erpc.cloud/config/projects/selection-policies)
- [eRPC hedging](https://docs.erpc.cloud/config/failsafe/hedge)
- [eRPC providers](https://docs.erpc.cloud/config/providers)
- [eRPC monitoring](https://docs.erpc.cloud/operation/monitoring)
