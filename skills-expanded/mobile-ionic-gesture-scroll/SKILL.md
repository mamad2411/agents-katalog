---
name: mobile-ionic-gesture-scroll
description: Use when debugging real mobile gesture, scroll, menu, modal, content, and safe-area bugs inspired by Ionic mobile app and website patterns.
metadata:
  short-description: Mobile gesture and scroll pathology from Ionic
---

# Mobile Ionic Gesture Scroll

Use this skill for mobile-realistic menu, modal, gesture, scroll, and safe-area behavior inspired by `ionic-team/ionic-framework`.

Primary source:
- https://github.com/ionic-team/ionic-framework

Focus areas:
- Menu/content coordination on touch devices.
- Modal and drawer scroll containment.
- Gesture conflicts between overlays, sliders, and page scroll.
- Safe-area insets on iOS devices.
- Hardware/browser differences between iOS Safari and Android Chrome.

Checklist:
- Decide which surface owns the gesture before calling `preventDefault`.
- Use `touch-action` to declare expected browser behavior.
- Keep overlays fixed to the viewport and panel content independently scrollable.
- Add `padding-bottom: env(safe-area-inset-bottom)` where content reaches device edges.
- Test nested scroll containers on real mobile dimensions.

Common fixes:
- If a modal traps scroll incorrectly, separate backdrop, panel, and scrollable content layers.
- If swipe navigation fights vertical page scroll, detect movement axis before intercepting.
- If bottom buttons are hidden by device UI, add safe-area-aware padding.
