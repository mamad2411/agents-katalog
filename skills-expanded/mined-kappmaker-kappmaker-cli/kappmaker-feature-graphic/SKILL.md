---
name: kappmaker-feature-graphic
description: Generate the Google Play feature graphic with AI — the 1024x500 banner at the top of a Play listing, built from the app name, brand color, logo and screenshots. Use when the user asks for a feature graphic, Play banner, store header image, or the wide image Google Play requires before publishing.
---

# KAppMaker — Feature Graphic

## Before running any command

1. **Prerequisites** — `kappmaker --version` (install: `npm i -g kappmaker`). If a credential is
   missing the CLI says so; re-run `kappmaker config init`.
2. **Read `AiGuidelines/` first** — the PRD, positioning and UI spec already answer most questions.


### generate-feature-image — AI Feature Graphic Generation

**Syntax**: `kappmaker generate-feature-image --spec <spec.json> [options]` (agent flow) or
`kappmaker generate-feature-image --prompt "<concept>" --app-name "<Name>" --primary-color "#RRGGBB" [options]` (OpenAI fallback)

**You are the AI — author the banner spec yourself. NEVER use the OpenAI path from this skill.**
Without `--spec`, the CLI calls OpenAI (GPT-4.1) to turn the inputs into a JSON banner spec — that
path exists solely for raw-CLI users without an agent. The flow:

1. Run `kappmaker spec-template feature-graphic --output Assets/playstore/feature-graphic-spec.json`
   — writes the canonical banner spec skeleton (the exact JSON shape the OpenAI path used; its
   `_instructions` key explains the rules and is auto-stripped before generation).
2. Optionally run `kappmaker generate-feature-image --print-prompt --prompt "<concept>" --app-name "<Name>" --primary-color "#RRGGBB" [--logo ...] [--reference ...]`
   for the full authoring guidance with your reference-image setup baked in.
3. Fill the skeleton yourself: app name, brand color and value props from `AiGuidelines/`. Banner
   text must be ONLY the real app name/subtitle. The skeleton is a proven baseline, not a
   straitjacket — add fields or write a richer spec when you can do better; only the wide-banner
   composition and real-text-only rules are fixed. If the user supplied their own spec JSON, use it as-is.
4. Run with `--spec` **plus the same `--logo`/`--reference` flags** (those control the uploaded
   images, independent of the spec).

**Options**:
- `--spec <path>` — Pre-authored banner spec JSON; skips OpenAI entirely (preferred from this skill)
- `--print-prompt` — Print the spec-authoring instructions and exit (no API calls)
- `--prompt <text>` — App concept / description (required unless `--spec` is given)
- `--app-name <name>` — App name rendered on the banner (required unless `--spec` is given)
- `--primary-color <hex>` — Brand color in hex (required unless `--spec` is given)
- `--subtitle <text>` — Tagline shown under the app name
- `--logo <path>` — App logo PNG to render on the brand panel (rendered pixel-faithfully)
- `--reference <paths...>` — App screenshot paths to place inside device frames (max 10)
- `--output <path>` — Custom output file path
- `--resolution <res>` — AI resolution: 1K, 2K, 4K (default: 2K)
- `--locale <code>` — Play Store locale for the default output path (default: en-US)
- `--poll-interval <seconds>` — fal.ai polling interval (default: 10)

**Prerequisites**: `falApiKey` (prompted on first use). `openaiApiKey` only for the legacy
non-`--spec` path — never from this skill. `imgbbApiKey` recommended when passing `--logo` or
`--reference` (falls back to inline data URIs otherwise).

**What it does**:
1. Takes the banner spec (yours via `--spec`, or OpenAI-generated otherwise).
2. fal.ai (`nano-banana-2`, or `/edit` when references are provided) generates one wide image.
3. `sharp` resizes/crops the result to EXACTLY 1024×500 px (Google Play feature graphic spec) via center cover.
4. Saves to `MobileApp/distribution/android/playstore_metadata/<locale>/images/featureGraphic.png` so the existing Fastlane publish flow picks it up automatically — falls back to `Assets/playstore/featureGraphic.png` outside a KAppMaker project.

**Tips**: Pass `--logo` to keep the exact app icon (the model will reproduce, not redraw, image #1). Pass `--reference` screenshots in the order they should appear inside the device mockups.

---

## Where this sits in the flow

- **Before this:** **kappmaker-logo** for brand consistency.
- **After this:** **kappmaker-gpc** — the feature graphic is a Play Store asset.
