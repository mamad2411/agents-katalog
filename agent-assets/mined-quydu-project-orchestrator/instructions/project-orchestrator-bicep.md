---
applyTo: "**/*.bicep,**/*.bicepparam"
description: Azure infrastructure-as-code standards for Bicep.
---

# Bicep Instructions

- Bicep is the only supported infrastructure definition language. Portal changes in shared environments are not permitted.
- Prefer Azure Verified Modules over hand-written resource declarations when a suitable module exists.
- Declare `targetScope` explicitly.
- Parameterize environment-specific values; never hard-code subscription IDs, tenant IDs, resource IDs, or regions.
- Use `@description` on every parameter and output, and `@allowed` where the value set is closed.
- Mark sensitive parameters `@secure()`. Never emit a secret as an output.
- Retrieve secrets with Key Vault references, not literal values in parameter files.
- Enable system-assigned or user-assigned Managed Identity on every resource that authenticates to another Azure service.
- Disable public network access by default; expose services through Private Endpoints unless an ADR documents otherwise.
- Enforce HTTPS/TLS 1.2 minimum, disable local authentication where a service supports Entra-only auth.
- Attach diagnostic settings routing to the central Log Analytics workspace.
- Apply the standard tag set: owner, environment, cost center, data classification.
- Use `uniqueString()` for globally unique names; keep names deterministic across deployments.
- Validate with `az deployment ... validate` and a what-if run before any apply. Applying to a shared environment requires explicit approval.
