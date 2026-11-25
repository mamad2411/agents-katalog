# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## What This Is

A personal Chrome extension (Manifest V3) that removes the max-width constraint on the Libby (libbyapp.com) magazine reader, allowing magazines to fill the full browser viewport.

## Architecture

- **manifest.json** — Extension manifest. Content scripts inject into all frames (`all_frames: true`, `match_about_blank: true`) because the Libby reader lives inside a nested iframe (dewey-* frame), not the top-level document.
- **override.css** — CSS overrides with `!important` to remove container constraints (`max-width` on `.book-pillar`, `max-height` on `.book-bounds`). This is the entire extension — CSS is applied before the app initializes, so its layout engine computes dimensions using our overridden values natively.

## Key Libby DOM Details

- `.book-pillar` — Main container, has inline `max-width: 1320px`
- `.book-bounds` — Inner container, has inline `max-height`
- `.scene` — Contains the page spread, has fixed inline width/height
- `.sheet.pre-paginated` — Individual page wrappers
- `iframe` inside sheets — Actual page content, rendered at 960x1285 native with `transform: scale(0.6875)` to fit the constrained layout

The app's JS continuously sets inline styles on these elements, so CSS `!important` is needed to override them. The app reads container dimensions at initialization and computes layout accordingly — this is why CSS overrides work well (applied before init).

## Important Constraints

- **Never compromise resolution.** Do not use `transform: scale()` to enlarge content — it stretches pixels and looks blurry on high-DPI displays. Instead, use CSS overrides (e.g., removing `max-width`) so the app's layout engine re-renders content at the larger size natively.
- **Prefer CSS over JS for layout overrides.** The app's layout engine reads container dimensions at init. CSS `!important` is applied before init, so the app computes correct layout natively. JS-based overrides run after init and cause the app to use stale dimensions (letterboxing, incorrect sizing).
- **The reader iframe has a 72px header offset.** `book-bounds` starts at top=72 within the viewport. Height overrides must account for this (e.g., `calc(100vh - 72px)`) or the bottom gets clipped by the iframe boundary.

## Development Workflow

1. Load/reload the unpacked extension at `chrome://extensions/` (enable Developer Mode)
2. After code changes, click the reload arrow on the extension card
3. Reload the Libby magazine page to see changes
4. Debug via DevTools console — look for `[Libby Full Width]` log messages
5. When checking the DOM, switch to the correct frame context in the console dropdown (the `dewey-*` frame, not `top`)
