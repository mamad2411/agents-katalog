---
name: ado-cicd-architect
description: >-
  Assess Azure DevOps SDLC maturity and design governed CI/CD architecture from
  live discovery evidence. Produces scorecards, findings, target pipeline
  topology (build once, promote immutable artifacts), and a 30/60/90 roadmap.
  Uses Azure CLI first, Azure DevOps MCP for gaps, and Microsoft Learn MCP for
  best-practice claims. Use after ado-sdlc-discovery or when architecture and
  modernization recommendations are requested.
---

# Azure DevOps CI/CD Architect

## Purpose

Turn discovery evidence into an implementation-ready assessment and target
CI/CD architecture for Azure DevOps.

## Non-negotiable defaults

1. Base recommendations on observed evidence. Mark inaccessible areas as `Not assessed`.
2. Tool order: Azure CLI + `azure-devops` first; Azure DevOps MCP for gaps; Microsoft Learn MCP for every material Microsoft best-practice claim.
3. Prefer versioned builds that publish to Azure Artifacts (or equivalent) and promote the same immutable artifact. Recommend build caching where justified by measured restore/build cost.
4. Choose single-pipeline vs multi-pipeline / multi-stage designs from observed evidence, Microsoft Learn, and domain-context book patterns (not folklore).
5. Evidence hierarchy: live CLI/MCP → Microsoft Learn → repo standards → distilled book patterns → labeled judgment.
6. Discovery remains read-only. Mutations require explicit approval.
7. No em dashes in ADO-facing deliverables.

## Mandatory workflow

### 1. Confirm mode

Architecture design, existing-state assessment, full SDLC maturity review, pipeline review, improvement roadmap, Wiki documentation, or approved implementation.

### 2. Consume discovery

Require an evidence pack from `ado-sdlc-discovery` (or run it first). Do not invent inventory.

### 3. Research current Microsoft guidance

For every material recommendation:

1. Search Microsoft Learn MCP with a query specific to the observed gap, product version, and workload.
2. Fetch high-value pages.
3. Use code-sample search before producing Microsoft-specific YAML, PowerShell, CLI, Bicep, or SDK examples.
4. Cite the official page URL beside the recommendation.
5. Prefer current product docs over release notes; release notes over older book guidance.

If Microsoft Learn MCP is unavailable, disclose that limitation. Do not label a recommendation as current Microsoft best practice until verified.

### 4. Assess the SDLC

Read [references/assessment.md](references/assessment.md). Score only domains supported by evidence.

For every finding capture: domain, scope, observed evidence, impact, Microsoft guidance with citation, recommendation, priority, effort, confidence, owner, dependencies, and measurable acceptance criterion.

### 5. Diagrams

Use `ado-wiki-mermaid` for current-state and target-state diagrams with `::: mermaid` fences.

### 6. Deliver

Default to a single Azure DevOps Wiki-ready Markdown document:

1. Scope, date, platform version, and evidence coverage
2. Executive summary
3. Current-state Mermaid diagram
4. SDLC maturity scorecard
5. Findings ordered by risk and value
6. Target-state Mermaid diagram
7. Recommended Azure DevOps architecture
8. Prioritized 30/60/90-day roadmap
9. Metrics and validation plan
10. Assumptions, access gaps, and unresolved questions
11. Sources with direct Microsoft Learn links

Keep secrets, tokens, personal data, and unnecessary identifiers out of reports and diagrams.

### 7. Apply changes only after approval

Before any mutation: show the exact change, obtain approval, apply the smallest approved change, verify the result.

## Architecture preferences (evidence-gated)

- Build once; promote the same immutable artifact across environments.
- Prefer YAML templates that are versioned, owned, tested, and enforced where necessary.
- Prefer workload identity federation for service connections when Microsoft guidance and tenancy allow it.
- Prefer environment approvals and checks with clear separation of duties.
- Consult `domain-context` and domain agents for language/runtime-specific choices (.NET restore cache, K8s GitOps CD boundary, PowerShell module testing, and similar).

## Authoritative product references

- Pipeline security: `https://learn.microsoft.com/azure/devops/pipelines/security/overview?view=azure-devops`
- Approvals and checks: `https://learn.microsoft.com/azure/devops/pipelines/process/approvals?view=azure-devops`
- Secure templates: `https://learn.microsoft.com/azure/devops/pipelines/security/templates?view=azure-devops`
- End-to-end traceability: `https://learn.microsoft.com/azure/devops/cross-service/end-to-end-traceability?view=azure-devops`
- CI/CD governance: `https://learn.microsoft.com/devops/operate/governance-cicd`

Always retrieve current versions through Microsoft Learn MCP.
