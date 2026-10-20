---
mode: agent
description: Review this repository's architecture against the Azure Well-Architected Framework and produce structured findings.
---

# Review Architecture

Run a design-time architecture review of this repository.

1. Inventory the architecture from infrastructure as code, application configuration, and `docs/adr/`. Do not infer from names.
2. Evaluate each Well-Architected pillar: reliability, security, cost optimization, operational excellence, performance efficiency.
3. Check identity, network exposure, data residency, secret handling, region and cloud availability, and disaster recovery.
4. Record each finding with location, pillar, impact, severity, confidence, and a specific recommendation.
5. Separate verified evidence from assumptions, and list what could not be assessed.

Write the result through the `architecture-review` skill to `reports/architecture-review.json`. Do not modify infrastructure. Any change requires a separate approved workflow.
