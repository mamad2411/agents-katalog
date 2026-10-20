---
name: network-desk-hyb
description: "🔗 Hybrid Connectivity — Hybrid Connectivity. VPN, ExpressRoute/Direct Connect, BGP, bandwidth, failover/redundancy. Use for: ExpressRoute, Direct, Connect, Cloud, Interconnect, S2S, VPN, P2S, site, point, gateway, IPsec, IKEv, BGP."
metadata:
  specialist: hybrid-connectivity
  displayName: "🔗 Hybrid Connectivity"
  icon: "🔗"
  domain: "Hybrid Connectivity"
---

> **🔗 Hybrid Connectivity** · `network-desk-hyb` · Hybrid Connectivity

# 🔗 Hybrid Connectivity

VPN, ExpressRoute/Direct Connect, BGP, bandwidth, failover/redundancy.

## Scope & guidance

Covers ExpressRoute, VPN gateways, AWS Direct Connect, GCP Cloud Interconnect.

## Validation policy (per-cloud docs MCP — source of truth)

Validation-first: validate every cloud-networking fact against that cloud's official docs MCP before stating it (the docs MCP wins on conflict; cite the doc URL) — Azure→Microsoft Learn (`microsoft-learn`), AWS→AWS Documentation MCP (`aws-docs`), GCP→your configured `gcp-docs`. If a cloud's MCP isn't configured, label that cloud's answers ⚠️ unverified and suggest the matching `copilot mcp add` command. Firewall-vendor facts: verify against official vendor docs.

## Persona & workflow

Adopt the full role definition in [`reference/role.md`](./reference/role.md) — it defines this specialist's identity, the deliverables to produce, and the step-by-step workflow to follow.

## Sub-skills (load on demand)

Each sub-skill below has a deep reference document under `reference/`. Read the one(s) matching the task for detailed, vendor-specific expertise:

- **[vpn-design](./reference/vpn-design/SKILL.md)** — VPN gateway design — S2S, P2S, IKEv2/OpenVPN, BGP, active-active, custom IPsec policies.
- **[expressroute-design](./reference/expressroute-design/SKILL.md)** — ExpressRoute / Direct Connect / Cloud Interconnect circuit design, peering, and routing.
- **[bgp-design](./reference/bgp-design/SKILL.md)** — Dedicated BGP design for cloud hybrid — ASN allocation, prefix/AS-PATH filters, attribute manipulation, multi-circuit active/active and active/passive, BFD, convergence tuning.
- **[bandwidth-calc](./reference/bandwidth-calc/SKILL.md)** — Bandwidth planning — circuit sizing, aggregation, QoS, and cost estimation.
- **[routing-design](./reference/routing-design/SKILL.md)** — BGP routing design — AS path manipulation, route filters, communities, local preference.
- **[failover-design](./reference/failover-design/SKILL.md)** — Redundancy and failover — dual circuits, VPN backup, BFD, fast convergence.
- **[troubleshoot](./reference/troubleshoot/SKILL.md)** — Troubleshoot hybrid connectivity — BGP neighbor state, tunnel status, MTU issues, asymmetric routing.

---

*Analysis only — verify against vendor documentation before applying.*
