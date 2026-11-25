---
name: superforge-scroll
description: >
  Build a scroll-scrubbed cinematic landing page where scroll drives a camera
  continuously through a generated world, with no cuts between scenes. Plans the
  camera before generating anything — floor plan or world map, room adjacency,
  a shot list with camera position, heading, lens and eye height per leg, a seam
  contract, and sun-derived light continuity — then renders through whichever
  video backend the user actually has (Kie.ai, Higgsfield, Monid, fal, Replicate,
  a vendor API, or an MCP tool) behind one capability contract and a mandatory
  frame-lock probe, and wires a portable vanilla-JS scrub engine. Use when the
  user says "cinematic scrolling", "scroll animation", "fly through", "3D world
  landing page", "diorama site", "Apple-style scroll", "walkthrough video",
  "scrollytelling", "シネマティックスクロール", "スクロール演出", "スクロールで動く
  サイト", "世界を飛び回る", "建築のウォークスルー", "間取りから動画", "カメラワーク",
  or runs /superforge-scroll.
license: MIT
metadata:
  author: Takao Umehara
  version: "1.0"
  derived-from: "scroll-world by cyw (github.com/oso95/scroll-world), MIT"
compatibility: >
  Standalone. Reads docs/brand.md when present for palette, tone, and art
  direction; writes docs/scroll-world.md.
  Needs ffmpeg/ffprobe and one qualified video-generation backend — reached by
  CLI, REST, or MCP. No backend is assumed and none is required to be installed
  before the interview.
---

# Superforge Scroll — Cinematic Scroll-Scrubbed Worlds

A landing page where **scroll drives a camera**. It flies through a space — into a
building, along a route, across a miniature world — continuously, with no visible cuts.
The visuals are pre-rendered AI video; the page just scrubs them by scroll position. This
is the technique behind Apple's scroll-through product pages: the camera genuinely moved,
scroll only drives time.

**What gets produced:** a camera plan → N scene stills → N legs → (architecture B only)
N−1 connectors → a self-contained scrub engine that plays the chain as one flight.

Three things distinguish a build that works from one that merely renders:

1. **The camera is planned before any pixel exists.** The still is not a picture of the
   scene, it is the camera's frame 0. Skip the plan and you are asking a model to invent
   routes between six unrelated viewpoints. → §2, `references/planning.md`
2. **Seams must be frame-identical.** Every chained clip starts from the *actual rendered
   last frame* of the previous one, never from a fresh render of the same subject. → §6
3. **The backend must be probed, not trusted.** A video API can accept your image, ignore
   your prompt, bill you, and return a frame-locked clip flying the wrong way. → §4,
   `references/providers.md`

The scrub engine is self-contained vanilla JS — it builds its own DOM and injects its own
CSS into a container you give it — so it drops into plain HTML, Next.js, Vue, Rails,
anything. Do not assume a framework. The value here is the plan, the seam method, and the
backend contract, not the frontend.

---

## 1. Interview — ask what you cannot sensibly default

**The subject is the user's to state.** Ask it as an open question in plain prose, never a
fabricated multiple-choice list of industries — a made-up list biases them and reads as
you deciding their business for them. Reserve structured choices for the genuinely
enumerable, lower-stakes decisions, and signal that "other" is available.

1. **Subject** — open question. "What should this world be about? Your business, a
   client's, or any idea — a word or a sentence is fine." Capture the subject, a one-line
   pitch, and a brand name if they have one.
2. **Do they have a plan of the space?** Ask this early and explicitly for anything
   architectural — a floor plan, a site plan, a listing PDF, a CAD export, a sketch. On
   architecture, interior, and real-estate work there almost always is one, and it is the
   single highest-value input available. Read it; don't ask them to describe it.
3. **Brand kit** — from `docs/brand.md` if `superforge-brand` already ran (palette, tone,
   and art direction are decided once in this suite, never twice). Otherwise: import from
   a URL, take it from the user, or propose and get approval. Capture 4–6 named hexes, a
   display name, a tone word or two.
4. **Art direction** — default "soft matte low-poly clay diorama, isometric, tilt-shift
   miniature, warm light." Alternatives: flat papercraft, glossy toy, claymation, neon
   night, photoreal architectural. Whatever is chosen becomes the **style preamble**
   reused byte-for-byte in every prompt. That identical text is what makes the world
   cohere.
5. **Camera feel** — ask, but ask it *after* §2 has classified the space, because the
   space rules some answers out (`planning.md` §1). Fly-through / one continuous
   walkthrough / locked isometric glide, each with its one-line trade-off.
6. **The journey** — 5–7 ordered scenes derived from the subject's own value chain or the
   building's own circulation. Each needs a subject description, eyebrow, headline, one
   line of body, 0–3 tag pills. Under four scenes there is no journey; over eight the
   visitor stops scrolling before the payoff.
7. **Mobile — always ask, never silently generate both.** The mobile version is a second
   camera chain rendered natively in 9:16, composed for phones rather than cropped from
   the landscape film, and it roughly **doubles the render spend** — state the number, not
   just the fact. "Desktop only" / "Desktop + mobile (native 9:16, ~2× cost)". A crop of
   the 16:9 film is a labelled stopgap the user must approve, never the default answer.
   The engine's phone hardening is always on regardless; that is not a mobile version,
   that is the page not breaking when a phone visits.
8. **Backend and budget** — §4. Decided before anything renders.

---

## 2. Plan the camera — the gate everything else waits behind

**Read `references/planning.md` and produce `docs/scroll-world.md` before generating
anything.** Copy `assets/templates/scroll-world.md` as the starting point.

The plan classifies the space (bounded interior → floor plan; continuous terrain → route
map; archipelago → island layout), which in turn decides which camera architecture is
even coherent. Then it fixes the four invariants — eye height, lens, sun azimuth, speed —
and produces two tables that the rest of the build consumes directly:

- **the shot list**, one row per leg: camera position and heading at start and end, the
  move, the focal point, the aperture it exits through, and the light clause *derived*
  from `sun_azimuth − heading` rather than chosen;
- **the seam contract**, one row per seam: what the outgoing frame must show, what the
  incoming frame must show, and the two shared anchors that carry across.

Render the plan and let the render check itself:

```bash
python3 scripts/plan_map.py docs/scroll-world.md      # -> docs/scroll-world.svg
python3 scripts/plan_map.py --lang ja                 # chrome in ja/ko/zh-CN/es; default en
```

Room footprints, apertures, the numbered camera path with a heading tick per leg, north,
the sun, a scale bar — and two of §8's checks run mechanically on the way past, because
`pos end == pos start` and Δheading are arithmetic on numbers already in the tables. It
exits non-zero on a failure and draws the map anyway; a picture of the broken plan is what
you want while fixing it. **Show the user this SVG** — it is the artifact they can approve
or reject in ten seconds, which is the whole point of gate 1.

Then walk the story order along the adjacency graph and confirm the camera can physically
make every move. When the story and the geometry disagree — and they will — reorder,
insert a transit leg, split a room in two, or declare an exception seam with a named
device. What you may not do is put the seam there anyway and hope.

Finish on `planning.md` §8's checklist. **Do not spend money until every line is true.**

Approve in three gates, cheapest first: the plan (free) → the stills as a contact sheet
(cheap) → the previz chain at the lowest tier (~⅕ of final) → the final render. Most of
the money wasted in a bad build is spent by someone who skipped the free gate.

---

## 3. Bootstrap the tools

- **ffmpeg / ffprobe** on `$PATH` — frame extraction and encoding. Genuinely required.
- **One qualified video backend** — §4. Nothing needs to be pre-installed before the
  interview; detection happens here.
- **An image generator** for the stills — the backend's own, a local `generate_image`
  tool, or any model that takes a prompt and returns a PNG. One source for all N stills
  of a build: two generators render with different character, and mixing them reads as
  style drift for the same reason the video chain uses one model.
- **Optional:** PIL / `cwebp` for background knockout if you want floating scenes (§7).
- **Caveats.** macOS ships bash 3.2 — no associative arrays in scripts. Generations take
  minutes each, so run them detached and poll; never a foreground blocking call. Keep
  every array-driven chain step in a `#!/bin/bash` script run as `bash script.sh` — zsh
  arrays are 1-indexed and an inline loop in an interactive macOS shell will hand the
  wrong frames to the wrong connector.

---

## 4. Choose and qualify the backend

**Read `references/providers.md`.** The short version:

The pipeline does not care who renders the clips. It cares that the backend can **start a
clip from a supplied frame** (C1), **still obey the prompt while doing so** (C3), and —
for architecture B connectors — **land on a supplied end frame** (C2). That is the
contract. Everything reduces to two shell functions, `vg_leg` and `vg_conn`.

**Detect, then ask.** Never silently pick a backend that spends the user's money.

| Available | Offer it as |
|---|---|
| `KIE_API_KEY` set | the default — one key, many model families |
| a video-generation MCP tool connected | preferred when present: no key handling at all |
| `higgsfield` CLI authenticated | good if they already pay for the plan |
| `monid` CLI with balance | pay-per-clip, no monthly commitment |
| fal / Replicate / a vendor key | when they want a specific model, or already have the contract |
| none of the above | the generic HTTP adapter (`providers.md` §5) plus whatever they have |

Then **run the probe** — three cheap clips at the lowest resolution, well under a dollar
against a chain that costs tens (`providers.md` §4). Probe 2 is the one nobody runs and
the one that matters: same image, two opposite prompts, confirm the outputs diverge. A
backend that silently drops the prompt returns a perfect-looking frame-locked clip going
the wrong direction, and every log says success.

Record the probe result and date in `docs/scroll-world.md`. Then state the estimated
total — `N stills + (2N−1) clips (×2 if mobile) + ~15% re-roll headroom` at the probed
per-clip price — and get a go before generating.

One model for the whole chain. Mixing renderers mid-chain keeps position continuity but
the motion/colour/grain shift reads as a subtle pop; the only sanctioned exception is
rescuing a single clip a content filter keeps rejecting.

---

## 5. Generate the scene stills

One image per scene, all sharing the byte-identical style preamble, **each carrying its
camera pose from the shot list**. A still generated without a stated camera pose is a
still generated from a pose the model invented — which is the failure §2 exists to
prevent.

```
[STYLE PREAMBLE — identical every time]
Camera: [LENS]mm equivalent, [Z]m above the floor, at [POS] facing [HEADING as prose],
level horizon, no tilt.
Light: [TIME OF DAY], [clause derived from sun_azimuth − heading].
Subject: [what is in THIS scene].
No text, no letters, no logos. [ASPECT].
```

Full templates in `references/prompts.md`; batch script in `references/pipeline.md`.

- Run all N concurrently and detached. Re-roll individual transient failures rather than
  restarting the batch.
- **Review before continuing — this is gate 2.** Lay the stills out in path order and ask
  whether a person could walk from each one into the next. If you can't, the model can't
  either. Regenerate anything off-style, optionally passing an approved scene as a style
  reference.
- Solid-background stills are what feed the video model; keep them. They double as video
  posters and lazy-load fallbacks.

---

## 6. Render the chain — the seam law

Two architectures. The plan already chose (`planning.md` §1); this step implements the
choice and never re-decides it.

### A) Continuous forward take — interiors, terrain, anything grounded

One camera that only ever glides forward, first scene to last. Legs render
**sequentially**: leg 0 from scene 0's still; every subsequent leg's start image is the
**previous leg's actual last frame**, extracted with ffmpeg. **No end image** — an end
image of a wide establishing shot forces the camera to pull back, which is the single
biggest cause of seam stutter. There are no connectors; the legs *are* the journey. Wire
each leg with `connectors: []` and a small crossfade.

Cost: strictly sequential, so slower and unparallelisable. Interiors trip content filters
often — budget three attempts per leg.

"Forward only" is the **seam** rule, not the **leg** rule. Inside a single leg the camera
is free: orbits, crane-ups, lateral tracking, a push-in that eases back out are all safe,
because one leg is one continuous render with no seam to break. Reversals are fatal only
*across* seams. So give each leg an expressive move from the plan's shot list, under the
**motion handoff contract**: every leg ends by settling into a slow steady forward drift
toward the named exit aperture in its final second, and every leg begins by continuing
that same drift. Keep both clauses verbatim.

**Eyeball each leg's last frame before chaining the next.** It should read as a frame from
a calm forward glide, through or approaching the aperture the shot list names, with both
seam anchors visible. If it doesn't, re-roll now — a bad handoff frame poisons every leg
after it.

### B) Dive-in plus aerial connector — diorama and miniature only

A dive into each scene, then a connector that pulls up and out and flies over to the next.
The pull-out **reverses camera direction at every seam**. In a miniature world that reads
as "zoom out to the map, fly to the next island"; in a grounded walkthrough it reads as a
rewind. Use B only for the map-like aesthetic.

Connectors are where B lives or dies, and the law is absolute:

```
start-image = the LAST frame extracted from leg i's RENDERED video
end-image   = the FIRST frame extracted from leg i+1's RENDERED video
```

**Never the original still.** Every generation renders slightly differently, so a
connector that ends on a fresh render of "the kitchen" will not match the next dive's own
render of that same kitchen, and you get a pop. Hand off the exact pixels:

```bash
ffmpeg -sseof -0.15 -i leg_i.mp4     -frames:v 1 -q:v 2 leg_i_last.png
ffmpeg -ss 0      -i leg_next.mp4    -frames:v 1 -q:v 2 leg_next_first.png
```

Now `leg_i.end == connector.start` and `connector.end == leg_{i+1}.start`. Models land
*close* to an end image but not always pixel-perfect, so the engine also applies a short
crossfade at each seam. Frame-matched endpoints plus a small crossfade means no visible
cut — but never skip the frame handoff and rely on the crossfade alone. A crossfade hides
drift; it cannot hide a content jump.

---

## 7. Optional — float the scenes

To sit dioramas over an atmospheric background rather than in a solid box, knock the flat
background out to transparency with `references/knockout.py` (border-connected flood fill,
so interior colour matching the background survives) and encode to webp. Simpler
alternative: make the page background the same colour as the scene background and skip
this entirely. Photoreal directions skip it always — those scenes are full-bleed.

---

## 8. Encode for scrubbing

Scrubbing means setting `video.currentTime` from scroll — when you ship video at all.
Several things matter here and every one of them is routinely gotten wrong.

**There is a second delivery format, and on a short hero it is the better one: a numbered
image sequence drawn to a canvas.** Frames decode from memory, so seek cost is not small
but structurally absent — no keyframe distance, no GOP, no `seekable`, no byte-range, no
iOS priming, no blob. The cost is bytes: on one measured build, 141 frames at 1440px WebP
q71 came to 5.9 MB against 2.7 MB for the same clip as mp4, ~2×. Pay it with progressive
loading — fetch frame 0 at high priority, paint it immediately, stream the rest at ~8
concurrent, and draw the nearest loaded frame in the meantime, so the hero is interactive
long before the sequence finishes.

Rule of thumb: **under ~200 frames, ship frames; over that, ship mp4** and do the
verification below. A 4-leg chain at 8s each is ~770 frames and belongs on mp4.

**Seekability, not keyframe density, is what makes scrubbing work.** Many static hosts —
including `python -m http.server` — don't serve HTTP byte-range requests, which pins
`video.seekable` to `[0,0]` and clamps every seek to frame 0. The video looks frozen. The
robust fix is fetching each clip as a **Blob** and playing it from an in-memory object
URL; blobs are always fully seekable. The engine does this, which is why you do *not* need
all-intra video.

**Don't shrink quality to buy smooth seeks.** Native resolution, `crf ~20`, and a small
GOP rather than all-intra — all-intra bloats an 8s clip to ~25 MB, `-g 8` is ~8 MB and
scrubs fine via blob.

**Grade before you encode, not in CSS.** Generative video comes back with wildly
inconsistent exposure, and a night or interior scene routinely lands unusably dark. Fix it
once at the encode, where it costs nothing at runtime. Prefer a curve that holds the black
point over a gamma lift — gamma raises the floor too and the result goes milky, which on a
dusk exterior blows the sky at the same time it lifts the shadows:

```
-vf "curves=master='0/0 0.08/0.30 0.30/0.60 0.65/0.86 1/1',eq=saturation=1.10"
```

Measured on one build's night clip: mean YAVG 34.4 → 62.1 over the whole clip, 15.5 → 49.2
over the last third, with the black point unmoved.

```bash
ffmpeg -i src.mp4 -an -vf "unsharp=5:5:0.8:5:5:0.0" \
  -c:v libx264 -preset slow -crf 20 -pix_fmt yuv420p \
  -g 8 -keyint_min 8 -sc_threshold 0 -movflags +faststart out.mp4
```

Same settings for every clip, for uniform quality.

**Verify the encode instead of trusting the flag.** A clip that skipped this step looks
identical in a player and scrubs three to ten times slower. Measured on one build: a hero
that shipped with **one keyframe for 141 frames** and no faststart seeked at p50 30.2 ms /
p90 51.4 ms, against 6.2 / 8.2 ms for a correctly encoded sibling. A 30 ms median seek caps
the footage at ~33 fps while the page composites at 120 — the page is smooth and the film
is not, and the eye reads the film.

```bash
ffprobe -v error -select_streams v:0 -show_entries frame=key_frame \
  -of csv=p=0 clip.mp4 | grep -c '^1'      # want frames/8, not 1
python3 -c "import sys;d=open(sys.argv[1],'rb').read(64);\
  print('faststart' if d[4:8]==b'ftyp' and b'moov' in d else 'CHECK')" clip.mp4
```

And measure the thing that actually matters, in a real browser: 40 pseudo-random seeks,
report p50/p90/max. Over ~15 ms at p90 and the footage cannot keep up with the page.

**Mobile encodes only if the user opted in at §1.7:** the native 9:16 chain encoded 720
wide, `-g 4` (twice the keyframes ≈ half the seek-decode work — phone seek cost scales
with GOP length), crf 23, wired as `clipMobile` / `connectorsMobile`, with each portrait
leg's first frame as the `stillMobile` poster. `pipeline.md` §6b.

---

## 9. Assemble the page

Copy `references/scrub-engine.js` into the project — and `references/index-template.html`
for a fully standalone page. Config-driven and self-contained:

```js
mountScrollWorld(document.getElementById('world'), {
  brand: { name: 'Pearl & Co.' },
  diveScroll: 1.3, connScroll: 0.9,        // viewport-heights of scroll per clip
  sections: [
    { id:'farm', label:'The Farms', still:'assets/farm.webp',
      clip:'assets/vid/farm.mp4',
      clipMobile:'assets/vid/farm-m.mp4',   // mobile opt-in only: native 9:16
      stillMobile:'assets/farm-m.webp',     // its first frame as the portrait poster
      scroll: 1.6, linger: 0.45,            // pacing: longer dwell, camera settles mid-scene
      accent:'#8FB98A', eyebrow:'From leaf to last sip', title:'It starts in the hills.',
      body:'…', tags:['Single-origin','Hand-picked'] },
  ],
  connectors:       ['assets/vid/conn1.mp4', /* … length = sections − 1 */],
  connectorsMobile: ['assets/vid/conn1-m.mp4' /* … same length; mobile opt-in only */],
});
```

The engine handles the ordered chain, scroll→`currentTime` with rAF smoothing, blob
loading, lazy prefetch of nearby clips, seam crossfades, pinned per-section copy, a route
rail, `prefers-reduced-motion`, and phone hardening. Theme it with CSS variables
(`--accent`, `--sw-bg`, `--sw-ink`); the visual identity comes from the clips, so the
chrome stays quiet.

**Pacing.** Per-section `scroll` overrides the default dwell. `linger` (0–1, keep ≤ 0.6)
remaps time within each beat:

```
v(u)  = u + k·sin(2πu)/(2π)        v(0) = 0,  v(1) = 1
v'(u) = 1 + k·cos(2πu)             v'(0.5) = 1 − k,  v'(0) = v'(1) = 1 + k
```

At k = 0.5 the camera runs at half speed exactly where the headline is legible and 1.5×
across the boundary. Beat boundaries are **fixed points**, so the remap can never shift
which beat the visitor is reading — that property is the reason to use this shape rather
than an ease.

Two traps worth a test each: do not clamp the input into the last beat
(`min(beats − ε, p·beats)` returns 0.9999999985 at p = 1 and the final frame is never
drawn), and clamp `k < 1` (at k = 1 the derivative reaches 0 and the film stalls dead
mid-beat).

Give the hero and finale a higher `scroll` plus some `linger`; keep transit scenes brisk.
Prefer expressive motion in the *clip* and restraint in the *scrub mapping*; they compound.

**Never unmount the pinned copy.** Swapping beats with `if (!active) return null` destroys
whatever the visitor had focused: tab to the hero CTA, scroll, and focus falls to `<body>`
— a keyboard user is returned to the top of the tab order by the act of scrolling. Keep
every beat mounted, cross-fade `opacity`, and mark the inactive ones `inert` +
`aria-hidden` so exactly one is in the reading order. Better still, lift the CTA out of the
beats entirely — one button that never moves and never remounts, rather than one per beat.
`scrub-engine.js` handles its own copy layer correctly; this applies the moment you write
your own, which most builds do.

**On phones the engine adapts automatically** (coarse pointer or ≤860px): serves the
mobile encodes when present, **coalesces seeks** so a fast flick can't queue a new
`currentTime` mid-seek and freeze the clip, keeps the still as a poster until the clip
paints its first frame, primes each video on first touch (fixes iOS's blank-until-played
video), drops the drifting particles, ignores URL-bar-only resizes, and respects safe-area
insets. All on by default.

And remember scroll is a scrubber — visitors scroll **up**, so every move also plays in
reverse. That's free, and it's another reason seam velocity must be consistent in both
directions.

---

## 10. QA — verify the seams, don't eyeball the page

- **First, prove the pin pins.** At 0/25/50/75/100% of the section, assert the pinned
  element's `getBoundingClientRect()` has `top <= 1` and `bottom >= innerHeight - 1` —
  whether it pins with `position: fixed` as `scrub-engine.js` does, or with
  `position: sticky` as a hand-written copy layer usually does. Reading
  the video or canvas proves it *painted*, not that anyone can *see* it — a released pin
  scrolls the hero off screen while every other check in this section still passes. Then
  walk the pin's ancestors and fail on any with a computed `overflow-y` other than
  `visible`, or a `transform` / `filter` / `contain` that creates a containing block.
- **Measure the exposure, do not eyeball it on your own monitor.** At each of the same five
  positions, mean luminance of the decoded frame must clear ~12% of white. Below that the
  hero reads as an empty black box to everyone not sitting in a dark room, and it will
  still pass every seam check because both sides of the seam are equally dark.

  ```bash
  ffprobe -v error -f lavfi -i "movie=clip.mp4,signalstats" \
    -show_entries frame_tags=lavfi.signalstats.YAVG -of csv=p=0 \
    | awk '{s+=$1;n++} END {printf "mean YAVG %.1f (%.0f%% of white)\n", s/n, s/n/255*100}'
  ```

- **Screenshot just before and just after each seam.** The two frames must be
  near-identical. Judge by **composition, not raw PSNR** — a correctly frame-locked seam
  can read 18–25 dB from detail shimmer alone. A real mismatch shows as different
  composition or props, not as softness. If they pop, you used a still instead of a
  rendered frame (§6), or the crossfade band is too short.
  **Screenshots lie about media.** Headless Chrome does not composite `<video>` into a CDP
  screenshot — you get a black rectangle from a perfectly good clip. Run headful, or skip
  the screenshot and read the pixels in-page with `ctx.drawImage(videoOrCanvas, …)` +
  `getImageData`. And `page.screenshot({clip})` is **document**-relative: after scrolling,
  `{x:0,y:0}` is the top of the page, not the top of the viewport. Use
  `captureBeyondViewport: false` and no clip.
- **Check the plan, not just the pixels.** At each seam, are the two anchors from the seam
  contract visible on both sides? Did the heading hold? Is the light still coming from the
  same side of the world? These are the failures that survive a clean PSNR.
- Console clear, `video.seekable.end(0) > 0` (blob working), `currentTime` tracking scroll
  across each clip's band.
- **Focus survives a scroll.** Focus the hero CTA, scroll past it, assert the element is
  still in the DOM and still `document.activeElement`.
- **A canvas is a blank rectangle to a screen reader.** `role="img"` plus an `aria-label`
  that describes the journey, and the beat copy in real DOM text — never baked into the
  frames.
- **Mobile.** Fail the build outright if the plan's `Mobile:` line still reads
  `not asked` — §1.7 is a question with an answer, and an unanswered one is a defect, not a
  default. Desktop-only build: sanity-check one phone viewport — loads, posters show,
  nothing overlaps. Opted-in mobile build: emulate a phone with CPU throttled 4–6× and
  scroll fast (should track without freezing); confirm the first scene shows immediately
  and the video takes over on scroll with no black flash (test iOS Safari specifically);
  verify in the Network panel that the `-m.mp4` variants are served on mobile and are
  **natively portrait** (`videoWidth < videoHeight`, not a downscaled 16:9 file); collapse
  the URL bar slowly and confirm the page does not jump; rotate and confirm clean
  recomposition.
- Reduced-motion falls back to the stills — no video, no particles.
- Run `/superforge-verify` before calling it done. "The build finished" is not "the seams
  hold."

---

## Gotchas

**Planning**

- **Seams technically perfect, building impossible** → stills were generated before the
  camera path. The frames hand off pixel-for-pixel while the geometry contradicts itself.
  No encoding fix exists; redo §2.
- **The camera teleports between two scenes** → the story order doesn't follow the
  adjacency graph. Reorder, insert a transit leg, split a room, or declare an exception
  seam with a device (`planning.md` §2d).
- **"Same building" that doesn't feel like one** → the sun moved. Light direction must be
  derived from a fixed azimuth minus the current heading, not chosen per scene
  (`planning.md` §4).
- **A cut the audience feels but can't name** → the lens or the eye height changed at a
  seam. Both are film-wide invariants; ramp inside a leg, never across a seam.

**Backend**

- **A perfect clip going the wrong way** → the backend dropped the prompt while accepting
  the image (or vice versa). This bills normally and logs as success. Probe 2 in
  `providers.md` §4 is the only thing that catches it.
- **The end frame is mandatory** → that model can't render architecture-A legs, which
  require no end image. Connector-only; pick another model for the legs or switch
  architecture.
- **Wrong aspect ratio** → many APIs let the output ratio follow the input image instead
  of your request. Pass the ratio explicitly on every clip and verify with ffprobe.
- **Result URL 404s an hour later** → they expire. Download inside the render function,
  immediately, before doing anything else.
- **Content filter false-positives** → interiors trip them constantly, especially bedroom,
  pool, and spa contexts, plus words like "bed", "pool", "wine", "swim". Fixes in order:
  re-roll (often non-deterministic); strip trigger words and add "empty, unoccupied, no
  people, architectural, tasteful"; regenerate that one clip on a different model with the
  same frames, accepting a slight character shift; or for architecture B, set the
  connector slot to `null` and let the engine crossfade that seam directly.
- **Seam pop only where you saved money** → you swapped models mid-chain, or used a
  start-only model where a connector needs an end image.

**Page**

- **The hero scrolls away instead of pinning** → an ancestor is a scroll container.
  `overflow-x: hidden` is the usual culprit: it is invalid beside a visible `overflow-y`,
  so the computed value becomes `hidden auto` and every descendant `position: sticky`
  silently dies. Use `overflow-x: clip`, which clips identically and creates no scrollport.
  `transform`, `filter`, `backdrop-filter`, `contain` and `will-change` on an ancestor do
  the same thing by a different mechanism.
- **Frozen video / stuck at frame 0** → `seekable=[0,0]`; the host isn't serving byte
  ranges. Blob URLs fix it; the engine already does.
- **Huge files** → all-intra. Use `-g 8` plus blob.
- **Soft or muddy** → you downscaled or over-compressed. Encode native, `crf ≤ 20`, add
  `unsharp`. Video is inherently softer than the stills; keep the stills as the fallback.
- **Blank/black scene on iOS when desktop was fine** → iOS Safari won't paint a seeked
  frame on a muted video that never played. The engine keeps the still as a poster until
  the clip paints and primes on first touch — don't hide the still on `loadedmetadata` or
  strip `playsinline`/`muted` if you port it.
- **Page jumps while scrolling on mobile** → something re-runs layout on the URL-bar
  resize. Gate resize handlers on a width change; keep the `orientationchange` path.
- **Copy behind the notch** → use the engine's safe-area offset and make sure the viewport
  meta has `viewport-fit=cover`.
- **Portrait shows only the middle of the scene** → a 16:9 clip on a tall phone. That's
  why the mobile version is the native 9:16 chain, never the crop.
- **Dark theme fights the engine** → it wraps its defaults in `@layer sw`, so a page-level
  `:root` / `.sw-root` block with `--sw-bg`, `--sw-ink`, `--sw-accent` wins cleanly.
- **Connector grabbed the wrong scene's frames** → the array loop ran in zsh, where arrays
  are 1-indexed. `#!/bin/bash`, run as `bash script.sh`.

---

## References

- `references/planning.md` — **read first.** World-type classification, floor plan and
  route map, camera invariants, the shot list, the seam contract, light continuity, the
  three approval gates, and the pre-spend validation checklist.
- `scripts/plan_map.py` — renders the plan's tables to an SVG floor plan with the camera
  path on it, and machine-checks position and heading continuity. Stdlib only; `--lang`
  for chrome labels (en default, plus ja / ko / zh-CN / es).
- `references/providers.md` — the backend capability contract, the adapter interface, the
  registry (Kie.ai, Higgsfield, Monid, fal, Replicate, vendor APIs, MCP, generic HTTP),
  the mandatory qualification probe, frame hosting, and key handling.
- `references/prompts.md` — style preamble, and every prompt template with the camera and
  light slots the plan fills.
- `references/pipeline.md` — copy-paste batch scripts, backend-agnostic, bash-3.2-safe.
- `references/scrub-engine.js` — the portable config-driven scrub engine.
- `references/index-template.html` — minimal standalone page that mounts the engine.
- `references/knockout.py` — border-connected background knockout for floating scenes.
- `assets/templates/scroll-world.md` — the plan template to copy into `docs/`.

---

## Attribution

Derived from **[scroll-world](https://github.com/oso95/scroll-world)** by cyw, MIT
licensed. The scrub engine, the knockout script, the page template, and the seam-handoff
method are that project's work, carried over with its licence intact — the engine and
knockout files are unmodified.

What this version adds: the pre-production planning layer (`planning.md`, and the gate in
§2), the backend abstraction that replaces the hardcoded vendor with a capability contract
and a probe (`providers.md`), camera-pose-driven still prompts, and integration into the
superforge suite.
