---
name: design-review
description: Craft + UX review of a user-facing change before merge — visual hierarchy, accessibility floor, and AI-slop tells, against an approval bar. Use in the VERIFY phase for any change that touched a UI surface, parallel to /security-review. Judges by default; reports severity-tagged findings, does not rebuild unless asked.
---

# /design-review — craft & UX gate

Goal: prove a user-facing change is *crafted*, not merely *correct*, before it merges. The
design counterpart to `/harness-claude:security-review` — a conditional VERIFY gate that
blocks on Blockers. It checks the build against the design brief from `/harness-claude:design`
and the bar in `references` (`skills/design/references/review-bar.md` + `ux-floor.md`).

## When to use
**Only when the change touched a user-facing surface** (a page, screen, component, form,
email, CLI/TUI presentation). Internal/back-end changes **skip — say so**. Run it in parallel
with `/harness-claude:review` and `/harness-claude:security-review` when the change is both
UI- and security-sensitive.

## Do this
1. **Scope & intent.** Bound what's under review (the branch's UI diff, or a named surface).
   Read the `/harness-claude:design` brief if one exists, and the project's saved design-system
   note (e.g. `.design/system.md`) if present — **review against the design's own intent**, not a
   generic ideal. Apply the harness's review standard in `references/review-bar.md`.
2. **See the whole first** (squint, before line-picking): does one thing lead, or is it a
   parking lot? Does it breathe, or a monotone grid? Does it look like *this* product? The
   worst slop is compositional. Squint the *rendered* output, not the source — serve it over
   http and screenshot (a headless browser usually blocks `file://`); a picture is worth 1000 tokens.
3. **Run the lenses** independently (review-bar.md): Hierarchy · Type & color · Surfaces &
   depth · Composition & rhythm · States/polish/motion · Structure-reuse-content.
4. **Apply the floor** (ux-floor.md): a11y §1 + touch §2 are **hard gates** — contrast 4.5:1,
   visible focus, keyboard nav, 44px targets, reduced-motion. Automated checks catch ~30%; the floor
   isn't met until you've **manually exercised it** — keyboard-only through the whole flow, a screen
   reader (VoiceOver/NVDA) over the key path, and 200%/400% zoom without breakage. Cite the specific
   **WCAG success criterion** per failure (e.g. 1.4.3 contrast, 2.1.1 keyboard, 2.4.7 focus-visible).
   A failure here is a Blocker, full stop.
5. **Score and filter.** Tag each finding Blocker / Should-fix / Note. Cut false positives:
   taste, a bold choice working as intended, out-of-scope/untouched lines, anything
   `system.md` ratifies, lint/format concerns. A few high-conviction findings beat forty nitpicks.

## Severity → action
| Severity | Meaning | Action |
|----------|---------|--------|
| **Blocker** | Reads as generic/broken, or fails the a11y/touch floor | **BLOCK merge** — fix, re-review |
| **Should-fix** | Real craft gap a design lead would call out; still functions | Fix before merge when reasonable |
| **Note** | Minor | Optional |

Presumptive blockers (unless justified against intent): no focal point · size-only/defaulted
typography · monotone layout · timid/competing-accent palette · harsh/fragmented surfaces ·
missing states · structural hacks · an inaccessible hand-rolled control where a primitive
should be used · any a11y/touch floor failure.

## Output
A verdict (**approved** / **not approved**) + findings. For each: **what defaulted**, **why it
costs the user / reads generic**, the **specific crafted fix** (the decision, not a patch),
tagged with severity. Blockers first. **Judge by default** — rebuild only when the user asks;
when they do, rebuild from the decision (re-derive focal point / hierarchy / surfaces), not as
patches over defaults. For a fast "make it stop looking generated" pass instead of a full
review, run the deslop mode in `references/review-bar.md`.

## Exit criterion
No Blockers remain (or each is explicitly justified against intent), and the a11y/touch floor
passes. Then back to `/harness-claude:test` for any regression, or on to `/harness-claude:ship`.
