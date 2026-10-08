---
name: billboards-and-demos
description: >-
  Patterns for configuring billboard side quests with interactive arcade demos,
  partner logos, and per-level theming. Use when adding demos to a level,
  swapping arcade embeds, adding new partner logos, or extending the billboard
  overlay with new content types.
---

# Billboards & Interactive Demos

## Overview

Each level has 3 billboards positioned along the sides of the track. Players can click them to pause the game, view an interactive arcade demo (or coming-soon placeholder), and earn +500 points per demo per run. The system spans these files:

| File | Responsibility |
|------|----------------|
| `src/data/config.js` | Billboard definitions per level (label, accent, logo, embed URL) |
| `src/game/Track.js` | 3D billboard meshes, canvas face textures, logo loading |
| `src/game/Game.js` | Click detection, camera zoom, overlay trigger, +500 bonus tracking |
| `src/game/UI.js` | Overlay content injection (iframe embed or placeholder), bonus badge |
| `index.html` | Billboard overlay HTML shell (topbar, content area, close button) |
| `style.css` | Overlay panel, iframe, placeholder, and bonus badge styling |

## Adding Demos to a Level

This is the most common task. You only need to edit `src/data/config.js`.

### Billboard Config Structure

Each level in `LEVELS` has a `billboards` array with 3 entries:

```js
billboards: [
  {
    id: "demo1",            // unique string across all levels
    label: "Instana",       // shown on billboard face + overlay topbar
    accent: 0x00c8ea,       // accent color for billboard frame glow + border
    logo: "./assets/instana-logo.png",  // optional — partner logo on billboard face + placeholder
    embed: "https://demo.arcade.software/...",  // arcade iframe URL — null for coming-soon
    embedTitle: "Unlock AIOps with IBM Instana",  // iframe title attribute
  },
  // ... 2 more entries
],
```

### Field Reference

| Field | Required | Type | Purpose |
|-------|----------|------|---------|
| `id` | Yes | string | Unique identifier. Used for click tracking and +500 bonus per-run dedup. Must be unique across all levels. |
| `label` | Yes | string | Display name on the 3D billboard face, overlay topbar, and placeholder. |
| `accent` | Yes | hex int | Glow color for billboard frame strips, border on canvas, and point light. |
| `logo` | No | string path | Path to a logo PNG in `assets/`. Displayed on the 3D billboard face and in the coming-soon placeholder. If omitted, falls back to text-only layout with "SIDE QUEST" header. |
| `embed` | No | string URL | Full arcade.software embed URL (or any iframe-friendly URL). If `null`, the overlay shows a coming-soon placeholder instead of an iframe. |
| `embedTitle` | No | string | Title attribute on the iframe for accessibility. |

### Step-by-Step: Adding Demos to a New Level

1. **Add logo PNGs** to `assets/` (e.g. `assets/mypartner-logo.png`). Keep them small — they're drawn onto a 512×320 canvas at max 240×100px.

2. **Edit the level's `billboards` array** in `src/data/config.js`:

```js
B: {
  // ... existing theme fields ...
  billboards: [
    {
      id: "demo4",
      label: "Partner A",
      accent: 0x44bb66,
      logo: "./assets/partner-a-logo.png",
      embed: "https://demo.arcade.software/xxxxx?embed&embed_mobile=tab&embed_desktop=inline&show_copy_link=true",
      embedTitle: "Partner A Demo Title",
    },
    {
      id: "demo5",
      label: "Partner B",
      accent: 0xddaa22,
      logo: "./assets/partner-b-logo.png",
      embed: null,  // coming soon
      embedTitle: "Partner B Demo",
    },
    {
      id: "demo6",
      label: "Partner C",
      accent: 0x8866dd,
      logo: "./assets/partner-c-logo.png",
      embed: "https://demo.arcade.software/yyyyy?embed&embed_mobile=tab&embed_desktop=inline&show_copy_link=true",
      embedTitle: "Partner C Demo Title",
    },
  ],
},
```

3. **Update `index.html` level card** if the level name changed:

```html
<button class="level-card" data-level="B">
  <canvas class="level-preview" width="180" height="120"></canvas>
  <div class="level-card-label">New Name</div>
  <div class="level-card-sub">New Subtitle</div>
</button>
```

4. That's it. No code changes needed in Track.js, Game.js, UI.js, or style.css — the system reads from config automatically.

### Updating an Existing Demo

To swap an embed URL (e.g. ServiceNow arcade is now ready):

```js
// In config.js, change embed from null to the URL:
{
  id: "demo2",
  label: "ServiceNow",
  accent: 0xff6644,
  logo: "./assets/servicenow-logo.png",
  embed: "https://demo.arcade.software/NEW_ID?embed&embed_mobile=tab&embed_desktop=inline&show_copy_link=true",
  embedTitle: "ServiceNow & Ansible Automation Platform",
},
```

## How the System Works (for deeper changes)

### 3D Billboard Face (`Track.js`)

`Track._billboards()` creates a 512×320 canvas per billboard:
- If `def.logo` exists, loads the image and draws it centered, scaled to fill the entire board (max size with 24px padding)
- If no logo, draws `def.label` in large 56px text
- No small text on the billboard face — logos need to be visible from the game camera distance
- Canvas becomes a `THREE.CanvasTexture` on a plane mesh in front of the billboard frame

Three billboards are positioned at fixed world coordinates:
- Billboard 0: `x: -18` (left side, rotated toward road)
- Billboard 1: `x: 18` (right side, rotated toward road)
- Billboard 2: `x: 36` (far right, rotated toward road)
- All at `z: -65`

### Click Detection (`Game.js`)

- `_bindBillboardInput()` tracks pointer down/move/up on the canvas
- `_checkBillboardHover()` raycasts against `track.getBillboardMeshes()` — each mesh has `userData._billboardId`
- On pointer up (without drag), `_openBillboard(id)` fires:
  - Sets `state = "billboard"` (pauses the game loop)
  - Computes camera target position facing the billboard
  - Stores `_bbDef` (full config object) for the overlay
- `_updateBillboardCamera(dt)` lerps camera toward the billboard; when close enough, calls `ui.showBillboard()` with the embed/logo/label

### Overlay Content (`UI.js`)

`showBillboard(visible, { label, embed, embedTitle, logo, showBonus })`:
- If `embed` is truthy: injects an `<iframe>` into `#billboard-content`
- If `embed` is null: injects a placeholder div with the logo image (or gear icon fallback) and "coming soon" text
- `showBonus` controls the "+500 Interactive Experience" badge visibility
- On open, clears all floating HUD text (combo display, status, damage/pickup popups, hippo announce) so nothing obscures the arcade demo

### Bonus Points (`Game.js`)

- `_demoCompleted` is a `Set` tracking which billboard IDs have been visited this run
- On `closeBillboard()`: if the demo ID isn't in the set, awards +500 points, shows "+500" popup and "⭐ +500 Interactive Experience" status
- `_demoCompleted` is cleared in `resetRun()` so each run is fresh
- Maximum possible bonus per run: 1,500 pts (3 billboards × 500)

### Closing the Billboard

Three ways to close and return to gameplay:
- **Escape key** — handled by a `document`-level `keydown` listener with `capture: true` in `UI.js`. This is necessary because cross-origin iframes (arcade.software) steal keyboard focus, so the normal `window` keydown in `Game.js` won't fire while the iframe is focused. The capture listener on `document` fires first regardless of iframe focus.
- **Close button** (×) — top-right of the overlay, wired in `UI._bindButtons()` → `onBillboardClose` → `Game.closeBillboard()`
- **Click backdrop** — clicking the dark area outside the billboard panel closes it (event target check on the overlay element in `UI.js`)

## Arcade Embed URL Format

The arcade.software embed URLs follow this pattern:

```
https://demo.arcade.software/{ARCADE_ID}?embed&embed_mobile=tab&embed_desktop=inline&show_copy_link=true
```

The `ARCADE_ID` is the unique identifier from arcade.software. The query parameters control the embed behavior:
- `embed` — enables embed mode
- `embed_mobile=tab` — opens in a new tab on mobile
- `embed_desktop=inline` — shows inline on desktop
- `show_copy_link=true` — shows a copy link button

## Logo Asset Guidelines

- Place logos in `assets/` at the project root
- PNG format with transparent background preferred
- They're drawn on a 512×320 canvas at max 240×100px, so anything 256px+ wide works well
- Same logo is used both on the 3D billboard face and in the coming-soon placeholder overlay
- File naming convention: `{partner}-logo.png` (lowercase, hyphenated)
