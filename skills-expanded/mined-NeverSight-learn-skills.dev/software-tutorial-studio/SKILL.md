---
name: software-tutorial-studio
description: >
  Generate narrated instructional tutorial videos for software platforms and websites.
  Provide a URL for live feature analysis, or drop in screenshots — the skill
  produces a step-by-step Remotion tutorial video with macOS TTS (or ElevenLabs) voiceover.
  Minimal input required. Optimized for tools like Airtable, Notion, Linear,
  custom dashboards, and any web-based platform.
metadata:
  tags: remotion, tutorial, instructional, macos-tts, airtable, software, onboarding, walkthrough, screencapture
---

# Claude Code Skill: Software Tutorial Studio

Turns a URL or screenshots of any software platform into a **narrated,
step-by-step instructional video** using Remotion and macOS TTS.

Drop in a link or images. The skill does the rest.

---

## What This Skill Does

| Input | Output |
|---|---|
| A platform URL + feature name | Narrated tutorial video walking through that feature |
| Screenshots of a platform/UI | Narrated tutorial video built from those screens |
| Both URL and screenshots | Hybrid — live analysis + screenshots as visual assets |

---

## Activation

```
🎓 Activate Software Tutorial Studio

# Option A — URL-based (skill visits and analyzes the platform)
URL: [https://your-platform.com]
Feature: [what to teach — e.g. "creating a linked record in Airtable"]

# Option B — Image-based (attach screenshots)
Images: [attach 1 or more screenshots]
Platform: [name of the platform shown — e.g. "Airtable", "our custom CRM"]
Feature: [what the screenshots demonstrate — optional, Claude will infer]

# Option C — Both
URL: [https://your-platform.com]
Images: [attach screenshots]
Feature: [optional — Claude will infer from URL + images]
```

> `🎓 Activate Software Tutorial Studio` is the **only** trigger.
> Do not activate from unrelated messages.

**Minimal input design:** Only `URL` or `Images` (or both) are required.
Everything else — step breakdown, narration, timing, visual layout — is
decided autonomously by Claude.

---

## Session Context

Initialize at activation and maintain across all steps:

```
input_mode:       <url | images | hybrid>
platform_name:    <confirmed platform name>
feature_name:     <confirmed feature being taught>
audience:         <inferred — end user | admin | developer>
step_count:       <populated after analysis>
flow_slug:        <kebab-case — e.g. "airtable-linked-records">
tts_voice:        <macOS voice name — e.g. "Samantha (Enhanced)">
render_output:    output/<flow-slug>-<YYYYMMDD>.mp4
fps:              30
dimensions:       1920×1080
```

---

## Autonomy Rules

### Claude decides autonomously
- Step breakdown, step count, and step labels
- Narration script for each step
- Which UI elements to highlight per step
- Example values to type into form fields, inputs, and search boxes
- macOS TTS voice selection (suggests one, user confirms or skips)
- Scene timing derived from measured audio duration
- Caption text and annotation placement
- Whether a screenshot or a rendered UI panel is used per step
- Which CSS library (DaisyUI, shadcn/ui, or existing `src/index.css` classes) to use for each UI element

### Claude must ask the user
- Activation inputs (URL and/or images + platform/feature if not obvious)
- TTS voice confirmation (Gate B)
- Step plan approval (Gate A)
- Whether to proceed past Gate C (component review)

---

## Step 0: Preflight Check

Run before any content work begins.

### Files
- [ ] `src/tutorials/` directory exists or will be created
- [ ] `src/tutorials/<flow-slug>/` will be created for this session
- [ ] Remotion project initialized (`package.json` has `remotion`)
- [ ] `remotion.config.ts` present and set to 1920×1080, 30fps
- [ ] `@remotion/tailwind-v4` and `tailwindcss` in devDependencies
- [ ] `src/index.css` starts with `@import "tailwindcss"` and has `@theme` block
- [ ] `src/Root.tsx` imports `./index.css`
- [ ] `audio/` directory exists or will be created
- [ ] `public/screenshots/` directory exists or will be created

### Environment Variables

No API key required for macOS TTS. Verify `say` and `ffmpeg` are available:

```bash
say --version && ffmpeg -version | head -1
```

```
✅ Preflight passed. Proceeding with tutorial: [FLOW-SLUG]
```

---

## Step 1: Platform Analysis

### Mode A — URL Analysis

Claude visits the provided URL and analyzes:

- **Platform type** — dashboard, database, form builder, CRM, project manager, etc.
- **Navigation structure** — sidebar, topbar, tabs, modals
- **Feature location** — where in the UI the target feature lives
- **Step decomposition** — what discrete actions a user takes to complete the feature
- **UI element identification** — buttons, fields, dropdowns, panels involved

Claude generates a **feature map**:

```
Platform:   Airtable
Feature:    Creating a linked record field
UI Chrome:  Left sidebar (bases), top tab bar (views), main grid
Entry Point: Base → Table → Field configuration panel

Steps identified:
  1. Open the target table
  2. Click the + icon to add a new field
  3. Select "Link to another record" from the field type list
  4. Choose the linked table from the dropdown
  5. Name the field and click Save
  6. Demonstrate using the linked field in a record row
```

### Mode B — Image Analysis

Claude analyzes each attached screenshot:

- **Platform identification** — infer from UI patterns, branding, layout
- **Screen state** — what is shown in each image (which step it represents)
- **UI element identification** — what is highlighted, active, or relevant
- **Sequence inference** — order the screenshots into a logical tutorial flow
- **Gap detection** — identify any missing steps between screenshots

Claude generates the same **feature map** format as Mode A.

### Mode C — Hybrid

Claude cross-references URL analysis with provided screenshots:
- Screenshots take priority as visual assets for their respective steps
- URL analysis fills in any steps not covered by screenshots
- Claude notes which steps use screenshots vs. rendered panels

---

## Step 2: Step Breakdown

From the feature map, generate the full step plan.

Each step defines:

```
Step N:
  label:        <short action label — "Click + Add Field">
  narration:    <full spoken sentence — "To add a new field, click the plus icon at the end of the field header row.">
  ui_focus:     <what region of the screen is active>
  interaction:  <click | type | hover | scroll | none>
  target:       <specific UI element>
  visual_asset: <screenshot-N | rendered-panel>
  highlight:    <element to spotlight — optional>
```

**Step count guidelines:**

| Feature complexity | Steps |
|---|---|
| Single action (e.g. toggle a setting) | 3–4 |
| Short flow (2–4 interactions) | 4–6 |
| Medium flow (4–7 interactions) | 6–9 |
| Complex flow (7+ interactions) | 9–13 |

Always include:
- **Step 1:** Orientation — where the user starts, what they'll learn
- **Step N:** Completion — task done, result visible, brief recap

---

## Step 3: Approval Gate A — Step Plan

Present:

```
Tutorial: [FLOW-SLUG]
Platform: [PLATFORM NAME]
Feature:  [FEATURE NAME]
Scenes:   N
Est. duration: ~Xs (before audio measurement)

Step 1: [label] — [narration preview]
Step 2: [label] — [narration preview]
...
Step N: [label] — [narration preview]
```

Await:
- ✅ **APPROVED** — Proceed to audio
- 🔄 **REVISE** — [specific changes]
- ❌ **RESTART** — [new direction]

---

## Step 4: macOS TTS Narration

### Voice Selection

Claude selects `Samantha (Enhanced)` automatically — the clearest, most natural
US English voice for professional tutorials. No confirmation needed. If the user
specified a different voice in activation inputs, use that instead.

State the chosen voice in the Gate C summary.

To see all available US English voices (reference only):
```bash
say -v '?' | grep "en_US"
```

### Audio Generation Rules

- Source files go in `audio/<flow-slug>/` (AIFF from `say`)
- Final MP3s go in `public/audio/<flow-slug>/` (Remotion serves from `public/`)
- **Critical:** re-encode at 44100Hz stereo — macOS `say` outputs 22050Hz mono,
  which causes "no waveform" in Remotion Studio (audio still plays in renders,
  but re-encoding to 44100Hz ensures full compatibility)
- File naming: `public/audio/<flow-slug>/step-{N}.mp3`

Generate all AIFFs in parallel, then convert each immediately after:

```bash
mkdir -p audio/<flow-slug> public/audio/<flow-slug>

# Generate all AIFFs in parallel
say -v "Samantha (Enhanced)" -o audio/<flow-slug>/step-1.aiff "narration for step 1" &
say -v "Samantha (Enhanced)" -o audio/<flow-slug>/step-2.aiff "narration for step 2" &
# ... one line per step ...
say -v "Samantha (Enhanced)" -o audio/<flow-slug>/step-N.aiff "narration for step N" &
wait

# Convert all AIFFs to 44100Hz stereo MP3 (sequential is fine — ffmpeg is fast)
for i in $(seq 1 <TOTAL_STEPS>); do
  ffmpeg -y -i audio/<flow-slug>/step-$i.aiff \
    -ar 44100 -ac 2 -codec:a libmp3lame -qscale:a 2 \
    public/audio/<flow-slug>/step-$i.mp3 -loglevel error
done
```

Measure all durations in one pass after conversion:

```bash
for i in $(seq 1 <TOTAL_STEPS>); do
  printf "step-%d: " $i
  ffprobe -v error -show_entries format=duration \
    -of default=noprint_wrappers=1:nokey=1 \
    public/audio/<flow-slug>/step-$i.mp3
done
```

**Note on "no waveform" in Remotion Studio:** This is a known Studio display
limitation with externally-generated audio files. The audio is embedded
correctly in the rendered MP4 — verify by playing the final render, not the
Studio preview.

### AUDIO_TIMING.md

Write to `src/tutorials/<flow-slug>/AUDIO_TIMING.md` (not the repo root).
Generate after all durations are measured:

```
| step | file                              | start_frame | end_frame | duration_s | narration_preview              |
|------|-----------------------------------|-------------|-----------|------------|-------------------------------|
| 1    | audio/<flow-slug>/step-1.mp3      | 0           | 127       | 4.23       | "In this tutorial, we'll..."  |
| 2    | audio/<flow-slug>/step-2.mp3      | 127         | 247       | 4.00       | "To add a new field..."       |
...

FPS: 30
Total frames: [N]
Total duration: [X]s
```

---

## Component Libraries Available

Two pre-built libraries are installed and can be used when building rendered UI panels.

### DaisyUI
- **Usage:** Pure CSS class names directly in JSX (`btn`, `badge`, `card`, `stat`, `alert`, `progress`, `loading`, etc.)
- **When to use in rendered panels (Mode A):** Yes — DaisyUI is pure CSS and renders perfectly in Remotion. Use it for quick, polished UI elements when building platform panel approximations: status badges, progress bars, stats, alerts, form inputs, navigation menus.
- **No install needed** — already active via `@plugin "daisyui"` in `src/index.css`.

### shadcn/ui
- **Components location:** `src/components/ui/` (add via `npx shadcn@latest add <component>`)
- **Import:** `import { Button } from "@/components/ui/button";` etc.
- **When to use in rendered panels (Mode A):** Static visual components only — Button, Card, Badge, Input, Avatar, Separator, Skeleton. These render as pixel-perfect UI in Remotion's static frame renderer. **Avoid** interactive Radix primitives (Dialog, Popover, Select) in video scenes.
- **When to use:** Prefer shadcn when the platform being simulated has a modern SaaS aesthetic that matches shadcn's design language (clean, zinc/white palette).

### Decision guide for rendered panels (Mode A)

| Panel element | Recommended |
|---|---|
| Status badge / tag | DaisyUI `badge` |
| Stats / metric display | DaisyUI `stat` |
| Loading state | DaisyUI `loading` |
| Progress bar | DaisyUI `progress` |
| Alert / notification | DaisyUI `alert` |
| Button | shadcn `Button` or DaisyUI `btn` |
| Card / panel container | shadcn `Card` or custom `.tut-*` class |
| Input field | shadcn `Input` (static, no interaction) |
| Custom brand styling | Custom classes in `src/index.css` |

---

## Step 5: Screenshot Asset Preparation

### Mode A (URL) — Rendered Panels (preferred over screenshots)

For any tutorial where the platform UI can be recreated in React, **rendered panels are always preferred** over screenshots. They enable:
- Typing animations (character-by-character text reveal driven by `frame`)
- Highlight rings applied as CSS (`boxShadow`) directly on the element — no coordinate math
- `scrollY` translation to reveal below-fold content

Claude generates a single panel component (e.g. `PlatformPanel.tsx`) that accepts:
- `highlight?: FieldName` — which field/section to ring
- `highlightOpacity?: number` — driven by `interpolate` in the scene
- `scrollY?: number` — shift content up for below-fold scenes
- `values?: { [field]: string }` — typed text for each input, revealed character-by-character

**CSS hierarchy for rendered panels — check in this order before writing anything custom:**

1. **Existing `src/index.css` classes** — check for `.tut-*`, `.instr-*`, `.web-*`, `.tt-*` that already cover the need
2. **DaisyUI** — `btn`, `badge`, `input`, `textarea`, `card`, `stat`, `alert`, `progress` etc. (already active, zero install)
3. **shadcn/ui** — `Button`, `Card`, `Input`, `Badge` etc. from `src/components/ui/` (static only, no Radix interactives)
4. **Custom inline styles** — only for animated values (`opacity`, `transform`, `boxShadow`) or one-off layout that has no library equivalent

Never write a custom CSS class when a DaisyUI or shadcn class already does the job.

### Mode B / C (Images) — Screenshot Assets
For each provided screenshot:

1. Save to `public/screenshots/<flow-slug>/step-<N>.png`
2. Reference in the asset manifest
3. Use as `<Img>` in the Remotion scene

### Screenshot Highlight Overlay
When a screenshot is used, Claude generates a `HighlightOverlay` that:
- Draws a colored rectangle or circle around the target UI element
- Animates in with a pulse effect at the interaction frame
- Optionally adds a label callout pointing to the element

#### Coordinate Pipeline — deterministic, not estimated

Never eyeball coordinates. Follow all four steps in order.

**Step 0 — Confirm `objectPosition` before measuring anything**

The `objectPosition` used when rendering the `<Img>` determines how the image
is cropped into the 1920×1080 frame. Getting this wrong silently shifts all Y
coordinates. Check the scene component before doing any math:

| Scene `<Img>` style | Pass to `toVideoRect()` |
|---|---|
| `objectFit:"cover"` with no `objectPosition` | `"top"` (default) |
| `objectFit:"cover" objectPosition:"top center"` | `"top"` |
| `objectFit:"cover" objectPosition:"center"` | `"center"` |
| Manual negative `top` shift on `<Img>` | Use `"top"`, then subtract the shift from all Y values after conversion |

**Step 1 — Get original image dimensions:**
```bash
sips -g pixelWidth -g pixelHeight public/screenshots/<flow-slug>/step-N.png
```

**Step 2 — Measure element bounds in the original PNG**

Open the original screenshot in Preview. Use **Tools → Show Inspector** (Cmd+I) —
it shows pixel coordinates as you move the cursor. For web platform screenshots,
open the original in a browser tab and run in DevTools console:

```js
// Click the element, then run:
document.querySelector('SELECTOR').getBoundingClientRect()
// → { x, y, width, height } in CSS pixels at the page's current zoom
```

Scale CSS pixels to screenshot pixels by multiplying by `window.devicePixelRatio`.

**Step 3 — Convert to video-space coordinates (CLI one-liner, no source file needed)**

Run this directly in the terminal — no need to add a temp file to your project:

```bash
npx tsx --tsconfig tsconfig.json -e "
import { toVideoRect, debugScaleInfo } from './src/tutorials/_utils/screenshotCoords';
const SHOT = { origW: 3314, origH: 1958 };        // replace with sips output
const POS  = 'top';                                // from Step 0

// Required: print scale factors first — confirms you have the right dimensions
console.log(debugScaleInfo(SHOT));
// → Screenshot: 3314×1958  →  Video: 1920×1080
// → Scale: 0.5793  |  Scaled height: 1134px  |  Y-offset (top-crop): 0px

// Convert each element rect (origX, origY, origW, origH):
console.log('button:', JSON.stringify(toVideoRect(869, 473, 1945, 52, SHOT, POS)));
// → { x: 503, y: 274, w: 1127, h: 30 }
"
```

Sanity-check every output rect before using it in code:
- `x ≥ 0` and `x + w ≤ 1920`
- `y ≥ 0` and `y + h ≤ 1080`

Any out-of-bounds value means wrong image dimensions or wrong `objectPosition`.

**Step 4 — Verify with frame extraction + zoom crop**

Extract the frame where the highlight is fully visible
(`scene.start + showAt + 10`):

```bash
npx remotion still <CompositionId> --frame=<N> \
  --output=public/screenshots/<flow-slug>/verify-scene<N>.png
```

Then crop tightly around the annotated element for a zoomed view — much easier
to judge ±5px accuracy than eyeballing a 1920×1080 image:

```bash
# Add ~80px padding around the highlight rect (x=420, y=180, w=200, h=40)
# crop=W:H:X:Y  →  W=200+160, H=40+160, X=420-80, Y=180-80
ffmpeg -i public/screenshots/<flow-slug>/verify-scene<N>.png \
  -vf "crop=360:200:340:100" \
  public/screenshots/<flow-slug>/verify-scene<N>-zoom.png -y -loglevel error

open public/screenshots/<flow-slug>/verify-scene<N>-zoom.png
```

The highlight border should sit flush on the element edges in the zoomed view.
If it is off, re-measure in the original PNG and re-run Step 3. Do not adjust
coordinates by trial-and-error — fix the measurement.

### Asset Manifest

Generate `public/screenshots/<flow-slug>/asset-manifest.json`:

```json
[
  {
    "step": 1,
    "file": "public/screenshots/airtable-linked-records/step-1.png",
    "source": "user-provided",
    "type": "screenshot",
    "highlight": { "x": 420, "y": 180, "w": 200, "h": 40 }
  },
  {
    "step": 3,
    "file": null,
    "source": "rendered-panel",
    "type": "component",
    "component": "Step_03"
  }
]
```

---

## Output Structure

```
src/tutorials/<flow-slug>/
├── components/
│   ├── TutorialShell.tsx       ← outer frame: platform chrome simulation
│   ├── Step_01.tsx             ← rendered UI panel (used when no screenshot)
│   ├── Step_02.tsx
│   └── ...
├── remotion/
│   ├── TutorialComposition.tsx ← main Remotion composition
│   ├── scenes/
│   │   ├── Scene_01.tsx        ← screenshot or panel + audio + overlays
│   │   ├── Scene_02.tsx
│   │   └── ...
│   └── overlays/
│       ├── HighlightBox.tsx    ← animated highlight rectangle
│       ├── ClickRipple.tsx     ← click feedback
│       ├── CursorOverlay.tsx   ← animated cursor
│       ├── Caption.tsx         ← bottom narration caption bar
│       ├── StepCounter.tsx     ← "Step 2 of 7" badge (top-right)
│       └── Tooltip.tsx         ← callout annotation
├── data/
│   └── flow.ts                 ← all step data, narration, timings, highlights
└── tutorialTimings.ts          ← frame map derived from AUDIO_TIMING.md
```

---

## Scene Architecture

Each scene is **audio-length-driven** — its duration is set by the measured
macOS TTS audio file, not a fixed frame count.

### Typing animation (use whenever a field is being filled)

Store example values in `data/typingData.ts` and reveal them character-by-character:

```ts
// data/typingData.ts
export const FORM_VALUES = {
  title:   "My example title",
  comment: "Detailed comment text goes here...",
} as const;

/** Reveal text at ~20 chars/sec starting at `startFrame`. */
export function typeText(text: string, frame: number, startFrame = 35): string {
  const chars = Math.max(0, Math.floor((frame - startFrame) * (20 / 30)));
  return text.slice(0, Math.min(chars, text.length));
}
```

In a scene, pass the partial string to the panel — carry forward all previously
typed values so the form looks progressively filled across scenes:

```tsx
const typedTitle = typeText(FORM_VALUES.title, frame, 40);

<PlatformPanel
  highlight="title"
  highlightOpacity={hlOpacity}
  values={{ title: typedTitle }}
/>
```

### Highlight ring (built into the rendered panel component)

Apply `boxShadow` directly on the element — no overlay component needed:

```tsx
// Inside PlatformPanel.tsx
const ring = (field: FieldName): React.CSSProperties =>
  highlight === field
    ? { boxShadow: `0 0 0 3px rgba(59,130,246,${highlightOpacity})`, borderRadius: 6 }
    : {};

// On each section div:
<div style={{ padding: 8, ...ring("title") }}>...</div>
```

### Full scene template (rendered panel)

```tsx
export const Scene_02: React.FC = () => {
  const frame = useCurrentFrame();
  const opacity   = interpolate(frame, [0, 12],  [0, 1], { extrapolateRight: "clamp" });
  const hlOpacity = interpolate(frame, [20, 32], [0, 1], { extrapolateRight: "clamp" });
  const typedTitle = typeText(FORM_VALUES.title, frame, 40);

  return (
    <AbsoluteFill style={{ opacity }}>
      <PlatformPanel highlight="title" highlightOpacity={hlOpacity} values={{ title: typedTitle }} />
      <Caption text={TUTORIAL_STEPS[1].narration} frame={frame} />
      <StepCounter current={2} total={7} frame={frame} />
      <Audio src={staticFile("audio/<flow-slug>/step-2.mp3")} />
    </AbsoluteFill>
  );
};
```

### Cursor + ClickRipple (optional — skip by default)

`CursorOverlay` and `ClickRipple` are available in `remotion/overlays/` but are
**not used by default**. Add them only when the user explicitly requests a cursor
animation, or when a click/hover interaction is the entire point of the step.
When used, position them over the highlighted element in the rendered panel.

---

## Overlay Components

### `HighlightBox.tsx`
```
Props: x, y, w, h, frame, showAt, color?
- Uses className="tut-highlight" from src/index.css
- Position/size via style={{ left: x, top: y, width: w, height: h }}
- Entrance opacity animated via style={{ opacity: interpolate(...) }} at showAt
- Pulse scale animated via style={{ transform: `scale(${pulse})` }}
- Optional label prop: renders a small tag above the box using .tut-step-badge styles
```

### `CursorOverlay.tsx`
```
Props: x, y, frame, clickAt?
- Uses className="tut-cursor" from src/index.css
- SVG cursor positioned via style={{ left: x, top: y }}
- Entrance opacity animated via style={{ opacity: interpolate(...) }}
- If clickAt: scale pulse via style={{ transform }} using spring()
- For scroll interactions: animated top via style={{ top: interpolate(...) }}
```

### `ClickRipple.tsx`
```
Props: x, y, frame, triggerAt
- Uses className="tut-ripple" from src/index.css
- Position via style={{ left: x, top: y }}
- Scale: 0 → 2.5 over 20 frames via style={{ transform: `scale(${s})` }}
- Opacity: 0.5 → 0 via style={{ opacity: interpolate(...) }}
```

### `Caption.tsx`
```
Props: text, frame
- Uses className="tut-caption" from src/index.css for all visual styling
- Entrance: slide up via style={{ transform: `translateY(${y}px)` }} over 10 frames
- Text: typewriter effect — slice string via interpolate, rendered as plain text node
- Mirrors the narration text for accessibility
```

### `StepCounter.tsx`
```
Props: current, total, frame
- Uses className="tut-step-badge" from src/index.css
- Renders "Step N of M" as text
- Entrance opacity via style={{ opacity: interpolate(...) }}
- Crossfades on scene change via opacity interpolation
```

### `Tooltip.tsx`
```
Props: text, targetX, targetY, frame, showAt
- Uses className="tut-tooltip" from src/index.css
- Position via style={{ left: targetX, top: targetY }}
- Entrance: opacity + scale from 0.85 via style={{}} at showAt
- Used to annotate UI elements that need extra explanation
```

---

## `flow.ts` Data File

```ts
// src/tutorials/<flow-slug>/data/flow.ts

export interface TutorialStep {
  id: string;
  stepNumber: number;
  label: string;
  narration: string;
  interaction: "click" | "type" | "hover" | "scroll" | "none";
  target?: string;
  typedValue?: string;
  cursorPosition?: { x: number; y: number };
  highlight?: { x: number; y: number; w: number; h: number };
  screenshotFile?: string;   // null if using rendered panel
  tooltipText?: string;
}

export const TUTORIAL_STEPS: TutorialStep[] = [
  {
    id: "step-01",
    stepNumber: 1,
    label: "Open the table",
    narration: "In this tutorial, you'll learn how to create a linked record field in Airtable. Start by opening the table where you want to add the link.",
    interaction: "none",
    screenshotFile: "public/screenshots/airtable-linked-records/step-1.png",
  },
  {
    id: "step-02",
    stepNumber: 2,
    label: "Click + Add Field",
    narration: "Click the plus icon at the end of the field header row to open the field creation panel.",
    interaction: "click",
    target: "add-field-button",
    cursorPosition: { x: 1180, y: 142 },
    highlight: { x: 1160, y: 128, w: 44, h: 32 },
    screenshotFile: "public/screenshots/airtable-linked-records/step-2.png",
  },
  // ...
];
```

---

## `tutorialTimings.ts`

Generated from `AUDIO_TIMING.md` — frame ranges are **derived from measured
audio durations**, not estimated.

```ts
// src/tutorials/<flow-slug>/remotion/tutorialTimings.ts

export const TUTORIAL_TIMINGS = {
  fps: 30,
  scenes: [
    { id: "step-01", label: "Open the table",   start: 0,   duration: 127 },
    { id: "step-02", label: "Click + Add Field", start: 127, duration: 120 },
    { id: "step-03", label: "Select field type", start: 247, duration: 135 },
    // ...
  ],
  totalFrames: 0, // sum of all durations — computed at generation time
} as const;
```

---

## `TutorialComposition.tsx`

```tsx
// src/tutorials/<flow-slug>/remotion/TutorialComposition.tsx

import React from "react";
import { Sequence } from "remotion";
import { TUTORIAL_TIMINGS } from "../tutorialTimings";
import { Scene_01 } from "./scenes/Scene_01";
import { Scene_02 } from "./scenes/Scene_02";
// ... one import per scene

const SCENES = [Scene_01, Scene_02, /* ... */];

export const TutorialComposition: React.FC = () => (
  <>
    {TUTORIAL_TIMINGS.scenes.map((scene, i) => {
      const SceneComponent = SCENES[i];
      return (
        <Sequence key={scene.id} from={scene.start} durationInFrames={scene.duration}>
          <SceneComponent />
        </Sequence>
      );
    })}
  </>
);
```

Register in `src/Root.tsx`:

```tsx
<Composition
  id="SoftwareTutorial"
  component={TutorialComposition}
  durationInFrames={TUTORIAL_TIMINGS.totalFrames}
  fps={30}
  width={1920}
  height={1080}
/>
```

---

## Approval Gate C — Review Before Render

```
Tutorial: [FLOW-SLUG]
Platform: [PLATFORM NAME]
Feature:  [FEATURE NAME]
Scenes:   N  |  Duration: Xs  |  Output: [FILENAME]

Steps:
  ✅ Step 1 — [label] — [duration]s — [screenshot | rendered panel]
  ✅ Step 2 — [label] — [duration]s — [screenshot | rendered panel]
  ...

Audio: macOS TTS — [Voice Name] — all [N] files generated at 44100Hz stereo
Overlays: HighlightBox, CursorOverlay, ClickRipple, Caption, StepCounter

Placeholder assets (need replacement before final use):
  ⚠️  Step 4 — no screenshot provided, using rendered panel

Ready to render?
```

Await GO / ADJUST.

---

## Render

### Frame Extraction — Overlay Position Verification (replaces test render)

Before doing a full render, verify every scene that has annotations using
`npx remotion still`. This takes ~2s per frame and catches coordinate bugs
without encoding an MP4.

```bash
# Extract a frame after the highlight has fully faded in
# Target: scene.start + showAt + 10
npx remotion still <CompositionId> --frame=<N> \
  --output=public/screenshots/<flow-slug>/verify-scene<N>.png

open public/screenshots/<flow-slug>/verify-scene<N>.png
```

Do this for **every scene with a HighlightBox or CursorOverlay**. Also extract
frame 0 of scene 1 to confirm no pop-in on cold start.

For annotated scenes, follow up with the zoom crop from the Coordinate Pipeline
(Step 4) to verify highlight placement at pixel precision — do not rely on
eyeballing the full 1920×1080 still.

Validate per frame:
- [ ] Highlight box sits flush on the correct UI element (confirm via zoom crop)
- [ ] Cursor positioned at the correct target
- [ ] Caption text readable against screenshot content
- [ ] Step counter visible and correct
- [ ] No pop-in on frame 0

If the highlight is off, re-measure the element in the original PNG and
re-run the `npx tsx` CLI one-liner from Step 3 — do not adjust by trial-and-error.

Fix all coordinate issues before proceeding to full render.

### Full Render

```bash
npx remotion render SoftwareTutorial \
  --output=output/<flow-slug>-<YYYYMMDD>.mp4 \
  --codec=h264 \
  --crf=18
```

---

## CSS Architecture Rule — MANDATORY

All CSS lives in `src/index.css`. No exceptions.

- **Never** write inline visual styles (`style={{ color, background, fontSize }}`) in any overlay or panel component
- **Never** create a separate `.css` file per tutorial or per component
- `style={{}}` is permitted **only** for animated values driven by `useCurrentFrame()` / `interpolate()` / `spring()`
- Before creating any new CSS class, check `src/index.css` for an existing class that covers the need (`.instr-*`, `.scene-*`, `.web-*`, `.tt-*`, etc.)
- Overlay components (`Caption`, `StepCounter`, `HighlightBox`, `Tooltip`) use classes defined in `src/index.css` — never hardcoded rgba/hex values in JSX
- Rendered UI panels (Mode A, no screenshots) use existing `src/index.css` layout and design-system classes (`web-*`, `instr-*`, or `tt-*`) as their base. If a platform's branding needs a custom class, add it to `src/index.css` under a labelled block:
  ```css
  /* ── Tutorial: <flow-slug> platform panel ──────────────────── */
  .tut-<flowslug>-topbar { @apply ...; }
  ```

---

## Visual Design

All tutorial videos use a consistent visual language regardless of platform.
All visual properties are applied via CSS classes from `src/index.css` — **not** hardcoded in components.

| Element | CSS Class / Token |
|---|---|
| Background | Platform screenshot or rendered panel (full bleed, 1920×1080) |
| Highlight box | `.tut-highlight` — blue-500 border, blue-500/40 fill, rounded-lg |
| Cursor | `.tut-cursor` — SVG, white fill with drop-shadow filter |
| Click ripple | `.tut-ripple` — blue-400 expanding ring (scale animated via `style={{}}`) |
| Caption bar | `.tut-caption` — dark semi-transparent strip, white `font-inter text-body` |
| Step counter | `.tut-step-badge` — white pill, top-right, `font-inter text-label` |
| Tooltip | `.tut-tooltip` — white card, dark text, blue arrow pointer |

Add these classes to `src/index.css` under `@layer components` on first use:

```css
  /* ── Instructional Tutorial Overlays ─────────────────────── */
  .tut-caption     { @apply absolute bottom-0 left-0 right-0 flex items-center px-8 font-inter; background: rgba(0,0,0,0.75); height: 64px; }
  .tut-step-badge  { @apply absolute top-8 right-8 bg-white rounded-full px-4 py-1 font-inter text-label font-semibold; color: #1C1E3C; }
  .tut-tooltip     { @apply absolute bg-white rounded-xl px-5 py-3 font-inter text-caption font-medium shadow-xl; color: #0F172A; }
  .tut-highlight   { @apply absolute rounded-lg pointer-events-none; border: 2px solid #3B82F6; background: rgba(59,130,246,0.15); }
  .tut-ripple      { @apply absolute rounded-full pointer-events-none; border: 2px solid #60A5FA; }
  .tut-cursor      { @apply absolute pointer-events-none; filter: drop-shadow(0 2px 4px rgba(0,0,0,0.5)); }
```

For rendered panels (no screenshot), Claude generates a faithful approximation of the
platform's UI using `src/index.css` layout classes and `@theme` tokens. Custom platform
colors go into `src/index.css` — never as inline JSX style props.

---

## Final Checklist

### Setup
- [ ] Activation inputs received (URL and/or images)
- [ ] Platform and feature confirmed
- [ ] Session context initialized
- [ ] Preflight passed

### Analysis
- [ ] Platform analyzed (URL crawl and/or image analysis)
- [ ] Feature map generated
- [ ] Step breakdown complete

### Planning
- [ ] Step plan approved (Gate A)

### Audio
- [ ] TTS voice noted in Gate C summary (default: Samantha Enhanced)
- [ ] All AIFFs generated in parallel via `say &` + `wait` into `audio/<flow-slug>/`
- [ ] All MP3s re-encoded at 44100Hz stereo into `public/audio/<flow-slug>/`
- [ ] All durations measured with `ffprobe` in one loop
- [ ] `src/tutorials/<flow-slug>/AUDIO_TIMING.md` generated

### Assets
- [ ] Screenshots saved to `public/screenshots/<flow-slug>/`
- [ ] Rendered panels generated for steps without screenshots
- [ ] Asset manifest generated
- [ ] `HighlightBox` coordinates set for all interactive steps

### CSS
- [ ] `src/index.css` checked for existing classes before creating any new ones
- [ ] `.tut-*` overlay classes added to `src/index.css` under `@layer components` if not already present
- [ ] Any platform-specific rendered-panel classes added to `src/index.css` with flow-slug label
- [ ] No CSS defined inside `.tsx` files, `<style>` tags, or separate `.css` files
- [ ] `style={{}}` used only for animated values (`opacity`, `transform`, `top`, `left`, `scale`)

### Code
- [ ] `data/flow.ts` generated — all step data typed
- [ ] `tutorialTimings.ts` generated — frame map from measured audio
- [ ] All scene components generated
- [ ] All overlay components generated
- [ ] `TutorialComposition.tsx` assembled
- [ ] Composition registered in `src/Root.tsx`
- [ ] Component review approved (Gate C)

### Render
- [ ] Frame extracted and verified for every annotated scene (`npx remotion still`)
- [ ] Frame 0 verified — no pop-in on cold start
- [ ] Full render completed
- [ ] Output: `output/<flow-slug>-<YYYYMMDD>.mp4`