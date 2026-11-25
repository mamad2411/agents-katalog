---
name: docker-dotnet-source-curation
description: Use when Docker .NET guidance must be curated from official sources, tracked for freshness, and converted into reusable skill-ready references with drift controls.
---

# Docker .NET Source Curation

## Specialization

Curate and maintain official-first Docker .NET reference sets so all related skills remain accurate, current, and reusable.

## Trigger Conditions

- New Docker .NET skill content is being authored or refreshed.
- Existing references may have drifted from official documentation.
- Teams need deterministic source-ledger and freshness controls.

## Scope Boundaries

In scope:

- Source discovery, tiering, and relevance mapping.
- Source freshness and drift checks.
- Reusable source-ledger and review templates.

Out of scope:

- Non-source implementation guidance.
- Product runtime troubleshooting.

## Required Inputs

- Target Docker .NET topic area.
- Desired depth and coverage expectations.
- Existing reference assets and update cadence.

## Required Outputs

- Source ledger with tiering and relevance notes.
- Drift assessment and remediation actions.
- Reusable curation templates and automation script.

## Deterministic Workflow

1. Collect candidate sources and classify by tier.
2. Prioritize official sources for normative guidance.
3. Record source relevance by topic branch.
4. Evaluate freshness against update threshold.
5. Publish drift findings and required updates.

## Decision Rules

- Normative rules must come from official standards/vendor docs.
- Community sources are corroborative only.
- Expired or superseded sources require explicit remediation entries.

## Anti-Pattern Checks

- Skill guidance without source links.
- Tier mixing where community guidance overrides official docs.
- No freshness timestamp or reassessment plan.

## Self-Contained Assets

- Sample code: [source-ledger.example.md](./references/examples/source-ledger.example.md)
- Sample configuration: [source-tier-policy.sample.yaml](./references/templates/config/source-tier-policy.sample.yaml)
- Template: [source-review-checklist-template.md](./references/templates/source-review-checklist-template.md)
- Checklist: [docker-dotnet-family-source-refresh-checkpoint.md](./references/checklists/docker-dotnet-family-source-refresh-checkpoint.md)
- Script: [check-source-freshness.ps1](./references/scripts/check-source-freshness.ps1)

## Done Criteria

- Official-first source ledger is complete.
- Freshness and drift status are explicit.
- Reusable curation assets are available.

## Inputs

- Request objective and scope boundary.
- Applicable constraints and risk context.

## Workflow

1. Capture inputs and constraints.
2. Execute this skill's deterministic steps.
3. Publish outputs with status and next actions.

## Execution Context
### Input Context

- Request objective and scope boundary.
- Applicable constraints and required outputs.

### Process Context

- Follow this skill's deterministic workflow from intake to closure.
- Record ownership and decisions for required outputs.

### Output Context

- Deliverables with explicit completion status.
- Residual risks and next actions.
## References Assets

- [Reference assets](./references/README.md)
