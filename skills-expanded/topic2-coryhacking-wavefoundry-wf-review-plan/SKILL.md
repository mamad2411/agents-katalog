---
name: wf-review-plan
description: Review a change doc, or the current wave record when no change is specified, before implementation by walking every unresolved decision branch one question at a time. The Review plan workflow; distinct from Review wave.
---

# Review a plan (Wavefoundry skill)

This skill is a thin pointer: the workflow lives in `docs/prompts/review-plan.prompt.md`. Read that document and follow it; do not improvise the steps from this summary.

- Review the named change doc, or fall back to the current wave record when no change is specified; this may run before or after admission, but only before implementation.
- Self-answer from project resources first; surface only the questions that genuinely need operator judgment.
- This optional review records no typed signoff and satisfies no lifecycle gate; use `wf-review-wave` for the open wave's required delivery-review lanes.
