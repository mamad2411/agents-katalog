# Game UI Testing

## Purpose
Verify game user interfaces across controller, keyboard, and touch input: deterministic focus navigation, safe-area compliance on all target resolutions, localization robustness (text expansion, RTL, font fallback), and correct UI state transitions under real frame-timing conditions.

## Use when
- Testing menu flows, HUD elements, dialogs, pause screens, or settings screens navigated with gamepad, keyboard, or touch.
- Validating title-safe and action-safe areas, resolution scaling, and aspect-ratio handling (16:9, 21:9, 4:3, portrait).
- Checking localized builds for text overflow, truncation, missing glyphs, or mirrored-layout defects.
- Auditing UI state machines for stuck states, double-activation, or input loss during scene transitions.

## Do not use when
- Testing web or desktop application UI rendered in a browser DOM (use `playwright-ui`).
- Profiling frame rate, draw calls, or GPU cost of UI rendering (use `performance-native`).
- Designing visual style, tokens, or layout systems from scratch (use `design-system`).

## Required context
- Target platform list with resolutions and DPIs (e.g., 1920x1080 TV, 1280x720 handheld, 3840x2160 monitor).
- Input map: gamepad bindings, keyboard shortcuts, and touch gestures that drive UI focus.
- UI screen inventory with focus graphs and state-transition diagrams.
- Locale list under test (e.g., en-US, pt-BR, ja-JP, ar-SA) plus the localization pipeline (gettext, CSV, localization service).

## Procedure
1. **Inventory screens and focus graphs**: Enumerate every screen (title, main menu, options, pause, game over, store). For each, record the initial focused control and the four-directional focus neighbors of every focusable widget.
2. **Automate directional navigation sweeps**: Drive synthetic input (e.g., Godot `--headless` GUT tests sending `Input.action_press("ui_right")`, Unreal Gauntlet `ClickOnWidget` sequences) covering all focus paths; assert no focus traps, no focus loss to non-focusable space, and visible focus indicator on every stop.
3. **Verify safe areas and scaling**: Render each screen at every target resolution with safe-area debug overlay enabled. Assert no interactive control lies outside the action-safe rectangle (3.5% inset) and no critical text outside title-safe (5% inset); verify anchor presets keep layouts intact at 21:9 and 4:3.
4. **Run pseudo-localization and locale passes**: Expand source strings by 40% with accented padding (`[!!! Strïng !!!]`), switch to ja-JP and ar-SA builds, and assert zero clipped labels, zero missing-glyph tofu boxes, and correct RTL mirroring of navigation bars and progress direction.
5. **Exercise state transitions under load**: Trigger pause/resume, modal stacking, and scene changes while frame time is artificially clamped to 50 ms; assert each transition completes within 500 ms of input, exactly one screen holds input focus, and no duplicate activation events fire.
6. **Capture screenshot evidence**: Store per-screen, per-resolution, per-locale screenshots (PNG) plus a pixel-diff report against baselines with acceptance threshold at or below 0.5% differing pixels; run `scripts/verify.sh` to confirm artifact completeness.

## Decision rules
- **Focus must never be homeless**: At any moment exactly one focusable control owns focus while a screen is active; focus loss to void is a blocking defect.
- **Safe-area violations block release**: Any interactive element outside action-safe on a declared target resolution fails the gate.
- **No hard-coded pixel layouts**: All positioning must use anchors, containers, or layout groups; absolute pixel offsets for dynamic text are forbidden.
- **Localization overflow is functional, not cosmetic**: Clipped or overlapping localized text is a P1 defect, never a polish backlog item.
- **State transitions are single-fire**: Double activation from one confirm press (gamepad A bounce, key repeat) must be debounced at the state-machine layer.

## Evidence required
- Focus-sweep logs showing full traversal of every screen with zero traps or losses.
- Safe-area screenshot set with overlay enabled for each target resolution.
- Pseudo-localization plus ja-JP and ar-SA screenshot evidence with overflow report.
- Completed `templates/game-ui-testing-spec.md` with per-screen verdicts.
- Passing execution log from `scripts/verify.sh`.

## Output contract
- UI test specification document with screen inventory, focus graphs, and per-locale verdicts.
- Automated navigation and transition tests integrated into the game's test suite.
- Screenshot baselines and pixel-diff report archived with the build under test.

## Stop conditions
- All inventoried screens pass focus, safe-area, localization, and transition gates with evidence.
- Zero P1 defects open; remaining minors triaged with owner and milestone.
- Token budget exhausted.
- Blocked on external dependency.

## Escalation rules
- Escalate to the UI/UX owner if a focus-graph redesign is required (missing screens, ambiguous navigation intent).
- Escalate to the localization lead if font fallback or shaping defects need new font licensing or engine-level text-stack changes.
- Escalate to the lead engineer immediately if input loss or double-activation indicates an engine input-system bug rather than content error.
