---
name: validate-change-plan
description: Validate one epic-scoped or standalone story or bugfix change plan before implementation. Use after `add-story` or `add-bugfix` to confirm or correct the selected artifact's `Ready` or `Blocked` state.
---

# Validate Change Plan

## Core Rule

Validate the written story or bugfix plan, not memory. Confirm exactly one change plan is ready to feed `implement-change`: it fits its selected placement, has complete implementation tasks, concrete verification, and no blocking open questions. Keep the selected artifact state aligned with the result: passing plans are `Ready`; non-passing plans are `Blocked` with `Blocked By` filled. Follow [references/clarification-policy.md](references/clarification-policy.md).

## Workflow

1. Load validation context:
   - When the user has not provided a specific artifact path, run this skill's `scripts/list-unvalidated-plans.sh <target-repo-root>` to find `Ready` or `Blocked` stories and bugfixes whose `Change Plan Validation` decision is missing or not `Pass`; use that filtered list to choose or ask for the single plan to validate.
   - Read one epic-scoped story or bugfix under `docs/epics/active/<epic>/story_*.md` or `docs/epics/active/<epic>/bugfix_*.md`, or one standalone story or bugfix under `docs/standalone-changes/active/story_*.md` or `docs/standalone-changes/active/bugfix_*.md`.
   - For epic-scoped work, read `docs/epics/active/<epic>/epic.md` and its source Product Vision when present.
   - For standalone work, read `docs/vision.md` when present, active epics under `docs/epics/active/`, and sibling standalone changes under `docs/standalone-changes/active/`.
   - Read relevant concern specs, sibling stories, sibling bugfixes, and code evidence when they affect scope, placement, or verification.

2. Validate placement fit:
   - For epic-scoped work, check that the selected story or bugfix stays inside epic scope and does not contradict the Product Vision, epic, concern specs, or sibling stories or bugfixes.
   - For standalone work, check that the routing decision explains why no active epic fits, why no new epic is needed, and how the work stays consistent with Product Vision, concern specs, and sibling standalone changes.
   - Check that any scope change, public behavior change, rollout change, material risk, or durable product direction change is reflected in the owning artifact; otherwise mark the item `Blocked` or `Fail` and recommend `add-story`, `add-bugfix`, `create-epic`, or `define-product-vision` as appropriate.

3. Validate change plan readiness:
   - For stories, check acceptance criteria, regression boundaries, implementation tasks, verification matrix, assumptions, and open questions.
   - For bugfixes, check current behavior, expected behavior, unchanged behavior, reproduction evidence, root cause, fix boundary, regression risks, implementation tasks, and verification matrix.
   - Check that every implementation task has purpose, scope, dependencies, verification steps, and pass criteria.
   - Check that verification methods are concrete enough to execute during `validate-implementation`.

4. Update validation status:
   - Update the selected story or bugfix's `Change Plan Validation` section with evidence, gaps, skipped checks, and a decision: `Pass`, `Fail`, `Partial`, or `Blocked`.
   - Set `State: Ready` when the decision is `Pass`.
   - Set `State: Blocked` and fill `Blocked By` with the concrete plan gap, dependency, question, or validation blocker when the decision is `Fail`, `Partial`, or `Blocked`.
   - Set `Blocked By: N/A` when the artifact is `Ready`.
   - Add remediation implementation tasks or notes when coverage or verification is missing.
   - Do not implement code; implementation belongs to `implement-change`.

5. Report result:
   - Summarize validation outcome, placement fit, coverage gaps, verification gaps, and blocking open questions.
   - Recommend `implement-change` when the result is `Pass`; otherwise recommend the specific artifact skill needed to fix the gap.

## Validation Checklist

- [ ] Selected story or bugfix fits its active epic, or standalone routing is justified and evidence-backed.
- [ ] Selected story or bugfix does not contradict sibling stories or bugfixes.
- [ ] Every acceptance, expected behavior, or unchanged behavior criterion has verification coverage.
- [ ] Every implementation task has concrete verification and pass criteria.
- [ ] Blocking open questions are resolved or recorded as `Blocked`.
- [ ] Result includes an overall decision: `Pass`, `Fail`, `Partial`, or `Blocked`.
- [ ] State is aligned to `Ready`, or `Blocked` with a concrete `Blocked By` value.
- [ ] Passing change plan can feed `implement-change`.
