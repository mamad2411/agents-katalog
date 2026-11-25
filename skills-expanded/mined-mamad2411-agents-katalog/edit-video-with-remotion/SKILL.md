---
name: edit-video-with-remotion
description: Edit, compose, and render video from existing footage with Remotion v4 on React
argument-hint: "[footage-or-idea]"
related:
  - follow-lib-remotion
  - deep-review-codebase
  - gen-subtitle-video
  - use-bun-native-api
  - follow-lib-animejs
  - follow-lib-iconify
  - run-build

---

## Goal

Programmatically edit, compose, and render video from existing footage with Remotion v4 on React — trim, concatenate, overlays, transitions, subtitles, audio mix, and export via CLI or cloud

## Scope

Use for:
- Video editing (trim, split, concatenate)
- Adding overlays such as text, image, animation
- Adding transitions and motion effects
- Adding subtitles/captions programmatically
- Handling audio (mix, fade, mute)
- Rendering via Remotion CLI or cloud services

See also: /follow-lib-remotion, /deep-review-codebase, /gen-subtitle-video

## Execute

### 1. Setup Project

> Goal: prepare a Remotion project for editing

1. Create the project with `bunx create-video@latest my-edit` and pick a suitable template (`--blank` for a blank template if flag-based prompts are supported)
2. Install packages via `bunx remotion add <pkg>` (auto-syncs versions with core):
   - `@remotion/media` — the main `<Video>`/`<Audio>` components (always required)
   - `@remotion/transitions` — transitions between scenes
   - `@remotion/captions` — parse `.srt` into captions
   - `@remotion/gif` — GIF as source/overlay
3. Put input footage in `public/` and reference it with `staticFile()`
4. Use `bun` as the runtime/package manager per the project

### 2. Import And Trim Source Videos

> Goal: use the existing footage as source

1. Use `<Video>` from `@remotion/media` (Mediabunny/WebCodecs — frame-perfect, fastest, identical preview + render)
2. Fall back to `<OffthreadVideo>` from `remotion` when a codec/container is unsupported (FFmpeg-based)
3. Set `src` with `staticFile('input.mp4')` or a remote URL (requires CORS)
4. Use `trimBefore` / `trimAfter` (in frames) to cut the start/end without re-encoding
5. Wrap the source video in `<Sequence>` to shift its position on the timeline with `from`
6. Compute frames from time: `frames = time * fps` using `useVideoConfig()`

### 3. Concatenate Clips

> Goal: play several clips back to back

1. Use `<Series>` and `<Series.Sequence>` from `remotion` to play clips sequentially (no transition)
2. Specify `durationInFrames` on each `<Series.Sequence>`
3. To transition between clips → use `<TransitionSeries>` instead (see step 7)
4. Use a plain `<Sequence>` when you need to control layout or overlap yourself
5. Ensure the total `durationInFrames` in `<Composition>` covers every clip (TransitionSeries shortens total length by the transition duration)

### 4. Add Overlays And Graphics

> Goal: add overlays on top of the video

1. Use `<AbsoluteFill>` as the full-frame overlay container
2. Use `<Img>` for logo/image overlays and `<Gif>` from `@remotion/gif` for GIFs
3. Use plain React text components for lower thirds and titles
4. Use `interpolate()` for opacity fade in/out (specify `extrapolateLeft/Right: 'clamp'`)
5. Use `spring()` for motion-based intro/outro
6. Use `useCurrentFrame()` to sync animation with the timeline — never use CSS animation

### 5. Add Subtitles

> Goal: add subtitles/captions to the video

1. Use `/gen-subtitle-video` to create a `.srt` and place it in `public/`
2. Fetch with `fetch(staticFile('subtitles.srt'))` inside `useDelayRender()` + `continueRender` after parsing completes
3. Parse with `parseSrt({input})` from `@remotion/captions` → `Caption[]` with `startMs`, `endMs`, `text`
4. Convert ms → frame with `(ms / 1000) * fps`, then conditionally render based on `useCurrentFrame()`
5. Place subtitles at the bottom of the screen with padding and background contrast

### 6. Handle Audio

> Goal: handle audio tracks

1. Use `<Audio>` from `@remotion/media` for background music / voice over
2. Mute the source audio with the `muted` prop on `<Video>` when mixing instead
3. Adjust `volume` (number or callback) and `playbackRate` per scene
4. Fade volume with a callback: `volume={(f) => interpolate(f, [0, fps], [0, 1], {extrapolateRight: 'clamp'})}`
5. `<Html5Audio>` from `remotion` is legacy — use it only as a preview fallback

### 7. Add Transitions

> Goal: add transitions between clips

1. Use `<TransitionSeries>` from `@remotion/transitions` instead of hand-rolled interpolation
2. Structure: alternate `<TransitionSeries.Sequence>` → `<TransitionSeries.Transition>` → `<TransitionSeries.Sequence>`
3. `presentation`: `fade()`, `slide()`, `wipe()` (import from `@remotion/transitions/fade`, etc.)
4. `timing`: `linearTiming({durationInFrames})` or `springTiming({config: {damping}})`
5. Use `<TransitionSeries.Overlay>` for effects layered over the cut point (e.g. light leak) without shortening the timeline
6. Remember that a transition makes 2 scenes overlap → total duration shortens by the transition duration

### 8. Render

> Goal: export the finished video

1. Test in Remotion Studio before rendering with `bunx remotion studio`
2. Render with `bunx remotion render <CompId> out/video.mp4` plus flags such as `--codec=h264`
3. Set `fps`, `width`, `height` in `<Composition>` per the deliverable
4. Use `--props=props.json` for dynamic input
5. If the output is a GIF → use `--codec=gif --every-nth-frame=2`
6. Set defaults via `remotion.config.ts` with `Config` from `@remotion/cli/config` (e.g. `Config.setConcurrency(8)`, `Config.setCodec('h265')`)
7. Use `@remotion/lambda` or `@remotion/cloudrun` for large-scale cloud rendering

### 9. Optimize

> Goal: reduce output size and render time

1. Use `<Video>` from `@remotion/media` — fastest render with partial asset loading
2. Lower the input resolution when 4K is not required
3. Use `/deep-review-codebase` for pre-compressing inputs
4. Use `--concurrency` around `os.cpus().length`, or set it in `remotion.config.ts`
5. Use `--image-format=jpeg` when the render needs no transparency

## Rules

### 1. Footage

- Use `staticFile()` for assets in `public/`
- Use `<Video>` from `@remotion/media` as the default — `<OffthreadVideo>` only as a fallback, `<Html5Video>` legacy only
- Compute frames from the composition's `fps`

### 2. Timing

- Every duration must be `durationInFrames`, not milliseconds (except `Caption` from parseSrt, which is in ms — must be converted)
- Use `useVideoConfig()` to get `fps` for calculations
- Use only `useCurrentFrame()`, never CSS animations

### 3. Audio

- Separate the audio track from the source with `muted` when mixing
- Use `<Audio>` from `@remotion/media` — `<Html5Audio>` only as a preview fallback
- Beware of background music copyright

### 4. Overlays

- Use `<AbsoluteFill>` as the main container
- Use `interpolate()` for fade/opacity
- Use `spring()` for motion
- Use `z-index` via style or component order, no more than 3 main layers

### 5. Subtitles

- Use `parseSrt()` from `@remotion/captions` — captions have `startMs`/`endMs` that must be converted to frames
- Always fetch subtitles inside `useDelayRender()`
- Use a readable font with high contrast
- Test on the real target device or resolution

- Use /follow-lib-remotion for Remotion API details
- Use /deep-review-codebase to optimize input/output
- Use /gen-subtitle-video to generate subtitles
- Use /use-bun-native-api when using Bun as the runtime
- Use /follow-lib-animejs for complex animations
- Use /follow-lib-iconify for icon overlays

## Expected Outcome

- Video trimmed, concatenated, with overlays, transitions, and subtitles as desired
- Render output in the chosen format (mp4, gif, image sequence)
- Audio correctly synced with video
- Project can render via CLI or cloud
