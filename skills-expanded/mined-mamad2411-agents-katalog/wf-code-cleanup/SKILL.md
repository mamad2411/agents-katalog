---
name: wf-code-cleanup
description: Recommend-only maintainability sweep of the whole codebase for dead code, duplication, complexity, abandoned files, and technical debt, producing keep/simplify/remove recommendations (Codebase cleanup review / Dead code review). It changes nothing itself; not a review of one artifact (wf-council) and not the open wave's required lanes (wf-review-wave).
---

# Codebase cleanup review (Wavefoundry skill)

This skill is a thin pointer: the workflow lives in `docs/prompts/codebase-cleanup-review.prompt.md`. Read that document and follow it; do not improvise the steps from this summary.

- The sweep is graph-based and recommend-only; it proposes, the operator disposes.
- Acting on a recommendation is ordinary lifecycle work (plan, admit, implement); never an inline mass deletion.
