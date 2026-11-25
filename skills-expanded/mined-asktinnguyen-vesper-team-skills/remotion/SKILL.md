---
name: remotion
description: Create programmatic videos using React with Remotion. Use for video compositions, animations, rendering to MP4/WebM/GIF, spring/interpolate animations, or Lambda deployment.
---

# Remotion

Videos are functions of frames. First frame is 0, last is `durationInFrames - 1`.

**Related skills:**
- `@launchpad-remotion` - Reusable components for trycua/launchpad projects
- `@ffmpeg` - Video processing, format conversion, speed adjustment
- External TTS/audio tools for voiceovers and sound effects

**Global knowledge base:** `~/docs/solutions/video-production/remotion/`
- `prompts.md` - 10 ready-to-use animation prompts
- `techniques.md` - Advanced animation techniques
- `libraries.md` - Component libraries & packages
- `github-examples.md` - Top GitHub repos

## Quick Start

```bash
npx create-video@latest      # Create project
npx remotion studio          # Preview
npx remotion render src/index.ts CompositionId out.mp4
```

## Core API

```tsx
import { useCurrentFrame, useVideoConfig, interpolate, spring, Easing } from 'remotion';

const frame = useCurrentFrame();
const { fps, durationInFrames, width, height } = useVideoConfig();

// Interpolate (always clamp!)
const opacity = interpolate(frame, [0, 30], [0, 1], { extrapolateRight: 'clamp' });

// Spring animation
const scale = spring({ frame, fps, config: { damping: 10, stiffness: 100 } });

// Easing
const value = interpolate(frame, [0, 30], [0, 100], { easing: Easing.bezier(0.25, 0.1, 0.25, 1) });

// Color interpolation
const color = interpolateColors(frame, [0, 30], ['#ff0000', '#0000ff']);
```

## Sequencing

```tsx
import { Sequence, Series, Loop, Freeze } from 'remotion';

// Time-shift (useCurrentFrame becomes relative)
<Sequence from={30} durationInFrames={60}><Scene /></Sequence>

// Play consecutively
<Series>
  <Series.Sequence durationInFrames={30}><Intro /></Series.Sequence>
  <Series.Sequence durationInFrames={60}><Main /></Series.Sequence>
</Series>

// Repeat
<Loop durationInFrames={30} times={3}><Animation /></Loop>

// Pause at frame
<Freeze frame={10}><Component /></Freeze>
```

## Media

```tsx
import { AbsoluteFill, Img, Video, OffthreadVideo, Audio, staticFile } from 'remotion';

<AbsoluteFill>
  <Img src={staticFile('image.png')} />
  <Video src={staticFile('clip.mp4')} volume={0.5} startFrom={30} />
  <OffthreadVideo src={staticFile('large.mp4')} />  {/* Better perf */}
  <Audio src={staticFile('music.mp3')} volume={0.8} />
</AbsoluteFill>
```

**Props:** `volume`, `playbackRate` (constant only!), `muted`, `loop`, `startFrom`, `endAt`

## Transitions

```tsx
import { TransitionSeries, linearTiming, springTiming } from '@remotion/transitions';
import { fade } from '@remotion/transitions/fade';
import { slide } from '@remotion/transitions/slide';

<TransitionSeries>
  <TransitionSeries.Sequence durationInFrames={60}><SceneA /></TransitionSeries.Sequence>
  <TransitionSeries.Transition presentation={fade()} timing={linearTiming({ durationInFrames: 15 })} />
  <TransitionSeries.Sequence durationInFrames={60}><SceneB /></TransitionSeries.Sequence>
</TransitionSeries>
```

**Official:** `fade()`, `slide({ direction })`, `wipe()`, `flip()`, `clockWipe()`
**Directions:** `from-left`, `from-right`, `from-top`, `from-bottom`

**Custom (digitalsamba toolkit `lib/transitions/`):**

| Transition | Options | Use Case |
|------------|---------|----------|
| `glitch()` | `intensity`, `slices`, `rgbShift` | Tech, cyberpunk |
| `rgbSplit()` | `direction`, `displacement` | Modern, energetic |
| `zoomBlur()` | `direction`, `blurAmount` | Impact, CTAs |
| `lightLeak()` | `temperature`, `direction` | Film aesthetic |
| `clockWipe()` | `startAngle`, `direction` | Time-related |
| `pixelate()` | `maxBlockSize`, `glitchArtifacts` | Retro, gaming |
| `checkerboard()` | `pattern`, `gridSize` | Playful reveals |

**Timing:** Quick=15-20f, Standard=30-45f, Dramatic=50-60f

## Composition

```tsx
// src/Root.tsx
<Composition
  id="MyVideo"
  component={MyComponent}
  durationInFrames={150}
  fps={30}
  width={1920}
  height={1080}
  defaultProps={{ title: 'Hello' }}
/>
```

## Async Data

```tsx
const [handle] = useState(() => delayRender());

useEffect(() => {
  fetchData().then(data => {
    setData(data);
    continueRender(handle);
  });
}, [handle]);
```

## CLI Rendering

```bash
npx remotion render src/index.ts MyComp out.mp4 \
  --codec=h264 --quality=80 --scale=2 --frames=0-59 \
  --props='{"title":"Hello"}'
```

## Critical Rules

1. **Frame-based only** - CSS transitions/animations are FORBIDDEN
2. **Always clamp** - `extrapolateRight: 'clamp'` prevents runaway values
3. **Use fps** - `2 * fps` for 2 seconds, not magic numbers
4. **OffthreadVideo** - Use for heavy videos
5. **delayRender** - Block until async data ready
6. **staticFile** - Reference public/ folder assets

## Deep Dive Rules

Read `rules/*.md` for detailed patterns:

| Topic | File |
|-------|------|
| 3D/Three.js | [rules/3d.md](rules/3d.md) |
| Animations | [rules/animations.md](rules/animations.md) |
| Audio | [rules/audio.md](rules/audio.md) |
| Captions | [rules/display-captions.md](rules/display-captions.md), [rules/transcribe-captions.md](rules/transcribe-captions.md) |
| Charts | [rules/charts.md](rules/charts.md) |
| Compositions | [rules/compositions.md](rules/compositions.md) |
| Fonts | [rules/fonts.md](rules/fonts.md) |
| GIFs | [rules/gifs.md](rules/gifs.md) |
| Images | [rules/images.md](rules/images.md) |
| Lottie | [rules/lottie.md](rules/lottie.md) |
| Maps | [rules/maps.md](rules/maps.md) |
| Measuring | [rules/measuring-text.md](rules/measuring-text.md), [rules/measuring-dom-nodes.md](rules/measuring-dom-nodes.md) |
| Parameters | [rules/parameters.md](rules/parameters.md) |
| Sequencing | [rules/sequencing.md](rules/sequencing.md) |
| Tailwind | [rules/tailwind.md](rules/tailwind.md) |
| Text animations | [rules/text-animations.md](rules/text-animations.md) |
| Timing/Easing | [rules/timing.md](rules/timing.md) |
| Transitions | [rules/transitions.md](rules/transitions.md) |
| Trimming | [rules/trimming.md](rules/trimming.md) |
| Videos | [rules/videos.md](rules/videos.md) |

## Lambda (Serverless)

```bash
npx remotion lambda policies user
npx remotion lambda functions deploy
npx remotion lambda sites create src/index.ts --site-name=mysite
npx remotion lambda render <serve-url> MyComp out.mp4
```

See [reference.md](reference.md) for full `@remotion/renderer` and `@remotion/lambda` APIs.

## Player (Embed)

```tsx
import { Player } from '@remotion/player';

<Player
  component={MyComp}
  durationInFrames={150}
  fps={30}
  compositionWidth={1920}
  compositionHeight={1080}
  controls loop autoPlay
/>
```
