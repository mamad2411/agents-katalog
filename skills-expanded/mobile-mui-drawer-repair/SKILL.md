---
name: mobile-mui-drawer-repair
description: Use when building or fixing real mobile website navigation with React/MUI-like drawer, menu, dialog, overlay, breakpoint switching, scroll lock, and iOS/Android mobile bugs.
metadata:
  short-description: Mobile drawer and overlay repair patterns from MUI
---

# Mobile MUI Drawer Repair

Use this skill for mobile-first drawer, menu, dialog, and overlay work inspired by `mui/material-ui`.

Primary source:
- https://github.com/mui/material-ui

Focus areas:
- Temporary versus permanent drawer behavior across breakpoints.
- Swipeable drawer tradeoffs, including performance and touch handling.
- Dialog and overlay scroll lock on iOS Safari and Android Chrome.
- Avoiding background scroll leaks when panels are open.
- Keeping open/closed state synchronized with ARIA and visual state.

Checklist:
- Use a real `button` for toggles.
- Keep `aria-expanded` and `aria-controls` synchronized.
- Close on escape, route change, backdrop click, and menu item selection where appropriate.
- Lock body/background scroll while modal navigation is open.
- Prefer `100dvh`/`svh`/`lvh` over plain `100vh` when viewport chrome matters.
- Test at 320px, 390px, 430px, 768px, and desktop widths.

Common fixes:
- If the page scrolls behind a drawer, lock the document body and make only the panel scrollable.
- If a drawer feels slow on mobile, reduce heavy transitions and avoid mounting expensive content unnecessarily.
- If desktop and mobile state conflict, derive variant from a stable media query and reset temporary state on breakpoint change.
