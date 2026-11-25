---
name: configure-view-transitions
description: Guidance on configuring view transition settings and custom animations in WordPress.
---

# Configure View Transitions

The View Transitions plugin enables cross-document view transitions in WordPress.

## Key Configuration Actions
- Enable via Settings > Reading after activation.
- Uses fade effect by default.
- Custom animation duration can be handled using `plvt_inject_animation_duration()`.
- Respects `prefers-reduced-motion` settings in browsers.
- Integrates automatically with the WP Admin for backend transitions as well.
