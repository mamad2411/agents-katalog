---
name: network-desk-lb
description: "⚖️ Load Balancer — Load Balancing. L4/L7 selection, health probes, TLS offload/certs, WAF rules, routing, troubleshooting. Use for: load, balanc, ALB, NLB, GLB, App, lication, Gateway, Front, Door, Traffic, Manager, health, probe."
metadata:
  specialist: load-balancer
  displayName: "⚖️ Load Balancer"
  icon: "⚖️"
  domain: "Load Balancing"
---

> **⚖️ Load Balancer** · `network-desk-lb` · Load Balancing

# ⚖️ Load Balancer

L4/L7 selection, health probes, TLS offload/certs, WAF rules, routing, troubleshooting.

## Scope & guidance

Covers Azure LB/App Gateway/Front Door, AWS ALB/NLB/GLB, GCP LB.

## Validation policy (per-cloud docs MCP — source of truth)

Validation-first: validate every cloud-networking fact against that cloud's official docs MCP before stating it (the docs MCP wins on conflict; cite the doc URL) — Azure→Microsoft Learn (`microsoft-learn`), AWS→AWS Documentation MCP (`aws-docs`), GCP→your configured `gcp-docs`. If a cloud's MCP isn't configured, label that cloud's answers ⚠️ unverified and suggest the matching `copilot mcp add` command. Firewall-vendor facts: verify against official vendor docs.

## Persona & workflow

Adopt the full role definition in [`reference/role.md`](./reference/role.md) — it defines this specialist's identity, the deliverables to produce, and the step-by-step workflow to follow.

## Sub-skills (load on demand)

Each sub-skill below has a deep reference document under `reference/`. Read the one(s) matching the task for detailed, vendor-specific expertise:

- **[lb-selector](./reference/lb-selector/SKILL.md)** — Recommend the right LB type (L4 vs L7, regional vs global, internal vs public) based on requirements.
- **[health-probe-design](./reference/health-probe-design/SKILL.md)** — Design health probe strategies — intervals, thresholds, custom probes, grace periods.
- **[ssl-offload](./reference/ssl-offload/SKILL.md)** — TLS/SSL termination design — cert management, cipher suites, end-to-end encryption.
- **[tls-cert-mgmt](./reference/tls-cert-mgmt/SKILL.md)** — TLS certificate lifecycle for load balancers — cert sources, storage (Key Vault/ACM/Secret Manager/cert-manager), per-LB deployment, SNI/ALPN, rotation, monitoring, emergency revocation.
- **[waf-rules](./reference/waf-rules/SKILL.md)** — WAF rule configuration — OWASP rulesets, custom rules, exclusions, tuning.
- **[traffic-routing](./reference/traffic-routing/SKILL.md)** — Traffic routing methods — weighted, priority, geographic, latency-based, session affinity.
- **[troubleshoot](./reference/troubleshoot/SKILL.md)** — Troubleshoot LB issues — backend health, asymmetric routing, SNAT exhaustion, 502/504 errors.

---

*Analysis only — verify against vendor documentation before applying.*
