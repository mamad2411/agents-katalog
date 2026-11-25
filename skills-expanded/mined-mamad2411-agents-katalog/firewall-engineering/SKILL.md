---
name: firewall-engineering
description: Design firewall rules and network segmentation. Use when
  controlling traffic flow between services.
metadata:
  tags: firewall, engineering
---

# Firewall & Network Policy

## Use this skill when
- Defining allow-lists and default-deny rulesets
- Segmenting networks and services
- Reviewing exposed services and ports

## Do not use this skill when
- Application-level auth
- Kubernetes network policies (use kubernetes-engineering)

## Instructions
1. Default to deny; open only what each service needs.
2. Use explicit allow lists by port, source, destination.
3. Segment tiers: web, app, db, admin on different subnets/zones.
4. Never expose management ports (SSH, 5432, 6379) publicly.
5. Keep rule lists reviewed and versioned (IaC).
6. Log and alert on dropped traffic to detect scanning.
7. Set stateful rules (established/related) carefully.

## Checklist
- No public admin/db ports
- Default-deny posture
- Rules reviewed/versioned

## Output Format
- Segments | ruleset | exposure | monitoring

## Common Mistakes
- Open 0.0.0.0* accordingly
- Allowing all egress “to be safe”
- Too complex rulesets never reviewed
