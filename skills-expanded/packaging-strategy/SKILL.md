---
name: packaging-strategy
description: "Bundle features into plans that feel natural for each customer segment. Covers feature classification, tier design, upgrade triggers, and avoiding common packaging mistakes. Use when designing tier structure, adding major features, or when upgrade rates are stagnant."
---

# Packaging Strategy

Bundle features into plans where each tier feels like a natural fit for a specific customer segment.

## How to use

- `/packaging-strategy` Apply packaging constraints to this conversation.
- `/packaging-strategy <product>` Design packaging for the described product and feature set.

## Constraints

### Feature Classification
Classify every feature before assigning to tiers:
- Table stakes: what every user needs for basic value. Goes in every plan including free.
- Differentiating: what makes your product better than alternatives. Mid-tier and above.
- Power features: what only sophisticated users need. Premium tier.
- Platform features: admin controls, SSO, audit logs, API access. Enterprise gates.
- NEVER gate table stakes features. It makes the bottom tier feel broken.

### Tier Design
- Start with who you're selling to, not with tiers. Define segments first.
- Each segment MUST have a clear answer to: what problem, what features, what budget, who decides
- MUST limit to 2-3 plans plus enterprise for most products. 5+ tiers is almost always wrong.
- Each tier MUST be describable in one sentence: "This plan is for [who] who need [what]"
- NEVER create a middle tier that's a confusing blend nobody picks

### Upgrade Triggers
- Each tier MUST have a natural trigger that makes someone upgrade
- Good triggers: team size grows, needs a specific feature, usage volume exceeds limit, org requires compliance
- Bad triggers: arbitrary limits uncorrelated with value, removing previously free functionality, gating quality-of-life features
- SHOULD design triggers around genuine moments where the next tier becomes the obvious choice

### Packaging Principles
- Each tier MUST have one hero feature — one clear reason to upgrade
- Feature comparison MUST be scannable in 10 seconds. Limit to 5-7 differentiating features.
- NEVER punish growth. Cost should scale proportionally, not exponentially.
- Add-ons are for genuinely optional capabilities, not for nickel-and-diming core value
- Upgrade and downgrade paths MUST be clean. No data loss on downgrade.

### Anti-Patterns
- The Feature Hostage: one essential feature in premium to force upgrades. Users see through this.
- The Bloated Enterprise: 5x the price but only adds SSO and "dedicated support"
- The Add-On Maze: base price looks reasonable, then every useful feature is extra
- Over-Segmentation: more tiers than the product complexity justifies
