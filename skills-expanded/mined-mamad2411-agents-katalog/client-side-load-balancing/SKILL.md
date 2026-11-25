---
name: client-side-load-balancing
description: >
  Design client-side load balancing for owned microservices: service discovery,
  endpoint subsets, power-of-two-choices / round-robin / weighted strategies,
  outlier detection, health awareness, and locality. Use when gRPC/Java/Envoy
  clients, or app LB libraries, pick backends without a central L4 balancer —
  complements circuit-breaker-patterns and retry-backoff-patterns.
---

# Client-Side Load Balancing

## Scope And Authorization

- **In scope:** services and clients you own; controlled load tests.
- **Out of scope:** directing abusive traffic at third-party infrastructure.
- Canary new policies; avoid sudden full-mesh storms against small backends.
- Pair with `circuit-breaker-patterns`, `retry-backoff-patterns`, and `code-quality-standards`.

## When To Use

- Clients resolve many backend addresses (xDS, DNS, Consul, K8s headless, static list).
- You need per-call distribution, zone preference, or sticky sessions with health.
- Central LB is absent/undesired (east-west mesh, gRPC thick clients).
- Tokens: client-side LB, P2C, EWMA, outlier detection, subsetting, locality, xDS.

## Do Not Use As Primary

| Need | Skill instead |
| --- | --- |
| Circuit breaker states | `circuit-breaker-patterns` |
| Retry budgets | `retry-backoff-patterns` |
| Edge/CDN load balancing | CDN/cloud LB skills |
| Cilium/network policy | `cilium-network-policy-basics` |
| Server-side kube Service only | platform networking docs |

## Strategy Cheat Sheet

| Strategy | Pros | Cons |
| --- | --- | --- |
| Round-robin | Simple | Ignores latency variance |
| Random | Simple | Same |
| Weighted RR | Capacity aware | Static weights drift |
| Least-request / P2C | Adapts to load | Needs in-flight stats |
| EWMA latency | Favors fast peers | Needs samples; cold start |
| Ring hash / maglev | Affinity | Imbalance if keys skew |
| Locality-aware | Lower RTT / egress cost | Failover complexity |

## Workflow

### 1. Confirm goals

1. Service name, discovery source, zone topology, SLO, sticky needs.
2. Success: even healthy distribution; unhealthy endpoints shed; failover works; no retry storms.
3. Rollback: previous resolver/LB policy via feature flag.

### 2. Inventory discovery + clients

```bash
# Examples
dig +short backends.service.consul SRV
kubectl get endpointslices -n app
# gRPC: service config / xDS dump per your stack
```

1. List client libraries (gRPC, Envoy sidecar, custom).
2. Note existing retries, timeouts, breakers (ordering matters).

### 3. Baseline

1. Per-endpoint QPS, p99, error rate, active connections.
2. Capture imbalance or hot-spot instances.
3. Document cold-start behavior when endpoint list changes.

### 4. Design policy

**Logical policy:**

```text
discovery: xDS or DNS (refresh interval, TTL)
subset: max_endpoints = 25 (or zone-first)
lb: P2C or least_request
health: active (optional) + passive outlier detection
outlier:
  consecutive_5xx: 5
  interval: 10s
  base_ejection_time: 30s
  max_ejection_percent: 50
locality: prefer same-zone, failover to region
panic_threshold: if healthy < 50%, use all (or fail controlled)
```

1. Combine with **timeouts** and **bounded retries** (budget per request tree).
2. Circuit breaker **per endpoint** or cluster — see `circuit-breaker-patterns`.
3. Avoid double LB (app + mesh) with conflicting subsets unless intentional.

### 5. Implement carefully

| Stack | Where policy lives |
| --- | --- |
| gRPC | service config `loadBalancingConfig`, xDS |
| Envoy / Istio | Cluster lb_policy, outlier detection |
| Java | Ribbon legacy / Spring Cloud LoadBalancer / custom |
| Go | custom picker, grpc-go balancers |

1. Ensure **connection pooling** aligns with LB (do not pin forever unless hash).
2. On endpoint removal: drain in-flight; do not send new RPCs.
3. Security: discover only trusted control plane; validate TLS to backends.

### 6. Verify

```bash
# Load test: scale one backend CPU high → P2C/EWMA shifts traffic
# Kill one pod → error rate blip then recovery; no permanent blackhole
# Metrics: requests_per_endpoint, ejected_hosts, discovery_refresh_errors
```

1. Prove unhealthy endpoint ejection and unejection.
2. Prove zone preference then failover.
3. Chaos: 50% backends down — panic threshold behavior acceptable.

### 7. Operate

1. Dashboards: distribution entropy, ejection count, discovery lag.
2. Alerts: all endpoints ejected; discovery empty; extreme imbalance.
3. Runbook: pin to static list for break-glass.

## Interaction Map

| Concern | Placement |
| --- | --- |
| Timeout | Around each attempt |
| LB pick | Each attempt / stream start |
| Retry | Next pick often different endpoint |
| Breaker | After repeated fails to peer |
| Hedging | Optional; increases load — careful |

## Good / Bad

| Topic | Good | Bad |
| --- | --- | --- |
| Discovery | Authenticated control plane | Unvalidated attacker DNS |
| Health | Outlier + readiness | Never remove dead peers |
| Retries | Budgeted across picks | Unlimited cross-all-backends |
| Affinity | Explicit hash when needed | Accidental long-lived sticky overload |
| Metrics | Per-endpoint | Only global QPS |

## Output Checklist

- [ ] Discovery source and topology documented
- [ ] LB strategy + subsetting chosen
- [ ] Outlier/health policy defined
- [ ] Timeouts/retries/breakers coordinated
- [ ] Load and chaos tests show redistribution
- [ ] Metrics/alerts live
- [ ] Break-glass static config exists
- [ ] Residual risk (herding, stampede) noted

## Rules

- Owned systems only; evidence from metrics over intuition.
- Prefer reversible policy flags.
- Focus on **client-side** balancing; edge CDN LB and pure breaker design are other skills.
