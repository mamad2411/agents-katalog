---
name: kappmaker-logo
description: Generate the app's logo with AI — the brand mark used for icons, splash and store art. Use when the user asks for a logo or brand mark. For any other picture use kappmaker-image; for platform icon sets use kappmaker-app-icons.
---

# KAppMaker — Logo

## Before running any command

1. **Prerequisites** — `kappmaker --version` (install: `npm i -g kappmaker`). If a credential is
   missing the CLI says so; re-run `kappmaker config init`.
2. **Read `AiGuidelines/` first** — the PRD, positioning and UI spec already answer most questions.


### create-logo — AI Logo Generation

**Syntax**: `kappmaker create-logo [--prompt <text>] [--spec <spec.json>] [--output <path>]`

**Prerequisites**: `falApiKey` (prompted on first use if not set).

**Prefer authoring the spec yourself** when you want brand-tailored variations: run
`kappmaker spec-template logo --output Assets/logo-spec.json` to get the canonical logo-grid spec
JSON (the proven prompt structure — grid rules, visual language, 16 style-theme slots), fill it from
`AiGuidelines/` (brand color, mood, audience; customize the 16 `style_themes`), then run
`kappmaker create-logo --spec Assets/logo-spec.json`. The skeleton is a proven baseline, not a
straitjacket — restructure or enrich it when you can do better, and use a user-supplied spec as-is.
ONE fixed rule: the spec MUST keep the 4×4 grid — the CLI slices the result into 16 cells. Plain
`--prompt` uses the built-in generic template instead.

**What it does**:
1. Builds the prompt from `--spec` (pre-authored JSON), or from `--prompt` / interactive app idea
2. Generates a 4x4 grid of 16 logo variations via fal.ai
3. Opens preview image
4. User selects a logo (1-16) with optional zoom/gap adjustments
5. Extracts selected logo to 512x512 PNG
6. Saves to `Assets/app_logo.png` (or custom `--output` path)

**Interactive**: Always interactive for the grid selection (number prompt). The initial app-idea prompt can be skipped by passing `--prompt "..."` up front.

---

## Where this sits in the flow

- **Before this:** **kappmaker-new-app**.
- **After this:** **kappmaker-app-icons** — turn the finished logo into iOS and Android icon sets.
