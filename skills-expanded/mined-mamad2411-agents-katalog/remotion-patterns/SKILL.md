---
name: remotion-patterns
description: Programmatic video with Remotion and React — compositions, sequences, spring animations, audio sync, SSR render, preview vs production render, and TypeScript project structure. Use when building code-driven explainers, UI demos, templated exports, or repeatable motion systems.
---

# Remotion Patterns

Remotion treats video as a **function of frame index**. Favor deterministic layouts, memoized calculations, and explicit timing over DOM-measured layout in render. Preview in Studio; trust SSR render for pixels.

## When Invoked

1. Confirm output spec: resolution, fps, duration in frames, codec, and whether audio is embedded.
2. Scaffold or align to existing Remotion project structure (Phase 1).
3. Build with **frame-derived state** — no `useEffect` for layout that affects visuals at render time.
4. Run preview smoke, then production render with concurrency settings from Phase 6.

## Phase 1: TypeScript Project Structure

Recommended layout:

```text
src/
  remotion/
    Root.tsx              # registerRoot, composition list
    compositions/
      LaunchVideo.tsx     # single entry composition
    scenes/
      IntroScene.tsx
      DemoScene.tsx
    components/
      TitleCard.tsx
      DeviceFrame.tsx
    lib/
      timing.ts           # seconds → frames helpers
      theme.ts            # colors, typography constants
      springs.ts          # shared spring configs
  assets/                 # static imports (images, fonts)
```

**Root.tsx responsibilities:**

- `registerRoot(() => <RemotionRoot />)`
- Each `<Composition>` declares `id`, `component`, `durationInFrames`, `fps`, `width`, `height`, `defaultProps`

**Props typing:**

```typescript
export type LaunchVideoProps = {
  headline: string;
  ctaUrl: string;
  accentColor: string;
};

export const defaultLaunchVideoProps: LaunchVideoProps = {
  headline: "Ship faster",
  ctaUrl: "https://example.com",
  accentColor: "#6366f1",
};
```

Pass props from CLI `--props='{"headline":"..."}'` for batch renders.

## Phase 2: Compositions and Sequences

### Composition boundaries

One **Composition** = one renderable output file (or variant). Use `defaultProps` for theming; duplicate compositions only when dimensions/fps differ — not for every copy tweak.

### Sequence pattern

Nest `<Sequence from={startFrame} durationInFrames={dur}>` for scenes.

```tsx
<AbsoluteFill>
  <Sequence from={0} durationInFrames={90}>
    <IntroScene title={headline} />
  </Sequence>
  <Sequence from={90} durationInFrames={210}>
    <DemoScene />
  </Sequence>
</AbsoluteFill>
```

**Rules:**

- Scene components assume **local frame 0** at their Sequence start — use `useCurrentFrame()` inside Sequence context
- For global timeline debugging, pass `startFrame` as prop if needed
- Hard-code durations in `timing.ts` as named constants (`INTRO_FRAMES = 3 * fps`)

### Series and transitions

Prefer explicit Sequence cuts for clarity. For crossfades, overlap Sequences and interpolate opacity on shared layers — avoid mystery transition plugins until needed.

## Phase 3: Animation — Springs and Interpolation

### Prefer springs for UI motion

```typescript
import { spring, useCurrentFrame, useVideoConfig } from "remotion";

const frame = useCurrentFrame();
const { fps } = useVideoConfig();
const progress = spring({
  frame,
  fps,
  config: { damping: 200, stiffness: 100 },
});
```

Centralize configs in `lib/springs.ts`:

| Preset | Use | Feel |
|--------|-----|------|
| `snappy` | Titles entering | Fast settle |
| `gentle` | Background parallax | Soft |
| `heavy` | Large panels | Weight |

### interpolate with clamp

```typescript
import { interpolate, Easing } from "remotion";

const opacity = interpolate(frame, [0, 15], [0, 1], {
  extrapolateLeft: "clamp",
  extrapolateRight: "clamp",
  easing: Easing.out(Easing.quad),
});
```

**Anti-pattern:** unclamped interpolate causing values to drift after segment end — always clamp scene-local interpolations.

### Layout thrash avoidance

| Do | Don't |
|----|-------|
| Fixed width/height on containers | Measuring DOM with `getBoundingClientRect` per frame |
| `AbsoluteFill` + flex with constants | Auto layout that reflows when fonts load mid-render |
| Preload fonts via `@remotion/google-fonts` or static `@font-face` | System font fallback that changes metrics |
| Transform/opacity for motion | Animating `width`/`height` every frame on large subtrees |

For text that must fit, compute font size from char count **once** from props (deterministic formula), not binary search in browser at render.

## Phase 4: Audio Sync

### Import audio

Place audio in `public/` or import with static file handling; use `<Audio src={staticFile("vo.mp3")} />` inside the composition tree.

### Align to frames

```typescript
const { fps } = useVideoConfig();
const beatFrames = 120; // frame 120 = 4s at 30fps
```

Use **waveform metadata** or known VO script timing:

- Mark scene `from` values to VO phrase starts
- Optional: `visualizeAudio()` or precomputed peak array for reactive elements (keep arrays in module scope, not fetched async per frame)

### Length discipline

Composition `durationInFrames` must cover full audio tail + fade-out (e.g. +15 frames). Short master → truncated CTA; long master → black tail.

## Phase 5: Preview vs Render

| Mode | Purpose | Notes |
|------|---------|-------|
| Studio preview | Scrub timeline, fast iteration | May differ slightly in font loading timing — fix fonts for parity |
| `@remotion/renderer` SSR | Production pixels | No React concurrent surprises if pure frame functions |
| `--frames=0-30` partial | Debug single scene | Faster than full re-render |

**Checklist before full render:**

- [ ] `npx remotion compositions` lists expected ids
- [ ] Props JSON validates against TypeScript types
- [ ] No `Math.random()` without `random()` seed from `@remotion/media-utils` or fixed seed
- [ ] No network fetch in render unless cached via `delayRender/continueRender`
- [ ] Images use `staticFile` or static import

### delayRender pattern for async assets

```typescript
import { delayRender, continueRender, cancelRender } from "remotion";

const handle = delayRender("loading-data");
fetch(url)
  .then((r) => r.json())
  .then((data) => { /* store in ref */ continueRender(handle); })
  .catch((e) => cancelRender(e));
```

Prefer **static imports** over fetch for reproducible CI renders.

## Phase 6: SSR Render and Ops

### CLI render

```bash
npx remotion render src/remotion/Root.tsx LaunchVideo out/launch.mp4 \
  --codec=h264 --crf=18 --props='{"headline":"Hello"}'
```

### Concurrency

- Local: `--concurrency=50%` or fixed CPU count
- CI: set concurrency from vCPU; watch memory on 4K compositions

### Output formats

| Format | When |
|--------|------|
| H.264 MP4 | Default delivery |
| ProRes | Further edit in NLE |
| PNG sequence | Complex post pipeline |
| WebM VP9 | Web embeds |

### Lambda / cloud (optional)

When using Remotion Lambda: bundle size limits, same props contract, store renders in S3 with versioned keys.

## Quality Rubric (code review, 0–100)

| Dimension | Weight | Criteria |
|-----------|--------|----------|
| Determinism | 25 | Same frame → same pixels; no unseeded random |
| Structure | 20 | Scenes isolated; timing constants centralized |
| Performance | 20 | No layout thrash; reasonable render time per minute of video |
| A11y/captions | 10 | Captions as data-driven layers if required |
| Audio | 15 | No pops; duration matches |
| Maintainability | 10 | Typed props; reusable components |

Ship at ≥80.

## Testing and CI

```bash
# Still frame snapshot (visual regression)
npx remotion still src/remotion/Root.tsx LaunchVideo out/frame-120.png --frame=120

# Short render smoke
npx remotion render src/remotion/Root.tsx LaunchVideo /tmp/smoke.mp4 --frames=0-60
```

Commit stills for hero frames only — not whole video binaries.

## Output Template

```markdown
# Remotion Build Spec — {composition id}
Date: {date}
Composition: {id}
Size: {width}x{height} @ {fps} fps
Duration: {frames} frames ({seconds}s)

## Props schema
{typescript or JSON schema}

## Scene map
| Scene | from frame | duration | component |
|-------|------------|----------|-----------|

## Assets
- fonts: 
- audio: 
- images: 

## Render command
{full CLI}

## Preview vs prod deltas
- 

## QC
- [ ] Determinism check
- [ ] Audio tail
- [ ] CRF/quality approved
- [ ] Smoke render passed
```

## Anti-Patterns

- `useEffect` + `setState` driving visible layout each frame
- Fetching fonts from Google CDN at render time without delayRender
- One 2000-line composition file — split scenes
- Hard-coded fps math scattered (`* 30` everywhere) — use `useVideoConfig().fps`
- Animating box-shadow and blur on full-screen layers (slow render)
- Preview-only `@media` CSS that SSR ignores
- Embedding secrets in props JSON committed to git
- Using Remotion for long generative AI clips — splice in post (`ai-video-gen`)
- `window` / `document` access without `'use client'` guards and fallbacks for SSR

## Workflow Integration

```
remotion-patterns (this skill)
    ← product-launch-video (spec, CTA, platform sizes)
    ↔ ai-video-gen (export generative segments to concat)
    ↔ frontend-design (motion matches brand tokens)
```

## Cross-References

| Skill | Relationship |
|-------|--------------|
| `product-launch-video` | Brief, hook timing, export matrix |
| `ai-video-gen` | Generative b-roll outside deterministic UI |
| `ai-image-gen` | Static assets imported into compositions |
| `frontend-design` | Typography and color tokens in `theme.ts` |
