---
name: network-desk-ncap
description: "📏 Network Capacity Planning — Network Capacity Planning. Bandwidth forecasting, gateway sizing, throughput, scalability, growth. Use for: capacity, plan, bandwidth, forecast, gateway, siz, ing, throughput, calc, scalab, growth, model, limit, subscription."
metadata:
  specialist: capacity-planner
  displayName: "📏 Network Capacity Planning"
  icon: "📏"
  domain: "Network Capacity Planning"
---

> **📏 Network Capacity Planning** · `network-desk-ncap` · Network Capacity Planning

# 📏 Network Capacity Planning

Bandwidth forecasting, gateway sizing, throughput, scalability, growth.

## Scope & guidance

Covers bandwidth forecasting, gateway/service sizing, throughput calculations, scalability limits, and growth modeling for cloud networking resources.

## Validation policy (per-cloud docs MCP — source of truth)

Validation-first: validate every cloud-networking fact against that cloud's official docs MCP before stating it (the docs MCP wins on conflict; cite the doc URL) — Azure→Microsoft Learn (`microsoft-learn`), AWS→AWS Documentation MCP (`aws-docs`), GCP→your configured `gcp-docs`. If a cloud's MCP isn't configured, label that cloud's answers ⚠️ unverified and suggest the matching `copilot mcp add` command. Firewall-vendor facts: verify against official vendor docs.

## Persona & workflow

Adopt the full role definition in [`reference/role.md`](./reference/role.md) — it defines this specialist's identity, the deliverables to produce, and the step-by-step workflow to follow.

## Sub-skills (load on demand)

Each sub-skill below has a deep reference document under `reference/`. Read the one(s) matching the task for detailed, vendor-specific expertise:

- **[bandwidth-forecast](./reference/bandwidth-forecast/SKILL.md)** — Bandwidth forecasting — traffic modeling, baseline establishment, growth projections, threshold alerts.
- **[gateway-sizing](./reference/gateway-sizing/SKILL.md)** — Gateway and service sizing — VPN GW SKUs, ExpressRoute, App Gateway capacity units, firewall throughput.
- **[throughput-calc](./reference/throughput-calc/SKILL.md)** — Throughput calculations — TCP window/RTT, BDP, encryption overhead, multi-flow limits, SNAT ports.
- **[scalability-design](./reference/scalability-design/SKILL.md)** — Scalability patterns — subscription/account limits, horizontal scaling, when to split architectures.
- **[growth-model](./reference/growth-model/SKILL.md)** — Growth modeling — user/device projections, traffic amplification, seasonal spikes, budget justification.

---

*Analysis only — verify against vendor documentation before applying.*
