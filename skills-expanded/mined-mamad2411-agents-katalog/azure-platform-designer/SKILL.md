---
name: azure-platform-designer
description: >-
  Recommend how many platforms to build and design their Azure topology:
  platform-count heuristic (thinnest viable platform, cognitive load, CAF
  platform teams), Radius environment ladder (simple / application-centric /
  enterprise by business unit x region x prod-nonprod), landing-zone design on
  Azure Verified Modules (subscription vending, foundation services, central
  Managed Grafana observability), and ADRs for every decision. Use for "how
  many platforms", environment topology, landing zone architecture, platform
  target-state design on Azure, or sizing a platform to an org.
---

# Azure Platform Designer

## Purpose
Answer the two questions every platform engagement starts with — *how many
platforms?* and *shaped how?* — with a citable reasoning chain instead of
folklore, then compile the answer into a deployable Azure design.

## The platform-count heuristic (opinionated, sources cited)
No authoritative source prescribes a number; the converged guidance:
1. **Default to one thin platform** per distinct developer population or app
   stack (CNCF Platforms whitepaper: "build the thinnest viable platform layer";
   Team Topologies TVP — a platform can start as a wiki page).
2. **Scale by adding environments, not platforms** — environments are cheap,
   platforms are not. Radius makes this concrete: one control plane and
   Resource Type catalog, many environments.
3. **Scale people into capability-aligned platform teams** before splitting the
   platform (Microsoft CAF: "A single platform team cannot meet the diverse
   needs of a large organization" — 6-10 person product-aligned teams).
4. **Split platforms only on population divergence** — when two user groups'
   needs and cognitive loads no longer fit one product.
5. **Right-size ambition per aspect** with the CNCF maturity model — never
   uniformly. Formal scoring delegates to
   `adp-enablement:platform-maturity-benchmark`; consume its gap register as
   interview input rather than re-scoring.

## The Radius environment ladder (topology sizing)
| Rung | Shape | When |
|---|---|---|
| Simple | One shared environment set | One team, early TVP |
| Application-centric | Environment set + resource group per application | Per-app recipe customization needed |
| Enterprise | Environments by business unit x region x prod/non-prod | Multi-BU, sovereignty, or regulatory splits |

## Sovereignty as a topology driver
When data-residency or regulatory boundaries are in play, they are a primary
topology input, not an afterthought. The Radius + Dapr model makes relocation a
deployment decision rather than a rewrite (Dapr = code portability, Radius =
deployment portability), so the design move is: **one Radius environment per
sovereignty boundary**, at the enterprise rung, with region-pinned Recipes and
no cross-boundary data connections. Because only Recipes differ across
boundaries, the same application definition serves every region — the platform
carries the sovereignty constraint, the app does not. Encode the residency
boundaries as constitution rules and cite them in the topology ADR. Full model
and checklist: `../../references/dapr-radius-sovereignty.md`.

## Landing-zone design (AVM-first)
- Management groups / policy / subscription vending via the ALZ pattern and
  `avm/ptn/lz/sub-vending`.
- Per-landing-zone foundation: Key Vault, Storage, Log Analytics workspace,
  Azure Monitor workspace (raw resource — no AVM module exists), workspace-based
  App Insights, diagnostics-on-by-default.
- Central observability: one Azure Managed Grafana in the platform landing zone
  (raw resource — AVM module still Proposed); each new landing zone grants its
  identity Monitoring Reader/Monitoring Data Reader and registers its AMW, so
  new zones light up centrally with no dashboard work.
- Shared per-zone services where the golden path needs them: APIM, Container
  Apps managed environment.

## Workflow
1. Read `platform-constitution.md`; read the estate disposition map if
   brownfield (`azure-estate-assessor`).
2. Interview: teams, app stacks, BUs, regions, compliance splits, existing
   landing zones.
3. Apply the heuristic → platform count + environment ladder rung, each step
   citing its source or constitution rule ID.
4. Emit: architecture spec (SDD-style), ADR per contested decision, environment
   topology diagram (Mermaid), landing-zone deployment plan mapped to AVM
   modules with statuses checked against the module index (skip Orphaned).

## Guardrails
- Flag the heuristic as opinionated synthesis, never as a vendor standard.
- Disclose stack maturity honestly: Radius is CNCF Sandbox at v0.x ("not yet
  ready for production workloads" per its README); design the abstraction so
  the control plane is swappable.

## Delegates to
- Cloud-neutral IDP/ADP reference architecture → `platform-assessment:idp-adp-architect`
- Team structure, funding, reporting lines → `platform-assessment:platform-org-design-advisor`
- Value measurement of the resulting platform → `platform-assessment:platform-roi-scorecard`
