---
name: html2video
description: Turn a web article URL into a polished 1920x1080 edited video (MP4) — code-driven editing with Remotion, not AI video generation. Use this whenever the user wants an article, blog post, research page or changelog made into a video, or says 文章转视频, 网页转视频, 把这篇做成视频, article-to-video, url-to-video, or asks for an explainer or montage cut of written content. It harvests the page's real structure, full-resolution figures and design tokens, mines the content for what matters (including the caveats most tools skip), commits to a reviewable storyboard.json, then renders through a hardened Chinese-typography shot library. Has a 口播 (spoken) mode — ask for 口播, 配音稿, a narration script or voice-over and it re-times the cut to speech and writes a recordable script with timecodes. Also use it to re-render or retune an existing storyboard.json, adjust crops or pacing, or pull stills.
metadata:
  version: 1.0.0
---

# html2video

Produce a 1920x1080 H.264 video from a web article. Chinese output by default;
English sources get translated during the reading stage.

The hard part is not rendering. It is deciding what deserves to be on screen —
and the thing that separates this from a slideshow is treating a page's figures
and figure captions as primary material rather than decoration.

## The pipeline

```
HARVEST ──→ READ ──→ STORYBOARD ──→ RENDER
 scripts     you     storyboard.json   library
```

Four stages, and the middle two are where the quality comes from. HARVEST and
RENDER are deterministic and already written; READ and STORYBOARD are editorial
judgement, which is your job.

| Script | Does |
|---|---|
| `scripts/harvest.py` | URL to structured content, full-resolution figures, design tokens |
| `scripts/render.mjs` | storyboard.json to MP4 (stages assets, subsets fonts, validates, renders) |
| `scripts/build_fonts.mjs` | subsets the CJK faces to this board's characters (called by render.mjs) |
| `scripts/sync.sh` | copies the engine from `assets/template/` into the runtime studio |

All paths below are relative to this skill's directory. The render engine lives
in `assets/template/` and runs from `~/.cache/html2video/studio/`, which is where
`node_modules` is kept so it survives between runs.

## 1. HARVEST

```bash
python3 scripts/harvest.py --url "https://example.com/article" --out ./work/myrun
```

Produces `work/myrun/harvest.json` plus `work/myrun/media/fig-NN.png`.

Read `harvest.json` before doing anything else. Look at, in this order:

1. **`figures[].caption`, and its `captionSource`.** When a page really uses
   `<figcaption>`, each caption is a finding compressed into one sentence with its
   illustration already attached — the densest editorial material available, and
   the shortest path to a good video.

   But check `captionSource` before trusting one. `figcaption` is authoritative;
   `proximity` means the text merely followed the image and **may belong to a
   different figure**; `none` means the page gave nothing. Many sites (Cloudflare's
   blog, for one) wrap images in `<figure>` with no caption at all.

   When it is `proximity` or `none`, **open the image and read the finding off the
   chart** — its own embedded title is usually the best source. Re-author that as a
   Chinese headline, and put the English original in `asset.sourceCaption`.
2. **`figures[].intrinsic`** — how many pixels you have to spend. A figure at
   2688px can be pushed into; one at 1590px cannot fill a 1920 frame at all.
3. **`sections`** — the article's real spine, with nav noise already dropped.
4. **`tokens`** — the site's actual colours and fonts, from a real browser.
   `cssVars` often contains the brand palette by name.

If the fetch looks thin, retry attached to a logged-in Chrome:

```bash
python3 scripts/harvest.py --url URL --out DIR --cdp-url http://localhost:9222
```

## 2. READ

This stage has no script because it is the judgement. Load
[references/editorial.md](references/editorial.md) and work through it. In short:

- state the core message in 40 Chinese characters or fewer
- pick 3 to 5 supporting points and **order them by audience relevance, not by
  where they appear in the article**
- triage everything else: keep / simplify / visualise / omit
- go looking for what the article half-buries — the limitation it admits, the
  number that contradicts expectation, the one example that makes it click.
  These are the moments other tools skip, and they are why a video is worth
  watching rather than skimming.

Write narrative headlines. "26% 的题目它知道自己在被测" beats "评测结果".

## 3. STORYBOARD

Author `work/myrun/storyboard.json`. The schema, every field's meaning, and a
complete worked example are in
[references/storyboard.md](references/storyboard.md). Shot-by-shot composition
and motion specs are in [references/shots.md](references/shots.md).

Three rules that the schema enforces, so it is cheaper to follow them than to
fight them:

- **Never author frames.** Scene length is a dimensionless `weight`; the solver
  converts weights to frames while respecting a reading floor computed from your
  text. Everything time-like inside a scene is normalised `0..1`.
- **Crops are normalised rects in source-image space**, and a crop that would
  need more pixels than the image has is rejected before rendering.
- **Assets are local.** No URLs anywhere; the render never waits on the network.

Then validate, which is much faster than rendering:

```bash
node scripts/render.mjs --storyboard ./work/myrun --still 0
```

The validation report prints resolved scene durations, pixel headroom per asset,
and character budgets. Fix everything it flags before rendering.

## 4. RENDER

```bash
# full video
node scripts/render.mjs --storyboard ./work/myrun --out ./myrun.mp4

# one frame, for checking a layout
node scripts/render.mjs --storyboard ./work/myrun --still 950

# interactive preview
node scripts/render.mjs --storyboard ./work/myrun --studio

# 口播 mode: script only, no render
node scripts/render.mjs --storyboard ./work/myrun --script
```

### 口播 mode

When the user asks for 口播 / a spoken version / a narration script, set
`audio.mode: "voice"` and give **every** scene a `narration` line. That does three
things, and the third is why this is a mode rather than an extra document:

- writes `narration.md` — a recordable script with timecodes, what is on screen at
  each moment, and a per-scene duration budget
- **re-times the cut to speech** rather than to reading speed, so the script and
  the video actually line up
- relaxes the reading floor, since the viewer is listening rather than reading

The video renders **silent** — you record over it. No TTS, no API key.

The single rule that matters: **narration must not read the on-screen text aloud.**
The screen says what it is; the narration says why, so what, and where it came from.
Read [references/narration.md](references/narration.md) before writing any of it —
it also covers trimming on-screen text, spoken syntax, and the `--sps` speech-rate
flag.

`render.mjs` stages assets, wraps props, subsets fonts, validates and renders in
one step. Use it rather than calling `remotion` directly — see the props note in
[references/pitfalls.md](references/pitfalls.md) for why.

**Use `--concurrency 3` or lower** if a render dies with `Visited
"http://localhost:3001/index.html" but got no response`. Measured on this
machine: 8 parallel tabs against the system Chrome fails that way, 3 is stable.
Stills always work because they run a single tab.

## Iterating on the visuals

This is the real work, and there is no automated substitute for looking at frames.

Do not re-render the whole video to check a change. Pull stills at the middle of
the scenes you touched:

```bash
node scripts/render.mjs --storyboard ./work/myrun --still 520   # a few seconds each
```

The validation report prints each scene's start in **frames** and its duration in
**seconds**, so mid-scene is `from + duration * fps / 2`. Look for, specifically:

- text landing on top of a figure, or on a busy part of one
- a headline competing with type that is already inside the figure
- a crop that cuts a word, a chart title, or an axis label — for a chart this is
  the most common problem, and the fix is `"fit": "contain"`
- rules and dividers that have vanished (anything under 2px does, in video)
- Chinese lines breaking mid-word — fix with an explicit `\n` in the text

When a figure fights you, the answer is usually a different slot or fit, not a
smaller font. A chart or schematic wants `"fit": "contain"` so nothing is cropped;
a wide schematic wants `band`; a screenshot wants `inset`; a photograph wants
`full` with `cover` and a push-in.

Watch the overall shape too: if every figure ends up `contain` + `hold`, the middle
of the video will read as slides. Give at least one figure that has the pixels for
it a gentle `push-in`.

## Constraints that are not negotiable

These come from Remotion's rendering model, and violating them produces videos
that look fine in preview and break in the render:

- **No CSS animations, transitions, or Tailwind `animate-*`.** Frames render
  across parallel browser tabs that share no animation state, so anything not
  driven by `useCurrentFrame()` flickers. Animate with `interpolate()`.
- **`interpolate()` returns a number, never a string.** Wrap it in a template
  literal for `translate`/`rotate`. And `translate` needs the two-value form:
  a bare number is translateX only.
- **`<Audio volume={(f) => …}>` receives audio-local frames**, not composition
  frames. The music bed is mounted at frame 0 outside any Sequence so the two
  coincide; keep it that way.
- **A `cut` is the absence of a transition**, not a zero-frame one.

The full list, with the reasoning and the failure each rule prevents, is in
[references/pitfalls.md](references/pitfalls.md). Read it before editing the
engine in `assets/template/src/`.

## Typography

Chinese in Remotion has one large trap: routing CJK through
`@remotion/google-fonts` means about 101 unicode-range subsets times 9 weights,
each its own `FontFace` and its own render-blocking `delayRender()` — hundreds of
network fetches per frame tab. This skill instead subsets two variable faces
locally with `pyftsubset` to exactly the characters the storyboard uses: about
310 codepoints becomes ~125KB total, versus ~36MB, with zero network at render.

The type scale, safe area, the exact character-per-line budgets and the CJK
line-breaking rules are in [references/cjk-type.md](references/cjk-type.md).
Read it before changing any font size.

## Requirements

Already present on this machine; listed so a failure is diagnosable.

| Needs | For | Check |
|---|---|---|
| `bun` | runs baoyu-fetch during harvest | `bun -v` |
| `agent-browser` | design tokens via getComputedStyle | `agent-browser --version` |
| `pyftsubset` with brotli | font subsetting | `pyftsubset --help` |
| `sips` | image dimensions (macOS built-in) | — |
| Node 20+, Chrome | rendering | `node -v` |

First run downloads two Noto CJK variable fonts (~37MB total) into
`~/.cache/html2video/fonts/` and caches them permanently. If that download fails
the skill falls back to a macOS system font and says so — text metrics then vary
between machines, which breaks reproducible line breaking.

No music ships with this skill, because shipping music means shipping a licence.
Drop a file into the harvest directory and set `audio.bed` to its name; without
one the video renders silent.

## Resources

- [references/editorial.md](references/editorial.md) — the READ stage: salience
  mining, triage, narrative arcs, banned phrasing
- [references/storyboard.md](references/storyboard.md) — schema field by field,
  plus a full worked example from a real article
- [references/shots.md](references/shots.md) — the ten shots: what each is for,
  its composition, its motion
- [references/cjk-type.md](references/cjk-type.md) — type scale, safe area,
  character budgets, CJK line breaking, font subsetting
- [references/narration.md](references/narration.md) — 口播 mode: writing a script
  people can record, trimming on-screen text, how speech length is estimated
- [references/pitfalls.md](references/pitfalls.md) — every constraint and
  hard-won gotcha, with the failure it prevents
