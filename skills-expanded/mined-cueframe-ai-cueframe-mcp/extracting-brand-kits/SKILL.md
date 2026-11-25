---
name: extracting-brand-kits
description: >-
  Use when the user says "make my video look like THIS" with a reference video, screenshots, or a moodboard — build a CueFrame brand kit FROM that inspiration so every subsequent compose speaks its visual language. Owns the extraction step: sample the reference's graphics-bearing frames, upload them as exemplars, reproduce each recurring motif as an authored graphic verified against the reference, and upsert the kit with the full language payload. Triggers on "match this style", "like this reference", "use this video as inspiration", "extract a brand kit", "moodboard". Hand off to cueframe-storyboard/composing-video once the kit is bound.
---

# Extracting brand kits: reference pixels → a kit the engine honors

Use the [project and capability policy](../composing-video/references/project-policy.md) for scope, current state and metered work.

## The one idea

**No summarization anywhere in the path.** A reference described in prose converges on house style
with the reference's palette — the pixels are the ground truth. You (the agent) are the extractor:
you SEE the reference, curate its frames, and reproduce its motifs as ordinary authored graphics,
verified against the reference by looking. The kit you produce carries (a) **exemplar frames** the
compose maker and judge both see, and (b) **motif skins** — card HTML the designer reproduces —
plus code-checked facts (caption profile, density, palette). Once bound to a project, the engine
takes over: the planner plans to your density, the designer sees your exemplars
(`view_style_reference`), the judge grades every candidate against them, and a half-applied kit
fails the compose loudly instead of shipping house style.

Everything below drives the public `/v1` API with your API key. Frames never pass through chat —
they go straight to storage via presigned PUTs.

## 0. Prereqs

- An API key with `projects:write`. `create_brand_kit` gates on the `brand_kits` entitlement, which EVERY plan grants including free, and it costs no credits — so brand kits are not a paywall to route around. (`get_account` confirms it; a 402 names the feature.)
- `ffmpeg` locally, and the reference video file (download it first if it's a URL).
- Know the org's IDENTITY kit if one exists (`get_profile` → brandKits). Inspiration NEVER overwrites identity: logo, brand fonts, and identity color slots come from the existing kit (or stay for the user to fill) — extraction contributes the LANGUAGE only.

## 1. Sample the reference (local, ffmpeg)

Uniform sampling misses short-lived graphics (1–3s overlays). Sample two ways and union:

```bash
# scene cuts
ffmpeg -i ref.mp4 -vf "select='gt(scene,0.22)',showinfo" -vsync vfr scenes/%03d.jpg
# 2fps sweep (catches overlays that appear without a cut)
ffmpeg -i ref.mp4 -vf fps=2,scale=720:-1 -q:v 4 sweep/%04d.jpg
```

Then LOOK at the frames and curate: keep the **graphics-bearing** ones — frames where a card,
pill, stat, lower-third, caption treatment, or end-card is visible and sharp. Drop near-duplicates.
**≤24 frames**, each downscaled to ≤720px width, jpeg. For each animated graphic, also note the
timestamp where it ENTERS (you'll classify its motion in step 5; re-watch that 1s window at
`ffmpeg -ss <t> -t 1 -i ref.mp4 -vf fps=12 burst/%02d.jpg` if you need to see the entrance).

Optional but recommended: build a contact sheet for the human's "right vibe?" check:
`ffmpeg -i frames/frame-%02d.jpg -filter_complex tile=6x4 sheet.jpg`.

## 2. Upload the exemplars (the ingest door)

```
POST /v1/brand-kits/exemplar-uploads  { "count": <n>, "includeContactSheet": true }
```

Returns presigned PUT slots under the org's `brand-inspiration/…` prefix — the ONLY namespace the
kit door accepts exemplar keys from. PUT each curated frame (order matters: frame-01 ↔ index 0 —
motif `evidence` arrays reference these indexes), PUT the sheet, keep the returned `key` list.
URLs expire in 15 minutes; re-POST for a fresh batch if you run over.

## 3. Inventory the motifs

Look across the exemplars and list every RECURRING graphic treatment (expect ~5–12 for a designed
reference). For each, write:

- `id` — `m1`, `m2`, …
- `observed` — one precise sentence ("thin-outline rounded keyword pill, single word, beside subject").
- `role` — the closed vocabulary the planner/designer speak (exact values):
  `title-card | stat | lower-third | pull-quote | hero | logo-tag | enumeration | sequence | comparison`.
  Pick the role each motif best SERVES — the designer's steering matches on it exactly.
- `evidence` — the exemplar indexes (0-based) it appears in.
- `zone` — normalized `{x, y, w, h}` where it lives.
- Behind-the-subject motifs (text the speaker occludes): record them with `coverage: "skipped"` and
  `skipReason: "behind-subject — card graphics render front-only"`. Do NOT attempt them.

Also read the CAPTION treatment off the frames (step 6 consumes it): plate or plateless? base/
highlight colors? case? emphasis styling? entrance feel (~ms)?

## 4. Reproduce each motif as a card (author → look → refine, ≤3 iterations)

For each non-skipped motif, author it as a **card** (freeform HTML/CSS — rendered verbatim) and
verify it against the exemplar BY LOOKING:

1. **Measure first**: read the exemplar — border weight, radius, padding, font size relative to
   frame, colors. Measurement-seeded CSS gets you ~90% in one shot.
2. Author `{ "kind": "card", "html": "…", "tokens": { … } }`. Bind every brand-swappable color
   through `tokens` with `$brand:` refs (e.g. `"line": "$brand:colors.accent"`, referenced in CSS
   as `var(--cf-line)`) so the kit's identity re-themes it. No `<script>`, no `@keyframes` (inert —
   motion is step 5).
3. Preview the isolated card with `preview_card` (or `preview_component` for an authored
   component) and compare against the exemplar side by side. Use `cueframe-compose-loop`'s
   [preview workflow](../cueframe-compose-loop/references/preview-workflow.md) for saved-context
   checks and motion windows. Fix the largest visible
   difference. Repeat — **cap 3 iterations**, keep the best.
4. Record `diffScore` (your honest 0–1 same-language judgment) and `coverage`:
   `"reproduced"` (≥0.8) or `"approximated"`.

Prefer a catalog primitive (`list_catalog`) over a card ONLY if it genuinely matches closer —
record it as `{ "kind": "overlay", "primitiveId": "…", "params": { … } }`. A custom component
(`{ "kind": "component", "componentId": "…" }`) only for motifs with internal motion (counters).

## 5. Classify motion (closed vocabulary — never invent animation)

Watch each motif's entrance burst and map it:

- Graphic motion presets (exact values): `fade-up | slide-in-left | slide-in-right | scale-pop | stagger-reveal`,
  with `enterMs` / `exitMs` / `staggerMs` timings you observed.
- Caption per-word entrances: `none | fade | word-pop | stagger-up`.
- Unsure or the reference does something the vocabulary can't say? Pick the NEAREST preset and set
  `"confidence": "low"` — honesty beats fabrication; the vocabulary grows engine-side, not here.

## 6. Compute the facts

- `captionProfile` — from step 3's caption read. The kit door speaks the full look: `color`,
  `highlightColor`, `plate` (`"none"` for the clean plateless look), `entrance`, `entranceMs`,
  `exitMs`, `emphasisColor/Scale/FontWeight/FontStyle`, `emphasisPlate` knobs, `textTransform`.
- `density` — `{ "graphicsPerMin": <count/duration*60>, "maxSimultaneous": <max overlapping> }`.
- Palette → `extraColors` entries `{ "hex", "label": "inspiration accent N", "usage": "swappable" }`.
  NEVER write the identity `colors.*` slots, `headingFont`/`bodyFont`, or `logo` from the
  reference — copy those from the base identity kit, or leave them for the user.
- `styleRubric` — 2–4 sentences the JUDGE will grade with: name the motif language, the caption
  treatment, and what disqualifies a frame ("filled chips or plated captions are off-language").

## 7. Upsert the kit + bind it

One `create_brand_kit` call (it's an upsert — re-POST the same `kitId` to curate):

```jsonc
{
  "kitId": "acme-launchfilm",
  "name": "Acme × Launch Film",
  // identity: copied from the base kit or neutral — never from the reference
  "colors": { … }, "headingFont": { … }, "bodyFont": { … },
  "extraColors": [ { "hex": "#F5B942", "label": "inspiration accent 1", "usage": "swappable" } ],
  "captionProfile": { "plate": "none", "entrance": "fade", "entranceMs": 220, … },
  "exemplarKeys": [ "<keys from step 2, in frame order>" ],
  "contactSheetKey": "<sheet key>",
  "motifs": [ { "id": "m1", "observed": "…", "body": { "kind": "card", … }, "motion": { "preset": "fade-up", "enterMs": 320 }, "role": "pull-quote", "zone": { … }, "evidence": [0, 2], "diffScore": 0.93, "coverage": "reproduced" } ],
  "styleRubric": "…",
  "density": { "graphicsPerMin": 4, "maxSimultaneous": 2 },
  "inspiration": { "sources": ["<reference URL>"], "extractedAt": <now ms>, "extractionVersion": "skill-1" }
}
```

The door validates loudly: exemplar keys must come from step 2's batch, motif roles/presets must be
in-vocabulary, evidence indexes must be in range. A 422 names exactly what to fix.

Then bind: `update_project { "brandKitId": "acme-launchfilm" }`. Show the human the contact sheet
("right vibe?") before composing. From here, hand off to **cueframe-storyboard** — every compose
against the project now plans, designs, and JUDGES in the reference's language, and refuses to
ship house style if any part of the kit fails to resolve.

## Failure honesty

- Reference has no graphics language (talking head, zero overlays)? Say so — upsert nothing, or a
  captions-only kit. Don't invent motifs.
- A motif you can't match in 3 iterations ships as `"approximated"` with its real diffScore — the
  judge's floor will surface it; don't inflate.
- Behind-subject motifs stay `"skipped"` with the reason. The engine refuses them loudly anyway.
