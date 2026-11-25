---
name: dns-architecture
version: 1.0.0
min_mindforge_version: 10.1.1
status: stable
triggers: dns architecture, dns load balancing, dns failover, GeoDNS, TTL strategy, dns service discovery, dns-based routing, dns health check, dns propagation, anycast dns, dns caching layer, dns resolution chain
---

# Skill — DNS Architecture

## When this skill activates
Any task involving DNS-based traffic management, load balancing via DNS,
failover strategies, GeoDNS routing, service discovery using DNS,
or TTL optimization for high-availability systems.

## Mandatory actions when this skill is active

### Before writing any code
1. Map the DNS resolution chain (client → resolver → authoritative → response).
2. Identify failover requirements (RTO target determines TTL).
3. Decide routing strategy (round-robin, weighted, latency, geo, failover).
4. Determine health check mechanism for DNS-managed endpoints.

### During implementation
- Set TTL appropriate to failover speed requirements.
- Implement health checks for all DNS-managed endpoints.
- Use anycast for latency-critical global services.
- Configure both primary and secondary DNS providers for resilience.
- Document propagation delays for operational runbooks.
- Never rely on DNS as sole load balancer for sub-second failover.

### After implementation
- Verify health checks remove unhealthy endpoints within TTL window.
- Test failover scenario end-to-end (kill primary, measure recovery time).
- Confirm GeoDNS routes correctly from each target region.
- Monitor DNS resolution latency and error rates.
- Validate TTL behavior in major resolvers (Google, Cloudflare, ISP).

## DNS Load Balancing

### Strategies
| Strategy | How It Works | Best For |
|----------|-------------|----------|
| Round-robin | Rotate through A records | Simple distribution |
| Weighted | Assign weight per endpoint | Canary, capacity differences |
| Latency-based | Route to lowest-latency endpoint | Global services |
| Failover | Primary/secondary with health check | HA with clear primary |
| Geo | Route by resolver geography | Data sovereignty, latency |

### Limitations
- DNS caching means changes take TTL seconds to propagate.
- Client-side caching may ignore TTL (some browsers cache 60s minimum).
- Cannot do sub-second failover via DNS alone.
- Resolver location != user location (use EDNS Client Subnet to improve).

## GeoDNS

### How It Works
1. DNS query arrives at authoritative server.
2. Server determines resolver's geographic location (via IP geolocation).
3. Returns IP address of nearest datacenter.
4. EDNS Client Subnet (ECS) improves accuracy by passing client subnet.

### Configuration
```
# Example GeoDNS policy
api.example.com:
  default: us-east-1.api.example.com
  EU: eu-west-1.api.example.com
  APAC: ap-southeast-1.api.example.com
  fallback: us-east-1.api.example.com  # if region unhealthy
```

### Considerations
- Resolver location != user location (corporate DNS, VPN users).
- ECS support improves accuracy but not universally supported.
- Always have fallback for unresolvable regions.
- Test from each target region to verify correct routing.

## TTL Strategy

### TTL Decision Framework
| Scenario | Recommended TTL | Reason |
|----------|----------------|--------|
| Fast failover needed | 30-60 seconds | Quick removal of unhealthy |
| Normal operation | 300 seconds (5 min) | Balance between freshness and cache |
| Static content CDN | 3600 seconds (1 hour) | Rarely changes, maximize cache |
| During migration | 60 seconds | Prepare for cutover |
| After migration stable | 300-3600 seconds | Return to normal caching |

### TTL Trade-offs
- **Low TTL (30s)**: Fast failover, more DNS queries, higher authoritative load.
- **High TTL (3600s)**: Fewer queries, better cache hit rate, slow failover.
- **Strategy**: Lower TTL before planned changes, raise after stability confirmed.

### Propagation Reality
- TTL expiry != instant propagation.
- Some resolvers enforce minimum TTL (30s-60s).
- Browser DNS cache may ignore TTL entirely.
- Java apps cache DNS indefinitely by default (set `networkaddress.cache.ttl`).

## Service Discovery via DNS

### Internal Service Discovery
- Use internal DNS zone (e.g., `service.internal`).
- SRV records provide port discovery alongside host.
- Short TTL (5-15s) for dynamic service registration.

### SRV Records
```
_http._tcp.api.internal. 15 IN SRV 10 100 8080 api-pod-1.internal.
_http._tcp.api.internal. 15 IN SRV 10 100 8080 api-pod-2.internal.
```

### Kubernetes DNS
- Service discovery built-in: `service-name.namespace.svc.cluster.local`.
- Headless services return individual pod IPs.
- ExternalName services alias external endpoints.

## Anycast DNS

### How It Works
- Multiple servers advertise the same IP address via BGP.
- Network routes traffic to the nearest server (by BGP path).
- If one server goes down, BGP re-routes to next nearest.

### Use Cases
- Authoritative DNS servers (Cloudflare, Route53).
- CDN edge nodes.
- DDoS mitigation (absorb attack across multiple PoPs).

### Considerations
- Failover speed depends on BGP convergence (seconds to minutes).
- TCP connections break on route change (DNS is UDP, so usually fine).
- Not suitable for stateful protocols without session persistence.

## Health Checks

### DNS Health Check Pattern
1. Health checker probes endpoints at regular intervals (10-30s).
2. If endpoint fails N consecutive checks, remove from DNS response.
3. Continue probing. If endpoint recovers, add back after M consecutive successes.
4. Removal takes effect within TTL seconds (resolver cache expiry).

### Health Check Types
| Type | Checks | Use For |
|------|--------|---------|
| TCP | Port open | Basic availability |
| HTTP | Status 200 + body match | Application health |
| HTTPS | Valid cert + status | Full stack health |
| Custom | Business logic probe | Application-specific |

### Timing
- Check interval: 10-30 seconds.
- Failure threshold: 2-3 consecutive failures.
- Recovery threshold: 2-3 consecutive successes.
- Effective failover time: check_interval × failure_threshold + TTL.

## Self-check
- [ ] TTL set appropriate to failover speed requirement.
- [ ] Health checks configured for all DNS-managed endpoints.
- [ ] Failover tested end-to-end (measured recovery time).
- [ ] GeoDNS verified from target regions.
- [ ] Secondary DNS provider configured for resilience.
- [ ] Propagation delays documented in runbook.
- [ ] Client-side DNS caching behavior accounted for.
- [ ] Monitoring in place for resolution latency and errors.
