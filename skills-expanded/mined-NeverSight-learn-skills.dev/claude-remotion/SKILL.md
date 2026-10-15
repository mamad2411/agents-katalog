---
name: claude-remotion-skill
description: Use when a user wants to build a programmatic video from a folder of materials (screenshots, recordings, narration audio, music, SFX) with Remotion. Scaffolds a TypeScript video project from a manifest.json and ships reusable motion-design components (browser frames, stat reveals, Ken Burns pans, comparison slides, terminal animations) plus audio primitives with automatic music ducking under narration. Pairs with claude-polly-skill (TTS) and claude-mflux-skill (image generation).
---

# claude-remotion-skill — Programmatic Video via Remotion

Generates rendered MP4 videos using [Remotion](https://www.remotion.dev/). Ships a **template** (copied into the user's project) with reusable components, audio-sync primitives, and a **manifest-driven** scene system. SKILL.md teaches the workflow; the underlying `remotion` CLI does the rendering.

## When to use

- User says "build a video", "render a walkthrough", "assemble these clips and screenshots"
- User has a materials folder (screenshots / recordings / narration audio / music / SFX) and wants a rendered MP4
- User wants a scaffolded Remotion project with sensible defaults
- Pair with `claude-polly-skill` when narration audio needs to be generated first
- Pair with `claude-mflux-skill` when title frames or background art need to be generated first

**Not for:**
- Planning scenes from a brief (that's the future `claude-video-director-skill`)
- One-off image → video with no motion design (use ffmpeg directly)

## Preflight

Before scaffolding, check:

- `node --version` → must be ≥ 18. If missing: `brew install node` / install from nodejs.org.
- `ffprobe -version` → must be present. If missing: `brew install ffmpeg` / install ffmpeg.

## Workflow

### 1. Scaffold a new project

```bash
bash scripts/scaffold.sh <target-dir>
cd <target-dir>
npm install
```

`scaffold.sh` copies `template/` into `<target-dir>` and renames `manifest.example.json` → `manifest.json`. Refuses to overwrite a non-empty target unless `--force` is passed.

### 2. Drop materials into assets/

```
<target-dir>/assets/
├── screenshots/       # PNG/JPG — consumed by UIFrame / KenBurns
├── recordings/        # MP4/WebM — consumed via <Video> tag
├── audio/narration/   # MP3 from Polly (or wherever)
├── audio/music/       # MP3 — single continuous bed
├── audio/sfx/         # WAV/MP3 — one-shot cues
└── branding/          # logos (SVG/PNG)
```

### 3. Measure audio durations

```bash
bash scripts/measure-audio.sh assets/audio/narration --json > /tmp/narration-durations.json
```

Copy the `seconds` values into `manifest.json` — one `duration` per scene that uses narration, OR set `durationFromAudio` to the narration path and then manually mirror the measured duration into `duration` (Remotion's Composition component needs a static number at registration time).

### 4. Edit manifest.json

The manifest is the single source of truth. Every field:

| Field | Type | Notes |
|---|---|---|
| `video.width`, `video.height`, `video.fps` | int | Default 1920×1080 @ 30fps |
| `audio.music` | object or null | `{src, baseVolume, duckTo}` — ducks under narration |
| `scenes[].id` | string | Unique, used as Sequence key |
| `scenes[].component` | string | Module path like `sequences/S3_Pipeline` |
| `scenes[].duration` | number | Seconds. Required (even if also setting durationFromAudio). |
| `scenes[].durationFromAudio` | string | **INFORMATIONAL ONLY** — Remotion needs static numbers at composition-registration time. Use `measure-audio.sh` to get the seconds, then mirror into `duration`. This field serves as a human-readable pointer to which audio file the duration came from. |
| `scenes[].narration` | string \| null | Path to narration MP3 — auto-wires NarrationTrack |
| `scenes[].sfx[]` | array | `[{src, atSecond}]` one-shot cues |
| `scenes[].props` | object | Passed as props to the scene component |

To customize colors, fonts, or spacing, edit `src/theme.ts` directly. Changes apply to all scenes.

Example:

```json
{
  "video": { "id": "demo", "width": 1920, "height": 1080, "fps": 30, "title": "Demo" },
  "audio": { "music": { "src": "assets/audio/music/bg.mp3", "baseVolume": 0.3, "duckTo": 0.15 } },
  "scenes": [
    {
      "id": "S1_title",
      "component": "sequences/S1_Title",
      "duration": 6,
      "narration": null,
      "sfx": []
    },
    {
      "id": "S2_overview",
      "component": "sequences/S2_Overview",
      "duration": 30,
      "narration": "assets/audio/narration/s2.mp3",
      "sfx": [{ "src": "assets/audio/sfx/whoosh.wav", "atSecond": 1.5 }],
      "props": { "strainCount": 277 }
    }
  ]
}
```

### 5. Write scene components

Each scene is a React component under `src/sequences/`. Fork `ExampleScene.tsx` as a template. Register every new scene in `src/Video.tsx`'s `sceneRegistry` map:

```ts
const sceneRegistry: Record<string, React.ComponentType<any>> = {
  "sequences/ExampleScene": ExampleScene,
  "sequences/S1_Title": S1Title,          // ← add entries here
  "sequences/S2_Overview": S2Overview,
};
```

**You must register every new scene in this map.** If you add a scene to `manifest.json` but forget to add it to `sceneRegistry`, the render fails with `Scene component "X" not in sceneRegistry`.

Scenes receive `manifest.scenes[].props` as React props. Use the shipped components:

| Component | Use case |
|---|---|
| `UIFrame` | Wrap a screenshot in a browser window chrome |
| `StatReveal` | Animated counter (277, 66,554, 99.3%) |
| `TerminalAnimation` | Typewriter error / code reveal |
| `ComparisonSlide` | Left-vs-right layout (before/after) |
| `ProgressBar` | Animated fill bar |
| `CategoryPill` | Animated chip / tag |
| `TitleCard` | Logo + title + subtitle slot |
| `FadeTransition` | Crossfade wrapper |
| `KenBurns` | Pan/zoom over a still image |

Audio is wired automatically from the manifest — you do NOT need to import `NarrationTrack` / `MusicBed` / `SFXCue` in your scene files; `Video.tsx` handles them.

### 6. Preview

```bash
npx remotion preview
```

Opens a browser at `http://localhost:3000`. Iterate until it looks right.

### 7. Render

```bash
mkdir -p output
npx remotion render src/index.ts Main "output/video_$(date +%Y%m%d_%H%M%S).mp4"
```

4K variant:

```bash
npx remotion render src/index.ts Main "output/video_4k_$(date +%Y%m%d_%H%M%S).mp4" --width 3840 --height 2160
```

### 8. Cleanup

```bash
bash scripts/cleanup.sh --dry-run                # preview
bash scripts/cleanup.sh                          # delete all video_*.mp4
bash scripts/cleanup.sh --older-than-days 7      # only old ones
```

Only files matching `video_*.mp4` are touched.

**When to suggest cleanup to the user:**
- If generating many renders during iteration, offer to clean up old ones before the next render
- Before archiving or sharing the project, remind the user `output/` is gitignored but contains accumulated MP4s
- When disk space is a concern — MP4 renders can be 50–500MB each

## Pairing with sibling skills

**Generate missing narration with `claude-polly-skill`:**

```bash
polly generate "Your narration text" --voice Matthew --language en-US
# MP3 lands in output/; copy into assets/audio/narration/ of your Remotion project
```

**Generate missing title frames with `claude-mflux-skill`:**

```bash
mflux-generate --model schnell --prompt "Dark technology gradient background" \
  --output output/mflux_$(date +%Y%m%d_%H%M%S).png --metadata
# Copy into assets/screenshots/ or assets/branding/
```

## Audio sync details

- **NarrationTrack** plays inside each scene's `<Sequence>`. Remotion handles the timing.
- **MusicBed** sits at the composition root (outside all sequences) and plays continuously. Its volume ducks to `audio.music.duckTo` during any narration range, with an 8-frame linear ramp at each boundary to avoid clicks. Ranges are computed from manifest scenes.
- **SFXCue** fires at `atSecond` within its parent scene — useful for UI clicks, chimes on stat reveals, etc.

## Subtitles

Remotion + Polly speech-marks is the documented path: generate speech-marks JSON via `aws polly synthesize-speech --output-format json --speech-mark-types word ...`, load it in a captions component using `@remotion/captions`. Not shipped in v1 — a future enhancement.

## What not to do

- **Don't hardcode frame offsets in scene components.** Use `useCurrentFrame()` and derive everything from the scene's duration (available via `useVideoConfig().durationInFrames`).
- **Don't use native `<img>` for screenshots.** Always use Remotion's `<Img src={staticFile(...)} />` so assets are bundled.
- **Don't use CSS animations or transitions.** All motion must use `interpolate()` or `spring()` against `useCurrentFrame()` — CSS animations run in real time, not video time.
- **Don't set `<Audio>` duration manually** — let the parent `<Sequence>`'s `durationInFrames` drive it.
- **Don't commit `output/` or `node_modules/`.** Template's `.gitignore` handles this.
- **Don't edit theme values inline in components.** Edit `src/theme.ts` to change colors, fonts, or spacing globally.
- **Don't add new scenes without registering them in `Video.tsx`'s `sceneRegistry`.** The error message is clear if you forget.

## Verifying a render

After `npx remotion render` completes, the MP4 path is printed. Verify:

```bash
ffprobe -v error -show_entries format=duration,size -of default=noprint_wrappers=1 output/video_*.mp4
```

Offer to open it: `open output/video_*.mp4` on macOS.
