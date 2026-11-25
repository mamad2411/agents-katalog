---
name: remotion-animation
description: Remotion video animation patterns from JonnyBurger's workflow. Spring physics, typewriter effects, 3D transforms, staggered reveals, flip transitions, composition architecture. Use when building Remotion compositions or programmatic video animations.
---

# Remotion Animation Patterns

Extracted from Jonny Burger's (Remotion creator) Claude Code session building a skills announcement video. These are production-quality Remotion patterns.

## Core Architecture

### Composition Hierarchy
```
Root.tsx          — Registers all compositions with dimensions/fps/duration
  Master.tsx      — Top-level orchestrator with background + sequences
    Sequence A    — First scene (e.g., terminal animation)
    Sequence B    — Second scene (e.g., logo reveal)
  SubComponent    — Reusable UI elements (terminal, cursor, text)
```

### Key Imports
```tsx
import {
  AbsoluteFill,     // Full-frame positioning
  Sequence,         // Timed scene placement (from/durationInFrames)
  Series,           // Sequential scenes (auto-positioned)
  useCurrentFrame,  // Current frame number
  useVideoConfig,   // fps, durationInFrames, width, height
  interpolate,      // Frame-based value interpolation
  spring,           // Physics-based spring animation
  Easing,           // Easing functions for interpolate
  Img,              // Image component
  staticFile,       // Reference to public/ assets
} from "remotion";
```

## Animation Techniques

### 1. Spring Animation (No Bounce)
High damping prevents bounce. Use for slide-in, scale-up, or any entry animation.
```tsx
const slideIn = spring({
  frame,
  fps,
  config: {
    damping: 200,   // High = no bounce (default 10 = bouncy)
    stiffness: 100, // Controls speed (higher = faster)
  },
});
const translateY = interpolate(slideIn, [0, 1], [700, 0]);
```

### 2. Typewriter Effect
Character-by-character text reveal at controlled speed.
```tsx
const command = "npx skills add remotion-dev/skills";
const charsPerSecond = 15;
const framesPerChar = fps / charsPerSecond;
const typingEndFrame = command.length * framesPerChar;

const visibleChars = Math.floor(
  interpolate(frame, [0, typingEndFrame], [0, command.length], {
    extrapolateRight: "clamp",
  })
);
const displayedText = command.slice(0, visibleChars);
const isTyping = visibleChars < command.length;
```

### 3. Blinking Cursor
Toggles visibility on a 0.5s cycle. Solid while typing, blinking when idle.
```tsx
const Cursor: React.FC<{ blinking: boolean }> = ({ blinking }) => {
  const frame = useCurrentFrame();
  const { fps } = useVideoConfig();
  const blinkCycle = Math.floor(frame / (fps * 0.5)) % 2;
  const opacity = blinking ? (blinkCycle === 0 ? 1 : 0) : 1;
  return (
    <span
      className="w-4 h-10 bg-[#333] ml-0.5 inline-block"
      style={{ opacity }}
    />
  );
};
```

### 4. Staggered Line Reveal
Lines appear one at a time at a fixed interval (e.g., 50ms per line).
```tsx
const framesPerLine = fps * 0.05; // 50ms per line
const linesStartFrame = outputStartFrame + framesPerLine;
const visibleLines = Math.floor(
  interpolate(
    frame,
    [linesStartFrame, linesStartFrame + OUTPUT_LINES.length * framesPerLine],
    [0, OUTPUT_LINES.length],
    { extrapolateLeft: "clamp", extrapolateRight: "clamp" }
  )
);
// Render: OUTPUT_LINES.slice(0, visibleLines).map(...)
```

### 5. 3D Perspective Transform
Gentle 3D rotation with perspective for depth. Animate rotateY over time for a slow pan effect.
```tsx
// Parent needs perspective
<AbsoluteFill style={{ perspective: 1000 }}>
  <Sequence
    style={{
      transform: `translateY(${translateY}px) rotateX(20deg) rotateY(${rotateY}deg) scale(${scale})`,
    }}
  >
    <Component />
  </Sequence>
</AbsoluteFill>

// Slow Y rotation over full duration
const rotateY = interpolate(frame, [0, durationInFrames], [10, -10]);
```

### 6. Flip-Away Transition
Terminal flips toward camera by rotating X axis. Transform origin at bottom edge.
```tsx
const flipOut = spring({
  frame: frame - OUTPUT_DONE_FRAME,
  fps,
  config: { damping: 200, stiffness: 100 },
});

const flipRotateX = frame >= OUTPUT_DONE_FRAME
  ? interpolate(flipOut, [0, 1], [0, -90])
  : 0;

// Wrapper with bottom transform origin
<div style={{ perspective: 1000 }}>
  <div style={{
    transformOrigin: "center bottom",
    transform: `rotateX(${flipRotateX}deg)`,
  }}>
    <MacTerminal />
  </div>
</div>
```

### 7. Scale Animation with Easing
Scale from 0 to 1 with ease-out curve for text reveals.
```tsx
const scale = interpolate(frame, [0, fps * 0.5], [0, 1], {
  extrapolateRight: "clamp",
  easing: Easing.out(Easing.cubic),
});
```

### 8. Gradual Scale Drift
Subtle scale increase over the full composition for cinematic feel.
```tsx
const scale = interpolate(frame, [0, durationInFrames], [0.9, 1]);
```

## UI Component Patterns

### macOS Terminal Window
```tsx
<AbsoluteFill className="p-8">
  <div className="w-full h-full flex flex-col rounded-xl overflow-hidden shadow-2xl">
    {/* Title bar */}
    <div className="h-14 bg-[#f6f6f6] flex items-center px-5 border-b border-[#e0e0e0]">
      <div className="flex gap-2.5">
        <div className="w-4 h-4 rounded-full bg-[#ff5f57]" />
        <div className="w-4 h-4 rounded-full bg-[#febc2e]" />
        <div className="w-4 h-4 rounded-full bg-[#28c840]" />
      </div>
      <div className="flex-1 text-center">
        <span className="text-[#4d4d4d] text-base font-medium">Terminal</span>
      </div>
      <div className="w-16" />
    </div>
    {/* Content */}
    <div className="flex-1 bg-white p-6 font-mono text-4xl">
      <TerminalContent />
    </div>
  </div>
</AbsoluteFill>
```

### Logo Combo with Series
```tsx
<Series>
  <Series.Sequence durationInFrames={60}>
    <AnnouncementText />  {/* 2s text with scale animation */}
  </Series.Sequence>
  <Series.Sequence durationInFrames={120}>
    <Logos />  {/* Logo images with + separator */}
  </Series.Sequence>
</Series>
```

## Composition Defaults

| Property | Recommended |
|----------|------------|
| fps | 30 |
| width | 1080 |
| height | 700 (16:10-ish) |
| duration | 240 frames (8s) |
| padding | p-8 (32px) for terminal |
| perspective | 1000 for 3D effects |
| spring damping | 200 (no bounce) or 10-20 (bouncy) |
| stagger interval | 50ms per element |
| typing speed | 15 chars/second |
| blink cycle | 500ms |

## Workflow Pattern

1. Start with composition dimensions and root setup
2. Build static UI components first (no animation)
3. Add typewriter/reveal animations
4. Extract reusable components (cursor, content) to separate files
5. Add 3D transforms and spring physics
6. Compose scenes with Sequence/Series in a Master component
7. Fine-tune timing, scale, rotation values iteratively
8. Render with `npx remotion render <CompositionId> out/video.mp4`

## Cross-References

- **`/frontend-design`** — For non-video frontend aesthetics
- **`/distilled-aesthetics`** — Anti-AI-slop typography and color choices
- **`/fixing-motion-performance`** — CSS animation performance (non-Remotion)
- **`/interface-design`** — For dashboard/app UI patterns
