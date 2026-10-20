---
name: leeway-api-governance
description: Governs consequential API design and review across contracts, versioning, compatibility, authentication, authorization, quotas, errors, observability, and deprecation. Use when approving or changing a public, partner, internal, or agent-facing API.
license: MIT
metadata:
  authority: Creator/Human Authority > LeeWay Standards
  source-class: normalized-drive-candidate
---

# LeeWay API Governance

Define consumers, trust boundary, schema, invariants, error model, idempotency, pagination, rate limits, version policy, compatibility window, observability, and retirement plan before approval. Require contract tests and security review for trust-boundary changes. Report `PROPOSED`, `VALIDATED`, or `BLOCKED`; never call an unexecuted contract live.
