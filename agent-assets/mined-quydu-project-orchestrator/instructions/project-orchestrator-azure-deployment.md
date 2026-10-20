---
applyTo: "infra/**"
description: Azure discovery and deployment standards for the infra pipeline.
---

# Azure Deployment Instructions

## Entry points and libraries

- `deploy.ps1` is the only entry point. `discover.ps1` and `deploy-infra.ps1` are libraries: they define functions and must be dot-sourced. Running one directly does nothing, which is a common and confusing mistake.
- Keep each module single-purpose. Add a new module rather than growing `deploy.ps1` into a monolith.

## Authentication

- Deployment reads the ignored `.azure/environment.json`, selects its cloud and subscription, and starts its recorded login method when needed. Never store a client secret, certificate, or token in source or a checked-in file.
- Collect cloud, subscription, authentication-method, and MCP preferences only when the profile is missing; do not ask for them repeatedly while it remains valid.
- Verify the active cloud and subscription before any mutating command, and fail closed on mismatch.
- The application authenticates with a managed identity and `DefaultAzureCredential`. Never write a service key into app settings; grant an RBAC role assignment instead.
- The baseline ships `publicNetworkAccess` as `Enabled` so a new project deploys to a working state. Identity-based authentication is not a substitute for network isolation: before the deployment carries real data, set it to `Disabled`, add private endpoints and private DNS, and record the decision in an ADR.

## Discovery before deployment

- Never hard-code a region's capabilities. Probe with `discover.ps1` and let the result drive Bicep parameters, so the same repository deploys to any subscription and region.
- Probe every region in the cloud when checking a service's availability, not just the target region. A single-region probe reports a false negative for region-limited services, and deploying into a region that does not list the SKU fails preflight with `SpecialFeatureOrQuotaIdRequired`.
- Treat a failed probe as unknown, not unavailable, and say so in the output.

## Sovereign clouds

- Support Azure US Government and Commercial from one build. Bicep sets `AZURE_CLOUD`; application code reads it to select the authority host and service endpoints.
- Never assume a `.com` endpoint. Resolve endpoints from the cloud profile.
- Model and SKU availability differs between clouds. Confirm the selection is valid in the target cloud before deploying.

## Approval

- Deployment mutates a shared external system. Run `-WhatIf` and present the plan before any apply, and require explicit approval for the apply itself.
- Never bypass a confirmation prompt to save a step.
