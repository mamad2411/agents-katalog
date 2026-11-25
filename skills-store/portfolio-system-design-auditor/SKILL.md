---
name: portfolio-system-design-auditor
description: "Evaluate cross-boundary or security-sensitive changes against project architecture."
---

# portfolio-system-design-auditor

Review actual behavior against [verified architecture](../../brain/architecture.md) and task acceptance criteria. Check secret exposure, input validation, authentication/authorization, transport failures, data access boundaries, and lifecycle ownership as relevant.

Prefer cohesive modules and services when complexity warrants them. A browser-facing public configuration value is not automatically a secret; privileged credentials must never be exposed. Streaming uses appropriate route handlers rather than an unconditional Server Actions rule.

Report concrete risks with evidence and a scoped remedy. Resolve routine authorized implementation choices autonomously; request user input only for material unresolved scope/product/permission decisions.
