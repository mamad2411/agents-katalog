---
name: video-scroll-effect
description: Executes ONE section of a site plan handed to it by site-planner, using the canvas image-sequence scrub technique (frame-scrub video, not WebGL). Generates the visual (or uses a user-supplied clip), slices it into frames with ffmpeg, builds that section, and deploys the finished site to a live URL. Does NOT decide site structure, section count, or content depth — site-planner owns those decisions. Trigger only via site-planner's hand-off, or directly if the user explicitly asks for the frame-scrub technique by name.
---

# Video-Scroll-Effect — frame-scrub execution engine

## What this actually is (read first)
The viral "3D scroll" effect is **not** Three.js. It's a **canvas image-sequence scrub**:
a short cinematic clip is exported to ~180 numbered JPGs, all preloaded, and the frame
drawn to a `<canvas>` is chosen by scroll progress. Scrolling forward/backward plays the
clip. Add Lenis smooth scroll + scroll-synced overlay copy and it reads as premium 3D.
The "3D" comes entirely from the source video — which we generate with Higgsfield.

Stack: plain **HTML + CSS + JS + Lenis** (zero build, runs from any static server).

## Scope — this skill does NOT decide
This skill executes a section (or sections) from a site plan produced by
site-planner. It does not decide: how many sections a site needs, what
type of sections those are, what the site's overall structure looks like, or
what content depth is appropriate for the product. If invoked without a plan
(e.g. the user asks for video-scroll-effect directly), ask for a `content_brief`,
`motion`, and `palette` for the section being built — do not invent a full
multi-section site structure yourself.

## Prerequisites
- **Higgsfield MCP** connected + credits (~$1–2 / clip) — OR the user can supply their own
  video clip instead (see Step 1b). At least one of these two paths is required.
- **ffmpeg** — expected to already be present in the environment. Step 0 below confirms this.
- This skill installed at `${CLAUDE_PLUGIN_ROOT}/skills/video-scroll-effect/`.

### Step 0 — Confirm ffmpeg (run first, always)
Run `ffmpeg -version`. If this fails, tell the user ffmpeg isn't available in this environment
and stop — do not attempt to download or install it.

## THE PIPELINE — executes one plan section

### 1. Read the section spec
Take the section's `motion`, `content_brief`, and the site's `palette` from the plan
handed off by site-planner. Use `content_brief` to write this section's actual
copy — don't invent unrelated content.

### 1b. Check for a user-supplied clip (skip Higgsfield if present)
Before generating anything, check whether the user's prompt included a video file path,
attachment, or URL to use as the source clip instead of generating one.
- If a usable clip is supplied: skip Steps 2–4 entirely (no Higgsfield calls, no credits spent).
  Use the supplied clip directly as input to Step 5 (frame extraction).
- If the supplied file isn't a video, or ffprobe/ffmpeg can't read it, tell the user plainly
  and ask them to either supply a valid clip or allow Higgsfield generation instead.
- If no clip is supplied at all: proceed to Step 2 as normal (Higgsfield generation).

### 2. Generate the hero keyframe (Higgsfield `generate_image`)
- Model: **`nano_banana_pro`** (top quality / crisp). Prompt from the section's
  `content_brief` and subject, strong lighting, intentional background, "ultra sharp,
  photorealistic, 8k, editorial/advertising". 16:9.
- Poll `job_display` until `status:"completed"`; keep the job **id** (used as the video start frame).

### 3. Generate the cinematic clip (Higgsfield `generate_video`)
- Model: **`seedance_2_0`**, `resolution:"1080p"`, `aspect_ratio:"16:9"`, `duration:6`,
  `medias:[{role:"start_image", value:<keyframe id>}]`. Always pass
  `declined_preset_id:"24bae836-2c4a-48e0-89b6-49fcc0b21612"` if it suggests a preset; if it
  suggests a different preset, retry with that preset's id in `declined_preset_id`.
- Use the section's `motion` value to pick the prompt pattern:
  - **orbit/turntable** — "smooth seamless full 360-degree rotation, one complete revolution, stays centered".
  - **fly-through** — "slow continuous forward camera flight through/around the scene, smooth dolly, deep parallax".
  - **reveal/explode** — "the components burst or assemble outward and float in slow motion" (keep it object/scene context — moderation-friendly).
  - **abstract** — "elegant slow-morphing liquid-metal / glass / particle form drifting and rotating".
  - **molten-birth** — "the subject forms out of a molten/liquid state, pouring and coiling, cooling and solidifying into its final form, slow and continuous" (creation instead of destruction — good for jewelry/craft/material-forward products).
  - **frozen-time** — "the subject and its surrounding motion (splash, spray, debris) hang perfectly frozen while the camera orbits around the suspended instant, nothing moves except the viewpoint" (pairs naturally with a `loopBack` beat that briefly releases the freeze — see "Multi-beat sections" below).
  - **bloom** — "the subject unfurls/opens/grows petal by petal or layer by layer, timelapse-smooth, ending fully open and holding" (growth instead of destruction — good for organic/beauty/botanical products).
  - **descent** — "the subject sinks/descends through its environment, light and color fading from bright to near-total darkness as depth increases, ending in near-black with only the subject's own glow/markers visible" (pairs naturally with `bgFrom`/`bgTo` background interpolation — see "Live scroll-synced meter" below).
  - **light-reveal** — "everything starts in true darkness; a single light beam sweeps across the subject, revealing it section by section as it passes, most of the frame always in shadow" (good when the product itself should feel discovered rather than presented).
  - If `motion` doesn't match any of these, write a new prompt in the same style rather
    than forcing it into one of the above.
- **Cost:** preflight with `get_cost:true` once; ~54 credits per 1080p clip. Confirm if the user is low.

### 3b. Multi-beat sections (`beats` instead of a single `motion`)
A section may declare `beats: ["orbit", "transform", "macro"]` (or similar) instead of
one `motion` value — a chaptered scroll-scrub within a single pinned section, all
generated from ONE shared anchor image so the subject's identity stays locked across
beats (same lighting, same materials, same product) rather than drifting between
independently-generated clips.
- `asset-generator` handles the actual generation/identity-lock (see its SKILL.md) and
  returns one clip per beat, already extracted into `frames/<section>/<beat>/`.
- Each beat gets its own sub-range of the section's overall scroll progress (see Step
  6's `beats` config format below) — earlier beats occupy earlier progress, in the
  order listed.
- A beat can set `loopBack: true` to play its own frames forward through the first half
  of its progress sub-range, then the SAME frames in reverse through the second half —
  one generated clip becomes two narrative beats (explode → reassemble, bloom → close)
  at zero extra Higgsfield cost. Good fit for `frozen-time`/`reveal-explode`/`bloom`
  motions specifically — a section can freeze/hold, briefly release forward, then fold
  back to its resting state without a fourth clip.
- Sections without `beats` are unaffected — this is purely additive; the single-`motion`
  pipeline above still works exactly as documented.

### 4. Handle render results
- `completed` → download `results.rawUrl` with `curl`.
- `nsfw` or `failed` → **refunded, retry once**. Moderation false-flags abstract "floating
  pills/dissolving figures"; reword to product-context, or switch that clip to
  **`grok_video_v15`** (`resolution:"720p"`, more lenient).
- Tell the user about any retry; never claim a clip rendered if it didn't.

### If the retry also fails (STOP — do not self-reroute)
If the one retry above still produces no usable clip — or video generation isn't
available at all for this section — this section CANNOT be built as video-scroll-effect.
Do not quietly build it as `3d-scene-effect`'s `image-plane` fallback yourself and move
on as if nothing changed: that fallback decision belongs to `site-planner`'s
routing rules, and silently making it here is exactly the failure mode that shipped a
site with zero video sections despite an approved plan promising two (see
`site-planner/SKILL.md`'s "Disclosing plan deviations"). Instead:
- Stop generating for this section. Report upward, to whichever skill/orchestrator is
  running this build, that this section needs `site-planner`'s image-plane
  fallback instead — with the reason (nsfw after retry, API failure, no Higgsfield
  video access, etc.) and whether any credits were spent on the failed attempt(s).
- This report becomes one entry in the final "⚠️ Plan deviations" section the director
  is required to show the user — never only a code comment or a footnote buried in a
  longer summary.

### 5. Slice + compress frames (ffmpeg)
- Single-motion section: `scripts/extract-frames.sh <clip.mp4> frames/<section-name> 180`
  → ~179 numbered JPGs, then `scripts/compress-frames.sh frames/<section-name> 1600 88`
  → 1600px wide, q88 (crisp, <~15MB/section).
- Multi-beat section: run both scripts once per beat, into
  `frames/<section-name>/<beat-name>/` — each beat gets its own frame count and its own
  compress pass, same 1600px/q88 settings.

### 6. Build this section from templates/
- **Project scaffold (once per site, whichever skill runs FIRST):** copy
  `${CLAUDE_PLUGIN_ROOT}/skills/shared-scroll-engine/templates/index.html`,
  `${CLAUDE_PLUGIN_ROOT}/skills/shared-scroll-engine/templates/base.css` (as the project's `styles.css`),
  and `${CLAUDE_PLUGIN_ROOT}/skills/shared-scroll-engine/templates/choreography.js` into the project.
  There is no per-skill `index.html` any more — the shell is shared so a project
  can never end up missing the Three.js / cannon-es / choreography tags just
  because of which technique happened to be built first.
- **This skill's own files (every time this skill runs):** copy
  `templates/video-scroll-effect.js` into the project, and APPEND `templates/styles.css`
  (a fragment, not a full stylesheet) to the project's `styles.css`.
- If the project already has the scaffold, do not overwrite it — subsequent
  sections append into what is already there.
- Add/edit a `SCRUB_SECTIONS` entry for this section. Single-motion sections keep the
  existing shape:
  `{ section:"#<section-id>", frameCount:179, bg:"<palette.bg>", framePath:(i)=>\`frames/<section-name>/frame_${String(i).padStart(4,"0")}.jpg\` }`.
  `frameCount` MUST match the number extract-frames.sh printed, and `section` must match a real id.
- Multi-beat sections use a `beats` array instead of top-level `frameCount`/`framePath`:
  `{ section:"#<section-id>", bg:"<palette.bg>", beats:[{ name:"orbit", frameCount:150, progressStart:0, progressEnd:0.33, loopBack:false, framePath:(i)=>\`frames/<section-name>/orbit/frame_${String(i).padStart(4,"0")}.jpg\` }, ...] }`.
  Each beat's `progressStart`/`progressEnd` carve up the section's 0-1 scroll range
  (beats in list order, ranges should be contiguous and non-overlapping); `loopBack:true`
  plays that beat's own frames there-and-back within its own sub-range, per "Multi-beat
  sections" above.
- Optional live scroll-synced meter/background fields, either shape: `bgFrom`/`bgTo`
  (hex colors — interpolated across the section's scroll progress and applied to its
  background, e.g. for a `descent` motion) — see "Class contract" below for the
  matching `[data-live-count]` markup these pair with.
- **Class contract** the engine depends on (rename these and it silently does nothing):
  - each scrub section: a `<canvas>` inside `.sticky`, wrapped by a `.cinematic` section with the config's id
  - `.reveal-line` + `data-in`/`data-out` — overlay copy fading over a progress window
  - `.progress-fill` and `[data-frame-readout]` — optional, auto-driven per section if present
  - `.reveal` (fades up on enter) and `.stat-num` + `data-count`/`data-suffix` (counts up once on reveal) — anywhere on the page
  - `[data-live-count]` + `data-target`/`data-suffix` — optional, CONTINUOUSLY reflects
    `progress * data-target` as the visitor scrolls (unlike `data-count`, which counts
    up once and then holds) — use for a live depth/altitude/percentage meter tied to
    this section's own scroll progress, only meaningful on sections with a `bgFrom`/`bgTo`
    or otherwise depth/progress-themed motion
- Opacity peaks at the **midpoint** of a line's `[in,out]` window and is 0 at both edges, so give the
  final line a `data-out` past 1.0 (e.g. `1.30`) or it fades to nothing exactly as the user lands.
- Write this section's copy from its `content_brief` — don't reuse generic placeholder copy.
- **Hue-shift trick** for product variants/colorways (no extra generation):
  `ffmpeg -i base.png -vf "hue=h=120:s=1.15" variant.png`.
- If this is the first section being built for this project (nav bar doesn't
  exist yet in index.html), generate the `.hud-nav` links from the full
  `plan.sections` list's `id`/`nav_label` pairs before proceeding to this
  section's own content.

### 7. Deploy to Cloudflare Pages + write out to connected folder
(unchanged from before — runs once, after all sections from site-planner's plan
have been built into the same project)
- Requires `CLOUDFLARE_API_TOKEN` and `CLOUDFLARE_ACCOUNT_ID` set as environment variables
  (never ask the user to paste these into chat; read them from the environment only).
- Load credentials first: `set -a && source .env && set +a` (run this from the repo root,
  before the wrangler command, so CLOUDFLARE_API_TOKEN and CLOUDFLARE_ACCOUNT_ID are in scope).
- Deploy with Wrangler (installs on first use, no separate setup step):
  `npx wrangler pages deploy <project-dir> --project-name=<slug> --branch=main`
  - `<project-dir>` is the folder containing `index.html`, `styles.css`, `choreography.js`,
    every engine `.js` file the plan uses, and the `frames/` folder.
  - `<slug>` is a kebab-case name derived from the brief/brand (e.g. `acme-launch`). If the
    project doesn't exist yet, Wrangler creates it automatically on first deploy.
  - Wrangler prints the live URL on success, in the form `https://<slug>.pages.dev`
    (and a unique preview URL per deployment).
- If the deploy command fails (auth error, network error, or the Cloudflare API being
  unreachable from this sandbox): tell the user plainly that deploy failed and why, and fall
  back to step 7b below — do not claim a URL exists if it doesn't.
- Confirm the live URL actually loads (`curl -sS -o /dev/null -w '%{http_code}' <url>` should
  return 200) before telling the user it's ready.
- Before telling the user the site is ready, read `build-reviewer`'s `plan_deviations`
  field (if any) and include it verbatim under a `⚠️ Plan deviations` heading in the
  final message, per `site-planner/SKILL.md`'s "Disclosing plan deviations" —
  never omit or soften what the reviewer flagged, even when the deploy itself succeeded.

### 7b. Write out to the connected folder (always, regardless of deploy success)
- Copy the entire project folder (site files + `frames/`) into the user's connected
  folder, under a subfolder named after the project slug, together with a `DESIGN.md`.
- `DESIGN.md` is REQUIRED, not optional, and must contain at minimum:
  - A summary of the design choices made (palette, section list, techniques used).
  - A **"Plan vs. build" table**: one row per section, its planned `technique`, its
    actual built technique, and a note if they differ (blank/"—" if they match). This
    is the durable, offline record of any deviation — build-reviewer hard-fails if
    this file is missing or empty, so don't skip it even under time pressure.
- This step runs every time — even if step 7's deploy failed — since it's the only guarantee
  the user's work survives after this session ends (the sandbox is disposable).
- Tell the user both: the live URL (if deploy succeeded) and the local folder path where the
  source now lives.

## Engine rules (already in templates/video-scroll-effect.js)
- Preload every frame; paint frame 0 on first load; redraw only when the frame index changes.
- Sticky stage: outer section `height: 420–600vh`, inner `position:sticky; top:0; height:100vh`.
  Progress = `clamp(-rect.top / (rect.height - innerH), 0, 1)`. Throttle in the rAF loop.
- Cover-fit draw + HiDPI (`devicePixelRatio`, cap 2). Drive updates from the Lenis rAF loop
  (robust to any scroll source). Overlay copy fades over per-line `[in,out]` progress windows.
- Multi-section: `SCRUB_SECTIONS` array; engine **skips** sections whose element is missing.

## Known gotchas
- More/larger frames = slow load → keep 1600px / q88 / ~180 frames (per beat, for
  multi-beat sections).
- Continuous-motion clips only (no hard cuts — ugly when scrubbed backward). This
  matters even more for `loopBack` beats, since the reverse half depends on the clip
  reading correctly played backward.
- `beats`' `progressStart`/`progressEnd` ranges must be contiguous and cover the full
  0-1 range between them — a gap leaves a dead zone where nothing updates, an overlap
  makes two beats fight over the same scroll range.
- A `bgFrom`/`bgTo` pair with no actual color difference, or a `[data-live-count]` with
  no `data-target`, is a silent no-op — confirm both are set meaningfully when used.
- The headless screenshot tool blanks sticky-canvas sections when scrolled; verify with
  pixel sampling, and view live in a real browser.
- In a backgrounded/headless pane `requestAnimationFrame` and `IntersectionObserver` are
  suspended entirely, so the scrub never advances and `.reveal` never fires — this is the
  harness, not the site. Verify by driving the engine yourself:
  `window.__scrubs.forEach(s => s.update())` after a `scrollTo`, then sample canvas pixels.
- The image-0 onload handler must NOT be set separately from the loop's onload/onerror
  handler — combine both behaviors in one handler (increment loadedCount AND draw frame 0
  via an `if (i === 0)` check) or the preloader will hang at (N-1)/N forever.
- Deploy failures should never be silently swallowed — always tell the user if Cloudflare
  deploy failed and confirm whether the write-out to their folder still succeeded.

## Files
- `templates/video-scroll-effect.js` — the scrub engine.
- `templates/styles.css` — `.cinematic` + preloader CSS fragment, appended to the project's
  `styles.css` on top of `shared-scroll-engine/templates/base.css`.
- The project shell (`index.html`, `base.css`, `choreography.js`) lives in
  `shared-scroll-engine/templates/` — see "Build this section from templates/" above.
- `templates/CinematicReveal.tsx` — LEGACY React/Next drop-in (optional). Single-motion
  only: it does NOT support `beats`, `loopBack`, `bgFrom`/`bgTo` or `[data-live-count]`.
  Don't reach for it when a section uses any of those — use the vanilla engine, which is
  the maintained one.
- `templates/Launch Demo.command` — double-click localhost launcher.
- `scripts/extract-frames.sh`, `scripts/compress-frames.sh` — the ffmpeg pipeline.