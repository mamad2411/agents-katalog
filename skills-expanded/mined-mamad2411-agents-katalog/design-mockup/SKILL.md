---
name: design-mockup
description: >-
  Produce on-brand UI mockups with the Stitch design-to-code tool BEFORE writing any
  implementation code, so design decisions get made and approved visually first. Auto-detects
  THIS project's design source of truth (a design.md / design spec, design tokens, Tailwind/theme
  config, or a live design-system page), seeds a Stitch design system from it, generates the
  requested screens, downloads and actually LOOKS AT each screenshot to verify brand fidelity,
  and presents a review gallery + the Stitch storyboard link. Use when the user says "mock this
  up", "design mockups", "stitch mockups", "let's design the screens", or wants to see a
  feature's UI before it's built. NOT for tiny visual tweaks to existing shipped UI. Portable:
  it reads whatever project you're in and never hardcodes one project's brand.
---

# Design-mockup — Stitch mockups, on this project's brand

Mockup-first: for any new UI or feature, produce and get approval on **visual mockups** before
implementation. This skill is **project-agnostic** — it adapts to the repo you're in.

Requires the Stitch MCP tools (`mcp__stitch__*`). Load them first with ToolSearch if deferred.

## STEP 0 — Find THIS project's design source of truth (always first)

Never invent a brand. Look, in priority order, for what the project already defines:
- A written design spec — `docs/design.md`, `DESIGN.md`, a style guide, or brand guidelines.
- **Design tokens** — a tokens file (`tokens.css`/`tokens.ts`), CSS `:root` custom properties,
  a Tailwind/theme config, `components.json` (shadcn), `globals.css`. Extract the real hex values.
- A **live design-system / storybook page** — often the truest "how to compose screens" reference.
- `CLAUDE.md` for any stated brand/UX rules.

Capture: primary/secondary/accent brand colors (real hexes), neutrals, typeface(s), corner radius
scale, light/dark support, and the reusable component vocabulary.

**If NO design source exists:** offer to author a `design.md` from whatever tokens/assets do exist
(sample brand colors straight from the logo asset if needed — don't eyeball). Get the user to
confirm the palette before generating. A wrong brand wastes every screen.

## STEP 1 — Stitch design system (once per brand)

- Reuse an existing project if appropriate, else `create_project`.
- `create_design_system` with the project's real tokens mapped to Stitch params:
  - `colorMode` LIGHT/DARK to match the project (many are light-only).
  - `headlineFont`/`bodyFont`/`labelFont` → the project's typeface (enum, e.g. `INTER`).
  - `roundness` → closest to the project's radii (`ROUND_FOUR` for ~4–6px, `ROUND_EIGHT` for ~8px).
  - `customColor` + `overridePrimaryColor` = brand primary; `overrideSecondaryColor` = secondary/ink;
    `overrideTertiaryColor` = accent; `overrideNeutralColor` = a representative neutral.
  - `colorVariant: FIDELITY` to hold close to the seed colors.
  - `designMd`: a COMPACT brand spec (palette + type + shape + a few usage rules + product tone).
- Keep the returned `assets/<id>` — pass it as `designSystem` to every generation for consistency.

## STEP 2 — Generate screens

- For each screen: `generate_screen_from_text` with `projectId`, the `designSystem` id, `deviceType`
  (DESKTOP/MOBILE/TABLET), and a detailed prompt.
- **Prompt recipe:** name the screen's job; specify layout top-to-bottom; give REAL copy (plain-English,
  outcome-focused, never system jargon); call out brand usage explicitly (one primary action in the
  primary color per screen, accent used sparingly, ink for headings); for in-context screens, describe
  the app chrome (sidebar/top bar) so it reads grounded; restate shape (small radii, no pills) and tone.
- **Generate ONE screen first, verify the brand, THEN batch the rest** — cheaper to fix the design
  system once than N times.

## STEP 3 — Verify by LOOKING (non-negotiable)

For every generated screen, download the `screenshot.downloadUrl` and **Read the PNG to actually view
it.** Confirm the brand colors, type, radii, and copy are right. TypeScript/tests can't catch a
wrong-looking screen — your eyes are the gate. If a screen is off, fix via `edit_screens` (targeted
change) or `generate_variants` (explore alternatives), not a blind re-generate.

## STEP 4 — Present for review

- Build a single **review gallery** (a self-contained HTML Artifact with the screenshots embedded as
  data URIs, annotated with each screen's role in the flow) so the user reviews everything in one place.
- Also give the **Stitch project link** (`https://stitch.withgoogle.com/projects/<projectId>`) as the
  editable storyboard.
- These are **mockups, not implementation.** Get the user's approval / edits before any code is written.
  On approval, hand off to implementation (or the project's ship/build flow). Never present a mockup as
  a shipped feature.

## Gotchas (learned in practice)

- Call Stitch tools with **structured params**, never a raw-JSON string wrapper — it fails to parse.
- A one-off **"Request contains an invalid argument"** is usually transient — **retry once** before
  diagnosing; the second identical call typically succeeds.
- `list_screens` can return empty even when screens exist — rely on each generation's returned screen
  id/name, not on list_screens.
- Each generation **echoes the full `designMd`** back in the response — keep that markdown tight to
  avoid bloating context across many screens.
- Screenshot URLs are large signed Google URLs — `curl -L` them; they may expire, so download promptly.
- **`edit_screens` on text-only changes patches the live DOM but does NOT refresh the exported
  screenshot/htmlCode** — the API keeps serving the pre-edit snapshot (same file id), so a downloaded
  thumbnail lags even though the Stitch web app shows the change. Layout-level edits (e.g. removing a
  sidebar) DO trigger a full re-render with a NEW screen id + fresh screenshot. So: verify text edits in
  the Stitch UI, and if you need an accurate exported thumbnail of a text-only change, re-generate the
  screen rather than trusting the screenshot URL.
- Don't over-generate: cover the distinct screens + one representative "template" screen for repeated
  patterns (e.g. one feature-guide covers the rest); note the repeats rather than rendering all.
