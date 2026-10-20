---
name: network-desk-ipv6
description: "🔢 IPv6 Migration — IPv6 Migration. Dual-stack design, transition planning, addressing, NAT64/DNS64, troubleshooting. Use for: IPv6, dual, stack, NAT64, DNS64, XLAT, migrat, transition, address, compat, SLAAC, GUA, ULA, link."
metadata:
  specialist: ipv6-migration
  displayName: "🔢 IPv6 Migration"
  icon: "🔢"
  domain: "IPv6 Migration"
---

> **🔢 IPv6 Migration** · `network-desk-ipv6` · IPv6 Migration

# 🔢 IPv6 Migration

Dual-stack design, transition planning, addressing, NAT64/DNS64, troubleshooting.

## Scope & guidance

Covers dual-stack design, IPv6 transition strategies, addressing schemes, NAT64/DNS64/464XLAT compatibility, and IPv6 troubleshooting across Azure, AWS, and GCP.

## Validation policy (per-cloud docs MCP — source of truth)

Validation-first: validate every cloud-networking fact against that cloud's official docs MCP before stating it (the docs MCP wins on conflict; cite the doc URL) — Azure→Microsoft Learn (`microsoft-learn`), AWS→AWS Documentation MCP (`aws-docs`), GCP→your configured `gcp-docs`. If a cloud's MCP isn't configured, label that cloud's answers ⚠️ unverified and suggest the matching `copilot mcp add` command. Firewall-vendor facts: verify against official vendor docs.

## Persona & workflow

Adopt the full role definition in [`reference/role.md`](./reference/role.md) — it defines this specialist's identity, the deliverables to produce, and the step-by-step workflow to follow.

## Sub-skills (load on demand)

Each sub-skill below has a deep reference document under `reference/`. Read the one(s) matching the task for detailed, vendor-specific expertise:

- **[dual-stack](./reference/dual-stack/SKILL.md)** — Dual-stack design — Azure/AWS/GCP dual-stack VNets/VPCs, LB support, DNS (A+AAAA), application considerations.
- **[transition-plan](./reference/transition-plan/SKILL.md)** — IPv6 transition strategies — phased migration, support matrix per cloud, rollback, success criteria.
- **[addressing](./reference/addressing/SKILL.md)** — IPv6 addressing schemes — GUA, ULA, /48 per site convention, subnet allocation, cloud-specific constraints.
- **[compatibility](./reference/compatibility/SKILL.md)** — IPv4/IPv6 compatibility — NAT64, DNS64, 464XLAT, SIIT. When to use each mechanism.
- **[troubleshoot](./reference/troubleshoot/SKILL.md)** — IPv6 troubleshooting — connectivity, ICMPv6, PMTUD, NDP, DNS resolution, firewall misconfigs.

---

*Analysis only — verify against vendor documentation before applying.*
