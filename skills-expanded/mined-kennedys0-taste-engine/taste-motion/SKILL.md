---
name: taste-motion
description: Optional Anime.js v4 micro-interaction guidance for existing or user-chosen web UI. Use on requests to add, improve, or audit purposeful frontend motion, button feedback, menus, or transitions. Do not impose a new style or install animation dependencies unless justified. Preserve keyboard, reduced-motion, and project design system.
license: MIT
metadata:
  version: "0.13.1"
---

# Taste Motion — opt-in motion companion

Use on meaningful micro-interaction tasks, not on unrelated backend, SEO or content work. If the existing project already has a design style, preserve it. If building entirely new visual UI with no specified theme, defer to a style router such as Taste Engine to select an aesthetic first.

Read [Motion Engine Adapter](references/motion-engine.md) before implementation. **This is not an instruction to install Anime.js everywhere.** CSS transitions or the existing project's animation library may be enough. The module covers Anime.js v4, React scoped lifecycle cleanup, reduced-motion behavior, and anti-slop checks. An optional demonstration can be found at [React button example](examples/react/anime-v4-press.jsx).

The selected project's style dictates timing, easing, and strength. Accessibility, product truth, and action responsiveness override decoration. Do not auto-run idle loops or make content depend on animation.
