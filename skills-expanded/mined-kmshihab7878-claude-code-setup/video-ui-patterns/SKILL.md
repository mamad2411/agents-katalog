---
name: video-ui-patterns
description: Reusable video UI component patterns for Remotion and programmatic video. macOS terminal mockups, announcement text, logo combos, ASCII art reveals, code typing simulations. Use when building video compositions that simulate software interfaces.
---

# Video UI Patterns

Reusable component patterns for building professional software demo videos with Remotion.

## Pattern 1: Terminal Command Demo

A terminal that types a command, shows output, then transitions away. The bread-and-butter of developer marketing videos.

### Structure
```
MacTerminal (container)
  ├── TitleBar (traffic lights + title)
  ├── TerminalContent
  │   ├── Prompt (~ $)
  │   ├── TypewriterText (command being typed)
  │   ├── Cursor (blinking/solid)
  │   └── Output (staggered lines after typing completes)
  └── Transition (flip/slide/fade away)
```

### Timing Template (8 seconds at 30fps = 240 frames)
| Phase | Frames | Duration | What Happens |
|-------|--------|----------|-------------|
| Slide in | 0-30 | 1s | Terminal springs up from below |
| Type command | 30-90 | 2s | Typewriter at 15 chars/sec |
| Pause | 90-105 | 0.5s | Cursor blinks, suspense |
| Show output | 105-160 | ~2s | Staggered lines at 50ms each |
| Hold | 160-180 | 0.7s | Let viewer read |
| Flip away | 180-210 | 1s | Terminal flips toward camera |
| Next scene | 210-240 | 1s | Logo/text reveal |

### Color Palette (Light Terminal Theme)
```
Background:     #f8fafc (soft blue-gray)
Terminal bg:    #ffffff
Title bar:      #f6f6f6
Title bar border: #e0e0e0
Title text:     #4d4d4d
Traffic lights: #ff5f57 (red), #febc2e (yellow), #28c840 (green)
Prompt ~:       #2ecc71 (green)
Terminal text:  #333333
Cursor:         #333333
Output text:    #333333
```

### Dark Terminal Variant
```
Background:     #1a1a2e
Terminal bg:    #0d1117
Title bar:      #161b22
Title bar border: #30363d
Title text:     #c9d1d9
Prompt ~:       #3fb950 (green)
Terminal text:  #c9d1d9
Cursor:         #c9d1d9
Output text:    #8b949e
```

## Pattern 2: Announcement Text

Large, bold text that scales in with easing. Used as a scene separator or headline.

```tsx
const AnnouncementText: React.FC<{ text: string }> = ({ text }) => {
  const frame = useCurrentFrame();
  const { fps } = useVideoConfig();

  const scale = interpolate(frame, [0, fps * 0.5], [0, 1], {
    extrapolateRight: "clamp",
    easing: Easing.out(Easing.cubic),
  });

  return (
    <AbsoluteFill className="flex items-center justify-center">
      <span style={{
        fontFamily: "'GT Planar', 'Inter', sans-serif",
        fontSize: 60,
        fontWeight: 700,
        color: "#333",
        transform: `scale(${scale})`,
      }}>
        {text}
      </span>
    </AbsoluteFill>
  );
};
```

## Pattern 3: Logo Combo

Multiple logos with separators. Common for "X + Y" partnership/integration videos.

```tsx
const LogoCombo: React.FC = () => (
  <AbsoluteFill className="flex items-center justify-center">
    <div className="flex items-center gap-12">
      <Img src={staticFile("logo-a.png")} className="h-32" alt="Product A" />
      <span className="text-6xl font-light text-gray-600">+</span>
      <Img src={staticFile("logo-b.svg")} className="h-24" alt="Product B" />
      <Img src={staticFile("logo-c.svg")} className="h-16" alt="Product C" />
    </div>
  </AbsoluteFill>
);
```

### Size hierarchy: Primary logo (h-32) > Secondary (h-24) > Tertiary (h-16)

## Pattern 4: ASCII Art Logo Reveal

ASCII art appears after command output, giving a retro-terminal feel.

```tsx
const SKILLS_LOGO = `███████╗██╗  ██╗██╗██╗     ██╗     ███████╗
██╔════╝██║ ██╔╝██║██║     ██║     ██╔════╝
███████╗█████╔╝ ██║██║     ██║     ███████╗
╚════██║██╔═██╗ ██║██║     ██║     ╚════██║
███████║██║  ██╗██║███████╗███████╗███████║
╚══════╝╚═╝  ╚═╝╚═╝╚══════╝╚══════╝╚══════╝`;

// Render as <pre> for monospace alignment
{showOutput && <pre className="text-[#333] text-lg">{SKILLS_LOGO}</pre>}
```

## Pattern 5: Terminal Output Lines

Simulated CLI output with unicode box-drawing characters.

```tsx
const OUTPUT_LINES = [
  "",
  "┌  skills",
  "│",
  "◇  Source: https://github.com/remotion-dev/skills.git",
  "│",
  "◇  Repository cloned",
  "│",
  "◇  Found 1 skill",
  "│",
  "●  Skill: remotion-best-practices",
  "│",
  "│  Best practices for Remotion - Video creation in React",
  "│",
  "◇  Detected 2 agents",
  "│",
  "└  Installation complete",
];
```

### Box-drawing character reference
| Char | Usage |
|------|-------|
| `┌` | Section start |
| `│` | Vertical connector |
| `└` | Section end |
| `◇` | Step completed (diamond) |
| `●` | Highlighted item (filled circle) |
| `◆` | Alternative highlight |
| `✓` | Success checkmark |
| `✗` | Failure mark |

## Composition Best Practices

1. **Separate components per file** — MacTerminal.tsx, TerminalContent.tsx, Cursor.tsx, etc.
2. **Use Sequence for timed overlapping scenes** — `<Sequence from={120}>`
3. **Use Series for sequential non-overlapping scenes** — `<Series><Series.Sequence>`
4. **Put transforms on Sequence, not on the component** — Keeps components reusable
5. **Use AbsoluteFill for full-frame positioning** — Every top-level wrapper
6. **Store logos in `public/`** — Reference with `staticFile("logo.png")`
7. **Transparent backgrounds on sub-compositions** — Only Master has the background color
8. **Font size for video: text-4xl (36px)** — Much larger than web; video text needs to be readable at smaller playback sizes

## Cross-References

- **`/remotion-animation`** — Spring physics, interpolation, 3D transforms
- **`/frontend-design`** — Web UI aesthetics (non-video)
- **`/distilled-aesthetics`** — Typography and color anti-patterns
- **`/clone-website`** — For pixel-perfect web reproduction (not video)
