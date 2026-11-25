---
name: product-launch-video
description: Turn a product URL, launch brief, or approved script into a production-ready launch video. Use for product reveals, feature announcements, SaaS launches, and narrated product films; not for generic explainers or editing existing footage.
---

# Product Launch Video

Create a launch film whose story, visual system, motion, and evidence all come
from the product being launched. The deliverable is a rendered video plus the
editable project that produced it.

Use HyperFrames when it is installed. A Remotion project is also supported;
prefer maintained remocn components over recreating common animation
primitives. Do not switch stacks after the storyboard is approved.

## Inputs to lock

Before building, establish:

- product URL or source brief;
- audience and the one change in belief the film should create;
- aspect ratio, target duration, language, and narration choice;
- claims that may appear and the evidence behind each;
- whether an existing script must remain verbatim or may be restructured.

If any of these would materially change the film, ask once before starting.

## Required output

Keep the project editable. At minimum, produce:

```text
capture/                 product copy, screenshots, logos, and design tokens
STORYBOARD.md            approved shot-by-shot plan
SCRIPT.md                narration, when the film is narrated
design.md                type, color, spacing, motion, and framing rules
compositions/            source for every shot
renders/launch.mp4       final delivery
```

Do not treat a preview, storyboard, contact sheet, or silent draft as the final
video.

## Workflow

### 1. Capture the product

Inspect the supplied URL or assets. Preserve exact product copy, real UI,
logos, typography, colors, and interface states. Record every usable asset and
its source. Do not invent features, customers, metrics, or integrations.

If no website exists, create a small source record from the brief and supplied
assets so later shots still have a traceable basis.

### 2. Choose the story

Write one sentence for each of these before storyboarding:

- the audience's present frustration;
- the product's distinctive mechanism;
- the proof the viewer should believe;
- the action the viewer should take.

Select only the beats the source material supports. A short film usually needs
a hook, mechanism, proof, and close; it does not need a feature inventory.

Read [references/story-and-shot-system.md](references/story-and-shot-system.md)
when planning the sequence.

### 3. Establish the visual system

Derive `design.md` from the captured product rather than from a generic video
template. Define the canvas, typography, color roles, grid, safe areas, visual
density, motion character, caption treatment, and transition family.

Limit the film to one visual grammar. Repetition creates identity; a new style
for every shot makes the film feel assembled from templates.

### 4. Storyboard before animation

For every shot, record:

- start and end time;
- narrative job;
- exact on-screen copy;
- source asset or UI state;
- composition and camera intent;
- entrance, development, and exit;
- transition to the next shot;
- any claim and its evidence source.

The frame must continue developing for its useful duration. Avoid an entrance
animation followed by several seconds of static content.

Show the storyboard for approval before building the full film.

### 5. Build with maintained primitives

HyperFrames is preferred for HTML shot sequences. For Remotion, read
[references/remotion-and-remocn.md](references/remotion-and-remocn.md) and use
remocn for common typography, terminal, chart, background, and transition
behaviors. Custom animation is appropriate only when the product requires a
motion idea that the library cannot express.

Every shot must be deterministic at an arbitrary frame. Do not rely on runtime
timers, non-seeded randomness, or interaction state that a renderer cannot
reproduce.

### 6. Review the assembled film

Before rendering, inspect:

- first, middle, and final frames of every shot;
- every transition seam;
- text wrapping, clipping, contrast, and safe areas;
- timing against narration and music;
- product fidelity and claim accuracy;
- the full film at normal speed with audio;
- a silent pass, so the visual story still makes sense.

Run `node scripts/check-project.mjs <project-dir>` for the package-level project
gate. Also run the native lint, validation, and render checks of the selected
video stack.

Pause for approval on the assembled preview. Render the final MP4 only after
approval.

## Evidence boundary

A polished example demonstrates intended craft; it does not prove the skill
improves model performance. Report separately:

- package and project checks;
- successful final render;
- human visual review;
- any comparative evaluation, only when recorded runs and scoring exist.

Never call the skill evaluated because one attractive video was produced.

## Failure conditions

Stop rather than ship when:

- the primary product claim cannot be sourced;
- captured UI is replaced by invented interface chrome;
- a shot is illegible at delivery resolution;
- narration and picture disagree;
- the project cannot render deterministically;
- the editable source or final MP4 is missing.

