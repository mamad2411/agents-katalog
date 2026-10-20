---
name: governance-audit
description: Use when assessing the workspace governance layer as a whole and producing a ranked, evidence-backed remediation report.
---

# Audit Governance

## Specialization

Run a workspace-level governance assessment and return a single report with coverage, standards outcomes, and prioritized remediation.

## Trigger Conditions

- Governance posture must be assessed across agents, instructions, prompts, skills, and catalogs.
- A periodic governance health check is requested.
- A restructuring event may have introduced drift.

## Inputs

- Workspace root path.
- Audit date (YYYY-MM-DD).
- Optional scope filter: all, agents, instructions, prompts, skills, catalogs.

## Required Outputs

- Governance report at `.docs/changes/governance/audits/governance-audit.md`.
- Coverage grid by lane.
- Standards grid for GOV-M* and GOV-S*.
- Ranked recommendations with priority and evidence.

#### Violation Code Legend

| Code Prefix | Standard | Type | Skill Source |
|---|---|---|---|
| GOV-M* | Mandatory governance check | MUST | governance-audit |
| GOV-S* | Advisory governance check | SHOULD | governance-audit |
| GOV-SK | Skill quality aggregate | Aggregate | governance aggregate source |
| GOV-CUS | Customization quality aggregate | Aggregate | governance aggregate source |
| GOV-OPT | Optimization factor coverage | Aggregate | governance aggregate source |
| SKR-M* | Mandatory skill quality check | MUST | governance aggregate source |
| SKR-S* | Advisory skill quality check | SHOULD | governance aggregate source |
| INR-M* | Mandatory instruction quality check | MUST | governance aggregate source |
| INR-S* | Advisory instruction quality check | SHOULD | governance aggregate source |
| AGR-M* | Mandatory agent quality check | MUST | governance aggregate source |
| AGR-S* | Advisory agent quality check | SHOULD | governance aggregate source |
| PRR-M* | Mandatory prompt quality check | MUST | governance aggregate source |
| PRR-S* | Advisory prompt quality check | SHOULD | governance aggregate source |
| OPR-M* | Mandatory optimization quality check | MUST | governance aggregate source |
| OPR-S* | Advisory optimization quality check | SHOULD | governance aggregate source |

## Standards

Core checks:
- GOV-M1 lane coverage
- GOV-M2 frontmatter validity
- GOV-M3 catalog integrity
- GOV-M4 lifecycle-governance coverage
- GOV-M5 skill self-containment: no cross-skill references (aligned with SKR-M4); each SKILL.md body must contain no invocations, delegations, or required-sub-skill directives pointing to other named skills
- GOV-S1..GOV-S11 advisory checks
- GOV-OPT optimization factor coverage across authoring and review routines
- GOV-S9 utilization coverage across skills, agents, and prompts
- GOV-S10 review recency threshold coverage for tracked assets
- GOV-S11 responsibility overlap threshold coverage across agents, instructions, prompts, and skills

Companion checks:
- Collect and reconcile GOV-SK outcomes from skill-quality evidence.
- Collect and reconcile GOV-CUS outcomes from customization-quality evidence.
- Collect and reconcile GOV-OPT outcomes from optimization evidence.

## Workflow

1. Inventory assets and read governance catalogs.
2. Run script-based checks from .github/scripts/powershell.
3. Evaluate GOV-M* first, then GOV-S*.
4. Pull GOV-SK, GOV-CUS, and GOV-OPT outcomes from available governance evidence artifacts.
5. Produce grids and prioritized remediation actions.

## Script Integration

Use these existing scripts:
- get-lane-counts.ps1
- test-catalog-integrity.ps1
- test-frontmatter-validity.ps1
- test-hub-file-sync.ps1
- test-governance-link-graph.ps1
- test-governance-artifact-contract.ps1
- test-utilization-coverage.ps1
- test-review-recency.ps1
- test-source-catalog-freshness.ps1
- test-responsibility-overlap.ps1

## Output Rules

- Use markdown grids for all outcomes.
- Mark MUST failures as High severity.
- Set final disposition to FAILED if any MUST check fails.

## Done Criteria

- All GOV-M* and GOV-S* checks executed with evidence.
- Report saved at required path.
- Recommendations mapped to specific failures or advisories.
- Source catalogs for sync-customizations and sync-skills are checked for freshness threshold drift.




