---
name: optimize-customizations
description: Use when authoring or reviewing agents, instructions, skills, and prompts to apply concise, deterministic optimization checks and produce actionable remediation.
---

# Optimize Customizations

## Specialization

Evaluate and improve authoring quality for `.agent.md`, `.instructions.md`, `.prompt.md`, and `SKILL.md` assets.

This skill is on-demand and review-focused. It does not run continuously and does not replace lane-specific specialist skills.

## Trigger Conditions

- A customization artifact is being created or edited.
- A governance or quality review needs optimization coverage.
- Drift is suspected in clarity, brevity, or deterministic guidance quality.

## Inputs

- Target scope: one artifact or a batch across agents, instructions, prompts, and skills.
- Review date (`YYYY-MM-DD`).
- Optional focus area: clarity, brevity, determinism, duplication, or cross-asset consistency.

## Required Outputs

- Optimization review artifact at `.docs/changes/customization/reviews/governance-audit-types-optimization.md`.
- Consolidated results grid with one row per reviewed artifact.
- Ranked remediation grid with concrete edits and priority.

#### Violation Code Legend

| Code Prefix | Standard | Type | Skill Source |
|---|---|---|---|
| OPR-M* | Mandatory optimization quality check | MUST | optimize-customizations |
| OPR-S* | Advisory optimization quality check | SHOULD | optimize-customizations |
| GOV-OPT | Optimization factor coverage | Aggregate | consolidated governance reporting |

## Assets

- Use [README.md](./references/README.md) for available reusable references.
- Use [optimization-factor-template.md](./references/optimization-factor-template.md) when generating the optimization review artifact.

## Workflow

1. Inventory target customization artifacts in scope.
2. Evaluate each artifact for optimization quality using OPR-M* and OPR-S* checks.
3. Record findings in a consolidated grid (pass, fail, advisory).
4. Produce remediation actions with exact target files and expected outcome.
5. Document follow-up edits directly in the ranked remediation grid with explicit target files and priorities.

## Optimization Review Standards

| ID | Standard | Type | Pass Criteria | Failure Action |
|---|---|---|---|---|
| OPR-M1 | Scope purity | MUST | Artifact keeps one primary objective and avoids role bleed. | Mark failed and split or refocus scope. |
| OPR-M2 | Deterministic wording | MUST | Guidance uses testable, concrete directives without ambiguity. | Mark failed and provide replacement wording. |
| OPR-M3 | Non-contradiction | MUST | Artifact does not conflict with active governance instructions or catalogs. | Mark failed and route conflict remediation. |
| OPR-M4 | No cross-skill delegation | MUST | SKILL.md bodies contain no invocations, required-sub-skill directives, or workflow steps that delegate execution to another named skill. | Mark failed; inline required content or introduce a dedicated orchestrator skill as the indirection layer. |
| OPR-S1 | Brevity | SHOULD | Wording is economical and avoids repeated sections or narrative padding. | Record advisory and propose concise reductions. |
| OPR-S2 | Reuse over duplication | SHOULD | Reusable references are preferred when they improve clarity and maintainability. | Record advisory and suggest reference consolidation. |
| OPR-S3 | Output clarity | SHOULD | Required outputs are explicit, complete, and easy to validate. | Record advisory and propose output contract tightening. |

## Done Criteria

- Reviewed artifacts are documented in the optimization-factor report.
- MUST failures are explicit, evidence-backed, and prioritized.
- Recommended remediations are actionable and mapped to concrete artifact edits.



