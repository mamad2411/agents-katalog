---
name: design-contract
description: Design versioned API, event, schema, and interface contracts. Use when a provider-consumer boundary, DTO, OpenAPI, AsyncAPI, Protobuf, or compatibility decision changes.
---

# INPUTS
- Approved boundary, provider, consumer, resolved context package, current contract registry, and compatibility policy.

# PRECONDITIONS
- Resolve architecture/API truth topics, confirm the boundary and participating services exist, and inspect any active contract version.

# ACTIONS
- Inspect contract consumers and providers.
- Design the smallest contract change, classify compatibility, and select a semantic version.
- Create a contract draft, import source schemas when applicable, and record required generated outputs.

# OUTPUTS
- Versioned contract draft, compatibility report, and migration requirement for breaking changes.

# VALIDATION
- Run schema and compatibility verification; validate provider, consumer, and contract references.

# FORBIDDEN
- Do not modify business implementation, approve or activate a contract, invent architecture, or silently overwrite an approved version.
