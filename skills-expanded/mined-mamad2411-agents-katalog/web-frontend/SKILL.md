---
name: web-frontend
description: >
  Web frontend engineering conventions for web projects.
---

# Stack

Choose the frontend stack based on the kind of project:

- For mostly static websites and landing pages, prefer Astro.
- For applications with meaningful client-side state, interactivity, or SPA/PWA behavior, prefer Svelte.
- Always use TypeScript instead of plain JavaScript.

# Libraries

Prefer a good existing library over implementing non-trivial infrastructure yourself unless I explicitly ask otherwise.

When choosing a library, prefer solutions that are:

- modern and actively evolving; prefer newer approaches over legacy solutions when both solve the problem well;
- actively maintained and supported;
- established enough to have real-world usage and community confidence, while not requiring mainstream popularity.

Use the latest stable release unless project compatibility requires otherwise.

Do not add a dependency for trivial functionality that is clearer to implement directly.

# Styling

- Use UnoCSS as the primary styling system. Prefer its rules, shortcuts, themes, and other reusable abstractions over accumulating plain CSS.
- Prefer modern native CSS features when they express the solution cleanly. Use plain CSS where it is the better tool rather than forcing everything through utilities.
- Always support light and dark themes through the OS/browser `prefers-color-scheme`. Do not add a manual theme toggle unless explicitly requested.

# Web Engine

- Write standards-based, browser-engine-independent code. Prefer modern web platform APIs and do not support obsolete browsers unless explicitly requested.
