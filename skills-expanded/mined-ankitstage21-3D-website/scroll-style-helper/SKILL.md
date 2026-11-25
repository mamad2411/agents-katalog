---
name: scroll-style-helper
description: Handles the small set of design decisions specific to scroll3d sites that a general design-taste tool wouldn't know about — sampling accent colors from actually-generated footage, capping overlay text density against scroll-timing math, choosing safe text-contrast against unpredictable video frame content, and sizing reveal-line windows so lines don't overlap mid-scroll. Only relevant if a general taste/design-system skill is also installed — if not, video-scroll-effect and 3d-scene-effect use their own built-in defaults instead.
---

# Scroll-Style-Helper — the four scroll3d-specific taste decisions

## Scope
This is intentionally narrow. If a general design-taste skill is installed
alongside this plugin, let it own layout, typography, and general visual
polish — this skill only covers the four things that are specific to how
video-scroll-effect and 3d-scene-effect actually work, which a general tool has
no way to know about.

## 1. Sample accent color from generated footage
Once a section's asset (video/image) exists, sample a few dominant colors
from actual frames (not just the prompt's described palette, since generation
doesn't always match exactly) and suggest an accent color that will read
clearly against that footage — avoid low-contrast pairings where overlay
text would wash out against a similarly-toned background.

## 2. Cap overlay text density against scroll timing
A `reveal-line`'s `[in, out]` window needs to be wide enough that the line
is actually readable before it fades — very short windows on fast-scrolling
sections make copy unreadable. Given a section's scroll height (vh) and
number of overlay lines planned, flag if the average window per line would
be too narrow (a rough floor: each line's `[in,out]` span should cover at
least ~15-20% of total scroll progress to be comfortably readable).

## 3. Text contrast against unpredictable frame content
Since frame content varies shot to shot, recommend a vignette/gradient
overlay strength (per the existing `.vignette` CSS pattern) sufficient to
guarantee text legibility across the whole scrub range, not just the frames
that happened to look good in preview.

## 4. Reveal-line window overlap check
Confirm consecutive `reveal-line` windows in a section don't overlap in a
way that causes two lines to be simultaneously visible and competing for
attention — each line's `out` value should generally not exceed the next
line's `in` value by a large margin, except deliberately for the final line
per the existing "peak past 1.0" pattern.

## What this returns
Specific values (a hex color, a set of adjusted `data-in`/`data-out` numbers,
a vignette opacity) that video-scroll-effect/3d-scene-effect apply directly — not
general design advice.

## What this never does
- Never makes layout, typography, or general brand decisions — defers to a
  general taste-skill tool if one is present, or to video-scroll-effect/
  3d-scene-effect's own existing defaults if not.
- Never invoked if no footage/frames exist yet — color sampling specifically
  needs Step 1's asset to already exist.