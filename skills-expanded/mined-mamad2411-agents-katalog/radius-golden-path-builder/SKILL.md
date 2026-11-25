---
name: radius-golden-path-builder
description: >-
  Build Azure golden paths on Radius + Dapr + Azure Verified Modules from the
  azure-agentic-idp reference templates: custom Resource Types, per-environment
  Bicep Recipes (dev k8s / Azure Container Apps / AKS compute; Cosmos DB /
  PostgreSQL state behind the Dapr state API), APIM route recipes, landing-zone
  foundation, and Flux GitOps layout. Use to stamp out a golden path for an
  org, add a recipe flavor, extend the reference architecture, or maintain the
  interchangeable-backend contract. Transitional: the golden-path API
  (golden-path-api-designer) supersedes repo-stamping as it lands.

---

# Radius Golden Path Builder

## Purpose
Implements golden paths on the opinionated Azure + OSS core: Radius (Resource
Types + Recipes + Environments), Dapr (state/pub-sub portability and the
sidecar), AVM Bicep modules, Flux GitOps. The method is
`adp-enablement:golden-path-designer`'s (paths as versioned products, TVP
scoping); this skill is the Azure/Radius substrate — the alternative back-end
to that skill's Backstage + Crossplane pattern.

**Status: transitional.** The target state exposes these operations as the
golden-path API behind APIM; until then, this skill stamps the reference
templates into org repos, and afterwards it remains the maintenance path for
the recipes the API drives.

## The reference implementation (azure-agentic-idp)
Template source: the `azure-agentic-idp` repository (pin a tag). One
`app.bicep`, three destinations — the interchangeable/routable contract:

- **Abstract types** (`ByteCloud.App/apiBackends`, `apiRoutes` — org namespace
  is a template token): the app's only contracts are the Dapr state API and an
  HTTP `baseUrl`.
- **Recipes as the swap mechanism:** dev = k8s containers + Redis;
  azure-aca = Container Apps + Cosmos DB; azure-aks = AKS Deployments +
  PostgreSQL Flexible Server. Same app definition; environment choice decides
  compute and store; the APIM route recipe re-points automatically because
  `backendUrl` flows from the recipe output at deploy time.
- **Landing-zone foundation:** Key Vault, Storage, Log Analytics, Azure
  Monitor workspace, App Insights; central Managed Grafana wiring
  (per `azure-platform-designer`).
- **Recipe output contracts are API:** every apiBackends recipe returns
  `host`/`port`/`baseUrl`; stateStores return Dapr `type`/`version`/metadata;
  apiRoutes return `publicUrl`. Breaking these breaks every app on the path.

## Two axes of portability (why this design holds)
This golden path implements the Radius + Dapr portability model directly:
- **Code portability (Dapr):** the app talks to building-block APIs (state,
  pub/sub, secrets), never a backend's native SDK — so the `statestore`
  component swaps Redis → Cosmos DB → PostgreSQL with no application change.
- **Deployment portability (Radius):** abstract Resource Types + per-environment
  Recipes mean the same `app.bicep` binds different infrastructure per
  Environment; across a sovereignty boundary **only the Recipes differ**.

The rule that makes it real: keep recipe `result.values` contracts stable, and
never let a workload import a backing store's native SDK — that is the failure
mode that silently breaks portability. Full guidance, the sovereignty
checklist, and caveats: `../../references/dapr-radius-sovereignty.md`.

## Workflow
1. Read constitution + the target environment design; resolve template tokens
   (org namespace, naming, registry) from TEMPLATING.md.
2. Resolve AVM module pins deterministically (registry tag query — never from
   memory); check module status in the index.
3. Stamp/extend: types YAML, recipes, environments, landing-zone Bicep, Flux
   layout, CI (pin-resolvability check + local e2e via k3d/rad/dapr).
4. Run `iac-guardrail-verifier`; open PRs.

## Known seams (disclose, do not hide)
- Radius is CNCF Sandbox v0.x; control plane requires Kubernetes even when
  targeting ACI/ACA; Flux is the only supported GitOps engine.
- ACA is not a Radius compute target — the ACA flavor is recipe-provisioned,
  which is exactly why the abstract-type design keeps one portable app.bicep.
- Durable Dapr workflows need AKS, not ACA (workflow SDK unsupported there).
- Demo shortcuts in the reference are marked and must be flipped for prod.

## Delegates to
- Golden-path product method (maturity levels, TVP, adoption metrics) → `adp-enablement:golden-path-designer`
- Path CI gates as fitness functions → `adp-enablement:platform-fitness-functions`
- The API that replaces stamping → `golden-path-api-designer`
