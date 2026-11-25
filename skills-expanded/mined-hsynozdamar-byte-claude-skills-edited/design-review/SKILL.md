---
name: design-review
description: "Prioritized design critique of a UI (URL, screenshot or component), ranked blocking to polish, with a fix for each. Use when asked to review or critique a design, or check craft before shipping."
---

# design-review

A senior craft critique: opinionated and specific, not a checklist dump.

## 1. Get the artifact
- **Screenshot**: read it. Best for visual judgment.
- **Code**: read it plus related CSS/tokens. Enables `file:line` fixes and `--apply`.
- **URL**: WebFetch gives source, not a render. For visual judgment, ask for a screenshot and the viewport.
- With neither a screenshot nor code, ask before guessing.

## 2. Evaluate
Use the dimensions in [references/rubric.md](references/rubric.md) (load it for the review). Measure where possible (contrast ratios, line-height, measure in ch, target px, durations) instead of judging by feel.

## 3. Report, ranked
Lead with the few findings that matter. Each one gives:
- **What**: the issue (element or `file:line`)
- **Why**: one line on the craft or usability reason
- **Fix**: an exact change, not "increase spacing"

Tiers, most important first:
- **Blocking**: broken, inaccessible, fails WCAG AA, or unusable on a target device.
- **Important**: noticeably hurts hierarchy, readability, usability or consistency.
- **Polish**: refinement that sharpens the craft.

End with **Strengths** (2 to 4 things done well) and, if useful, the single highest-leverage change to make first.

## 4. Apply (optional)
With `--apply` or on request, edit the clear, safe findings (contrast, spacing values, focus states, reduced motion, semantic tags, alt text). Leave subjective or structural changes as recommendations until the user confirms. Re-verify values after editing.

## Tone
Direct and respectful, like reviewing a colleague's work; every problem comes with its fix. Calibrate depth to the surface: a marketing hero gets type and motion scrutiny, a form gets states and accessibility scrutiny.
