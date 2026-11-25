---
name: bigeye-sticker-video
description: Create sticker-style / paper-collage animated product videos, UI walkthroughs, feature spots and posters. Edit content.js, preview frames, generate optional procedural music, and render locally with Chrome and FFmpeg. Use for the paper-and-sticker visual style, not live-action editing.
metadata:
  displayName: BigEye-Sticker-Video
  title: BigEye-Sticker-Video
---

# BigEye-Sticker-Video

A **sticker style system** plus a deterministic production pipeline. The visual language is
locked so every film feels like the same studio; the storyboard, scene order, palette and
copy are yours.

```
content.js (data)  →  engine.js (style + components)  →  __render(t)  →  headless Chrome
                   →  frames/*.png  →  ffmpeg + procedural score  →  out/video.mp4
```

Default: **1920×1080 / 30 fps / H.264 + AAC**, plus poster and contact sheet.

## What is locked, what is free

| Locked — the sticker look | Free — everything else |
|---|---|
| warm paper desk + subtle dot/grid/grain/vignette | palette preset or brand colors |
| die-cut stickers: 16/512 white border + 4/512 ink outline | scene count, order, timing |
| flat vector art, no gradients/photoreal inside stickers | copy, language, mascot choice |
| soft hard-ish shadows, −4°…+4° rotations | launch / UI tour / feature spot / event / still |
| ink-first type with mono English texture | 16:9 engine default; custom scenes for other ratios |
| 120 BPM beat cut grid (0.5 s), cut-driven transitions | music style / voiceover / SFX |
| optional mascot, same character throughout | whether a mascot appears at all |

**Do not clone a previous film.** Reuse the style tokens and components, then choose the
format that fits the brief. `template/content.js` is a demo, not the required structure.

## When to use / not use

Use for: product launches, **UI / feature walkthroughs**, benchmark explainers, event
intros, social promos, brand mascot films, “paper + sticker” motion graphics.

Don't use for: live-action, photoreal 3D, long-form narrative, subtitled interviews.
The built-in layouts are 16:9; vertical 9:16 needs custom scene code (`type:'custom'`).

## Prerequisites

- macOS or Linux, **Google Chrome**, **Node.js ≥ 22.4** (built-in WebSocket), **ffmpeg/ffprobe**, `lsof`
- Optional audio: **Python 3 + numpy** (`python3 -m pip install numpy`)
- CJK fonts (macOS Hiragino/PingFang; Linux Noto Sans CJK) + a mono font;
  override `brand.fonts` if needed

On Linux or with a non-default Chrome location, set `CHROME` to the browser executable path.

## Quick start

```bash
# 1. scaffold (run from the skill folder)
bash scripts/new-project.sh /tmp/my-video
cd /tmp/my-video

# 2. choose a format + palette, edit content.js
#    (see "Formats" below; preview stills before the full render)
STILLS="2,6,12,18,24" OUT="$PWD/stills" node scripts/cdp-render.mjs

# 3. audio (optional)
node scripts/cue-sheet.mjs
python3 scripts/build_audio.py --cues audio/cues.json --out audio/soundtrack.wav

# 4. render + encode
bash scripts/render.sh
bash scripts/encode.sh

# 5. QA gate
bash scripts/qa.sh
```

Deliver `out/video.mp4`, `out/poster.jpg`, `out/contact-sheet.jpg`, source, audio licenses.
Delete `frames/` (3–4 GB) after encoding.

## Formats (pick one, then adapt)

### A. Launch film — 30–48 s
`hero → statement → numbers/stats → gallery → features → quote → cta`
The classic 8-card recipe is in `references/STORYBOARD.md`. Use it only if it fits.

### B. UI / feature tour — 25–45 s
Show the real interface, then point at the one control that matters:

```
hero (title + promise)
→ ui (screen + spotlight + cursor click + callout)   × 3–5 features
→ quote / statement (one human line)
→ cta
```

Each `ui` scene takes over the role of a feature card: a screenshot or a UI mock inside a
sticker frame, a dimmed screen with a spotlight hole, a cursor that moves and clicks, and
a numbered callout card connected by a hand-drawn dashed arrow. See `references/UI-TOUR.md`.

### C. Feature spot — 12–20 s
`hero → statement → ui/features → cta`. One feature, one click, one proof.

### D. Announcement / event — 20–30 s
`hero → statement → numbers/quote → cta`. No product screens required.

### E. Still / poster
Render one frame with `STILLS="..."`; same style, no video. Good for covers and thumbnails.

## Edit `content.js`

- `brand.palette`: `kraft` (default, terracotta/teal) · `deepseek` (blue/red) ·
  `candy` (pink/violet) · `mono` (ink + one red). Or set `brand.colors` per role.
- `brand.background`: `dots` (default) · `grid` · `plain`.
- `brand.mascot`: any 512×512 sticker SVG; set `mascot:false` on a scene to skip it.
- `scenes`: `type`, `duration`, `chapter*`, `transition`, `mascot` + type fields.
- Field reference: `references/SCENES.md`; UI tour fields: `references/UI-TOUR.md`.
- Copy rules: title ≤ ~14 CJK chars, chips ≤ 4, card text ≤ 2 lines.
- Anything not covered: `{ type:'custom', draw(tl,t){ ... } }` with `window.__STICKER`.

## Scene components

| type | key fields |
|---|---|
| `hero` | `date,kicker,titleLines[{text,size,color}],subtitle,stamp,stampLabel,chips` |
| `statement` | `lines[{text,size,color}],sub,chips[],underlineY` |
| `stats` | `title,sub,rows[{label,before,after,highlight}],max,badge,footnote` |
| `numbers` | `title,sub,items[{icon|image,label,value,note,badge}],banner` |
| `gallery` | `title,sub,items[{image|icon,title,sub,bg}],tags[]` |
| `features` | `title,sub,items[{icon,title,desc}]` |
| `bullets` | `title,sub,items[string|{icon,text,sub}]` |
| `quote` | `text` (`\n` ok), `cite`, `quoteMark:false` |
| `ui` | `image,focus{x,y,w,h},cursor,callout{no,title,text},title,sub` |
| `cta` | `tagline,brandName,versionLine,line,chips[],seal,sealLabel,url` |
| `custom` | `draw(tl,t)` with `window.__STICKER` |

Transitions: `peel, slide, zoom, whip, zoomthrough, flurry, flip, slideup, cut`.
Camera: `push, pull, none, {z0,z1,dx,dy}`.
Mascot: `{anim:'enter-left'|'cross-top'|'cross-mid'|'below'|'corner'|'orbit'|'hero', x,y,size,rot,trail,facingLeft}`.

## Assets

- 16 built-in SVGs in `assets/sticker-kit/` (medal, price-tag, ribbon, banner,
  stamp-ring, spark, star, magnifier, globe, open-box, paper-arrow, tape,
  check-badge, bubble, cursor, mascot-star).
- UI screenshots/mocks go in `assets/ui/` (1600×960 recommended for the `ui` layout).
- Any brand mascot: **512×512 transparent SVG**, subject centered, white border +
  ink outline baked in. The engine adds shadow/rotation only.
- Gallery images: SVG/PNG/JPG, cover-cropped in the polaroid; keep content in the
  center 80% safe area.

## Audio

`node scripts/cue-sheet.mjs` writes `audio/cues.json` (duration, cuts, scenes).
`python3 scripts/build_audio.py --cues audio/cues.json --out audio/soundtrack.wav`
produces a 120 BPM score with an accent on every cut; `--energy high|calm`.
Optional Openverse SFX: `references/AUDIO.md` (CC0/CC-BY only, record licenses).

## Render & QA

- `bash scripts/render.sh` — 4 parallel Chrome workers; `WORKERS=2` on shared machines.
- `START=12 END=18 node scripts/cdp-render.mjs` — re-render a segment.
- `bash scripts/qa.sh` — gate: specs, loudness, black/freeze, cut keyframes; exits non-zero.
- Then **look** at `out/contact-sheet.jpg` and `qa/keyframes/`.

## Style QA (the locked part)

- [ ] Paper + dot/grid texture visible; no pure white/flat frame
- [ ] Stickers have consistent white border + ink outline; no baked shadows/extra strokes
- [ ] Flat vector look; no photoreal/gradient inside sticker art
- [ ] Shadows/rotations consistent; typography ink-first, mono English as texture
- [ ] Cuts on the 0.5 s grid; transitions don't rewind the first element
- [ ] If a mascot is used: same character, readable size, not upside-down/over the header
- [ ] Specs/duration exact; QA passes; keyframes reviewed at every cut

## Install

Copy the folder into a DSH skill root (depth 1, with `SKILL.md`):

```bash
cp -R bigeye-sticker-video ~/.dsh/skills/          # user-level
# or: cp -R bigeye-sticker-video <project>/.dsh/skills/
```

Then load it with the `skill` tool (`bigeye-sticker-video`).
