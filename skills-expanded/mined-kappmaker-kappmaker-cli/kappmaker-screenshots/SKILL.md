---
name: kappmaker-screenshots
description: Design and translate App Store and Play Store MARKETING screenshots with AI — headlines, brand panels, device frames. Use when the user asks for store screenshots, marketing screenshots, or screenshots in other languages. Capturing the app's real screens is different — that is the project-bundled capture-app-screens skill, whose output feeds this one as references.
---

# KAppMaker — Screenshots

## Before running any command

1. **Prerequisites** — `kappmaker --version` (install: `npm i -g kappmaker`). If a credential is
   missing the CLI says so; re-run `kappmaker config init`.
2. **Read `AiGuidelines/` first** — the PRD, positioning and UI spec already answer most questions.


### generate-screenshots — AI Screenshot Generation

**Syntax**: `kappmaker generate-screenshots --spec <spec.json> [options]` (agent flow) or
`kappmaker generate-screenshots --prompt "<app description>" [options]` (OpenAI fallback)

**You are the AI — author the spec yourself. NEVER use the bare `--prompt` path from this skill.**
The `--prompt`-only path calls OpenAI (GPT-4.1) to write a JSON screenshot spec, which exists solely
for users running the raw CLI without an agent. You can write that JSON better yourself, with full
project context, and no `openaiApiKey` is needed. The flow:

1. Ask the user which style preset (1–8) they want if not specified.
2. Run `kappmaker spec-template screenshots --output Assets/screenshots/spec.json` — writes the
   canonical spec skeleton (the exact JSON shape the OpenAI path used; its `_instructions` key
   explains the rules and is auto-stripped before generation).
3. Run `kappmaker generate-screenshots --print-prompt --prompt "<one-line app description>" --style <id>`
   — it prints the style-specific visual direction (device framing, layout zones, typography rules)
   and exits without calling any API. It also reports whether reference screenshots were detected.
4. Fill the skeleton yourself: exactly 8 `screenshots` entries, marketing copy drawn from
   `AiGuidelines/` (value props, brand color, tone), style direction baked into the style/lighting
   fields. The skeleton is a proven baseline, not a straitjacket — add fields or write a richer spec
   when you can do better; only the 2×4 grid + 8 entries are mechanically fixed (the CLI slices the
   output on that assumption). If the user supplied their own spec JSON, use it as-is.
5. Run `kappmaker generate-screenshots --spec Assets/screenshots/spec.json [--input <dir>] [--style <id>]`.

**Options**:
- `--spec <path>` — Pre-authored spec JSON; skips OpenAI entirely (preferred from this skill)
- `--print-prompt` — Print the spec-authoring instructions for `--style` and exit (no API calls)
- `--prompt <text>` — App description or PRD (required unless `--spec`; with `--spec` only needed for `--print-prompt`)
- `--input <dir>` — Reference screenshots directory (default: auto-detect `Assets/screenshots`)
- `--style <id>` — Style preset 1-8 (default: 1)
- `--output <dir>` — Output directory (default: `Assets/screenshots`)
- `--resolution <res>` — AI resolution: 1K, 2K, 4K (default: 2K)
- `--poll-interval <seconds>` — fal.ai polling interval (default: 10)

**Prerequisites**: `falApiKey`, `imgbbApiKey` (prompted on first use). `openaiApiKey` is only needed
for the legacy `--prompt`-without-`--spec` path — never from this skill.

**What it does**: Takes the screenshot spec (yours via `--spec`, or OpenAI-generated from `--prompt`),
sends it to fal.ai to generate 8 marketing screenshots in a fixed 2×4 grid, splits them into 8
individual 1284×2778 images, saves to appstore/playstore directories. Grid shape is fixed by design —
number of reference images does not change the output count.

**Style presets** (1-8): Different visual styles for the screenshots. Ask the user what style they prefer if not specified.

**Where the reference screenshots come from**: `--input` wants plain captures of the app's real
screens — no headlines, no device frames (`--reference` is a different command's flag —
`generate-image` / `generate-feature-image` — this one only takes `--input <dir>`). In a
KAppMaker-boilerplate project those are produced by the `capture-app-screens` skill (`MobileApp/./scripts/generate_store_screenshots.sh`), which renders `@Preview @StoreScreenshot` composables at storefront pixel sizes into `distribution/store_screenshots/<locale>/<device>/`. Point `--input` there rather than asking the user to screenshot a simulator by hand. That skill only produces the bare screen art; the design pass — marketing copy, brand panel, device frames — is this command's job, so the two are complementary, not alternatives.

---

### translate-screenshots — Locale Translation

**Syntax**: `kappmaker translate-screenshots [source-dir] [options]`

**Options**:
- `[source-dir]` — Source screenshots directory (default: `MobileApp/distribution/ios/appstore_metadata/screenshots/en-US`)
- `--output <path>` — Distribution directory root
- `--locales <codes...>` — Target Play Store locale codes, space-separated (default: all 48+)
- `--rows <n>` — Grid rows (default: 2)
- `--cols <n>` — Grid columns (default: 4)
- `--resolution <res>` — 1K, 2K, 4K (default: 2K)
- `--poll-interval <seconds>` — fal.ai polling interval (default: 10)

**Prerequisites**: `falApiKey`, `imgbbApiKey` (prompted on first use if not set).

**What it does**: Combines source screenshots into a grid, translates to all target locales in parallel via fal.ai, splits translated grids back into individual images, saves to Fastlane distribution structure for both iOS and Android.

---

## Where this sits in the flow

- **Before this:** A running app to capture, and **kappmaker-app-icons** for a finished look.
- **After this:** **kappmaker-asc** / **kappmaker-gpc** to attach them to the listing.
