---
name: cross-device-check
description: Audits a game's UI and interaction across supported viewports, aspect ratios, pixel densities, orientations, and input capabilities. Use when mobile, tablet, desktop, controller, keyboard, pointer, or touch support is being checked; UI clips, overlaps, blurs, or overflows; controls are unreachable or hard to use; resizing or orientation changes break layout; or an explicit pre-release device-coverage pass is requested. Reproduces each issue on the relevant target and reports severity, evidence, exact trigger conditions, and fixes while distinguishing observed from source-inferred findings.
---

# Cross-Device Check

Test the supported environment, not a device label. Reproduce each defect under the
capabilities and display conditions that trigger it.

## 1. Establish the support matrix

Inspect the engine or runtime, build and run commands, declared platforms, internal
resolution and scaling policy, UI system, safe-area handling, and supported input
capabilities. Read project configuration and distribution targets before assuming that
phone, desktop, or controller support is required.

If the support matrix is missing, infer it from the delivery environment and state the
assumption. Ask the user when choosing the wrong platform would materially change the
work. For an otherwise unspecified browser game, use
[device-baselines.md](references/device-baselines.md) as a provisional matrix.

## 2. Reproduce the matrix

Run the game under each relevant combination of:

- viewport and aspect ratio;
- orientation and live resize;
- pixel density, UI scale, and safe-area inset;
- touch, pointer, keyboard, controller, and supported hybrid combinations;
- input changes during a session, when the platform permits them.

Prefer real devices or the engine's simulator. Viewport emulation proves only the
conditions it actually emulates. If the game cannot run, inspect source and label every
finding inferred rather than observed.

## 3. Check the experience

**Layout.** Check the play area, HUD, menus, overlays, and system UI at the narrowest,
widest, shortest, and tallest supported shapes. Verify orientation changes and resizing
after load.

**Rendering.** Check logical-to-physical pixel scaling, fixed-resolution scaling or
letterboxing, texture and text sharpness, and changes in pixel density.

**Input.** Make every action and menu reachable by every input the support matrix
promises. Check keyboard focus, controller navigation, pointer precision, touch
reachability, simultaneous inputs, and transitions between active inputs. Preserve
on-screen controls according to supported capabilities or player preference rather
than inferring them from “mobile” versus “desktop.”

**Safe interaction.** Follow the project's platform and accessibility requirements.
When none exist, use the heuristics in
[device-baselines.md](references/device-baselines.md). Ensure a finger does not obscure
critical feedback while pressing and that controls avoid notches, rounded corners, and
system gestures.

**Readability.** Check text size, contrast, glyph rendering, line wrapping, clipping,
and text drawn over changing gameplay backgrounds.

**Feedback.** Confirm immediate acknowledgement of input and a meaningful state for
perceptible or indeterminate waits. Make damage, score, selection, loading, and game-over
state changes legible through more than an unnoticed number.

**First screen.** Open from a clean state and verify that the first available action is
discoverable. This check covers first-screen communication, not the depth of onboarding.

## 4. Report and fix

Report one row per defect:

| Defect | Exact trigger | Evidence | Status | Severity | Fix |
|---|---|---|---|---|---|
| Score HUD covers play | 360 × 800, portrait, touch | screenshot or source location | observed | blocks play | move inside safe area |

Use **blocks play**, **degrades play**, or **polish**, ordered by severity. An inferred
finding remains a suspicion until reproduced.

Apply fixes only when the user requested changes or approves them. Re-run the failing
condition and adjacent matrix cases; a layout fix at one size often breaks another.

## Constraints

- Preserve the game's visual direction and deliberate art choices.
- Use the project's existing UI system; solve local defects without introducing a new
  framework by default.
- Support capability combinations instead of hiding one input merely because another
  is present.
