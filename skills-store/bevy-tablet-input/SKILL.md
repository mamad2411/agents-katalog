---
name: bevy-tablet-input
description: Implement or review Rasterra tablet and stylus input through Bevy 0.19 and octotablet, including Wayland window-handle ownership, framed tool events, pressure, tilt, roll, erasers, timing, and mouse arbitration.
---

# Integrate tablet input

1. Read `CONTRIBUTING.md`, `docs/plan.md`, and the `bevy-019` skill.
2. Keep octotablet types inside `src/app/tablet.rs`. Normalize host events into
   `rasterra::input::PointerSample` before they reach the brush engine.
3. Poll octotablet without blocking during Bevy `PreUpdate` on the main thread.
4. Accumulate `In`, `Down`, `Pose`, `Up`, and `Out` changes per tool. Publish a
   coherent state or painting sample only when the matching `Frame` arrives;
   events inside a frame are simultaneous and arbitrarily ordered.
5. Treat `Down` as a hard positional discontinuity. Treat `Up`, `Out`, removal,
   window loss, and backend loss as stroke-ending or cancelling transitions.
6. Prefer octotablet `Builder::build_shared`. Clone Bevy's
   `RawHandleWrapper`, obtain its thread-locked wrapper on the main thread, and
   let octotablet retain it. Do not use `build_raw` while this owned route works.
7. Document the `RawHandleWrapper::get_handle` unsafe block with the invariant:
   it runs on winit's main thread and the cloned wrapper owns the window for at
   least as long as the tablet manager.

## Units and arbitration

- Octotablet positions are logical window pixels from the top-left. Convert
  them through the same window-to-document transform used by the mouse.
- Feed framed tablet motion and primary contact into Bevy's `PointerInput`
  stream so Feathers and headless widgets retain their ordinary interaction
  behavior. Preserve the real logical-pixel movement delta: Bevy ignores
  zero-delta moves for dragging. Order the adapter before
  `PickingSystems::ProcessInput`.
- Mirror the same contact edges into `MouseButtonInput`: `no -> yes` is left
  button pressed and `yes -> no` is left button released. Order the adapter
  before `InputSystems` so `ButtonInput<MouseButton>` updates that frame.
- Octotablet tilt is radians from perpendicular. MyPaint expects normalized
  X/Y tilt where `1.0` represents 60 degrees; validate signs on real hardware,
  convert with `sin(angle)`, and clamp each result to `[-1, 1]`.
- Octotablet roll is radians. Normalize it to turns for `PointerSample`.
- Preserve octotablet frame timestamps long enough to derive sample deltas.
  Test missing and discontinuous timestamps and use a conservative frame-time
  fallback.
- Disable octotablet mouse emulation. While a real tool is in proximity or
  contact, suppress compositor-generated mouse painting and picking samples.
- Treat pressure, tilt, roll, and tool identity as independently optional.
  Missing tilt and roll are neutral; missing pressure falls back to full
  contact pressure so a basic tablet remains usable.
- Reduce tool-button changes on `Frame`, alongside pose and contact. Octotablet
  button IDs are opaque and explicitly have no semantic index; Rasterra's
  initial B1/B2 policy orders the first two stable IDs per tool and displays the
  resulting states in diagnostics. Keep the policy replaceable by future user
  bindings.
- Side-button canvas gestures use hover position without synthesizing contact.
  B1 motion pans; B2 motion zooms relative to its press origin, with right/up
  positive and left/down negative. A navigation gesture cancels or suppresses
  painting for the same framed input.

## Validation

- Test the normalized event reducer with synthetic frames; do not require
  tablet hardware in automated tests.
- Cover event reordering within a frame, lift/move/recontact boundaries,
  `Out` and `Removed`, multiple tools, unit conversion, timestamp fallback,
  and mouse suppression.
- Keep a live inspector for hardware validation. Confirm pressure range, tilt
  axes and signs, eraser identity, proximity, disconnect/reconnect, and the
  absence of bridged or duplicate strokes on a real Wacom tablet.

## Primary references

- [octotablet API](https://docs.rs/octotablet/0.1.0/octotablet/)
- [octotablet event model](https://docs.rs/octotablet/0.1.0/octotablet/events/enum.ToolEvent.html)
- [octotablet winit painting example](https://docs.rs/crate/octotablet/0.1.0/source/examples/winit-paint.rs)
- [Bevy 0.19 `RawHandleWrapper`](https://docs.rs/bevy/0.19.0/bevy/window/struct.RawHandleWrapper.html)
