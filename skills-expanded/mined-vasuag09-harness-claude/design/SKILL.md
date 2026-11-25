---
name: design
description: Produce a product/UX/UI design brief before building a user-facing surface. Use in the PLAN phase after /plan, alongside /architect, when a change has a UI (dashboard, app, marketing page, mobile screen). Routes to the right craft rubric, overlays the accessibility/UX floor, and emits a brief that guides implementation. Self-skips when there is no user-facing surface.
---

# /design — product/UX design brief

Goal: decide *what this should look like and how it should behave* before code, so design
isn't improvised inside `/harness-claude:implement` (where it comes out worst). The product-design
counterpart to `/harness-claude:architect` (system design). Both are conditional PLAN steps —
a change can need one, both, or neither.

## When to use
**Only when the change has a user-facing surface** — a page, screen, component, dashboard,
form, email, or CLI/TUI presentation a human looks at. If the work is internal/back-end
(an API, a script, a refactor with no visible change), **skip and say so** — like
`/harness-claude:architect` skips routine work. The harness itself (a CLI plugin) skips this step.

## Do this

### 1. Route by surface
Pick the leading craft rubric from the change's surface, then **always** overlay the floor:

| Surface | Lead rubric |
|---------|-------------|
| Product UI — dashboard, admin, SaaS, tool, settings, data | `references/product-ui.md` |
| Marketing / brand / landing / portfolio / expressive | `references/aesthetic-direction.md` |
| Mobile / native (iOS/Android, React Native, Flutter) | `references/ux-floor.md` (+ closest of the two above) |
| **Every** surface (overlay, not optional) | `references/ux-floor.md` |

Read the leading rubric(s) under `skills/design/references/`. These are the harness's own design
standard and are fully self-contained — no external plugin or install is required. If the project
keeps a saved design-system note (e.g. `.design/system.md`), read it too and hold to its decisions.

### 2. Explore before proposing (don't default)
Per the lead rubric: name the **human** (who, where, what they did 5 min before/after), the
**task** (the verb), and the **feel** (in words that mean something). For product/marketing,
do the domain exploration — domain · color-world · signature · the 3 defaults you're rejecting.
*Test:* remove the product name from your proposal — could someone still tell what it's for?

### 3. Emit the design brief
Keep it to one screen. This is the artifact `/harness-claude:implement` builds against, and
what `/harness-claude:design-review` later checks the build against.

```
# Design brief: <surface>
Human:      [who, where, prior/next action]
Task:       [the verb — what leads, what hides]
Feel:       [3–5 words that mean something; not "clean and modern"]
Surface:    [product UI | marketing | mobile] → [lead rubric]
Direction:  [domain · color-world · signature · rejected defaults]
Hierarchy:  [focal element + how it wins; type scale; density in px]
System:     [palette w/ why · type pairing · depth strategy (one) · spacing base]
Floor:      [a11y/touch/perf items that apply — from ux-floor.md]
States:     [the default/hover/focus/disabled + loading/empty/error this surface needs]
Success:    [observable signals — what "it works + looks designed" looks like]
```

## Constraints
- **Never trade the floor for aesthetics.** ux-floor §1 (a11y) + §2 (touch) are part of the
  harness accuracy floor — contrast, focus rings, keyboard nav, 44px targets are non-negotiable.
- Don't hand-roll controls a primitive should own (see product-ui.md "Use what exists").
- Lean: the brief is a working brief, not a spec novel. Confirm direction with the user only
  when it's ambiguous or costly to change; otherwise state a responsible assumption and proceed.

## Output
The design brief above (saved to the session file for multi-session work via
`/harness-claude:save-session`), plus a one-line note of which rubric/skill led and what you
overlaid. If there's no user-facing surface: say "skipped — no UI surface" and move on.

## Exit criterion
A design brief with a named focal point, a committed system (palette/type/depth/spacing), the
applicable floor items, and required states — concrete enough to build and to review against.
Then `/harness-claude:architect` (if also warranted) or `/harness-claude:harness-implement`.
