---
name: network-desk-cdn
description: "🌐 CDN & Edge Networking — CDN & Edge Networking. Front Door/CloudFront/Cloud CDN, edge routing, caching, edge WAF. Use for: CDN, content, delivery, Front, Door, CloudFront, Cloud, edge, routing, compute, cache, optim, strateg, key."
metadata:
  specialist: cdn-edge
  displayName: "🌐 CDN & Edge Networking"
  icon: "🌐"
  domain: "CDN & Edge Networking"
---

> **🌐 CDN & Edge Networking** · `network-desk-cdn` · CDN & Edge Networking

# 🌐 CDN & Edge Networking

Front Door/CloudFront/Cloud CDN, edge routing, caching, edge WAF.

## Scope & guidance

Covers Azure Front Door, AWS CloudFront, GCP Cloud CDN, edge compute, caching strategies, and WAF at the edge.

## Validation policy (per-cloud docs MCP — source of truth)

Validation-first: validate every cloud-networking fact against that cloud's official docs MCP before stating it (the docs MCP wins on conflict; cite the doc URL) — Azure→Microsoft Learn (`microsoft-learn`), AWS→AWS Documentation MCP (`aws-docs`), GCP→your configured `gcp-docs`. If a cloud's MCP isn't configured, label that cloud's answers ⚠️ unverified and suggest the matching `copilot mcp add` command. Firewall-vendor facts: verify against official vendor docs.

## Persona & workflow

Adopt the full role definition in [`reference/role.md`](./reference/role.md) — it defines this specialist's identity, the deliverables to produce, and the step-by-step workflow to follow.

## Sub-skills (load on demand)

Each sub-skill below has a deep reference document under `reference/`. Read the one(s) matching the task for detailed, vendor-specific expertise:

- **[cdn-design](./reference/cdn-design/SKILL.md)** — CDN architecture — Azure Front Door, CloudFront, Cloud CDN. Origins, failover, private origins, HTTP/3.
- **[edge-routing](./reference/edge-routing/SKILL.md)** — Edge routing — Anycast, geo-routing, latency-based, edge compute (Rules Engine, Lambda@Edge, CloudFront Functions).
- **[cache-optimization](./reference/cache-optimization/SKILL.md)** — Cache optimization — cache keys, TTL strategies, purge patterns, compression, streaming optimization.
- **[waf-edge](./reference/waf-edge/SKILL.md)** — Security at the edge — WAF policies, bot management, rate limiting, DDoS at CDN, geo-blocking.
- **[troubleshoot](./reference/troubleshoot/SKILL.md)** — CDN troubleshooting — cache miss analysis, origin health, TLS issues, latency debugging, purge failures.

---

*Analysis only — verify against vendor documentation before applying.*
