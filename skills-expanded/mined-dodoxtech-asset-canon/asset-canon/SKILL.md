---
name: asset-canon
description: Orchestrator skill for generating production-ready image assets. Reads an asset brief, selects the right specialist (icon / illustration / sprite / texture / social), drives the image model to produce the image(s), then post-processes (transparent background, resize, webp/png export, deterministic file names) and writes them into the project. Instruction-first — the agent runs the pipeline with its own tools; bundled scripts are an optional repo/CI convenience. Enforces a single consistent palette, fixed canvas sizes, alpha-correct edges, and zero AI slop. Use whenever the user asks to create, generate, redraw, or batch produce visual assets for a website, app, or game.
---

# ASSET-CANON — CODEX IMAGE ASSET ORCHESTRATOR

You are an asset director that turns a short brief into a set of **production-ready image files** on disk, using Codex as the generation executor.

You do not just "make an image." You run a deterministic pipeline:

```
BRIEF  ->  PLAN  ->  GENERATE  ->  POST-PROCESS  ->  WRITE  ->  VERIFY  ->  REPORT
```

---

## HOW THIS SKILL RUNS — instruction-first

This skill is a set of **instructions, not a program the user must install.** Carry out each step with the tools you already have: generate through the image model the environment provides, and use Write / Read / Bash to post-process, record, and verify — all under the user's normal approval prompts, where they can see every command.

The `scripts/` in this repo are an **optional convenience** that automate these steps for people working *inside the asset-canon repo or in CI*. They are **never required** and **never the only way**. Rules:

- A user who only installed the skill should **never** be told to download or run a bundled script to get a result.
- Do the work inline with your own tools by default. Each step below describes the actual procedure; the script is shown only as an *optional shortcut* for repo/CI users.
- When a step genuinely needs an image library (resize, sheet compositing, alpha keying): use a script that is **already present**, or **write a short, readable helper into the user's own project** and run it with their consent — don't pull in an opaque binary.

---

## 0. HARD RULES — READ FIRST

1. **Pixels come from an image model — never from code.** Every asset must be rendered by an image-generation **API/model** (the `codex-imagegen` wrapper, OpenAI Images, or ChatGPT image generation). **Do NOT fabricate the image by drawing it in code** — no canvas/`<canvas>` rendering, no hand-written SVG/HTML/CSS "art", no ASCII, no programmatic shape-drawing dressed up as the asset. Those are not production art and will look like it. If no image model is reachable (no API key, wrapper fails, offline), **stop and say so immediately** — e.g. *"Can't generate: no image model available. I won't hand-draw this in code because the quality won't be acceptable."* — and wait for the user. Never silently substitute a code-drawn placeholder.
2. **Every asset is a real file on disk.** Never return a description in place of an actual generated file. If you cannot run the pipeline, say so explicitly.
3. **One consistent palette per batch.** All assets in a single request share one palette, one line weight, one shading model. Define it once in the PLAN and reuse it.
4. **Fixed canvas, never "approximately."** Each asset type has exact target dimensions. Generate at the largest target, then downscale — never upscale.
5. **Transparent where it matters.** Icons, sprites, illustrations with no background → alpha PNG. Verify the background is actually transparent, not white.
6. **Deterministic names.** Files use `<slug>-<variant>-<WxH>.<ext>` (e.g. `cart-icon-line-512x512.png`). No spaces, no timestamps, lowercase kebab-case.
7. **No AI slop.** No purple/blue glow defaults, no meaningless floating blobs, no fake-3D bevels unless the brief asks. Match the brand, not the model's defaults.
8. **Every asset ships with a sidecar descriptor.** Alongside the image files, write a machine-readable **YAML** descriptor to `docs/assets/<slug>.yaml` that describes the asset's content, style, and intended placement — so another agent can place it correctly **without ever opening the image**. An asset is not "done" until its descriptor exists. (See **ASSET DESCRIPTOR** below.)
9. **Key out a chroma plate — don't trust "transparent".** For any asset that needs a transparent background (icon, sprite, illustration), generate it on a solid **chroma-green** plate (`#00B140`) and key that green to alpha in post. Direct "transparent" output leaves white halos and ragged alpha. **The asset's own colors must avoid the green family (~`#00A040`–`#40FF80`)** — if any part of the subject uses that green, keying will punch holes in the asset. If the subject is naturally green (a leaf, a frog, money), switch to a **chroma-magenta** plate (`#FF00FF`) and forbid magenta instead. Full-bleed assets (texture, social) keep their background and skip this.

---

## CHROMA-KEY BACKGROUND (transparent assets)

The plate exists only to be deleted. Pick the plate color that is *furthest* from everything in the asset, then forbid that color in the subject.

```
GOOD  ┌───────────────┐      BAD   ┌───────────────┐
      │███████████████│            │███████████████│
      │███┌───────┐███│            │███┌──▓▓▓──┐███│  ← asset uses the SAME green
      │███│ asset │███│            │███│ as▓et │███│    as the plate
      │███│ #FF5C │███│            │███│ #2FE0 │███│
      │███└───────┘███│            │███└──▓▓▓──┘███│
      │███████████████│            │███████████████│
      └───────────────┘            └───────────────┘
   plate #00B140, asset has         keying #00B140 also deletes the
   zero green → clean alpha cut      green pixels INSIDE the asset → holes
```

- **GOOD:** plate `#00B140`; asset palette is orange/charcoal/cream with no greens. Keying the green yields crisp, hole-free alpha edges.
- **BAD:** plate `#00B140`; asset has a green leaf/badge in the same hue range. Keying eats the leaf, leaving transparent gaps mid-asset.
- **FIX for green subjects:** swap the plate to chroma-magenta `#FF00FF` and forbid magenta in the asset instead.

### Key with a tolerance, never an exact hex match

The model **does not paint a perfectly flat plate.** A `#FF00FF` plate comes back as a cloud of near-magenta pixels — `#F00AD9`, `#F20CDB`, `#E707D4`, etc. — plus a halo where the plate bleeds into the subject's edge. Matching the exact plate color leaves a fringe of leftover background.

So key by **distance, not equality:**
1. **Threshold, not equality.** Treat a pixel as background if it's within a tolerance of the plate color — e.g. Euclidean distance in RGB below a threshold (start ~60/255 and widen if residue remains), or convert to HSV and key the plate's **hue band** (magenta ≈ 290–330°, green ≈ 120–150°) with loose saturation/value bounds. This catches `#F00AD9` and `#E707D4` even though neither equals `#FF00FF`.
2. **Spill suppression on the edge.** After cutting alpha, the surviving rim pixels often still lean toward the plate hue (magenta/green tint). Desaturate that residual cast on near-transparent edge pixels so the outline doesn't glow.
3. **Soft alpha, not a hard 1-bit cut.** Ramp alpha across the threshold band so edges anti-alias instead of jaggedly stair-stepping.

### Re-check the output — prove the plate is gone

`sharp` keys the pixels, but it does not *confirm* the result — and an exact-match key can silently leave residue. After keying, **scan the output and verify no plate-family color survives** among the non-transparent pixels:
- sample the opaque pixels and assert **none** fall inside the plate's hue/distance band (no leftover `#F0xxDx`-type magenta, no leftover green);
- confirm the four corners read fully transparent (alpha 0), since the plate always reached the corners;
- confirm the subject is intact — no interior holes (the BAD case above).

If any plate-colored pixels remain, **widen the tolerance and re-key**, then re-check — don't ship a fringed asset. Only when the scan is clean is the cutout done.

> *Optional (repo/CI):* `node "${CLAUDE_PLUGIN_ROOT:-.}/scripts/asset-qa.mjs" --in <dir> --require-alpha --plate '#FF00FF' --plate-tol 70` fails the asset if any opaque pixel still sits within the tolerance band of the plate.

---

## 1. BRIEF — what to extract

> **First, is this a restyle?** If the user asks to change the style of assets that *already exist* ("switch to Disney style", "make everything flat", "recolor the set"), don't treat it as a new brief — jump to the **RESTYLE** flow (update the profile → confirm → regenerate from the existing descriptors).
>
> **Or a style extraction?** If the user imports a reference image to anchor the look ("match this image", "use this as the style", "make assets that look like this"), don't reverse-engineer the style here — read **`reference/asset-style-extract.md`** and follow it: it reads the reference and writes `docs/assets/styles/style-profile-<slug>.yaml`. Then generation continues normally, inheriting that profile.

Before generating anything, resolve these. Ask only if a value is load-bearing and missing:

- **Asset type** → icon / illustration / sprite / texture / social (routes to a specialist skill)
- **Subject(s)** → list of concrete items ("cart, heart, bell" → 3 assets)
- **Style** → flat / line / duotone / pixel / 3d-clay / photographic / gradient-mesh
- **Palette** → hex list, or derive from the project's existing tokens/CSS
- **Dimensions** → use the specialist's default if unspecified
- **Format** → png (alpha), webp, svg-trace, or sprite-sheet
- **Output dir** → **detect the project's framework and write to its conventional public/static folder** (see OUTPUT TARGET below). Never assume `assets/` blindly.
- **Count / variants** → how many, and which variations (color, size, state)

## 2. PLAN — write it before generating

Emit a short plan the user can sanity-check:

```
Palette:   #0B0B0F bg, #F5F5F5 fg, #FF5C39 accent
Style:     flat line, 2px stroke, 24px grid, 4px corner radius
Assets:    3  ->  cart, heart, bell
Canvas:    512x512, transparent PNG
Target:    Next.js detected -> public/assets/icons/   (see OUTPUT TARGET)
Specialist: asset-icon
```

Route to the matching specialist reference (`reference/asset-icon.md`, `reference/asset-illustration.md`, `reference/asset-sprite.md`, `reference/asset-texture.md`, `reference/asset-social.md`) and follow its art-direction rules for the prompt.

**Persist the style at two levels.** Don't keep palette/style only in this transient plan — write it out so it's reproducible:
- **Project (shared):** write `docs/assets/styles/style-profile-<slug>.yaml` once, so every later generation and every other agent inherits the same context. Then write/update the pointer `docs/assets/styles/active.yaml` (`active: style-profile-<slug>.yaml`) so readers know **which** shared profile is in force — multiple can coexist (e.g. an old version, a new RESTYLE), only the one `active.yaml` names is current.
- **Per asset (snapshot):** for **each** asset the user describes, freeze the *resolved* style it was generated with into `docs/assets/styles/style-profile-<slug>.yaml` — the shared profile merged with any per-asset overrides (a one-off accent, a different camera). This is the exact recipe that produced that asset, so a variant or a re-render months later reproduces it pixel-for-pixel without guessing.

Sanity-check both by reading back: `id`, a hex `palette`, and a `prompt_suffix` are required. The full shape is in **STYLE PROFILE** below.

> *Optional (repo/CI):* `node "${CLAUDE_PLUGIN_ROOT:-.}/scripts/validate-style-profile.mjs" --in docs/assets/styles/style-profile-<slug>.yaml` gates the profile automatically.

## 3. GENERATE — drive the image model

Generate each asset with the **image model the environment provides** (the user's configured image generation / API). Build one structured prompt per asset:

```
<art-directed prompt from specialist>
+ "centered on a solid chroma-green #00B140 background, no green anywhere in the subject"   (transparent assets)
+ the style profile's `prompt_suffix`
+ "Avoid: <the profile's `negative` list>"
```

You apply the shared style yourself: resolve the active profile (read `docs/assets/styles/active.yaml` → its `active:` field → read that `docs/assets/styles/style-profile-<slug>.yaml`), append its `prompt_suffix` and `Avoid: …` to every prompt, and carry its `seed` if the backend supports one — **this is what keeps a batch consistent.** Generate at the **largest** required size once; downscale in post-process. For transparent assets, bake the chroma plate into the prompt (see **CHROMA-KEY BACKGROUND**) and key the green to alpha in post — don't ask the model for "transparent" directly.

For a batch, generate **sequentially in the same run** and announce progress: `Asset 1 of 3: cart`, `Asset 2 of 3: heart`, …

> *Optional (repo/CI):* the wrapper applies the profile and calls the Codex CLI / OpenAI image API for you:
> ```bash
> node "${CLAUDE_PLUGIN_ROOT:-.}/scripts/codex-imagegen.mjs" --prompt "<…>" \
>   --size 1024x1024 --background opaque --style-profile docs/assets/styles/style-profile-<slug>.yaml \
>   --out assets/generated/icons/cart-icon-line-1024x1024.png
> ```

## 4. POST-PROCESS — make it production-ready

What has to happen:
- Key the chroma plate to alpha (transparent assets).
- Downscale to every requested size (never upscale).
- Export requested formats (webp for web, png for alpha-critical, ico for favicons).
- Strip metadata, quantize where lossless allows.
- For sprites: pack frames into a grid sheet + emit an atlas.
- For textures: run the seamless-edge check.

These touch real pixels, so they need an image library — **`sharp`**. Background removal (keying the chroma plate to alpha), resizing, and format export all depend on it.

**Before any pixel step, check that `sharp` is reachable** (e.g. `node -e "require('sharp')"` in the directory the work runs from). If it's missing, **stop and recommend the user install it** rather than skipping or faking the post-process:

> *"To remove the background and export the size/format ladder I need `sharp`. It's not installed. Run `npm install sharp` (downloads a native libvips binary for your OS), then I'll continue."*

Wait for their go-ahead, then proceed. Use whatever is **already available**: if the asset-canon repo is present, its `optimize-assets.mjs` / `pack-sprite.mjs` do this; otherwise write a short, readable helper into the user's project and run it with their consent. Don't make the user fetch and trust an opaque binary.

If the user declines `sharp`, say plainly what you **can't** do (no transparent background, no resize ladder, no webp/ico) and deliver only what's possible (the raw generated image) — never silently ship an asset that still has its chroma-green plate.

> *Optional (repo/CI):*
> ```bash
> node "${CLAUDE_PLUGIN_ROOT:-.}/scripts/optimize-assets.mjs" --in assets/generated/icons --sizes 512,256,128,64 --formats webp,png --strip
> ```

## 5. WRITE + REPORT

Write files to the **framework-detected target** (OUTPUT TARGET above — e.g. `public/assets/icons/` for Next.js, `assets/` as fallback) using the deterministic naming scheme. **For every asset, also write two sidecars in the same step:**
- its descriptor to `docs/assets/<slug>.yaml` (what the image *is* — content, placement; see ASSET DESCRIPTOR below),
- its resolved style snapshot to `docs/assets/styles/style-profile-<slug>.yaml` (the style recipe that *produced* it; see STYLE PROFILE below).

The image, its descriptor, and its style snapshot land together — an asset is not "done" until all three exist. Then report a table:

```
| file                              | size    | format | bytes |
|-----------------------------------|---------|--------|-------|
| cart-icon-line-512x512.png        | 512x512 | png    | 4.1KB |
| cart-icon-line-512x512.webp       | 512x512 | webp   | 2.3KB |
```

Note the descriptor path in the report (`docs/assets/cart.yaml`), then end with the reference snippet that matches the **detected framework** — a `public/`-served file is referenced by URL, not imported (e.g. Next.js: `<img src="/assets/icons/cart-icon-line-512x512.webp" />`), whereas a bundled `src/assets` path is imported (e.g. `import cart from "@/assets/icons/cart-icon-line-512x512.webp"`).

## 6. VERIFY — final acceptance gate

**Don't call it done on faith.** After writing, run a last pass over the **files on disk** and confirm each asset meets the standard. Only report success for assets that pass; for any that fail, fix and re-run the relevant step (re-key, re-export, regenerate) before reporting.

The checklist — per asset:
- **Naming** — `<slug>-<variant>-<WxH>.<ext>`, lowercase kebab-case, no spaces/timestamps.
- **Dimensions** — actual pixels equal the `WxH` in the filename (no upscale lie).
- **Background** — for transparent assets: corners are alpha 0 **and** no plate-family residue survives among opaque pixels (see CHROMA-KEY re-check). Full-bleed assets: background intact, no stray alpha.
- **Subject integrity** — no interior holes punched by keying.
- **Palette** — colors stay within the batch budget; no off-palette slop (purple/blue AI glow, fake bevels).
- **Formats** — every requested format/size actually emitted.
- **Sidecars exist** — `docs/assets/<slug>.yaml` **and** `docs/assets/styles/style-profile-<slug>.yaml` are present and truthful (list only files that exist).
- **Textures** — seamless edge-wrap verified. **Sprites** — frame count + atlas match the sheet.

End the report with an explicit verdict per asset — `✓ PASS` or `✗ FAIL: <reason>` — never a silent "done."

> *Optional (repo/CI):* `node "${CLAUDE_PLUGIN_ROOT:-.}/scripts/asset-qa.mjs" --in <dir> --require-alpha --max-colors N --plate '#FF00FF' --plate-tol 70` runs naming/dimension/alpha/palette/plate-residue as a CI-friendly gate (exit 1 on any failure), and `validate-descriptors.mjs` gates that every asset has its descriptor.

---

## ASSET DESCRIPTOR (sidecar metadata)

Goal: an agent that has **never seen the pixels** can read the descriptor and know what the asset depicts, how it looks, and where it belongs. One YAML file per logical asset at `docs/assets/<slug>.yaml`; all size/format variants are listed inside it.

Write it directly with the Write tool — you authored the prompt and know the content. Get the measurable facts honestly: bytes via `wc -c` / `ls -l`, and pixel dimensions from the size in the filename (or the image tool). List **only files that exist**.

> *Optional (repo/CI):* author the descriptive content as a JSON spec and let the writer measure bytes/dims and emit canonical YAML, then gate the batch:
> ```bash
> node "${CLAUDE_PLUGIN_ROOT:-.}/scripts/write-descriptor.mjs" --spec cart.spec.json
> node "${CLAUDE_PLUGIN_ROOT:-.}/scripts/validate-descriptors.mjs" --in assets/generated/icons
> ```

```yaml
# docs/assets/cart.yaml
id: cart
type: icon                      # icon | illustration | sprite | texture | social
subject: shopping cart          # the concrete thing depicted
description: >                  # plain-language content, enough to place it blind
  A minimal line-art shopping cart facing right, single charcoal stroke,
  no fill, no background. Reads as "add to cart / checkout".
keywords: [cart, ecommerce, checkout, basket, buy]
placement:                      # where another agent should USE this
  intended_use: primary "add to cart" button and cart nav link
  context: ecommerce header, product cards
  do: [use at 24–32px in UI, pair with accent on hover]
  dont: [do not stretch, do not place on busy photo backgrounds]
style:
  art_style: flat line
  stroke: 2px @ 24px grid
  shading: none
palette: ["#1A1A1A"]            # the asset's actual colors (not the chroma plate)
background: transparent         # transparent | full-bleed | chroma-keyed
dimensions:
  master: 1024x1024
  aspect: "1:1"
safe_area: full                 # or e.g. "inner 90%" for social
accessibility:
  alt_text: "Shopping cart icon"
files:                          # every variant on disk, by path
  - path: assets/generated/icons/cart-icon-line-512x512.webp
    size: 512x512
    format: webp
    bytes: 2360
  - path: assets/generated/icons/cart-icon-line-512x512.png
    size: 512x512
    format: png
    bytes: 4180
source:                         # provenance — never a code-drawn asset
  model: codex-imagegen (openai images)
  prompt: "Minimal flat line icon of a shopping cart, 2px stroke, …"
  generated: 2026-06-23
```

**Type-specific blocks to add when relevant:**

- **sprite** — add an `animation` block so the motion is reconstructable without opening the sheet:
  ```yaml
  animation:
    sheet: assets/generated/sprites/hero_run-512x128.png
    cell: { w: 64, h: 64 }
    columns: 8
    count: 8
    fps: 12
    loop: true
    anchor: [0.5, 1.0]
    clips: { run: [0, 7] }
  ```
- **social** — add `platform: og` / `safe_area: inner 90%` / `text_overlay: "added in code, not baked"`.
- **texture** — add `tileable: true`, `tile_size: 1024x1024`, `tonality: low-contrast`.
- **illustration** — add `composition: "negative space top-right for headline"`.

Rules: keep `description`/`placement` truthful to what was actually generated; list **only files that exist**; the `palette` is the asset's own colors, never the chroma plate. If you batch N assets, write N descriptor files (one per slug).

---

## STYLE PROFILE (shared style context)

A descriptor describes **one output**; the style profile prescribes the **shared input style** that keeps every asset consistent. It is the design-tokens-as-style-brief pattern (Style Dictionary / Penpot) applied to image generation: define the look once in `docs/assets/styles/style-profile-<slug>.yaml`, and every generation — now or months later, by you or another agent — inherits it.

Write `docs/assets/styles/style-profile-<slug>.yaml` in the user's project using the shape below, then on **every** generation apply it yourself:
- append `prompt_suffix` (the positive style anchor) to the prompt,
- append `Avoid: <negative…>` (the anti-slop guard),
- carry `seed` if the backend supports one (gpt-image-1 has no seed parameter, so skip it there).

Required fields: `id`, `palette` (hex), `prompt_suffix`. Recommended: `line`, `shading`, `negative`, `seed`. Commit it so the style is reproducible.

**Which profile is active.** `docs/assets/styles/` holds many `style-profile-<slug>.yaml` files — the shared project look(s) (slug = the *style* name, e.g. `acme-v1`, `ref-hero-v1`) plus one per-asset snapshot per generated asset (slug = the *asset* name, e.g. `cart-icon`). A one-line pointer file names which shared profile is the **active reference** every generation inherits:

```yaml
# docs/assets/styles/active.yaml
active: style-profile-<slug>.yaml   # filename, relative to docs/assets/styles/
```

Every reader resolves the style through `active.yaml` first, then loads the file it names. Switching the project's look = write the new look as its own `style-profile-<new-slug>.yaml` and repoint `active.yaml` at it; no file is overwritten, so old versions stay reproducible. Per-asset snapshots are addressed directly (by their asset slug) and are **not** pointed at by `active.yaml`.

**Optional richer blocks** (written by `asset-style-extract` when a profile is reverse-engineered from a reference image, ignored safely by every reader that doesn't need them): `source_ref` (path to the analyzed reference), `medium`, `swatches` (palette colors with `role` + area `weight`), `ramps` (per-material shadow→mid→highlight), `color` (saturation/temperature/contrast/harmony/hue_shift), `fx`, and `confidence` (per-field certainty). `palette` itself stays a **flat hex list** so the validator and the generator keep working — the detail lives in these side blocks.

**Two tiers — shared source + per-asset snapshot** (both are `style-profile-<slug>.yaml` files; they differ only in what the slug names). The file below is the *project source* (slug = the style name; this is what `active.yaml` points at). Additionally, every time the user describes an asset, freeze the **resolved** style for that one asset to `docs/assets/styles/style-profile-<asset-slug>.yaml`: copy the active shared profile, apply any per-asset overrides actually used (a one-off accent, a different `camera`, a `magenta` plate for a green subject), and set `id` to `<style-slug>/<asset-slug>` so the snapshot records its parent. This snapshot is the exact recipe that produced the asset — point a future `--style-profile` at it to make a faithful variant. The shared profile keeps the *batch* consistent; the per-asset snapshot makes a *single asset* reproducible.

```yaml
# docs/assets/styles/style-profile-<slug>.yaml — the SHARED style context for a whole project.
# Define it once; every generation (and every other agent) reads it so assets
# stay visually consistent — design-tokens-as-style-brief applied to image gen.
# The generator injects prompt_suffix + "Avoid: <negative>", and seed (only on
# backends that support it — gpt-image-1 has no seed param).

id: acme-v1                         # required — name/version of this style
palette:                            # required — the brand colors (hex)
  - "#0B0B0F"
  - "#F5F5F5"
  - "#FF5C39"

line:
  weight: "2px @ 24px grid"
  style: uniform                    # none | uniform | tapered
shading: flat                       # flat | two-tone | soft-gradient
lighting: top-left
camera: front-flat                  # front-flat | side | iso
proportions:
  head_body: "1:6"

# Appended to every prompt — the positive style anchor.
prompt_suffix: "flat vector, cohesive Acme brand, crisp edges"

# Appended as "Avoid: …" — the anti-slop guard.
negative:
  - "purple/blue AI glow"
  - "fake 3D bevel"
  - "meaningless floating blobs"
  - "gradient mesh"

# Locked seed for reproducibility. Honored only by backends that support it;
# gpt-image-1 has no seed parameter, so it is recorded for provenance but not sent.
seed: 73122
```

> *Optional (repo/CI):* `validate-style-profile.mjs` gates the profile and `codex-imagegen.mjs --style-profile docs/assets/styles/style-profile-<slug>.yaml` applies it automatically.

> **Scope note:** this is text/structured conditioning only. A profile can be **reverse-engineered from a reference image** by `asset-style-extract` (which fills the optional blocks above and records `source_ref`), but the conditioning that reaches the model is still text — `prompt_suffix` + `Avoid: <negative>`. Stronger visual locking — passing the `source_ref` image to gpt-image-1, or a local SD + LoRA backend — is a deliberate future step the schema is forward-compatible with, not part of this profile yet.

---

## RESTYLE — change the style of assets that already exist

When the user asks to **change the style of what's already generated** — *"switch from pixel to Disney style"*, *"make everything flat"*, *"recolor the set to our new palette"* — do **not** treat it as a fresh brief and do **not** start generating. Run this flow, in order:

**1. Update the style profile first — generate nothing yet.**
Resolve the current profile through `docs/assets/styles/active.yaml`, apply the requested change (e.g. `style: pixel → 3d-clay/disney`, rewrite `prompt_suffix`, adjust `palette`/ramps/`shading`/`negative` to match), and **bump the `id`** to mark the new version (e.g. `acme-v1 → acme-disney-v1`). Write the new version as a **new** `docs/assets/styles/style-profile-<new-slug>.yaml` (don't clobber the old one — it stays reproducible) and repoint `active.yaml` to it. Show the user the before→after of the key fields so the new direction is explicit.

**2. Enumerate what exists — read the sidecar files (this is "check the current JSON").**
Glob `docs/assets/*.yaml` (the descriptors) and `docs/assets/styles/style-profile-*.yaml` (the per-asset snapshots). These are exactly what makes regeneration possible *without the original prompts*: each descriptor carries the asset's `subject`, `type`/specialist, `placement`, files, and content; each snapshot carries the style it was last made with. Build the list of affected assets from them.

**3. Confirm before regenerating — ask, don't auto-burn.**
Present the change and the impact, then stop for a decision:
> *"Updated the style profile to **disney-v1**. This affects **N** assets: cart, hero, knight-run, … Regenerate them now? — **all** / **pick some** / **none** (profile stays updated; new assets will use it)."*
Generation costs money and overwrites files, so never skip this confirmation. If the user says none, you're done — the profile is updated and future generations inherit it.

**4. On approval, regenerate each chosen asset.**
For each one: rebuild the prompt from its **descriptor** (`subject` + `type` + composition/placement notes) merged with the **new** style profile, route to the matching specialist, run GENERATE → POST-PROCESS → WRITE → VERIFY. Because names are deterministic, the new files **overwrite the same paths** (same `<slug>-<variant>-<WxH>.<ext>`), so nothing in the user's code needs to change. Update each per-asset **style snapshot** to the new resolved style, and update the **style fields** of each descriptor (keep its `subject`/`placement`/content truthful — only the look changed).

**5. Report** the before→after profile `id`, which assets were regenerated (and which were skipped), and the file paths touched.

> Selective restyle is supported by design: the user can keep a one-off asset on its old snapshot (skip it in step 3) while the rest move to the new profile — the per-asset snapshot is what preserves that divergence.

---

## OUTPUT TARGET — detect the framework, write to its public folder

Don't dump assets in a generic `assets/` by default. **First detect what the project is**, then write the image files where that framework actually serves static assets. Detect by reading the manifest/config at the repo root (don't guess from a single file):

| Detected by | Framework | Asset target |
|---|---|---|
| `next.config.*`, or `next` in `package.json` deps | **Next.js** | `public/assets/` |
| `nuxt.config.*`, or `nuxt` in deps | **Nuxt** | `public/assets/` (Nuxt 3) — fall back to `static/assets/` if a `static/` dir exists (Nuxt 2) |
| `astro.config.*` | **Astro** | `public/assets/` |
| `svelte.config.*` + `@sveltejs/kit` | **SvelteKit** | `static/assets/` |
| `vite.config.*` (no Next/SvelteKit) | **Vite** (Vue/React/Solid) | `public/assets/` |
| `react-scripts` in deps | **Create React App** | `public/assets/` |
| `angular.json` | **Angular** | `src/assets/` |
| `gatsby-config.*` | **Gatsby** | `static/assets/` |
| `vue.config.*` | **Vue CLI** | `public/assets/` |
| `_config.yml` + `Gemfile`, or `config.toml`/Hugo | **Jekyll / Hugo** | `static/assets/` (Hugo) · `assets/` (Jekyll) |
| an existing `public/` dir, nothing else recognized | static site | `public/assets/` |
| **nothing recognized, or empty repo** | unknown | `assets/` (repo-root fallback) |

Rules:
- **Confirm before writing** if detection is ambiguous or the target dir doesn't exist yet: state the framework you detected and the path you'll write to, e.g. *"Detected Next.js → writing to `public/assets/icons/`. OK?"*
- Append the **asset-type subfolder** under the target: `icons/`, `illustrations/`, `sprites/`, `textures/`, `social/`.
- If the user gave an explicit output dir in the brief, **that wins** — skip detection.
- **Descriptors and style snapshots stay in `docs/`** regardless of framework (`docs/assets/<slug>.yaml`, `docs/assets/styles/`). Only the *served image files* follow the framework convention.
- Monorepo: detect within the **package/app the user is working in**, not the workspace root.

> *Optional (repo/CI):* a one-liner that reads `package.json`/configs and prints the target keeps this deterministic, but the agent can resolve it inline from the table above.

---

## ROUTING TABLE

| Brief says… | Read this reference |
|---|---|
| favicon, app icon, glyph, ui icon set | `reference/asset-icon.md` |
| hero art, spot illustration, empty state | `reference/asset-illustration.md` |
| game sprite, character, tile, spritesheet | `reference/asset-sprite.md` |
| background, pattern, seamless, surface | `reference/asset-texture.md` |
| OG image, social card, thumbnail, banner | `reference/asset-social.md` |
| "match this image", imported reference to copy the look from | `reference/asset-style-extract.md` |

When in doubt, ask the user which specialist fits, then commit to one palette and run the pipeline.

> `reference/asset-style-extract.md` is a **pre-step**, not an output specialist: it produces a style profile from a reference, then you route the actual subject to one of the five generators above.
