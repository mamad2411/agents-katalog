---
name: deep-codebase-review
description: >-
  Review an entire repository, its architecture, technical debt, or a substantial branch. Produce findings about boundaries, lifecycle, concurrency, duplication, tests, plans, and maintenance. Do not use this skill for small changes, narrow defects, or visual UI review. Do not use it for repository guidance or an OpenAI Agents SDK production review.
---

# Deep Codebase Review

Review the system structure and behavior. Do not review only isolated code. First, report specific risks. Then report structural conditions that can increase the cost of future changes.

## Workflow

### 1. Bound the review

- Identify the target. The target can be a whole repository, a merge-base diff, a branch, or a named set of modules.
- For a pull request or branch, inspect the diff first.
- Inspect dependencies, contracts, tests, and design documents only when they help you assess the change.
- State important scope exclusions and coverage limits in the report.

### 2. Establish intent

- Read repository instructions and the documents that apply to the scope. These documents can describe architecture, plans, roadmaps, or packages.
- When design guidance is absent, infer the intended structure from the implementation.
- Identify each inference.

### 3. Review All Major Areas Before Detailed Inspection

- Scan the relevant tree. Sample each major layer in scope before you inspect a possible problem in detail.
- Load [references/review-lenses.md](references/review-lenses.md) and select the review areas that apply to the system.
- Include tests and future plans when they define the intended contract.
- Include them when they conflict with that contract.
- For structural and maintenance assessment, read [references/design-for-change.md](references/design-for-change.md). Test one or two evidence-based likely changes against the current boundaries.
- Inspect representative calls for misleading ownership or effects. Keep naming preferences separate from specific maintenance risks.

### 4. Classify and verify

- Report an observation as a finding only when it has a specific harmful result. Examples include incorrect behavior, loss of data integrity, high maintenance cost, a design conflict, or a likely regression.
- Classify a possible future weakness without current harm as a future risk.
- Cite exact files and lines when possible.
- Explain how the defect or maintenance cost occurs.
- Identify assumptions.
- Before you recommend reuse, identify the repeated pattern and the boundary for a shared implementation.
- Test whether deletion, consolidation, derivation, or an existing capability can resolve the issue before proposing new code. Explain what disappears and which behavior remains.
- Compare present complexity with the benefit for likely changes. Retain a sufficient design when added flexibility has no demonstrated benefit.

## Model Guidance

When the harness lets you choose a model, use a model that has high code-analysis capability. Use high reasoning effort. The model must trace behavior. It must find evidence, check claims, and identify causes. If the harness does not have a reasoning setting, tell each reviewer to do detailed checks. Tell each reviewer to resolve important uncertainty.

## Council Mode

Use a small group of sub-agents by default for whole-repository reviews. Also use the group for substantial pull request or branch reviews. Use the group only when sub-agents are available. Load [references/council-review-protocol.md](references/council-review-protocol.md) before you delegate work.

If sub-agents are not available, state this limit. Continue with the same role-based reviews. Stop for confirmation only when the user required a council. Do not paste the specialist reports. Verify their evidence and combine it into one assessment.

## Output

Include only applicable sections. Keep the report proportional to the scope and findings. Use this order:

1. Findings ordered by severity.
2. Structural future risks and likely refactors.
3. Roadmap or design alignment.
4. Open questions and residual risk.
5. Follow-up actions with the highest verified benefit.

State when there are no specific findings. Report test gaps and future risks as separate items. Do not classify them as defects. For a report example, read [examples/review-output.md](examples/review-output.md).

## Follow-Through

- Prefer a small number of corrections that have clear evidence. Avoid broad cleanup and redesign without evidence.
- When the user requests fixes, update a planning document only if it is the authoritative future plan.
- Update that document only when the accepted change affects future work.
- Update it only when documentation changes are in scope.
- Keep forward-looking plans distinct from changelogs.
