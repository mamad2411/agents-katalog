---
name: mobile-headlessui-accessible-overlay
description: Use when building accessible mobile menus, dialogs, popovers, disclosure panels, focus management, keyboard behavior, and ARIA state inspired by Headless UI.
metadata:
  short-description: Accessible mobile menus and overlays from Headless UI
---

# Mobile Headless UI Accessible Overlay

Use this skill for accessible mobile menus, popovers, dialogs, and disclosure panels inspired by `tailwindlabs/headlessui`.

Primary source:
- https://github.com/tailwindlabs/headlessui

Focus areas:
- Semantic menu, dialog, popover, and disclosure behavior.
- ARIA state synchronization.
- Focus trap and focus restore.
- Escape key and outside click behavior.
- Touch-first interaction without losing keyboard support.

Checklist:
- Use native interactive elements before custom roles.
- Set `aria-expanded` on disclosure/menu buttons.
- Link controls to panels with `aria-controls` where useful.
- Move focus into modal dialogs and restore focus on close.
- Provide escape, backdrop/outside click, and navigation close paths.
- Ensure tap targets are large enough and do not depend on hover.

Common fixes:
- If a mobile menu opens visually but screen readers do not understand it, repair button semantics and state.
- If keyboard focus remains behind a dialog, add focus management.
- If outside click fails on touch devices, handle pointer events consistently.
