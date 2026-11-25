---
name: assess-architecture
description: Assess project boundaries, dependencies, C4 structure, and design-policy evidence. Use for architecture changes, cross-module tradeoffs, and architecture discovery.
---

# INPUTS
- Resolved L0-L3 context package, project artifact bundle, context registry, source discovery, design policy, and decisions.

# PRECONDITIONS
- Resolve the architecture authority, read the current artifact manifest, and identify the requested architectural boundary.

# ACTIONS
- Inspect canonical sources and classify every finding as observed, inferred, or proposed.
- Assess ownership, dependency direction, contracts, and change impact.
- Write an assessment or decision proposal with provenance and rationale.

# OUTPUTS
- Architecture assessment or decision proposal with classified observations and risks.

# VALIDATION
- Run architecture and artifact validation plus design-policy validation; ensure proposed relationships do not enter active gating.

# FORBIDDEN
- Do not present an inference as observed, modify business implementation, approve design exceptions, or create lifecycle verdicts.
