---
name: capture-inspo
description: "Capture full-page screenshots of real sites by aesthetic or vibe as design inspiration, driving your own Chrome via playwriter over Land-book, Lapa Ninja, Awwwards and Mobbin. Use for \"capture inspo\"."
---

# Capture Inspo

Turn a vibe ("country wedding", "neo-brutalist", "warm editorial") into a folder of full-page
website screenshots, captured from the user's real Chrome, ready to drag into Claude Design.

Background on why this exists: the user's vault note "Building Beautiful UI with AI - Ras Mic"
describes generating a design system in Claude Design from a full-page screenshot of an
inspiration site. This skill automates the "go find and screenshot good inspiration" step.

## Prerequisites

- **Read the playwriter skill first**: run `playwriter skill` and follow its rules (observe→act,
  `state.page`, single quotes, etc.). This skill assumes you drive the browser through playwriter.
- Chrome must be running with the playwriter extension connected (`playwriter session new`).
- Capture writes via Playwright's `path` (real fs, any dir). In-sandbox `require('fs')` is scoped
  and **cannot** read `/tmp` or arbitrary dirs — verify saved files from the outer shell instead.

## Source map (vibe → gallery)

| Vibe / intent | Galleries (in order) | Notes |
|---|---|---|
| Marketing / landing page | `land-book.com`, `lapa.ninja` | Free, direct links to live sites, style filters. Default. |
| Premium / award-winning / animated | add `awwwards.com` | High craft; many are WebGL-heavy → expect viewport fallback. |
| Mobile / web app screens & flows | `mobbin.com` | Best for app UI. Needs login, but the user's Chrome session handles it. Only when asked. |

Skip recent.design / Godly: they link to X posts, not live sites.

## Workflow

### Phase 1 — discover + preview (cheap)
1. Map the vibe to a gallery + the closest style filter / search term.
2. With playwriter: open the gallery, dismiss any cookie modal, apply the filter, then
   `page.evaluate()` to extract candidates as `{ title, liveUrl, thumbnailUrl }`. Strip
   `?ref=...` tracking params from `liveUrl`. Collect ~8–12.
3. Download each `thumbnailUrl` into `<dir>/_previews/` and Read them inline so the user can see
   the shortlist. Present a numbered list (title + URL).
4. **Ask the user which to keep.** Do not full-capture everything.

### Phase 2 — capture chosen (expensive)
For each chosen `liveUrl`, run the bundled capture script (handles viewport pin, cookie dismiss,
lazy-load scroll, and WebGL fallback):

```bash
playwriter -s <SID> -e 'state.captureUrl="https://round.ai/"; state.outPath="/Users/<you>/screenshots/inspo/<slug>/round-ai.png"'
playwriter -s <SID> -f ~/.claude/skills/capture-inspo/scripts/capture.js
```

The script logs `{ url, outPath, mode }` where `mode` is `fullPage` or `viewport` (fallback).

## Output location

Save to `~/screenshots/inspo/<vibe-slug>-<YYYY-MM-DD>/` (e.g. `country-wedding-2026-06-24/`).
Get the date from the environment, never hardcode it. After capture:
- Make downscaled previews (`sips --resampleWidth 800 in.png --out preview.png`) for any image you
  read back, so you don't burn tokens on multi-MB full-page PNGs.
- Print the absolute folder path and tell the user it's ready to upload to Claude Design.

## Caveats (learned, real)

- **`fullPage` fails on WebGL/canvas-heavy sites** (e.g. family.co). The script catches this and
  falls back to a viewport shot — flag those to the user as partial.
- **Always pin viewport width** (the script uses 1440). Without it, capture inherits the monitor
  width (e.g. 3440 ultrawide) → distorted layout and huge files.
- **Full-page PNGs are large** (multi-MB). Fine for Claude Design upload; resize before reading back.
- **Login walls** (Mobbin, Twitter) work because it's the real Chrome session, not headless.
