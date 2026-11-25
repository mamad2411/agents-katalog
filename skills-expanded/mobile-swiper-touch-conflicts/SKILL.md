---
name: mobile-swiper-touch-conflicts
description: Use when building or repairing mobile carousels, sliders, horizontal swipe regions, touch-action, axis detection, and vertical scroll conflicts.
metadata:
  short-description: Touch and swipe conflict repair from Swiper
---

# Mobile Swiper Touch Conflicts

Use this skill for mobile carousel and horizontal swipe behavior inspired by `nolimits4web/swiper`.

Primary source:
- https://github.com/nolimits4web/swiper

Focus areas:
- Horizontal swipe versus vertical scroll conflict.
- Axis detection with `dx` and `dy`.
- `touch-action` policies such as `pan-y`.
- No-swiping zones for buttons, links, inputs, and nested controls.
- Avoiding blind `preventDefault`.

Checklist:
- Set `.carousel { touch-action: pan-y; }` when vertical page scroll must remain available.
- Track pointer/touch start coordinates and compare horizontal and vertical movement.
- Only intercept after a clear horizontal gesture is detected.
- Do not block native scrolling for taps, links, form fields, or vertical drags.
- Test fast flicks, slow drags, diagonal gestures, and nested controls.

Common fixes:
- If users cannot scroll the page over a carousel, allow `pan-y` and delay interception.
- If buttons inside a slider are hard to tap, create no-swipe zones.
- If diagonal gestures feel broken, increase the threshold before claiming the swipe.
