---
applyTo: "docs/plan/**/*.md"
---

<!-- type: reference -->

# Planning Surface

You are editing planning documents that define intended work, scope boundaries, and acceptance conditions.
Keep plans concrete, reviewable, and written in the repository's domain language.

## Structure rules

- Preserve the existing plan structure unless the task explicitly requires a reorganization.
- Keep headings, phase boundaries, and status markers legible so a reader can track what is proposed, what is implemented, and what remains open.
- Include explicit file targets when a plan item changes repository surfaces.
- Include acceptance criteria for each meaningful work item so the plan can be validated after implementation.

## Scoping rules

- Separate additive changes from breaking changes; do not blend compatibility-preserving work with contract-breaking work in the same unchecked bullet.
- State whether a task adds a new surface, refines an existing surface, or changes a supported contract.
- Keep dependencies and non-goals visible when they affect sequencing or rollout.

## Language rules

- Use the repository's domain terms: deterministic forecastability triage, readiness, leakage risk, informative horizons, primary lags, seasonality structure, covariate informativeness, and downstream hand-off.
- Do not describe the repository as a forecasting framework, model zoo, or replacement for downstream forecasting libraries; defer exact identity wording to `docs/wording_policy.md` when needed.
- Do not replace domain language with generic AI buzzwords, vague automation language, or empty platform phrasing.
- Prefer operational instructions that tell a coding agent what to create, update, preserve, or validate.

## Review checklist

- Does each planned item identify the target file or surface?
- Does each planned item include concrete acceptance criteria?
- Are additive and breaking changes separated clearly?
- Does the wording stay in forecastability-triage language instead of generic AI terminology?