---
name: kappmaker-mascot
description: Generate an AI mascot for a KAppMaker app and its emotional states — a character that boosts engagement, virality and growth. Pick from 16 concepts, then render the chosen mascot in 16 app-UI states (happy, loading, error, celebrating...), backgrounds auto-removed; selected states can be animated into short looping clips. Use when the user asks for a mascot, app character, mascot emotions/states, or animating the mascot. For the brand logo use kappmaker-logo.
---

# KAppMaker — Mascot

## Before running any command

1. **Prerequisites** — `kappmaker --version` (install: `npm i -g kappmaker`). If a credential is
   missing the CLI says so; re-run `kappmaker config init`.
2. **Read `AiGuidelines/` first** — the PRD, positioning and UI spec already answer most questions
   (app idea, tone, brand colors).

## Why a mascot

A mascot personifies the app: it reacts on loading/empty/success/error screens, carries onboarding
and streaks, and makes the app feel alive — measurably better engagement and shareability. The flow
mirrors logo generation: a 4×4 grid of 16 concepts → the user picks one → that exact character is
rendered in 16 emotional states, sliced into individual files, backgrounds removed.

### create-mascot — Concept grid + 16 emotional states

**Syntax**: `kappmaker create-mascot [--prompt <text>] [--tone <text>] [--spec <file>] [--states-spec <file>] [options]`

**Prefer authoring the specs yourself** (same principle as the other image skills — structured JSON
beats prose, and templates preserve the proven prompt shape):

1. `kappmaker spec-template mascot --output Assets/mascot/mascot-spec.json` — stage-1 skeleton
   (16 concept grid). Fill `app_idea`, `app_tone`, `brand_colors` from `AiGuidelines/`; tune
   `concept_directions` to the brand. MUST stay a 4×4 grid — the CLI slices it.
2. `kappmaker spec-template mascot-states --output Assets/mascot/mascot-states-spec.json` — stage-2
   skeleton. Its `states` list MUST have exactly 16 entries in grid order — sliced files are named
   after it. Swap defaults for states the app actually needs (streak, paywall, empty-inbox…); ask
   the user which states they want if unclear.
3. Run `kappmaker create-mascot --spec Assets/mascot/mascot-spec.json --states-spec Assets/mascot/mascot-states-spec.json`.
   Both specs are baselines, not straitjackets — enrich freely within the grid contracts. Plain
   `--prompt "<app idea>" [--tone ...]` works too, using the built-in prompts.

**Agent flow (no TTY)** — when driving this from a coding agent, the interactive picker can't be
used; run two-phase instead:

1. `kappmaker create-mascot --spec ... --grid-only` — generates and saves the concept grid, exits.
2. Show `Assets/mascot/mascot_variations.png` to the user and ask which cell (1-16) they like.
3. `kappmaker create-mascot --spec ... --states-spec ... --choose <n> --yes` — reuses the saved
   grid, extracts cell n, removes background, generates the 16 states, slices and cleans them.

**Flow** (interactive terminal):
1. Generates a 4×4 grid of 16 mascot concepts → opens preview → user picks 1-16 (or R to regenerate;
   optional `5 --zoom 1.1 --gap 3`).
2. Extracts the chosen mascot to `Assets/mascot/mascot.png` + background-removed `mascot_no_bg.png`.
3. Asks to continue, then renders the SAME mascot in 16 states (chosen mascot passed as the
   reference image so identity stays consistent), slices, names each file after its state
   (`states/happy.png`, `states/loading.png`, …) and removes every background.

**Options**:
- `--prompt <text>` — App idea (skips interactive prompt; not needed when both specs given)
- `--tone <text>` — App tone for the concept grid (e.g. "playful and cozy")
- `--spec <path>` / `--states-spec <path>` — Pre-authored stage-1 / stage-2 spec JSON (preferred)
- `--states <names...>` — Custom state names without a spec (topped up to 16 with defaults)
- `--output <dir>` — Output directory (default `Assets/mascot`)
- `--resolution <res>` — 1K, 2K, 4K (default 2K)
- `--skip-states` — Stop after the mascot is chosen
- `--skip-remove-bg` — Keep original backgrounds

**Default states**: happy, sad, excited, thinking, loading, success, error, idle, celebrating,
confused, proud, curious, sleeping, encouraging, waving, love.

**Prerequisites**: `falApiKey` (prompted on first use). No OpenAI key ever.

### mascot-add-state — One more state later

**Syntax**: `kappmaker mascot-add-state --state "<description>" [--mascot <path>] [options]`

Generates a single new state for the existing mascot (default reference:
`Assets/mascot/mascot_no_bg.png`, falls back to `mascot.png`), saves to
`Assets/mascot/states/<slug>.png`, removes the background. Use for states discovered later —
"shopping", "level up", "streak lost". `--spec <path>` accepts a pre-authored single-state spec;
`--skip-remove-bg` and `--output` as above.

### mascot-animate — Animate a state into a looping clip

**Syntax**: `kappmaker mascot-animate --state <name> [--motion "<description>"] [options]`

Turns ONE existing state PNG into a short video clip (image-to-video), saved as MP4 +
looping WebP (WebP conversion needs ffmpeg; skipped gracefully without it).

**Video generation is priced per second — NEVER animate all states.** Animate only the states the
user actually needs (typically 1-3: an onboarding hero, a celebration, maybe loading). Always let
the command show its cost estimate and confirmation; pass `--yes` only when the user already
approved the spend in conversation.

- Default model **seedance-mini** (Seedance 2.0 Mini): ~$0.07/s at 480p, auto duration → a clip ≈ $0.30-0.45. Reliable and cheap.
- `--model ltx` (`fal-ai/ltxv-2/image-to-video/fast`): cheapest at 1080p (~$0.04/s) but the backend has outages — if it fails with "Downstream service error", fall back to seedance-mini.
- `--model seedance` (full Seedance 2.0): ~$0.24/s — reserve for one hero moment, not UI loops.
- `--gif` also emits a looping GIF (READMEs, chats). WebP/GIF conversion requires **ffmpeg on the
  machine** (NOT bundled with kappmaker — `brew install ffmpeg`); without it the MP4 is still saved
  and conversion is skipped with a tip.
- **Format guidance — never put a GIF in the app bundle.** GIF is 3-6× larger than WebP (256
  colors, weak compression) and exists only for marketing surfaces (GitHub README, emails, chat).
  In-app: use the looping **WebP** (~0.5MB per clip); MP4 + player for a full-screen onboarding
  hero. For small always-on UI mascots,
  tweening the static state PNGs app-side is a few KB and usually reads better.
- Transparent source PNGs are auto-flattened onto white before upload (video models have no alpha).
- `--motion` defaults to a per-state preset (happy → gentle bounce, loading → patient sway, …);
  write a custom one for anything specific. `--spec` accepts a pre-authored animation spec
  (`kappmaker spec-template mascot-animation`) — fill `motion`/`mood`, keep the loop rules.
- Output: `Assets/mascot/animations/<state>.mp4` (+ `.webp`).
- Honest guidance for the user: for small in-app "alive" effects, tweening the static state PNGs
  app-side (scale pulse, crossfade) is free and often reads better — reserve video clips for
  onboarding heroes, celebrations, App Store preview material and social posts.

---

## Where this sits in the flow

- **Before this:** **kappmaker-new-app**; `AiGuidelines/` filled in.
- **After this:** use the states in app UI (empty/loading/error screens, onboarding); **kappmaker-screenshots** can feature the mascot in store screenshots; **kappmaker-image-tools** for extra processing.
