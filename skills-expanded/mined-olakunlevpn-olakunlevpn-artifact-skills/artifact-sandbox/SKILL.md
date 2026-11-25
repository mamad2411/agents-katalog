---
name: artifact-sandbox
description: OUTPUT IS ALWAYS A SINGLE `.html` FILE (never `.md`, never separate CSS/JS files) containing a live, tunable demo of one CSS/JS technique. Use this skill whenever the user asks for an animation playground, animation sandbox, "let me tune the easing", "show me different timings of X", interactive demo of one effect, CSS demo, transition tuner, or any artifact whose primary shape is "one thing animating, with sliders to tune it". Pair with `artifact-css` for the underlying design system and `jQuery 4.0.0 + jQuery UI 1.14.2` for the slider widgets. Do NOT use for full editor UIs (use `artifact-editor`) — sandbox is single-effect focused.
---

# artifact-sandbox

> ## OUTPUT CONTRACT
>
> **Produces ONE `.html` file.** A sandbox is a single tunable demo of one CSS/JS technique. ALL of: the demo stage, the controls, the live source preview, and the documentation — in one file.
>
> File extension is `.html`. File name typically `<technique>-sandbox.html`.

---

An interactive demo of one animation or CSS effect, with sliders to tune the parameters live, and the resulting CSS source updating in real time. Useful for "what should the easing be on this transition" conversations, or for capturing the agreed-upon timing for a motion spec.

Read `artifact-css/SKILL.md` first for the OUTPUT CONTRACT, design tokens, and the **Interactivity layer** documenting the jQuery + jQuery UI loader pattern. Sandboxes opt-in to that layer for the slider widgets.

## When to reach for this skill

- User says "let me play with the easing", "tune this animation live", "show me different timings".
- User wants a motion spec they can hand to a designer or PM to converge on values.
- User wants to ship one effect with a "live preview" page attached.

If they want a triage board / form editor with multiple data structures, use `artifact-editor`. If they want a slide deck walking through animation principles, use `artifact-deck`.

## Anatomy of a sandbox

Six blocks.

1. **Header** — eyebrow + technique name + lead. One sentence on what the demo demonstrates.
2. **Stage** — the live demo. Centered. Plays the effect on a button press (or on load + loop).
3. **Controls panel** — sliders + selects for every tunable parameter. Each control updates the stage immediately. Pair each slider with an `<output>` showing the current value.
4. **Live source** — a `.code-block` showing the resulting CSS (or JS) that matches the current control state. Updates on every change. Includes a "copy" button.
5. **Presets row** — three to five preset configurations (`Subtle`, `Default`, `Bold`, `Bouncy`) as buttons. Clicking sets all sliders.
6. **Notes** — short prose explaining when to reach for the effect, what to watch out for (perceived performance, accessibility prefers-reduced-motion), and any constraints.

## Common technique types this skill handles

| Type | Tunable parameters |
|---|---|
| CSS transition | duration · easing · property · delay |
| CSS keyframe animation | duration · iteration · easing · fill mode · keyframe stops |
| Transform stack | translate · rotate · scale (each with its own slider) |
| Color transition | from-color · to-color · duration |
| Stagger / cascade | item count · stagger delay · per-item duration |

Pick ONE technique per sandbox. A sandbox demonstrating four different transitions is unfocused.

## Voice and density rules

1. **One technique, one stage.** No second demo on the same page. Make a sibling file.
2. **All controls visible at once.** No tabbed controls. The whole point is fast iteration.
3. **Default state must look good.** First load = the preset you'd actually recommend. Not a random midpoint.
4. **The code is the spec.** The live source IS what the user is going to commit. Make it copy-ready.
5. **Respect prefers-reduced-motion.** Add a media query that disables looping animations. Show the user this is happening with a small note.

## Fallback contract

With JS disabled:
- Stage still renders (CSS-only effects play; JS-driven effects render the static end state).
- Sliders render as `<input type="range">` HTML5 native — still adjust values, no styled chrome.
- Live source shows the default preset.

## Common mistakes

- **Auto-looping at full speed without a pause button.** Annoying. Always pair with play/pause control.
- **Sliders without output values.** Without seeing the number, the user can't reproduce the setting elsewhere.
- **No prefers-reduced-motion respect.** Accessibility blocker. Always include the media query.
- **Demo element too small.** A 60px square animating subtly is invisible. Stage should be 200-400px on each side.
- **No "reset to default" button.** Users tune, hate, want back. Give them the escape hatch.

## After the artifact

Offer two derivatives:
1. The current CSS spec as a copy-ready snippet (motion spec for design hand-off).
2. A short note on browser support / performance implications for the tuned values.
