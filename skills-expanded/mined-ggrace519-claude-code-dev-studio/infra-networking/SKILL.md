---
name: infra-networking
description: Network topology, VPC / subnets, peering, transit gateways, VPN, service mesh, DNS, egress / ingress, firewalling. Auto-invoked when designing network layout, debugging connectivity, or reviewing zero-trust / segmentation posture.
---

# Infra Networking

Networking is silent until it isn't — and when it breaks, it looks like everyone
else's bug. The work is the paths packets take across VPCs, regions, clouds, and
the on-prem edge, plus the policy and observability that make them debuggable.

## When to reach for this

- Designing VPC/VNet layout: CIDR allocation, subnet tiers, AZ spread
- Connecting things: peering vs. transit gateway/hub-spoke, VPN, Direct
  Connect/ExpressRoute, cross-cloud
- Reviewing egress/ingress posture, segmentation, or zero-trust policy
- Debugging connectivity, DNS resolution, latency, or MTU issues

## Principles

1. **Allocate CIDRs for 5+ years.** Running out of IP space mid-growth is a
   6-month renumbering project. Reserve a /16 per region per environment from a
   non-overlapping org-wide plan (mind on-prem and partner ranges), carve /24
   subnets with AZ affinity, and write the plan down.
2. **Private by default.** New services start in private subnets with explicit
   egress via VPC endpoints or NAT. Public exposure requires an ADR and an
   ALB/WAF in front — never a public IP on the workload itself.
3. **Prefer endpoints over NAT for cloud-service traffic.** Gateway endpoints
   (S3/DynamoDB) are free; interface endpoints/PrivateLink keep traffic off the
   NAT path. NAT gateways bill per-GB processed (~$0.045/GB on AWS) — S3-heavy
   workloads behind NAT are a classic silent cost and a needless dependency.
4. **Segment east-west.** Security groups alone are not a segmentation story:
   per-service egress allowlists, default-deny between namespaces/tiers, and
   service-mesh mTLS with authz policies where identity-based policy is needed.
   Adopt a mesh for mTLS + traffic policy at scale, not for one retry knob.
5. **DNS is a debug crime scene.** The resolver chain (host → stub resolver →
   VPC resolver → private zones → external) hides failures. Centralize
   resolution policy, enable resolver query logging, alert on NXDOMAIN spikes,
   and keep split-horizon zones documented.
6. **Flow logs are the truth.** Enable VPC/NSG flow logs everywhere with
   retention that covers your incident lookback; during an incident, "which
   service talked to which, when" must be a query, not archaeology.
7. **Cross-AZ and egress traffic cost real money.** AWS cross-AZ runs ~$0.01/GB
   each direction; internet egress ~$0.09/GB. Map heavy flows and co-locate
   chatty services deliberately — treat egress cost like a latency budget.

## Connectivity decision table

| Situation | Use | Why |
|---|---|---|
| 2–3 VPCs, simple mutual access | VPC peering | cheapest, no transit hop; no transitive routing |
| Many VPCs / multi-account hub-spoke | Transit gateway / hub VNet | transitive routing, central inspection; per-GB cost |
| On-prem, latency-tolerant or interim | Site-to-site VPN | fast to stand up; ~1.25 Gbps per tunnel ceiling |
| On-prem, steady high bandwidth | Direct Connect / ExpressRoute | predictable latency; weeks of lead time — order early |
| Single service exposed across accounts | PrivateLink | no CIDR coordination, no route sprawl |

## Connectivity debug order

1. DNS — does the name resolve, and to what (`dig` against each resolver in the chain)?
2. Route — is there a route table entry for the destination (and a return path)?
3. Policy — security group / NACL / network policy / mesh authz, in both directions
4. Path — MTU (VPN/overlay tunnels clamp below 1500; blackholed large packets
   look like hangs), conntrack exhaustion, NAT port limits
5. Endpoint — is the listener actually up (`ss -ltn` on the target)?

## Pitfalls

- Overlapping CIDRs with a future acquisition, partner, or on-prem range —
  un-fixable without renumbering or NAT hacks
- Security groups referencing CIDRs where SG-references would do — rules rot as
  IPs churn
- Asymmetric routing through stateful firewalls/NAT — replies drop and only
  some flows fail, intermittently
- A single NAT gateway (one AZ) as the egress path for a multi-AZ workload —
  cross-AZ tax plus an availability single point
- TLS terminated at the edge with plaintext east-west "because it's internal"
- Debugging connectivity without flow logs enabled — turning them on after the
  incident starts the clock at zero

---
*Related: `infra-k8s` (in-cluster network policy and CNI), `infra-iam`
(identity is the other half of zero-trust), `infra-observability` (flow-log
pipelines), `infra-finops` (egress and cross-AZ cost) · domain agent:
`infra-architect` · output/ADR format: `playbook-conventions`*
