---
name: playwright-tutorial-video
description: >
  Record a real user flow with Playwright, then generate a Remotion tutorial video.
  Three entry points: capture (discrete screenshots + coordinates per step),
  recording (continuous video with timestamp-synced overlays), or from-manifest
  (re-generate scenes from existing manifest). No new UI code created.
metadata:
  tags: playwright, remotion, tutorial, live-components, automation, frontend, coordinates, onboarding, recording, video
---

# Claude Code Skill: Playwright Tutorial Video

Bridges **Playwright automation** and **Remotion video** in one pipeline.

Playwright runs your real app and captures every interaction step — screenshots,
element coordinates, typed values. That manifest feeds directly into Remotion
scene generation that imports your **existing** components. No new UI code is
written. No coordinate guesswork. No manual screenshot measurement.

```
Your app (running)
  → Playwright capture script (auto-generated)
    → manifest.json (steps + screenshots + coords)
      → Remotion scenes (wrap your existing components)
        → tutorial video
```

---

## Entry Points

| Entry | When to use | Output |
|---|---|---|
| `capture` | App is running — discrete screenshot per step | N scene files, each with a screenshot background |
| `recording` | App is running — one continuous video of the whole flow | Single `VideoComposition` with `OffthreadVideo` background + timestamp-synced overlays |
| `from-manifest` | Capture already done — regenerate scenes from existing manifest | Same as whichever entry produced the manifest |

**Choosing between `capture` and `recording`:**
- Use `capture` when the flow has distinct, pausable states you want to show one at a time
- Use `recording` when the flow has continuous motion (scroll, drag, typing) or you want the real interactions visible in the video rather than simulated cursor overlays

---

## Activation

```
🎭 Activate Playwright Tutorial

Entry: [capture | recording | from-manifest]

# For capture entry:
App URL:    [e.g. http://localhost:3000]
Task:       [what the user does — e.g. "complete the onboarding checklist"]
Components: [paths to existing components — e.g. "src/components/, src/features/onboarding/"]
Shell:      [optional — path to layout/shell component that wraps all scenes]
Selectors:  [optional — CSS selectors or ARIA labels for key elements; Claude infers if omitted]

# For recording entry:
App URL:    [e.g. http://localhost:3000]
Task:       [what the user does — the full flow to record end-to-end]
Selectors:  [optional — Claude infers from the task]

# For from-manifest entry:
Manifest:   [path to manifest.json — e.g. "public/screenshots/onboarding/manifest.json"]
Components: [paths to existing components — omit for recording manifests]
Shell:      [optional]
```

> `🎭 Activate Playwright Tutorial` is the **only** trigger.
> Do not activate from unrelated messages.

---

## Session Context

Initialize at activation and maintain across all steps:

```
entry:            <capture | recording | from-manifest>
app_url:          <URL of running app>
task:             <what the user is doing>
flow_slug:        <kebab-case — e.g. "onboarding-checklist">
component_paths:  <list of resolved paths — omit for recording entry>
shell_path:       <optional — path to existing shell/layout component>
viewport:         <populated from manifest — e.g. { width: 1280, height: 720 }>
video:            { width: 1920, height: 1080, fps: 30 }
manifest_path:    public/recordings/<flow-slug>/manifest.json   ← recording entry
                  public/screenshots/<flow-slug>/manifest.json  ← capture entry
render_output:    output/<flow-slug>-<YYYYMMDD>.mp4
discovered:       [] ← capture entry only
```

---

## Autonomy Rules

### Claude decides autonomously
- Which existing component maps to each captured step
- What props to pass to each component to match the captured UI state
- Typing animation speed and start frame
- Entrance animation (fade + translateY, 12 frames default)
- Overlay timing (highlight fade-in, cursor entrance)
- Caption text (from manifest `caption` field — refined for flow if needed)
- Scene duration (from interaction type defaults, same as ui-flow-studio)

### Claude must ask the user
- Entry point and activation inputs
- Confirm component-to-step mapping before generating scenes (Gate A)
- Whether to proceed past Gate C (component review)
- Any ambiguous selector (asks once, does not re-ask)

---

## Step 0: Preflight

Run before any content work begins.

### Environment
```bash
# Playwright installed and browsers provisioned
npx playwright --version
npx playwright install chromium --dry-run 2>&1 | head -1

# App is reachable
curl -s -o /dev/null -w "%{http_code}" <APP_URL>

# Remotion project initialized
node -e "require('./package.json').dependencies['remotion'] && console.log('ok')"

# tsx available for running capture scripts
npx tsx --version
```

### Directories
- [ ] `scripts/` directory exists or will be created
- [ ] `public/screenshots/<flow-slug>/` will be created by the capture script
- [ ] `src/flows/<flow-slug>/` will be created for scenes
- [ ] `@remotion/tailwind-v4` and `tailwindcss` in devDependencies
- [ ] `src/index.css` starts with `@import "tailwindcss"` and has `@theme` block

```
✅ Preflight passed. Proceeding with flow: [FLOW-SLUG]
```

---

## Step 1: Generate Capture Helper (capture entry only)

Write `scripts/playwright-capture.ts` to the project **once** — skip if already present.
This is the reusable capture utility imported by every flow's capture script.

```typescript
// scripts/playwright-capture.ts
import { type Page } from 'playwright';  // type-only import required in ESM projects
import * as fs from 'fs';
import * as path from 'path';

export interface CapturedElement {
  selector: string;
  x: number;
  y: number;
  width: number;
  height: number;
}

export interface CapturedStep {
  step: number;
  label: string;
  caption: string;
  screenshotFile: string;
  interaction: 'click' | 'fill' | 'hover' | 'scroll' | 'none';
  element: CapturedElement | null;
  typedValue?: string;
}

export interface FlowManifest {
  flowSlug: string;
  capturedAt: string;
  viewport: { width: number; height: number };
  steps: CapturedStep[];
}

export class TutorialCapture {
  private steps: CapturedStep[] = [];
  private stepIndex = 0;
  private screenshotDir: string;

  constructor(
    private page: Page,
    private flowSlug: string,
  ) {
    this.screenshotDir = path.join('public', 'screenshots', flowSlug);
    fs.mkdirSync(this.screenshotDir, { recursive: true });
  }

  private async snapshot(): Promise<string> {
    const filename = `step-${String(this.stepIndex + 1).padStart(2, '0')}.png`;
    const filepath = path.join(this.screenshotDir, filename);
    await this.page.screenshot({ path: filepath, fullPage: false });
    return filepath;
  }

  private async getBox(selector: string): Promise<CapturedElement | null> {
    try {
      const locator = this.page.locator(selector).first();
      await locator.scrollIntoViewIfNeeded();
      const box = await locator.boundingBox();
      if (!box) return null;
      return { selector, x: box.x, y: box.y, width: box.width, height: box.height };
    } catch {
      return null;
    }
  }

  /** Capture a scene with no interaction — screenshot only. */
  async scene(label: string, caption: string): Promise<void> {
    const file = await this.snapshot();
    this.steps.push({
      step: ++this.stepIndex,
      label, caption,
      screenshotFile: file,
      interaction: 'none',
      element: null,
    });
  }

  /** Capture before click, then click. */
  async click(selector: string, label: string, caption: string): Promise<void> {
    const element = await this.getBox(selector);
    const file = await this.snapshot();
    this.steps.push({
      step: ++this.stepIndex,
      label, caption,
      screenshotFile: file,
      interaction: 'click',
      element,
    });
    await this.page.locator(selector).first().click();
  }

  /** Capture before fill, then fill. */
  async fill(selector: string, value: string, label: string, caption: string): Promise<void> {
    await this.page.locator(selector).first().scrollIntoViewIfNeeded();
    const element = await this.getBox(selector);
    const file = await this.snapshot();
    this.steps.push({
      step: ++this.stepIndex,
      label, caption,
      screenshotFile: file,
      interaction: 'fill',
      element,
      typedValue: value,
    });
    await this.page.locator(selector).first().fill(value);
  }

  /** Hover to trigger tooltip/focus state, then capture. */
  async hover(selector: string, label: string, caption: string): Promise<void> {
    await this.page.locator(selector).first().hover();
    const element = await this.getBox(selector);
    const file = await this.snapshot();
    this.steps.push({
      step: ++this.stepIndex,
      label, caption,
      screenshotFile: file,
      interaction: 'hover',
      element,
    });
  }

  /** Scroll to position and capture. */
  async scroll(scrollY: number, label: string, caption: string): Promise<void> {
    await this.page.evaluate((y) => window.scrollTo({ top: y, behavior: 'instant' }), scrollY);
    await this.page.waitForTimeout(100);
    const file = await this.snapshot();
    this.steps.push({
      step: ++this.stepIndex,
      label, caption,
      screenshotFile: file,
      interaction: 'scroll',
      element: null,
    });
  }

  /** Write manifest.json and print summary. */
  async save(): Promise<string> {
    const vp = this.page.viewportSize() ?? { width: 1280, height: 720 };
    const manifest: FlowManifest = {
      flowSlug: this.flowSlug,
      capturedAt: new Date().toISOString(),
      viewport: vp,
      steps: this.steps,
    };
    const out = path.join(this.screenshotDir, 'manifest.json');
    fs.writeFileSync(out, JSON.stringify(manifest, null, 2));
    console.log(`\n✅ Captured ${this.steps.length} steps → ${out}`);
    this.steps.forEach(s =>
      console.log(`  Step ${s.step}: [${s.interaction}] ${s.label}`)
    );
    return out;
  }
}
```

---

## Step 2: Generate Flow Capture Script (capture entry only)

Based on the `Task` and `Selectors` provided at activation, generate
`scripts/<flow-slug>-capture.ts` — the one-off script for this specific flow.

Claude infers selectors from the task description if not provided. Use semantic
selectors in priority order: ARIA roles > data-testid > text content > CSS class.

**Template:**

```typescript
// scripts/<flow-slug>-capture.ts
// Run with: npx tsx scripts/<flow-slug>-capture.ts
import { chromium } from 'playwright';
import { TutorialCapture } from './playwright-capture';

const FLOW_SLUG = '<flow-slug>';
const APP_URL   = '<app-url>';

(async () => {
  // capture entry uses 1280×720 — screenshots scale ×1.5 to 1920×1080 in coords.ts
  // recording entry uses 1920×1080 — no scaling needed
  const browser = await chromium.launch({ headless: false });
  const page    = await browser.newPage({ viewport: { width: 1280, height: 720 } });
  const capture = new TutorialCapture(page, FLOW_SLUG);

  await page.goto(APP_URL);
  await page.waitForLoadState('networkidle');

  // ── Step 1: orientation ────────────────────────────────────────────
  await capture.scene(
    'Dashboard overview',
    'Start from the main dashboard. The sidebar shows all your workspaces.',
  );

  // ── Step 2: first interaction ──────────────────────────────────────
  await capture.click(
    '[data-testid="new-project-btn"]',
    'Click New Project',
    "Click the '+ New Project' button in the sidebar to open the creation dialog.",
  );

  // ── Step 3: fill in a field ────────────────────────────────────────
  await capture.fill(
    '[placeholder="Project name"]',
    'Q3 Launch Plan',
    'Enter project name',
    "Type the project name. This becomes the title shown across all views.",
  );

  // … one call per step …

  await capture.save();
  await browser.close();
})();
```

**Selector inference rules** (apply when `Selectors` not provided at activation):

| Element type | Preferred selector |
|---|---|
| Button with visible text | `role=button[name="Submit"]` |
| Input with placeholder | `[placeholder="Project name"]` |
| Input with label | `role=textbox[name="Email"]` |
| data-testid present | `[data-testid="submit-btn"]` |
| Link | `role=link[name="Settings"]` |
| Fallback | `.class-name` (least preferred — note it in capture script comment) |

Present the generated capture script to the user and ask:
**"Does this look right? Adjust any selectors or steps, then run it with `npx tsx scripts/<flow-slug>-capture.ts`."**

Wait for the user to confirm the manifest was generated before proceeding.

---

## Step 1b: Generate Recording Capture Script (recording entry only)

Add `TutorialCaptureRecording` to `scripts/playwright-capture.ts` **once** — skip if already present.

```typescript
// Append to scripts/playwright-capture.ts

export interface TimedStep {
  step: number;
  label: string;
  caption: string;
  startMs: number;          // ms since recording started
  interaction: 'click' | 'fill' | 'select' | 'none';
  element: CapturedElement | null;
  typedValue?: string;
}

export interface RecordingManifest {
  flowSlug: string;
  capturedAt: string;
  recordingFile: string;    // path to .webm relative to project root
  videoDurationMs: number;  // populated after context.close()
  viewport: { width: number; height: number };
  steps: TimedStep[];
}

export class TutorialCaptureRecording {
  private steps: TimedStep[] = [];
  private stepIndex = 0;
  private t0 = 0;
  private manifestPath: string;

  constructor(private page: Page, private flowSlug: string) {
    const dir = path.join('public', 'recordings', flowSlug);
    fs.mkdirSync(dir, { recursive: true });
    this.manifestPath = path.join(dir, 'manifest.json');
  }

  start(): void {
    this.t0 = Date.now();
  }

  private elapsed(): number {
    return Date.now() - this.t0;
  }

  private async getBox(selector: string): Promise<CapturedElement | null> {
    try {
      const locator = this.page.locator(selector).first();
      await locator.scrollIntoViewIfNeeded();
      const box = await locator.boundingBox();
      if (!box) return null;
      return { selector, x: box.x, y: box.y, width: box.width, height: box.height };
    } catch { return null; }
  }

  /** Mark a moment in the recording with an optional element to highlight — no interaction. */
  async mark(label: string, caption: string, selector?: string): Promise<void> {
    const startMs = this.elapsed();
    const element = selector ? await this.getBox(selector) : null;
    this.steps.push({ step: ++this.stepIndex, label, caption, startMs, interaction: 'none', element });
  }

  /** Record a click interaction — visible in the video recording. */
  async click(selector: string, label: string, caption: string): Promise<void> {
    const startMs = this.elapsed();
    const element = await this.getBox(selector);
    this.steps.push({ step: ++this.stepIndex, label, caption, startMs, interaction: 'click', element });
    await this.page.locator(selector).first().click();
  }

  /** Select an option — records the moment the value changes. */
  async select(selector: string, value: string, label: string, caption: string): Promise<void> {
    const startMs = this.elapsed();
    const element = await this.getBox(selector);
    this.steps.push({ step: ++this.stepIndex, label, caption, startMs, interaction: 'select', element, typedValue: value });
    await this.page.locator(selector).first().selectOption(value);
  }

  /** Fill a text field — records as typing begins. */
  async fill(selector: string, value: string, label: string, caption: string): Promise<void> {
    const startMs = this.elapsed();
    const element = await this.getBox(selector);
    this.steps.push({ step: ++this.stepIndex, label, caption, startMs, interaction: 'fill', element, typedValue: value });
    await this.page.locator(selector).first().fill(value);
  }

  /** Write manifest after context.close() — pass the finalized video path and duration. */
  async save(recordingWebmPath: string, videoDurationMs: number): Promise<void> {
    const vp = this.page.viewportSize() ?? { width: 1280, height: 720 };
    const manifest: RecordingManifest = {
      flowSlug: this.flowSlug,
      capturedAt: new Date().toISOString(),
      recordingFile: recordingWebmPath,
      videoDurationMs,
      viewport: vp,
      steps: this.steps,
    };
    fs.writeFileSync(this.manifestPath, JSON.stringify(manifest, null, 2));
    console.log(`\n✅ Recording manifest → ${this.manifestPath}`);
    console.log(`   Video: ${recordingWebmPath}  (${(videoDurationMs / 1000).toFixed(1)}s)`);
    this.steps.forEach(s =>
      console.log(`   Step ${s.step} @${(s.startMs / 1000).toFixed(2)}s: [${s.interaction}] ${s.label}`)
    );
  }
}
```

Then generate the flow-specific recording script:

```typescript
// scripts/<flow-slug>-recording.ts
import { chromium } from 'playwright';
import { TutorialCaptureRecording } from './playwright-capture';
import * as fs from 'fs';
import * as path from 'path';

const FLOW_SLUG = '<flow-slug>';
const APP_URL   = '<app-url>';

(async () => {
  // headless required — headed mode crashes during recordVideo on many setups.
  // Viewport matches Remotion composition size — element coordinates are native
  // 1920×1080 pixels, no scaling needed.
  const browser = await chromium.launch({ headless: true });
  const context = await browser.newContext({
    viewport: { width: 1920, height: 1080 },
    recordVideo: {
      dir: `public/recordings/${FLOW_SLUG}/`,
      size: { width: 1920, height: 1080 },
    },
  });

  const page    = await context.newPage();
  const capture = new TutorialCaptureRecording(page, FLOW_SLUG);

  await page.goto(APP_URL);
  // Use domcontentloaded — networkidle never fires with WebSocket-based apps (Convex, Supabase, etc.)
  await page.waitForLoadState('domcontentloaded');
  await page.waitForSelector('<first-visible-selector>', { timeout: 10000 });
  await page.waitForTimeout(1000); // let initial animations settle before starting the clock

  capture.start(); // ← t = 0 starts here, not at page.goto()

  // ── Step 1: orientation ──────────────────────────────────────────
  await capture.mark('Overview', 'caption...', 'selector-to-highlight');
  await page.waitForTimeout(3000); // viewers need ~2s to read a full caption after typewriter completes

  // ── Step 2: first interaction ────────────────────────────────────
  await capture.click('button:has-text("...")', 'Label', 'Caption...');
  await page.waitForTimeout(500);  // wait for UI to update
  await capture.mark('Result state', 'What changed...', 'result-selector');
  await page.waitForTimeout(3000); // hold long enough to read the result caption

  // ── Between steps: reset/clear interactions ───────────────────────
  await capture.click('button:has-text("Clear")', 'Clear', 'Reset...');
  await page.waitForTimeout(1500); // shorter — no caption to read, just a transition

  // … one call per step …

  const endMs = Date.now();
  await context.close(); // finalizes the .webm

  const videoPath = await page.video()!.path();
  const videoDurationMs = endMs - (capture as any).t0;

  fs.mkdirSync(path.dirname(`public/recordings/${FLOW_SLUG}/recording.webm`), { recursive: true });
  fs.renameSync(videoPath, `public/recordings/${FLOW_SLUG}/recording.webm`);

  await capture.save(`public/recordings/${FLOW_SLUG}/recording.webm`, videoDurationMs);
  await browser.close();
})();
```

### Recording pacing guide

The single most common mistake is moving too fast — the viewer can't read a caption that's still typing when the next step starts. Minimum wait times:

| After this call | `waitForTimeout` | Why |
|---|---|---|
| Initial `mark()` (orientation) | **3000ms** | Caption types ~2s, reader needs ~1s after |
| `select()` or `click()` (interaction) | **400–500ms** | Let the UI finish updating |
| `mark()` after showing a result | **3000ms** | Same as orientation — hold long enough to read |
| `click()` for a reset/clear | **1500ms** | Transition only — no result caption to read |
| Final `mark()` (end state) | **3500ms** | Last frame — hold it extra long |

**Why these numbers:** The `Caption` component typewriter effect runs at ~40 chars/sec. A 70-char caption takes ~1.75s to finish typing. The viewer then needs ~1s to absorb the fully visible text. So 3s minimum per step is the floor, not the target.

**When audio is added (recommended):** Replace the fixed `HOLD_STEP` constant with the measured audio duration + 1000ms buffer. Measure first with ffprobe, then set wait times accordingly — see the Audio section below.

For `select:nth-of-type()` selectors: these are unreliable when selects live in separate parent elements. Use `.nth(index)` via an index parameter instead. The `TutorialCaptureRecording.select()` method accepts `index = 0` as a fifth argument for exactly this case.

---

## Step 1c: macOS TTS Audio (recommended for both entry modes)

Generate one narration audio file per step. The narration text is the step's `caption` field.

### Voice selection

Default: `Samantha (Enhanced)` — clear, professional US English. No API key required.

```bash
# List all available US English voices (reference only)
say -v '?' | grep "en_US"
```

### Generate all AIFFs in parallel, then convert

```bash
mkdir -p audio/<flow-slug> public/audio/<flow-slug>

# Generate all AIFFs in parallel (one line per step)
say -v "Samantha (Enhanced)" -o audio/<flow-slug>/step-01.aiff "Step 1 caption text" &
say -v "Samantha (Enhanced)" -o audio/<flow-slug>/step-02.aiff "Step 2 caption text" &
# ... one per step
wait

# Convert all to 44100Hz stereo MP3 — macOS say outputs 22050Hz mono which
# causes "no waveform" in Remotion Studio (audio still plays in final renders,
# but re-encoding ensures full compatibility)
for i in $(seq -w 1 <N>); do
  ffmpeg -y -i audio/<flow-slug>/step-$i.aiff \
    -ar 44100 -ac 2 -codec:a libmp3lame -qscale:a 2 \
    public/audio/<flow-slug>/step-$i.mp3 -loglevel error
done
```

### Measure durations

```bash
for i in $(seq -w 1 <N>); do
  printf "step-%s: " $i
  ffprobe -v error -show_entries format=duration \
    -of default=noprint_wrappers=1:nokey=1 \
    public/audio/<flow-slug>/step-$i.mp3
done
```

### Audio timing rules

| Step type | Audio wait | Why |
|---|---|---|
| `mark()` / `none` | `audioDurationMs + 800` | Audio must finish before next step |
| `select()` / `click()` (interaction) | `400` | React settles quickly; audio overlaps the next `mark()` |
| `mark()` after interaction result | `audioDurationMs + 800` | Audio for the result caption |
| Final `mark()` | `audioDurationMs + 1500` | Extra tail at the end |

**Workflow with audio:**
1. Write the recording script with placeholder `HOLD_STEP = 4000`
2. Run a dry-run to get caption text into `flow.ts`
3. Generate audio and measure durations
4. Replace `HOLD_STEP` with per-step values based on measured audio: `audioDurationMs[i] + 800`
5. Re-run the recording with audio-informed timing

### Using audio in Remotion

**capture entry** (scene-based): scene `durationInFrames` is set to the measured audio duration, same as `software-tutorial-studio`. Audio drives timing.

**recording entry** (continuous video): audio plays as a `<Sequence>`-wrapped `<Audio>` overlay starting at each step's `captionStart`. The recording video is the ground truth for timing — make sure `waitForTimeout` values are at least `audioDurationMs + 800` so audio doesn't get cut by the next step.

---

## Step 2b: Recording Mode Remotion Composition

After the manifest is generated, create a single `VideoComposition.tsx` instead of per-scene files.

### `msToFrame` utility

```typescript
// src/flows/<flow-slug>/remotion/msToFrame.ts
const FPS = 30;
export const msToFrame = (ms: number): number => Math.round(ms / 1000 * FPS);
```

### Timed step data

```typescript
// src/flows/<flow-slug>/data/flow.ts
import { msToFrame } from '../remotion/msToFrame';

export interface TimedStep {
  id: string;
  label: string;
  caption: string;
  startMs: number;
  overlayDelayMs: number;   // how long after startMs before overlay appears
  overlayDurationMs: number;
  highlight?: { x: number; y: number; w: number; h: number };
}

// Paste startMs values from manifest, scale element coords × 1.5
export const TIMED_STEPS: TimedStep[] = [
  {
    id: 'step-01',
    label: 'Overview',
    caption: '...',
    startMs: 0,
    overlayDelayMs: 200,
    overlayDurationMs: 2800,
    highlight: { x: 36, y: 78, w: 101, h: 65 }, // scaled
  },
  // ...
];

// Derive frame numbers from timestamps — no hardcoding needed
export const STEPS_WITH_FRAMES = TIMED_STEPS.map(s => ({
  ...s,
  overlayStart:    msToFrame(s.startMs + s.overlayDelayMs),
  overlayDuration: msToFrame(s.overlayDurationMs),
  captionStart:    msToFrame(s.startMs),
  captionDuration: msToFrame(s.overlayDelayMs + s.overlayDurationMs),
}));
```

### `RecordingCaption.tsx`

**Do not use sequenced `<Caption>` components in recording mode.** Mounting a new `Caption` at each step boundary triggers the slide-up entrance animation repeatedly, and the small inter-step gap causes the bar to flash off and on — visible as glitching on every transition.

Instead, use a single persistent component that stays mounted for the full video duration:

```tsx
// src/flows/<flow-slug>/remotion/RecordingCaption.tsx
import React from 'react';
import { useCurrentFrame, interpolate } from 'remotion';
import { TIMED_STEPS } from '../data/flow';

// Never unmounts. Finds the active step from the frame and restarts
// the typewriter at each step boundary without any slide-up animation.
export const RecordingCaption: React.FC = () => {
  const frame = useCurrentFrame();

  // Only show captions for steps that have audio.
  // Steps where audioDuration > captionDuration are skipped for both audio and caption —
  // they are brief interaction steps (~450ms) with no room for narration.
  const step = [...TIMED_STEPS].reverse().find(
    s => frame >= s.captionStart && s.audioDuration <= s.captionDuration
  );
  if (!step) return null;

  const localFrame = frame - step.captionStart;
  const { caption } = step;
  const charCount = Math.floor(
    interpolate(localFrame, [0, caption.length * 0.75], [0, caption.length], {
      extrapolateLeft: 'clamp',   // required — without this, negative charCount causes slice(0,-N)
      extrapolateRight: 'clamp',  // which returns nearly the full string, flashing before typewriter
    })
  );
  const opacity = interpolate(frame, [step.captionStart, step.captionStart + 10], [0, 1], {
    extrapolateLeft: 'clamp', extrapolateRight: 'clamp',
  });

  return (
    <div className="tut-caption" style={{ opacity }}>
      {caption.slice(0, charCount)}
    </div>
  );
};
```

### `VideoComposition.tsx`

```tsx
// src/flows/<flow-slug>/remotion/VideoComposition.tsx
import React from 'react';
import { AbsoluteFill, OffthreadVideo, staticFile, Sequence, Audio } from 'remotion';
import { HighlightBox } from './overlays/HighlightBox';
import { RecordingCaption } from './RecordingCaption';
import { TIMED_STEPS } from '../data/flow';

export const VideoComposition: React.FC = () => (
  <AbsoluteFill>
    {/* Continuous Playwright recording — real interactions, no jump cuts */}
    <OffthreadVideo
      src={staticFile('recordings/<flow-slug>/recording.webm')}
      style={{ width: '100%', height: '100%' }}
      muted
    />

    {/* Highlight ring per step — sequenced per interaction */}
    {TIMED_STEPS.filter(s => s.highlight).map(step => (
      <Sequence key={`hl-${step.id}`} from={step.overlayStart} durationInFrames={step.overlayDuration}>
        <HighlightBox {...step.highlight!} showAt={0} />
      </Sequence>
    ))}

    {/* Audio narration — starts at captionStart, runs for captionDuration */}
    {TIMED_STEPS.map((step, i) => (
      <Sequence key={`audio-${step.id}`} from={step.captionStart} durationInFrames={step.captionDuration}>
        <Audio src={staticFile(`audio/<flow-slug>/step-${String(i + 1).padStart(2, '0')}.mp3`)} />
      </Sequence>
    ))}

    {/* Single persistent caption — never mounts/unmounts, no glitch between steps */}
    <RecordingCaption />
  </AbsoluteFill>
);
```

Register in `src/Root.tsx` (or `src/remotion-root.tsx`):

```tsx
import { msToFrame } from './flows/<flow-slug>/remotion/msToFrame';

// videoDurationMs comes from the manifest
<Composition
  id="RecordingTutorial"
  component={VideoComposition}
  durationInFrames={msToFrame(videoDurationMs)}
  fps={30}
  width={1920}
  height={1080}
/>
```

### Overlay timing rules for recording mode

| Step type | `overlayDelayMs` | `overlayDurationMs` |
|---|---|---|
| `mark` (orientation) | 200 | until next step − 300 |
| `click` | 400 — after click settles | until next step − 300 |
| `select` | 300 — after value updates | until next step − 300 |
| `fill` | 0 — as typing begins | until next step − 300 |
| Last step | 200 | remaining duration − 200 |

---

## Step 3: Read Manifest

After the user confirms the capture ran successfully, read the manifest:

```bash
cat public/screenshots/<flow-slug>/manifest.json
```

Report what was captured:

```
Manifest read: public/screenshots/<flow-slug>/manifest.json
Captured: 2024-11-15T14:32:07Z
Viewport: 1280×720
Steps: 7

  1  [none]  Dashboard overview
  2  [click] Click New Project         → .new-project-btn  (x:192, y:340, w:140, h:36)
  3  [fill]  Enter project name        → [placeholder="..."] (x:320, y:280, w:400, h:40)  "Q3 Launch Plan"
  4  [click] Select template           → [data-testid="template-card"] (x:480, y:440, w:200, h:120)
  5  [none]  Template selected
  6  [click] Click Create              → role=button[name="Create"] (x:640, y:560, w:120, h:40)
  7  [none]  Project created — success state
```

---

## Step 4: Component Discovery

Read every file at the provided `component_paths` (recursively if a directory).
For each component file, extract:

- **Export name** — component identifier for import statements
- **Relative path from project root** — used in scene file imports
- **Props interface** — all props with types, especially state-driving ones
- **Visual role** — page, form, card, shell/layout, modal, etc.
- **State-driving props** — props that change what the UI looks like

Cross-reference with the manifest: for each captured step, identify which
existing component most closely represents that UI state.

Present a discovery + mapping report:

```
Discovered components (N total):

  DashboardPage      src/pages/DashboardPage.tsx
    Props: workspaces: Workspace[], activeWorkspace?: string
    Role: page — state-driving: activeWorkspace

  NewProjectModal    src/features/projects/NewProjectModal.tsx
    Props: isOpen: boolean, onClose: fn, onSubmit: fn, defaultValues?: Partial<Project>
    Role: modal — state-driving: isOpen, defaultValues

  AppLayout          src/components/AppLayout.tsx
    Props: children: ReactNode, activePage?: string
    Role: shell — designated as scene wrapper

Component → step mapping:

  Step 1  DashboardPage      props: { workspaces: MOCK_WORKSPACES }
  Step 2  DashboardPage      props: { workspaces: MOCK_WORKSPACES }   (cursor on sidebar btn)
  Step 3  NewProjectModal    props: { isOpen: true, defaultValues: { name: "" } }
  Step 4  NewProjectModal    props: { isOpen: true, defaultValues: { name: "Q3 Launch Plan" } }
  ...
```

Ask: **"Does this mapping look right?"** Proceed only after confirmation.

---

## Step 5: Coordinate Scaling

Scale all element coordinates from viewport space to video space (1920×1080).

Generate `src/flows/<flow-slug>/remotion/coords.ts` — the scaling utility for this flow:

```typescript
// src/flows/<flow-slug>/remotion/coords.ts
// Scales browser-space coordinates to Remotion video space.
// Viewport and video dimensions are baked in from the captured manifest.

const VIEWPORT = { width: <viewport.width>, height: <viewport.height> } as const;
const VIDEO    = { width: 1920, height: 1080 } as const;
const SCALE_X  = VIDEO.width  / VIEWPORT.width;
const SCALE_Y  = VIDEO.height / VIEWPORT.height;

interface BrowserRect { x: number; y: number; width: number; height: number }
export interface VideoRect { x: number; y: number; w: number; h: number }

export function toVideoRect(el: BrowserRect): VideoRect {
  return {
    x: Math.round(el.x * SCALE_X),
    y: Math.round(el.y * SCALE_Y),
    w: Math.round(el.width  * SCALE_X),
    h: Math.round(el.height * SCALE_Y),
  };
}

export function toCursorCenter(el: BrowserRect): { x: number; y: number } {
  const r = toVideoRect(el);
  return { x: r.x + Math.round(r.w / 2), y: r.y + Math.round(r.h / 2) };
}
```

Apply scaling to every step that has an `element`. Store scaled results in
`data/flow.ts` alongside the step data — scenes import from there, not from
the manifest directly.

---

## Step 6: Gate A — Step Plan

Present the complete plan with scaled coordinates before writing any scene files:

```
Flow:     [FLOW-SLUG]
Task:     [TASK]
Scenes:   7
Duration: ~21s (estimate)

Step 1 — Dashboard overview
  Component:   DashboardPage (src/pages/DashboardPage.tsx)
  Props:       { workspaces: MOCK_WORKSPACES }
  Interaction: none
  Caption:     "Start from the main dashboard..."
  Duration:    60f (2s)

Step 2 — Click New Project
  Component:   DashboardPage
  Props:       { workspaces: MOCK_WORKSPACES }
  Interaction: click
  Cursor:      (288, 709) → scaled from (192, 340) @ 1280×720
  Highlight:   { x:210, y:693, w:210, h:75 } → scaled
  Caption:     "Click '+ New Project' in the sidebar..."
  Duration:    75f (2.5s)

Step 3 — Enter project name
  Component:   NewProjectModal
  Props:       { isOpen: true, defaultValues: { name: "" → "Q3 Launch Plan" } }
  Interaction: fill (typing animation)
  Cursor:      (480, 583)
  Highlight:   { x:240, y:560, w:960, h:84 }
  Caption:     "Type the project name..."
  Duration:    120f (4s)

...
```

Await:
- ✅ **APPROVED** — Proceed to scene generation
- 🔄 **REVISE** — [specific changes]
- ❌ **RESTART** — [new direction]

---

## Step 7: Generate `data/flow.ts`

All step data as typed constants — scaled coordinates baked in, no runtime math in scene files.

```typescript
// src/flows/<flow-slug>/data/flow.ts

export interface FlowStep {
  id: string;
  step: number;
  label: string;
  caption: string;
  interaction: 'click' | 'fill' | 'hover' | 'scroll' | 'none';
  cursor?: { x: number; y: number };
  highlight?: { x: number; y: number; w: number; h: number };
  typedValue?: string;
  typingProp?: string;
}

export const FLOW_STEPS: FlowStep[] = [
  {
    id: 'step-01',
    step: 1,
    label: 'Dashboard overview',
    caption: 'Start from the main dashboard. The sidebar shows all your workspaces.',
    interaction: 'none',
  },
  {
    id: 'step-02',
    step: 2,
    label: 'Click New Project',
    caption: "Click '+ New Project' in the sidebar to open the creation dialog.",
    interaction: 'click',
    cursor:    { x: 288, y: 709 },
    highlight: { x: 210, y: 693, w: 210, h: 75 },
  },
  {
    id: 'step-03',
    step: 3,
    label: 'Enter project name',
    caption: 'Type the project name. This becomes the title shown across all views.',
    interaction: 'fill',
    cursor:    { x: 480, y: 583 },
    highlight: { x: 240, y: 560, w: 960, h: 84 },
    typedValue: 'Q3 Launch Plan',
    typingProp: 'name',
  },
  // ...
];
```

---

## Step 8: Scene Generation

Generate `src/flows/<flow-slug>/remotion/scenes/Scene_0N.tsx` for each step.

### Scene template — click interaction

```tsx
// src/flows/<flow-slug>/remotion/scenes/Scene_02.tsx
import React from 'react';
import { AbsoluteFill, useCurrentFrame, interpolate } from 'remotion';
import { DashboardPage } from '../../../../src/pages/DashboardPage';
import { AppLayout } from '../../../../src/components/AppLayout';
import { CursorOverlay } from '../overlays/CursorOverlay';
import { ClickRipple } from '../overlays/ClickRipple';
import { HighlightBox } from '../overlays/HighlightBox';
import { Caption } from '../overlays/Caption';
import { FLOW_STEPS } from '../../data/flow';
import { MOCK_WORKSPACES } from '../../data/mocks';

const STEP = FLOW_STEPS[1];
const CLICK_AT = 45;

export const Scene_02: React.FC = () => {
  const frame = useCurrentFrame();
  const opacity   = interpolate(frame, [0, 12],  [0, 1],  { extrapolateRight: 'clamp' });
  const hlOpacity = interpolate(frame, [20, 32], [0, 1],  { extrapolateRight: 'clamp' });

  return (
    <AbsoluteFill style={{ opacity }}>
      <AppLayout activePage="dashboard">
        <DashboardPage workspaces={MOCK_WORKSPACES} />
      </AppLayout>
      <HighlightBox {...STEP.highlight!} frame={frame} showAt={20} />
      <CursorOverlay x={STEP.cursor!.x} y={STEP.cursor!.y} frame={frame} clickAt={CLICK_AT} />
      <ClickRipple   x={STEP.cursor!.x} y={STEP.cursor!.y} frame={frame} triggerAt={CLICK_AT} />
      <Caption text={STEP.caption} frame={frame} />
    </AbsoluteFill>
  );
};
```

### Scene template — fill/typing interaction

```tsx
// src/flows/<flow-slug>/remotion/scenes/Scene_03.tsx
import React from 'react';
import { AbsoluteFill, useCurrentFrame, interpolate } from 'remotion';
import { NewProjectModal } from '../../../../src/features/projects/NewProjectModal';
import { AppLayout } from '../../../../src/components/AppLayout';
import { CursorOverlay } from '../overlays/CursorOverlay';
import { HighlightBox } from '../overlays/HighlightBox';
import { Caption } from '../overlays/Caption';
import { FLOW_STEPS } from '../../data/flow';

const STEP = FLOW_STEPS[2];
const FULL_VALUE = STEP.typedValue!;  // "Q3 Launch Plan"
const TYPE_START = 30;
const TYPE_END   = 100;

export const Scene_03: React.FC = () => {
  const frame = useCurrentFrame();
  const opacity   = interpolate(frame, [0, 12], [0, 1], { extrapolateRight: 'clamp' });
  const hlOpacity = interpolate(frame, [15, 27], [0, 1], { extrapolateRight: 'clamp' });

  const charCount = Math.floor(
    interpolate(frame, [TYPE_START, TYPE_END], [0, FULL_VALUE.length], { extrapolateRight: 'clamp' })
  );
  const typedName = FULL_VALUE.slice(0, charCount);

  return (
    <AbsoluteFill style={{ opacity }}>
      <AppLayout activePage="dashboard">
        <NewProjectModal
          isOpen
          defaultValues={{ name: typedName }}
          onClose={() => {}}
          onSubmit={() => {}}
        />
      </AppLayout>
      <HighlightBox {...STEP.highlight!} frame={frame} showAt={15} />
      <CursorOverlay x={STEP.cursor!.x} y={STEP.cursor!.y} frame={frame} />
      <Caption text={STEP.caption} frame={frame} />
    </AbsoluteFill>
  );
};
```

### Import path rule

Always use relative paths from the scene file to the existing source file.
Never use path aliases (`@/`) unless confirmed working in the Remotion bundler
(check `remotion.config.ts` for `webpackOverride` or `vitePlugin` alias config).

### Mock data

If a component requires data (workspaces list, user object, etc.) that only
exists at runtime, generate `src/flows/<flow-slug>/data/mocks.ts` with typed
placeholder values that match the component's prop shape. Use realistic values —
the video will show this data on screen.

### Props that don't exist

If a step requires a UI state the existing component cannot express via props,
choose one resolution and note it in Gate C:

| Situation | Resolution |
|---|---|
| State is visually important, no prop exists | Propose a minimal `__tutorialHighlight?: string` prop addition to the existing file |
| State is minor / cosmetic | Overlay a `HighlightBox` or `Tooltip` directly in the scene — no component change |
| Component has no useful state-driving props | Report at Gate A: recommend switching to `software-tutorial-studio` (screenshot mode) for that step |

---

## Overlay Components

Generated once per project in `src/flows/<flow-slug>/remotion/overlays/`.
Same visual language as `ui-flow-studio` — all visual styles in `src/index.css`.

### `HighlightBox.tsx`
```
Props: x, y, w, h, frame, showAt, color?
- className="tut-highlight" from src/index.css
- Entrance opacity at showAt via style={{ opacity: interpolate(...) }}
- Pulse scale via style={{ transform }}
```

### `CursorOverlay.tsx`
```
Props: x, y, frame, clickAt?
- className="tut-cursor" from src/index.css
- SVG cursor at (x, y)
- If clickAt: scale pulse via spring()
```

### `ClickRipple.tsx`
```
Props: x, y, frame, triggerAt
- className="tut-ripple" from src/index.css
- Scale 0 → 2.5, opacity 0.5 → 0 over 20 frames
```

### `Caption.tsx`
```
Props: text, frame
- className="tut-caption" from src/index.css
- Slide up from bottom over 10 frames
- Typewriter text reveal
```

Add these to `src/index.css` under `@layer components` if not already present:

```css
/* ── Playwright Tutorial Overlays ──────────────────────────────── */
.tut-caption   { @apply absolute bottom-0 left-0 right-0 flex items-center px-8 font-sans; background: rgba(0,0,0,0.75); height: 64px; color: white; font-size: 1.125rem; }
.tut-highlight { @apply absolute rounded-lg pointer-events-none; border: 2px solid #3B82F6; background: rgba(59,130,246,0.15); }
.tut-ripple    { @apply absolute rounded-full pointer-events-none; border: 2px solid #60A5FA; }
.tut-cursor    { @apply absolute pointer-events-none; filter: drop-shadow(0 2px 4px rgba(0,0,0,0.5)); }
```

---

## `flowTimings.ts`

```typescript
// src/flows/<flow-slug>/remotion/flowTimings.ts

export const FLOW_TIMINGS = {
  fps: 30,
  scenes: [
    { id: 'step-01', label: 'Dashboard overview',  start: 0,   duration: 60  },
    { id: 'step-02', label: 'Click New Project',   start: 60,  duration: 75  },
    { id: 'step-03', label: 'Enter project name',  start: 135, duration: 120 },
    // ...
  ],
  totalFrames: 0, // sum computed at generation time
} as const;
```

Default durations by interaction type — minimum values. Increase if captions are long:

| Interaction | Duration | Reasoning |
|---|---|---|
| none (establish/result) | **150f (5s)** | Caption typewriter ~2s + ~1.5s reading time at rest |
| click | **150f (5s)** | Same — click is fast, caption needs the time |
| fill (short < 20 chars) | **120f (4s)** | Typing animation + read time |
| fill (long 20+ chars) | **150f (5s)** | — |
| hover | 90f (3s) | Tooltip visible |
| scroll | 90f (3s) | Smooth scroll |
| success / final state | **180f (6s)** | Last frame — hold extra long |

**Why 5s minimum:** The `Caption` typewriter runs at ~40 chars/sec. A typical 80-char caption takes ~2s to finish typing. The viewer then needs at least 1.5s of settled reading time. 2s scenes (60f) guaranteed cut mid-caption.

---

## `FlowComposition.tsx`

```tsx
// src/flows/<flow-slug>/remotion/FlowComposition.tsx
import React from 'react';
import { Sequence } from 'remotion';
import { FLOW_TIMINGS } from './flowTimings';
import { Scene_01 } from './scenes/Scene_01';
import { Scene_02 } from './scenes/Scene_02';
// ... one import per scene

const SCENES = [Scene_01, Scene_02, /* ... */];

export const FlowComposition: React.FC = () => (
  <>
    {FLOW_TIMINGS.scenes.map((scene, i) => {
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
  id="PlaywrightTutorial"
  component={FlowComposition}
  durationInFrames={FLOW_TIMINGS.totalFrames}
  fps={30}
  width={1920}
  height={1080}
/>
```

---

## Gate C — Review Before Render

```
Flow:     [FLOW-SLUG]
Task:     [TASK]
Scenes:   N  |  Duration: ~Xs  |  Output: [FILENAME]

Capture:
  Source:   scripts/<flow-slug>-capture.ts
  Manifest: public/screenshots/<flow-slug>/manifest.json
  Viewport: 1280×720  →  scaled to 1920×1080 (1.5× both axes)

Component mapping:
  ✅ Step 1 — DashboardPage       (src/pages/DashboardPage.tsx)
  ✅ Step 2 — DashboardPage       click at (288, 709)
  ✅ Step 3 — NewProjectModal     typing "Q3 Launch Plan" into name prop
  ✅ Step 4 — NewProjectModal     name complete, submit highlighted
  ...

Prop issues (if any):
  ⚠️  Step 5 — ProjectCard has no highlight prop — using HighlightBox overlay instead

Mock data: src/flows/<flow-slug>/data/mocks.ts

Ready to render?
```

Await GO / ADJUST.

---

## Gate D — Testing Phase

**Do not start the render until this gate passes and the user confirms.**

Run the full testing sequence in order. Report every result to the user. Only after all checks pass and the user says "go" should you proceed to the render.

### 1. TypeScript type-check

```bash
npx tsc --noEmit
```

All generated files (`data/flow.ts`, `data/mocks.ts`, `remotion/flowTimings.ts`, `remotion/scenes/Scene_*.tsx`, `remotion/overlays/*.tsx`) must compile without errors. Fix any type errors before continuing.

### 2. Extract a Remotion still for every scene

```bash
# Run for every scene — frame = scene.start + 20 (past entrance animation)
npx remotion still PlaywrightTutorial --frame=<scene.start + 20> \
  --output=public/screenshots/<flow-slug>/verify-scene<N>.png
```

Open all stills:

```bash
open public/screenshots/<flow-slug>/verify-scene*.png
```

### 3. Cross-reference with captured screenshots

For every annotated scene, compare:
- `verify-scene<N>.png` (Remotion still) — highlight box / cursor position
- `step-<N>.png` (original Playwright screenshot) — actual element position

The highlight ring must sit on the correct element in both images. If it is off, the coordinate scaling is the first thing to check: re-read the manifest `viewport` and confirm `SCALE_X` / `SCALE_Y` in `coords.ts`.

### 4. Present testing summary to the user

Report the outcome of every check before asking to proceed:

```
Testing phase complete

TypeScript: ✅ 0 errors

Remotion stills:
  Scene 1  public/screenshots/<flow-slug>/verify-scene1.png  ✅ overlay correct
  Scene 2  public/screenshots/<flow-slug>/verify-scene2.png  ✅ highlight on correct element
  Scene 3  public/screenshots/<flow-slug>/verify-scene3.png  ✅ cursor positioned correctly
  ...

All N scenes verified.

Ready to render? (yes / adjust first)
```

Do not proceed until the user explicitly confirms. If the user wants adjustments, fix them, re-run the affected stills, and present a revised summary before asking again.

---

## Render

### Remotion entry file requirement

The entry file passed to `remotion render` / `remotion still` **must call `registerRoot()`** — exporting the root component is not enough:

```tsx
// src/remotion-root.tsx
import { registerRoot } from 'remotion';
const RemotionRoot = () => <><Composition .../></>;
registerRoot(RemotionRoot); // ← required
```

### Full render

**Always run from the project root directory** — Remotion resolves `public/` and `remotion.config.ts` relative to the CWD. Running from a different directory causes `staticFile()` URLs to 404 silently.

```bash
cd /path/to/project   # ← must be the project root, not a parent directory
node_modules/.bin/remotion render src/remotion-root.tsx <CompositionId> \
  output/<flow-slug>-<YYYYMMDD>.mp4 \
  --codec=h264 \
  --crf=18
```

---

## Output Structure

```
scripts/
├── playwright-capture.ts         ← reusable capture helper (written once)
└── <flow-slug>-capture.ts        ← flow-specific capture script

public/screenshots/<flow-slug>/
├── manifest.json                 ← step sequence, coordinates, viewport
├── step-01.png                   ← reference screenshots (not used in video)
├── step-02.png
└── ...

src/flows/<flow-slug>/
├── data/
│   ├── flow.ts                   ← step data + scaled coordinates
│   └── mocks.ts                  ← typed placeholder data for component props
├── remotion/
│   ├── FlowComposition.tsx
│   ├── coords.ts                 ← toVideoRect / toCursorCenter utilities
│   ├── flowTimings.ts
│   ├── scenes/
│   │   ├── Scene_01.tsx          ← imports from existing app components
│   │   ├── Scene_02.tsx
│   │   └── ...
│   └── overlays/
│       ├── HighlightBox.tsx
│       ├── CursorOverlay.tsx
│       ├── ClickRipple.tsx
│       └── Caption.tsx

output/
└── <flow-slug>-<YYYYMMDD>.mp4   ← final render
```

No `components/` directory is ever created. All scene imports point to the
user's existing source files.

---

## CSS Architecture Rule — MANDATORY

All CSS lives in `src/index.css`. No exceptions.

- **Never** write inline visual styles in overlay or scene components
- `style={{}}` only for animated values driven by `useCurrentFrame()` / `interpolate()` / `spring()`
- Check `src/index.css` for existing `.tut-*` classes before adding new ones
- Overlay components (`Caption`, `HighlightBox`, `CursorOverlay`, `ClickRipple`) reference
  classes from `src/index.css` — never hardcoded color/size values in JSX

---

## Final Checklist

### Setup
- [ ] Preflight passed — Playwright, tsx, Remotion, app URL all verified
- [ ] `scripts/playwright-capture.ts` written to project

### Capture (capture entry)
- [ ] `scripts/<flow-slug>-capture.ts` generated and reviewed by user
- [ ] Capture script run — `manifest.json` confirmed present
- [ ] Manifest read and step summary reported

### Analysis
- [ ] Component discovery complete — props and visual roles documented
- [ ] Component-to-step mapping confirmed by user
- [ ] Coordinates scaled from viewport to video space in `coords.ts`
- [ ] Step plan presented and approved (Gate A)

### Generation
- [ ] `data/flow.ts` generated — scaled coordinates baked in
- [ ] `data/mocks.ts` generated — realistic typed placeholder data
- [ ] `remotion/flowTimings.ts` generated — complete frame map
- [ ] All scene files generated — imports point to existing app paths
- [ ] All overlay files generated
- [ ] `FlowComposition.tsx` assembled
- [ ] Composition registered in `src/Root.tsx`
- [ ] `.tut-*` overlay classes present in `src/index.css`
- [ ] Any prop-gap situations documented and resolved
- [ ] Gate C review approved

### Testing (Gate D — must complete before render)
- [ ] TypeScript type-check passed — 0 errors across all generated files
- [ ] Remotion still extracted for every scene
- [ ] All stills cross-referenced against captured screenshots — overlays on correct elements
- [ ] Testing summary presented to user
- [ ] User confirmed "go" before render started

### Render
- [ ] Full render completed
- [ ] Output: `output/<flow-slug>-<YYYYMMDD>.mp4`
