---
name: ui-flow-studio
description: >
  Generate UI tutorial videos and interactive components from the same source.
  Describe a task flow, a UI mockup idea, or a component with states — the skill
  produces a Remotion animation AND deployable React/Tailwind components in one pass.
  Four modes: Tutorial, Mockup, State Demo, Live Components (reuses existing app components).
metadata:
  tags: remotion, tailwind, react, tutorial, ui, animation, components, dual-use, onboarding, prototype
---

# Claude Code Skill: UI Flow Studio

Turns UI descriptions into **Remotion tutorial videos** and **interactive
React/Tailwind components** from a single generation pass.

One source of truth. Two usable outputs.

---

## Modes at a Glance

| Mode | You Describe | You Get |
|---|---|---|
| `tutorial` | An app + a task a user performs | Step-by-step animated walkthrough video + per-step components |
| `mockup` | A feature or screen idea | Explorable UI mockup video + interactive prototype + **live `npm run dev:site` page** |
| `state-demo` | A component + its states | State-transition video + live component with all states wired |
| `live-components` | Paths to existing components + a task | Tutorial video that imports **your** components — no new UI code generated |

---

## Activation

```
🎬 Activate UI Flow Studio

Mode: [tutorial | mockup | state-demo | live-components]

# For tutorial mode:
App: [app name or description]
Task: [what the user is doing, e.g. "create a new project and invite a teammate"]
UI Style: [minimal | material | shadcn | custom — optional, defaults to minimal]

# For mockup mode:
Feature: [describe the screen or feature]
Interaction: [what a user does on this screen — optional]
UI Style: [same options]

# For state-demo mode:
Component: [describe the component]
States: [list the states, e.g. "idle, loading, success, error"]
UI Style: [same options]

# For live-components mode:
Components: [one or more paths — e.g. "src/components/", "src/features/checkout/CheckoutForm.tsx"]
Task: [what the user is doing — e.g. "complete a checkout flow"]
Shell: [optional — path to a layout/shell component that wraps all scenes]
```

> `🎬 Activate UI Flow Studio` is the **only** trigger.
> Do not activate from unrelated messages.

---

## Session Context

Initialize at activation and maintain across all steps:

```
mode:             <tutorial | mockup | state-demo | live-components>
app_or_feature:   <confirmed subject>
task_or_states:   <confirmed flow or state list>
ui_style:         <minimal | material | shadcn | custom | existing>
steps:            [] ← populated in Step 2
flow_slug:        <kebab-case identifier, e.g. "notion-create-project">
render_output:    output/<flow-slug>-<YYYYMMDD>.mp4

# live-components mode only:
component_paths:  <list of resolved paths or globs provided at activation>
shell_path:       <optional — path to existing shell/layout component>
discovered:       [] ← populated during Step 0c (component discovery)
```

---

## Autonomy Rules

### Claude decides autonomously
- Step breakdown and step count for tutorial/mockup flows
- UI panel layout and component structure per step
- Cursor position, interaction type (click, type, hover, drag) per step
- State transition timing and easing curves
- Which Tailwind tokens to use within the selected UI style
- Caption/annotation text per step
- Component prop interfaces
- *(live-components)* Which existing component maps to each tutorial step
- *(live-components)* Which props to pass at each frame to drive the tutorial state

### Claude must ask the user
- Mode and subject (activation)
- UI style if not provided (Step 0) — skipped in live-components mode
- Step plan approval (Gate A)
- Whether to proceed past each gate
- *(live-components)* Confirm component-to-step mapping before generating scenes

---

## Component Libraries Available

Two pre-built libraries are installed and ready to use alongside the custom design system in `src/index.css`.

### DaisyUI
- **Installed as:** `daisyui` npm package + `@plugin "daisyui"` in `src/index.css`
- **Usage:** Pure CSS class names (e.g. `btn`, `badge`, `card`, `stat`, `alert`, `progress`)
- **When to use in video scenes (Remotion):** Yes — DaisyUI is pure CSS, renders perfectly in every Remotion frame. Ideal for quick UI elements in rendered panels (Mode A/URL-based, no screenshots): buttons, badges, stats, form inputs, alerts, progress bars.
- **When to use in web components (`components/`):** Yes — great for the standalone interactive page and state-demo wrappers.
- **Docs:** `https://daisyui.com/components/`

### shadcn/ui
- **Installed as:** `components.json` config + `src/lib/utils.ts` (`cn()` helper) + deps: `clsx`, `tailwind-merge`, `class-variance-authority`, `lucide-react`
- **Add components via CLI:** `npx shadcn@latest add button card badge input` etc.
- **Components land in:** `src/components/ui/`
- **When to use in video scenes (Remotion):** Static visual components only (Button, Card, Badge, Input, Avatar) — they render fine as Remotion captures static frames. Avoid interactive primitives (Dialog, Popover, Select, DropdownMenu) in scenes — they depend on browser event state that Remotion's renderer doesn't drive.
- **When to use in web components (`components/`):** Yes — preferred for the standalone interactive page and any component that will be deployed to a real app. shadcn components are production-quality and composable.
- **Import pattern:**
```tsx
import { Button } from "@/components/ui/button";
import { Card, CardContent } from "@/components/ui/card";
import { cn } from "@/lib/utils";
```

### Decision guide

| Need | Use |
|---|---|
| Quick badge / stat / alert in a video panel | DaisyUI (`badge`, `stat`, `alert`) |
| Polished button or card in a video panel | shadcn Button / Card |
| Full interactive web page (mockup standalone) | shadcn (primary) + DaisyUI for accents |
| State-demo interactive wrapper | shadcn for the shell, DaisyUI for state indicators |
| Custom brand styling for a flow | Custom classes in `src/index.css` (`.tt-*`, `.flow-*` etc.) |

---

## UI Styles

| ID | Aesthetic | Tailwind Basis |
|---|---|---|
| `minimal` | White bg, gray-900 text, blue-600 accent, sharp corners | Tailwind defaults, no radius |
| `material` | White bg, gray-800 text, indigo-500 accent, rounded-lg | Material density, elevation shadows |
| `shadcn` | White/zinc bg, zinc-900 text, black accent, rounded-md | shadcn/ui components from `src/components/ui/` |
| `daisy` | DaisyUI theme, white/neutral base, semantic color tokens | DaisyUI class names (`btn`, `card`, `badge`, etc.) |
| `custom` | User-defined | Claude asks for 3 tokens: bg, text, accent |

---

## Step 0: Style Confirmation

If `UI Style` was not provided at activation:

```
Which UI style should be used for generated components and video?

1. ⬜ Minimal   — white canvas, blue accent, sharp edges
2. 🎨 Material  — cards with elevation, indigo, rounded
3. 🖤 shadcn    — zinc palette, high contrast, radii
4. 🎛️ Custom    — you define bg / text / accent colors
```

Once confirmed, initialize `ui_style` in session context and load the
corresponding token set (see **Token Reference** section at end of this file).

For `shadcn` style: check that `src/components/ui/` has the needed components. If not, run `npx shadcn@latest add <component>` before generating scenes.
For `daisy` style: DaisyUI is already active globally — use class names directly, no install step needed.

Run the **Preflight Check**.

---

## Step 0b: Preflight Check

### Files
- [ ] `src/flows/` directory exists or will be created
- [ ] `src/flows/<flow-slug>/` will be created for this session
- [ ] Remotion project initialized (`package.json` has `remotion`)
- [ ] `remotion.config.ts` present
- [ ] `@remotion/tailwind-v4` and `tailwindcss` in devDependencies
- [ ] `src/index.css` starts with `@import "tailwindcss"` and has `@theme` block
- [ ] `src/Root.tsx` imports `./index.css`

### Optional Capabilities

| Capability | Env Variable | Fallback |
|---|---|---|
| Custom fonts | None needed | System sans-serif stack |
| Screenshot assets | User-provided to `public/flows/<flow-slug>/` | Placeholder panels |

```
✅ Preflight passed. Proceeding with [MODE] flow: [FLOW-SLUG]
```

---

## Step 0c: Component Discovery (live-components mode only)

Skip this step for all other modes.

Read every file at the provided `component_paths` (recursively if a directory). For each component file, extract:

- **Export name** — the component identifier to import
- **Relative path from project root** — used for import statements in scene files
- **Props interface** — enumerate all props with their types (especially optional ones that control visual state)
- **Visual role** — infer from the component name and props: is it a page, a form, a card, a shell/layout, a modal, etc.?
- **State-driving props** — identify props that change what the UI looks like: `isLoading`, `activeStep`, `error`, `value`, `selected`, etc.

Present a discovery report:

```
Discovered components (N total):

  CheckoutForm       src/features/checkout/CheckoutForm.tsx
    Props: step: 1|2|3, values: CheckoutValues, onNext: fn, isSubmitting: boolean
    Role: multi-step form — state-driving props: step, isSubmitting

  OrderSummary       src/features/checkout/OrderSummary.tsx
    Props: items: CartItem[], total: number, promoApplied?: boolean
    Role: summary panel — state-driving props: promoApplied

  AppLayout          src/components/AppLayout.tsx
    Props: children: ReactNode, activePage?: string
    Role: shell — will wrap all scenes
    → Designated as shell (matches Shell: input)
```

If `Shell:` was provided at activation, mark the matching component as the scene wrapper. If it was not provided but a clear layout/shell component is found, suggest it and ask for confirmation in one line.

After the report, ask: **"Does this mapping look right, or should any component be re-assigned?"**

Proceed only after the user confirms.

---

## Output Structure (All Modes)

```
src/flows/<flow-slug>/
├── components/               ← pure React/Tailwind — zero Remotion, deployable anywhere
│   ├── AppShell.tsx          ← outer chrome: nav, sidebar, topbar (if applicable)
│   ├── Step_01.tsx           ← one file per step or state
│   ├── Step_02.tsx
│   └── ...
├── remotion/
│   ├── FlowComposition.tsx   ← main Remotion composition
│   ├── scenes/
│   │   ├── Scene_01.tsx      ← Remotion wrapper: imports Step_01 + adds animation
│   │   ├── Scene_02.tsx
│   │   └── ...
│   ├── overlays/
│   │   ├── CursorOverlay.tsx ← animated cursor (tutorial mode)
│   │   ├── ClickRipple.tsx   ← click feedback animation
│   │   ├── Tooltip.tsx       ← step annotation callout
│   │   └── Caption.tsx       ← bottom caption bar
│   └── flowTimings.ts        ← frame map for all scenes
├── data/
│   └── flow.ts               ← all step data, captions, interaction descriptors
├── style.ts                  ← active token references for this flow
├── <FlowSlug>App.tsx         ← (mockup mode only) interactive app with useState routing
└── site.tsx                  ← (mockup mode only) Vite entry point for standalone page
```

**Mockup mode** also creates two root-level files (once per project, not per flow):
- `site.html` — HTML entry point, loads `site.tsx` via Vite
- `vite.config.ts` — Vite config pointing at `site.html`

And adds to `package.json`:
```json
"dev:site":   "vite --config vite.config.ts",
"build:site": "vite build --config vite.config.ts"
```

Running `npm run dev:site` opens the standalone interactive page at `http://localhost:5174/site.html`.

**live-components mode output** — no `components/` directory is generated:

```
src/flows/<flow-slug>/
├── remotion/
│   ├── FlowComposition.tsx   ← imports existing components, not generated ones
│   ├── scenes/
│   │   ├── Scene_01.tsx      ← imports from existing app paths
│   │   ├── Scene_02.tsx
│   │   └── ...
│   ├── overlays/             ← same overlays as tutorial mode
│   │   ├── CursorOverlay.tsx
│   │   ├── ClickRipple.tsx
│   │   ├── Tooltip.tsx
│   │   └── Caption.tsx
│   └── flowTimings.ts
└── data/
    └── flow.ts               ← step data, prop snapshots, cursor positions
```

No new component files are written. All `import` statements in scene files point to the user's existing source paths.

---

## Dual-Use Architecture Rule

**Base components (`components/`)** — zero Remotion primitives:
- Pure React + Tailwind
- No `useCurrentFrame()`, `interpolate()`, `spring()`
- No `<Audio>`, `<Video>`, `<Sequence>`
- Accept only data props + optional `className` + optional `activeState?: string`
- Directly deployable into any React project

**Remotion wrappers (`remotion/scenes/`)** — animation only:
- Import the base component, add entrance/transition animation
- Use `useCurrentFrame()` + `interpolate()` + `spring()`
- Compose overlays (cursor, ripple, caption) on top
- Never duplicate visual markup — all UI structure lives in the base

**CSS Architecture Rule — MANDATORY:**
- All CSS class definitions live exclusively in `src/index.css` under `@layer components`
- **Never** write CSS in `.tsx` files, `<style>` tags, separate `.css` files, or `styled-components`
- **Never** use `style={{}}` for visual properties — only for values driven by `useCurrentFrame()` / `interpolate()` / `spring()`
- Before generating any component, check `src/index.css` for existing classes that satisfy the need (`.tt-*`, `.vwi-*`, `.web-*`, `.flow-*`, etc.)
- If no existing class covers the need, add a new named block to `src/index.css` first, then reference it in the component
- Custom brand styles for a new flow go into `src/index.css` as a clearly labelled section (e.g. `/* ── UI Flow Studio: MyFlow ──── */`) — never inlined

```tsx
// ✅ Correct — base component: pure UI, no Remotion
// src/flows/notion-create-project/components/Step_02.tsx
export const Step_02: React.FC<Step02Props> = ({ projectName, highlighted }) => (
  <div className="flow-panel">
    <input
      className={cn("flow-input", highlighted && "flow-input--focused")}
      placeholder="Project name"
      value={projectName}
    />
    <button className="flow-btn-primary">Create project</button>
  </div>
);

// ✅ Correct — Remotion wrapper: animation + overlays only
// src/flows/notion-create-project/remotion/scenes/Scene_02.tsx
export const Scene_02: React.FC = () => {
  const frame = useCurrentFrame();
  const { fps } = useVideoConfig();
  const opacity = interpolate(frame, [0, 12], [0, 1], { extrapolateRight: "clamp" });
  const y = interpolate(frame, [0, 12], [16, 0], { extrapolateRight: "clamp" });
  const typedChars = Math.floor(interpolate(frame, [20, 50], [0, 14], { extrapolateRight: "clamp" }));

  return (
    <AbsoluteFill className="bg-white" style={{ opacity }}>
      <div style={{ transform: `translateY(${y}px)` }}>
        <AppShell>
          <Step_02 projectName={"My New Project".slice(0, typedChars)} highlighted />
        </AppShell>
      </div>
      <CursorOverlay x={640} y={380} frame={frame} clickAt={55} />
      <Caption text="Type the project name and press Create" frame={frame} />
    </AbsoluteFill>
  );
};
```

---

## Mode Workflows

---

### 🎓 TUTORIAL MODE

#### Step 1: Task Analysis

From the activation input, infer:
- **App type** (dashboard, editor, CRM, dev tool, etc.)
- **User role** performing the task (admin, end user, developer)
- **Complexity** — how many discrete UI interactions are involved
- **App chrome** needed — does the task require nav, sidebar, modal, breadcrumbs?

Ask **at most 1 clarifying question** if the task is ambiguous.

#### Step 2: Step Breakdown

Decompose the task into discrete steps. Each step = one scene in the video.

For each step, define:

```
Step N:
  label:        <short action label — "Click New Project">
  caption:      <full sentence for caption bar — "Click the + New Project button in the sidebar">
  ui_panel:     <what the user sees — described structurally>
  interaction:  <click | type | hover | drag | scroll | none>
  target:       <what UI element is being interacted with>
  result:       <what changes after interaction>
```

**Step count guidelines:**
- Simple task (< 3 interactions): 3–5 steps
- Medium task (3–6 interactions): 5–8 steps
- Complex task (6+ interactions): 8–12 steps, consider splitting into sub-flows

Always include:
- **Step 1:** Initial state — where the user starts
- **Step N:** Final state — task complete, success feedback visible

#### Step 3: Approval Gate A — Step Plan

Present:
```
Flow: [FLOW-SLUG]
Total scenes: N
Estimated video length: ~Xs

Step 1: [label] — [caption]
Step 2: [label] — [caption]
...
Step N: [label] — [caption]
```

Await:
- ✅ **APPROVED** — Proceed to component generation
- 🔄 **REVISE** — [specific changes]
- ❌ **RESTART** — [new direction]

#### Step 4: App Shell Design

Design the `AppShell.tsx` component — the persistent outer chrome:

- Decide which chrome elements are present: topbar / sidebar / breadcrumb / none
- Generate the shell as a pure Tailwind component
- Shell accepts `children` for the content area
- Shell accepts `activeNav?: string` prop for highlighting nav items

#### Step 5: Step Component Generation

For each step, generate:

**`components/Step_0N.tsx`** — the UI panel at that step:
- Extends `AppShell` or stands alone if no shell
- Shows the UI state *before* the interaction completes (interaction happens in the scene)
- Accepts props for any dynamic values (typed text, selected items, loaded data)
- Uses `activeState` prop if the component has a highlighted/focused element

**`remotion/scenes/Scene_0N.tsx`** — the Remotion wrapper:
- Imports `Step_0N`
- Applies entrance animation (fade + translate Y, 12-frame default)
- Composes appropriate overlays:
  - `CursorOverlay` for click/hover/drag interactions
  - Typing animation via `interpolate` on string slice for type interactions
  - `ClickRipple` on click frame
  - `Caption` at bottom with the step caption
- Drives any prop changes (typed text, state transitions) via `interpolate`

---

### 🖥️ MOCKUP MODE

#### Step 1: Feature Analysis

From the activation input, infer:
- **Screen type** (dashboard, settings page, onboarding, modal, data table, etc.)
- **Primary action** the user takes on this screen
- **Data density** (sparse / medium / dense)
- **Interaction depth** — does the screen have sub-states or is it static?

#### Step 2: Scene Planning

Plan the mockup as a video journey through the screen:

```
Scene 1: Establish — full screen shown, no interaction (2–3s)
Scene 2: Highlight — zoom or spotlight on primary action area (2s)
Scene 3: Interact — animate the primary interaction (2–4s)
Scene 4: Result — show the post-interaction state (2–3s)
Scene 5: Overview — pull back to show full screen with result (2s)
```

Adjust scene count based on screen complexity. Present as Gate A.

#### Step 3: Approval Gate A — Scene Plan

Same format as Tutorial Gate A. Await approval.

#### Step 4: Component + Scene Generation

Generate:
- `components/Screen.tsx` — the full mockup screen as a deployable component
  - Accepts `activeState?: "default" | "interacted" | "result"` prop
  - All states renderable without Remotion
- `components/ScreenData.tsx` — realistic placeholder data as typed constants
- Remotion scenes that animate through the mockup journey

#### Step 5: Standalone Page (Mockup Mode — Always)

After components are generated, always produce the standalone interactive page:

**`<FlowSlug>App.tsx`** — the interactive React app:
- Uses `useState` to track the current view (hub / selected item / etc.)
- Wires `onClick` / `onBack` props between `ServicesHub` and `SolutionPage` (or equivalent)
- No Remotion — runs in any browser via Vite
- Pattern:
```tsx
export const <FlowSlug>App: React.FC = () => {
  const [view, setView] = useState<"hub" | string>("hub");
  if (view !== "hub") return <DetailPage id={view} onBack={() => setView("hub")} />;
  return <HubPage onItemClick={(id) => setView(id)} />;
};
```

**`site.tsx`** — Vite entry:
```tsx
import React from "react";
import { createRoot } from "react-dom/client";
import { <FlowSlug>App } from "./<FlowSlug>App";
import "../../index.css";
createRoot(document.getElementById("root")!).render(<<FlowSlug>App />);
```

**Root-level files** (create once; skip if already present):
- `site.html` — HTML shell that loads `site.tsx` via `<script type="module">`
- `vite.config.ts` — Vite config with `root: "."`, `build.rollupOptions.input: "site.html"`, `server.open: "/site.html"`

**`package.json` scripts** (add if not present):
```json
"dev:site":   "vite --config vite.config.ts",
"build:site": "vite build --config vite.config.ts"
```

Announce at Gate C:
```
Standalone page: npm run dev:site → http://localhost:5174/site.html
```

#### Step 6: Interaction Depth

If `Interaction` was provided at activation, also generate:
- A second variant of `Screen.tsx` showing the interactive state
- `Scene_Interact.tsx` that transitions between the two states using `spring()`

---

### 🔲 STATE-DEMO MODE

#### Step 1: State Analysis

From the activation input, enumerate all states:
- Parse user-provided state list
- Infer any missing transitional states (e.g. if user lists "idle" and "success", infer "loading")
- For each state, define:

```
State: [name]
  visual_change: <what looks different vs idle>
  trigger:       <what causes entry into this state>
  duration:      <instantaneous | brief (< 1s) | sustained>
  exit_to:       <which state follows>
```

Present state map for confirmation — this is Gate A.

#### Step 2: Approval Gate A — State Map

```
Component: [COMPONENT NAME]
States: N

idle       →  (click)   →  loading
loading    →  (success) →  success
loading    →  (error)   →  error
success    →  (reset)   →  idle
error      →  (retry)   →  loading
```

Await approval.

#### Step 3: Component Generation

Generate one unified component with all states:

```tsx
// src/flows/<flow-slug>/components/Component.tsx

type ComponentState = "idle" | "loading" | "success" | "error";

interface ComponentProps {
  state?: ComponentState;       // for interactive use
  className?: string;
}

export const Component: React.FC<ComponentProps> = ({
  state = "idle",
  className,
}) => {
  // All states rendered via conditional Tailwind classes
  // No Remotion primitives
  // Transition CSS (transition-all duration-200) allowed — these are CSS, not JS animations
};
```

Also generate `ComponentDemo.tsx` — a standalone interactive wrapper with `useState` that lets the component be tested in isolation outside Remotion.

#### Step 4: Scene Generation

Generate one scene per state transition:

```
Scene_01: idle        (establish, 60 frames)
Scene_02: → loading   (transition, 45 frames)
Scene_03: loading     (sustain, 60 frames)
Scene_04: → success   (transition, 30 frames)
Scene_05: success     (sustain, 90 frames)
...
```

Each transition scene uses `spring()` to interpolate between state appearances.
A `StateLabel` overlay shows the current state name in the top-right corner of the video (useful for documentation).

---

### 🔌 LIVE COMPONENTS MODE

This mode generates **only Remotion scene wrappers**. No new base components are created. All imports point to the user's existing source files.

#### Step 1: Component Discovery

Run Step 0c (component discovery) now if not already done. Confirm the mapping with the user before proceeding.

#### Step 2: Step Breakdown

Decompose the task into discrete steps using the discovered components. For each step define:

```
Step N:
  label:        <short action label>
  caption:      <full sentence for the caption bar>
  component:    <ExistingComponentName from src/…/Component.tsx>
  import_path:  <relative path from the scene file to the component>
  props:        <prop snapshot — the exact prop values that represent this step's UI state>
  interaction:  <click | type | hover | scroll | none>
  cursor:       <{ x, y } in video pixels — only for click/hover/type>
  typing:       <{ prop: "fieldPropName", value: "full string", startFrame: N } — only for type>
```

**Props snapshot rules:**
- List every prop that differs from the component's default at this step
- For type interactions: `typing.prop` is a string prop on the component; the scene drives it character-by-character via `interpolate` on string length
- For click interactions: show the *before* state; the result appears in the next scene

#### Step 3: Approval Gate A — Step Plan

Present:
```
Flow: [FLOW-SLUG]  (live-components mode)
Task: [TASK]
Total scenes: N

Step 1: [label]
  Component:  ExistingComponentName  (src/…)
  Props:      { step: 1, isLoading: false }
  Interaction: none — caption: "[caption]"

Step 2: [label]
  Component:  ExistingComponentName  (src/…)
  Props:      { step: 1, isLoading: false }
  Interaction: click at (640, 380) — caption: "[caption]"

...
```

Await:
- ✅ **APPROVED** — Proceed to scene generation
- 🔄 **REVISE** — [specific changes]
- ❌ **RESTART** — [new direction]

#### Step 4: Scene Generation

Generate one `Scene_0N.tsx` per step. Each scene:

- Imports the existing component using the confirmed `import_path`
- Passes the step's prop snapshot directly
- Drives typing props via `interpolate` on string slice (never mutates app state)
- Composes overlays (cursor, ripple, caption) on top
- Applies entrance animation (fade + translateY, 12 frames)
- Wraps the component in the shell if one was designated

**Scene template — live-components mode:**

```tsx
// src/flows/<flow-slug>/remotion/scenes/Scene_02.tsx
import React from "react";
import { AbsoluteFill, useCurrentFrame, interpolate } from "remotion";
import { CheckoutForm } from "../../../../src/features/checkout/CheckoutForm";
import { AppLayout } from "../../../../src/components/AppLayout";
import { CursorOverlay } from "../overlays/CursorOverlay";
import { Caption } from "../overlays/Caption";

export const Scene_02: React.FC = () => {
  const frame = useCurrentFrame();
  const opacity = interpolate(frame, [0, 12], [0, 1], { extrapolateRight: "clamp" });
  const y = interpolate(frame, [0, 12], [16, 0], { extrapolateRight: "clamp" });

  // Drive a typing prop character-by-character
  const emailChars = Math.floor(
    interpolate(frame, [20, 55], [0, 17], { extrapolateRight: "clamp" })
  );
  const email = "user@example.com".slice(0, emailChars);

  return (
    <AbsoluteFill style={{ opacity }}>
      <div style={{ transform: `translateY(${y}px)`, height: "100%" }}>
        <AppLayout activePage="checkout">
          <CheckoutForm step={1} values={{ email }} isSubmitting={false} />
        </AppLayout>
      </div>
      <CursorOverlay x={640} y={380} frame={frame} clickAt={60} />
      <Caption text="Enter your email address to continue." frame={frame} />
    </AbsoluteFill>
  );
};
```

**Import path rule:** Always use a relative path from the scene file to the existing source file. Never use path aliases (`@/`) in scene files — Remotion's bundler may not resolve them unless the project's `tsconfig.paths` is explicitly configured.

If the project uses path aliases and they are confirmed working in Remotion, Claude may use them — but must note this in the Gate C summary.

#### Step 5: Props That Don't Exist

If a step requires a UI state that the existing component cannot express via props (e.g. the component has no `isHighlighted` prop), Claude must choose one option and note it clearly in Gate C:

| Situation | Resolution |
|---|---|
| State is visually important but no prop exists | Add a `__tutorialHighlight?: string` prop to the existing component — Claude proposes the minimal diff |
| State is minor or cosmetic | Overlay a `HighlightBox` or `Tooltip` on top in the scene — no component change needed |
| Component is too opaque (no useful props) | Report at Gate A: "Component X has no state-driving props — recommend switching to tutorial mode for this step" |

Claude never silently ignores a missing state. It always picks one of the above and explains why.

---

## Overlay Components

These are generated once per project and reused across all scenes.

### `CursorOverlay.tsx`
```
Props: x, y, frame, clickAt?
- Cursor SVG positioned absolutely at (x, y)
- If clickAt provided: scale pulse at that frame (spring-based)
- Cursor entrance: fade in over 8 frames
- Movement: if multiple positions needed, use interpolate between keyframes
```

### `ClickRipple.tsx`
```
Props: x, y, frame, triggerAt
- Expanding circle centered at (x, y)
- Triggered at triggerAt frame
- Scale: 0 → 2 over 20 frames, opacity: 0.4 → 0
```

### `Caption.tsx`
```
Props: text, frame
- Fixed bottom bar, 56px height
- Background: rgba(0,0,0,0.7), white text
- Entrance: slide up from bottom over 10 frames
- Text: appears character by character over 20 frames (typewriter)
```

### `Tooltip.tsx`
```
Props: text, targetX, targetY, frame, showAt
- Callout box with arrow pointing to target
- Entrance: fade + scale from 0.9 at showAt frame
- Used for annotating UI elements in mockup/tutorial mode
```

### `StateLabel.tsx`
```
Props: state, frame
- Top-right badge showing current state name
- Used in state-demo mode only
- Crossfade between state names on change
```

---

## `flowTimings.ts`

Generated after Gate A approval. Maps all scenes to frame ranges.

```ts
// src/flows/<flow-slug>/remotion/flowTimings.ts

export const FLOW_TIMINGS = {
  fps: 30,
  scenes: [
    { id: "step-01", label: "Initial state",    start: 0,   duration: 60  },
    { id: "step-02", label: "Click New Project", start: 60,  duration: 90  },
    { id: "step-03", label: "Name the project",  start: 150, duration: 120 },
    // ...
  ],
  totalFrames: <sum>,
} as const;

export type SceneId = typeof FLOW_TIMINGS.scenes[number]["id"];
```

**Default durations by interaction type:**

| Interaction | Duration | Reasoning |
|---|---|---|
| Establish / overview | 60f (2s) | Time to orient |
| Click | 75f (2.5s) | Cursor move + click + result |
| Type (short, < 20 chars) | 90f (3s) | Typing animation legible |
| Type (long, 20+ chars) | 120f (4s) | — |
| Hover | 60f (2s) | Show tooltip if present |
| Scroll | 90f (3s) | Smooth scroll animation |
| State transition | 45f (1.5s) | Transition only, no sustain |
| State sustain | 60f (2s) | Let state register visually |
| Success / completion | 90f (3s) | Let result land |

---

## `flow.ts` Data File

All step content as typed constants — no hardcoded strings in components.

```ts
// src/flows/<flow-slug>/data/flow.ts

export interface Step {
  id: string;
  label: string;
  caption: string;
  interaction: "click" | "type" | "hover" | "drag" | "scroll" | "none";
  target?: string;
  typedValue?: string;
  cursorPosition?: { x: number; y: number };
}

export const FLOW_STEPS: Step[] = [
  {
    id: "step-01",
    label: "Open the dashboard",
    caption: "Start from the main dashboard. The sidebar shows all your workspaces.",
    interaction: "none",
  },
  {
    id: "step-02",
    label: "Click New Project",
    caption: "Click '+ New Project' in the left sidebar to open the creation dialog.",
    interaction: "click",
    target: "sidebar-new-project-btn",
    cursorPosition: { x: 192, y: 340 },
  },
  // ...
];
```

---

## Approval Gate C — Component Review

Before rendering, present a plain-text review:

```
Flow: [FLOW-SLUG]
Mode: [MODE]
Scenes: N  |  Total duration: Xs  |  Output: [FILENAME]

Components generated:
  ✅ AppShell.tsx
  ✅ Step_01.tsx  — [brief description]
  ✅ Step_02.tsx  — [brief description]
  ...

Overlays: CursorOverlay, ClickRipple, Caption
Placeholder assets: [list any — e.g. "Step 03 uses placeholder screenshot"]

These components can be used independently outside Remotion:
  import { Step_02 } from "./src/flows/<flow-slug>/components/Step_02"
```

Await GO / ADJUST.

---

## Render

### Test Render (first 2 scenes)

```bash
npx remotion render FlowComposition \
  --frames=0-$(node -e "const t=require('./src/flows/<flow-slug>/remotion/flowTimings'); console.log(t.FLOW_TIMINGS.scenes[1].start + t.FLOW_TIMINGS.scenes[1].duration - 1)") \
  --output=test-<flow-slug>.mp4
```

Validate:
- [ ] No TypeScript errors
- [ ] UI style tokens render correctly (not fallback grays)
- [ ] Cursor appears at correct position
- [ ] Caption readable against content
- [ ] Animations are smooth — no pop-in on frame 0

Fix all issues before full render.

### Full Render

```bash
npx remotion render FlowComposition \
  --output=output/<flow-slug>-<YYYYMMDD>.mp4 \
  --codec=h264 \
  --crf=18
```

---

## Using Components Outside Remotion

After render, `src/flows/<flow-slug>/components/` is a self-contained, deployable
component set. To use in a real project:

1. Copy `components/` into the target project's component directory
2. Copy the flow's CSS block from `src/index.css` — the section labelled
   `/* ── UI Flow Studio: <flow-slug> ── */` under `@layer components`
3. Ensure the target project's CSS file imports Tailwind v4 (`@import "tailwindcss"`)
   so the `@apply` directives resolve correctly
4. For **interactive use**, pass `activeState` props and wire to your own state management
5. For **onboarding overlays**, wrap any step component in a modal or spotlight overlay

For **state-demo components**, use `ComponentDemo.tsx` directly — it includes
its own `useState` wiring and renders all transitions interactively.

---

## Token Reference

All flow components use semantic class names defined in **`src/index.css`** under `@layer components`.

**When generating a new flow, Claude MUST:**
1. Check `src/index.css` for existing classes that cover the need before creating any new ones
2. If new classes are needed, write them directly into `src/index.css` as a new labelled block (e.g. `/* ── UI Flow Studio: notion-create-project ── */`)
3. Reference those class names in components — never define CSS anywhere else

The token sets below are **templates to be written into `src/index.css`**, not inline CSS.
Each block is added once per flow-slug and reused by all components in that flow.

### Minimal Style Tokens — write into `src/index.css`
```css
  /* ── UI Flow Studio: <flow-slug> ─────────────────────────────── */
  .flow-panel          { @apply bg-white border border-gray-200 rounded p-6; }
  .flow-btn-primary    { @apply bg-blue-600 text-white px-4 py-2 rounded text-sm font-medium; }
  .flow-btn-secondary  { @apply bg-white border border-gray-300 text-gray-700 px-4 py-2 rounded text-sm; }
  .flow-input          { @apply border border-gray-300 rounded px-3 py-2 text-sm w-full; }
  .flow-input--focused { @apply border-blue-500 ring-2 ring-blue-100; }
  .flow-sidebar        { @apply bg-gray-50 border-r border-gray-200 w-56 flex-shrink-0; }
  .flow-topbar         { @apply bg-white border-b border-gray-200 h-14 px-6 flex items-center; }
  .flow-label          { @apply text-xs font-medium text-gray-500 uppercase tracking-wide; }
  .flow-badge          { @apply inline-flex items-center px-2 py-0.5 rounded text-xs font-medium; }
  .flow-card           { @apply bg-white border border-gray-200 rounded-lg p-4 shadow-sm; }
```

### shadcn Style — use `src/components/ui/` components directly

For `shadcn` style, Claude uses installed shadcn/ui components instead of writing custom CSS classes.
Run `npx shadcn@latest add <component>` for any component not yet in `src/components/ui/`.

```tsx
import { Button } from "@/components/ui/button";
import { Card, CardContent, CardHeader, CardTitle } from "@/components/ui/card";
import { Badge } from "@/components/ui/badge";
import { Input } from "@/components/ui/input";
import { cn } from "@/lib/utils";

// Wrapper classes for layout (still go in src/index.css):
// .flow-sidebar  { @apply bg-zinc-50 border-r border-zinc-200 w-56 flex-shrink-0; }
// .flow-topbar   { @apply bg-white border-b border-zinc-200 h-14 px-6 flex items-center; }
```

Common shadcn components for flows: `button`, `card`, `badge`, `input`, `avatar`, `separator`, `skeleton`, `tabs`, `progress`

### DaisyUI Style Tokens — write into `src/index.css`

For `daisy` style, use DaisyUI class names directly in JSX. Only write CSS classes for layout scaffolding that DaisyUI doesn't cover.

```tsx
// DaisyUI classes used directly in JSX — no custom CSS needed:
<button className="btn btn-primary">Create</button>
<div className="badge badge-success gap-1">Active</div>
<div className="card bg-base-100 shadow-md"><div className="card-body">...</div></div>
<progress className="progress progress-primary w-56" value={70} max={100} />
<div className="stat"><div className="stat-title">Revenue</div><div className="stat-value">$4,200</div></div>
<span className="loading loading-spinner loading-sm" />

// Layout scaffolding (add to src/index.css under flow-slug label):
// .flow-sidebar  { @apply bg-base-200 border-r border-base-300 w-56 flex-shrink-0; }
// .flow-topbar   { @apply bg-base-100 border-b border-base-300 h-14 px-6 flex items-center; }
```

### Material Style Tokens — write into `src/index.css`
```css
  /* ── UI Flow Studio: <flow-slug> ─────────────────────────────── */
  .flow-panel          { @apply bg-white rounded-lg p-6 shadow-md; }
  .flow-btn-primary    { @apply bg-indigo-500 text-white px-6 py-2 rounded-full text-sm font-medium shadow; }
  .flow-btn-secondary  { @apply bg-white border border-indigo-300 text-indigo-700 px-6 py-2 rounded-full text-sm; }
  .flow-input          { @apply border-b-2 border-gray-300 px-2 py-2 text-sm w-full bg-transparent; }
  .flow-input--focused { @apply border-b-indigo-500; }
  .flow-sidebar        { @apply bg-white border-r border-gray-100 w-60 flex-shrink-0 shadow-sm; }
  .flow-topbar         { @apply bg-white h-16 px-6 flex items-center shadow-sm; }
  .flow-label          { @apply text-xs font-medium text-gray-500 uppercase tracking-widest; }
  .flow-badge          { @apply inline-flex items-center px-3 py-1 rounded-full text-xs font-medium; }
  .flow-card           { @apply bg-white rounded-xl p-5 shadow-md; }
```

### Custom Style — write into `src/index.css`

When `ui_style = custom`, Claude asks for bg / text / accent colors, then writes a new
named block into `src/index.css`. All class names use the flow-slug as a prefix to avoid
collisions (e.g. `.myflow-btn-primary`).

---

## Final Checklist

### Setup
- [ ] Mode and subject confirmed at activation
- [ ] UI style confirmed (Step 0) — *skip for live-components mode*
- [ ] Session context initialized
- [ ] Preflight passed
- [ ] *(live-components)* Component discovery complete (Step 0c) — component-to-step mapping confirmed by user

### Planning
- [ ] Step/scene/state plan generated
- [ ] Plan approved (Gate A)
- [ ] *(live-components)* Each step lists: component name, import path, prop snapshot, interaction type

### CSS
- [ ] `src/index.css` checked for existing classes before creating any new ones
- [ ] Flow token block written to `src/index.css` under `@layer components` with flow-slug label — *skip for live-components if no new overlay classes are needed*
- [ ] No CSS defined inside any `.tsx` file, `<style>` tag, or separate `.css` file
- [ ] `style={{}}` used only for values driven by `useCurrentFrame()` / `interpolate()` / `spring()`

### Generation
- [ ] `data/flow.ts` generated — all step data typed
- [ ] `style.ts` generated — token references for this flow's style — *skip for live-components*
- [ ] `flowTimings.ts` generated — complete frame map
- [ ] All base components generated (`components/`) — zero Remotion primitives — *skip for live-components*
- [ ] `AppShell.tsx` generated (tutorial/mockup modes) — *skip for live-components (use existing shell)*
- [ ] All Remotion scenes generated (`remotion/scenes/`)
- [ ] All overlays generated (`remotion/overlays/`)
- [ ] `FlowComposition.tsx` assembled — all scenes sequenced
- [ ] Composition registered in `src/Root.tsx`
- [ ] *(mockup mode)* `<FlowSlug>App.tsx` generated — interactive app with useState routing
- [ ] *(mockup mode)* `site.tsx` generated — Vite entry importing the app
- [ ] *(mockup mode)* `site.html` + `vite.config.ts` present at project root
- [ ] *(mockup mode)* `dev:site` + `build:site` scripts in `package.json`
- [ ] *(live-components)* Every scene `import` path verified to resolve from the scene file's location
- [ ] *(live-components)* Any missing-prop situations documented in Gate C with chosen resolution
- [ ] Component review approved (Gate C)

### Render
- [ ] Test render (first 2 scenes) passes validation
- [ ] Full render completed
- [ ] Output: `output/<flow-slug>-<YYYYMMDD>.mp4`
- [ ] *(mockup mode)* `npm run dev:site` verified — page loads at `http://localhost:5174/site.html`
