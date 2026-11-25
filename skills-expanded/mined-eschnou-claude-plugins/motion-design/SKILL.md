---
name: motion-design
description: >
  Create motion design videos programmatically using Remotion (React for video). Use this skill whenever the user wants to create a video, motion graphics, animated explainer, social media video, product demo video, promotional clip, text animation video, or any kind of programmatic video content. Also trigger when the user mentions "Remotion", "motion design", "animated video", "video from code", or asks to turn content into a video. Even if the user just says "make me a video" or "create an animation" without mentioning Remotion, this skill is the right choice since Remotion is the video creation tool for this workflow. Works in Claude Code and in Cowork.
---

# Remotion Motion Design

Build motion graphics as React components, preview them as still frames, render to MP4. Targets **Remotion 4.x** (verified against 4.0.529). Works in Claude Code (local machine) and Cowork (sandbox).

## Workflow

1. **Plan**: scenes, on-screen text, duration, fps, dimensions (see Design Tips). Write the storyboard as a short list before coding.
2. **Set up** a project (or reuse the existing one).
3. **Write** one component per scene, compose them on a timeline.
4. **Check** key frames as stills and look at them (see Verify).
5. **Render** to MP4 and deliver the file to the user.

Users may edit the project between turns. If code changed in a way you did not expect, assume it was intentional; do not overwrite it.

---

## Step 1: Environment

| | Claude Code | Cowork |
|---|---|---|
| Node.js / npm | Present | Present |
| Browser for rendering | `npx remotion browser ensure` downloads one | Remotion's download is blocked; use Playwright Chromium |
| Where to build | A folder in the user's workspace (never scaffold into a folder with unrelated files; use a subfolder) | A folder in the session working directory |
| Delivering the video | Tell the user the path | Copy the final file to the outputs folder so the user can open it |

`scripts/find_browser.sh` handles the browser difference automatically and `scripts/render.sh` calls it, so the same commands work in both.

## Step 2: Project setup

Preferred: the bundled script (works everywhere, installs exact matching versions, produces a renderable starter):

```bash
bash <skill-dir>/scripts/setup_project.sh my-video
cd my-video
```

Alternative in Claude Code with a normal network: `npx create-video@latest --yes --blank --no-tailwind my-video`.

Rules that prevent most install problems:

- **All `remotion` and `@remotion/*` packages must be the exact same version** (no `^`). Add packages with `npx remotion add @remotion/<name>` so the version matches, or `npm install --save-exact`.
- Assets go in `public/` and are referenced with `staticFile("file.png")`.
- Check the installed version with `npx remotion versions`; upgrade with `npx remotion upgrade`.

Project layout:

```
my-video/
├── public/            # images, fonts, audio, video
├── src/
│   ├── index.ts       # registerRoot(RemotionRoot)
│   ├── Root.tsx       # <Composition> definitions
│   └── MyVideo.tsx    # scene components
├── package.json
└── tsconfig.json
```

Root composition (`src/Root.tsx`):

```tsx
import React from "react";
import { Composition } from "remotion";
import { MyVideo } from "./MyVideo";

export const RemotionRoot: React.FC = () => (
  <Composition
    id="MyVideo"
    component={MyVideo}
    durationInFrames={150} // 5 seconds at 30fps
    fps={30}
    width={1920}
    height={1080}
  />
);
```

## Step 3: Animation fundamentals

### Golden rule

Every animated value MUST be derived from `useCurrentFrame()`. CSS `transition`, CSS `animation`, and Tailwind animation classes do not render correctly because Remotion captures each frame independently.

Express time in seconds times fps (`0.5 * fps`), not raw frame numbers, so timing survives an fps change.

### interpolate + Easing

```tsx
import { interpolate, Easing, useCurrentFrame, useVideoConfig } from "remotion";

const frame = useCurrentFrame();
const { fps } = useVideoConfig();

const opacity = interpolate(frame, [0, 0.5 * fps], [0, 1], {
  extrapolateLeft: "clamp",   // without clamping, values run past the range
  extrapolateRight: "clamp",
  easing: Easing.bezier(0.16, 1, 0.3, 1), // strong ease-out, a good default
});
```

- Multiple keyframes: `interpolate(frame, [0, 1*fps, 9*fps, 10*fps], [0, 1, 1, 0], {...})`. Pass an `easing` array with one entry per segment (n-1 entries) to vary easing.
- Colors and units interpolate too: `["0px 0px", "100px 100px"]`, `["20deg", "90deg"]`, `["#fff", "#000"]`.
- `Easing.spring({ damping: 200 })` gives a spring curve inside `interpolate` (no bounce at 200).
- Animating **scale**: add `output: "perceptual-scale"` so growth looks even instead of slowing at larger sizes.
- Prefer the individual CSS properties `scale`, `translate`, `rotate` over a combined `transform` string; use `transform` only for `skew()`, `perspective()`, or order-sensitive chains.
- `posterize: 3` samples every 3rd frame for an intentionally choppy look.

### spring()

```tsx
import { spring } from "remotion";

const s = spring({ frame, fps, config: { damping: 12, stiffness: 200 } });
// then: style={{ opacity: s, scale: s }}
```

Presets:

- **Smooth** (reveals, backgrounds): `{ damping: 200 }` — no bounce
- **Snappy** (UI elements): `{ damping: 20, stiffness: 200 }` — minimal bounce
- **Bouncy** (playful entrances): `{ damping: 8 }` — visible bounce
- **Heavy** (weighty objects): `{ damping: 15, stiffness: 80, mass: 2 }` — slow, heavy

`spring()` also accepts `delay` and `durationInFrames`. For an exit, subtract a second spring: `enter - spring({ frame: frame - exitStart, fps, config })` goes 0 → 1 → 0.

## Step 4: Sequencing and composition

### Sequence: place things on the timeline

```tsx
import { AbsoluteFill, Sequence } from "remotion";

<AbsoluteFill>
  <Background />
  <Sequence from={30} durationInFrames={60} premountFor={fps}>
    <Title />
  </Sequence>
  <Sequence from={60} durationInFrames={60} premountFor={fps}>
    <Subtitle />
  </Sequence>
</AbsoluteFill>
```

- Inside a `<Sequence>`, `useCurrentFrame()` is **local** (starts at 0), not the global frame.
- Set `premountFor` (frames, e.g. `fps`) so images, video and fonts inside are loaded before the sequence appears.
- By default a Sequence wraps its children in an absolute-fill element. `layout="none"` removes that wrapper (use it inside `<ThreeCanvas>` or when you position children yourself), but it cannot be combined with `premountFor`.
- `<Sequence width={..} height={..}>` overrides `useVideoConfig()` for its children (nesting a differently sized composition).

### Series: back to back

```tsx
import { Series } from "remotion";

<Series>
  <Series.Sequence durationInFrames={45}><Intro /></Series.Sequence>
  <Series.Sequence durationInFrames={60}><Main /></Series.Sequence>
  <Series.Sequence offset={-15} durationInFrames={30}><Outro /></Series.Sequence>
  {/* negative offset = starts 15 frames before the previous scene ends */}
</Series>
```

### TransitionSeries: scenes with transitions

```tsx
import { TransitionSeries, linearTiming, springTiming } from "@remotion/transitions";
import { fade } from "@remotion/transitions/fade";
import { slide } from "@remotion/transitions/slide";

<TransitionSeries>
  <TransitionSeries.Sequence durationInFrames={60}><Scene1 /></TransitionSeries.Sequence>
  <TransitionSeries.Transition presentation={fade()} timing={linearTiming({ durationInFrames: 15 })} />
  <TransitionSeries.Sequence durationInFrames={60}><Scene2 /></TransitionSeries.Sequence>
  <TransitionSeries.Transition
    presentation={slide({ direction: "from-right" })}
    timing={springTiming({ config: { damping: 200 } })}
  />
  <TransitionSeries.Sequence durationInFrames={60}><Scene3 /></TransitionSeries.Sequence>
</TransitionSeries>
```

- Presentations: `fade`, `slide` (`from-left|right|top|bottom`), `wipe`, `flip`, `clockWipe` (from `@remotion/transitions/clock-wipe`).
- **Transitions shorten the timeline** because scenes overlap: 60 + 60 with a 15-frame transition = 105 frames. Set the composition's `durationInFrames` to `sum(scenes) - sum(transitions)`. Get a transition's length with `timing.getDurationInFrames({ fps })` (needed for `springTiming` without an explicit duration).
- `<TransitionSeries.Overlay durationInFrames={n}>` renders an effect over a cut without shortening the timeline. An overlay cannot sit next to a transition or another overlay.

## Step 5: Assets

```tsx
import { staticFile, Img } from "remotion";
import { Audio, Video } from "@remotion/media"; // Audio and Video come from @remotion/media

<Img src={staticFile("logo.png")} />          // waits for the image to load; remote URLs work too
<Video src={staticFile("clip.mp4")} />
<Audio src={staticFile("music.mp3")} volume={0.5} />
```

Install the package first if missing: `npx remotion add @remotion/media`.

Audio props (`Audio` / `Video`): `from` (delay, in frames), `trimBefore` / `trimAfter` (frames), `playbackRate`, `muted`, `loop`, `volume` (number, or `(f) => number` where `f` counts from when the audio starts), `toneFrequency` (pitch 0.01–2, render only, not in preview).

```tsx
<Audio
  src={staticFile("bgm.mp3")}
  volume={(f) => interpolate(f, [0, 1 * fps], [0, 1], { extrapolateRight: "clamp" })}
/>
```

Animated GIF/WebP/APNG/AVIF: `<AnimatedImage src={staticFile("x.gif")} />` from `remotion` (Chrome). Otherwise `@remotion/gif`.

### Fonts

```tsx
import { loadFont } from "@remotion/google-fonts/Inter";

const { fontFamily } = loadFont("normal", { weights: ["400", "700"], subsets: ["latin"] });
// style={{ fontFamily }}
```

Loading blocks rendering until the font is ready. Restrict weights/subsets to keep it small. Google Fonts need network access at render time; if the sandbox is offline, put a font file in `public/` and load it with `@remotion/fonts` (`loadFont({ family, url: staticFile("font.woff2") })`) or fall back to system fonts.

## Step 6: Text animation

Typewriter — slice the string; never fade individual characters:

```tsx
const TypeWriter: React.FC<{ text: string }> = ({ text }) => {
  const frame = useCurrentFrame();
  const chars = Math.floor(
    interpolate(frame, [0, text.length * 2], [0, text.length], { extrapolateRight: "clamp" }),
  );
  return <span>{text.slice(0, chars)}</span>;
};
```

Staggered words:

```tsx
const words = "Motion Design is Fun".split(" ");
<div style={{ display: "flex", gap: 16 }}>
  {words.map((word, i) => {
    const s = spring({ frame: frame - i * 5, fps, config: { damping: 12 } });
    return (
      <span key={i} style={{ opacity: s, translate: `0px ${(1 - s) * 30}px` }}>{word}</span>
    );
  })}
</div>
```

Video-first text sizing: text is watched at a distance, so headlines are typically 80–160px on a 1920×1080 canvas and body text no smaller than ~40px. Use `@remotion/layout-utils` (`fitText`, `measureText`) to fit text to a box.

## Step 7: Verify, then render

### Look at frames before rendering the full video

Rendering stills is cheap. Render key frames (start, mid-animation, end of each scene) and view them:

```bash
bash <skill-dir>/scripts/render.sh MyVideo out/f30.png --still --frame=30
```

Or several at once: `npx remotion render MyVideo out/frames --frames=0,45,90,140 --image-format=png`. Open the PNGs with the image viewer/Read tool and check layout, contrast, text overflow, and that nothing is blank. In Claude Code you can also run `npx remotion studio --no-open` and open the printed URL for an interactive preview.

### Render

```bash
bash <skill-dir>/scripts/render.sh MyVideo out/video.mp4
```

Only render the full video when the user wants a deliverable; renders are the slow step.

Useful options (pass after the output path):

- `--codec=h264` (default for .mp4); `--crf=18` quality (lower = better; 18 is visually lossless)
- `--pixel-format=yuv420p` best player compatibility
- `--concurrency=2` parallel frames (raise if the machine allows; lower if it runs out of memory)
- `--image-format=jpeg` faster than png when no transparency is needed
- `--props='{"title":"Custom"}'` override input props of a parameterized composition
- Transparent video, audio visualization, dynamic metadata, 3D, captions, GIF/Lottie: see `references/advanced-patterns.md`.

## Design tips

- **Timing**: most reveals feel right at 0.5–1 s. Keep animations under 2 s unless deliberate. Hold each key message on screen long enough to read it twice.
- **Easing**: springs and bezier curves for organic motion; avoid plain linear except for constant-speed things (progress bars, rotation).
- **Contrast**: dark background with bright text reads best. No light gray on white.
- **Spacing**: generous padding; keep important content inside a ~5–8% safe margin, especially for portrait social formats.
- **Frame rate**: 30fps standard; 60fps only for fast motion.
- **Sizes**: 1920×1080 landscape, 1080×1920 portrait/stories, 1080×1080 square. Derive positions from `useVideoConfig()` width/height rather than hard-coding pixels when a composition must support multiple sizes.
- **Structure**: one component per scene; shared design tokens (colors, fonts, spacing) in one file.

## Troubleshooting

| Problem | Solution |
|---------|----------|
| "Chrome not found" / browser download fails | Run `bash <skill-dir>/scripts/find_browser.sh`; if it prints a path, add `--browser-executable="<path>"` (render.sh does this for you) |
| Version mismatch errors between Remotion packages | Make every `remotion` / `@remotion/*` version identical and exact; `npx remotion versions` shows mismatches, `npx remotion upgrade` fixes them |
| CSS animations don't play | Replace with `useCurrentFrame()` + `interpolate()` / `spring()` |
| Assets not loading | Put them in `public/`, reference with `staticFile()` |
| Blank frames | Make sure the component returns visible content for every frame range; check `Sequence` `from`/`durationInFrames` |
| `Audio` / `Video` not found in `remotion` | Import them from `@remotion/media` (`npx remotion add @remotion/media`) |
| Font looks wrong in render | Use `loadFont()` at module top level so rendering waits for it; check network access for Google Fonts |
| Render runs out of memory | Lower `--concurrency`; lower resolution while iterating |
| Total length is shorter than expected | Transitions overlap scenes; subtract them from `durationInFrames` |

## Licensing note

Remotion is free for individuals, non-profits, and for-profit companies with up to 3 employees; larger for-profit companies need a Remotion company license (https://www.remotion.dev/license). Mention this to the user when the video is for commercial use inside a larger company.

## More Remotion APIs

This file covers the common path. For anything else, read the current docs: append `.md` to a docs page URL (for example `https://www.remotion.dev/docs/cli/render.md`) or start from `https://www.remotion.dev/llms.txt`. Remotion also publishes official agent skills (`npx skills add remotion-dev/skills`) with deeper rule files for maps, captions, effects, and SaaS/Lambda rendering. See `references/advanced-patterns.md` for patterns bundled with this skill.
