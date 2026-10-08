---
name: q-plan-tech-foundation
description: "Define or reconcile a project's stack, versioned technology guidance, NFRs, security, testing, deployment, and operations from product requirements, repository evidence, and user decisions. Use for stage 2, when a later stage invalidates a technical choice, or when the selected stack changes. Requires the q-core-contract companion. Part of the Quasar AI delivery skills."
---

# Technical foundation definition

Create or update the project's canonical technical foundation. The workflow is profile-driven: recommend technologies from requirements and evidence, keep the user in charge of selection, and declare coverage gaps instead of treating one stack as mandatory.

Read the `q-core-contract` companion for shared governance; if it is missing, stop and install it with `npx skills add flaviogragnolati/ai-workflow --skill q-core-contract`. In orchestrated mode, write only the owned technical foundation and return its delta; the root orchestrator updates global state and `technical_foundation_ref`.

## Required inputs

- a baselined or sufficiently mature product core;
- applicable proposal constraints and technical commitments;
- repository evidence when a codebase exists;
- hosting, security, compliance, interoperability, performance, and operational constraints known so far;
- the current technical foundation, decisions, risks, and change requests when reconciling.

Separate observed repository facts, user mandates, workflow recommendations, assumptions, and unresolved choices. Preserve an existing stack unless requirements or evidence justify a migration.

## Modes

Use exactly one mode:

- `initial-definition`: create the first `Working` technical foundation and make downstream readiness explicit.
- `reconcile-and-update`: create a new version when later requirements, architecture, repository evidence, or an approved user decision changes technical meaning. Never rewrite a `Baselined` version in place.

Complete mode selection when the current artifact version, change trigger, and write scope are explicit.

## Selection procedure

1. Classify the product shape and lifecycle: existing or greenfield; web application, headless API, distributed system, embedded software, performance-critical workload, or another evidenced shape.
2. Derive evaluation criteria from requirements and NFRs before naming technologies.
3. Inspect the repository and deployment environment. Treat installed technologies and working conventions as evidence, not accidental mandates.
4. Evaluate an explicit user proposal against the criteria. Preserve it when it fits; surface concrete trade-offs or incompatibilities when it does not.
5. For a suitable greenfield web application without a mandated stack, read [`references/web-stack-recommendation.md`](references/web-stack-recommendation.md) and present its advisory T3 Core recommendation plus only the secondary options whose applicability conditions hold.
6. For another product shape, or when the web recommendation does not fit, compare viable alternatives using current primary sources such as official documentation, specifications, first-party source, or vendor support policies. When `durable-supporting-investigation-of-stack-alternatives-or-vendor-support-policies-is-warranted` and `q-code-research` is installed, route the bounded question there; if it is absent, `record-the-bounded-comparison-in-the-technical-foundation-and-name-the-research-gap`.
7. Obtain user confirmation for the core stack and every material secondary technology. Do not infer approval from the absence of an objection.
8. Record the selected profile, rejected alternatives, rationale, consequences, exceptions, risks, and evidence.

Complete selection when the chosen technologies satisfy the accepted criteria, the user has confirmed material choices, and uncertainty that could change architecture is either resolved or blocking.

## Canonical output

Create or update `docs/development-workflow/technical/02-technical-foundation.md` using [`assets/technical-foundation-template.md`](assets/technical-foundation-template.md). Register it as an authored canonical artifact for stack selection, versioned technology guidance, NFR and operational fit, testing strategy, and environment expectations.

The artifact must include:

- artifact identity, lifecycle, version, `as_of`, and source versions;
- product shape, constraints, architecture drivers, and NFR evaluation criteria;
- recommended and selected profiles with `selection_source`;
- concrete technologies and versions by capability;
- adopted recommendations, pitfalls, and antipatterns with stable IDs and applicability;
- real project commands and quality signals discovered from the repository;
- security, privacy, testing, observability, operations, recovery, environments, deployment, and migration expectations;
- for a product with a user interface, the visual platform, UI or component library, styling and documentation tooling, the accessibility target, and the design-token format and validator with their exact versions and real project command;
- decisions, alternatives, trade-offs, risks, assumptions, exceptions, and unresolved items;
- requirement, ADR, repository, and external-source traceability;
- a reference register with documentation owner, URL, applicable version, access date, and supported guidance IDs.

External references support the artifact; they do not choose the stack. Prefer concise paraphrases and links over copied documentation. Mark guidance unverified when its applicable version or source cannot be confirmed.

## Reconciliation and ownership

`q-plan-design-system` consumes these interface selections and turns them into reusable design contracts; it never chooses the library, tooling, format, or accessibility target itself. Record `WCAG 2.2 Level AA` as the web default unless a contract, regulation, or platform requires another target, and add the platform's own standards for a non-web product. Confirm a token-format validator only when the project will genuinely run it; an absent validator is a declared coverage gap downstream, not a reason to invent a dependency.

When a downstream stage discovers a conflicting technical constraint, it returns the affected requirement or decision IDs, marks the current technical foundation stale when appropriate, and routes `reconcile-and-update` here. Reconcile connected ADRs and application standards through their owners; reference them rather than copying their decisions.

After a successful orchestrated run, return the authored or updated artifact ID and version so the orchestrator can write `technical_foundation_ref`. A standalone run always requires later reconciliation.

## Gate

Return `completed` only when architecture-driving selections are confirmed, versioned, evidence-backed, traceable, and sufficient for the next stage. Return `completed_with_warnings` when work can proceed under explicit, bounded coverage gaps. Return `blocked` only for an unresolved decision, unmet requirement, unavailable execution capability, or evidence gap that would make downstream work or technical approval unsafe.

Never block solely because the selected stack is not T3, and never issue a stack-specific approval from generic criteria alone.

Return a valid `stage_result`; the orchestrator alone updates workflow state and the artifact index.
