# Skill: Load Balancer Selector (`lb_selector`)

Decision matrix and selection guide for choosing the right load balancer across Azure, AWS, and GCP based on traffic pattern, protocol layer, scope, and feature requirements.

---

## Decision Inputs

Before recommending a load balancer, gather these five inputs:

| Input | Options | Why It Matters |
|---|---|---|
| **Protocol layer** | L4 (TCP/UDP) vs L7 (HTTP/HTTPS/gRPC) | Determines whether you need content-based routing, header inspection, or raw pass-through |
| **Traffic direction** | Public (internet-facing) vs Private (internal) | Affects SKU choice, IP allocation, and security posture |
| **Scope** | Regional vs Global (multi-region) | Global requires DNS-based or anycast-based distribution |
| **Special features** | WAF, WebSocket, gRPC, static IP, PrivateLink, mutual TLS | Eliminates options that lack required capabilities |
| **Cost sensitivity** | Low-traffic dev/test vs high-throughput production | Some products charge per rule, per connection, or per capacity unit |

---

## Azure Decision Tree

```
Is the traffic HTTP/HTTPS (L7)?
├── YES → Is it global (multi-region)?
│   ├── YES → Azure Front Door (Standard/Premium)
│   │         • Premium if you need Private Link origins or Bot Manager
│   │         • Standard for CDN + basic WAF
│   └── NO → Is WAF required?
│       ├── YES → Application Gateway v2 with WAF_v2 policy
│       └── NO → Application Gateway v2 (Standard_v2)
└── NO (L4 TCP/UDP) → Is it global?
    ├── YES → Is DNS-based steering acceptable?
    │   ├── YES → Traffic Manager (DNS steering only: priority/weighted/geographic/performance)
    │   └── NO → Azure Standard Load Balancer Global tier for cross-region TCP/UDP
    │             (verify current Global tier capabilities: https://learn.microsoft.com/azure/load-balancer/cross-region-overview)
    └── NO → Azure Load Balancer Standard
              • Use HA Ports rule for NVA/firewall scenarios
              • Use outbound rules for SNAT control
```

**Key Azure constraints:**
- Azure LB Basic is being retired — always recommend Standard.
- Application Gateway v1 is retired; direct users to Application Gateway v2 migration and verify current retirement guidance: https://learn.microsoft.com/azure/application-gateway/v1-retirement.
- Traffic Manager is DNS-only (no inline proxy) — clients connect directly to the endpoint. TTL-based failover is slower than proxy-based.
- Azure Front Door is L7 HTTP/HTTPS/CDN, not an L4 TCP/UDP proxy. For global L4, use Standard Load Balancer Global tier; verify current capabilities: https://learn.microsoft.com/azure/load-balancer/cross-region-overview.
- Front Door Classic is deprecated — use Standard/Premium for HTTP(S).

---

## AWS Decision Tree

```
Is the traffic HTTP/HTTPS (L7)?
├── YES → Application Load Balancer (ALB)
│         • Content-based routing (path, host, header, query string)
│         • gRPC support, Lambda targets, weighted target groups
│         • Integrates with WAF v2 and Cognito
│         • No static IP (use Global Accelerator or NLB → ALB for static IPs)
└── NO (L4 TCP/UDP/TLS) → Do you need inline appliance inspection?
    ├── YES → Gateway Load Balancer (GLB)
    │         • GENEVE encapsulation for transparent firewalls/IDS
    │         • Chained to ALB/NLB via GLB endpoint
    └── NO → Network Load Balancer (NLB)
              • Ultra-low latency, millions of RPS
              • Static IPs (one per AZ) or Elastic IPs
              • TLS termination supported
              • PrivateLink provider endpoint
              • Cross-zone LB is opt-in (has cost implications)
```

**For global distribution (multi-region):**
- **L7**: CloudFront (CDN + Lambda@Edge) or ALB with Route 53 latency-based routing.
- **L4**: AWS Global Accelerator (anycast IPs → regional NLB/ALB endpoints).

**Key AWS constraints:**
- ALB does not have static IPs natively — use NLB in front of ALB or Global Accelerator.
- Classic Load Balancer (CLB) is legacy — migrate to ALB or NLB.
- GLB is for inspection appliances only — not a general-purpose LB.
- NLB cross-zone load balancing has per-GB data charges when enabled.

---

## GCP Decision Tree

```
Is the traffic HTTP/HTTPS (L7)?
├── YES → Is it external (internet-facing)?
│   ├── YES → Is global scope needed?
│   │   ├── YES → Global external Application Load Balancer (legacy: External HTTP(S) LB)
│   │   │         • Anycast VIP, Cloud Armor (WAF), Cloud CDN
│   │   │         • Supports managed SSL certificates
│   │   └── NO → Regional external Application Load Balancer
│   │             • Data residency / sovereignty requirements
│   └── NO (internal) → Internal Application Load Balancer
│                        • Regional, for internal microservices
│                        • Envoy-based, supports traffic splitting
└── NO (L4 TCP/UDP) → Is it external?
    ├── YES → External passthrough Network Load Balancer (regional) or external proxy Network Load Balancer where proxy features are required
    │         • Verify current scope and protocol support: https://cloud.google.com/load-balancing/docs/load-balancing-overview
    └── NO → Internal passthrough Network Load Balancer
              • Regional, for internal databases/services
              • Supports failover groups
```

**Key GCP constraints:**
- Verify current GCP Cloud Load Balancing product names, scope, and Network Service Tier constraints in the official overview: https://cloud.google.com/load-balancing/docs/load-balancing-overview.
- Internal Application Load Balancer is Envoy-based (proxy) — account for proxy behavior in latency-sensitive designs.
- Cloud CDN only works with supported external Application Load Balancer/backend bucket patterns; verify current supported backends in GCP docs.

---

## Cross-Cloud Comparison Table

| Feature | Azure | AWS | GCP |
|---|---|---|---|
| **L7 regional** | Application Gateway v2 | ALB | Regional external/internal Application Load Balancer |
| **L7 global** | Front Door Standard/Premium | CloudFront + ALB | Global external Application Load Balancer |
| **L4 regional** | Load Balancer Standard | NLB | External/internal passthrough Network Load Balancer |
| **L4 global** | Standard Load Balancer Global tier | Global Accelerator + NLB | External proxy Network Load Balancer (verify protocol support) |
| **DNS-based global** | Traffic Manager | Route 53 routing policies | Cloud DNS routing policies |
| **WAF** | Front Door WAF / AppGW WAF_v2 | AWS WAF v2 (on ALB/CF) | Cloud Armor (on Application Load Balancer) |
| **Static IP** | LB Standard, AppGW v2 | NLB (per AZ EIP) | External passthrough/proxy Network Load Balancer |
| **WebSocket** | AppGW v2, Front Door | ALB | Application Load Balancer |
| **gRPC** | Verify current AppGW v2 support | ALB | Application Load Balancer |
| **PrivateLink provider** | Private Link Service + Std LB | NLB (PrivateLink) | Internal LB + Service Attachment |
| **mTLS** | AppGW v2 | ALB | HTTP(S) LB |
| **Free tier / low cost** | LB Standard (rule-based pricing) | ALB (LCU pricing) | Forwarding-rule pricing |

---

## Common Selection Mistakes

1. **Using L7 when L4 is sufficient** — L7 LBs add latency and cost. If you don't need content-based routing, use L4.
2. **Choosing regional when global is needed** — Adding a DNS layer later creates complexity. Plan global from the start if multi-region is on the roadmap.
3. **Ignoring PrivateLink requirements** — Only certain LB types can serve as PrivateLink/PSC providers (Azure Standard LB, AWS NLB, GCP Internal LB).
4. **Overlooking static IP needs** — If downstream firewalls whitelist by IP, you need a product that supports static/elastic IPs.
5. **Forgetting WAF** — Every public-facing L7 endpoint should have a WAF. Not all L7 products include WAF natively.

---

## Quick Reference CLI

```bash
# Azure — List available LB SKUs
az network lb list-skus --output table

# AWS — Describe load balancers by type
aws elbv2 describe-load-balancers --query 'LoadBalancers[].{Name:LoadBalancerName,Type:Type,Scheme:Scheme}' --output table

# GCP — List forwarding rules (LB frontends)
gcloud compute forwarding-rules list --format='table(name,region,loadBalancingScheme,target)'
```

**Analysis only — verify against vendor documentation before applying.**
