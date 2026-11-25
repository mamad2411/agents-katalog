---

name: remotion-video-editing
description: Create, edit, and render videos using Remotion — a React-based video-as-code framework. Covers setup from scratch, project structure, key commands, core concepts, and known pitfalls.
trigger: When the user wants to create, edit, or render videos using Remotion (video-as-code with React), including batch-producing short-form content, adding text overlays, subtitles, animations, or compositing.

---
## What This Skill Does

This skill Create, edit, and render videos using Remotion — a React-based video-as-code framework. Covers setup from scratch, project structure, key commands, core concepts, and known pitfalls.

## Setup
Remotion source is cloned at `/root/.openclaw/workspace/remotion` (reference only).
Your actual project is at `/root/.openclaw/workspace/remotion-project`.

If the project doesn't exist yet, create it:

```bash
cd /root/.openclaw/workspace
printf '\n\n' | npx create-video@latest remotion-project --blank --yes
cd remotion-project
npm install
```

**CRITICAL:** Do NOT try to build the full Remotion monorepo. `bun run build` in the monorepo root fails with ESM export errors (the esm bundler produces index.mjs with re-exports but no implementation files). Always use `create-video` to scaffold a consumer project instead.

## Project structure
- `src/Root.tsx` — defines compositions (video templates)
- `src/MyComposition.tsx` — the actual video component
- `src/index.ts` — entry point, registers compositions with `registerRoot`
- `remotion.config.ts` — global config
- `public/` — static assets (images, fonts, audio)

## Key commands
```bash
cd /root/.openclaw/workspace/remotion-project
npm run dev          # Start Remotion Studio (preview in browser)
npx remotion compositions  # List available compositions
npx remotion render <comp-id> out/video.mp4  # Render a video
npx remotion still <comp-id> out/still.png   # Render a still
```

## Key Remotion concepts
- **Composition** — a video template with duration, FPS, dimensions, and input props
- **Frames** — each frame is 1/FPS of a second. At 30fps, frame 30 = 1 second
- **`useCurrentFrame()`** — hook to get current frame number in a component
- **`useVideoConfig()`** — hook for dimensions, FPS, duration
- **`<Sequence>`** — layer components in time (use `from` and `durationInFrames`)
- **`<AbsoluteFill>`** — full-width container
- **`<OffthreadVideo>`** — for playing video/audio clips
- **`interpolate()`** — animate values across frame ranges
- **`spring()`** — spring-based animations (use `config: { damping, stiffness }` for feel)

## Hormozi-Style Text Video (TikTok/Reels/Shorts)

Fast, punchy short-form video: **one word at a time**, spring zoom entrance, color flash behind highlighted keywords, progress bar at bottom. Built for retention.

### Key Design Rule
**ONE WORD per Sequence entry.** Do NOT group multiple words into the same segment — they will overlap on screen. Use a flat word array where each word gets its own `Sequence` with a distinct `startFrame`.

### Word Schedule Pattern
```tsx
interface WordEntry {
  word: string;
  duration: number;     // frames this word stays visible
  highlight: boolean;   // gets color flash + bigger font + glow
  color: string;        // text + flash color
  size: number;         // 0=normal (68px), 1=big (96px)
}

const WORDS: WordEntry[] = [
  { word: 'How', duration: 6, highlight: false, color: '#FFFFFF', size: 0 },
  { word: 'To', duration: 6, highlight: false, color: '#FFFFFF', size: 0 },
  { word: 'Estimate', duration: 10, highlight: false, color: '#FFFFFF', size: 0 },
  { word: 'Property', duration: 8, highlight: true, color: '#FFD700', size: 1 },
  // ... more words
];

// Build schedule with computed startFrame
let frameCursor = 0;
const SCHEDULE = WORDS.map((w) => {
  const start = frameCursor;
  frameCursor += w.duration;
  return { ...w, startFrame: start };
});
```

### Word Pop Animation
Each word uses `spring()` for the entrance zoom and `interpolate()` for slide-up + exit fade:

```tsx
function WordDisplay({ word, color, size, entryFrame, fps, exitProgress }) {
  const scale = spring({
    frame: entryFrame,
    fps,
    config: { damping: 10, stiffness: 240, mass: 0.4 },
    durationInFrames: 5,
  });

  const slideY = interpolate(entryFrame, [0, 6], [60, 0], { extrapolateRight: 'clamp' });
  const opacity = exitProgress > 0.7
    ? interpolate(exitProgress, [0.7, 1], [1, 0], { extrapolateRight: 'clamp' })
    : 1;

  // Background flash for highlighted words
  const flashOpacity = spring({
    frame: entryFrame, fps,
    config: { damping: 6, stiffness: 120 },
    durationInFrames: 8,
  });

  return (
    <AbsoluteFill style={{ justifyContent: 'center', alignItems: 'center' }}>
      <AbsoluteFill style={{ backgroundColor: color, opacity: flashOpacity * 0.25 }} />
      <AbsoluteFill style={{ background: 'radial-gradient(ellipse at center, #111122 0%, #000 100%)' }} />
      <div style={{
        transform: `scale(${1 + scale * 0.35}) translateY(${slideY}px)`,
        opacity, color, fontWeight: 900,
        fontSize: size ? 96 : 68,
        fontFamily: 'Inter, Arial Black, Impact, sans-serif',
        textShadow: size ? `0 0 40px ${color}60, 0 8px 30px rgba(0,0,0,0.8)` : '0 4px 20px rgba(0,0,0,0.6)',
        letterSpacing: '-2px', lineHeight: 1.1,
      }}>
        {word}
      </div>
    </AbsoluteFill>
  );
}
```

### Composition Registration
```tsx
<Composition id="Hormozi" component={HormoziVideo}
  durationInFrames={450} fps={30} width={1080} height={1920} />
```

### Render
```bash
npx remotion render Hormozi out/video.mp4
```

### Hormozi Pitfalls
- **DO NOT group words in a single Sequence** — they render on top of each other
- Word durations of 5-14 frames (at 30fps) feel fast but readable
- Highlighted words (brand colors, step labels) should use size=1 + unique color
- Add a progress bar at the bottom for visual momentum
- Typical 15-second video = 450 frames = ~35 seconds render time

## Common patterns

### Staggered list reveal
Each item in a list starts later than the previous:
```tsx
{items.map((item, index) => (
  <Sequence key={index} from={startFrame + index * staggerFrames} durationInFrames={duration}>
    <ItemComponent item={item} index={index} />
  </Sequence>
))}
```
Inside ItemComponent, offset the frame by the stagger:
```tsx
const adjustedFrame = Math.max(0, frame - index * staggerFrames);
const anim = spring({ frame: adjustedFrame, fps, config: { damping: 12, stiffness: 100 } });
```

### Vertical 9:16 (Shorts/Reels/TikTok) composition
```tsx
<Composition id="Id" component={Comp} durationInFrames={450} fps={30} width={1080} height={1920} />
```
Root container must use exact pixel values, not destructured width/height from useVideoConfig.

## Rendering pipeline
1. Write the React component defining the video
2. Register it in `src/Root.tsx` as a composition
3. Run `npm run dev` to preview in Remotion Studio
4. Run `npx remotion render` to produce the final MP4

## Pitfalls
- The Remotion monorepo build fails with ESM export errors — DO NOT build it. Use `create-video` to scaffold a consumer project instead.
- Interactive CLI prompts need `printf '\n\n' | ...` piping to answer defaults non-interactively
- Use absolute dimensions (e.g., `width: 1080, height: 1920`) in the root component style rather than destructuring from `useVideoConfig()` — the latter can cause issues with Spring/Sequence animations
- `npx remotion render` downloads Chrome Headless Shell (~87MB) on first run — this is normal, takes ~10s
- Render times: ~35s for a 15-second 1080x1920 video on this machine (roughly 12 frames/sec, 2x concurrency)
- Remotion is free for teams of up to 3 (UNLICENSED in starter)
- Video rendering needs a working browser (Chromium) — the CLI handles this automatically
