---
name: cueframe-product-video
description: Use when turning a screen recording (with cursor/click events) into a polished, auto-zooming product video or demo reel via CueFrame — e.g. "make a product demo from this Browserbase capture", "auto-zoom this screen recording to where the user clicked", "turn this walkthrough into a social demo". This is a USE-CASE recipe over the CueFrame primitives in the `cueframe-cli` skill.
---

# CueFrame — Product Video recipe

Use the [project and capability policy](../composing-video/references/project-policy.md) for scope, current state and metered work.

A **use-case recipe**, not new framework surface. CueFrame's engine only knows
primitives (`upload` → `composition put` → `render`, the `reframe` viewport, the
overlay/effect primitives). This skill is the *judgment* on top: how to turn a
captured walkthrough into a product video that looks good. This tells you *what*
to author, not how to transport it.

**Drive the primitives over MCP if you can call tools** (`new_composition` /
`apply_composition` / `validate_composition` / `create_render` — see the
`cueframe-connect` skill for the one-line setup). The `npx -y cueframe@0.12 …` commands
written out below are the same operations for a terminal or CI job with no MCP
host; see the `cueframe-cli` skill.

## The pipeline

```
capture (video + cursor/click points)  →  auto-zoom (points → reframe)
   →  compose (video track + per-clip reframe)  →  polish (overlay primitives)
   →  render
```

## 1. Capture → timed focus points

Get a screen recording **plus** the cursor/click events with viewport
coordinates and timestamps (e.g. from a browser-automation capture). Normalize
every point to `{ t: seconds, x: 0..1, y: 0..1 }` against the **real captured
viewport** — these are the *focus points* the zoom follows. Measure the rendered
video's true duration (ffprobe) and map point times onto it.

## 2. Points → reframe (auto-zoom)

The framework owns the tuning. Canonical implementation:
`autoZoom(points, style)` in `@cueframe/composition` (timed focus points →
gapless `reframe` segments; never re-derive this with an LLM — it drifts). Pick a
**style**, never raw numbers:

| style | zoom (`<1` punches in) | feel |
|---|---|---|
| `subtle`   | 0.80 | gentle, corporate |
| `standard` | 0.67 | default |
| `punchy`   | 0.55 | snappy, social |

The tiling rule (what `autoZoom` does — use this until it's exposed as
`cueframe compose from-points`): sort points by `t`; group points within
`mergeGap`s; pad each group `prePad` before / `postPad` after; drop groups
shorter than `minZoom`; merge overlapping windows; emit `frame-center` zoom 1
in the gaps and a `point` punch-in (`focus:{mode:"point",x,y}`, `zoom` = the
style's) over each window. Result → `source.reframe.segments` on the clip.

## 3. Compose

One video track, the screen recording as a media clip carrying the reframe.
`npx -y cueframe@0.12 composition put <projectId> -b @composition.json --if-match <etag>`, with the
ETag from `composition get` (`--create` for the project's first composition; see `cueframe-cli`).
Choose `-a 16:9` for landscape product video, `9:16` for social.

## 4. Polish — layer overlay primitives (this is what makes it look "produced")

A bare auto-zoom reads as a raw screen-grab. Add overlay/effect clips referencing
registered primitives (`registry/params-required.json` lists each one's params;
`$brand:` tokens bind brand colors/fonts at render). Tasteful default set for a
product demo:

| Goal | primitiveId | kind |
|---|---|---|
| animated cursor tracing the click path | `cursor-flow` / `simulated-cursor` | overlay |
| title / context | `lower-third` or `heroText` | overlay |
| highlight a clicked element | `marker-highlight` / `pulsing-indicator` | overlay |
| device/browser frame | `device-mockup-zoom` / `browser-flow` | overlay |
| captions (if narrated) | the top-level `captions` field | — |
| finish/look | `color-grade` + `vignette` | effect |
| several cells sharing space that should reflow (feature grid, rail + fluid content) | author one card or native component laid out with CSS flex/grid (see `cueframe-component-authoring`) | overlay (authored) |

Static PiP / split-screen is `region` + `fit` on the clips (EX3 / EX4). Cells that must
**reflow together** or hold mixed content are one authored card or native component laid out
with CSS flex/grid.

A primitive is the `source` of a clip; the clip wraps it with `id`/`startTime`/`duration`:
- Overlay clip (on a `kind:"overlay"` track): `{ "id":"t1", "startTime":1, "duration":3, "source":{ "kind":"overlay", "primitiveId":"lower-third", "params":{…}, "zPlane":"front" } }`.
- Effect clip (on a `kind:"effect"` track): `{ "id":"e1", "startTime":0, "duration":9, "source":{ "kind":"effect", "primitiveId":"color-grade", "params":{…} } }`.
Simultaneous overlays go on **separate tracks** — clips on one track can't overlap in time.
**Don't over-decorate** — 2–4 primitives. Cursor + title + grade is usually enough.

## 5. Render

First use `cueframe-compose-loop`'s [preview workflow](../cueframe-compose-loop/references/preview-workflow.md):
check framing with `preview_frame` and click/zoom timing with an affected-window `preview_clip`.
For a small revision, verify that change and relevant regressions without exporting the whole film.
When delivering the finished video:

`npx -y cueframe@0.12 render <projectId> -o out.mp4 --json`. Verify the output (ffprobe +
sample frames) before declaring done.

## Worked examples — composition JSON

These are **orientation, not the contract.** The live wire schema is
`npx -y cueframe@0.12 schema composition`, and the way to know a draft is correct is
`npx -y cueframe@0.12 composition validate -b @composition.json` — it runs the same
validator the server enforces, with no save and no render. Discover + validate
before you render; never spend a render to find a schema mistake.

Each block below is a complete `@composition.json` (the bare object `composition put`
accepts: top-level `v`, `format`, `tracks`, optional `captions`). All five validate
against the real wire schema + save invariants (swap the `<…MediaId>` placeholders for
real `npx -y cueframe@0.12 upload` ids). Conventions that keep them valid:

- Tracks hold **`contents`** (not `clips`); each clip wraps a `source`.
- A clip's `source.kind` must match the track `kind`: `media` → `video`/`image`/`audio`
  tracks, `overlay` → `overlay` tracks, `effect` → `effect` tracks.
- Clip/segment times are **seconds** (`startTime`, `duration`, `startSec`, `endSec`,
  `trim`); caption word times are **milliseconds** (`startMs`/`endMs`).
- `region`/`fit` are **clip-level** (siblings of `source`); `reframe` lives on the media `source`.
- Clips on one track can't overlap — put simultaneous layers on **separate tracks**.
- `zoom < 1` punches in (range `[0.1, 1]`, default `1`). Durations are illustrative — match your source.

### EX1 · Auto-zoom screen demo (16:9)
One screen recording with `reframe` punch-ins (the `autoZoom` output: `frame-center` in the gaps, `point` over each click) + a cinematic grade.

```json
{
  "v": 1,
  "format": { "aspectRatio": "16:9", "fps": 30 },
  "tracks": [
    {
      "id": "v-screen", "kind": "video", "contents": [
        {
          "id": "rec", "startTime": 0, "duration": 12,
          "source": {
            "kind": "media", "mediaId": "<mediaId>",
            "reframe": { "segments": [
              { "startSec": 0,  "endSec": 2,  "focus": { "mode": "frame-center" }, "zoom": 1 },
              { "startSec": 2,  "endSec": 5,  "focus": { "mode": "point", "x": 0.28, "y": 0.42 }, "zoom": 0.6,  "ease": { "in": 0.4, "out": 0.4 } },
              { "startSec": 5,  "endSec": 7,  "focus": { "mode": "frame-center" }, "zoom": 1, "ease": { "in": 0.4, "out": 0.4 } },
              { "startSec": 7,  "endSec": 10, "focus": { "mode": "point", "x": 0.72, "y": 0.66 }, "zoom": 0.55, "ease": { "in": 0.4, "out": 0.4 } },
              { "startSec": 10, "endSec": 12, "focus": { "mode": "frame-center" }, "zoom": 1, "ease": { "in": 0.4, "out": 0.4 } }
            ] }
          }
        }
      ]
    },
    {
      "id": "fx", "kind": "effect", "contents": [
        { "id": "grade", "startTime": 0, "duration": 12, "source": { "kind": "effect", "primitiveId": "color-grade", "params": { "preset": "cinematic" } } }
      ]
    }
  ]
}
```

### EX2 · Social vertical with captions (9:16)
Reframe + a `lower-third` title, then a `cursor-flow` overlay (non-overlapping on one overlay track), transcript `captions` (ms timing), warm grade. `$brand:` refs bind brand colors/fonts at render.

```json
{
  "v": 1,
  "format": { "aspectRatio": "9:16", "fps": 30, "platform": "tiktok" },
  "tracks": [
    {
      "id": "v", "kind": "video", "contents": [
        {
          "id": "rec", "startTime": 0, "duration": 10,
          "source": {
            "kind": "media", "mediaId": "<mediaId>",
            "reframe": { "segments": [
              { "startSec": 0, "endSec": 4,  "focus": { "mode": "point", "x": 0.3,  "y": 0.4 },  "zoom": 0.7,  "ease": { "in": 0.4, "out": 0.4 } },
              { "startSec": 4, "endSec": 10, "focus": { "mode": "point", "x": 0.62, "y": 0.55 }, "zoom": 0.62, "ease": { "in": 0.4, "out": 0.4 } }
            ] }
          }
        }
      ]
    },
    {
      "id": "ov", "kind": "overlay", "contents": [
        {
          "id": "title", "startTime": 0, "duration": 3.5,
          "source": {
            "kind": "overlay", "primitiveId": "lower-third",
            "params": {
              "text": "AI video, one command", "subtitle": "cueframe", "variant": "modern",
              "tokens": { "textColor": "$brand:colors.textOnMedia", "accentColor": "$brand:colors.accent", "fontFamily": "$brand:fonts.heading.family" }
            }
          }
        },
        {
          "id": "cursor", "startTime": 3.5, "duration": 6,
          "source": {
            "kind": "overlay", "primitiveId": "cursor-flow",
            "params": {
              "waypoints": [ { "x": 200, "y": 180 }, { "x": 540, "y": 240, "click": true, "label": "Generate" }, { "x": 1040, "y": 520, "click": true, "label": "Publish" } ],
              "cursorColor": "$brand:colors.text", "showTargets": true
            }
          }
        }
      ]
    },
    {
      "id": "fx", "kind": "effect", "contents": [
        { "id": "grade", "startTime": 0, "duration": 10, "source": { "kind": "effect", "primitiveId": "color-grade", "params": { "preset": "warm" } } }
      ]
    }
  ],
  "captions": {
    "segments": [
      { "words": [
        { "text": "Watch",   "startMs": 0,    "endMs": 320 },
        { "text": "this",    "startMs": 320,  "endMs": 560, "emphasis": true },
        { "text": "render",  "startMs": 560,  "endMs": 980 },
        { "text": "in",      "startMs": 980,  "endMs": 1120 },
        { "text": "one",     "startMs": 1120, "endMs": 1360, "emphasis": true },
        { "text": "command", "startMs": 1360, "endMs": 1900 }
      ] }
    ],
    "style": { "fontFamily": "Inter", "fontSize": 6.5, "fontWeight": 900, "color": "#ffffff", "highlightColor": "#10B981", "position": "bottom", "textTransform": "uppercase" }
  }
}
```

### EX3 · Picture-in-picture (16:9)
Full-frame screen recording + a webcam **inset** placed with `region`/`fit` on a second video track (composites on top by track order). Two uploads → two `mediaId`s.

```json
{
  "v": 1,
  "format": { "aspectRatio": "16:9", "fps": 30 },
  "tracks": [
    { "id": "v-screen", "kind": "video", "contents": [
      { "id": "screen", "startTime": 0, "duration": 10, "source": { "kind": "media", "mediaId": "<screenMediaId>" } }
    ] },
    { "id": "v-cam", "kind": "video", "contents": [
      { "id": "cam", "startTime": 0, "duration": 10, "source": { "kind": "media", "mediaId": "<webcamMediaId>" }, "region": { "x": 0.68, "y": 0.04, "w": 0.3, "h": 0.3 }, "fit": "cover" }
    ] }
  ]
}
```

### EX4 · Split-screen (16:9)
Two sources side-by-side, each with a half-frame `region` on its own video track.

```json
{
  "v": 1,
  "format": { "aspectRatio": "16:9", "fps": 30 },
  "tracks": [
    { "id": "v-left", "kind": "video", "contents": [
      { "id": "left", "startTime": 0, "duration": 8, "source": { "kind": "media", "mediaId": "<leftMediaId>" }, "region": { "x": 0, "y": 0, "w": 0.5, "h": 1 }, "fit": "cover" }
    ] },
    { "id": "v-right", "kind": "video", "contents": [
      { "id": "right", "startTime": 0, "duration": 8, "source": { "kind": "media", "mediaId": "<rightMediaId>" }, "region": { "x": 0.5, "y": 0, "w": 0.5, "h": 1 }, "fit": "cover" }
    ] }
  ]
}
```

### EX5 · Presenter intro — title behind the speaker (9:16)
Talking-head with an `active-speaker` reframe and a `heroText` title at `zPlane:"behind-subject"`. The speaker **detection** and the person **matte** are both resolved automatically at render (see the `cueframe-cli` skill's "Render resolves expensive intents" section) — author the intent, render, done.

```json
{
  "v": 1,
  "format": { "aspectRatio": "9:16", "fps": 30 },
  "tracks": [
    { "id": "v", "kind": "video", "contents": [
      { "id": "cam", "startTime": 0, "duration": 6, "source": { "kind": "media", "mediaId": "<mediaId>", "reframe": { "segments": [ { "startSec": 0, "endSec": 6, "focus": { "mode": "active-speaker" }, "zoom": 0.8 } ] } } }
    ] },
    { "id": "ov", "kind": "overlay", "contents": [
      { "id": "hero", "startTime": 0.5, "duration": 5, "source": {
        "kind": "overlay", "primitiveId": "heroText",
        "params": { "text": "SHIP IN MINUTES", "fontSizePct": 14, "textColor": "$brand:colors.textOnMedia", "fontFamily": "$brand:fonts.heading.family" },
        "zPlane": "behind-subject", "anchor": { "space": "scene", "x": 0.5, "y": 0.42 }
      } }
    ] }
  ]
}
```

## Notes / honesty

- **Picture-in-picture / inset cards render** — per-clip output-space placement
  (`region:{x,y,w,h}` in `[0,1]` + `fit`) is wired for PiP / inset / split-screen,
  for video, image, and overlay clips. Set `region`/`fit` on the **clip** (siblings
  of `source`, not inside it — as an agent, patch them with an `apply_composition`
  `clip.update` op: `{ type: 'clip.update', clipId, patch: { region, fit } }`); two
  clips with different placement composite by track order instead of occluding the
  background. See EX3 / EX4 below.
- This recipe lives in a skill on purpose: the engine stays use-case-free; the
  product opinions (style, which primitives, layout) live here and ship via
  `npx -y cueframe@0.12 install`. Add sibling recipes (`cueframe-podcast-clip`, …) the same way.
