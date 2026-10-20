---
name: dns-latency-triage
description: >
  Triage high DNS latency and resolution failures on owned networks and apps: recursive vs
  authoritative path, cache TTLs, NXDOMAIN storms, split-horizon, captive resolvers, and
  application timeouts. Use when slow DNS, high resolve time, intermittent NXDOMAIN,
  dig +stats latency, kube DNS latency, or owned resolver performance — not for attacking
  public DNS infrastructure.
---

# DNS Latency Triage

## Scope And Authorization

- **In scope:** Resolvers, zones, clusters, and clients you operate.
- **Out of scope:** Flooding public resolvers; unauthorized zone transfers.
- Prefer query traces from staging and samples of production clients with approval.
- Redact internal hostnames in public postmortems if required.
- Pair with `dns-over-https-basics`, `dnssec-deployment-basics`, and app timeout skills.

## When To Use

- App p99 spikes with high DNS lookup time in APM.
- `dig` shows multi-second queries; intermittent failures.
- Kubernetes `CoreDNS` latency or timeout errors.
- After DNS provider change, DNSSEC enable, or DoH rollout.
- Distinguishing network RTT vs recursive resolution work.

## Do Not Use As Primary

| Need | Skill instead |
| --- | --- |
| DoH/DoT deployment | `dns-over-https-basics` |
| DNSSEC BOGUS/SERVFAIL | `dnssec-deployment-basics` |
| DNS rebinding defense | `dns-rebinding-defense-design` |
| Email auth records | `dmarc-spf-dkim-hardening` |
| Disk/CPU host issues | host triage skills |
| Code quality baseline | `code-quality-standards` |

## Latency components

| Segment | What you measure |
| --- | --- |
| Client → stub/recursive | Local resolver RTT |
| Recursive work | Cache miss → auth queries |
| Authoritative | Your NS response time |
| Negative cache | NXDOMAIN/TTL behavior |
| App library | Happy Eyeballs, parallel A/AAAA, timeouts |

## Workflow

### 1. Confirm scope and success criteria

1. Failing names, client sites, time window, change list.
2. Success: p99 resolve under target; root cause class documented; fix or ticket.
3. Avoid production query floods—sample carefully.

### 2. Baseline with dig/drill

```bash
dig example.com A +stats
dig @10.0.0.53 example.com A +stats   # specific recursive
dig example.com A +trace              # path to auth (use sparingly)
dig example.com AAAA +stats
# Compare cache hit vs miss: repeat dig; check Query time ms
```

1. Record: Query time, SERVER, status (NOERROR/NXDOMAIN/SERVFAIL).
2. Test both cold and warm cache.
3. From multiple networks (pod, node, laptop, region).

### 3. Split failure classes

| Symptom | Likely class |
| --- | --- |
| Fast NXDOMAIN | Name wrong / missing record |
| SERVFAIL slow | Upstream, DNSSEC, lame delegation |
| Only AAAA slow | IPv6 path broken |
| Only in cluster | CoreDNS/ndots/search domains |
| Periodic spikes | Forwarder overload, rate limit, GC |
| First query slow | Cold cache, high TTL miss path |

### 4. Application and OS factors

```bash
# Linux resolv
cat /etc/resolv.conf
# ndots:5 in K8s causes extra search expansions — measure
getent hosts api.internal
```

1. Search domains multiply queries—trim `ndots`/searches when safe.
2. Dual-stack timeouts: broken AAAA adds delay—fix IPv6 or happy eyeballs config.
3. Connection pools: resolve once vs every request; cache positive/negative appropriately.
4. Hard-coded IPs hide DNS issues—don’t “fix” latency only by hardcoding without ops plan.

### 5. Infrastructure checks

| System | Checks |
| --- | --- |
| CoreDNS | latency metrics, upstream forwarders, cache plugin, errors |
| Unbound/BIND | recursion clients, jostle, rate limits, forward zones |
| Cloud DNS | provider status, query logs, geo |
| DNSSEC | validation failures → `dnssec-deployment-basics` |
| Network | firewall to 53/tcp-udp, fragmented responses, anycast |

```bash
# K8s (authorized)
kubectl -n kube-system logs -l k8s-app=kube-dns --tail=100
kubectl -n kube-system top pod -l k8s-app=kube-dns
```

### 6. Mitigate

1. Fix broken records/delegations; lower TTL only with care during migration.
2. Scale/cache recursive; fix forwarder loops.
3. Application: timeouts, retries with jitter, cache resolved endpoints for services.
4. Split-horizon: ensure internal clients hit internal views (not hairpin public).
5. Negative caching: avoid NXDOMAIN storms for optional dependencies.

### 7. Verify and hand off

1. Re-measure dig + app p99.
2. Dashboards: resolver latency, error codes, CoreDNS cache hit ratio.
3. Document: search path, forwarders, owners.
4. Alert on resolve error rate and latency SLO.

## Good / Bad

| Topic | Good | Bad |
| --- | --- | --- |
| Measure | dig +stats multi-vantage | Single ping of 8.8.8.8 |
| K8s | Fix ndots/CoreDNS | Restart nodes only |
| IPv6 | Fix AAAA path | Ignore dual-stack delay |
| Cache | Understand TTL | TTL=0 everywhere forever |
| SERVFAIL | Check DNSSEC/upstream | Randomly flush all caches |
| Load | Sample queries | dig flood as load test on shared |

## Output Checklist

- [ ] Names, clients, window recorded
- [ ] dig stats for cache hit/miss and statuses
- [ ] Failure class identified
- [ ] Search/ndots/AAAA factors checked
- [ ] Recursive/auth infrastructure reviewed
- [ ] Mitigations applied with evidence
- [ ] App timeouts/caching reviewed
- [ ] Monitoring/alerts updated
- [ ] Owners documented
- [ ] Residual risk noted

## Rules

- Evidence over guesses; multi-vantage measurements.
- Do not DDoS resolvers while testing.
- DNS latency is often search lists or dual-stack—not only “slow ISP.”
- Owned infrastructure only.
- Hand DNSSEC and DoH specifics to neighbor skills when primary.
