---
name: ux-ui-review
description: >-
  UX/UI usability checklist: user flows, forms, wireframe alignment,
  accessibility, and mobile. Use with ux-reviewer subagent after QA pass on
  user-facing features.
---

# UX / UI Review

Validates **usability and design quality** of implemented UI — complementary to QA (functional AC), marketing (copy authoring), and SEO (landing metadata/headings).

## Audience & language

- Primary persona: as defined in `docs/PRODUCT_VISION.md` / `project-context`.
- **Respondent-facing UI** must match the UI language in `project-context` — flag wrong-locale leaks, jargon, or tone that undermines trust.
- Admin UI may differ; still evaluate clarity.

## Review method

1. Read wireframes or design docs for the affected screen(s) when they exist.
2. Walk the happy path and 2–3 error/edge paths (empty required field, back navigation, slow load).
3. Test **desktop** (~1280px) and **mobile** (~390px).
4. Note findings with **screen name + step** and severity.

Optional: use Playwright UI mode or browser tools; reference routes from `05-implementation-frontend.md`.

## Heuristic checklist (Nielsen-inspired)

| #   | Heuristic                   | Checks                                                                         |
| --- | --------------------------- | ------------------------------------------------------------------------------ |
| 1   | Visibility of system status | Progress; loading states; save/submit feedback                                 |
| 2   | Match real world            | Labels match user language (not dev terms); outcomes explained plainly         |
| 3   | User control                | Back without losing data; clear skip/cancel where product allows               |
| 4   | Consistency                 | Same button labels; heading hierarchy; spacing/typography across steps         |
| 5   | Error prevention            | Required fields marked; validation before advance; confirm destructive actions |
| 6   | Recognition over recall     | Options visible; helper text on complex steps                                  |
| 7   | Flexibility                 | Optional fields and skip paths where product allows                            |
| 8   | Minimalist design           | One primary CTA per screen; scannable results                                  |
| 9   | Error recovery              | Messages say _what_ failed and _what to do_                                    |
| 10  | Help & documentation        | Trust/privacy where needed; tooltips on complex controls                       |

## Forms & multi-step flows

- Progress indicator present and accurate.
- Tab order and keyboard: primary action reachable.
- Long forms: chunk by step; avoid walls of inputs unless designed that way.
- Results: headline outcome first; clear next CTA.

## Visual & layout

- Adequate touch targets on mobile (≈44px min for primary controls).
- Contrast readable (WCAG AA target).
- Empty/loading/error states designed — not blank screens or raw JSON errors.

## Accessibility (MVP bar)

- Headings reflect page structure (`h1` once per view).
- Form inputs have associated labels (visible or `aria-label`).
- Focus visible on interactive elements.
- Images: alt text when informative; decorative images empty alt.

## Verdict guidance

| Verdict     | Meaning                                                                              |
| ----------- | ------------------------------------------------------------------------------------ |
| **PASS**    | Usable; only nice-to-have notes                                                      |
| **IMPROVE** | Usability friction — should fix before wider release                                 |
| **BLOCKER** | Confusing flow, broken mobile, wrong-locale copy, missing progress/errors — must fix |

## Return routing

| Finding                                    | Return to                                          |
| ------------------------------------------ | -------------------------------------------------- |
| Layout, components, states, a11y structure | `frontend-developer`                               |
| Copy tone, labels, trust messaging         | `marketing-specialist` → then `frontend-developer` |
| Both layout and copy                       | `both`                                             |

After fix: `/qa-tester` (if interaction changed) → `/ux-reviewer` re-review.

## Anti-patterns to flag

- Wrong language on public user-facing pages
- No feedback after submit/save
- Dead-end screens (no back, no next, no explanation)
- Misleading claims or fake metrics in UI
- Tiny click targets on mobile
- Primary and secondary CTAs visually equal weight
