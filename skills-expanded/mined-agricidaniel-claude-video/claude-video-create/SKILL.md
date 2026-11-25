---
name: claude-video-create
description: >
  Programmatic video creation using Remotion (React-based). Generates title cards,
  data visualizations, motion graphics, branded intros/outros, animated text,
  and template-based videos from data. Claude writes React components, Remotion
  renders them headlessly to video. Use when user says "create video", "title card",
  "intro", "outro", "motion graphics", "animated text", "data visualization video",
  "remotion", "programmatic video", or "generate video from data".
allowed-tools:
  - Bash
  - Read
  - Write
  - Edit
---

# claude-video-create — Programmatic Video via Remotion

## Pre-Flight

1. Check Node.js: `node --version` (requires 18+)
2. Check if Remotion is available: `npx remotion --version 2>/dev/null`
3. If no Remotion project exists, scaffold one first

## When to Use Remotion vs FFmpeg

**Use Remotion for**:
- Complex text animations (spring physics, staggered reveals, typewriter effects)
- Data-driven videos (charts, graphs, dashboards from JSON/CSV)
- React component-based templates (reusable, parameterized)
- Branded intros/outros with motion graphics
- Content that updates from data (weekly reports, scorecards)

**Use FFmpeg for** (route to other sub-skills):
- Transcoding, trimming, concatenation
- Simple text overlay (drawtext is sufficient)
- Audio processing
- Anything that doesn't need programmatic rendering

## Scaffold a New Project

```bash
# Create new Remotion project
npx create-video@latest --template blank my-video-project
cd my-video-project
npm install
```

This creates a standard Remotion project with:
- `src/Root.tsx` — Composition registry
- `src/` — Component directory
- `remotion.config.ts` — Rendering configuration
- `package.json` — Dependencies

## Core Concepts

**Composition**: A video definition with width, height, fps, and duration.
**Component**: A React component that receives `useCurrentFrame()` and renders for that frame.
**Sequence**: A timed sub-section within a composition.
**Spring**: Physics-based animation for natural motion.

## Example: Title Card

Claude should generate this component:

```tsx
// src/TitleCard.tsx
import { AbsoluteFill, useCurrentFrame, useVideoConfig, spring, interpolate } from 'remotion';

export const TitleCard: React.FC<{ title: string; subtitle?: string }> = ({ title, subtitle }) => {
  const frame = useCurrentFrame();
  const { fps } = useVideoConfig();

  const titleScale = spring({ frame, fps, config: { damping: 12 } });
  const subtitleOpacity = interpolate(frame, [20, 40], [0, 1], { extrapolateRight: 'clamp' });

  return (
    <AbsoluteFill style={{ backgroundColor: '#0a0a0a', justifyContent: 'center', alignItems: 'center' }}>
      <h1 style={{
        color: 'white',
        fontSize: 80,
        fontFamily: 'Inter, sans-serif',
        transform: `scale(${titleScale})`,
      }}>
        {title}
      </h1>
      {subtitle && (
        <p style={{
          color: '#888',
          fontSize: 32,
          opacity: subtitleOpacity,
          marginTop: 20,
        }}>
          {subtitle}
        </p>
      )}
    </AbsoluteFill>
  );
};
```

Register in Root.tsx:
```tsx
import { Composition } from 'remotion';
import { TitleCard } from './TitleCard';

export const RemotionRoot: React.FC = () => (
  <Composition
    id="TitleCard"
    component={TitleCard}
    durationInFrames={90}
    fps={30}
    width={1920}
    height={1080}
    defaultProps={{ title: "My Video", subtitle: "A subtitle" }}
  />
);
```

## Render to Video

```bash
# Render a specific composition
npx remotion render src/index.ts TitleCard output.mp4 \
  --props='{"title":"Hello World","subtitle":"Made with claude-video"}' \
  --codec h264 --crf 18

# Render as transparent (for overlays)
npx remotion render src/index.ts TitleCard output.webm \
  --props='{"title":"Overlay Text"}' \
  --codec vp8 --image-format png

# Render specific frames (for thumbnails)
npx remotion still src/index.ts TitleCard thumbnail.png \
  --props='{"title":"Thumbnail"}' --frame 45
```

## Common Patterns

### Data-Driven Video (JSON input)

```tsx
// Claude generates this based on user's data
const data = [
  { label: "Q1", value: 100 },
  { label: "Q2", value: 200 },
  { label: "Q3", value: 150 },
  { label: "Q4", value: 300 },
];

// Render with:
npx remotion render src/index.ts BarChart output.mp4 \
  --props='{"data":[{"label":"Q1","value":100},{"label":"Q2","value":200}]}'
```

### Animated Text Sequence

```tsx
import { Sequence } from 'remotion';

// Show text lines one by one
const lines = ["First line", "Second line", "Third line"];
return (
  <AbsoluteFill>
    {lines.map((line, i) => (
      <Sequence from={i * 30} durationInFrames={60} key={i}>
        <AnimatedLine text={line} />
      </Sequence>
    ))}
  </AbsoluteFill>
);
```

### Branded Intro/Outro Template

Claude generates a reusable template with:
- Logo animation (scale + fade in)
- Title text with spring animation
- Subtitle with delayed fade
- Background gradient or solid color
- Configurable via props (logo URL, colors, text)

## Rendering Options

| Flag | Purpose | Example |
|------|---------|---------|
| `--codec` | Output codec | h264, h265, vp8, vp9 |
| `--crf` | Quality (lower = better) | 18 |
| `--image-format` | Frame format | jpeg, png (png for transparency) |
| `--scale` | Resolution multiplier | 0.5 (half), 2 (double) |
| `--every-nth-frame` | Skip frames (preview) | 2 |
| `--concurrency` | Parallel rendering threads | 4 |
| `--props` | JSON props to composition | '{"title":"Hello"}' |

## Workflow Integration

After Remotion renders a video, pipe it into other claude-video sub-skills:
1. Create title card with Remotion → concat with main video (edit sub-skill)
2. Create data viz with Remotion → add captions (caption sub-skill)
3. Create intro + outro → sandwich around edited content → export for platform

## Limitations

- Requires Node.js 18+ and Chrome Headless Shell
- Rendering is slower than FFmpeg (screenshot per frame)
- First render downloads Chrome Headless (~200MB)
- Remotion licensing: free for individuals, paid for companies with 4+ employees
- Not suitable for simple operations (use FFmpeg directly for those)

## Reference

Load `references/remotion.md` for Remotion API patterns, component architecture, and rendering configuration.
