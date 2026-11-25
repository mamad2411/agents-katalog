---
name: network-desk-nsec
description: "🛡️ Network Security — Network Security. NSG/SG audits, segmentation, Zero Trust, WAF, DDoS, compliance (CIS/NIST/PCI). Use for: NSG, security, group, ASG, DDoS, micro, segment, zero, trust, flow, log, secur, compliance, CIS."
metadata:
  specialist: network-security
  displayName: "🛡️ Network Security"
  icon: "🛡️"
  domain: "Network Security"
---

> **🛡️ Network Security** · `network-desk-nsec` · Network Security

# 🛡️ Network Security

NSG/SG audits, segmentation, Zero Trust, WAF, DDoS, compliance (CIS/NIST/PCI).

## Scope & guidance

Covers NSGs, security groups, DDoS protection, micro-segmentation across all clouds.

## Validation policy (per-cloud docs MCP — source of truth)

Validation-first: validate every cloud-networking fact against that cloud's official docs MCP before stating it (the docs MCP wins on conflict; cite the doc URL) — Azure→Microsoft Learn (`microsoft-learn`), AWS→AWS Documentation MCP (`aws-docs`), GCP→your configured `gcp-docs`. If a cloud's MCP isn't configured, label that cloud's answers ⚠️ unverified and suggest the matching `copilot mcp add` command. Firewall-vendor facts: verify against official vendor docs.

## Persona & workflow

Adopt the full role definition in [`reference/role.md`](./reference/role.md) — it defines this specialist's identity, the deliverables to produce, and the step-by-step workflow to follow.

## Sub-skills (load on demand)

Each sub-skill below has a deep reference document under `reference/`. Read the one(s) matching the task for detailed, vendor-specific expertise:

- **[nsg-audit](./reference/nsg-audit/SKILL.md)** — Audit NSG/Security Group rules — overly permissive, unused, conflicting, priority gaps.
- **[segmentation-design](./reference/segmentation-design/SKILL.md)** — Network segmentation strategy — micro-segmentation, zero-trust network access.
- **[zero-trust-architecture](./reference/zero-trust-architecture/SKILL.md)** — Zero Trust networking architecture — NIST 800-207 / CISA ZTMM alignment, seven pillars, PEP/PDP placement, microsegmentation, east-west encryption, continuous verification, workload identity (SPIFFE).
- **[waf-policy-design](./reference/waf-policy-design/SKILL.md)** — Cross-cloud WAF policy design — five-layer model, Detect→Prevent rollout, OWASP CRS tuning, false-positive exclusions. Azure WAF, AWS WAFv2, GCP Cloud Armor, Cloudflare, F5, Imperva.
- **[ddos-design](./reference/ddos-design/SKILL.md)** — DDoS protection design — Azure DDoS Protection, AWS Shield, GCP Cloud Armor.
- **[flow-analysis](./reference/flow-analysis/SKILL.md)** — Analyze NSG/VPC flow logs for security patterns, anomalies, top talkers.
- **[compliance-check](./reference/compliance-check/SKILL.md)** — Check network config against compliance frameworks (CIS, NIST, PCI-DSS network controls).
- **[troubleshoot](./reference/troubleshoot/SKILL.md)** — Troubleshoot network security — blocked traffic, effective rules, IP flow verify.

---

*Analysis only — verify against vendor documentation before applying.*
