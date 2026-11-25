---
name: network-segmentation
description: "Covers network segmentation vs microsegmentation: trust zones, east-west control, where to enforce (firewall, NACL, security group, host, identity), the Purdue model and IDMZ for OT, and how segmentation caps blast radius. Use when the user asks how to segment a network, VLAN or zone design, microsegmentation products, limiting lateral movement or ransomware spread, or separating IT from OT. (Full OT treatment: ot-ics.)"
license: Apache-2.0
metadata:
  verified: "2026-11-17"
---

# Network Segmentation

Segmentation exists for one reason: **contain the blast radius**. A flat network means one compromised host can reach everything; the attacker's lateral movement is free. Segmentation makes every hop cost the attacker another control to defeat. Judge any segmentation design by one question: _when host X is owned, what can it now reach?_

This is the network-centric leg of zero trust; it pairs with `load_skill zero-trust` (identity decides who; segmentation shrinks what they can touch).

## Segmentation vs microsegmentation

A spectrum of granularity, not two products. Pick the coarsest level that bounds the blast radius you care about.

- **Macro-segmentation**: coarse zones (VLANs/subnets, prod vs dev, DMZ, PCI cardholder data environment). Controls **north-south** (zone-to-zone) traffic at a firewall. Cheap, well understood; useless against lateral movement _inside_ a zone.
- **Microsegmentation**: per-workload / per-application policy, ideally identity- or label-based, enforced at the host or workload edge (host firewall, hypervisor, service-mesh sidecar, cloud security group). Controls **east-west** (workload-to-workload). This is where lateral movement actually dies.
- Reach for microsegmentation around **crown jewels and high-blast-radius tiers** (domain controllers, databases, OT, PCI CDE), not uniformly everywhere (operationally unaffordable). Macro-segment the estate; micro-segment the prizes.

## East-west is the point

Perimeter (north-south) firewalls catch the inbound attacker but see nothing once they're inside. Most damage is **east-west**: lateral movement from a phished workstation to a server to the domain controller. If an internal tester can walk freely host-to-host, your segmentation is decorative.

- Default-deny east-west between tiers; allow only the specific flows the app needs.
- Block workstation-to-workstation entirely where possible (no business reason for peer SMB/RDP); it kills the most common lateral path.
- Segment management planes (RDP/SSH/WinRM/iLO) onto a separate admin network reached only via a jump host / PAW.

## Enforcement points: choose by trust and granularity

The enforcement point _is_ the architecture decision. Closer to the workload = smaller implicit-trust zone behind it, but more policy to manage.

| Enforcement point                    | Granularity            | Use for                                               |
| ------------------------------------ | ---------------------- | ----------------------------------------------------- |
| Perimeter / NGFW                     | Zone (north-south)     | Internet edge, zone boundaries, DMZ                   |
| Internal L3 firewall / router ACL    | Subnet/VLAN            | Macro-zones between business tiers                    |
| Cloud **Security Group** (stateful)  | Instance/ENI           | Default east-west control in cloud: per-workload      |
| Cloud **NACL** (stateless, subnet)   | Subnet                 | Coarse subnet guardrail; backstop, not primary        |
| **Host firewall** / agent (microseg) | Per-host / per-proc    | East-west kill-switch independent of network topology |
| **Service mesh** (mTLS + L7 policy)  | Per-service / identity | Container/K8s workloads; identity-based allow         |
| **Identity / ZTNA / SDP**            | Per-session/user       | Replace network reachability with brokered access     |

- In cloud, **Security Groups are your real microsegmentation** (per-instance, stateful, identity-referenceable); NACLs are a coarse stateless backstop. See `load_skill cloud-security`.
- Host-based enforcement survives a topology you don't control (cloud, BYOD, M&A): preferred for true microsegmentation.
- The most resilient layer is identity (ZTNA): if the resource has _no_ network route and is reachable only through an authenticated broker, segmentation failures matter less.

## Trust zones: design rules

- Define zones by **data sensitivity + blast-radius tolerance**, not org chart.
- Every zone boundary gets default-deny + an explicit, documented allow-list. An undocumented allow rule is a finding.
- **No transitive trust**: zone A→B and B→C must not silently yield A→C.
- Put a **DMZ** between untrusted and internal; nothing internet-facing terminates directly on the internal network.
- Management/OT/IoT each get their own zone: they speak weak or unauthenticated protocols and must never share a broadcast domain with users.

## Purdue model (OT / ICS segmentation)

Industrial networks segment by **Purdue level**, L0 process up to L4/L5 enterprise IT, with **L3.5 (the IDMZ)** as the load-bearing boundary: the only place IT and OT exchange data, mediated by brokers, historians and jump hosts. Treat it as the crown-jewel boundary and allow no direct IT→OT path across it.

The rule that differs from IT: **OT is unpatched, fragile and safety-critical, so segmentation _is_ the primary control**, not a supplement to patching. IEC 62443 zones-and-conduits is the modern framing layered on Purdue. Full treatment (the levels, Security Levels, safe monitoring and the regulatory pull) in `load_skill ot-ics`.

## How segmentation caps blast radius (the payoff)

- Compromise of one segment ≠ compromise of the estate: the attacker must defeat a fresh control at each boundary, and each attempt generates detectable east-west traffic.
- Smaller segments = **smaller incident scope** = cheaper containment, narrower forensics, fewer notification obligations.
- It directly shrinks **compliance scope**: a well-segmented PCI CDE pulls everything outside it out of audit scope.
- Map segmentation gaps to controls with `load_skill control-mapping` (CWE-668; ISO A.8.20/A.8.22; NIST SC-7; CIS 12/13) and feed residual exposure into `load_skill risk-assessment`.

## Rules

- Segmentation without east-west enforcement is theater: perimeter-only does not contain a breach.
- Microsegment the crown jewels, macro-segment the rest; uniform microsegmentation collapses operationally.
- Every allow rule must trace to a documented app flow; undocumented allows are findings.
- In OT, segment don't patch; the L3.5 DMZ is non-negotiable.
