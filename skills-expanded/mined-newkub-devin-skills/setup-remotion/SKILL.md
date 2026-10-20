---
name: follow-lib-remotion-setup-remotion
description: Setup Remotion — create-video, Composition, Studio smoke test
argument-hint: "[project-name]"
related:
  - follow-lib-remotion
  - run-install
  - run-dev
  - resolve-errors
---

## Goal

Set up a Remotion project — `create-video`, the `<Composition>` setup, and a Studio smoke test

## Scope

Use when creating a new Remotion project or setting Remotion up in an existing one — covers scaffolding, the root composition, Studio, and the first render

## Execute

### 1. Create Project

> Goal: scaffold the Remotion project with the official CLI

```bash
bunx create-video@latest --yes --blank my-video
# or skip TailwindCSS
bunx create-video@latest --yes --blank --no-tailwind my-video

cd my-video
bun install
```

1. `--yes` is non-interactive (a template flag and directory are required)
2. `--blank` uses the blank template — add `--no-tailwind` if Tailwind is not wanted
3. if the project already exists → install `remotion` and `@remotion/cli` per the official docs at `https://remotion.dev`

### 2. Setup Composition

> Goal: create a working root composition

```tsx
import { Composition } from 'remotion'
import { MyComp } from './MyComp'

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
)
```

1. declare `id`, `component`, `durationInFrames`, `fps`, `width`, `height` explicitly
2. put `defaultProps` as an inline object literal so the Studio infers controls
3. use `useCurrentFrame()` + `interpolate()` inside the component — not CSS animations
4. use `staticFile()` for assets in `public/`

### 3. Start Studio

> Goal: open Remotion Studio for preview

1. `bunx remotion studio --no-open` or `bun run dev`
2. `bunx remotion preview` is deprecated — use `remotion studio` only
3. press `s` in the terminal to reopen the browser

### 4. Verify

> Goal: smoke test the first render

1. the Studio opens and the composition renders correctly in the preview
2. test a real render: `bunx remotion render MyComp out/video.mp4`
3. check the output file is created and playable
4. if it breaks → run `/resolve-errors` max 3 rounds, then stop and report

## Rules

- Always use `create-video` scaffolding for new projects — don't hand-config from scratch
- `useCurrentFrame()` is the source of truth for animation — no CSS animations/JS timers
- Convert seconds to frames with `time * fps`
- Use `--no-open` for remote/CI
- Use `/follow-lib-remotion` for the full reference and cloud rendering

## Expected Outcome

- The Remotion project scaffolds successfully and the Studio opens
- The composition renders correctly in the preview
- The first render via the CLI produces an output
