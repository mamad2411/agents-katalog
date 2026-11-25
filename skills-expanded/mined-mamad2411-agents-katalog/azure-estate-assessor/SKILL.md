---
name: azure-estate-assessor
description: >-
  Assess an existing Azure estate with open-source tooling and produce a
  disposition map for platform onboarding: Azure Resource Graph inventory, azqr
  best-practice findings, Azure Governance Visualizer policy/RBAC map, and
  aztfexport / Bicep-decompile IaC-coverage analysis. Use for brownfield
  discovery, "what do we actually run", IaC coverage ratios, migration triage
  (wrap / refactor / leave / retire), or to run increment I9 (Cloud estate,
  Azure) of the assessment-orchestrator and return an assessment delta.
  Read-only by design; requires az CLI access (Reader role) when run live.
---

# Azure Estate Assessor

## Purpose
Organizational assessment (`platform-assessment`) senses people, process, and
maturity; this skill senses the **infrastructure itself**. No official Microsoft
guidance assembles the brownfield pipeline end to end — the pieces exist and
this skill composes them into evidence and a decision artifact: which workloads
land on which platform, and how.

## The assessment pipeline (all OSS, all read-only)
1. **Inventory — Azure Resource Graph.** KQL over subscriptions in scope:
   resource counts by type/region/RG, orphaned resources, tag coverage against
   the constitution's mandatory tags, public-endpoint exposure. Available via
   the Azure MCP Server or `az graph query`.
2. **Best-practice findings — azqr** (`github.com/Azure/azqr`): scans
   subscriptions/RGs for Well-Architected compliance; also invocable through
   the Azure MCP Server's compliance tools.
3. **Governance map — Azure Governance Visualizer** (AzGovViz): management
   group hierarchy, Azure Policy assignments, RBAC sprawl, custom-role usage.
4. **IaC coverage — aztfexport + Bicep decompile.** `aztfexport --hcl-only`
   (preview, no state writes) per candidate RG reveals what could be brought
   under Terraform; `az group export` + `az bicep decompile` for the Bicep
   path. Compare against what is already in Git to compute the coverage ratio.
   Honor Microsoft's own warning: "Export is not guaranteed to succeed" — every
   export is a draft, not production IaC.

## Primary output: the disposition map
One row per workload/RG, the connective tissue between assessment and build:

| Workload | Evidence refs | Disposition | Target platform/environment | Effort | Notes |
|---|---|---|---|---|---|
| orders-api | I9-E003, I9-E011 | **Recipe-wrap** (existing Terraform absorbed as a Radius Recipe) | azure-aks / prod | S | already IaC'd |
| legacy-batch | I9-E007 | **Refactor** to golden path (AVM regen) | azure-aca / prod | M | no IaC, public SQL |
| vendor-appliance | I9-E015 | **Leave in place** | — | — | unsupported topology |
| old-poc-rg | I9-E018 | **Retire** | — | S | 0 requests / 90 days |

Dispositions: *Recipe-wrap* (absorb existing IaC unchanged behind a platform
abstraction), *Refactor* (regenerate on the golden path with AVM modules),
*Leave in place*, *Retire*. Handoff: `workload-onboarder` executes the map.

## Running as assessment increment I9
When an `assessment-orchestrator` engagement is active, run this skill as
increment **I9 Cloud estate (Azure)**: operator = platform engineer with
Reader (+ `Cost Management Reader` only if approved under I4); return an
assessment **delta** in the canonical `assessment-state.yaml` format with
increment-prefixed evidence IDs (`I9-Exxx`), provenance (query/tool + date),
confidence, and the disposition map attached as an evidence artifact. Never
edit the canonical state directly.

## Guardrails
- Reader-level credentials only; refuse write scopes even if offered.
- No secret values, connection strings, or key material in evidence — resource
  IDs and configuration flags only.
- Point-in-time honesty: stamp every finding with query date; estates drift.

## Delegates to
- Organizational/maturity signals from repos, CI, sentiment → `platform-assessment:platform-maturity-discovery`
- Formal maturity scoring → `adp-enablement:platform-maturity-benchmark`
- Cost analysis beyond inventory → assessment increment I4 (FinOps)
