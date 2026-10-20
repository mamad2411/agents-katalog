---
agent: architect
description: "Perform WAF assessment, CAF design area mapping, and Enterprise Landing Zone architecture"
---

# Step 2: Architecture Assessment

Act as the Oracle (🏛️). Perform a Well-Architected Framework assessment and
CAF design area mapping for an Enterprise Landing Zone based on `01-requirements.md`.

## Process

1. Read `agent-output/{customer}/01-requirements.md`
2. Design the **management group hierarchy** using the customer's `{prefix}` (from `AZURE_MANAGEMENT_GROUP_PREFIX`, default `mrg`):
   - Platform MGs: `{prefix}-platform-management`, `{prefix}-platform-connectivity`, `{prefix}-platform-identity`, `{prefix}-platform-security`
   - App LZ MGs: `{prefix}-landingzones-corp`, `{prefix}-landingzones-online`
   - Utility: `{prefix}-sandbox`, `{prefix}-decommissioned`
3. Define **4 platform LZs** with subscription assignments:
   - Management (LAW, Automation Account)
   - Connectivity (Hub VNet, Bastion, optional Firewall, DNS zones)
   - Identity (Spoke VNet, peered to hub, DC subnet)
   - Security (Sentinel, Defender plans, Key Vault, SOAR)
4. Design **hub-spoke networking**: hub VNet CIDRs, spoke peering, Bastion, optional Azure Firewall
5. Map **app LZ archetypes** to profiles: corp (private), online (public-facing), sandbox
6. Assess against all 5 WAF pillars using 221 WARA checks (APRL-synced, per-pillar)
7. Estimate cost ranges for the proposed architecture
8. Identify risks and recommendations
9. All deployments are **subscription-scoped** (not resource-group-scoped)

## Output

Produce `02-architecture-assessment.md` with:
- Management group hierarchy diagram
- Platform LZ architecture (4 LZs with key resources)
- Hub-spoke network topology with CIDRs
- App LZ archetype mapping
- WAF pillar scoring (1-5 per pillar)
- CAF design area → IaC module mapping
- Cost estimation (monthly ranges per environment)
- Risk register with mitigations

## Skills to reference

- `.github/skills/caf-design-areas/SKILL.md` — CAF mapping
- `.github/skills/security-baseline/SKILL.md` — 6 non-negotiable rules
- `.github/skills/cost-governance/SKILL.md` — budget enforcement
- `.github/skills/wara-assessment/SKILL.md` — 221 WAF checks
