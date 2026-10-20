---
name: cost-estimate
description: Bottom-up cloud cost estimate per architecture variant at three load points, with estimate class and hidden-dimension checks.
---

# /cost-estimate [variant]

Owner: **cost-analyst**; inputs from **platform-lead** (service mapping) and the brief (load profile).

## Sequence
1. Precondition: component-to-service mapping exists for the variant(s). Missing → request via
   /architecture-variants.
2. Per mapped service: pricing dimension(s), unit price (platform catalog cost notes or cited
   vendor pricing page with retrieval date), expected units at launch / expected / 10x load.
   Show the arithmetic per line.
3. Hidden dimensions checked explicitly: egress, NAT, cross-AZ traffic, per-request storage
   ops, log ingestion, idle dev/staging environments, third-party SaaS seats.
4. State estimate class (rough ±50% / budgetary ±25% / definitive) and the crossover points
   between variants ("variant B becomes cheaper above N req/day").
5. Compare against the brief's budget ceiling — over-ceiling at expected load is a BLOCKER.

## Output
`architecture/cost-model.md`: per-variant tables, crossovers, top-3 cost risks, savings levers.
Post-deploy: actuals-vs-estimate section appended.
