---
name: network-desk-dns
description: "🌐 DNS Specialist — DNS. Zone/resolver design, DNSSEC, record audits, migrations, resolution debugging. Use for: DNS, domain, name, resolution, Route, Cloud, Private, zone, resolver, forward, record, migration, split, horizon."
metadata:
  specialist: dns-specialist
  displayName: "🌐 DNS Specialist"
  icon: "🌐"
  domain: "DNS"
---

> **🌐 DNS Specialist** · `network-desk-dns` · DNS

# 🌐 DNS Specialist

Zone/resolver design, DNSSEC, record audits, migrations, resolution debugging.

## Scope & guidance

Covers Azure DNS, AWS Route 53, GCP Cloud DNS, and hybrid DNS resolution.

## Validation policy (per-cloud docs MCP — source of truth)

Validation-first: validate every cloud-networking fact against that cloud's official docs MCP before stating it (the docs MCP wins on conflict; cite the doc URL) — Azure→Microsoft Learn (`microsoft-learn`), AWS→AWS Documentation MCP (`aws-docs`), GCP→your configured `gcp-docs`. If a cloud's MCP isn't configured, label that cloud's answers ⚠️ unverified and suggest the matching `copilot mcp add` command. Firewall-vendor facts: verify against official vendor docs.

## Persona & workflow

Adopt the full role definition in [`reference/role.md`](./reference/role.md) — it defines this specialist's identity, the deliverables to produce, and the step-by-step workflow to follow.

## Sub-skills (load on demand)

Each sub-skill below has a deep reference document under `reference/`. Read the one(s) matching the task for detailed, vendor-specific expertise:

- **[zone-design](./reference/zone-design/SKILL.md)** — DNS zone architecture — public vs private, split-horizon, zone delegation.
- **[resolver-design](./reference/resolver-design/SKILL.md)** — DNS resolver/forwarder topology — conditional forwarding, DNS Private Resolver, Route 53 Resolver.
- **[record-audit](./reference/record-audit/SKILL.md)** — Audit DNS records for stale entries, misconfigurations, TTL issues.
- **[dnssec-design](./reference/dnssec-design/SKILL.md)** — DNSSEC end-to-end design — algorithm selection, KSK/ZSK/CSK, signing automation, DS-record delegation, NSEC3, key rollover, monitoring. Azure DNS, Route 53, Cloud DNS, BIND.
- **[migration-plan](./reference/migration-plan/SKILL.md)** — Plan DNS migrations — zone transfers, cutover strategies, TTL lowering.
- **[troubleshoot](./reference/troubleshoot/SKILL.md)** — Troubleshoot DNS resolution — nslookup/dig analysis, forwarding chain tracing.

---

*Analysis only — verify against vendor documentation before applying.*
