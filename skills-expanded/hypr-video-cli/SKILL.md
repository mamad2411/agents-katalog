---
name: hypr-video-cli
description: >
  Generates MP4 videos from canvasState JSON via CLI. Builds canvasState JSON with elements,
  animations, transitions, keyframes, captions, and effects, then renders with `npx hypr-video-cli`.
  Activates when creating videos, promos, clips, or animations from descriptions; composing
  video/image/text/shape/audio elements on a timeline; building canvasState JSON; rendering MP4.
  Triggers: "make a video", "create a promo", "render MP4", "product launch video", "social media clip",
  "animated text", "tutorial intro", "video from JSON", "social media reel".
  Does NOT handle frontend UI code, MobX store editing, or React component development.
---

# Video Generation via CLI

## Quick Reference

```bash
# Write config → generate JSON → render
node scripts/gen_canvas.mjs /tmp/video-<name>.mjs /tmp/video-<name>.json
npx hypr-video-cli /tmp/video-<name>.json -o ./output/<name>.mp4
```

## Workflow

```
- [ ] Step 1: Read references & plan scenes
- [ ] Step 2: Build config & generate JSON
- [ ] Step 3: Render & verify
```

### Step 1 — Read references & plan scenes

**1a.** Read these references (always required):

- [gen-canvas.md](references/gen-canvas.md) — config spec: `theme()` (24 themes), 11 role helpers, `autoTracks()`, inline `animIn`/`animOut`/`kf`, SVG helpers, `buildCanvas`. Pitfalls are inline with ⚠️ markers.

**1b.** Plan scenes: identify video type, list scene names/durations, pick best SVG helpers per scene, pick best elements and emoji.

**1c.** Read extras based on the plan:

| When | Reference |
| ---- | --------- |
| Using SVG helpers (almost always) | [svg-helpers.md](references/svg-helpers.md) — params for all 65 helpers |
| Choosing fonts | [font-assets.md](references/font-assets.md) — 18 bundled fonts & pairings |
| Adding emoji/unicode decorations | [icons.md](references/icons.md) |

### Step 2 — Build config & generate JSON

**2a.** Write a config `.mjs` file. Config and JSON go in `/tmp/` — never write to `examples/`.

```js
export default function build(h) {
  const {
    makeShape, makeEffect, buildCanvas, theme, autoTracks,
    svgVignette, svgDotGrid, svgGradientOrb, svgParticles,
    svgCheckMark, svgNumberCounter, // ...SVG helpers as needed
  } = h;

  const t = theme("cyberpunk");  // 24 themes — colors + role helpers + fonts
  const MAX = 25000;

  // ── Global layers ──
  const g_dot = svgDotGrid("g_dot", { start: 0, end: MAX, opacity: 0.04, color: t.ACCENT });
  const g_vig = svgVignette("g_vig", { start: 0, end: MAX, opacity: 0.6 });

  // ── Scene 1: Hero (0–7s) ──
  const s1_orb = svgGradientOrb("s1_orb", {
    x: 360, y: 60, w: 1200, h: 960, start: 0, end: 7500, opacity: 0.10, color: t.ACCENT,
  });
  const s1_title = t.hero("s1_title", "Product Name", {
    x: 160, y: 340, start: 0, end: 7000,
    animIn: ["blurIn", 1200], animOut: ["blurOut", 700],
    kf: { scale: { dur: 7000, amp: 0.02 } },
  });
  const s1_div = makeShape("s1_div", "rect", t.ACCENT, {
    x: 760, y: 510, w: 400, h: 3, start: 500, end: 6500,
    animIn: ["expandIn", 500], animOut: ["fadeOut", 300],
  });
  const s1_sub = t.subtitle("s1_sub", "Tagline goes here", {
    x: 260, y: 540, start: 700, end: 6500,
    animIn: ["fadeIn", 800], animOut: ["fadeOut", 500],
  });

  // ── Scene 2: Features (6.5–16s) ──
  // ... more scenes follow the same pattern

  const elements = [g_dot, g_vig, s1_orb, s1_title, s1_div, s1_sub /* ... */];

  return buildCanvas({
    bg: t.BG, maxTime: MAX,
    // t.fonts is an OBJECT { Montserrat: {...}, "Fira Code": {...}, ... } — NOT an array
    // To add extra fonts (e.g. CJK), use object spread:
    fontAssets: {
      ...t.fonts,
      "Noto Sans SC": { url: "skill/assets/fonts/NotoSansSC-Variable.ttf", fileType: "ttf" },
    },
    elements, tracks: autoTracks(elements),
    fps: 30, quality: "medium",
  });
}
```

```bash
node scripts/gen_canvas.mjs /tmp/video-<name>.mjs /tmp/video-<name>.json
```

**2b.** Before rendering, verify:

1. All text uses role helpers (`t.hero` … `t.eyebrow`) — use raw `makeText` only for custom font/size/color (e.g. code blocks, CJK with `Noto Sans SC`)
2. Every visible element has `animIn` + `animOut`; stagger 300–500ms between elements
3. SVG bg opacity ≤ 0.15; 2–4 helpers per scene; global layers span `0–MAX`
4. `maxTime` >= last element's `end`

### Step 3 — Render & verify

```bash
npx hypr-video-cli /tmp/video-<name>.json -o ./output/<name>.mp4
```

CLI flags: `--fps 24|30|60`, `--quality low|medium|high|very_high`, `--format mp4|mov|mp3`, `--width N`, `--height N`, `-q` (quiet).

If render fails → check ⚠️ pitfalls in [gen-canvas.md](references/gen-canvas.md) 

## Critical Rules

1. **`maxTime` >= largest element `end`** — too small = elements cut off
2. **Config files go in `/tmp/`** — never write to `examples/`
3. **Always use modern API** — `theme()` + role helpers + inline `animIn`/`animOut`/`kf` + `autoTracks()`. 
4. **Scene structure** — prefix element IDs with `s1_`/`s2_`… per scene; use comment blocks `// ── Scene N: Title (Xs–Ys) ──`
5. **Transitions** require adjacent elements on same track (prefer effect-based flash/glitch cuts)
6. **Use `backgroundColor` via `bg: t.BG`** — not a full-screen background shape
7. **`gen_canvas.mjs` path** — run from skill root: `node scripts/gen_canvas.mjs` (NOT `skill/scripts/`)
8. **`t.fonts` is an object, not an array** — use `{ ...t.fonts, "Extra Font": { url: "...", fileType: "ttf" } }` to add fonts. Never use `[...t.fonts]` (array spread)
