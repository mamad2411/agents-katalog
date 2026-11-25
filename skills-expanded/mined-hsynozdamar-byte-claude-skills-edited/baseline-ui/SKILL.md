---
name: baseline-ui
description: Quickly deslop UI code by fixing spacing, hierarchy, typography, and small layout issues. Use when the interface needs a fast cleanup or polish pass.
---

# Baseline UI

A fast cleanup pass on existing UI. The job is to fix what's broken or sloppy, not to redesign. Keep the project's stack, tokens, and visual direction; if the design deliberately uses gradients, glow, custom easing, or tracking, that's a choice, not slop.

`/baseline-ui` applies this to UI work in the conversation. `/baseline-ui <file>` reviews a file: quote the snippet, say why in one line, give the fix.

## What to look for

**Hierarchy and spacing.** One clear focal point per view, spacing from a consistent scale, one accent color doing the work. Empty states get one clear next action.

**Typography.** `text-balance` on headings, `text-pretty` on body, `tabular-nums` for changing numbers, `truncate`/`line-clamp` in dense UI.

**Mobile.** `h-dvh` instead of `h-screen`; fixed elements respect `safe-area-inset`.

**Accessibility.** Use the project's existing primitives (Radix, Base UI, React Aria) for anything with focus or keyboard behavior instead of hand-rolling it, and don't mix systems in one surface. Icon-only buttons need `aria-label`. Never block paste in inputs. Errors appear next to the action that caused them; destructive actions get a confirm.

**Motion and performance.** Animate `transform` and `opacity`, not layout props. Interaction feedback stays fast (around 200ms or less). Respect `prefers-reduced-motion`, pause off-screen loops, avoid animating large `blur()`/`backdrop-filter` surfaces, use `will-change` only while animating. Don't use `useEffect` for what render logic can express.

**Layout.** A z-index scale instead of arbitrary values; `size-*` for squares.

## During a cleanup pass

Don't add things the UI didn't have: no new animations, gradients, glows, or fonts. Those belong to a design decision, not a polish pass.
