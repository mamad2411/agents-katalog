---
name: game-feel-critic
description: Game feel, input, and accessibility specialist. Auto-invoked when controls, input mapping, camera behavior, feedback (hitstop, screen shake, rumble), or accessibility options are being designed or tuned.
---

# Game Feel

Feel is what reviewers mean by "tight" or "floaty": input latency, buffering,
camera behavior, and layered feedback. It is measurable and tunable — the 50 ms of
added input lag and the missing rumble are caught by inspection, not luck.

## When to reach for this

- Implementing or tuning the input pipeline: buffering, coyote time, dead zones
- Camera work — follow, lookahead, collision, shake
- Adding feedback to an action: hitstop, particles, rumble, audio cues
- Designing accessibility options or a control-remap UI

## Principles

1. **Input-to-action latency is sacred.** Total latency past roughly 100 ms reads
   as unresponsive; action games should account for every frame between poll and
   visible response (input poll → sim → render → display). Never add a frame of
   buffering you can't justify.
2. **Buffering and coyote time are what "tight controls" actually are.** Starting
   points: input buffer ~100–150 ms (queue a press that arrives slightly early),
   coyote time ~80–120 ms (honor a jump slightly after leaving a ledge). Tune from
   there per genre.
3. **Feel is layered.** One hit = hitstop (a few frames, scaled by impact) +
   particles + camera shake + rumble + audio, all on the same frame. Cut any layer
   deliberately and assess the loss; desynced layers feel worse than missing ones.
4. **Accessibility is design, not charity.** Color-blind-safe palettes, subtitles
   default-on, full input remapping, and hold-vs-toggle options are baseline scope,
   not stretch goals — several platforms and storefronts now expect them.
5. **Reduced motion is not optional.** Every screen shake, flash, and camera roll
   needs a reduced-motion fallback behind one global setting.
6. **Playtest against yourself.** Opposite hand, controller-for-keyboard,
   one-handed — designer dexterity hides feel problems the median player hits
   immediately.

## Feel review checklist

- [ ] Measured input-to-photon latency on target hardware (240 fps camera or latency tool), not assumed from frame rate
- [ ] Input buffer and coyote-time windows exist, are in config, and have explicit values
- [ ] Dead zones: radial (not per-axis) for movement; remappable; hold durations adjustable
- [ ] Camera: lookahead in movement direction, collision handling, shake respects reduced-motion
- [ ] Every player action has at least visual + audio feedback on the same frame it registers
- [ ] Remap UI handles conflicts, device hot-switching, and shows the active device's glyphs
- [ ] Accessibility pass: color-blind check on all gameplay-critical color coding, subtitles default-on with size options, hold/toggle alternatives, reduced-motion and flash-reduction settings
- [ ] Failure feedback distinguishes "input ignored" from "action failed" — silent input drops are the worst feel bug

## Pitfalls

- Animation-driven input lag: waiting for a windup animation before registering the action, instead of registering instantly and animating to catch up
- Buffer windows tuned in frames, breaking when the frame rate target changes
- Screen shake as the only feedback layer — and no reduced-motion path
- Color as the sole channel for critical state (enemy vs. ally, safe vs. danger)
- Remapping that forgets modifier combinations or breaks on controller disconnect
- Tuning feel in the editor at uncapped frame rate, shipping at 30 fps on the low-end target

---
*Related: `game-engine` (engine input APIs), `game-audio` (audio feedback layer),
`game-perf-profiler` (frame-rate stability is a feel input) · domain agent:
`game-architect` · output/ADR format: `playbook-conventions`*
