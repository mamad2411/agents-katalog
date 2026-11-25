---
name: cueframe-brand-demo
description: Use when turning a local app into a brand-consistent product demo with CueFrame — extract the brand straight from the repo (colors/fonts/logo/motion), capture a Playwright walkthrough of the running app, and author a branded, auto-zoomed demo whose intro/outro/logo/colors/fonts/motion are frozen by CueFrame's engine — e.g. "make an on-brand demo of my app", "record my localhost and produce a branded launch video". This is the end-to-end brand pipeline over the CueFrame curated tools.
---

# CueFrame — Brand demo recipe

Use the [project and capability policy](../composing-video/references/project-policy.md) for scope, current state and metered work.

> **Kit truth over MCP (current limits):** kit CONTENTS are not yet inspectable over MCP (`get_profile` lists names only), so `$brand:` tokens resolve blind — verify resolved fonts/colors with a `preview_frame` still, and when the kit conflicts with an explicit client spec, the spec wins (hardcode it and note the conflict). Bind kits by the SERVER id from `get_profile` (slug binding is unreliable — it can silently bind nothing); always confirm via the project response `brandKitId`.

A **use-case recipe** that runs end-to-end from inside the user's own project
folder. You (Claude) already see their code and their running app — that's the
unfair advantage. This skill turns that context into a brand-consistent product
video: pull the brand from the repo, capture the app, and author a demo whose
**brand identity is enforced by the engine**, not re-typed per clip.

Two things make this different from `cueframe-product-video`:

1. **The brand is real engine state.** A `brandKit` (created with
   `create_brand_kit`) carries colors / fonts / spacing / sizing / motion / logo
   / intro / outro / watermark. A composition references it by `brandKitId`;
   **render freezes it** — intro/outro bumpers are auto-prepended/appended, and
   every overlay that binds a `$brand:` token resolves against the kit. Edit the
   kit, re-render, the whole video re-themes. You don't hand-paint brand colors
   onto each clip.
2. **Drive CueFrame directly.** Brand consistency is a first-class CueFrame
   capability now. Don't reach for an external generator to "make it look
   branded"; author the intent against the brand kit and let render
   materialize it.

Drive the primitives with the `cueframe-cli` skill and converge with
`cueframe-compose-loop`; this tells you *what brand-demo to author*.

Use the compose-loop [preview workflow](../cueframe-compose-loop/references/preview-workflow.md)
for iteration. Check brand/layout with stills and motion with `preview_clip`; a small revision
does not require rerunning the Director or exporting the whole film. The pipeline below is for
a new finished demo; choose the self-driven loop when the user has not asked for Director authoring.

## The pipeline

```
extract brand (repo + live UI)  →  create_brand_kit
   →  capture (screen-capture client: Playwright walkthrough of localhost → MP4)  →  import_media
   →  get_media_context (faces + transcript)
   →  apply_composition (edit plan + brand template, refs brandKitId + $brand:)
   →  compose { fromComposition:true }  →  wait_job kind:compose
   →  create_render  →  wait_job kind:render  →  branded MP4
```

## 1. Extract the brand → `create_brand_kit`

You are running in the user's project. Read the brand out of the codebase
instead of asking for it:

- **Colors** — `tailwind.config.*` `theme.extend.colors`, CSS custom properties
  (`:root { --primary … }`), a `design.md` / tokens file, or the rendered UI.
- **Fonts** — `@font-face` / `next/font` / `<link>` declarations, the Tailwind
  `fontFamily` map, and which family is headings vs body.
- **Logo** — `public/`/`assets/` SVG/PNG; host it at a public https URL (or
  `import_media` it and use the resulting URL) so render can fetch it.
- **Spacing / sizing / radius** — the Tailwind scale, `--radius`, base font sizes.
- **Voice** — README / landing copy → a one-paragraph `voiceGuidelines`.

Synthesize and call `create_brand_kit`. The accepted shape (Phase 1 — the kit now
carries full brand identity, not just colors/fonts):

```jsonc
{
  "kitId": "acme",                 // caller-chosen stable id (re-POST upserts in place)
  "name": "Acme",
  "tagline": "Ship faster",
  "colors": {                       // REQUIRED — all five
    "primary": "#4F46E5", "secondary": "#0EA5E9", "accent": "#22C55E",
    "background": "#0B0B0F", "text": "#FAFAFA"
  },
  "headingFont": { "fontFamily": "Geist", "fontWeight": 700 },
  "bodyFont":    { "fontFamily": "Inter", "fontWeight": 400 },
  "voiceGuidelines": "Confident, plain-spoken, no hype.",
  "motion":    { "duration": 0.4, "easing": "ease-out", "entrance": "stagger-up", "staggerMs": 60 },
  "logo":      { "src": "https://…/logo.svg", "placement": "br", "sizePct": 8 },
  "intro":     { "kind": "card", "title": "Acme", "subtitle": "Ship faster", "durationMs": 1500 },
  "outro":     { "kind": "card", "title": "acme.dev", "durationMs": 2000 },
  "watermark": { "src": "https://…/mark.svg", "opacity": 0.6, "placement": "br" },
  "spacing":   { "base": 16, "lg": 32, "sm": 8 },
  "sizing":    { "fontSizeHeading": 64, "fontSizeBody": 28, "borderRadius": 12 }
}
```

`colors{primary,secondary,accent,background,text}`, `headingFont`, `bodyFont`,
`name`, `kitId` are required; everything else is optional. The response returns the
kit `id` — that's the `brandKitId` you'll reference. **Show the founder the
synthesized kit and let them override** before composing; the kit is the brand
contract for every clip.

## 2. Capture → one clean MP4

Record a walkthrough of the **running local app** with an external screen-capture
client: a headed Playwright script drives `localhost` while a native screen
recorder captures it, and you get one
CFR / faststart MP4 plus the cursor/click events (timed viewport coordinates —
the focus points the auto-zoom follows; see `cueframe-product-video` §1–2). Use
your codebase knowledge to script the walkthrough: open the real flows that
matter, click the features worth showing, pause on results.

Get the recording into CueFrame with `import_media` (public https URL) — it's
async; poll `list_media` for `processingStatus:"ready"` (or register
`create_webhook` on `media.completed`). Keep the click points; you'll map them onto
the rendered duration for the zoom.

## 3. Context → `get_media_context`

`get_media_context` returns **faces** (subject roster + `speakingShare`, for any
talking-head/presenter beat) and the **transcript** (per-word `start`/`end` for
caption timing). Combine it with what you already know from the code — you can
script and interpret the demo better than transcript-alone, because you know what
each screen *is*.

## 4. Author the seed composition → `apply_composition`

Author the edit plan **and** the brand template in one composition, then reference
the kit by `brandKitId`. Two layers:

**a. The edit plan** (same craft as `cueframe-product-video`): the screen
recording on a video track carrying `reframe` punch-ins from the click points
(`autoZoom` output — `frame-center` in the gaps, `point` over each click),
optional speed, and transcript-timed `captions`.

**b. The brand template** — overlays that bind `$brand:` tokens so they resolve
against the kit at render:

| Goal | how |
|---|---|
| intro / outro card | **automatic** — the kit's `intro`/`outro` are prepended/appended at render. Don't author bumper clips. |
| logo bug | **automatic** — the kit's `logo` is painted as a corner mark at render (placement/size from the kit; it lifts above the caption band). Don't author a logo overlay. |
| lower-third / title | `lower-third` or `heroText` overlay, colors/fonts bound to `$brand:` tokens |
| captions | top-level `captions` — themed by the kit's `captionProfile` + `syncCaptions` (don't bind `$brand:` in `captions.style`; captions resolve through the profile, not token refs) |
| motion identity | overlays inherit `$brand:motion.*`; the kit's entrance/timing drive the feel |

The `$brand:` vocabulary (the frozen token paths render resolves) — bind these,
never hardcode brand hexes/fonts:

- **colors** — `$brand:colors.{background,surface,card,text,textMuted,textOnMedia,border,accent,accentMuted,textOnAccent,textOnSurface}`.
  Text **over footage** → `$brand:colors.textOnMedia` (the legible-over-video slot).
- **fonts** — `$brand:fonts.heading.family`, `$brand:fonts.body.family`, `$brand:fonts.caption.family`.
- **motion** — `$brand:motion.{duration,easing,entrance,staggerMs,exitMs}`.
- **spacing / sizing** — `$brand:spacing.{base,lg,sm}`, `$brand:sizing.{fontSizeHeading,fontSizeBody,fontSizeLabel,borderRadius}`.

An unset brand-driven slot on a text overlay auto-binds to its token (you don't
have to spell out every one); spell out the ones you care about. A `$brand:` ref
that doesn't resolve is **loud** in render logs and a contrast-critical text color
falls to a legible neutral — it never silently ships an off-brand frame.

Set `brandKitId` at the top of the composition. `apply_composition` with
`dry_run:true` validates the batch without persisting — validate before you
compose.

### Worked example — branded seed composition (16:9)

`brandKitId` ties the kit in; the intro/outro/logo come from the kit
automatically (NOT authored here); the `lower-third` binds `$brand:` tokens and
the `captions` are themed by the kit's `captionProfile`. Swap `<…>` for real ids;
durations are illustrative — match your source.

```json
{
  "v": 1,
  "format": { "aspectRatio": "16:9", "fps": 30 },
  "brandKitId": "<brandKitId>",
  "tracks": [
    {
      "id": "v-screen", "kind": "video", "contents": [
        {
          "id": "rec", "startTime": 0, "duration": 12,
          "source": {
            "kind": "media", "mediaId": "<screenMediaId>",
            "reframe": { "segments": [
              { "startSec": 0,  "endSec": 2,  "focus": { "mode": "frame-center" }, "zoom": 1 },
              { "startSec": 2,  "endSec": 5,  "focus": { "mode": "point", "x": 0.28, "y": 0.42 }, "zoom": 0.6,  "ease": { "in": 0.4, "out": 0.4 } },
              { "startSec": 5,  "endSec": 7,  "focus": { "mode": "frame-center" }, "zoom": 1,    "ease": { "in": 0.4, "out": 0.4 } },
              { "startSec": 7,  "endSec": 10, "focus": { "mode": "point", "x": 0.72, "y": 0.66 }, "zoom": 0.55, "ease": { "in": 0.4, "out": 0.4 } },
              { "startSec": 10, "endSec": 12, "focus": { "mode": "frame-center" }, "zoom": 1,    "ease": { "in": 0.4, "out": 0.4 } }
            ] }
          }
        }
      ]
    },
    {
      "id": "ov", "kind": "overlay", "contents": [
        {
          "id": "title", "startTime": 1, "duration": 3.5,
          "source": {
            "kind": "overlay", "primitiveId": "lower-third",
            "params": {
              "text": "One-command deploys", "subtitle": "Acme", "variant": "modern",
              "tokens": {
                "textColor": "$brand:colors.textOnMedia",
                "accentColor": "$brand:colors.accent",
                "fontFamily": "$brand:fonts.heading.family"
              }
            }
          }
        }
      ]
    }
  ],
  "captions": {
    "segments": [
      { "words": [
        { "text": "Ship",    "startMs": 0,    "endMs": 360 },
        { "text": "in",      "startMs": 360,  "endMs": 520 },
        { "text": "one",     "startMs": 520,  "endMs": 760, "emphasis": true },
        { "text": "command", "startMs": 760,  "endMs": 1300 }
      ] }
    ]
  }
}
```

## 5. Refine + judge → `compose { fromComposition: true }`

Hand the seed to the Director: `compose` with `{ fromComposition: true }`
authors an ensemble of candidates from your seed, runs the **server-side judge —
including the brand axis** (on-brand color/type/voice cohesion), and saves the
winner. Returns a `composeJobId`; `wait_job` `kind:"compose"` (or a webhook on
`compose.completed`). The result carries the winner's composite score — verification
is built in. Pass your brief as `editorialIntent` so editorial is graded against
what you meant. (To self-drive the loop instead, see `cueframe-compose-loop`.)

## 6. Render → branded MP4

`create_render` → `wait_job` `kind:"render"` (or a webhook on `render.completed`)
for the download URL. The output is brand-frozen: the kit's **intro/outro** bumper
the video, the **logo** bug sits in its corner, **motion** drives the overlay
entrances, and every `$brand:` color/font is resolved. Verify the output (sample
frames) before declaring done.

## Notes / honesty

- **The brand kit is the source of truth — edit it, re-render, re-theme.** Brand
  values are resolved at render from the `brandKitId`-referenced kit, so a
  `create_brand_kit` upsert (same `kitId`) re-themes every existing composition
  that points at it. Don't bake brand hexes/fonts into clips.
- **Intro / outro / logo are NOT clips you author** — they live on the kit and
  the engine places them at render (intro prepended, outro appended, logo painted
  as a corner mark). A srcless/absent bumper or logo reserves/draws nothing (soft)
  — it's just skipped, never an error.
- **`watermark` is accepted by `create_brand_kit` and persisted, but render does
  NOT yet auto-composite the kit's watermark asset** (the only watermark painted
  today is CueFrame's product mark). Set it for forward-compat, but custom
  watermarks are not composited into the output yet — don't promise one.
- **Drive CueFrame directly.** Everything downstream of the capture — the brand,
  the compose, the render — is CueFrame. Reach for an external generator only for
  footage CueFrame genuinely can't produce — not to "make it look branded,"
  which is the engine's job now.
- This recipe lives in a skill on purpose: the engine stays use-case-free; the
  product opinions (what to extract, which overlays, how to brand) live here and
  ship via `npx -y cueframe@0.12 install`.
