---
name: ui-journey
description: Use when a web project (game, site, browser app) should accumulate progressive screenshots at development milestones, when you want a visual changelog or replayable history of how a UI evolved, or when Playwright runs should produce a step-through record of key implementations.
---

# UI Journey

## Overview

Capture progressive screenshots of a web project as it hits development
milestones, recorded in an append-only manifest, then generate a playback
viewer that lets anyone step through the development journey.

**Core principle:** loose PNG files are just pixels. The *manifest* — label,
caption, git SHA, ordering — is what makes a journey replayable. Never capture
a screenshot without recording it in the manifest. The manifest *records* a git
SHA, but the manifest file itself need not live in the code repo — it can live
in an external docs vault (see "Output location" below).

## When to Use

- A milestone or feature has landed and its visual state is worth recording.
- You want a "this is how the UI evolved" history for a README, wiki, or demo.
- Existing Playwright tests should leave behind a visual record, not just pass/fail.

Not for: pixel-diff visual-regression gating (that is a test assertion, not a
journey). Not for one-off debug screenshots.

## How It Works

Three bundled pieces, all zero-dependency (only `@playwright/test`, already
present, plus Node built-ins):

| File | Role |
|---|---|
| `lib/capture.ts` | `captureMilestone(page, label, opts)` + `waitForStableFrame` |
| `lib/manifest.ts` | manifest schema, read/write |
| `scripts/build-viewer.mjs` | manifest -> HTML viewer + markdown gallery |
| `assets/viewer.html` | the step-through UI template |

To install into a project, see `references/wiring.md`.

**Output location.** The *tooling* above always lives in the repo. The
*output* — manifest, `shots/`, generated viewer — has a configurable location
via the `JOURNEY_DIR` env var or the `journeyDir` capture option (default
`journey/` in the repo). If the project keeps curated artifacts in an external
docs vault, point `JOURNEY_DIR` there. See `references/wiring.md`.

## Capturing

Call `captureMilestone` from inside an existing Playwright test, or from a
standalone capture script:

```ts
import { captureMilestone } from "../journey/capture";

await captureMilestone(page, "lobby-prematch", {
  caption: "Pre-match lobby, both players connected",
  clip: page.locator("#game"),                      // optional element scope
  waitFor: () => window.__render?.ready === true,   // optional readiness gate
});
```

Each call waits for a stable frame, screenshots into the journey directory's
`shots/`, collects git metadata, and appends one manifest entry. Multiple captures may share a
`label` — they are kept and ordered by capture time, which is how a single
screen's evolution becomes replayable.

**Conventions:**

- **Labels** are stable kebab-case, one per logical screen/state.
- **Captions** state what the milestone *demonstrates*, not just what is shown.
- A caption is required — the API will not let you capture without one.

## Stable Frames (the most common failure)

A screenshot taken mid-animation or before assets load is noise. `waitForStableFrame`
(run automatically by `captureMilestone`) handles it:

- Disables CSS animations/transitions and awaits `document.fonts.ready`.
- Applies a short settle delay.

**Canvas / WebGL apps and games:** CSS disabling does nothing for a `<canvas>`.
You MUST pass an explicit `waitFor` predicate that reports real readiness
(`() => window.__game?.ready`). Without it you will capture half-rendered
frames. Also avoid live clocks/timestamps in-frame — they make every capture
look "changed."

## Playback

Generate the viewer after capturing:

```bash
node journey/build-viewer.mjs
```

Environment variables control output:

- `JOURNEY_OUTPUT` — `html` | `md` | `both` (default `both`)
- `JOURNEY_DIR` — journey directory (default `journey`)

`index.html` is a self-contained step-through viewer: prev/next, arrow keys,
timeline scrubber, caption + commit-SHA badge, and an auto-play button with
adjustable speed. `index.md` is a static gallery for wikis and READMEs.

## Common Mistakes

- **Capturing without a manifest entry** — defeats the entire skill. Always go
  through `captureMilestone`, never a raw `page.screenshot`.
- **No `waitFor` on a canvas/game** — produces half-rendered captures.
- **Vague captions** ("the screen") — the journey is only as useful as its captions.
- **Committing the shots but not `manifest.json`** — the viewer needs both.
- **Forgetting the manifest is append-only** — re-running a capture spec adds
  more entries. To start over, delete `manifest.json` and `shots/` from the
  journey directory (`JOURNEY_DIR`, default `journey/`).
