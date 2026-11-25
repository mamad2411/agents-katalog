---
name: mobile-ui-debugging
description: Debug checklist for mobile UI lockups caused by overlays, z-index, and stale scroll locks.
---

# Mobile UI debugging

- Check for invisible overlays intercepting taps after closing a drawer.
- Check `html`/`body` classes and inline styles after every close path.
- Verify scroll works after closing at top, middle, and bottom of the page.
- Verify menu links, backdrop, Escape, and theme buttons do not trap interaction.
- Prefer simple cleanup over complex scroll-position locking unless required.
- Confirm no horizontal overflow on common mobile widths.