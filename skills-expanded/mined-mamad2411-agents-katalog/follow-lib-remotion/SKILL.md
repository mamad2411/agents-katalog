---
name: follow-lib-remotion
description: Use Remotion v4 to create programmatic videos with React and render via CLI
argument-hint: "[composition-or-task]"
related:
  - edit-video-with-remotion
  - follow-lib-react
  - follow-lib-zod

---

## Goal

Use Remotion v4 (latest ~4.0.524) to create programmatic videos with React, frame-based animations, and render via CLI or cloud

## Scope

Used for:
- Creating programmatic videos with React components (`<Composition>` model)
- Animations with `useCurrentFrame()` and `interpolate()`
- Type-safe props with a Zod schema
- Rendering videos, GIFs, image sequences via CLI or cloud (Lambda, Cloud Run, Vercel)

- Latest: `remotion@4.0.527` (verified 2026-09-24)
- It is React-based — use `/follow-lib-react` for component patterns and `/follow-lib-zod` for prop schemas
- References: [apis](references/apis.md) | [cli](references/cli.md) 
## Execute

### 1. Create Project

> Goal: scaffold a Remotion project with `create-video`

```bash
bunx create-video@latest --yes --blank my-video
# or skip TailwindCSS
bunx create-video@latest --yes --blank --no-tailwind my-video

cd my-video
bun install
```

- `--yes` is non-interactive mode (requires a template flag and directory)
- `--blank` uses the blank template
- `--no-tailwind` skips the Tailwind install
- `--tmp` creates in a temp directory

### 2. Start Studio

> Goal: open Remotion Studio for preview

```bash
bunx remotion studio --no-open
# or
bun run dev
```

- `bunx remotion preview` is deprecated; use `remotion studio`
- Press `s` in the terminal to reopen the browser
- `--disable-interactivity` is used for debugging

### 3. Build Composition

> Goal: create a Composition with frame-based animation

Example `src/Root.tsx`:

```tsx
import { Composition } from 'remotion';
import { MyComp } from './MyComp';

export const RemotionRoot = () => (
  <Composition
    id="MyComp"
    component={MyComp}
    durationInFrames={150}
    fps={30}
    width={1920}
    height={1080}
    defaultProps={{ title: 'Hello' }}
  />
);
```

In the component:

```tsx
import { useCurrentFrame, interpolate } from 'remotion';

export const MyComp = ({ title }) => {
  const frame = useCurrentFrame();
  const opacity = interpolate(frame, [0, 30], [0, 1], {
    extrapolateRight: 'clamp',
  });
  return <div style={{ opacity }}>{title}</div>;
};
```

### 4. Type-safe Props With Zod

> Goal: type-safe props with a Zod schema

```bash
bun add zod @remotion/zod-types
```

```tsx
import { z } from 'zod';
import { Composition } from 'remotion';
import { zColor } from '@remotion/zod-types';

const mySchema = z.object({
  title: z.string(),
  color: zColor(),
});

type MyProps = z.infer<typeof mySchema>;

export const RemotionRoot = () => (
  <Composition
    id="MyComp"
    component={MyComp}
    durationInFrames={150}
    fps={30}
    width={1920}
    height={1080}
    schema={mySchema}
    defaultProps={{ title: 'Hello', color: '#000000' }}
  />
);

const MyComp: React.FC<MyProps> = ({ title, color }) => {
  const frame = useCurrentFrame();
  return <div style={{ color, opacity: frame / 100 }}>{title}</div>;
};
```

- If you don't need complex validation, `defaultProps` alone works (Studio infers basic controls since v4.0.521)
- Use a schema when you need constraints, choices, descriptions, or specialized controls

### 5. Use Assets And Media

> Goal: use static assets and media in a composition

```tsx
import { staticFile, Img, OffthreadVideo } from 'remotion';

const img = staticFile('/my-image.png');
const video = staticFile('/video.mp4');

<Img src={img} />
<OffthreadVideo src={video} />
```

- Use `staticFile()` for files in `public/`
- For large videos use `<OffthreadVideo>` or `<Video>` from `@remotion/media`
- Use `trimBefore`/`trimAfter` instead of the deprecated `startFrom`/`endAt`

### 6. Render Video

> Goal: render video/GIF/image sequence via CLI

```bash
# render video with the default entry point
bunx remotion render MyComp

# specify entry point and output
bunx remotion render src/index.tsx MyComp out/video.mp4

# set codec, fps, size
bunx remotion render MyComp --codec=h264 --fps=30 --width=1920 --height=1080
```

Render GIF:

```bash
bunx remotion render MyComp --codec=gif --every-nth-frame=2 --number-of-gif-loops=0
```

Render image sequence:

```bash
bunx remotion render MyComp --sequence
```

### 7. Test, Debug, And Iterate

> Goal: test in Studio before real renders

- test in Remotion Studio before rendering
- use `--props props.json` for input props (on Windows use a file instead of inline JSON)
- use `--repro` to record state for debugging
- use `--log=verbose` when you need more logs

### 8. Cloud Rendering

> Goal: pick the cloud rendering option per scale

- Use `@remotion/lambda` (AWS), `@remotion/cloudrun` (GCP), or `@remotion/vercel` per platform — see details at docs.remotion.dev

### Workflows

- Setup project — `create-video`, Composition, Studio smoke test → `workflows/setup-remotion/SKILL.md`
- Render performance, codecs/flags, Lambda notes → `workflows/optimize-render/SKILL.md`

## Rules

### 1. Animation

- Always use `useCurrentFrame()` — don't use CSS animations
- Use `interpolate()` for smooth transitions
- Use `spring()` for physics-based motion
- Use `extrapolateLeft/Right: 'clamp'` to stop values outside the range
- Use `output: 'perceptual-scale'` for scale interpolation (v4.0.521+)

### 2. Type Safety

- Use a Zod schema for props when validation/controls are needed
- Convert seconds to frames — use `time * fps`
- Use `z.infer<typeof schema>` for the TypeScript type

### 3. Assets And Performance

- Use `staticFile()` for assets in `public/`
- Use `<OffthreadVideo>` or `<Video>` from `@remotion/media` for large videos
- Optimize assets before rendering
- Avoid `defaultProps` with large payloads

### 4. Composition

- Specify `durationInFrames`, `fps`, `width`, `height` clearly
- Provide `defaultProps` as an inline object literal so Studio can infer controls
- Use `lazyComponent` when you want lazy loading

### 5. Workflow

- test in Studio before rendering
- use `--no-open` for remote/CI
- render with a suitable `--codec` (`h264`, `h265`, `vp9`, `gif`, `png`)
- use `/edit-video-with-remotion` for editing video from existing footage
- use `/follow-lib-react` or `/follow-lib-zod` if needed

- See best-practices/ for recommended patterns and pitfalls

## Expected Outcome

- Programmatic videos built with React
- Smooth and consistent animations
- Automated and flexible programmatic video creation
- Scalable cloud rendering
- Type-safe components with Zod
