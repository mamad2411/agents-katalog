---
name: kappmaker
description: Entry point for the KAppMaker CLI — routes to the right KAppMaker skill. Use when the user mentions kappmaker, or wants to work on a mobile app but which part is not yet clear: creating a new app, Firebase, subscriptions and in-app purchases, Adapty, RevenueCat, App Store Connect, Google Play Console, ASO keywords, logos, mascots, illustrations, app icons, store screenshots, the feature graphic, building and publishing (including shipping iOS without a Mac), version bumps, renaming the package, or configuring the CLI's API keys.
argument-hint: "[command or description]"
---

# KAppMaker CLI

Each area of the CLI is its own skill, so only what you need gets loaded. Pick from the table and
use that skill — do not hand-roll a command a skill already documents.

| The user wants… | Use this skill |
|---|---|
| A new app, a new project, "I have an app idea" | **kappmaker-new-app** |
| Set an API key, configure the CLI, fix a missing credential | **kappmaker-config** |
| Firebase, google-services, auth/analytics | **kappmaker-firebase** |
| Subscription / IAP products, credit packs, price changes | **kappmaker-monetization** |
| Adapty — provider dashboard, entitlements, paywalls | **kappmaker-adapty** |
| RevenueCat — entitlements, offerings, packages | **kappmaker-revenuecat** |
| App Store Connect, iOS listing | **kappmaker-asc** |
| Google Play Console, Android listing, data safety, releases | **kappmaker-gpc** |
| Which keywords to target, ASO research | **kappmaker-aso** |
| What to write in title / subtitle / keywords, per locale | **kappmaker-aso-metadata** |
| The app logo / brand mark | **kappmaker-logo** |
| An app mascot / character and its emotional states | **kappmaker-mascot** |
| Any other image — illustrations, empty states, onboarding art | **kappmaker-image** |
| Edit an existing image — split, remove background, enhance, WebP | **kappmaker-image-tools** |
| App icons, launcher icons | **kappmaker-app-icons** |
| Store screenshots, or screenshots in other languages | **kappmaker-screenshots** |
| The Play feature graphic | **kappmaker-feature-graphic** |
| Build, sign, ship — fastlane, keystore, AAB, upload | **kappmaker-publish** |
| Ship iOS without a Mac (GitHub Actions, TestFlight) | **kappmaker-ios-ci** |
| Bump the version | **kappmaker-version** |
| Rename the package, bundle ID or app name | **kappmaker-refactor** |

Two asks that are easy to misroute:

- **"Re-sync / refresh my prices"** → **kappmaker-monetization**. It owns pricing and points at
  the two push commands (`appstore-monetization-push`, `gpc monetization push`) whose platform
  details live in **kappmaker-asc** / **kappmaker-gpc**.
- **"Take screenshots of my app"** → capturing the app's *real* screens is the project-bundled
  `capture-app-screens` skill, not this CLI. **kappmaker-screenshots** designs *marketing*
  screenshots (and consumes those captures as references).

## The usual journey

Idea → **new-app** → *(interview via the project's own `new-app` skill)* → **firebase** →
**monetization** + a provider (**adapty** / **revenuecat**) → **logo** → **app-icons** → build features →
**asc** / **gpc** → **aso** → **aso-metadata** → **screenshots** + **feature-graphic** →
**version** → **publish**.

Nobody does all of it at once. Each skill ends with what comes before and after it, so if a step
turns out to need something earlier, follow the pointer rather than improvising.

**Chained work stays in one skill.** Shipping is keystore → signed AAB → upload; all three live in
**kappmaker-publish** because they are one flow, not three separate asks. Same for Firebase's five
subcommands (**kappmaker-firebase**) and store setup (**kappmaker-asc** / **kappmaker-gpc**, which
`create` chains automatically).

## Context Gathering — Read `AiGuidelines/` First

**Before running ANY kappmaker command, if the user's request is missing inputs the command needs
(app idea, app name, tagline, brand color, screenshot direction, keywords, target audience, etc.),
read the project's `AiGuidelines/` folder first.** Do not jump straight to asking the user — the
answers are usually already written down in the project.

`AiGuidelines/` is the canonical home for AI-facing planning docs in a KAppMaker project:

- `app-idea.md` — short pitch / one-liner / target audience
- `prd.md` — product requirements (features, screens, user flows)
- `keywords.md` — ASO keyword research output
- `brand.md` / `style.md` — brand voice, primary color, typography (if present)

**Cascade order** (stop at first useful match):

1. `AiGuidelines/*.md` — primary source
2. `README.md` at the project root — usually the elevator pitch
3. Existing ASO metadata under `MobileApp/distribution/ios/appstore_metadata/texts/en-US/`
   (`name.txt`, `subtitle.txt`, `description.txt`) — app name + tagline
4. `Assets/googleplay-config.json` / `Assets/appstore-config.json` — `app.name`, `package_name`

Fill CLI flags from what you find and only prompt for inputs that genuinely have no answer in the
project. For anything inferred, **state the source briefly** ("Using app name 'Masclet' from
`AiGuidelines/app-idea.md`") so the user can correct a wrong inference.

If the folder is missing and the request is rich enough, proceed without prompting. If the folder
is missing AND the request is sparse, offer to create `AiGuidelines/app-idea.md` from a few quick
answers — once written, every future kappmaker command in this project benefits.

## Template-Bundled Agent Skills — the project has its own playbook

The KAppMaker boilerplate ships ~36 agent skills **inside every scaffolded project**: a `skills/`
folder at the repo root, auto-discovered by Claude Code via the `.claude/skills` symlink (other
agents find them through `AGENTS.md` / `GEMINI.md` / `.cursorrules` pointers). The index is
`<project>/skills/README.md`. They cover what this CLI does not: **writing the actual app**.

- **Phase guides** — ordered blueprints: `getting-started` (run locally + MVP, no accounts),
  `integrations` (Firebase, auth), `publishing`, `monetization`, `growth`. Progress lives in
  committed `PROGRESS_FEATURES.md` / `PROGRESS_P1…P5*.md` files — read them first, continue from
  the first unchecked item. The CLI's own 13-step setup uses `PROGRESS_SETUP.md` the same way.
- **Task skills** — one job each: `new-app` (idea → PRD interview), `build-features`,
  `new-screen`, `run-the-app`, `run-quality-gates`, `verify-ui`, `capture-app-screens`, and more.

**Division of labor**: this CLI does scaffolding, AI assets, store/provider automation, builds,
publishing, ASO, versions. Project-bundled skills do in-repo development and the phase journey —
several of them invoke kappmaker commands at the right moment; when following one, let it drive.
When the user asks for in-project work this CLI doesn't cover, check `<project>/skills/README.md`
before improvising. Projects cloned from older templates may have no `skills/` folder — fall back
to normal engineering.

### Starting from a raw idea (interview-first flow)

When the user arrives with only an idea — "build me a habit tracker" — and there's no app name, no
PRD, no project directory, do **not** jump into `kappmaker create`'s prompts, and do **not** invent
the product for them. The bundled **`new-app`** skill owns the idea-to-PRD interview; pre-clone
your job is only the one input scaffolding needs:

1. **Name first**: no name → suggest **3 candidates**, one marked ✅ recommended; derive the app id
   from the pick (`com.<org>.<appname>`, lowercase). Validate PascalCase. "You decide" → take the
   ✅ one and say so.
2. **Scaffold light**: `kappmaker clone <AppName>` (not the full `create`). Phase 1 needs no
   Firebase / store / Adapty accounts — the template ships a mock subscription provider — so
   deferring the 13-step flow keeps the user moving in minutes.
3. **Hand off to the project's `new-app` skill** (`<project>/skills/new-app/SKILL.md`): it
   interviews properly — in batches of 2–3 questions, each with concrete options, a ✅ recommended
   pick, and "decide for me" / "later" escape hatches — writes `AiGuidelines/prd.md` /
   `user_flow.md` / `ui_ux.md`, then hands off to `getting-started`.
4. **Infra when a phase demands it**: Firebase → the `integrations` guide; stores/monetization →
   `publishing` / `monetization` guides. The full `kappmaker create` remains right when the user
   explicitly wants everything provisioned up front.

Follow the interview style, don't just reference it: **never ask an open-ended question when
options will do, batch 2–3 questions max, always mark a ✅ recommended choice, and stop and wait
after each batch.**

## Error Handling

- Missing API keys (fal.ai, OpenAI, imgbb) are prompted inline on first use and saved to config —
  never a fatal exit. For key sources and all config keys → **kappmaker-config**.
- **Firebase auth errors**: run `firebase login` first.
- **`asc` not found**: `brew install asc`. **`adapty` not found**: `npm install -g adapty`.
- **App name validation**: PascalCase, starts uppercase, alphanumeric only.
- Steps that fail on a missing dependency warn and skip rather than aborting the whole flow; if no
  config file exists when `create` runs, `config init` is triggered automatically.
