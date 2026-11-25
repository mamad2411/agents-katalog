---
name: vanilla-js-safe-menu
description: Safe Vanilla JS event-handling notes for mobile menus without external dependencies.
---

# Vanilla JS safe menu

- Use small named functions: `openMobileNav`, `closeMobileNav`, `toggleMobileNav`, `cleanupMobileNavState`.
- Event handlers should be idempotent and safe if elements are missing.
- Closing the menu must remove all open classes from menu/backdrop/html/body.
- Clean stale inline scroll-lock styles on `body` and `documentElement`.
- Theme buttons inside the menu must not leave the page locked.
- Avoid copying external code directly; adapt only the principle.